"""
LLRC Header Start
文件功能: SmartRecruit 子系统 Python 模块：smartrecruit_system/hr_module/candidates.py
创建时间: 2025-08-28 15:05
创建人: 张宇成
更新记录:
- 2025-08-28 15:35 by 张宇成
LLRC Header End
"""
"""
FILE-HEADER-AUTO-ADDED
文件: smartrecruit_system/hr_module/candidates.py
功能: 通用模块
创建时间: 2025-09-01 14:34
创建人: 苏杰
更新记录:
- 2025-08-30 17:13 by 潘显雨
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, g, current_app, abort, send_file, jsonify
from app.models import Job, User, Application, db
from app import applications_collection
import os

candidates_bp = Blueprint('candidates', __name__, url_prefix='/candidates')

@candidates_bp.route('/')
def index():
    """候选人模块入口，重定向到带数据的列表页"""
    from flask import redirect, url_for, flash
    if g.user is None:
        flash('请先登录。', 'danger')
        return redirect(url_for('common.auth.sign'))
    if not getattr(g.user, 'is_hr', False):
        flash('只有HR用户可以访问此页面。', 'danger')
        return redirect(url_for('common.auth.sign'))
    return redirect(url_for('smartrecruit.hr.dashboard.candidates_list'))

@candidates_bp.route('/view_candidates/<int:job_id>')
def view_candidates(job_id):
    """查看某个职位的候选人"""
    if g.user is None:
        flash('请先登录。', 'danger')
        return redirect(url_for('common.auth.sign'))
    
    if not getattr(g.user, 'is_hr', False):
        flash('只有HR用户才能访问此页面。', 'danger')
        return redirect(url_for('common.auth.sign'))
    
    job = Job.query.get_or_404(job_id)
    if job.user_id != g.user.id:
        abort(403)
    
    # 获取申请了该职位的候选人
    applications = Application.query.filter_by(job_id=job_id).all()
    candidates = []
    
    for app in applications:
        user = User.query.get(app.user_id)
        if user:
            candidates.append({
                'user': user,
                'application': app
            })
    
    return render_template('smartrecruit/hr/view_candidates.html', 
                         job=job, 
                         candidates=candidates)

@candidates_bp.route('/view_interview/<int:application_id>')
def view_interview(application_id):
    """查看面试详情 - 性能优化版本"""
    if g.user is None:
        flash('请先登录。', 'danger')
        return redirect(url_for('common.auth.sign'))
    
    if not getattr(g.user, 'is_hr', False):
        flash('只有HR用户才能访问此页面。', 'danger')
        return redirect(url_for('common.auth.sign'))
    
    try:
        # 使用数据库事务优化查询
        application = Application.query.get_or_404(application_id)
        job = Job.query.get(application.job_id)
        
        if not job or job.user_id != g.user.id:
            abort(403)
        
        user = User.query.get(application.user_id)
        
        # 优化AI面试结果查询 - 添加超时控制
        ai_interview_result = None
        try:
            # 设置查询超时
            ai_interview_result = applications_collection.find_one(
                {
                    'user_id': str(application.user_id),
                    'job_id': str(application.job_id),
                    'type': 'ai_interview_result'
                },
                max_time_ms=3000  # 3秒超时
            )
        except Exception as e:
            print(f"AI面试结果查询失败: {e}")
            ai_interview_result = None
        
        # 优化面试反馈查询 - 添加超时控制
        feedback_list = []
        try:
            feedback_cursor = applications_collection.find(
                {
                    'user_id': str(application.user_id),
                    'job_id': str(application.job_id),
                    'type': 'ai_interview_feedback'
                },
                max_time_ms=3000  # 3秒超时
            ).sort('created_at', -1).limit(10)  # 限制结果数量
            
            for feedback in feedback_cursor:
                feedback_list.append({
                    'question': feedback.get('question', ''),
                    'response': feedback.get('response', ''),
                    'feedback': feedback.get('feedback', ''),
                    'score': feedback.get('score', 0)
                })
        except Exception as e:
            print(f"面试反馈查询失败: {e}")
            feedback_list = []
        
        return render_template('smartrecruit/hr/view_interview.html', 
                             application=application,
                             job=job,
                             user=user,
                             interview_details=ai_interview_result,
                             feedback_list=feedback_list)
                             
    except Exception as e:
        flash(f'加载面试详情失败：{str(e)}', 'danger')
        return redirect(url_for('smartrecruit.hr.dashboard.interviews'))

@candidates_bp.route('/accept_application/<int:application_id>', methods=['POST'])
def accept_application(application_id):
    """接受申请"""
    if g.user is None:
        flash('请先登录。', 'danger')
        return redirect(url_for('common.auth.sign'))
    
    if not getattr(g.user, 'is_hr', False):
        flash('只有HR用户才能访问此页面。', 'danger')
        return redirect(url_for('common.auth.sign'))
    
    application = Application.query.get_or_404(application_id)
    job = Job.query.get(application.job_id)
    
    if not job or job.user_id != g.user.id:
        abort(403)
    
    # 更新申请状态
    application.status = 'accepted'
    db.session.commit()
    
    flash('申请已接受！', 'success')
    return redirect(url_for('smartrecruit.hr.candidates.view_interview', application_id=application_id))

@candidates_bp.route('/reject_application/<int:application_id>', methods=['POST'])
def reject_application(application_id):
    """拒绝申请"""
    if g.user is None:
        flash('请先登录。', 'danger')
        return redirect(url_for('common.auth.sign'))
    
    if not getattr(g.user, 'is_hr', False):
        flash('只有HR用户才能访问此页面。', 'danger')
        return redirect(url_for('common.auth.sign'))
    
    application = Application.query.get_or_404(application_id)
    job = Job.query.get(application.job_id)
    
    if not job or job.user_id != g.user.id:
        abort(403)
    
    # 更新申请状态
    application.status = 'rejected'
    db.session.commit()
    
    flash('申请已拒绝。', 'warning')
    return redirect(url_for('smartrecruit.hr.candidates.view_interview', application_id=application_id))

@candidates_bp.route('/view_candidate_resume/<int:user_id>')
def view_candidate_resume(user_id):
    """查看候选人简历详情"""
    if g.user is None:
        flash('请先登录。', 'danger')
        return redirect(url_for('common.auth.sign'))
    
    if not getattr(g.user, 'is_hr', False):
        flash('只有HR用户才能访问此页面。', 'danger')
        return redirect(url_for('common.auth.sign'))
    
    # 获取候选人信息
    candidate = User.query.get_or_404(user_id)
    
    # 检查是否有简历文件
    has_resume = bool(getattr(candidate, 'cv_file', None))
    
    # 获取候选人的申请记录
    applications = Application.query.filter_by(user_id=user_id).all()
    
    # 获取候选人申请的职位信息
    applied_jobs = []
    for app in applications:
        job = Job.query.get(app.job_id)
        if job:
            applied_jobs.append({
                'job': job,
                'application': app
            })
    
    return render_template('smartrecruit/hr/view_candidate_resume.html',
                         candidate=candidate,
                         has_resume=has_resume,
                         applied_jobs=applied_jobs)

@candidates_bp.route('/download_candidate_resume/<int:user_id>')
def download_candidate_resume(user_id):
    """下载候选人简历文件"""
    if g.user is None:
        abort(401)
    
    if not getattr(g.user, 'is_hr', False):
        abort(403)
    
    # 获取候选人信息
    candidate = User.query.get_or_404(user_id)
    
    # 检查是否有简历文件
    if not getattr(candidate, 'cv_file', None):
        abort(404, description="候选人没有上传简历")
    
    # 构建文件路径
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER_CV'], candidate.cv_file)
    
    # 检查文件是否存在
    if not os.path.exists(file_path):
        abort(404, description="简历文件不存在")
    
    # 获取文件扩展名
    file_ext = candidate.cv_file.rsplit('.', 1)[1].lower() if '.' in candidate.cv_file else ''
    
    # 设置MIME类型
    mime_types = {
        'pdf': 'application/pdf',
        'doc': 'application/msword',
        'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'png': 'image/png',
        'jpg': 'image/jpeg',
        'jpeg': 'image/jpeg',
        'mp4': 'video/mp4',
        'mov': 'video/quicktime',
        'webm': 'video/webm',
        'ogg': 'video/ogg',
        'avi': 'video/x-msvideo',
        'mkv': 'video/x-matroska'
    }
    
    mimetype = mime_types.get(file_ext, 'application/octet-stream')
    
    # 发送文件
    return send_file(
        file_path,
        as_attachment=True,
        download_name=f"简历_{candidate.first_name}_{candidate.last_name}.{file_ext}",
        mimetype=mimetype
    )

@candidates_bp.route('/preview_candidate_resume/<int:user_id>')
def preview_candidate_resume(user_id):
    """预览候选人简历文件（不下载）"""
    if g.user is None:
        abort(401)
    
    if not getattr(g.user, 'is_hr', False):
        abort(403)
    
    # 获取候选人信息
    candidate = User.query.get_or_404(user_id)
    
    # 检查是否有简历文件
    if not getattr(candidate, 'cv_file', None):
        abort(404, description="候选人没有上传简历")
    
    # 构建文件路径
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER_CV'], candidate.cv_file)
    
    # 检查文件是否存在
    if not os.path.exists(file_path):
        abort(404, description="简历文件不存在")
    
    # 获取文件扩展名
    file_ext = candidate.cv_file.rsplit('.', 1)[1].lower() if '.' in candidate.cv_file else ''
    
    # 对于图片和视频文件，直接显示
    if file_ext in ['png', 'jpg', 'jpeg', 'gif', 'mp4', 'mov', 'webm', 'ogg', 'avi', 'mkv']:
        return send_file(file_path)
    
    # 对于文档文件，尝试转换为HTML或PDF进行预览
    # 这里可以根据需要实现文档预览功能
    # 目前先返回下载链接
    return jsonify({
        'message': '文档预览功能开发中，请使用下载功能',
        'download_url': url_for('smartrecruit.hr.candidates.download_candidate_resume', user_id=user_id)
    })

@candidates_bp.route('/get_candidate_info/<int:user_id>')
def get_candidate_info(user_id):
    """获取候选人信息的API接口"""
    if g.user is None:
        return jsonify({'error': '未登录'}), 401
    
    if not getattr(g.user, 'is_hr', False):
        return jsonify({'error': '权限不足'}), 403
    
    # 获取候选人信息
    candidate = User.query.get_or_404(user_id)
    
    # 获取候选人的申请记录
    applications = Application.query.filter_by(user_id=user_id).all()
    
    # 构建候选人信息
    candidate_info = {
        'id': candidate.id,
        'first_name': candidate.first_name,
        'last_name': candidate.last_name,
        'email': candidate.email,
        'phone_number': candidate.phone_number,
        'company_name': candidate.company_name,
        'position': candidate.position,
        'department': candidate.department,
        'skills': candidate.skills,
        'education': candidate.education,
        'experience': candidate.experience,
        'bio': candidate.bio,
        'has_resume': bool(getattr(candidate, 'cv_file', None)),
        'resume_filename': getattr(candidate, 'cv_file', None),
        'resume_download_url': url_for('smartrecruit.hr.candidates.download_candidate_resume', user_id=user_id) if getattr(candidate, 'cv_file', None) else None,
        'resume_preview_url': url_for('smartrecruit.hr.candidates.preview_candidate_resume', user_id=user_id) if getattr(candidate, 'cv_file', None) else None,
        'applications_count': len(applications),
        'applied_jobs': []
    }
    
    # 添加申请的职位信息
    for app in applications:
        job = Job.query.get(app.job_id)
        if job:
            candidate_info['applied_jobs'].append({
                'job_id': job.id,
                'job_title': job.title,
                'company_name': job.company_name,
                'application_status': app.status,
                'application_date': app.timestamp.strftime('%Y-%m-%d %H:%M:%S') if app.timestamp else None,
                'application_message': app.message
            })
    
    return jsonify(candidate_info)

@candidates_bp.route('/schedule_interview/<int:application_id>', methods=['GET', 'POST'])
def schedule_interview(application_id):
    """安排面试 - 支持HR手动设置AI面试状态"""
    if g.user is None:
        flash('请先登录。', 'danger')
        return redirect(url_for('common.auth.sign'))
    
    if not getattr(g.user, 'is_hr', False):
        flash('只有HR用户才能访问此页面。', 'danger')
        return redirect(url_for('common.auth.sign'))
    
    try:
        # 获取申请信息
        application = Application.query.get_or_404(application_id)
        job = Job.query.get(application.job_id)
        
        if not job or job.user_id != g.user.id:
            abort(403)
        
        candidate = User.query.get(application.user_id)
        
        # 获取AI面试状态
        ai_interview_passed = False
        try:
            interview_details = applications_collection.find_one(
                {
                    'user_id': str(application.user_id),
                    'job_id': str(application.job_id),
                    'type': 'ai_interview_result'
                },
                max_time_ms=3000
            )
            
            if interview_details and interview_details.get('status') == 'passed':
                ai_interview_passed = True
                
        except Exception as e:
            print(f"AI面试结果查询失败: {e}")
            ai_interview_passed = False
        
        if request.method == 'POST':
            try:
                from datetime import datetime
                from app.models import InterviewSchedule
                
                # 获取表单数据
                interview_date = datetime.strptime(request.form['interview_date'], '%Y-%m-%d').date()
                start_time = datetime.strptime(request.form['start_time'], '%H:%M').time()
                end_time = datetime.strptime(request.form['end_time'], '%H:%M').time()
                interview_type = request.form['interview_type']
                location = request.form['location']
                interviewer_name = request.form['interviewer_name']
                notes = request.form.get('notes', '')
                
                # 处理HR手动设置的AI面试状态
                hr_ai_interview_override = 'hr_ai_interview_override' in request.form
                if hr_ai_interview_override:
                    ai_interview_passed = request.form.get('ai_interview_passed') == '1'
                    hr_ai_interview_notes = request.form.get('hr_ai_interview_notes', '')
                else:
                    hr_ai_interview_notes = None
                
                # 创建面试安排
                interview_schedule = InterviewSchedule(
                    application_id=application_id,
                    candidate_id=candidate.id,
                    job_id=job.id,
                    hr_id=g.user.id,
                    interview_date=interview_date,
                    start_time=start_time,
                    end_time=end_time,
                    interview_type=interview_type,
                    location=location,
                    interviewer_name=interviewer_name,
                    notes=notes,
                    ai_interview_passed=ai_interview_passed,
                    hr_ai_interview_override=hr_ai_interview_override,
                    hr_ai_interview_notes=hr_ai_interview_notes,
                    status='scheduled'
                )
                
                db.session.add(interview_schedule)
                db.session.commit()
                
                # 更新申请状态
                application.status = 'interview_scheduled'
                db.session.commit()
                
                # 发送通知
                try:
                    send_interview_notification(interview_schedule)
                except Exception as e:
                    print(f"通知发送失败，但不影响面试安排: {e}")
                
                flash('面试安排成功！已通知候选人。', 'success')
                return redirect(url_for('smartrecruit.hr.dashboard.interviews'))
                
            except Exception as e:
                db.session.rollback()
                flash(f'面试安排失败：{str(e)}', 'danger')
        
        return render_template('smartrecruit/hr/schedule_interview.html',
                             application=application,
                             job=job,
                             candidate=candidate,
                             ai_interview_passed=ai_interview_passed)
                             
    except Exception as e:
        flash(f'加载页面失败：{str(e)}', 'danger')
        return redirect(url_for('smartrecruit.hr.dashboard.interviews'))

def send_interview_notification(interview_schedule):
    """发送面试通知"""
    try:
        from datetime import datetime
        
        # 插入通知到MongoDB
        notification_data = {
            'user_id': str(interview_schedule.candidate_id),
            'job_id': str(interview_schedule.job_id),
            'type': 'interview_notification',
            'title': '面试安排通知',
            'message': '请你进行线下面试',
            'interview_date': interview_schedule.interview_date.strftime('%Y-%m-%d'),
            'start_time': interview_schedule.start_time.strftime('%H:%M'),
            'end_time': interview_schedule.end_time.strftime('%H:%M'),
            'interview_type': interview_schedule.interview_type,
            'location': interview_schedule.location,
            'interviewer_name': interview_schedule.interviewer_name,
            'notes': interview_schedule.notes,
            'created_at': datetime.utcnow(),
            'read': False
        }
        
        applications_collection.insert_one(notification_data)
        
        # 更新面试安排的通知状态
        interview_schedule.notification_sent = True
        interview_schedule.notification_sent_at = datetime.utcnow()
        db.session.commit()
        
    except Exception as e:
        print(f"发送面试通知失败: {e}")
        raise e

@candidates_bp.route('/get_ai_interview_candidates')
def get_ai_interview_candidates():
    """获取通过AI面试的候选人列表 - 性能优化版本"""
    if g.user is None:
        return jsonify({'error': '未登录'}), 401
    
    if not getattr(g.user, 'is_hr', False):
        return jsonify({'error': '权限不足'}), 403
    
    try:
        # 获取当前HR发布的职位
        hr_jobs = Job.query.filter_by(user_id=g.user.id).all()
        job_ids = [str(job.id) for job in hr_jobs]
        
        if not job_ids:
            return jsonify([])
        
        # 查询通过AI面试的候选人
        ai_candidates = []
        try:
            cursor = applications_collection.find(
                {
                    'job_id': {'$in': job_ids},
                    'type': 'ai_interview_result',
                    'status': 'passed'
                },
                max_time_ms=5000
            ).limit(50)
            
            for doc in cursor:
                ai_candidates.append({
                    'user_id': doc.get('user_id'),
                    'job_id': doc.get('job_id'),
                    'score': doc.get('score', 0),
                    'feedback': doc.get('feedback', ''),
                    'interview_date': doc.get('created_at')
                })
                
        except Exception as e:
            print(f"查询AI面试候选人失败: {e}")
            return jsonify([])
        
        return jsonify(ai_candidates)
        
    except Exception as e:
        print(f"获取AI面试候选人失败: {e}")
        return jsonify([])
