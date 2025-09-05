"""
LLRC Header Start
文件功能: 应用后端 Python 模块：app/common/__init__.py
创建时间: 2025-08-24 11:03
创建人: 谢佳悦
更新记录:
- 2025-08-24 11:33 by 侯东杨
LLRC Header End
"""
"""
FILE-HEADER-AUTO-ADDED
文件: app/common/__init__.py
功能: 通用模块
创建时间: 2025-08-23 11:50
创建人: 潘显雨
更新记录:
- 2025-08-30 17:16 by 潘显雨
- 2025-09-02 10:24 by 李雨梦
"""
from flask import Blueprint
from .auth import auth_bp
from .files import files_bp

# 创建主蓝图
common_bp = Blueprint('common', __name__)

# 注册子蓝图
common_bp.register_blueprint(auth_bp)
common_bp.register_blueprint(files_bp)
