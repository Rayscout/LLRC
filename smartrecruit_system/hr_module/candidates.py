from flask import Blueprint, render_template, request, redirect, url_for, flash, g, current_app, abort
from app.models import Job, User, Application, db
from app import applications_collection
from app.sync_service import DataSyncService

candidates_bp = Blueprint('candidates', __name__, url_prefix='/candidates')

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
    
    # 同步申请状态更新
    DataSyncService.sync_application_status_update(application.id)
    
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
    
    # 同步申请状态更新
    DataSyncService.sync_application_status_update(application.id)
    
    flash('申请已拒绝。', 'warning')
    return redirect(url_for('smartrecruit.hr.candidates.view_interview', application_id=application_id))
