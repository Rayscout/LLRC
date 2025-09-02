#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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
