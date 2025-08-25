from flask import Blueprint, render_template, request, redirect, url_for, flash, g, current_app, jsonify, session
from werkzeug.utils import secure_filename
import os
import logging
from app.models import Job, Application, User, db
from app.utils import (
    evaluate_cv,
    generate_interview_questions,
    generate_feedback,
    extract_text_from_resume,
    extract_text_from_file,
    allowed_file,
    get_allowed_cv_extensions,
)
from app.utils import _gemini_generate  # 使用 Gemini，避免走 HF 降级
from app import applications_collection
from datetime import datetime
from sqlalchemy import text
from .candidate_ai import update_user_skills_from_resume

applications_bp = Blueprint('applications', __name__, url_prefix='/applications')

@applications_bp.route('/pre_apply/<int:job_id>', methods=['GET', 'POST'])
def pre_apply(job_id):
    """预申请：若有简历则直接申请；否则提供上传界面"""
    if g.user is None:
        flash('请先登录。', 'danger')
        return redirect(url_for('common.auth.sign'))

    job = Job.query.get_or_404(job_id)

    # 已有简历，直接进入申请流程
    if getattr(g.user, 'cv_file', None):
        return redirect(url_for('smartrecruit.candidate.applications.apply', job_id=job_id))

    if request.method == 'POST':
        file = request.files.get('cv_file')
        if not file or not file.filename:
            flash('请选择简历文件。', 'danger')
            return redirect(url_for('smartrecruit.candidate.applications.pre_apply', job_id=job_id))

        allowed_extensions = get_allowed_cv_extensions()
        if not allowed_file(file.filename, allowed_extensions):
            flash(f'不支持的文件格式。支持：{", ".join(allowed_extensions)}', 'danger')
            return redirect(url_for('smartrecruit.candidate.applications.pre_apply', job_id=job_id))

        try:
            filename = secure_filename(file.filename)
            upload_path = current_app.config['UPLOAD_FOLDER_CV']
            filepath = os.path.join(upload_path, filename)
            os.makedirs(upload_path, exist_ok=True)
            file.save(filepath)

            ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
            video_exts = {'mp4', 'webm', 'ogg', 'mov', 'avi', 'mkv'}

            cv_data = None
            if ext not in video_exts:
                try:
                    file.stream.seek(0)
                    cv_data = file.read()
                except Exception:
                    cv_data = None

            g.user.cv_file = filename
            g.user.cv_data = cv_data
            db.session.commit()

            # 基于AI自动解析技能并保存
            try:
                parsed_skills = update_user_skills_from_resume(g.user, cv_data or b'', filename)
                if parsed_skills:
                    flash('已基于简历自动更新技能标签。', 'success')
            except Exception as e:
                current_app.logger.warning(f'AI skill extraction failed: {e}')

            flash('简历上传成功！', 'success')
            return redirect(url_for('smartrecruit.candidate.applications.apply', job_id=job_id))
        except Exception as e:
            current_app.logger.error(f'上传简历失败: {e}')
            flash('上传简历失败，请稍后重试。', 'danger')
            return redirect(url_for('smartrecruit.candidate.applications.pre_apply', job_id=job_id))

    return render_template('smartrecruit/candidate/upload_resume_apply.html', job=job)

@applications_bp.route('/withdraw/<int:application_id>', methods=['POST'])
def withdraw_application(application_id):
    """撤销申请：仅允许撤销本人申请，状态改为 Withdrawn"""
    if g.user is None:
        flash('请先登录。', 'danger')
        return redirect(url_for('common.auth.sign'))

    app_rec = Application.query.filter_by(id=application_id, user_id=g.user.id).first()
    if not app_rec:
        flash('未找到该申请或无权限。', 'danger')
        return redirect(url_for('smartrecruit.candidate.applications.my_applications'))

    try:
        app_rec.status = 'Withdrawn'
        app_rec.message = '用户已撤销申请'
        db.session.commit()
        flash('已撤销该申请。', 'success')
    except Exception as e:
        logging.error(f"撤销申请失败: {e}")
        flash('撤销失败，请稍后重试。', 'danger')

    return redirect(url_for('smartrecruit.candidate.applications.my_applications'))

@applications_bp.route('/virtual_interview', methods=['GET'])
def virtual_interview():
    """AI 虚拟面试（前端界面，提供API在同文件中）"""
    if g.user is None:
        flash('请先登录。', 'danger')
        return redirect(url_for('common.auth.sign'))

    return render_template('smartrecruit/candidate/virtual_interview.html')

@applications_bp.route('/api/virtual_interview/start', methods=['GET'])
def api_vi_start():
    """返回基于简历/资料动态生成的问题列表。"""
    if g.user is None:
        return jsonify({'success': False, 'message': '请先登录'}), 401
    try:
        # 获取简历文本，若没有则根据资料拼接
        cv_text = ''
        if getattr(g.user, 'cv_data', None) and getattr(g.user, 'cv_file', None):
            try:
                cv_text = extract_text_from_resume(g.user.cv_data, g.user.cv_file) or ''
            except Exception:
                cv_text = ''
        if not cv_text:
            cv_text = f"姓名:{g.user.first_name} {g.user.last_name}\n公司:{g.user.company_name}\n职位:{g.user.position or ''}\n简介:{g.user.bio or ''}\n经验:{g.user.experience or ''}\n教育:{g.user.education or ''}\n技能:{g.user.skills or ''}"
        job_desc = request.args.get('job_desc', '')

        # 强制优先使用 Gemini，避免走 HF
        prompt = (
            "基于以下候选人简历与职位描述，用中文生成5道不重复的结构化面试问题。\n"
            "每道题尽量具体，长度不超过40字。只输出JSON数组，数组元素为字符串，不要任何额外文字。\n"
            f"简历:\n{cv_text}\n职位描述:\n{job_desc}\n输出:"
        )
        questions = None
        gem = _gemini_generate(prompt, max_tokens=600)
        if gem:
            import json, re
            text = gem.strip()
            # 去掉markdown代码块围栏
            text = text.replace('```json', '').replace('```', '').strip()
            # 优先尝试提取方括号JSON
            m = re.search(r"\[[\s\S]*\]", text)
            if m:
                candidate = m.group(0)
                try:
                    parsed = json.loads(candidate)
                    if isinstance(parsed, list):
                        questions = [str(x).strip().strip('"\'') for x in parsed if str(x).strip()]
                except Exception:
                    questions = None
            # 若仍未解析，按行切分并过滤噪声
            if not questions:
                lines = [ln.strip('- ').strip() for ln in text.splitlines() if ln.strip()]
                filtered = [ln for ln in lines if ln not in ('[',']','```json','```')]
                if filtered:
                    questions = filtered

        if not questions:
            # 退回到旧的通用生成（内部仍可能降级），再取前5
            questions = generate_interview_questions(cv_text, job_desc)
            questions = questions[:5] if isinstance(questions, list) else []
        else:
            questions = questions[:5]
        return jsonify({'success': True, 'questions': questions})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@applications_bp.route('/api/virtual_interview/score', methods=['POST'])
def api_vi_score():
    """对单题作答给出反馈和（文本中包含）评分。"""
    if g.user is None:
        return jsonify({'success': False, 'message': '请先登录'}), 401
    try:
        data = request.get_json(silent=True) or {}
        q = data.get('question', '')
        a = data.get('answer', '')
        job_desc = data.get('job_desc', '')
        if not q or not a:
            return jsonify({'success': False, 'message': '缺少问题或答案'}), 400
        # 先用 Gemini 直接打分
        prompt = (
            "使用中文，对候选人的回答给出简洁、可执行的反馈，并在最后单独一行输出‘评分：X/10’。\n"
            f"问题：{q}\n回答：{a}\n职位描述：{job_desc}\n反馈："
        )
        fb = _gemini_generate(prompt, max_tokens=400)
        feedback = (fb.strip() if fb else None) or generate_feedback(q, a, job_desc)
        return jsonify({'success': True, 'feedback': feedback})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@applications_bp.route('/virtual_feedback', methods=['GET'])
def virtual_feedback():
    """AI 虚拟面试反馈（仅前端界面，不接入API）"""
    if g.user is None:
        flash('请先登录。', 'danger')
        return redirect(url_for('common.auth.sign'))

    return render_template('smartrecruit/candidate/virtual_feedback.html')

@applications_bp.route('/apply/<int:job_id>', methods=['GET', 'POST'])
def apply(job_id):
    """申请职位：可使用已有简历或上传新简历，创建申请并跳转到“我的申请”。"""
    if g.user is None:
        flash('请先登录。', 'danger')
        return redirect(url_for('common.auth.sign'))

    job = Job.query.get_or_404(job_id)

    # 检查是否有活跃的申请（未撤销的申请）
    existing_active_application = Application.query.filter_by(
        user_id=g.user.id, 
        job_id=job_id, 
        is_active=True
    ).first()
    
    if existing_active_application:
        flash('你已申请过该职位，请等待处理结果。', 'info')
        return redirect(url_for('smartrecruit.candidate.applications.my_applications'))

    if request.method == 'GET':
        return render_template(
            'smartrecruit/candidate/apply_resume.html',
            job=job,
            has_saved_cv=bool(getattr(g.user, 'cv_file', None)),
            saved_cv_filename=getattr(g.user, 'cv_file', '')
        )

    # POST: 处理表单
    use_saved = request.form.get('use_saved') == 'on'
    note = request.form.get('note', '').strip()
    uploaded = request.files.get('cv_file')

    cv_filename_to_use = getattr(g.user, 'cv_file', None) if use_saved else None

    if uploaded and uploaded.filename:
        filename = secure_filename(uploaded.filename)
        if not allowed_file(filename, { 'pdf','doc','docx','png','jpg','jpeg' }):
            flash('不支持的文件类型，请上传 PDF/DOC/DOCX/PNG/JPG。', 'danger')
            return redirect(request.url)
        # 保存文件
        name_root, ext = os.path.splitext(filename)
        unique_name = f"u{g.user.id}_j{job_id}_{int(datetime.utcnow().timestamp())}{ext}"
        save_dir = current_app.config['UPLOAD_FOLDER_CV']
        os.makedirs(save_dir, exist_ok=True)
        save_path = os.path.join(save_dir, unique_name)
        uploaded.save(save_path)
        # 记录到用户资料，作为最新简历
        g.user.cv_file = unique_name
        db.session.commit()
        cv_filename_to_use = unique_name

    if not cv_filename_to_use:
        flash('请勾选使用已保存的简历或上传新简历。', 'warning')
        return redirect(request.url)

    # 创建申请记录
    try:
        message = note or f'已提交简历: {cv_filename_to_use}'
        application = Application(
            user_id=g.user.id,
            job_id=job_id,
            status='submitted',
            message=message,
            is_active=True
        )
        db.session.add(application)
        db.session.commit()

        # 可选写入 Mongo
        try:
            applications_collection.insert_one({
                'user_id': str(g.user.id),
                'job_id': str(job_id),
                'message': message,
                'created_at': datetime.utcnow()
            })
        except Exception:
            pass

        flash('申请已提交！', 'success')
        return redirect(url_for('smartrecruit.candidate.applications.my_applications'))
    except Exception as e:
        logging.error(f"保存申请失败: {e}")
        db.session.rollback()
        flash('保存申请失败，请稍后重试。', 'danger')
        return redirect(url_for('smartrecruit.candidate.jobs.job_detail', job_id=job_id))
@applications_bp.route('/interview_questions', methods=['GET', 'POST'])
def interview_questions():
    """面试问题页面"""
    if g.user is None:
        flash('请先登录。', 'danger')
        return redirect(url_for('common.auth.sign'))

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
                return redirect(url_for('smartrecruit.candidate.applications.review_responses'))

    if current_question < len(questions):
        question = questions[current_question]
        return render_template('smartrecruit/candidate/interview_questions.html', 
                             question_number=current_question + 1, 
                             question_text=question)
    else:
        return redirect(url_for('smartrecruit.candidate.applications.review_responses'))

@applications_bp.route('/review_responses')
def review_responses():
    """回顾回答页面"""
    if g.user is None:
        flash('请先登录。', 'danger')
        return redirect(url_for('common.auth.sign'))

    return render_template('smartrecruit/candidate/loading.html', 
                         next_url=url_for('smartrecruit.candidate.applications.generate_feedbacks'))

@applications_bp.route('/generate_feedbacks')
def generate_feedbacks():
    """生成反馈"""
    if g.user is None:
        flash('You need to sign in first.', 'danger')
        return redirect(url_for('common.auth.sign'))

    responses = session.get('responses', {})
    questions = session.get('questions', [])
    job_id = session.get('job_id')
    similarity_score = session.get('similarity_score', 0)

    if not all([responses, questions, job_id]):
        flash('面试数据不完整，请重新开始。', 'danger')
        return redirect(url_for('smartrecruit.candidate.jobs.job_list'))

    # 生成反馈
    feedbacks = []
    total_score = 0
    
    for i, question in enumerate(questions):
        response = responses.get(str(i), '')
        feedback = generate_feedback(question, response)
        feedbacks.append({
            'question': question,
            'response': response,
            'feedback': feedback
        })
        
        # 简单评分逻辑
        if response and len(response.strip()) > 10:
            total_score += 1
    
    final_score = (total_score / len(questions)) * 100 if questions else 0

    # 保存到数据库
    try:
        # SQLite：若已存在活跃申请，则更新；否则创建
        application = Application.query.filter_by(user_id=g.user.id, job_id=job_id, is_active=True).first()
        if application:
            application.status = 'Completed'
            application.message = f'相似度: {similarity_score:.2f}%, 面试得分: {final_score:.1f}%'
        else:
            application = Application(
                user_id=g.user.id,
                job_id=job_id,
                status='Completed',
                message=f'相似度: {similarity_score:.2f}%, 面试得分: {final_score:.1f}%',
                is_active=True
            )
            db.session.add(application)
        db.session.commit()
        
        # MongoDB (可选)
        try:
            mongo_data = {
                'user_id': str(g.user.id),
                'job_id': str(job_id),
                'questions': questions,
                'responses': responses,
                'feedbacks': feedbacks,
                'similarity_score': similarity_score,
                'final_score': final_score,
                'created_at': datetime.utcnow()
            }
            applications_collection.insert_one(mongo_data)
        except Exception as e:
            logging.warning(f"Failed to save to MongoDB: {e}")
            
    except Exception as e:
        logging.error(f"Failed to save application: {e}")
        flash('保存申请失败，但面试已完成。', 'warning')

    # 清理session
    session.pop('questions', None)
    session.pop('current_question', None)
    session.pop('responses', None)
    session.pop('job_id', None)
    session.pop('similarity_score', None)

    return render_template('smartrecruit/candidate/interview_results.html', 
                         feedbacks=feedbacks,
                         final_score=final_score,
                         similarity_score=similarity_score)

@applications_bp.route('/my_applications')
def my_applications():
    """我的申请列表"""
    if g.user is None:
        flash('请先登录。', 'danger')
        return redirect(url_for('common.auth.sign'))

    # 从SQLite获取活跃的申请
    applications = Application.query.filter_by(user_id=g.user.id, is_active=True).order_by(Application.timestamp.desc()).all()
    
    # 获取职位信息
    applications_with_jobs = []
    for app in applications:
        job = Job.query.get(app.job_id)
        if job:
            applications_with_jobs.append({
                'application': app,
                'job': job
            })
    
    return render_template('smartrecruit/candidate/view_applications.html', 
                         applications=applications_with_jobs)

@applications_bp.route('/withdraw/<int:application_id>', methods=['POST', 'GET'])
def withdraw(application_id: int):
    """撤销当前用户的一条申请（软撤销：设置is_active为False，允许重新申请）。"""
    if g.user is None:
        flash('请先登录。', 'danger')
        return redirect(url_for('common.auth.sign'))

    app_obj = Application.query.filter_by(id=application_id, user_id=g.user.id, is_active=True).first()
    if app_obj is None:
        flash('未找到该申请或无权限操作。', 'warning')
        return redirect(url_for('smartrecruit.candidate.applications.my_applications'))

    try:
        # 软删除：设置is_active为False，保留历史记录
        app_obj.is_active = False
        app_obj.status = 'Withdrawn'
        app_obj.message = f'{app_obj.message} (已撤销)'
        db.session.commit()
        
        # 可选：从 Mongo 清理对应记录（忽略异常）
        try:
            applications_collection.delete_many({'user_id': str(g.user.id), 'job_id': str(app_obj.job_id)})
        except Exception:
            pass
            
        # AJAX 请求直接返回 JSON，页面立即更新而不重定向
        if request.args.get('ajax') == '1' or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': True})
        flash('已撤销该申请，现在可以重新申请该职位。', 'success')
    except Exception as e:
        db.session.rollback()
        logging.error(f'撤销申请失败: {e}')
        if request.args.get('ajax') == '1' or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': False, 'message': '撤销失败，请稍后重试。'}), 500
        flash('撤销失败，请稍后重试。', 'danger')
    return redirect(url_for('smartrecruit.candidate.applications.my_applications'))

@applications_bp.route('/view_applications')
def view_applications():
    """查看申请列表"""
    if g.user is None:
        flash('请先登录。', 'danger')
        return redirect(url_for('common.auth.sign'))
    
    # 这里可以添加获取用户申请列表的逻辑
    # 目前返回模拟数据
    return render_template('smartrecruit/candidate/view_applications.html', user=g.user)

@applications_bp.route('/apply_job/<int:job_id>', methods=['GET', 'POST'])
def apply_job(job_id):
    """申请职位"""
    if g.user is None:
        if request.headers.get('Content-Type') == 'application/json':
            return jsonify({'success': False, 'message': '请先登录'}), 401
        flash('请先登录。', 'danger')
        return redirect(url_for('common.auth.sign'))
    
    # 检查职位是否存在
    job = Job.query.get(job_id)
    if not job:
        if request.headers.get('Content-Type') == 'application/json':
            return jsonify({'success': False, 'message': '职位不存在'}), 404
        flash('职位不存在。', 'danger')
        return redirect(url_for('smartrecruit.candidate.jobs.search'))
    
    if request.method == 'POST':
        try:
            # 检查是否已经申请过这个职位
            existing_application = Application.query.filter_by(
                user_id=g.user.id, 
                job_id=job_id
            ).first()
            
            if existing_application:
                if existing_application.is_active:
                    if request.headers.get('Content-Type') == 'application/json':
                        return jsonify({'success': False, 'message': '您已经申请过这个职位'}), 400
                    flash('您已经申请过这个职位。', 'warning')
                    return redirect(url_for('smartrecruit.candidate.applications.my_applications'))
                else:
                    # 如果之前撤销过，重新激活申请
                    existing_application.is_active = True
                    existing_application.status = 'Pending'
                    existing_application.timestamp = datetime.utcnow()
                    existing_application.message = '重新申请'
                    db.session.commit()
                    
                    if request.headers.get('Content-Type') == 'application/json':
                        return jsonify({'success': True, 'message': '申请已重新提交'})
                    flash('申请已重新提交！', 'success')
                    return redirect(url_for('smartrecruit.candidate.applications.my_applications'))
            
            # 创建新的申请
            new_application = Application(
                user_id=g.user.id,
                job_id=job_id,
                message=f'申请职位：{job.title}',
                status='Pending'
            )
            
            db.session.add(new_application)
            db.session.commit()
            
            if request.headers.get('Content-Type') == 'application/json':
                return jsonify({'success': True, 'message': '申请提交成功'})
            flash('职位申请已提交！', 'success')
            return redirect(url_for('smartrecruit.candidate.applications.my_applications'))
            
        except Exception as e:
            db.session.rollback()
            logging.error(f'申请职位失败: {e}')
            if request.headers.get('Content-Type') == 'application/json':
                return jsonify({'success': False, 'message': '申请失败，请稍后重试'}), 500
            flash('申请失败，请稍后重试。', 'danger')
            return redirect(url_for('smartrecruit.candidate.jobs.search'))
    
    # GET 请求显示申请表单
    return render_template('smartrecruit/candidate/apply_job.html', job_id=job_id, user=g.user, job=job)

def get_user_applications_count(user_id):
    """获取用户申请数量"""
    try:
        # 获取活跃的申请数量
        count = Application.query.filter_by(user_id=user_id, is_active=True).count()
        return count
    except Exception:
        return 0
