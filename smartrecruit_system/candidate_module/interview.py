from flask import Blueprint, render_template, request, jsonify, session, g
from app.models import User, Job, Application
from app.utils import generate_interview_questions, generate_feedback
import json
import uuid
from datetime import datetime

interview_bp = Blueprint('interview', __name__, url_prefix='/interview')

# 模拟面试会话存储
INTERVIEW_SESSIONS = {}

@interview_bp.route('/')
def interview_dashboard():
    """AI虚拟面试仪表板"""
    if g.user is None:
        return jsonify({'error': '请先登录'}), 401
    
    # 初始化available_jobs变量
    available_jobs = []
    
    try:
        # 获取用户的申请记录
        applications = Application.query.filter_by(user_id=g.user.id).all()
        
        # 获取可进行面试的职位
        for app in applications:
            if app.status in ['Pending', 'Reviewing']:
                job = Job.query.get(app.job_id)
                if job:
                    available_jobs.append({
                        'job': job,
                        'application': app
                    })
        
        # 如果没有申请记录，提供一些示例职位用于演示
        if not available_jobs:
            # 创建一些示例职位用于演示
            demo_jobs = [
                {
                    'job': type('Job', (), {
                        'id': 1,
                        'title': 'Python开发工程师',
                        'company': '科技公司A',
                        'location': '北京',
                        'job_type': '全职',
                        'description': '负责公司核心产品的后端开发，要求熟悉Python、Django、MySQL等技术栈。'
                    })(),
                    'application': type('Application', (), {
                        'status': 'Pending',
                        'created_at': datetime.now()
                    })()
                },
                {
                    'job': type('Job', (), {
                        'id': 2,
                        'title': '前端开发工程师',
                        'company': '互联网公司B',
                        'location': '上海',
                        'job_type': '全职',
                        'description': '负责公司产品的前端开发，要求熟悉React、Vue、JavaScript等技术。'
                    })(),
                    'application': type('Application', (), {
                        'status': 'Reviewing',
                        'created_at': datetime.now()
                    })()
                }
            ]
            available_jobs = demo_jobs
    
    except Exception as e:
        # 如果出现异常，使用演示数据
        demo_jobs = [
            {
                'job': type('Job', (), {
                    'id': 1,
                    'title': 'Python开发工程师',
                    'company': '科技公司A',
                    'location': '北京',
                    'job_type': '全职',
                    'description': '负责公司核心产品的后端开发，要求熟悉Python、Django、MySQL等技术栈。'
                })(),
                'application': type('Application', (), {
                    'status': 'Pending',
                    'created_at': datetime.now()
                })()
            },
            {
                'job': type('Job', (), {
                    'id': 2,
                    'title': '前端开发工程师',
                    'company': '互联网公司B',
                    'location': '上海',
                    'job_type': '全职',
                    'description': '负责公司产品的前端开发，要求熟悉React、Vue、JavaScript等技术。'
                })(),
                'application': type('Application', (), {
                    'status': 'Reviewing',
                    'created_at': datetime.now()
                })()
            }
        ]
        available_jobs = demo_jobs
    
    return render_template('smartrecruit/candidate/interview_dashboard.html',
                         user=g.user,
                         available_jobs=available_jobs)

@interview_bp.route('/start/<int:job_id>', methods=['POST'])
def start_interview(job_id):
    """开始AI虚拟面试"""
    if g.user is None:
        return jsonify({'error': '请先登录'}), 401
    
    try:
        job = Job.query.get_or_404(job_id)
        
        # 获取用户简历内容
        cv_text = ""
        if g.user.cv_data:
            from app.utils import extract_text_from_resume
            cv_text = extract_text_from_resume(g.user.cv_data, g.user.cv_file or "resume.pdf")
        
        if not cv_text:
            # 如果没有简历文件，使用用户资料
            cv_text = f"""
            姓名: {g.user.first_name} {g.user.last_name}
            公司: {g.user.company_name}
            职位: {g.user.position or '未指定'}
            简介: {g.user.bio or '无'}
            经验: {g.user.experience or '无'}
            教育: {g.user.education or '无'}
            技能: {g.user.skills or '无'}
            """
        
        # 生成面试问题
        questions = generate_interview_questions(cv_text, job.description)
        
        # 创建面试会话
        session_id = str(uuid.uuid4())
        INTERVIEW_SESSIONS[session_id] = {
            'user_id': g.user.id,
            'job_id': job_id,
            'questions': questions,
            'current_question': 0,
            'answers': [],
            'start_time': datetime.now(),
            'status': 'active'
        }
        
        return jsonify({
            'success': True,
            'session_id': session_id,
            'question': questions[0],
            'total_questions': len(questions)
        })
        
    except Exception as e:
        return jsonify({'error': f'开始面试失败: {str(e)}'}), 500

@interview_bp.route('/session/<session_id>')
def interview_session(session_id):
    """面试会话页面"""
    if g.user is None:
        return jsonify({'error': '请先登录'}), 401
    
    if session_id not in INTERVIEW_SESSIONS:
        return jsonify({'error': '面试会话不存在'}), 404
    
    session_data = INTERVIEW_SESSIONS[session_id]
    if session_data['user_id'] != g.user.id:
        return jsonify({'error': '无权访问此面试会话'}), 403
    
    job = Job.query.get(session_data['job_id'])
    current_question = session_data['questions'][session_data['current_question']]
    
    return render_template('smartrecruit/candidate/interview_session.html',
                         user=g.user,
                         job=job,
                         session_id=session_id,
                         current_question=current_question,
                         question_number=session_data['current_question'] + 1,
                         total_questions=len(session_data['questions']))

@interview_bp.route('/answer/<session_id>', methods=['POST'])
def submit_answer(session_id):
    """提交面试答案"""
    if g.user is None:
        return jsonify({'error': '请先登录'}), 401
    
    if session_id not in INTERVIEW_SESSIONS:
        return jsonify({'error': '面试会话不存在'}), 404
    
    session_data = INTERVIEW_SESSIONS[session_id]
    if session_data['user_id'] != g.user.id:
        return jsonify({'error': '无权访问此面试会话'}), 403
    
    try:
        answer = request.form.get('answer', '').strip()
        if not answer:
            return jsonify({'error': '答案不能为空'}), 400
        
        # 获取当前问题
        current_question = session_data['questions'][session_data['current_question']]
        
        # 生成反馈
        job = Job.query.get(session_data['job_id'])
        feedback = generate_feedback(current_question, answer, job.description)
        
        # 保存答案和反馈
        session_data['answers'].append({
            'question': current_question,
            'answer': answer,
            'feedback': feedback,
            'timestamp': datetime.now()
        })
        
        # 移动到下一题
        session_data['current_question'] += 1
        
        # 检查是否完成
        if session_data['current_question'] >= len(session_data['questions']):
            session_data['status'] = 'completed'
            session_data['end_time'] = datetime.now()
            
            # 计算总分
            total_score = calculate_interview_score(session_data['answers'])
            session_data['total_score'] = total_score
            
            return jsonify({
                'success': True,
                'completed': True,
                'total_score': total_score,
                'message': '面试完成！'
            })
        else:
            next_question = session_data['questions'][session_data['current_question']]
            return jsonify({
                'success': True,
                'completed': False,
                'feedback': feedback,
                'next_question': next_question,
                'question_number': session_data['current_question'] + 1
            })
        
    except Exception as e:
        return jsonify({'error': f'提交答案失败: {str(e)}'}), 500

@interview_bp.route('/result/<session_id>')
def interview_result(session_id):
    """面试结果页面"""
    if g.user is None:
        return jsonify({'error': '请先登录'}), 401
    
    if session_id not in INTERVIEW_SESSIONS:
        return jsonify({'error': '面试会话不存在'}), 404
    
    session_data = INTERVIEW_SESSIONS[session_id]
    if session_data['user_id'] != g.user.id:
        return jsonify({'error': '无权访问此面试会话'}), 403
    
    if session_data['status'] != 'completed':
        return jsonify({'error': '面试尚未完成'}), 400
    
    job = Job.query.get(session_data['job_id'])
    
    return render_template('smartrecruit/candidate/interview_result.html',
                         user=g.user,
                         job=job,
                         session_data=session_data)

@interview_bp.route('/history')
def interview_history():
    """面试历史记录"""
    if g.user is None:
        return jsonify({'error': '请先登录'}), 401
    
    # 获取用户的面试历史
    user_sessions = []
    for session_data in INTERVIEW_SESSIONS.values():
        if session_data['user_id'] == g.user.id and session_data['status'] == 'completed':
            # 添加职位信息
            job = Job.query.get(session_data['job_id'])
            if job:
                session_data['job_title'] = job.title
                session_data['company_name'] = job.company
            else:
                session_data['job_title'] = '未知职位'
                session_data['company_name'] = '未知公司'
            user_sessions.append(session_data)
    
    # 按时间排序
    user_sessions.sort(key=lambda x: x['end_time'], reverse=True)
    
    return render_template('smartrecruit/candidate/interview_history.html',
                         user=g.user,
                         sessions=user_sessions)

def calculate_interview_score(answers):
    """计算面试总分"""
    if not answers:
        return 0
    
    total_score = 0
    for answer_data in answers:
        feedback = answer_data['feedback']
        # 从反馈中提取分数
        if '评分：' in feedback:
            try:
                score_text = feedback.split('评分：')[-1].split('/')[0]
                score = int(score_text)
                total_score += score
            except:
                total_score += 5  # 默认分数
        else:
            total_score += 5  # 默认分数
    
    return round(total_score / len(answers), 1)
