from flask import Blueprint, render_template, redirect, url_for, flash, request, session, g, current_app, abort, jsonify
from markdown import markdown
from werkzeug.utils import secure_filename
from datetime import datetime
import os
try:
    import pdfplumber  # type: ignore
except Exception:
    pdfplumber = None  # type: ignore
import logging
import time

from . import db, applications_collection
from .models import User, Job, Application
from .utils import allowed_file, evaluate_cv, extract_score, generate_interview_questions, generate_feedback, convert_keys_to_strings, extract_text_from_file, get_allowed_cv_extensions



main = Blueprint('main', __name__)

@main.before_app_request
def load_user():
    user_id = session.get('user_id')
    if user_id:
        g.user = User.query.get(user_id)
    else:
        g.user = None

@main.context_processor
def inject_user():
    return {'user': g.user}

@main.route('/')
def home():
    if g.user is None:
        return redirect(url_for('main.auth'))
    
    # 获取所有职位
    all_jobs = Job.query.filter(Job.user_id != g.user.id).all()
    
    # 获取用户技能
    user_skills = []
    if g.user.cv_file:
        try:
            cv_text = extract_text_from_file(os.path.join(current_app.config['UPLOAD_FOLDER_CV'], g.user.cv_file))
            skill_keywords = ['python', 'java', 'javascript', 'react', 'vue', 'angular', 'node.js', 'sql', 'mongodb', 'docker', 'kubernetes', 'aws', 'azure', 'git', 'html', 'css', 'php', 'c++', 'c#', '.net', 'spring', 'django', 'flask', 'express', 'mysql', 'postgresql', 'redis', 'elasticsearch', 'kafka', 'rabbitmq', 'jenkins', 'ci/cd', 'agile', 'scrum', 'machine learning', 'ai', 'data science', 'analytics', 'devops', 'frontend', 'backend', 'fullstack']
            user_skills = [skill for skill in skill_keywords if skill.lower() in cv_text.lower()]
        except:
            pass
    
    # 计算推荐职位
    recommended_jobs = []
    for job in all_jobs:
        match_score = calculate_job_match(job, user_skills, '')
        if match_score > 30:  # 只推荐匹配度超过30%的职位
            recommended_jobs.append({
                'job': job,
                'match_score': match_score
            })
    
    # 按匹配度排序，取前6个作为推荐
    recommended_jobs.sort(key=lambda x: x['match_score'], reverse=True)
    recommended_jobs = recommended_jobs[:6]
    
    return render_template('snippet_career_list.html', 
                         jobs=all_jobs, 
                         recommended_jobs=recommended_jobs,
                         user_skills=user_skills)

@main.route('/sign', methods=['GET', 'POST'])
def auth():
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'signup':
            # Collect form data
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            company_name = request.form['company_name']
            email = request.form['email']
            phone_number = request.form['phone_number']
            birthday = request.form['birthday']
            password = request.form['password']
            confirm_password = request.form['confirm_password']

            # Validate password match
            if password != confirm_password:
                flash('两次输入的密码不一致。', 'danger')
                return redirect(url_for('main.auth'))

            # Check if the email already exists
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                flash('该邮箱已被注册。', 'danger')
                return redirect(url_for('main.auth'))

            # Create a new user
            user = User(
                first_name=first_name,
                last_name=last_name,
                company_name=company_name,
                email=email,
                phone_number=phone_number,
                birthday=birthday,
                password=password
            )
            db.session.add(user)
            db.session.commit()
            flash('注册成功！现在可以登录。', 'success')
            return redirect(url_for('main.auth'))

        elif action == 'signin':
            # Collect form data
            email = request.form['email']
            password = request.form['password']

            # Check if the user exists
            user = User.query.filter_by(email=email).first()
            if user and user.password == password:
                session['user_id'] = user.id
                flash('登录成功！', 'success')
                return redirect(url_for('main.home'))
            else:
                flash('邮箱或密码错误。', 'danger')
                return redirect(url_for('main.auth'))

    return render_template('sign.html')

@main.route('/logout')
def logout():
    session.clear()
    flash('你已退出登录。', 'success')
    return redirect(url_for('main.auth'))

@main.route('/create_job', methods=['GET', 'POST'])
def create_job():
    if g.user is None:
        flash('请先登录。', 'danger')
        return redirect(url_for('main.auth'))

    if request.method == 'POST':
        title = request.form['title']
        location = request.form['location']
        description = request.form['description']
        salary = request.form['salary']

        new_job = Job(
            title=title,
            location=location,
            description=description,
            salary=salary,
            user_id=g.user.id
        )
        db.session.add(new_job)
        db.session.commit()
        flash('职位创建成功！', 'success')
        return redirect(url_for('main.my_jobs'))

    return render_template('create_job.html')

@main.route('/my_jobs')
def my_jobs():
    if g.user is None:
        flash('请先登录。', 'danger')
        return redirect(url_for('main.auth'))

    jobs = Job.query.filter_by(user_id=g.user.id).all()
    return render_template('my_jobs.html', jobs=jobs)

@main.route('/edit_job/<int:job_id>', methods=['GET', 'POST'])
def edit_job(job_id):
    if g.user is None:
        flash('请先登录。', 'danger')
        return redirect(url_for('main.auth'))

    job = Job.query.get_or_404(job_id)
    if job.user_id != g.user.id:
        abort(403)

    if request.method == 'POST':
        job.title = request.form['title']
        job.location = request.form['location']
        job.description = request.form['description']
        job.salary = request.form['salary']
        db.session.commit()
        flash('职位更新成功！', 'success')
        return redirect(url_for('main.my_jobs'))

    return render_template('edit_job.html', job=job)

@main.route('/delete_job/<int:job_id>', methods=['POST'])
def delete_job(job_id):
    if g.user is None:
        flash('请先登录。', 'danger')
        return redirect(url_for('main.auth'))

    job = Job.query.get_or_404(job_id)
    if job.user_id != g.user.id:
        abort(403)

    db.session.delete(job)
    db.session.commit()
    flash('职位删除成功！', 'success')
    return redirect(url_for('main.my_jobs'))

@main.route('/settings', methods=['GET', 'POST'])
def settings():
    if 'user_id' not in session:
        flash('请先登录。', 'danger')
        return redirect(url_for('main.auth'))

    user = User.query.get(session['user_id'])
    
    if user is None:
        flash('未找到用户。', 'danger')
        return redirect(url_for('main.auth'))

    if request.method == 'POST':
        # Handle General Settings Form Submission
        if 'save_changes' in request.form:
            # Fetching and validating form data
            first_name = request.form.get('first_name')
            last_name = request.form.get('last_name')
            company_name = request.form.get('company_name')
            email = request.form.get('email')
            phone_number = request.form.get('phone_number')
            birthday = request.form.get('birthday')

            # Ensure no required fields are empty
            if not all([first_name, last_name, company_name, email, phone_number, birthday]):
                flash('所有字段均为必填。', 'danger')
                return redirect(url_for('main.settings'))

            # Update user details
            user.first_name = first_name
            user.last_name = last_name
            user.company_name = company_name
            user.email = email
            user.phone_number = phone_number
            user.birthday = birthday

            # Handle Profile Photo Upload
            if 'profile_photo' in request.files:
                profile_photo = request.files['profile_photo']
                if profile_photo and allowed_file(profile_photo.filename, {'jpg', 'jpeg', 'png'}):
                    photo_filename = secure_filename(profile_photo.filename)
                    profile_photo.save(os.path.join(current_app.config['UPLOAD_FOLDER_PHOTOS'], photo_filename))
                    user.profile_photo = photo_filename

            # Commit changes to the database
            try:
                db.session.commit()
                flash('基本信息更新成功！', 'success')
            except Exception as e:
                db.session.rollback()
                logging.error(f"Error updating settings: {e}")
                flash('更新设置时发生错误，请重试。', 'danger')

            return redirect(url_for('main.settings'))

        # Handle CV Upload Form Submission
        if 'upload_cv' in request.form:
            if 'cv_file' in request.files:
                cv_file = request.files['cv_file']
                if cv_file and allowed_file(cv_file.filename, get_allowed_cv_extensions()):
                    original_name = secure_filename(cv_file.filename)
                    name, ext = os.path.splitext(original_name)
                    unique_name = f"{name}_{int(datetime.utcnow().timestamp())}{ext}"
                    dest_path = os.path.join(current_app.config['UPLOAD_FOLDER_CV'], unique_name)

                    # Remove old CV file if present
                    if user.cv_file:
                        old_path = os.path.join(current_app.config['UPLOAD_FOLDER_CV'], user.cv_file)
                        try:
                            if os.path.isfile(old_path):
                                os.remove(old_path)
                        except Exception as e:
                            logging.warning(f"Failed to remove old CV file: {e}")

                    # Save the new file
                    cv_file.save(dest_path)
                    
                    # Verify file was saved and get file info
                    if os.path.exists(dest_path):
                        file_size = os.path.getsize(dest_path)
                        logging.info(f"CV file saved successfully: {dest_path}, size: {file_size} bytes")
                        flash(f'简历上传成功！文件大小: {file_size} 字节', 'success')
                    else:
                        logging.error(f"Failed to save CV file: {dest_path}")
                        flash('简历上传失败，请重试', 'danger')
                        return redirect(url_for('main.settings'))
                    
                    user.cv_file = unique_name
                else:
                    flash('不支持的文件格式', 'danger')
                    return redirect(url_for('main.settings'))
            else:
                flash('请选择要上传的文件', 'danger')
                return redirect(url_for('main.settings'))

            # Commit changes to the database
            try:
                db.session.commit()
                logging.info(f"CV upload committed to database for user {user.id}")
            except Exception as e:
                db.session.rollback()
                logging.error(f"Error committing CV upload to database: {e}")
                flash('数据库更新失败，请重试', 'danger')
                return redirect(url_for('main.settings'))

            return redirect(url_for('main.settings'))

    return render_template('settings.html', user=user)

@main.route('/job/<int:job_id>')
def job_detail(job_id):
    if g.user is None:
        flash('请先登录。', 'danger')
        return redirect(url_for('main.auth'))

    job = Job.query.get_or_404(job_id)
    job.description = markdown(job.description)
    return render_template('job_detail.html', job=job)

@main.route('/apply/<int:job_id>', methods=['GET'])
def apply(job_id):
    if g.user is None:
        flash('You need to sign in first.', 'danger')
        return redirect(url_for('main.auth'))

    job = Job.query.get_or_404(job_id)

    existing_application_sqlite = Application.query.filter_by(user_id=g.user.id, job_id=job_id).first()
    existing_application_mongo = applications_collection.find_one({
        'user_id': str(g.user.id),
        'job_id': str(job_id)
    })

    if existing_application_sqlite or existing_application_mongo:
        flash('你已申请过该职位。', 'alert')
        return redirect(url_for('main.job_detail', job_id=job_id))

    if not g.user.cv_file:
        flash('申请前请在设置中上传你的简历。', 'danger')
        return redirect(url_for('main.settings'))

    cv_path = os.path.join(current_app.config['UPLOAD_FOLDER_CV'], g.user.cv_file)
    if not os.path.isfile(cv_path):
        flash('未找到简历文件，请重新上传。', 'danger')
        return redirect(url_for('main.settings'))

    # Video resumes: allow upload/preview but do not parse for evaluation
    ext = os.path.splitext(g.user.cv_file)[1].lower().lstrip('.')
    if ext in {'mp4', 'webm', 'ogg', 'mov', 'avi', 'mkv'}:
        flash('已上传视频简历，但目前无法自动解析评分。请上传 PDF/DOCX/PNG/JPG 简历用于申请。', 'danger')
        return redirect(url_for('main.settings'))

    try:
        text = extract_text_from_file(cv_path)
    except Exception as e:
        logging.error(f"Failed to process CV: {e}")
        flash('处理简历失败。', 'danger')
        return redirect(url_for('main.job_detail', job_id=job_id))

    match, similarity_score = evaluate_cv(text, job.description)
    if not match:
        flash(f'你的简历与职位要求不匹配。相似度：{similarity_score:.2f}', 'error')
        return redirect(url_for('main.job_detail', job_id=job_id))

    questions = generate_interview_questions(text, job.description)
    session['questions'] = questions
    session['current_question'] = 0
    session['responses'] = {}
    session['job_id'] = job_id
    session['similarity_score'] = similarity_score

    return redirect(url_for('main.interview_questions'))

@main.route('/interview_questions', methods=['GET', 'POST'])
def interview_questions():
    if g.user is None:
        flash('请先登录。', 'danger')
        return redirect(url_for('main.auth'))

    questions = session.get('questions')
    current_question = session.get('current_question', 0)
    responses = session.get('responses', {})

    if request.method == 'POST':
        response = request.form.get('response')
        if response:
            responses[str(current_question)] = response
            session['responses'] = responses
            current_question += 1
            session['current_question'] = current_question

            if current_question >= len(questions):
                return redirect(url_for('main.review_responses'))

    if current_question < len(questions):
        question = questions[current_question]
        return render_template('interview_questions.html', question_number=current_question + 1, question_text=question)
    else:
        return redirect(url_for('main.review_responses'))

@main.route('/review_responses')
def review_responses():
    if g.user is None:
        flash('请先登录。', 'danger')
        return redirect(url_for('main.auth'))

    return render_template('loading.html', next_url = url_for('main.generate_feedbacks'))

@main.route('/generate_feedbacks')
def generate_feedbacks():
    if g.user is None:
        flash('You need to sign in first.', 'danger')
        return redirect(url_for('main.auth'))

    responses = session.get('responses', {})
    questions = session.get('questions', [])
    job_id = session.get('job_id')
    job = Job.query.get_or_404(job_id)
    similarity_score = session.get('similarity_score')

    feedback_list = []
    for idx, response in responses.items():
        question = questions[int(idx)]
        feedback = generate_feedback(question, response, job.description)
        score = extract_score(feedback)
        time.sleep(2)  
        feedback_list.append({
            'question': question,
            'response': response,
            'feedback': feedback,
            'score':score
        })

    new_application = Application(
        user_id=g.user.id,
        job_id=job_id,
        message=similarity_score,
        timestamp=datetime.utcnow(),
        status='待处理'
    )
    db.session.add(new_application)
    db.session.commit()

    application_data = {
        'application_id': str(new_application.id),
        'user_id': str(g.user.id),
        'job_id': str(job_id),
        'responses': convert_keys_to_strings(responses),
        'feedback': feedback_list
    }
    applications_collection.insert_one(application_data)

    flash('申请提交成功！', 'success')
    return redirect(url_for('main.view_applications'))

@main.route('/view_applications')
def view_applications():
    if g.user is None:
        flash('请先登录。', 'danger')
        return redirect(url_for('main.auth'))

    applications = Application.query.filter_by(user_id=g.user.id).all()

    # Fetch job details for each application
    applications_list = []
    status_map = {
        'Pending': '待处理',
        'Accepted': '已接受',
        'Rejected': '已拒绝'
    }
    for app in applications:
        job = Job.query.get(app.job_id)
        localized_status = status_map.get(app.status, app.status)
        applications_list.append({
            'id': app.id,
            'job_title': job.title if job else '未知',
            'application_date': app.timestamp,
            'status': localized_status
        })

    return render_template('view_applications.html', applications=applications_list)

@main.route('/view_candidates/<int:job_id>')
def view_candidates(job_id):
    if g.user is None:
        flash('请先登录。', 'danger')
        return redirect(url_for('main.auth'))

    job = Job.query.get_or_404(job_id)
    if job.user_id != g.user.id:
        abort(403)

    applications = Application.query.filter_by(job_id=job_id).all()
    candidates = []
    for app in applications:
        user = User.query.get(app.user_id)
        candidates.append({
            'application_id': app.id,
            'name': f"{user.first_name} {user.last_name}",
            'email': user.email,
            'phone': user.phone_number,
            'status': app.status,
            'applied_on': app.timestamp
        })

    return render_template('view_candidates.html', candidates=candidates, job=job)

@main.route('/view_interview/<int:application_id>')
def view_interview(application_id):
    if g.user is None:
        flash('You need to sign in first.', 'danger')
        return redirect(url_for('main.auth'))

    application = Application.query.get_or_404(application_id)
    job = Job.query.get(application.job_id)
    if job.user_id != g.user.id:
        abort(403)

    application_data = applications_collection.find_one({'application_id': str(application_id)})
    if not application_data:
        flash('未找到面试数据。', 'danger')
        return redirect(url_for('main.view_candidates', job_id=job.id))

    feedback_list = application_data.get('feedback', [])
    
    # Pass application_id to the template
    return render_template('view_interview.html', feedback_list=feedback_list, applicant=application.user, application_id=application_id)

@main.route('/accept_application/<int:application_id>', methods=['POST'])
def accept_application(application_id):
    if g.user is None:
        flash('请先登录。', 'danger')
        return redirect(url_for('main.auth'))

    application = Application.query.get_or_404(application_id)
    job = Job.query.get(application.job_id)
    if job.user_id != g.user.id:
        abort(403)

    application.status = '已接受'
    db.session.commit()
    flash('已接受该申请。', 'success')
    return redirect(url_for('main.view_candidates', job_id=job.id))

@main.route('/reject_application/<int:application_id>', methods=['POST'])
def reject_application(application_id):
    if g.user is None:
        flash('请先登录。', 'danger')
        return redirect(url_for('main.auth'))

    application = Application.query.get_or_404(application_id)
    job = Job.query.get(application.job_id)
    if job.user_id != g.user.id:
        abort(403)

    application.status = '已拒绝'
    db.session.commit()
    flash('已拒绝该申请。', 'success')
    return redirect(url_for('main.view_candidates', job_id=job.id))

@main.route('/dashboard')
def dashboard():
    if g.user is None:
        flash('请先登录。', 'danger')
        return redirect(url_for('main.auth'))

    jobs = Job.query.filter_by(user_id=g.user.id).all()
    return render_template('dashboard.html', jobs=jobs)

@main.route('/get_job_data/<int:job_id>')
def get_job_data(job_id):
    if g.user is None:
        abort(403)

    job = Job.query.get_or_404(job_id)
    if job.user_id != g.user.id:
        abort(403)

    applications = Application.query.filter_by(job_id=job_id).all()
    candidates = []
    ages = []
    questions_responses = []

    for app in applications:
        candidate = User.query.get(app.user_id)
        feedback_data = applications_collection.find_one({'application_id': str(app.id)})
        total_score = sum(fb['score'] for fb in feedback_data.get('feedback', []) if fb['score'] is not None)

        # Calculate age from birthday
        try:
            birthday = datetime.strptime(candidate.birthday, "%Y-%m-%d")
            today = datetime.now()
            age = today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))
        except ValueError:
            age = None  # or set a default value if the birthday format is incorrect

        if age is not None:
            ages.append(age)

        candidates.append({
            'name': f"{candidate.first_name} {candidate.last_name}",
            'score': total_score,
            'app_id': app.id  # Store app ID for later use
        })

        # Add questions and responses
        if feedback_data:
            for feedback in feedback_data.get('feedback', []):
                # Handle None score values by setting them to 0
                score = feedback.get('score', 0) or 0
                questions_responses.append({
                    'question': feedback.get('question', ''),
                    'response': feedback.get('response', ''),
                    'score': score
                })

    # Sort candidates by score and select the top 3
    top_candidates = sorted(candidates, key=lambda x: x['score'], reverse=True)[:3]

    # Add similarity score for top 3 candidates
    for candidate in top_candidates:
        app = Application.query.get(candidate['app_id'])
        try:
            similarity_score = float(app.message)
        except ValueError:
            similarity_score = 0.0  # Default value if conversion fails

        candidate['similarity'] = similarity_score  # Add similarity score to top candidates

    # Prepare data for both top candidates and all candidates
    all_candidates = [{'name': c['name'], 'totalScore': c['score']} for c in candidates]
    scores = [{'name': c['name'], 'totalScore': c['score'], 'similarity': c.get('similarity', 0)} for c in top_candidates]

    return jsonify({
        'topCandidates': top_candidates,
        'allCandidates': all_candidates,
        'scores': scores,
        'ages': ages,
        'questionsResponses': sorted(questions_responses, key=lambda x: x['score'], reverse=True)
    })

@main.route('/debug/video/<filename>')
def debug_video(filename):
    """Debug route to test video file access"""
    if g.user is None:
        return jsonify({'error': 'Not authenticated'}), 401
    
    cv_path = os.path.join(current_app.config['UPLOAD_FOLDER_CV'], filename)
    
    if not os.path.exists(cv_path):
        return jsonify({'error': 'File not found', 'path': cv_path}), 404
    
    file_info = {
        'filename': filename,
        'path': cv_path,
        'size': os.path.getsize(cv_path),
        'exists': os.path.exists(cv_path),
        'readable': os.access(cv_path, os.R_OK),
        'url': url_for('static', filename=f'uploads/cv/{filename}'),
        'mime_type': 'video/mp4' if filename.endswith('.mp4') else 'unknown'
    }
    
    return jsonify(file_info)

@main.route('/video/<filename>')
def serve_video(filename):
    """专门用于提供视频文件的路由"""
    if g.user is None:
        return jsonify({'error': 'Not authenticated'}), 401
    
    # 安全检查：确保文件名安全
    if not allowed_file(filename):
        return jsonify({'error': 'Invalid filename'}), 400
    
    # 构建文件路径
    video_path = os.path.join(current_app.config['UPLOAD_FOLDER_CV'], filename)
    
    # 检查文件是否存在
    if not os.path.exists(video_path):
        return jsonify({'error': 'Video file not found', 'path': video_path}), 404
    
    # 检查文件是否可读
    if not os.access(video_path, os.R_OK):
        return jsonify({'error': 'Video file not readable'}), 403
    
    # 获取文件大小
    file_size = os.path.getsize(video_path)
    
    # 获取文件扩展名
    file_ext = os.path.splitext(filename)[1].lower()
    
    # 设置正确的MIME类型
    mime_types = {
        '.mp4': 'video/mp4',
        '.mov': 'video/quicktime',
        '.webm': 'video/webm',
        '.ogg': 'video/ogg',
        '.avi': 'video/x-msvideo',
        '.mkv': 'video/x-matroska'
    }
    
    content_type = mime_types.get(file_ext, 'video/mp4')
    
    # 检查是否是下载请求
    is_download = request.args.get('download', 'false').lower() == 'true'
    
    # 返回视频文件
    from flask import send_file, Response
    try:
        return send_file(
            video_path,
            mimetype=content_type,
            as_attachment=is_download,  # 如果是下载请求，设置为附件
            download_name=filename,     # 设置下载文件名
            conditional=True
        )
    except Exception as e:
        logging.error(f"Error serving video {filename}: {e}")
        return jsonify({'error': 'Error serving video file', 'details': str(e)}), 500

@main.route('/download/video/<filename>')
def download_video(filename):
    """专门用于下载视频文件的路由"""
    if g.user is None:
        return jsonify({'error': 'Not authenticated'}), 401
    
    # 安全检查：确保文件名安全
    allowed_extensions = {'mp4', 'mov', 'webm', 'ogg', 'avi', 'mkv'}
    if not allowed_file(filename, allowed_extensions):
        return jsonify({'error': 'Invalid filename'}), 400
    
    # 构建文件路径
    video_path = os.path.join(current_app.config['UPLOAD_FOLDER_CV'], filename)
    
    # 检查文件是否存在
    if not os.path.exists(video_path):
        return jsonify({'error': 'Video file not found', 'path': video_path}), 404
    
    # 检查文件是否可读
    if not os.access(video_path, os.R_OK):
        return jsonify({'error': 'Video file not readable'}), 403
    
    # 获取文件大小
    file_size = os.path.getsize(video_path)
    
    # 获取文件扩展名
    file_ext = os.path.splitext(filename)[1].lower()
    
    # 设置正确的MIME类型
    mime_types = {
        '.mp4': 'video/mp4',
        '.mov': 'video/quicktime',
        '.webm': 'video/webm',
        '.ogg': 'video/ogg',
        '.avi': 'video/x-msvideo',
        '.mkv': 'video/x-matroska'
    }
    
    content_type = mime_types.get(file_ext, 'application/octet-stream')
    
    # 返回文件作为下载
    from flask import send_file, Response
    try:
        # 读取文件内容
        with open(video_path, 'rb') as f:
            file_content = f.read()
        
        # 创建响应
        response = Response(file_content, mimetype=content_type)
        response.headers['Content-Disposition'] = f'attachment; filename="{filename}"'
        response.headers['Content-Length'] = str(file_size)
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        
        return response
        
    except Exception as e:
        logging.error(f"Error downloading video {filename}: {e}")
        return jsonify({'error': 'Error downloading video file', 'details': str(e)}), 500

@main.route('/simple/video/<filename>')
def simple_video_download(filename):
    """最简单的视频下载路由，直接返回文件"""
    if g.user is None:
        return jsonify({'error': 'Not authenticated'}), 401
    
    # 构建文件路径
    video_path = os.path.join(current_app.config['UPLOAD_FOLDER_CV'], filename)
    
    # 检查文件是否存在
    if not os.path.exists(video_path):
        return jsonify({'error': 'Video file not found', 'path': video_path}), 404
    
    try:
        # 使用send_file的最简单方式
        from flask import send_file
        return send_file(
            video_path,
            as_attachment=True,
            download_name=filename
        )
    except Exception as e:
        logging.error(f"Error in simple video download {filename}: {e}")
        return jsonify({'error': 'Download failed', 'details': str(e)}), 500

@main.route('/download/file/<filename>')
def download_file(filename):
    """通用的文件下载路由，支持所有文件类型"""
    if g.user is None:
        return jsonify({'error': 'Not authenticated'}), 401
    
    # 构建文件路径
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER_CV'], filename)
    
    # 检查文件是否存在
    if not os.path.exists(file_path):
        return jsonify({'error': 'File not found', 'path': file_path}), 404
    
    # 检查文件是否可读
    if not os.access(file_path, os.R_OK):
        return jsonify({'error': 'File not readable'}), 403
    
    try:
        # 使用send_file下载文件
        from flask import send_file
        return send_file(
            file_path,
            as_attachment=True,
            download_name=filename
        )
    except Exception as e:
        logging.error(f"Error downloading file {filename}: {e}")
        return jsonify({'error': 'Download failed', 'details': str(e)}), 500

@main.route('/job_search')
def job_search():
    """智能岗位搜索页面"""
    if g.user is None:
        return redirect(url_for('main.auth'))
    
    # 获取所有职位
    jobs = Job.query.all()
    
    # 获取用户技能（从简历中提取）
    user_skills = []
    if g.user.cv_file:
        try:
            cv_text = extract_text_from_file(os.path.join(current_app.config['UPLOAD_FOLDER_CV'], g.user.cv_file))
            # 简单的技能提取逻辑
            skill_keywords = ['python', 'java', 'javascript', 'react', 'vue', 'angular', 'node.js', 'sql', 'mongodb', 'docker', 'kubernetes', 'aws', 'azure', 'git', 'html', 'css', 'php', 'c++', 'c#', '.net', 'spring', 'django', 'flask', 'express', 'mysql', 'postgresql', 'redis', 'elasticsearch', 'kafka', 'rabbitmq', 'jenkins', 'ci/cd', 'agile', 'scrum', 'machine learning', 'ai', 'data science', 'analytics', 'devops', 'frontend', 'backend', 'fullstack']
            user_skills = [skill for skill in skill_keywords if skill.lower() in cv_text.lower()]
        except:
            pass
    
    return render_template('job_search.html', jobs=jobs, user_skills=user_skills)

@main.route('/api/search_jobs', methods=['POST'])
def api_search_jobs():
    """API: 智能搜索职位"""
    if g.user is None:
        return jsonify({'success': False, 'message': '未登录'}), 401
    
    try:
        data = request.get_json()
        search_query = data.get('query', '').lower()
        location_filter = data.get('location', '')
        salary_min = data.get('salary_min', 0)
        salary_max = data.get('salary_max', 999999)
        job_type = data.get('job_type', '')
        experience_level = data.get('experience_level', '')
        
        # 基础查询
        query = Job.query
        
        # 应用过滤器
        if search_query:
            query = query.filter(
                db.or_(
                    Job.title.contains(search_query),
                    Job.description.contains(search_query),
                    Job.requirements.contains(search_query),
                    Job.company_name.contains(search_query)
                )
            )
        
        if location_filter:
            query = query.filter(Job.location.contains(location_filter))
        
        if salary_min > 0:
            query = query.filter(Job.salary >= salary_min)
        
        if salary_max < 999999:
            query = query.filter(Job.salary <= salary_max)
        
        if job_type:
            query = query.filter(Job.job_type == job_type)
        
        if experience_level:
            query = query.filter(Job.experience_level == experience_level)
        
        jobs = query.all()
        
        # 计算匹配度
        job_matches = []
        user_skills = []
        
        # 提取用户技能
        if g.user.cv_file:
            try:
                cv_text = extract_text_from_file(os.path.join(current_app.config['UPLOAD_FOLDER_CV'], g.user.cv_file))
                skill_keywords = ['python', 'java', 'javascript', 'react', 'vue', 'angular', 'node.js', 'sql', 'mongodb', 'docker', 'kubernetes', 'aws', 'azure', 'git', 'html', 'css', 'php', 'c++', 'c#', '.net', 'spring', 'django', 'flask', 'express', 'mysql', 'postgresql', 'redis', 'elasticsearch', 'kafka', 'rabbitmq', 'jenkins', 'ci/cd', 'agile', 'scrum', 'machine learning', 'ai', 'data science', 'analytics', 'devops', 'frontend', 'backend', 'fullstack']
                user_skills = [skill for skill in skill_keywords if skill.lower() in cv_text.lower()]
            except:
                pass
        
        for job in jobs:
            match_score = calculate_job_match(job, user_skills, search_query)
            job_matches.append({
                'id': job.id,
                'title': job.title,
                'company_name': job.company_name,
                'location': job.location,
                'salary': job.salary,
                'job_type': job.job_type,
                'experience_level': job.experience_level,
                'description': job.description[:200] + '...' if len(job.description) > 200 else job.description,
                'match_score': match_score,
                'posted_date': job.created_at.strftime('%Y-%m-%d') if job.created_at else ''
            })
        
        # 按匹配度排序
        job_matches.sort(key=lambda x: x['match_score'], reverse=True)
        
        return jsonify({
            'success': True,
            'jobs': job_matches,
            'total_count': len(job_matches)
        })
        
    except Exception as e:
        logging.error(f"搜索职位时发生错误: {e}")
        return jsonify({
            'success': False,
            'message': '搜索失败，请稍后重试'
        }), 500

@main.route('/api/recommend_jobs')
def api_recommend_jobs():
    """API: 获取推荐职位"""
    if g.user is None:
        return jsonify({'success': False, 'message': '未登录'}), 401
    
    try:
        # 获取用户技能
        user_skills = []
        if g.user.cv_file:
            try:
                cv_text = extract_text_from_file(os.path.join(current_app.config['UPLOAD_FOLDER_CV'], g.user.cv_file))
                skill_keywords = ['python', 'java', 'javascript', 'react', 'vue', 'angular', 'node.js', 'sql', 'mongodb', 'docker', 'kubernetes', 'aws', 'azure', 'git', 'html', 'css', 'php', 'c++', 'c#', '.net', 'spring', 'django', 'flask', 'express', 'mysql', 'postgresql', 'redis', 'elasticsearch', 'kafka', 'rabbitmq', 'jenkins', 'ci/cd', 'agile', 'scrum', 'machine learning', 'ai', 'data science', 'analytics', 'devops', 'frontend', 'backend', 'fullstack']
                user_skills = [skill for skill in skill_keywords if skill.lower() in cv_text.lower()]
            except:
                pass
        
        # 获取所有职位
        all_jobs = Job.query.all()
        
        # 计算匹配度并排序
        job_matches = []
        for job in all_jobs:
            match_score = calculate_job_match(job, user_skills, '')
            if match_score > 30:  # 只推荐匹配度超过30%的职位
                job_matches.append({
                    'id': job.id,
                    'title': job.title,
                    'company_name': job.company_name,
                    'location': job.location,
                    'salary': job.salary,
                    'job_type': job.job_type,
                    'experience_level': job.experience_level,
                    'description': job.description[:150] + '...' if len(job.description) > 150 else job.description,
                    'match_score': match_score,
                    'posted_date': job.created_at.strftime('%Y-%m-%d') if job.created_at else ''
                })
        
        # 按匹配度排序，取前10个
        job_matches.sort(key=lambda x: x['match_score'], reverse=True)
        recommended_jobs = job_matches[:10]
        
        return jsonify({
            'success': True,
            'jobs': recommended_jobs,
            'user_skills': user_skills
        })
        
    except Exception as e:
        logging.error(f"获取推荐职位时发生错误: {e}")
        return jsonify({
            'success': False,
            'message': '获取推荐失败，请稍后重试'
        }), 500

def calculate_job_match(job, user_skills, search_query):
    """计算职位匹配度"""
    score = 0
    
    # 技能匹配 (40%)
    if user_skills:
        # 安全获取职位文本
        job_text_parts = [job.title, job.description]
        if hasattr(job, 'requirements') and job.requirements:
            job_text_parts.append(job.requirements)
        job_text = " ".join(job_text_parts).lower()
        
        matched_skills = sum(1 for skill in user_skills if skill.lower() in job_text)
        skill_score = (matched_skills / len(user_skills)) * 40 if user_skills else 0
        score += skill_score
    
    # 搜索关键词匹配 (30%)
    if search_query:
        job_text_parts = [job.title, job.description]
        if hasattr(job, 'requirements') and job.requirements:
            job_text_parts.append(job.requirements)
        job_text = " ".join(job_text_parts).lower()
        
        query_words = search_query.split()
        matched_words = sum(1 for word in query_words if word in job_text)
        search_score = (matched_words / len(query_words)) * 30 if query_words else 0
        score += search_score
    
    # 职位类型匹配 (15%)
    if hasattr(job, 'job_type') and job.job_type:
        # 检查是否有用户对象和偏好设置
        if hasattr(g, 'user') and g.user and hasattr(g.user, 'preferred_job_type') and g.user.preferred_job_type:
            if job.job_type.lower() == g.user.preferred_job_type.lower():
                score += 15
    
    # 经验级别匹配 (15%)
    if hasattr(job, 'experience_level') and job.experience_level:
        # 检查是否有用户对象和经验级别
        if hasattr(g, 'user') and g.user and hasattr(g.user, 'experience_level') and g.user.experience_level:
            if job.experience_level.lower() == g.user.experience_level.lower():
                score += 15
    
    return min(100, round(score))

@main.route('/demo/job_search')
def demo_job_search():
    """智能搜索演示页面（无需登录）"""
    try:
        # 获取所有职位
        jobs = Job.query.all()
        
        # 模拟用户技能
        demo_skills = ['python', 'javascript', 'react', 'sql', 'git']
        
        # 计算推荐职位
        recommended_jobs = []
        for job in jobs:
            match_score = calculate_job_match(job, demo_skills, '')
            if match_score > 20:  # 降低阈值以显示更多推荐
                recommended_jobs.append({
                    'job': job,
                    'match_score': match_score
                })
        
        # 按匹配度排序，取前6个作为推荐
        recommended_jobs.sort(key=lambda x: x['match_score'], reverse=True)
        recommended_jobs = recommended_jobs[:6]
        
        return render_template('demo_job_search.html', 
                             jobs=jobs, 
                             recommended_jobs=recommended_jobs,
                             user_skills=demo_skills)
    except Exception as e:
        # 如果数据库访问失败，返回模拟数据
        logging.error(f"演示页面错误: {e}")
        demo_skills = ['python', 'javascript', 'react', 'sql', 'git']
        
        # 创建模拟Job对象
        class MockJob:
            def __init__(self, **kwargs):
                for key, value in kwargs.items():
                    setattr(self, key, value)
        
        demo_jobs = [
            MockJob(
                id=1,
                title='Python开发工程师',
                company_name='科技公司A',
                location='北京',
                salary='15000',
                job_type='全职',
                experience_level='中级',
                description='负责Python后端开发，熟悉Django、Flask框架，有数据库设计经验。',
                requirements='Python, Django, Flask, SQL, Git'
            ),
            MockJob(
                id=2,
                title='前端开发工程师',
                company_name='互联网公司B',
                location='上海',
                salary='18000',
                job_type='全职',
                experience_level='初级',
                description='精通JavaScript、React、Vue等前端技术，有良好的UI/UX设计能力。',
                requirements='JavaScript, React, Vue, HTML, CSS'
            ),
            MockJob(
                id=3,
                title='全栈开发工程师',
                company_name='创业公司C',
                location='深圳',
                salary='20000',
                job_type='全职',
                experience_level='高级',
                description='熟悉前后端开发，掌握Python、JavaScript、SQL等技术栈。',
                requirements='Python, JavaScript, SQL, React, Node.js'
            )
        ]
        
        demo_recommended = [
            {'job': demo_jobs[0], 'match_score': 85},
            {'job': demo_jobs[2], 'match_score': 75},
            {'job': demo_jobs[1], 'match_score': 65}
        ]
        
        return render_template('demo_job_search.html', 
                             jobs=demo_jobs, 
                             recommended_jobs=demo_recommended,
                             user_skills=demo_skills)


