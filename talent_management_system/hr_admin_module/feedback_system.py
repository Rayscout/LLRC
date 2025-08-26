#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
高管团队成员反馈系统
"""

from flask import Blueprint, render_template, request, jsonify, session, flash, redirect, url_for
from app.models import User, Feedback, FeedbackNotification, db
from datetime import datetime
import uuid
import json

feedback_system_bp = Blueprint('feedback_system', __name__, url_prefix='/feedback_system')

def get_team_members(executive_id):
    """获取高管的团队成员列表"""
    try:
        # 获取高管信息
        executive = User.query.get(executive_id)
        if not executive:
            return {}
        
        # 根据高管类型获取团队成员
        if executive.user_type == 'executive':
            # 高管可以看到所有员工
            team_members = User.query.filter(
                User.user_type.in_(['employee', 'supervisor']),
                User.id != executive_id
            ).all()
        else:
            # 主管只能看到其下属
            team_members = User.query.filter(
                User.supervisor_id == executive_id,
                User.user_type == 'employee'
            ).all()
        
        # 转换为字典格式
        members_dict = {}
        for member in team_members:
            members_dict[f"{member.first_name} {member.last_name}"] = {
                'id': member.id,
                'position': member.position or '未知职位',
                'department': member.department or '未知部门',
                'email': member.email,
                'avatar': '👨‍💻' if member.user_type == 'employee' else '👩‍💼',
                'user_type': member.user_type,
                'employee_id': member.employee_id
            }
        
        return members_dict
    except Exception as e:
        print(f"获取团队成员失败: {e}")
        return {}

def get_feedback_categories():
    """获取反馈分类"""
    return {
        'skill': {
            'name': '技能发展',
            'icon': '🚀',
            'description': '专业技能、技术能力、学习成长'
        },
        'communication': {
            'name': '沟通协作',
            'icon': '💬',
            'description': '团队合作、沟通表达、人际关系'
        },
        'performance': {
            'name': '绩效表现',
            'icon': '📈',
            'description': '工作成果、效率质量、目标达成'
        }
    }

def get_feedback_templates():
    """获取反馈模板"""
    return {
        'skill': [
            '在{skill}方面表现优秀，建议继续保持并分享经验',
            '{skill}技能需要提升，建议参加相关培训课程',
            '在{skill}领域有潜力，建议设定具体发展目标',
            '{skill}技能已达到预期水平，可以考虑更高阶挑战'
        ],
        'communication': [
            '团队协作表现良好，能够有效促进团队合作',
            '沟通表达需要改进，建议提升演讲和汇报能力',
            '跨部门协作积极主动，是团队的重要桥梁',
            '建议加强主动沟通，及时反馈工作进展'
        ],
        'performance': [
            '工作成果超出预期，展现了优秀的执行能力',
            '任务完成质量良好，建议关注效率提升',
            '目标达成率较高，体现了良好的职业素养',
            '建议设定更具挑战性的目标，发挥更大潜力'
        ]
    }

def create_feedback_notification(feedback_id, recipient_id, sender_name, category, feedback_type, priority):
    """创建反馈通知"""
    try:
        notification = FeedbackNotification(
            user_id=recipient_id,
            feedback_id=feedback_id,
            notification_type='new_feedback',
            title=f'来自{sender_name}的新反馈',
            message=f'您收到了一个关于{category}的{feedback_type}反馈',
            is_read=False
        )
        db.session.add(notification)
        db.session.commit()
        return True
    except Exception as e:
        print(f"创建反馈通知失败: {e}")
        db.session.rollback()
        return False

@feedback_system_bp.route('/dashboard')
def feedback_dashboard():
    """反馈系统仪表板"""
    if 'user_id' not in session:
        return jsonify({'error': '请先登录'}), 401
    
    user = User.query.get(session['user_id'])
    if not user or user.user_type not in ['executive', 'supervisor']:
        return jsonify({'error': '权限不足'}), 403
    
    # 获取数据
    team_members = get_team_members(user.id)
    feedback_categories = get_feedback_categories()
    
    # 统计反馈数据 - 包括发送和接收的反馈
    sent_feedback = Feedback.query.filter_by(sender_id=user.id).all()
    received_feedback = Feedback.query.filter_by(recipient_id=user.id).all()
    
    total_sent = len(sent_feedback)
    total_received = len(received_feedback)
    total_feedback = total_sent + total_received
    
    recent_sent = len([f for f in sent_feedback 
                      if (datetime.now() - f.created_at).days <= 7])
    recent_received = len([f for f in received_feedback 
                          if (datetime.now() - f.created_at).days <= 7])
    recent_feedback = recent_sent + recent_received
    
    # 获取最近的发送反馈记录
    recent_sent_records = Feedback.query.filter_by(sender_id=user.id)\
        .order_by(Feedback.created_at.desc()).limit(5).all()
    
    # 获取最近的接收反馈记录
    recent_received_records = Feedback.query.filter_by(recipient_id=user.id)\
        .order_by(Feedback.created_at.desc()).limit(5).all()
    
    # 转换为字典格式用于模板渲染 - 发送的反馈
    recent_sent_records_dict = []
    for record in recent_sent_records:
        recipient = User.query.get(record.recipient_id)
        recent_sent_records_dict.append({
            'id': record.id,
            'recipient_name': f"{recipient.first_name} {recipient.last_name}" if recipient else '未知用户',
            'category': record.category,
            'feedback_type': record.feedback_type,
            'content': record.content,
            'priority': record.priority,
            'status': record.status,
            'created_at': record.created_at
        })
    
    # 转换为字典格式用于模板渲染 - 接收的反馈
    recent_received_records_dict = []
    for record in recent_received_records:
        sender = User.query.get(record.sender_id)
        recent_received_records_dict.append({
            'id': record.id,
            'sender_name': f"{sender.first_name} {sender.last_name}" if sender else '未知用户',
            'category': record.category,
            'feedback_type': record.feedback_type,
            'content': record.content,
            'priority': record.priority,
            'status': record.status,
            'created_at': record.created_at
        })
    
    return render_template(
        'talent_management/hr_admin/feedback_dashboard.html',
        user=user,
        team_members=team_members,
        feedback_categories=feedback_categories,
        total_feedback=total_feedback,
        recent_feedback=recent_feedback,
        total_sent=total_sent,
        total_received=total_received,
        recent_sent=recent_sent,
        recent_received=recent_received,
        recent_sent_records=recent_sent_records_dict,
        recent_received_records=recent_received_records_dict
    )

@feedback_system_bp.route('/send_feedback', methods=['GET', 'POST'])
def send_feedback():
    """发送反馈页面"""
    if 'user_id' not in session:
        return jsonify({'error': '请先登录'}), 401
    
    user = User.query.get(session['user_id'])
    if not user or user.user_type not in ['executive', 'supervisor']:
        return jsonify({'error': '权限不足'}), 403
    
    if request.method == 'POST':
        # 处理反馈提交
        recipient_id = request.form.get('recipient_id')
        category = request.form.get('category')
        feedback_type = request.form.get('feedback_type')
        content = request.form.get('content')
        priority = request.form.get('priority', 'medium')
        
        if not all([recipient_id, category, feedback_type, content]):
            flash('请填写完整的反馈信息', 'error')
            return redirect(url_for('talent_management.hr_admin.feedback_system.send_feedback'))
        
        # 验证接收者是否存在
        recipient = User.query.get(recipient_id)
        if not recipient:
            flash('选择的团队成员不存在', 'error')
            return redirect(url_for('talent_management.hr_admin.feedback_system.send_feedback'))
        
        try:
            # 创建反馈记录
            feedback = Feedback(
                sender_id=user.id,
                recipient_id=recipient_id,
                category=category,
                feedback_type=feedback_type,
                content=content,
                priority=priority,
                status='sent'
            )
            db.session.add(feedback)
            db.session.commit()
            
            # 创建通知
            sender_name = f"{user.first_name} {user.last_name}"
            create_feedback_notification(
                feedback.id, 
                recipient_id, 
                sender_name, 
                category, 
                feedback_type, 
                priority
            )
            
            flash(f'反馈已成功发送给 {recipient.first_name} {recipient.last_name}', 'success')
            return redirect(url_for('talent_management.hr_admin.feedback_system.feedback_dashboard'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'发送反馈失败: {str(e)}', 'error')
            return redirect(url_for('talent_management.hr_admin.feedback_system.send_feedback'))
    
    # GET请求显示发送反馈页面
    team_members = get_team_members(user.id)
    feedback_categories = get_feedback_categories()
    feedback_templates = get_feedback_templates()
    
    return render_template(
        'talent_management/hr_admin/send_feedback.html',
        user=user,
        team_members=team_members,
        feedback_categories=feedback_categories,
        feedback_templates=feedback_templates
    )

@feedback_system_bp.route('/feedback_history')
def feedback_history():
    """反馈历史记录"""
    if 'user_id' not in session:
        return jsonify({'error': '请先登录'}), 401
    
    user = User.query.get(session['user_id'])
    if not user or user.user_type not in ['executive', 'supervisor']:
        return jsonify({'error': '权限不足'}), 403
    
    # 获取筛选参数
    category_filter = request.args.get('category', '')
    recipient_filter = request.args.get('recipient', '')
    date_filter = request.args.get('date', '')
    
    # 构建查询
    query = Feedback.query.filter_by(sender_id=user.id)
    
    if category_filter:
        query = query.filter_by(category=category_filter)
    
    if recipient_filter:
        # 通过接收者姓名筛选
        recipients = User.query.filter(
            User.first_name.contains(recipient_filter) | 
            User.last_name.contains(recipient_filter)
        ).all()
        recipient_ids = [r.id for r in recipients]
        query = query.filter(Feedback.recipient_id.in_(recipient_ids))
    
    if date_filter:
        # 按日期筛选
        from datetime import datetime, timedelta
        start_date = datetime.strptime(date_filter, '%Y-%m-%d')
        end_date = start_date + timedelta(days=1)
        query = query.filter(Feedback.created_at >= start_date, Feedback.created_at < end_date)
    
    # 获取反馈记录
    feedback_records = query.order_by(Feedback.created_at.desc()).all()
    
    # 转换为字典格式
    records_dict = []
    for record in feedback_records:
        recipient = User.query.get(record.recipient_id)
        records_dict.append({
            'id': record.id,
            'sender_name': f"{user.first_name} {user.last_name}",
            'recipient_name': f"{recipient.first_name} {recipient.last_name}" if recipient else '未知用户',
            'category': record.category,
            'feedback_type': record.feedback_type,
            'content': record.content,
            'priority': record.priority,
            'status': record.status,
            'created_at': record.created_at,
            'read_at': record.read_at,
            'responded_at': record.responded_at
        })
    
    team_members = get_team_members(user.id)
    feedback_categories = get_feedback_categories()
    
    return render_template(
        'talent_management/hr_admin/feedback_history.html',
        user=user,
        feedback_records=records_dict,
        team_members=team_members,
        feedback_categories=feedback_categories,
        category_filter=category_filter,
        recipient_filter=recipient_filter,
        date_filter=date_filter
    )

@feedback_system_bp.route('/api/team_members')
def api_team_members():
    """获取团队成员API"""
    if 'user_id' not in session:
        return jsonify({'error': '请先登录'}), 401
    
    user = User.query.get(session['user_id'])
    if not user or user.user_type not in ['executive', 'supervisor']:
        return jsonify({'error': '权限不足'}), 403
    
    team_members = get_team_members(user.id)
    return jsonify(team_members)

@feedback_system_bp.route('/api/feedback_categories')
def api_feedback_categories():
    """获取反馈分类API"""
    if 'user_id' not in session:
        return jsonify({'error': '请先登录'}), 401
    
    user = User.query.get(session['user_id'])
    if not user or user.user_type not in ['executive', 'supervisor']:
        return jsonify({'error': '权限不足'}), 403
    
    feedback_categories = get_feedback_categories()
    return jsonify(feedback_categories)

@feedback_system_bp.route('/api/feedback_templates/<category>')
def api_feedback_templates(category):
    """获取反馈模板API"""
    if 'user_id' not in session:
        return jsonify({'error': '请先登录'}), 401
    
    user = User.query.get(session['user_id'])
    if not user or user.user_type not in ['executive', 'supervisor']:
        return jsonify({'error': '权限不足'}), 403
    
    feedback_templates = get_feedback_templates()
    if category in feedback_templates:
        return jsonify(feedback_templates[category])
    else:
        return jsonify([])

@feedback_system_bp.route('/api/feedback_stats')
def api_feedback_stats():
    """获取反馈统计API"""
    if 'user_id' not in session:
        return jsonify({'error': '请先登录'}), 401
    
    user = User.query.get(session['user_id'])
    if not user or user.user_type not in ['executive', 'supervisor']:
        return jsonify({'error': '权限不足'}), 403
    
    # 统计数据
    sent_feedback = Feedback.query.filter_by(sender_id=user.id).all()
    total_feedback = len(sent_feedback)
    recent_feedback = len([f for f in sent_feedback 
                          if (datetime.now() - f.created_at).days <= 7])
    
    # 按分类统计
    category_stats = {}
    feedback_categories = get_feedback_categories()
    for category in feedback_categories:
        category_stats[category] = len([f for f in sent_feedback 
                                      if f.category == category])
    
    # 按优先级统计
    priority_stats = {
        'high': len([f for f in sent_feedback if f.priority == 'high']),
        'medium': len([f for f in sent_feedback if f.priority == 'medium']),
        'low': len([f for f in sent_feedback if f.priority == 'low'])
    }
    
    return jsonify({
        'total_feedback': total_feedback,
        'recent_feedback': recent_feedback,
        'category_stats': category_stats,
        'priority_stats': priority_stats
    })
