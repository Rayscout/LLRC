"""
LLRC Header Start
文件功能: SmartRecruit 子系统 Python 模块：smartrecruit_system/hr_module/__init__.py
创建时间: 2025-08-21 16:10
创建人: 李雨梦
更新记录:
- 2025-08-22 10:16 by 侯东杨
LLRC Header End
"""
"""
FILE-HEADER-AUTO-ADDED
文件: smartrecruit_system/hr_module/__init__.py
功能: 通用模块
创建时间: 2025-08-21 10:25
创建人: 谢佳悦
更新记录:
- 2025-08-21 16:40 by 侯东杨
- 2025-08-26 14:29 by 苏杰
- 2025-09-02 09:55 by 侯东杨
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
