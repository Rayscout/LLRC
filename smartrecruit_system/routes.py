"""
LLRC Header Start
文件功能: SmartRecruit 子系统 Python 模块：smartrecruit_system/routes.py
创建时间: 2025-08-19 12:50
创建人: 潘显雨
更新记录:
- 2025-08-19 13:20 by 李雨梦
- 2025-08-31 09:06 by 侯东杨
LLRC Header End
"""
"""
FILE-HEADER-AUTO-ADDED
文件: smartrecruit_system/routes.py
功能: 通用模块
创建时间: 2025-08-28 13:15
创建人: 潘显雨
更新记录:
- 2025-08-21 11:19 by 谢佳悦
- 2025-08-27 18:24 by 苏杰
- 2025-08-31 18:39 by 谢佳悦
"""
from flask import Blueprint
from .hr_module import hr_bp
from .candidate_module import candidate_bp

# 创建智能招聘系统主蓝图
smartrecruit_bp = Blueprint('smartrecruit', __name__, url_prefix='/smartrecruit')

# 注册子蓝图
smartrecruit_bp.register_blueprint(hr_bp)
smartrecruit_bp.register_blueprint(candidate_bp)
