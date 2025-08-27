#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
添加反馈系统数据表的数据库迁移脚本
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

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

