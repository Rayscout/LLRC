#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
高管团队成员反馈系统
"""

from flask import Blueprint, render_template, request, jsonify, session, flash, redirect, url_for
from app.models import User, db
from datetime import datetime
import uuid
import json

feedback_system_bp = Blueprint('feedback_system', __name__, url_prefix='/feedback_system')

# 模拟反馈数据存储（实际项目中应使用数据库）
feedback_records = {}
feedback_notifications = {}

def generate_team_members():
    """生成团队成员列表"""
    return {
        '张工程师': {
            'id': '001',
            'position': '高级软件工程师',
            'department': '技术部',
            'email': 'zhang.engineer@company.com',
            'avatar': '👨‍💻'
        },
        '李产品经理': {
            'id': '002',
            'position': '产品经理',
            'department': '产品部',
            'email': 'li.pm@company.com',
            'avatar': '👩‍💼'
        },
        '王设计师': {
            'id': '003',
            'position': 'UI/UX设计师',
            'department': '设计部',
            'email': 'wang.designer@company.com',
            'avatar': '🎨'
        },
        '陈运营': {
            'id': '004',
            'position': '运营专员',
            'department': '运营部',
            'email': 'chen.ops@company.com',
            'avatar': '📊'
        },
        '刘销售': {
            'id': '005',
            'position': '销售代表',
            'department': '销售部',
            'email': 'liu.sales@company.com',
            'avatar': '💼'
        }
    }

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

@feedback_system_bp.route('/dashboard')
def feedback_dashboard():
    """反馈系统仪表板"""
    if 'user_id' not in session:
        return jsonify({'error': '请先登录'}), 401
    
    user = User.query.get(session['user_id'])
    if not user or user.user_type != 'executive':
        return jsonify({'error': '权限不足'}), 403
    
    # 获取数据
    team_members = generate_team_members()
    feedback_categories = get_feedback_categories()
    
    # 统计反馈数据
    total_feedback = len(feedback_records)
    recent_feedback = len([f for f in feedback_records.values() 
                          if (datetime.now() - f['created_at']).days <= 7])
    
    # 获取最近的反馈记录
    recent_records = sorted(feedback_records.values(), 
                           key=lambda x: x['created_at'], reverse=True)[:5]
    
    return render_template(
        'talent_management/hr_admin/feedback_dashboard.html',
        user=user,
        team_members=team_members,
        feedback_categories=feedback_categories,
        total_feedback=total_feedback,
        recent_feedback=recent_feedback,
        recent_records=recent_records
    )

@feedback_system_bp.route('/send_feedback', methods=['GET', 'POST'])
def send_feedback():
    """发送反馈页面"""
    if 'user_id' not in session:
        return jsonify({'error': '请先登录'}), 401
    
    user = User.query.get(session['user_id'])
    if not user or user.user_type != 'executive':
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
        
        # 创建反馈记录
        feedback_id = str(uuid.uuid4())
        team_members = generate_team_members()
        recipient_name = None
        for name, member in team_members.items():
            if member['id'] == recipient_id:
                recipient_name = name
                break
        
        if not recipient_name:
            flash('选择的团队成员不存在', 'error')
            return redirect(url_for('talent_management.hr_admin.feedback_system.send_feedback'))
        
        # 保存反馈记录
        feedback_records[feedback_id] = {
            'id': feedback_id,
            'sender_id': user.id,
            'sender_name': f"{user.first_name} {user.last_name}",
            'recipient_id': recipient_id,
            'recipient_name': recipient_name,
            'category': category,
            'feedback_type': feedback_type,
            'content': content,
            'priority': priority,
            'status': 'sent',
            'created_at': datetime.now(),
            'read_at': None
        }
        
        # 创建通知
        notification_id = str(uuid.uuid4())
        feedback_notifications[notification_id] = {
            'id': notification_id,
            'feedback_id': feedback_id,
            'recipient_id': recipient_id,
            'recipient_name': recipient_name,
            'sender_name': f"{user.first_name} {user.last_name}",
            'category': category,
            'feedback_type': feedback_type,
            'priority': priority,
            'is_read': False,
            'created_at': datetime.now()
        }
        
        flash(f'反馈已成功发送给 {recipient_name}', 'success')
        return redirect(url_for('talent_management.hr_admin.feedback_system.feedback_dashboard'))
    
    # GET请求显示发送反馈页面
    team_members = generate_team_members()
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
    if not user or user.user_type != 'executive':
        return jsonify({'error': '权限不足'}), 403
    
    # 获取筛选参数
    category_filter = request.args.get('category', '')
    recipient_filter = request.args.get('recipient', '')
    date_filter = request.args.get('date', '')
    
    # 筛选反馈记录
    filtered_records = []
    for record in feedback_records.values():
        if record['sender_id'] == user.id:  # 只显示发送的反馈
            include_record = True
            
            if category_filter and record['category'] != category_filter:
                include_record = False
            if recipient_filter and recipient_filter not in record['recipient_name']:
                include_record = False
            if date_filter:
                record_date = record['created_at'].strftime('%Y-%m-%d')
                if record_date != date_filter:
                    include_record = False
            
            if include_record:
                filtered_records.append(record)
    
    # 按时间排序
    filtered_records.sort(key=lambda x: x['created_at'], reverse=True)
    
    team_members = generate_team_members()
    feedback_categories = get_feedback_categories()
    
    return render_template(
        'talent_management/hr_admin/feedback_history.html',
        user=user,
        feedback_records=filtered_records,
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
    if not user or user.user_type != 'executive':
        return jsonify({'error': '权限不足'}), 403
    
    team_members = generate_team_members()
    return jsonify(team_members)

@feedback_system_bp.route('/api/feedback_categories')
def api_feedback_categories():
    """获取反馈分类API"""
    if 'user_id' not in session:
        return jsonify({'error': '请先登录'}), 401
    
    user = User.query.get(session['user_id'])
    if not user or user.user_type != 'executive':
        return jsonify({'error': '权限不足'}), 403
    
    feedback_categories = get_feedback_categories()
    return jsonify(feedback_categories)

@feedback_system_bp.route('/api/feedback_templates/<category>')
def api_feedback_templates(category):
    """获取反馈模板API"""
    if 'user_id' not in session:
        return jsonify({'error': '请先登录'}), 401
    
    user = User.query.get(session['user_id'])
    if not user or user.user_type != 'executive':
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
    if not user or user.user_type != 'executive':
        return jsonify({'error': '权限不足'}), 403
    
    # 统计数据
    total_feedback = len(feedback_records)
    recent_feedback = len([f for f in feedback_records.values() 
                          if (datetime.now() - f['created_at']).days <= 7])
    
    # 按分类统计
    category_stats = {}
    feedback_categories = get_feedback_categories()
    for category in feedback_categories:
        category_stats[category] = len([f for f in feedback_records.values() 
                                      if f['category'] == category])
    
    # 按优先级统计
    priority_stats = {
        'high': len([f for f in feedback_records.values() if f['priority'] == 'high']),
        'medium': len([f for f in feedback_records.values() if f['priority'] == 'medium']),
        'low': len([f for f in feedback_records.values() if f['priority'] == 'low'])
    }
    
    return jsonify({
        'total_feedback': total_feedback,
        'recent_feedback': recent_feedback,
        'category_stats': category_stats,
        'priority_stats': priority_stats
    })
