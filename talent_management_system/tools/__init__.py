"""
LLRC Header Start
文件功能: 人才管理子系统 Python 模块：talent_management_system/tools/__init__.py
创建时间: 2025-08-19 11:40
创建人: 谢佳悦
更新记录:
- 2025-08-23 17:04 by 李雨梦
- 2025-08-28 17:49 by 侯东杨
LLRC Header End
"""
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FILE-HEADER-AUTO-ADDED
文件: talent_management_system/tools/__init__.py
功能: 通用模块
创建时间: 2025-08-28 09:27
创建人: 潘显雨
更新记录:
- 2025-08-19 12:10 by 苏杰
- 2025-09-03 18:30 by 潘显雨
"""
"""
人才管理系统工具模块
提供数据库迁移、测试、UI修复等功能
"""

from .database_migration import DatabaseMigrationTool
from .feedback_test_tool import FeedbackTestTool
from .ui_fix_tool import UIFixTool

__all__ = [
    'DatabaseMigrationTool',
    'FeedbackTestTool', 
    'UIFixTool'
]

__version__ = '1.0.0'
__author__ = 'Talent Management System Team'
__description__ = '人才管理系统工具模块'
