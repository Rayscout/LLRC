"""
LLRC Header Start
文件功能: 人才管理子系统 Python 模块：talent_management_system/hr_admin_module/routes.py
创建时间: 2025-08-25 11:47
创建人: 谢佳悦
更新记录:
- 2025-08-28 14:12 by 潘显雨
LLRC Header End
"""
"""
FILE-HEADER-AUTO-ADDED
文件: talent_management_system/hr_admin_module/routes.py
功能: 通用模块
创建时间: 2025-08-28 18:14
创建人: 李雨梦
更新记录:
- 2025-08-25 12:17 by 侯东杨
"""
from flask import Blueprint
from .dashboard import dashboard_bp
from .employees import employees_bp

# 创建HR管理主蓝图
hr_admin_bp = Blueprint('hr_admin', __name__, url_prefix='/hr_admin')

# 注册HR管理子蓝图
hr_admin_bp.register_blueprint(dashboard_bp)
hr_admin_bp.register_blueprint(employees_bp)
