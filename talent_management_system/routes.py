"""
LLRC Header Start
文件功能: 人才管理子系统 Python 模块：talent_management_system/routes.py
创建时间: 2025-08-21 09:07
创建人: 潘显雨
更新记录:
- 2025-08-21 10:49 by 谢佳悦
LLRC Header End
"""
"""
FILE-HEADER-AUTO-ADDED
文件: talent_management_system/routes.py
功能: 通用模块
创建时间: 2025-08-28 17:43
创建人: 谢佳悦
更新记录:
- 2025-08-21 09:37 by 潘显雨
- 2025-08-25 12:02 by 潘显雨
"""
from flask import Blueprint
from .hr_admin_module import hr_admin_bp
from .hr_admin_module.executive_auth import executive_auth_bp
from .employee_manager_module import employee_manager_bp, employee_management_bp
from .employee_manager_module.employee_auth import employee_auth_bp

# 创建人才管理主蓝图
talent_management_bp = Blueprint('talent_management', __name__, url_prefix='/talent')

# 注册子蓝图
talent_management_bp.register_blueprint(hr_admin_bp)
talent_management_bp.register_blueprint(executive_auth_bp)
talent_management_bp.register_blueprint(employee_manager_bp)
talent_management_bp.register_blueprint(employee_management_bp)
talent_management_bp.register_blueprint(employee_auth_bp)
