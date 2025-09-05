"""
LLRC Header Start
文件功能: SmartRecruit 子系统 Python 模块：smartrecruit_system/hr_module/routes.py
创建时间: 2025-08-25 15:01
创建人: 侯东杨
更新记录:
- 2025-08-29 11:34 by 潘显雨
- 2025-08-30 13:42 by 潘显雨
- 2025-09-03 15:11 by 潘显雨
LLRC Header End
"""
"""
FILE-HEADER-AUTO-ADDED
文件: smartrecruit_system/hr_module/routes.py
功能: 通用模块
创建时间: 2025-08-22 12:09
创建人: 侯东杨
更新记录:
- 2025-08-25 15:31 by 李雨梦
- 2025-09-03 13:40 by 谢佳悦
"""
from flask import Blueprint
from .dashboard import dashboard_bp
from .recruitment import recruitment_bp
from .candidates import candidates_bp
from .profile import profile_bp

# 创建HR主蓝图
hr_bp = Blueprint('hr', __name__, url_prefix='/hr')

# 注册HR子蓝图
hr_bp.register_blueprint(dashboard_bp)
hr_bp.register_blueprint(recruitment_bp)
hr_bp.register_blueprint(candidates_bp)
hr_bp.register_blueprint(profile_bp)
