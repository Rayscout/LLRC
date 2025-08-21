from flask import Blueprint, render_template, request, redirect, url_for, flash, g, current_app, jsonify
import os
import logging
from app.models import Job, Application, db
from app.utils import evaluate_cv, generate_interview_questions, generate_feedback, extract_text_from_resume, extract_text_from_file
from app import applications_collection
from datetime import datetime

applications_bp = Blueprint('applications', __name__, url_prefix='/applications')

@applications_bp.route('/apply/<int:job_id>', methods=['GET'])
def apply(job_id):
    """申请职位"""
    if g.user is None:
        flash('You need to sign in first.', 'danger')
        return redirect(url_for('common.auth.sign'))

    job = Job.query.get_or_404(job_id)

    # 检查是否已经申请过
    existing_application_sqlite = Application.query.filter_by(user_id=g.user.id, job_id=job_id).first()
    existing_application_mongo = None
    try:
        existing_application_mongo = applications_collection.find_one({
            'user_id': str(g.user.id),
            'job_id': str(job_id)
        })
    except Exception:
        pass

    if existing_application_sqlite or existing_application_mongo:
        flash('你已申请过该职位。', 'alert')
        return redirect(url_for('smartrecruit.candidate.jobs.job_detail', job_id=job_id))

    if not g.user.cv_file:
        flash('申请前请在设置中上传你的简历。', 'danger')
        return redirect(url_for('smartrecruit.candidate.profile.settings'))

    # 提取简历文本
    text = ''
    try:
        if getattr(g.user, 'cv_data', None):
            text = extract_text_from_resume(g.user.cv_data, g.user.cv_file or '')
        else:
            cv_path = os.path.join(current_app.config['UPLOAD_FOLDER_CV'], g.user.cv_file)
            if not os.path.isfile(cv_path):
                flash('未找到简历文件，请重新上传。', 'danger')
                return redirect(url_for('smartrecruit.candidate.profile.settings'))
            
            # 视频简历：允许上传/预览但不解析评分
            ext = os.path.splitext(g.user.cv_file)[1].lower().lstrip('.')
            if ext in {'mp4', 'webm', 'ogg', 'mov', 'avi', 'mkv'}:
                flash('已上传视频简历，但目前无法自动解析评分。请上传 PDF/DOCX/PNG/JPG 简历用于申请。', 'danger')
                return redirect(url_for('smartrecruit.candidate.profile.settings'))
            
            text = extract_text_from_file(cv_path)
    except Exception as e:
        logging.error(f"Failed to process CV: {e}")
        flash('处理简历失败。', 'danger')
        return redirect(url_for('smartrecruit.candidate.jobs.job_detail', job_id=job_id))

    # 评估简历匹配度
    match, similarity_score = evaluate_cv(text, job.description)
    if not match:
        flash(f'你的简历与职位要求不匹配。相似度：{similarity_score:.2f}', 'error')
        return redirect(url_for('smartrecruit.candidate.jobs.job_detail', job_id=job_id))

    # 生成面试问题
    questions = generate_interview_questions(text, job.description)
    session['questions'] = questions
    session['current_question'] = 0
    session['responses'] = {}
    session['job_id'] = job_id
    session['similarity_score'] = similarity_score

    return redirect(url_for('smartrecruit.candidate.applications.interview_questions'))

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
        # SQLite
        application = Application(
            user_id=g.user.id,
            job_id=job_id,
            status='completed',
            message=f'相似度: {similarity_score:.2f}%, 面试得分: {final_score:.1f}%'
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

    # 从SQLite获取申请
    applications = Application.query.filter_by(user_id=g.user.id).all()
    
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
