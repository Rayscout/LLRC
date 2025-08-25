from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from app.models import User, Feedback, FeedbackNotification, db
from datetime import datetime, timedelta
import json
import uuid

feedback_bp = Blueprint('feedback', __name__, url_prefix='/feedback')

@feedback_bp.route('/')
def feedback_dashboard():
    """反馈管理仪表板"""
    try:
        if 'user_id' not in session:
            flash('请先登录', 'warning')
            return redirect(url_for('common.auth.sign'))
        
        user = User.query.get(session['user_id'])
        if not user or user.user_type != 'employee':
            flash('用户信息获取失败', 'warning')
            return redirect(url_for('common.auth.sign'))
        
        # 获取收到的反馈（来自高管和主管）
        received_feedback = Feedback.query.filter_by(recipient_id=user.id)\
            .order_by(Feedback.created_at.desc()).all()
        
        # 获取未读反馈
        unread_feedback = [f for f in received_feedback if f.status == 'sent']
        
        # 获取反馈统计
        feedback_stats = get_feedback_statistics(user.id)
        
        # 获取最近的反馈通知
        recent_notifications = FeedbackNotification.query.filter_by(
            user_id=user.id, is_read=False
        ).order_by(FeedbackNotification.created_at.desc()).limit(5).all()
        
        return render_template('talent_management/employee_management/feedback_dashboard.html',
                             user=user,
                             received_feedback=received_feedback,
                             unread_feedback=unread_feedback,
                             feedback_stats=feedback_stats,
                             recent_notifications=recent_notifications)
                             
    except Exception as e:
        flash(f'加载反馈页面时发生错误: {str(e)}', 'danger')
        return redirect(url_for('talent_management.employee_auth.employee_dashboard'))

@feedback_bp.route('/view/<feedback_id>')
def view_feedback(feedback_id):
    """查看反馈详情"""
    try:
        if 'user_id' not in session:
            flash('请先登录', 'warning')
            return redirect(url_for('common.auth.sign'))
        
        user = User.query.get(session['user_id'])
        if not user or user.user_type != 'employee':
            flash('用户信息获取失败', 'warning')
            return redirect(url_for('common.auth.sign'))
        
        # 获取反馈详情
        feedback = Feedback.query.get(feedback_id)
        if not feedback:
            flash('反馈不存在', 'warning')
            return redirect(url_for('talent_management.employee_manager.feedback.feedback_dashboard'))
        
        # 检查是否有权限查看
        if feedback.recipient_id != user.id:
            flash('您没有权限查看此反馈', 'warning')
            return redirect(url_for('talent_management.employee_manager.feedback.feedback_dashboard'))
        
        # 标记为已读
        if feedback.status == 'sent':
            feedback.status = 'read'
            feedback.read_at = datetime.now()
            db.session.commit()
        
        # 获取发送者信息
        sender = User.query.get(feedback.sender_id)
        
        return render_template('talent_management/employee_management/view_feedback.html',
                             user=user, feedback=feedback, sender=sender)
                             
    except Exception as e:
        flash(f'查看反馈时发生错误: {str(e)}', 'danger')
        return redirect(url_for('talent_management.employee_manager.feedback.feedback_dashboard'))

@feedback_bp.route('/respond/<feedback_id>', methods=['GET', 'POST'])
def respond_feedback(feedback_id):
    """回复反馈"""
    try:
        if 'user_id' not in session:
            flash('请先登录', 'warning')
            return redirect(url_for('common.auth.sign'))
        
        user = User.query.get(session['user_id'])
        if not user or user.user_type != 'employee':
            flash('用户信息获取失败', 'warning')
            return redirect(url_for('common.auth.sign'))
        
        # 获取反馈详情
        feedback = Feedback.query.get(feedback_id)
        if not feedback:
            flash('反馈不存在', 'warning')
            return redirect(url_for('talent_management.employee_manager.feedback.feedback_dashboard'))
        
        # 检查是否有权限回复
        if feedback.recipient_id != user.id:
            flash('您没有权限回复此反馈', 'warning')
            return redirect(url_for('talent_management.employee_manager.feedback.feedback_dashboard'))
        
        if request.method == 'POST':
            # 处理反馈回复
            response_text = request.form.get('response_text')
            rating = request.form.get('rating')
            suggestions = request.form.get('suggestions', '')
            
            if not response_text:
                flash('请填写反馈回复', 'warning')
                return redirect(url_for('talent_management.employee_manager.feedback.respond_feedback', feedback_id=feedback_id))
            
            # 更新反馈状态
            feedback.status = 'responded'
            feedback.responded_at = datetime.now()
            
            # 这里可以添加回复内容到反馈记录中（如果需要的话）
            # 或者创建单独的回复表
            
            db.session.commit()
            
            # 创建通知给发送者
            create_response_notification(feedback.id, feedback.sender_id, user.id)
            
            flash('反馈回复已提交', 'success')
            return redirect(url_for('talent_management.employee_manager.feedback.feedback_dashboard'))
        
        # 获取发送者信息
        sender = User.query.get(feedback.sender_id)
        
        return render_template('talent_management/employee_management/respond_feedback.html',
                             user=user, feedback=feedback, sender=sender)
                             
    except Exception as e:
        flash(f'回复反馈时发生错误: {str(e)}', 'danger')
        return redirect(url_for('talent_management.employee_manager.feedback.feedback_dashboard'))

@feedback_bp.route('/archive/<feedback_id>')
def archive_feedback(feedback_id):
    """归档反馈"""
    try:
        if 'user_id' not in session:
            flash('请先登录', 'warning')
            return redirect(url_for('common.auth.sign'))
        
        user = User.query.get(session['user_id'])
        if not user or user.user_type != 'employee':
            flash('用户信息获取失败', 'warning')
            return redirect(url_for('common.auth.sign'))
        
        # 获取反馈详情
        feedback = Feedback.query.get(feedback_id)
        if not feedback:
            flash('反馈不存在', 'warning')
            return redirect(url_for('talent_management.employee_manager.feedback.feedback_dashboard'))
        
        # 检查是否有权限归档
        if feedback.recipient_id != user.id:
            flash('您没有权限归档此反馈', 'warning')
            return redirect(url_for('talent_management.employee_manager.feedback.feedback_dashboard'))
        
        # 归档反馈
        feedback.status = 'archived'
        db.session.commit()
        
        flash('反馈已归档', 'success')
        return redirect(url_for('talent_management.employee_manager.feedback.feedback_dashboard'))
                             
    except Exception as e:
        flash(f'归档反馈时发生错误: {str(e)}', 'danger')
        return redirect(url_for('talent_management.employee_manager.feedback.feedback_dashboard'))

@feedback_bp.route('/api/notifications')
def api_notifications():
    """获取通知API"""
    try:
        if 'user_id' not in session:
            return jsonify({'success': False, 'message': '请先登录'})
        
        user = User.query.get(session['user_id'])
        if not user:
            return jsonify({'success': False, 'message': '用户信息获取失败'})
        
        notifications = FeedbackNotification.query.filter_by(
            user_id=user.id, is_read=False
        ).order_by(FeedbackNotification.created_at.desc()).all()
        
        notifications_data = []
        for notification in notifications:
            notifications_data.append({
                'id': notification.id,
                'title': notification.title,
                'message': notification.message,
                'type': notification.notification_type,
                'created_at': notification.created_at.isoformat(),
                'feedback_id': notification.feedback_id
            })
        
        return jsonify({'success': True, 'data': notifications_data})
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'获取通知失败: {str(e)}'})

@feedback_bp.route('/api/mark_read/<notification_id>')
def api_mark_read(notification_id):
    """标记通知为已读API"""
    try:
        if 'user_id' not in session:
            return jsonify({'success': False, 'message': '请先登录'})
        
        user = User.query.get(session['user_id'])
        if not user:
            return jsonify({'success': False, 'message': '用户信息获取失败'})
        
        notification = FeedbackNotification.query.get(notification_id)
        if not notification or notification.user_id != user.id:
            return jsonify({'success': False, 'message': '通知不存在或无权限'})
        
        notification.is_read = True
        db.session.commit()
        
        return jsonify({'success': True, 'message': '通知已标记为已读'})
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'标记失败: {str(e)}'})

@feedback_bp.route('/api/mark_all_read')
def api_mark_all_read():
    """标记所有通知为已读API"""
    try:
        if 'user_id' not in session:
            return jsonify({'success': False, 'message': '请先登录'})
        
        user = User.query.get(session['user_id'])
        if not user:
            return jsonify({'success': False, 'message': '用户信息获取失败'})
        
        FeedbackNotification.query.filter_by(
            user_id=user.id, is_read=False
        ).update({'is_read': True})
        db.session.commit()
        
        return jsonify({'success': True, 'message': '所有通知已标记为已读'})
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'标记失败: {str(e)}'})

# 辅助函数
def get_feedback_statistics(user_id):
    """获取反馈统计"""
    try:
        # 获取用户收到的所有反馈
        received_feedback = Feedback.query.filter_by(recipient_id=user_id).all()
        
        stats = {
            'total_received': len(received_feedback),
            'unread': len([f for f in received_feedback if f.status == 'sent']),
            'read': len([f for f in received_feedback if f.status == 'read']),
            'responded': len([f for f in received_feedback if f.status == 'responded']),
            'archived': len([f for f in received_feedback if f.status == 'archived']),
            'high_priority': len([f for f in received_feedback if f.priority == 'high']),
            'medium_priority': len([f for f in received_feedback if f.priority == 'medium']),
            'low_priority': len([f for f in received_feedback if f.priority == 'low'])
        }
        
        return stats
    except Exception as e:
        print(f"获取反馈统计失败: {e}")
        return {}

def create_response_notification(feedback_id, sender_id, responder_id):
    """创建回复通知"""
    try:
        responder = User.query.get(responder_id)
        responder_name = f"{responder.first_name} {responder.last_name}"
        
        notification = FeedbackNotification(
            user_id=sender_id,
            feedback_id=feedback_id,
            notification_type='feedback_responded',
            title=f'反馈已回复',
            message=f'{responder_name}已回复了您的反馈',
            is_read=False
        )
        db.session.add(notification)
        db.session.commit()
        return True
    except Exception as e:
        print(f"创建回复通知失败: {e}")
        db.session.rollback()
        return False
