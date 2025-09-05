"""
LLRC Header Start
文件功能: 人才管理子系统 Python 模块：talent_management_system/tools/add_feedback_tables.py
创建时间: 2025-08-22 09:03
创建人: 李雨梦
更新记录:
- 2025-08-22 09:33 by 谢佳悦
- 2025-08-28 14:35 by 苏杰
- 2025-09-01 12:52 by 谢佳悦
LLRC Header End
"""
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FILE-HEADER-AUTO-ADDED
文件: talent_management_system/tools/add_feedback_tables.py
功能: 通用模块
创建时间: 2025-09-03 14:14
创建人: 侯东杨
更新记录:
- 2025-08-23 15:19 by 侯东杨
- 2025-08-26 11:11 by 潘显雨
- 2025-09-02 15:54 by 李雨梦
"""
"""
添加反馈系统数据表的数据库迁移脚本
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app import create_app, db
from app.models import Feedback, FeedbackNotification

def add_feedback_tables():
    """添加反馈系统相关的数据表"""
    app = create_app()
    
    with app.app_context():
        try:
            print("开始创建反馈系统数据表...")
            
            # 创建Feedback表
            db.create_all()
            
            print("✅ 反馈系统数据表创建成功！")
            print("已创建的表:")
            print("- feedback (反馈表)")
            print("- feedback_notification (反馈通知表)")
            
            # 验证表是否创建成功
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            
            if 'feedback' in tables and 'feedback_notification' in tables:
                print("✅ 表创建验证成功")
            else:
                print("❌ 表创建验证失败")
                return False
                
            return True
            
        except Exception as e:
            print(f"❌ 创建反馈系统数据表时发生错误: {str(e)}")
            return False

if __name__ == '__main__':
    success = add_feedback_tables()
    if success:
        print("\n🎉 反馈系统数据表迁移完成！")
    else:
        print("\n💥 反馈系统数据表迁移失败！")
        sys.exit(1)

