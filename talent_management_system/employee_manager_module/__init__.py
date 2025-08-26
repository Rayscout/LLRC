from flask import Blueprint, render_template, session, flash, redirect, url_for
from app.models import User
from datetime import datetime

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
    
    # 模拟数据用于展示界面效果
    dashboard_data = {
        'current_date': current_date,
        'profile_completeness': 85,
        'performance_score': 92,
        'project_count': 5,
        'learning_progress': 78,
        'skills_count': 12
    }

def calculate_profile_completion(user):
    """计算用户资料完整度"""
    fields = [
        user.first_name, user.last_name, user.email, user.phone_number,
        user.birthday, user.company_name, user.position, user.cv_file
    ]
    
    filled_fields = sum(1 for field in fields if field)
    total_fields = len(fields)
    
    return int((filled_fields / total_fields) * 100) if total_fields > 0 else 0

    # 获取统计数据
    try:
        from smartrecruit_system.candidate_module.jobs import extract_user_skills
        user_skills = extract_user_skills(user)
    except Exception:
        user_skills = []

    # 计算资料完整度
    profile_completion = calculate_profile_completion(user)
    
    # 模拟申请数量和收藏职位数量
    applications_count = 4
    saved_jobs_count = 3
    
    # 修改模板中的链接，让它们指向员工相关的功能
    template_data = {
        'user': user,
        'user_skills': user_skills,
        'applications_count': applications_count,
        'saved_jobs_count': saved_jobs_count,
        'profile_completion': profile_completion,
        'is_employee': True  # 标记这是员工页面
    }
    
    return render_template('talent_management/employee_management/employee_dashboard_new.html', **template_data)
