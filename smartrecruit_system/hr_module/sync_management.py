"""
数据同步管理模块
让HR可以查看同步状态和管理数据同步
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, g, current_app, jsonify
import logging
from app.sync_service import DataSyncService
from app.models import Job, Application, User, db

sync_management_bp = Blueprint('sync_management', __name__, url_prefix='/sync')

@sync_management_bp.route('/dashboard')
def sync_dashboard():
    """数据同步仪表盘"""
    if g.user is None:
        flash('请先登录。', 'danger')
        return redirect(url_for('common.auth.sign'))
    
    if not getattr(g.user, 'is_hr', False):
        flash('只有HR用户才能访问此页面。', 'danger')
        return redirect(url_for('common.auth.sign'))
    
    try:
        # 获取同步状态
        sync_status = DataSyncService.get_sync_status()
        
        # 获取最近的同步活动
        recent_sync_activities = get_recent_sync_activities()
        
        return render_template('smartrecruit/hr/sync_dashboard.html',
                             sync_status=sync_status,
                             recent_activities=recent_sync_activities)
    except Exception as e:
        logging.error(f"加载同步仪表盘失败: {e}")
        flash('加载同步仪表盘时出现错误，请稍后重试。', 'danger')
        return render_template('smartrecruit/hr/sync_dashboard.html',
                             sync_status={},
                             recent_activities=[])

@sync_management_bp.route('/status')
def sync_status():
    """获取详细同步状态"""
    if g.user is None:
        return jsonify({'error': '请先登录'}), 401
    
    if not getattr(g.user, 'is_hr', False):
        return jsonify({'error': '只有HR用户才能访问此页面'}), 403
    
    try:
        sync_status = DataSyncService.get_sync_status()
        return jsonify(sync_status)
    except Exception as e:
        logging.error(f"获取同步状态失败: {e}")
        return jsonify({'error': str(e)}), 500

@sync_management_bp.route('/force_sync', methods=['POST'])
def force_sync():
    """强制同步所有数据"""
    if g.user is None:
        return jsonify({'error': '请先登录'}), 401
    
    if not getattr(g.user, 'is_hr', False):
        return jsonify({'error': '只有HR用户才能访问此页面'}), 403
    
    try:
        # 执行强制同步
        success = DataSyncService.force_sync_all()
        
        if success:
            return jsonify({
                'success': True,
                'message': '强制同步完成'
            })
        else:
            return jsonify({
                'success': False,
                'message': '强制同步失败'
            }), 500
            
    except Exception as e:
        logging.error(f"强制同步失败: {e}")
        return jsonify({
            'success': False,
            'message': f'强制同步失败: {str(e)}'
        }), 500

@sync_management_bp.route('/sync_job/<int:job_id>', methods=['POST'])
def sync_specific_job(job_id):
    """同步特定职位"""
    if g.user is None:
        return jsonify({'error': '请先登录'}), 401
    
    if not getattr(g.user, 'is_hr', False):
        return jsonify({'error': '只有HR用户才能访问此页面'}), 403
    
    try:
        # 检查职位是否属于当前HR
        job = Job.query.get_or_404(job_id)
        if job.user_id != g.user.id:
            return jsonify({'error': '无权操作此职位'}), 403
        
        # 执行同步
        success = DataSyncService.sync_job_to_candidates(job_id)
        
        if success:
            return jsonify({
                'success': True,
                'message': f'职位 "{job.title}" 同步完成'
            })
        else:
            return jsonify({
                'success': False,
                'message': f'职位 "{job.title}" 同步失败'
            }), 500
            
    except Exception as e:
        logging.error(f"同步职位 {job_id} 失败: {e}")
        return jsonify({
            'success': False,
            'message': f'同步失败: {str(e)}'
        }), 500

@sync_management_bp.route('/sync_application/<int:application_id>', methods=['POST'])
def sync_specific_application(application_id):
    """同步特定申请"""
    if g.user is None:
        return jsonify({'error': '请先登录'}), 401
    
    if not getattr(g.user, 'is_hr', False):
        return jsonify({'error': '只有HR用户才能访问此页面'}), 403
    
    try:
        # 检查申请是否属于当前HR的职位
        application = Application.query.get_or_404(application_id)
        job = Job.query.get(application.job_id)
        
        if not job or job.user_id != g.user.id:
            return jsonify({'error': '无权操作此申请'}), 403
        
        # 执行同步
        success = DataSyncService.sync_application_to_hr(application_id)
        
        if success:
            return jsonify({
                'success': True,
                'message': f'申请同步完成'
            })
        else:
            return jsonify({
                'success': False,
                'message': f'申请同步失败'
            }), 500
            
    except Exception as e:
        logging.error(f"同步申请 {application_id} 失败: {e}")
        return jsonify({
            'success': False,
            'message': f'同步失败: {str(e)}'
        }), 500

@sync_management_bp.route('/sync_user/<int:user_id>', methods=['POST'])
def sync_specific_user(user_id):
    """同步特定用户的简历"""
    if g.user is None:
        return jsonify({'error': '请先登录'}), 401
    
    if not getattr(g.user, 'is_hr', False):
        return jsonify({'error': '只有HR用户才能访问此页面'}), 403
    
    try:
        # 执行同步
        success = DataSyncService.sync_cv_update_to_hr(user_id)
        
        if success:
            return jsonify({
                'success': True,
                'message': '用户简历同步完成'
            })
        else:
            return jsonify({
                'success': False,
                'message': '用户简历同步失败'
            }), 500
            
    except Exception as e:
        logging.error(f"同步用户 {user_id} 简历失败: {e}")
        return jsonify({
            'success': False,
            'message': f'同步失败: {str(e)}'
        }), 500

@sync_management_bp.route('/logs')
def sync_logs():
    """查看同步日志"""
    if g.user is None:
        flash('请先登录。', 'danger')
        return redirect(url_for('common.auth.sign'))
    
    if not getattr(g.user, 'is_hr', False):
        flash('只有HR用户才能访问此页面。', 'danger')
        return redirect(url_for('common.auth.sign'))
    
    try:
        # 获取同步日志（这里可以从日志文件或数据库获取）
        sync_logs = get_sync_logs()
        
        return render_template('smartrecruit/hr/sync_logs.html',
                             sync_logs=sync_logs)
    except Exception as e:
        logging.error(f"加载同步日志失败: {e}")
        flash('加载同步日志时出现错误，请稍后重试。', 'danger')
        return render_template('smartrecruit/hr/sync_logs.html',
                             sync_logs=[])

def get_recent_sync_activities():
    """获取最近的同步活动"""
    try:
        activities = []
        
        # 获取最近同步的职位
        recent_jobs = Job.query.filter(Job.last_synced.isnot(None)).order_by(Job.last_synced.desc()).limit(5).all()
        for job in recent_jobs:
            activities.append({
                'type': 'job_sync',
                'id': job.id,
                'title': job.title,
                'timestamp': job.last_synced,
                'status': 'success'
            })
        
        # 获取最近同步的申请
        recent_applications = Application.query.filter(Application.last_synced.isnot(None)).order_by(Application.last_synced.desc()).limit(5).all()
        for app in recent_applications:
            activities.append({
                'type': 'application_sync',
                'id': app.id,
                'title': f'申请同步 (用户ID: {app.user_id})',
                'timestamp': app.last_synced,
                'status': 'success'
            })
        
        # 获取最近同步的用户简历
        recent_users = User.query.filter(User.cv_last_synced.isnot(None)).order_by(User.cv_last_synced.desc()).limit(5).all()
        for user in recent_users:
            activities.append({
                'type': 'cv_sync',
                'id': user.id,
                'title': f'简历同步 ({user.email})',
                'timestamp': user.cv_last_synced,
                'status': 'success'
            })
        
        # 按时间排序
        activities.sort(key=lambda x: x['timestamp'], reverse=True)
        return activities[:10]  # 返回最近10个活动
        
    except Exception as e:
        logging.error(f"获取最近同步活动失败: {e}")
        return []

def get_sync_logs():
    """获取同步日志"""
    try:
        # 这里可以从日志文件或数据库获取同步日志
        # 目前返回模拟数据
        return [
            {
                'timestamp': '2024-01-15 10:30:00',
                'level': 'INFO',
                'message': '职位 "前端工程师" 同步完成',
                'user': 'HR用户'
            },
            {
                'timestamp': '2024-01-15 10:25:00',
                'level': 'INFO',
                'message': '申请同步完成 (用户ID: 123)',
                'user': '系统'
            },
            {
                'timestamp': '2024-01-15 10:20:00',
                'level': 'INFO',
                'message': '用户简历同步完成 (user@example.com)',
                'user': '系统'
            }
        ]
    except Exception as e:
        logging.error(f"获取同步日志失败: {e}")
        return []
