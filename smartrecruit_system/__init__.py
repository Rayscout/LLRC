"""
LLRC Header Start
文件功能: SmartRecruit 子系统 Python 模块：smartrecruit_system/__init__.py
创建时间: 2025-08-24 18:00
创建人: 谢佳悦
更新记录:
- 2025-08-26 10:10 by 张宇成
- 2025-08-28 16:40 by 侯东杨
- 2025-08-29 10:32 by 侯东杨
LLRC Header End
"""
"""
FILE-HEADER-AUTO-ADDED
文件: smartrecruit_system/__init__.py
功能: 通用模块
创建时间: 2025-09-02 12:20
创建人: 谢佳悦
更新记录:
- 2025-08-24 18:34 by 侯东杨
- 2025-08-28 14:07 by 李雨梦
"""
from flask import Blueprint

smartrecruit_bp = Blueprint('smartrecruit', __name__, url_prefix='/smartrecruit')

from . import routes
