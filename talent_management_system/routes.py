from flask import Blueprint
from .hr_admin_module import hr_admin_bp
from .employee_manager_module import employee_manager_bp

# 创建人才管理主蓝图
talent_management_bp = Blueprint('talent_management', __name__, url_prefix='/talent')

# 注册子蓝图
talent_management_bp.register_blueprint(hr_admin_bp)
talent_management_bp.register_blueprint(employee_manager_bp)
