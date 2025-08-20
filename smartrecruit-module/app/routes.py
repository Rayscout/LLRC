from flask import Blueprint, render_template, redirect, url_for, flash, request, session, g, current_app, abort, jsonify
from flask_login import login_user, logout_user, current_user
from markdown import markdown
from werkzeug.utils import secure_filename
from datetime import datetime
import os
import pdfplumber  # type: ignore
import logging
import time
from functools import wraps

from . import db, applications_collection
from .models import User, Job, Application
from .utils import allowed_file, evaluate_cv, extract_score, generate_interview_questions, generate_feedback, convert_keys_to_strings

main = Blueprint('main', __name__)

def login_required(f):
    """自定义的登录要求装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user:
            flash('请先登录以访问此页面。', 'warning')
            return redirect(url_for('main.auth'))
        return f(*args, **kwargs)
    return decorated_function

@main.before_app_request
def load_user():
    pass  # Flask-Login 已经处理了用户加载

@main.context_processor
def inject_user():
    return {'user': current_user}

@main.route('/')
def home():
    if not current_user.is_authenticated:
        return redirect(url_for('main.auth'))
    
    # 如果是HR用户，重定向到HR仪表盘
    if current_user.is_hr:
        return redirect(url_for('main.hr_dashboard'))
    
    # 普通用户显示职位列表
    jobs = Job.query.filter(Job.user_id != current_user.id).all()
    return render_template('snippet_career_list.html', jobs=jobs)

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
                flash('密码不匹配。', 'danger')
                return redirect(url_for('main.auth'))

            # Check if the email already exists
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                flash('此邮箱已存在账户。', 'danger')
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
            flash('注册成功！您现在可以登录了。', 'success')
            return redirect(url_for('main.auth'))

        elif action == 'signin':
            # Collect form data
            email = request.form['email']
            password = request.form['password']

            # Check if the user exists
            user = User.query.filter_by(email=email).first()
            if user and user.password == password:
                login_user(user)
                flash('登录成功！', 'success')
                return redirect(url_for('main.home'))
            else:
                flash('邮箱或密码无效。', 'danger')
                return redirect(url_for('main.auth'))

    return render_template('sign.html')

@main.route('/logout')
def logout():
    logout_user()
    flash('您已退出登录。', 'success')
    return redirect(url_for('main.auth'))

@main.route('/create_job', methods=['GET', 'POST'])
@login_required
def create_job():

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
            user_id=current_user.id
        )
        db.session.add(new_job)
        db.session.commit()
        flash('职位创建成功！', 'success')
        return redirect(url_for('main.my_jobs'))

    return render_template('create_job.html')

@main.route('/publish_recruitment', methods=['GET', 'POST'])
@login_required
def publish_recruitment():
    # 检查用户是否为HR
    if not current_user.is_hr:
        flash('只有HR用户才能发布招聘启事。', 'danger')
        return redirect(url_for('main.home'))

    # 检查是否为编辑模式
    edit_job_id = request.args.get('edit')
    job_to_edit = None
    
    if edit_job_id:
        try:
            job_to_edit = Job.query.get_or_404(int(edit_job_id))
            # 检查权限
            if job_to_edit.user_id != current_user.id:
                flash('您没有权限编辑此招聘启事。', 'danger')
                return redirect(url_for('main.my_jobs'))
        except ValueError:
            flash('无效的招聘启事ID。', 'danger')
            return redirect(url_for('main.my_jobs'))

    if request.method == 'POST':
        try:
            # 获取表单数据
            title = request.form['title']
            location = request.form['location']
            description = request.form['description']
            salary = request.form['salary']
            positions_needed = int(request.form['positions_needed'])
            min_age = int(request.form['min_age']) if request.form['min_age'] else None
            max_age = int(request.form['max_age']) if request.form['max_age'] else None
            education_requirement = request.form['education_requirement']
            experience_years = int(request.form['experience_years']) if request.form['experience_years'] else None
            skills_required = request.form['skills_required']
            benefits = request.form['benefits']
            contact_email = request.form['contact_email']
            contact_phone = request.form['contact_phone']
            application_deadline = datetime.strptime(request.form['application_deadline'], '%Y-%m-%d') if request.form['application_deadline'] else None
            job_type = request.form['job_type']
            department = request.form['department']

            if edit_job_id and job_to_edit:
                # 更新现有招聘启事
                job_to_edit.title = title
                job_to_edit.location = location
                job_to_edit.description = description
                job_to_edit.salary = salary
                job_to_edit.positions_needed = positions_needed
                job_to_edit.min_age = min_age
                job_to_edit.max_age = max_age
                job_to_edit.education_requirement = education_requirement
                job_to_edit.experience_years = experience_years
                job_to_edit.skills_required = skills_required
                job_to_edit.benefits = benefits
                job_to_edit.contact_email = contact_email
                job_to_edit.contact_phone = contact_phone
                job_to_edit.application_deadline = application_deadline
                job_to_edit.job_type = job_type
                job_to_edit.department = department
                
                db.session.commit()
                flash('招聘启事更新成功！', 'success')
            else:
                # 创建新的招聘启事
                new_recruitment = Job(
                    title=title,
                    location=location,
                    description=description,
                    salary=salary,
                    user_id=current_user.id,
                    positions_needed=positions_needed,
                    min_age=min_age,
                    max_age=max_age,
                    education_requirement=education_requirement,
                    experience_years=experience_years,
                    skills_required=skills_required,
                    benefits=benefits,
                    contact_email=contact_email,
                    contact_phone=contact_phone,
                    application_deadline=application_deadline,
                    job_type=job_type,
                    department=department
                )
                
                db.session.add(new_recruitment)
                db.session.commit()
                flash('招聘启事发布成功！', 'success')
            
            return redirect(url_for('main.my_jobs'))
            
        except ValueError as e:
            flash('请检查输入的数据格式是否正确。', 'danger')
        except Exception as e:
            flash('操作失败，请稍后重试。', 'danger')
            db.session.rollback()

    return render_template('publish_recruitment.html', job=job_to_edit, is_edit=bool(edit_job_id))

@main.route('/my_jobs')
@login_required
def my_jobs():
    jobs = Job.query.filter_by(user_id=current_user.id).all()
    now = datetime.utcnow()
    return render_template('my_jobs.html', jobs=jobs, now=now)

@main.route('/edit_job/<int:job_id>', methods=['GET', 'POST'])
@login_required
def edit_job(job_id):

    job = Job.query.get_or_404(job_id)
    if job.user_id != current_user.id:
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
@login_required
def delete_job(job_id):

    job = Job.query.get_or_404(job_id)
    if job.user_id != current_user.id:
        abort(403)

    db.session.delete(job)
    db.session.commit()
    flash('职位删除成功！', 'success')
    return redirect(url_for('main.my_jobs'))

@main.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    user = current_user

    if request.method == 'POST':
        # Handle General Settings Form Submission
        if 'save_changes' in request.form:
            # Fetching and validating form data
            first_name = request.form.get('first_name')
            last_name = request.form.get('last_name')
            company_name = request.form.get('company_name')
            position = request.form.get('position')
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
            user.position = position
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
                flash('常规设置更新成功！', 'success')
            except Exception as e:
                db.session.rollback()
                logging.error(f"Error updating settings: {e}")
                flash('更新设置时发生错误，请重试。', 'danger')

            return redirect(url_for('main.settings'))

        # Handle CV Upload Form Submission
        if 'upload_cv' in request.form:
            if 'cv_file' in request.files:
                cv_file = request.files['cv_file']
                if cv_file and allowed_file(cv_file.filename, {'pdf'}):
                    cv_filename = secure_filename(cv_file.filename)
                    cv_file.save(os.path.join(current_app.config['UPLOAD_FOLDER_CV'], cv_filename))
                    user.cv_file = cv_filename

            # Commit changes to the database
            try:
                db.session.commit()
                flash('简历上传成功！', 'success')
            except Exception as e:
                db.session.rollback()
                logging.error(f"Error uploading CV: {e}")
                flash('上传简历时发生错误，请重试。', 'danger')

            return redirect(url_for('main.settings'))

    return render_template('settings.html', user=user)

@main.route('/job/<int:job_id>')
@login_required
def job_detail(job_id):

    job = Job.query.get_or_404(job_id)
    job.description = markdown(job.description)
    return render_template('job_detail.html', job=job)

@main.route('/apply/<int:job_id>', methods=['GET'])
@login_required
def apply(job_id):

    job = Job.query.get_or_404(job_id)

    existing_application_sqlite = Application.query.filter_by(user_id=current_user.id, job_id=job_id).first()
    existing_application_mongo = applications_collection.find_one({
        'user_id': str(current_user.id),
        'job_id': str(job_id)
    })

    if existing_application_sqlite or existing_application_mongo:
        flash('您已申请过此职位。', 'alert')
        return redirect(url_for('main.job_detail', job_id=job_id))

    if not current_user.cv_file:
        flash('请在设置中上传您的简历。', 'danger')
        return redirect(url_for('main.settings'))

    cv_path = os.path.join(current_app.config['UPLOAD_FOLDER_CV'], current_user.cv_file)
    if not os.path.isfile(cv_path):
        flash('简历文件未找到。请重新上传。', 'danger')
        return redirect(url_for('main.settings'))

    try:
        with pdfplumber.open(cv_path) as pdf:
            text = ''.join(page.extract_text() for page in pdf.pages if page.extract_text())
    except Exception as e:
        logging.error(f"Failed to process CV: {e}")
        flash('简历处理失败。', 'danger')
        return redirect(url_for('main.job_detail', job_id=job_id))

    match, similarity_score = evaluate_cv(text, job.description)
    if not match:
        flash(f'您的简历不符合职位要求。相似度分数：{similarity_score:.2f}', 'error')
        return redirect(url_for('main.job_detail', job_id=job_id))

    questions = generate_interview_questions(text, job.description)
    session['questions'] = questions
    session['current_question'] = 0
    session['responses'] = {}
    session['job_id'] = job_id
    session['similarity_score'] = similarity_score

    return redirect(url_for('main.interview_questions'))

@main.route('/interview_questions', methods=['GET', 'POST'])
@login_required
def interview_questions():

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
@login_required
def review_responses():

    return render_template('loading.html', next_url = url_for('main.generate_feedbacks'))

@main.route('/generate_feedbacks')
@login_required
def generate_feedbacks():

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
        user_id=current_user.id,
        job_id=job_id,
        message=similarity_score,
        timestamp=datetime.utcnow(),
        status='Pending'
    )
    db.session.add(new_application)
    db.session.commit()

    application_data = {
        'application_id': str(new_application.id),
        'user_id': str(current_user.id),
        'job_id': str(job_id),
        'responses': convert_keys_to_strings(responses),
        'feedback': feedback_list
    }
    applications_collection.insert_one(application_data)

    flash('申请提交成功！', 'success')
    return redirect(url_for('main.view_applications'))

@main.route('/view_applications')
@login_required
def view_applications():

    applications = Application.query.filter_by(user_id=current_user.id).all()

    # Fetch job details for each application
    applications_list = []
    for app in applications:
        job = Job.query.get(app.job_id)
        applications_list.append({
            'id': app.id,
            'job_title': job.title if job else '未知',
            'application_date': app.timestamp,
            'status': app.status
        })

    return render_template('view_applications.html', applications=applications_list)

@main.route('/view_candidates/<int:job_id>')
@login_required
def view_candidates(job_id):

    job = Job.query.get_or_404(job_id)
    if job.user_id != current_user.id:
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
@login_required
def view_interview(application_id):

    application = Application.query.get_or_404(application_id)
    job = Job.query.get(application.job_id)
    if job.user_id != current_user.id:
        abort(403)

    application_data = applications_collection.find_one({'application_id': str(application_id)})
    if not application_data:
        flash('面试数据未找到。', 'danger')
        return redirect(url_for('main.view_candidates', job_id=job.id))

    feedback_list = application_data.get('feedback', [])
    
    # Pass application_id to the template
    return render_template('view_interview.html', feedback_list=feedback_list, applicant=application.user, application_id=application_id)

@main.route('/accept_application/<int:application_id>', methods=['POST'])
@login_required
def accept_application(application_id):

    application = Application.query.get_or_404(application_id)
    job = Job.query.get(application.job_id)
    if job.user_id != current_user.id:
        abort(403)

    application.status = 'Accepted'
    db.session.commit()
    flash('申请已接受。', 'success')
    return redirect(url_for('main.view_candidates', job_id=job.id))

@main.route('/reject_application/<int:application_id>', methods=['POST'])
@login_required
def reject_application(application_id):

    application = Application.query.get_or_404(application_id)
    job = Job.query.get(application.job_id)
    if job.user_id != current_user.id:
        abort(403)

    application.status = 'Rejected'
    db.session.commit()
    flash('申请已拒绝。', 'success')
    return redirect(url_for('main.view_candidates', job_id=job.id))

@main.route('/dashboard')
@login_required
def dashboard():

    jobs = Job.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', jobs=jobs)

@main.route('/get_job_data/<int:job_id>')
@login_required
def get_job_data(job_id):

    job = Job.query.get_or_404(job_id)
    if job.user_id != current_user.id:
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

@main.route('/hr_dashboard')
@login_required
def hr_dashboard():
    """HR仪表板页面"""
    if not current_user.is_hr:
        flash('您没有权限访问此页面', 'error')
        return redirect(url_for('main.home'))
    
    # 这里可以添加数据查询逻辑
    # 示例数据
    dashboard_data = {
        'total_candidates': 150,
        'interviews_scheduled': 25,
        'offers_made': 8,
        'hires_completed': 5,
        'funnel_data': {
            'applied': 150,
            'screened': 120,
            'interviewed': 80,
            'hired': 25
        },
        'recent_activities': []
    }
    
    return render_template('hr_dashboard.html', **dashboard_data)

@main.route('/hr_candidates')
@login_required
def hr_candidates():
    """HR候选人管理页面"""
    if not current_user.is_hr:
        flash('您没有权限访问此页面', 'error')
        return redirect(url_for('main.home'))
    
    # 这里可以添加候选人数据查询逻辑
    candidates = []
    
    return render_template('hr_candidates.html', candidates=candidates)

@main.route('/hr_interviews')
@login_required
def hr_interviews():
    """HR面试安排页面"""
    if not current_user.is_hr:
        flash('您没有权限访问此页面', 'error')
        return redirect(url_for('main.home'))
    
    # 这里可以添加面试数据查询逻辑
    interviews = []
    
    return render_template('hr_interviews.html', interviews=interviews)

@main.route('/hr_reports')
@login_required
def hr_reports():
    """HR数据报告页面"""
    if not current_user.is_hr:
        flash('您没有权限访问此页面', 'error')
        return redirect(url_for('main.home'))
    
    # 这里可以添加报告数据查询逻辑
    
    return render_template('hr_reports.html')

@main.route('/hr_insights')
@login_required
def hr_insights():
    """HR AI洞察页面"""
    if not current_user.is_hr:
        flash('您没有权限访问此页面', 'error')
        return redirect(url_for('main.home'))
    
    return render_template('hr_insights.html')
