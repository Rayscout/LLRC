from flask import Blueprint, render_template, session, flash, redirect, url_for
from app.models import User, SmartGoal, Project, TaskEvaluation, TalentDevelopmentData, Feedback
from datetime import datetime, timedelta
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

    # 从数据库获取真实数据
    dashboard_data = get_dashboard_data(user)

    return render_template('talent_management/employee_management/employee_dashboard.html',
                         user=user, supervisor=supervisor, current_date=current_date, **dashboard_data)

def get_dashboard_data(user):
    """获取员工仪表板数据"""
    try:
        # 1. 获取绩效评分
        performance_score = get_performance_score(user.id)

        # 2. 获取学习进度
        learning_progress = get_learning_progress(user.id)

        # 3. 获取任务完成情况
        task_completion = get_task_completion(user.id)

        # 4. 获取综合评分
        overall_score = get_overall_score(user.id)

        # 5. 获取最近活动
        recent_activities = get_recent_activities(user.id)

        # 6. 获取其他统计数据
        stats_data = get_additional_stats(user.id)

        return {
            'performance_score': performance_score,
            'learning_progress': learning_progress,
            'task_completion': task_completion,
            'overall_score': overall_score,
            'recent_activities': recent_activities,
            'stats_data': stats_data
        }
    except Exception as e:
        print(f"获取仪表板数据时出错: {e}")
        # 返回默认数据
        return {
            'performance_score': 0.0,
            'learning_progress': 0,
            'task_completion': {'completed': 0, 'total': 0},
            'overall_score': 0.0,
            'recent_activities': [],
            'stats_data': {}
        }

def get_performance_score(user_id):
    """获取绩效评分"""
    try:
        # 首先尝试从TalentDevelopmentData获取
        talent_data = TalentDevelopmentData.query.filter_by(employee_id=user_id).order_by(TalentDevelopmentData.updated_at.desc()).first()
        if talent_data and talent_data.performance_score:
            return round(talent_data.performance_score, 1)

        # 如果没有，从TaskEvaluation计算平均分
        evaluations = TaskEvaluation.query.filter_by(employee_id=user_id).all()
        if evaluations:
            total_score = sum(eval.total_score for eval in evaluations)
            avg_score = total_score / len(evaluations)
            return round(avg_score / 5.0 * 100, 1)  # 转换为百分制

        return 0.0
    except:
        return 0.0

def get_learning_progress(user_id):
    """获取学习进度"""
    try:
        goals = SmartGoal.query.filter_by(user_id=user_id).all()
        if not goals:
            return 0

        total_progress = sum(goal.progress for goal in goals)
        avg_progress = total_progress / len(goals)
        return round(avg_progress)
    except:
        return 0

def get_task_completion(user_id):
    """获取任务完成情况"""
    try:
        # 这里可以根据实际的任务系统来获取数据
        # 暂时使用模拟数据，可以根据实际需求修改
        evaluations = TaskEvaluation.query.filter_by(employee_id=user_id).all()
        completed_tasks = len([e for e in evaluations if e.total_score >= 12])  # 假设12分以上算完成
        total_tasks = len(evaluations)

        return {
            'completed': completed_tasks,
            'total': total_tasks if total_tasks > 0 else 15  # 默认15个任务
        }
    except:
        return {'completed': 0, 'total': 15}

def get_overall_score(user_id):
    """获取综合评分"""
    try:
        # 计算各项评分的加权平均
        performance_score = get_performance_score(user_id)
        learning_progress = get_learning_progress(user_id)

        # 综合评分 = 绩效评分 * 0.7 + 学习进度 * 0.3
        overall_score = performance_score * 0.7 + learning_progress * 0.3
        return round(overall_score, 1)
    except:
        return 0.0

def get_recent_activities(user_id):
    """获取最近活动"""
    activities = []

    try:
        # 1. 获取最近的目标更新
        recent_goals = SmartGoal.query.filter_by(user_id=user_id).order_by(SmartGoal.last_updated.desc()).limit(3).all()
        for goal in recent_goals:
            if goal.last_updated:
                activities.append({
                    'type': 'goal',
                    'title': f'目标进度更新',
                    'description': f'"{goal.title}" 进度更新为 {goal.progress}%',
                    'time': goal.last_updated.strftime('%Y-%m-%d %H:%M'),
                    'icon': 'fas fa-bullseye',
                    'time_ago': get_time_ago(goal.last_updated)
                })

        # 2. 获取最近的项目操作
        recent_projects = Project.query.filter_by(user_id=user_id).order_by(Project.updated_at.desc()).limit(2).all()
        for project in recent_projects:
            activities.append({
                'type': 'project',
                'title': f'项目更新',
                'description': f'"{project.name}" 项目信息已更新',
                'time': project.updated_at.strftime('%Y-%m-%d %H:%M'),
                'icon': 'fas fa-project-diagram',
                'time_ago': get_time_ago(project.updated_at)
            })

        # 3. 获取最近的反馈
        recent_feedback = Feedback.query.filter_by(recipient_id=user_id).order_by(Feedback.created_at.desc()).limit(2).all()
        for feedback in recent_feedback:
            activities.append({
                'type': 'feedback',
                'title': f'收到反馈',
                'description': f'来自 {feedback.sender.first_name} 的反馈',
                'time': feedback.created_at.strftime('%Y-%m-%d %H:%M'),
                'icon': 'fas fa-comments',
                'time_ago': get_time_ago(feedback.created_at)
            })

        # 4. 获取最近的绩效评估
        recent_evaluations = TaskEvaluation.query.filter_by(employee_id=user_id).order_by(TaskEvaluation.created_at.desc()).limit(2).all()
        for evaluation in recent_evaluations:
            activities.append({
                'type': 'evaluation',
                'title': f'绩效评估',
                'description': f'任务 "{evaluation.task_title}" 获得 {evaluation.total_score} 分',
                'time': evaluation.created_at.strftime('%Y-%m-%d %H:%M'),
                'icon': 'fas fa-chart-line',
                'time_ago': get_time_ago(evaluation.created_at)
            })

        # 按时间排序并取最新的6条
        activities.sort(key=lambda x: x['time'], reverse=True)
        return activities[:6]

    except Exception as e:
        print(f"获取最近活动时出错: {e}")
        return []

def get_additional_stats(user_id):
    """获取其他统计数据"""
    try:
        stats = {}

        # 项目数量
        project_count = Project.query.filter_by(user_id=user_id).count()
        stats['project_count'] = project_count

        # 证书数量（从TalentDevelopmentData获取）
        talent_data = TalentDevelopmentData.query.filter_by(employee_id=user_id).first()
        stats['certification_count'] = talent_data.certification_count if talent_data else 0

        return stats
    except:
        return {'project_count': 0, 'certification_count': 0}

def get_time_ago(dt):
    """计算时间差"""
    try:
        now = datetime.utcnow()
        diff = now - dt

        if diff.days > 0:
            return f"{diff.days}天前"
        elif diff.seconds // 3600 > 0:
            return f"{diff.seconds // 3600}小时前"
        elif diff.seconds // 60 > 0:
            return f"{diff.seconds // 60}分钟前"
        else:
            return "刚刚"
    except:
        return "未知时间"
