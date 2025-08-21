from flask import Blueprint
from .profile import profile_bp
from .performance import performance_bp
from .projects import projects_bp

# 创建员工/经理主蓝图
employee_manager_bp = Blueprint('employee_manager', __name__, url_prefix='/employee_manager')

# 注册员工/经理子蓝图
employee_manager_bp.register_blueprint(profile_bp)
employee_manager_bp.register_blueprint(performance_bp)
employee_manager_bp.register_blueprint(projects_bp)
