from flask import Blueprint, render_template, session, flash, redirect, url_for, jsonify
from app.models import User
from datetime import datetime
import json

# 创建员工/经理主蓝图
employee_manager_bp = Blueprint('employee_manager', __name__, url_prefix='/employee_manager')

# 创建员工管理蓝图 (为了匹配路由 talent_management.employee_management.employee_dashboard)
employee_management_bp = Blueprint('employee_management', __name__, url_prefix='/employee_management')

# 导入子模块并注册蓝图
from .profile import profile_bp
from .performance import performance_bp 
from .projects import projects_bp
from .learning_recommendation import learning_recommendation_bp
from .smart_goals import smart_goals_bp
from .compensation import compensation_bp
from .feedback import feedback_bp
from .evaluations import evaluations_bp

# 导入调试和状态检查工具
from .status_check import employee_interface_status
from .debug_tools import debug_employee_errors, debug_employee_routes, debug_employee_auth

# 注册子蓝图到employee_manager_bp
employee_manager_bp.register_blueprint(profile_bp)
employee_manager_bp.register_blueprint(performance_bp)
employee_manager_bp.register_blueprint(projects_bp)
employee_manager_bp.register_blueprint(learning_recommendation_bp)
employee_manager_bp.register_blueprint(smart_goals_bp)
employee_manager_bp.register_blueprint(compensation_bp)
employee_manager_bp.register_blueprint(feedback_bp)
employee_manager_bp.register_blueprint(evaluations_bp)

# 注册子蓝图到employee_management_bp (为了匹配模板中的路由)
employee_management_bp.register_blueprint(profile_bp)
employee_management_bp.register_blueprint(performance_bp)
employee_management_bp.register_blueprint(projects_bp)
employee_management_bp.register_blueprint(learning_recommendation_bp)
employee_management_bp.register_blueprint(smart_goals_bp)
employee_management_bp.register_blueprint(compensation_bp)
employee_management_bp.register_blueprint(feedback_bp)
employee_management_bp.register_blueprint(evaluations_bp)

# 员工仪表板路由 (添加到employee_management_bp中)
@employee_management_bp.route('/employee_dashboard')
def employee_dashboard():
    """员工仪表盘"""
    if 'user_id' not in session or session.get('user_type') != 'employee':
        flash('请先登录员工账号。', 'danger')
        return redirect(url_for('talent_management.employee_auth.employee_auth'))
    
    user = User.query.get(session['user_id'])
    if not user or user.user_type != 'employee':
        session.clear()
        flash('账号验证失败，请重新登录。', 'danger')
        return redirect(url_for('talent_management.employee_auth.employee_auth'))
    
    # 获取主管信息
    supervisor = None
    if user.supervisor_id:
        supervisor = User.query.get(user.supervisor_id)
    
    # 获取当前日期
    current_date = datetime.now().strftime('%Y年%m月%d日')
    
    # 从各个功能模块获取真实数据
    dashboard_data = get_real_dashboard_data(user)
    
    return render_template('talent_management/employee_management/employee_dashboard.html', 
                         user=user, supervisor=supervisor, current_date=current_date, **dashboard_data)

@employee_management_bp.route('/api/dashboard_data')
def api_dashboard_data():
    """API端点：获取仪表盘数据的JSON格式"""
    if 'user_id' not in session or session.get('user_type') != 'employee':
        return jsonify({'error': '未登录或权限不足'}), 401
    
    user = User.query.get(session['user_id'])
    if not user or user.user_type != 'employee':
        return jsonify({'error': '用户信息无效'}), 400
    
    try:
        dashboard_data = get_real_dashboard_data(user)
        return jsonify({
            'success': True,
            'data': dashboard_data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

def get_real_dashboard_data(user):
    """获取仪表盘的真实数据"""
    try:
        from talent_management_system.models import SmartGoal, EmployeeProjectExperience
        from app.models import TaskEvaluation, Feedback
        
        # 1. 绩效评分 - 从TaskEvaluation获取最新的绩效评分
        performance_score = 0.0
        latest_evaluation = TaskEvaluation.query.filter_by(employee_id=user.id)\
            .order_by(TaskEvaluation.created_at.desc()).first()
        if latest_evaluation:
            performance_score = latest_evaluation.total_score / 3.0  # 转换为0-5分制
        
        # 2. 学习进度 - 从SmartGoal获取学习目标的平均进度
        learning_progress = 0.0
        learning_goals = SmartGoal.query.filter_by(
            user_id=user.id, 
            category='learning'
        ).all()
        if learning_goals:
            total_progress = sum(goal.progress for goal in learning_goals)
            learning_progress = total_progress / len(learning_goals)
        
        # 3. 任务完成 - 从SmartGoal获取目标完成情况
        completed_goals = SmartGoal.query.filter_by(
            user_id=user.id, 
            status='completed'
        ).count()
        total_goals = SmartGoal.query.filter_by(user_id=user.id).count()
        task_completion = f"{completed_goals}/{total_goals}" if total_goals > 0 else "0/0"
        
        # 4. 综合评分 - 综合绩效、学习进度和目标完成度
        overall_score = 0.0
        if performance_score > 0:
            overall_score += performance_score * 0.4  # 绩效权重40%
        if learning_progress > 0:
            overall_score += (learning_progress / 100.0) * 5.0 * 0.3  # 学习进度权重30%
        if total_goals > 0:
            completion_rate = completed_goals / total_goals
            overall_score += completion_rate * 5.0 * 0.3  # 目标完成度权重30%
        
        # 5. 项目数量 - 从EmployeeProjectExperience获取
        project_count = EmployeeProjectExperience.query.filter_by(user_id=user.id).count()
        
        # 6. 技能数量 - 从用户资料中提取
        skills_count = 0
        if user.bio:
            skills_count += len([s for s in user.bio.split(',') if s.strip()])
        if hasattr(user, 'skills') and user.skills:
            try:
                skills_data = json.loads(user.skills) if isinstance(user.skills, str) else user.skills
                if isinstance(skills_data, list):
                    skills_count += len(skills_data)
                elif isinstance(skills_data, dict):
                    skills_count += len(skills_data.get('technical', [])) + len(skills_data.get('soft', []))
            except:
                pass
        
        # 7. 最近活动 - 获取最新的活动记录
        recent_activities = get_recent_activities(user)
        
        return {
            'performance_score': round(performance_score, 1),
            'learning_progress': round(learning_progress, 1),
            'task_completion': task_completion,
            'overall_score': round(overall_score, 1),
            'project_count': project_count,
            'skills_count': skills_count,
            'recent_activities': recent_activities
        }
        
    except Exception as e:
        print(f"获取仪表盘数据时出错: {str(e)}")
        # 如果出错，返回默认数据
        return {
            'performance_score': 0.0,
            'learning_progress': 0.0,
            'task_completion': "0/0",
            'overall_score': 0.0,
            'project_count': 0,
            'skills_count': 0,
            'recent_activities': []
        }

def get_recent_activities(user):
    """获取用户最近的活动记录"""
    try:
        from talent_management_system.models import SmartGoal, EmployeeProjectExperience
        from app.models import TaskEvaluation, Feedback
        
        activities = []
        
        # 获取最新的目标更新
        recent_goals = SmartGoal.query.filter_by(user_id=user.id)\
            .order_by(SmartGoal.last_updated.desc()).limit(3).all()
        for goal in recent_goals:
            activities.append({
                'type': 'goal',
                'title': f'目标进度更新：{goal.title}',
                'description': f'目标"{goal.title}"进度达到{goal.progress}%',
                'time': goal.last_updated.strftime('%Y-%m-%d %H:%M'),
                'icon': 'fas fa-bullseye'
            })
        
        # 获取最新的绩效评估
        recent_evaluations = TaskEvaluation.query.filter_by(employee_id=user.id)\
            .order_by(TaskEvaluation.created_at.desc()).limit(2).all()
        for eval in recent_evaluations:
            activities.append({
                'type': 'performance',
                'title': f'绩效评估：{eval.task_title}',
                'description': f'获得{eval.total_score}分评价',
                'time': eval.created_at.strftime('%Y-%m-%d %H:%M'),
                'icon': 'fas fa-chart-line'
            })
        
        # 获取最新的反馈
        recent_feedback = Feedback.query.filter_by(recipient_id=user.id)\
            .order_by(Feedback.created_at.desc()).limit(2).all()
        for feedback in recent_feedback:
            activities.append({
                'type': 'feedback',
                'title': f'收到{feedback.sender.first_name}的反馈',
                'description': f'关于{feedback.category}的{feedback.feedback_type}反馈',
                'time': feedback.created_at.strftime('%Y-%m-%d %H:%M'),
                'icon': 'fas fa-comments'
            })
        
        # 按时间排序并返回最新的5个活动
        activities.sort(key=lambda x: x['time'], reverse=True)
        return activities[:5]
        
    except Exception as e:
        print(f"获取最近活动时出错: {str(e)}")
        return []
