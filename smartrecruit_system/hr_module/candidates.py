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
    """查看面试详情"""
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
    
    user = User.query.get(application.user_id)
    
    # 从MongoDB获取面试详情
    interview_details = None
    try:
        interview_details = applications_collection.find_one({
            'user_id': str(application.user_id),
            'job_id': str(application.job_id)
        })
    except Exception:
        pass
    
    return render_template('smartrecruit/hr/view_interview.html', 
                         application=application,
                         job=job,
                         user=user,
                         interview_details=interview_details)

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
