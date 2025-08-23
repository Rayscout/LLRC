from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from app.models import User, db
from datetime import datetime, timedelta
import json
import uuid

feedback_bp = Blueprint('feedback', __name__, url_prefix='/feedback')

# 模拟反馈数据存储
FEEDBACK_REQUESTS = {}
FEEDBACK_RESPONSES = {}
NOTIFICATIONS = {}

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
        
        # 获取用户的反馈请求
        user_requests = get_user_feedback_requests(user.id)
        
        # 获取收到的反馈请求
        received_requests = get_received_feedback_requests(user.id)
        
        # 获取待回复的反馈
        pending_responses = get_pending_feedback_responses(user.id)
        
        # 获取反馈统计
        feedback_stats = get_feedback_statistics(user.id)
        
        return render_template('talent_management/employee_management/feedback_dashboard.html',
                             user=user,
                             user_requests=user_requests,
                             received_requests=received_requests,
                             pending_responses=pending_responses,
                             feedback_stats=feedback_stats)
                             
    except Exception as e:
        flash(f'加载反馈页面时发生错误: {str(e)}', 'danger')
        return redirect(url_for('talent_management.employee_auth.employee_dashboard'))

@feedback_bp.route('/request', methods=['GET', 'POST'])
def request_feedback():
    """请求反馈"""
    try:
        if 'user_id' not in session:
            flash('请先登录', 'warning')
            return redirect(url_for('common.auth.sign'))
        
        user = User.query.get(session['user_id'])
        if not user or user.user_type != 'employee':
            flash('用户信息获取失败', 'warning')
            return redirect(url_for('common.auth.sign'))
        
        if request.method == 'POST':
            # 处理反馈请求
            recipient_id = request.form.get('recipient_id')
            feedback_type = request.form.get('feedback_type')
            message = request.form.get('message')
            priority = request.form.get('priority', 'medium')
            due_date = request.form.get('due_date')
            
            if not all([recipient_id, feedback_type, message]):
                flash('请填写所有必填字段', 'warning')
                return redirect(url_for('talent_management.employee_manager.feedback.request_feedback'))
            
            # 创建反馈请求
            request_id = create_feedback_request(
                user.id, recipient_id, feedback_type, message, priority, due_date
            )
            
            if request_id:
                flash('反馈请求已发送', 'success')
                return redirect(url_for('talent_management.employee_manager.feedback.feedback_dashboard'))
            else:
                flash('发送反馈请求失败', 'danger')
        
        # 获取可选的反馈接收者
        recipients = get_available_recipients(user.id)
        
        return render_template('talent_management/employee_management/request_feedback.html',
                             user=user, recipients=recipients)
                             
    except Exception as e:
        flash(f'请求反馈时发生错误: {str(e)}', 'danger')
        return redirect(url_for('talent_management.employee_manager.feedback.feedback_dashboard'))

@feedback_bp.route('/respond/<request_id>', methods=['GET', 'POST'])
def respond_feedback(request_id):
    """回复反馈"""
    try:
        if 'user_id' not in session:
            flash('请先登录', 'warning')
            return redirect(url_for('common.auth.sign'))
        
        user = User.query.get(session['user_id'])
        if not user or user.user_type != 'employee':
            flash('用户信息获取失败', 'warning')
            return redirect(url_for('common.auth.sign'))
        
        # 获取反馈请求详情
        feedback_request = get_feedback_request(request_id)
        if not feedback_request:
            flash('反馈请求不存在', 'warning')
            return redirect(url_for('talent_management.employee_manager.feedback.feedback_dashboard'))
        
        # 检查是否有权限回复
        if feedback_request['recipient_id'] != user.id:
            flash('您没有权限回复此反馈请求', 'warning')
            return redirect(url_for('talent_management.employee_manager.feedback.feedback_dashboard'))
        
        if request.method == 'POST':
            # 处理反馈回复
            response_text = request.form.get('response_text')
            rating = request.form.get('rating')
            suggestions = request.form.get('suggestions', '')
            
            if not response_text:
                flash('请填写反馈回复', 'warning')
                return redirect(url_for('talent_management.employee_manager.feedback.respond_feedback', request_id=request_id))
            
            # 创建反馈回复
            if create_feedback_response(request_id, user.id, response_text, rating, suggestions):
                flash('反馈回复已提交', 'success')
                return redirect(url_for('talent_management.employee_manager.feedback.feedback_dashboard'))
            else:
                flash('提交反馈回复失败', 'danger')
        
        return render_template('talent_management/employee_management/respond_feedback.html',
                             user=user, feedback_request=feedback_request)
                             
    except Exception as e:
        flash(f'回复反馈时发生错误: {str(e)}', 'danger')
        return redirect(url_for('talent_management.employee_manager.feedback.feedback_dashboard'))

@feedback_bp.route('/view/<request_id>')
def view_feedback(request_id):
    """查看反馈详情"""
    try:
        if 'user_id' not in session:
            flash('请先登录', 'warning')
            return redirect(url_for('common.auth.sign'))
        
        user = User.query.get(session['user_id'])
        if not user or user.user_type != 'employee':
            flash('用户信息获取失败', 'warning')
            return redirect(url_for('common.auth.sign'))
        
        # 获取反馈请求详情
        feedback_request = get_feedback_request(request_id)
        if not feedback_request:
            flash('反馈请求不存在', 'warning')
            return redirect(url_for('talent_management.employee_manager.feedback.feedback_dashboard'))
        
        # 检查是否有权限查看
        if feedback_request['requester_id'] != user.id and feedback_request['recipient_id'] != user.id:
            flash('您没有权限查看此反馈请求', 'warning')
            return redirect(url_for('talent_management.employee_manager.feedback.feedback_dashboard'))
        
        # 获取反馈回复
        feedback_response = get_feedback_response(request_id)
        
        return render_template('talent_management/employee_management/view_feedback.html',
                             user=user, feedback_request=feedback_request, feedback_response=feedback_response)
                             
    except Exception as e:
        flash(f'查看反馈时发生错误: {str(e)}', 'danger')
        return redirect(url_for('talent_management.employee_manager.feedback.feedback_dashboard'))

@feedback_bp.route('/archive/<request_id>')
def archive_feedback(request_id):
    """归档反馈"""
    try:
        if 'user_id' not in session:
            flash('请先登录', 'warning')
            return redirect(url_for('common.auth.sign'))
        
        user = User.query.get(session['user_id'])
        if not user or user.user_type != 'employee':
            flash('用户信息获取失败', 'warning')
            return redirect(url_for('common.auth.sign'))
        
        # 获取反馈请求详情
        feedback_request = get_feedback_request(request_id)
        if not feedback_request:
            flash('反馈请求不存在', 'warning')
            return redirect(url_for('talent_management.employee_manager.feedback.feedback_dashboard'))
        
        # 检查是否有权限归档
        if feedback_request['requester_id'] != user.id:
            flash('您没有权限归档此反馈请求', 'warning')
            return redirect(url_for('talent_management.employee_manager.feedback.feedback_dashboard'))
        
        # 归档反馈
        if archive_feedback_request(request_id):
            flash('反馈已归档', 'success')
        else:
            flash('归档失败', 'danger')
        
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
        
        notifications = get_user_notifications(user.id)
        return jsonify({'success': True, 'data': notifications})
        
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
        
        if mark_notification_read(notification_id, user.id):
            return jsonify({'success': True, 'message': '通知已标记为已读'})
        else:
            return jsonify({'success': False, 'message': '标记失败'})
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'标记失败: {str(e)}'})

# 辅助函数
def get_available_recipients(user_id):
    """获取可选的反馈接收者"""
    try:
        # 获取所有员工和主管
        users = User.query.filter(User.id != user_id).all()
        recipients = []
        
        for user in users:
            if user.user_type in ['employee', 'supervisor']:
                recipients.append({
                    'id': user.id,
                    'name': user.name or user.email,
                    'email': user.email,
                    'user_type': user.user_type,
                    'department': getattr(user, 'department', '未知部门')
                })
        
        return recipients
    except Exception as e:
        print(f"获取接收者失败: {e}")
        return []

def create_feedback_request(requester_id, recipient_id, feedback_type, message, priority, due_date):
    """创建反馈请求"""
    try:
        request_id = str(uuid.uuid4())
        
        # 创建反馈请求
        FEEDBACK_REQUESTS[request_id] = {
            'id': request_id,
            'requester_id': requester_id,
            'recipient_id': recipient_id,
            'feedback_type': feedback_type,
            'message': message,
            'priority': priority,
            'due_date': due_date,
            'status': 'pending',
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        
        # 创建通知
        notification_id = str(uuid.uuid4())
        NOTIFICATIONS[notification_id] = {
            'id': notification_id,
            'user_id': recipient_id,
            'type': 'feedback_request',
            'title': '新的反馈请求',
            'message': f'您收到了一个{feedback_type}反馈请求',
            'related_id': request_id,
            'is_read': False,
            'created_at': datetime.now().isoformat()
        }
        
        return request_id
    except Exception as e:
        print(f"创建反馈请求失败: {e}")
        return None

def get_user_feedback_requests(user_id):
    """获取用户发送的反馈请求"""
    try:
        requests = []
        for request_id, request_data in FEEDBACK_REQUESTS.items():
            if request_data['requester_id'] == user_id:
                # 获取接收者信息
                recipient = User.query.get(request_data['recipient_id'])
                request_data['recipient_name'] = recipient.name if recipient else '未知用户'
                request_data['recipient_email'] = recipient.email if recipient else ''
                
                # 获取回复状态
                request_data['has_response'] = request_id in FEEDBACK_RESPONSES
                
                requests.append(request_data)
        
        # 按创建时间排序
        requests.sort(key=lambda x: x['created_at'], reverse=True)
        return requests
    except Exception as e:
        print(f"获取用户反馈请求失败: {e}")
        return []

def get_received_feedback_requests(user_id):
    """获取用户收到的反馈请求"""
    try:
        requests = []
        for request_id, request_data in FEEDBACK_REQUESTS.items():
            if request_data['recipient_id'] == user_id:
                # 获取请求者信息
                requester = User.query.get(request_data['requester_id'])
                request_data['requester_name'] = requester.name if requester else '未知用户'
                request_data['requester_email'] = requester.email if requester else ''
                
                # 获取回复状态
                request_data['has_response'] = request_id in FEEDBACK_RESPONSES
                
                requests.append(request_data)
        
        # 按创建时间排序
        requests.sort(key=lambda x: x['created_at'], reverse=True)
        return requests
    except Exception as e:
        print(f"获取收到的反馈请求失败: {e}")
        return []

def get_pending_feedback_responses(user_id):
    """获取待回复的反馈"""
    try:
        pending = []
        for request_id, request_data in FEEDBACK_REQUESTS.items():
            if (request_data['recipient_id'] == user_id and 
                request_data['status'] == 'pending' and 
                request_id not in FEEDBACK_RESPONSES):
                
                # 获取请求者信息
                requester = User.query.get(request_data['requester_id'])
                request_data['requester_name'] = requester.name if requester else '未知用户'
                request_data['requester_email'] = requester.email if requester else ''
                
                pending.append(request_data)
        
        # 按优先级和创建时间排序
        priority_order = {'high': 3, 'medium': 2, 'low': 1}
        pending.sort(key=lambda x: (priority_order.get(x['priority'], 0), x['created_at']), reverse=True)
        return pending
    except Exception as e:
        print(f"获取待回复反馈失败: {e}")
        return []

def get_feedback_statistics(user_id):
    """获取反馈统计"""
    try:
        stats = {
            'total_sent': 0,
            'total_received': 0,
            'pending_responses': 0,
            'completed': 0,
            'archived': 0
        }
        
        for request_id, request_data in FEEDBACK_REQUESTS.items():
            if request_data['requester_id'] == user_id:
                stats['total_sent'] += 1
                if request_data['status'] == 'archived':
                    stats['archived'] += 1
                elif request_id in FEEDBACK_RESPONSES:
                    stats['completed'] += 1
            
            if request_data['recipient_id'] == user_id:
                stats['total_received'] += 1
                if (request_data['status'] == 'pending' and 
                    request_id not in FEEDBACK_RESPONSES):
                    stats['pending_responses'] += 1
        
        return stats
    except Exception as e:
        print(f"获取反馈统计失败: {e}")
        return {}

def get_feedback_request(request_id):
    """获取反馈请求详情"""
    return FEEDBACK_REQUESTS.get(request_id)

def create_feedback_response(request_id, responder_id, response_text, rating, suggestions):
    """创建反馈回复"""
    try:
        response_id = str(uuid.uuid4())
        
        # 创建反馈回复
        FEEDBACK_RESPONSES[request_id] = {
            'id': response_id,
            'request_id': request_id,
            'responder_id': responder_id,
            'response_text': response_text,
            'rating': rating,
            'suggestions': suggestions,
            'created_at': datetime.now().isoformat()
        }
        
        # 更新反馈请求状态
        if request_id in FEEDBACK_REQUESTS:
            FEEDBACK_REQUESTS[request_id]['status'] = 'completed'
            FEEDBACK_REQUESTS[request_id]['updated_at'] = datetime.now().isoformat()
        
        # 创建通知给请求者
        if request_id in FEEDBACK_REQUESTS:
            requester_id = FEEDBACK_REQUESTS[request_id]['requester_id']
            notification_id = str(uuid.uuid4())
            NOTIFICATIONS[notification_id] = {
                'id': notification_id,
                'user_id': requester_id,
                'type': 'feedback_response',
                'title': '反馈已回复',
                'message': '您的反馈请求已收到回复',
                'related_id': request_id,
                'is_read': False,
                'created_at': datetime.now().isoformat()
            }
        
        return True
    except Exception as e:
        print(f"创建反馈回复失败: {e}")
        return False

def get_feedback_response(request_id):
    """获取反馈回复"""
    return FEEDBACK_RESPONSES.get(request_id)

def archive_feedback_request(request_id):
    """归档反馈请求"""
    try:
        if request_id in FEEDBACK_REQUESTS:
            FEEDBACK_REQUESTS[request_id]['status'] = 'archived'
            FEEDBACK_REQUESTS[request_id]['updated_at'] = datetime.now().isoformat()
            return True
        return False
    except Exception as e:
        print(f"归档反馈请求失败: {e}")
        return False

def get_user_notifications(user_id):
    """获取用户通知"""
    try:
        notifications = []
        for notification_id, notification_data in NOTIFICATIONS.items():
            if notification_data['user_id'] == user_id:
                notifications.append(notification_data)
        
        # 按创建时间排序
        notifications.sort(key=lambda x: x['created_at'], reverse=True)
        return notifications
    except Exception as e:
        print(f"获取用户通知失败: {e}")
        return []

def mark_notification_read(notification_id, user_id):
    """标记通知为已读"""
    try:
        if (notification_id in NOTIFICATIONS and 
            NOTIFICATIONS[notification_id]['user_id'] == user_id):
            NOTIFICATIONS[notification_id]['is_read'] = True
            return True
        return False
    except Exception as e:
        print(f"标记通知已读失败: {e}")
        return False
