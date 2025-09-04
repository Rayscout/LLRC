"""
LLRC Header Start
文件功能: SmartRecruit 子系统 Python 模块：smartrecruit_system/candidate_module/__init__.py
创建时间: 2025-08-22 15:52
创建人: 苏杰
更新记录:
- 2025-08-22 16:22 by 潘显雨
- 2025-08-28 11:17 by 张宇成
LLRC Header End
"""
"""
FILE-HEADER-AUTO-ADDED
文件: smartrecruit_system/candidate_module/__init__.py
功能: 通用模块
创建时间: 2025-08-20 13:14
创建人: 苏杰
更新记录:
- 2025-08-23 16:36 by 谢佳悦
- 2025-09-01 17:07 by 潘显雨
"""
# 统一从 routes 导出含首页的 candidate_bp，避免重复定义导致路由缺失
from .routes import candidate_bp  # noqa: F401
