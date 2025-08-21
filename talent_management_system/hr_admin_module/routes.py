from flask import Blueprint
from .dashboard import dashboard_bp
from .employees import employees_bp
from .departments import departments_bp

# 创建HR管理主蓝图
hr_admin_bp = Blueprint('hr_admin', __name__, url_prefix='/hr_admin')

# 注册HR管理子蓝图
hr_admin_bp.register_blueprint(dashboard_bp)
hr_admin_bp.register_blueprint(employees_bp)
hr_admin_bp.register_blueprint(departments_bp)
