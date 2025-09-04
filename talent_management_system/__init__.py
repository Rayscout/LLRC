"""
LLRC Header Start
文件功能: 人才管理子系统 Python 模块：talent_management_system/__init__.py
创建时间: 2025-08-20 13:14
创建人: 侯东杨
更新记录:
- 2025-08-21 12:19 by 苏杰
- 2025-08-27 10:37 by 张宇成
- 2025-08-31 10:20 by 侯东杨
LLRC Header End
"""
"""
FILE-HEADER-AUTO-ADDED
文件: talent_management_system/__init__.py
功能: 通用模块
创建时间: 2025-09-01 14:25
创建人: 张宇成
更新记录:
- 2025-08-20 13:44 by 侯东杨
- 2025-08-22 16:39 by 潘显雨
- 2025-08-25 09:15 by 谢佳悦
"""
from flask import Blueprint

talent_management_bp = Blueprint('talent_management', __name__, url_prefix='/talent')

from . import routes
