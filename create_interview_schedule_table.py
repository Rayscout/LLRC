#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创建面试安排表的数据库迁移脚本
"""

import os
import sys

# 添加项目根目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from app import create_app, db
from app.models import InterviewSchedule
from sqlalchemy import text

def create_interview_schedule_table():
    """创建面试安排表"""
    app = create_app()
    
    with app.app_context():
        try:
            # 创建表
            db.create_all()
            print("✓ 面试安排表创建成功！")
            
            # 验证表是否存在
            try:
                # 使用SQLAlchemy的text()函数包装SQL查询
                result = db.session.execute(text("SELECT name FROM sqlite_master WHERE type='table' AND name='interview_schedule'"))
                if result.fetchone():
                    print("✓ 表 'interview_schedule' 已存在于数据库中")
                else:
                    print("✗ 表 'interview_schedule' 创建失败")
                    return False
            except Exception as e:
                print(f"✗ 验证表创建失败: {e}")
                return False
            
            # 显示表结构
            try:
                result = db.session.execute(text("PRAGMA table_info(interview_schedule)"))
                columns = result.fetchall()
                print("\n表结构:")
                print("-" * 60)
                for col in columns:
                    print(f"{col[1]:<20} {col[2]:<15} {'NOT NULL' if col[3] else 'NULL':<10} {col[4] or ''}")
                print("-" * 60)
            except Exception as e:
                print(f"获取表结构失败: {e}")
            
            return True
            
        except Exception as e:
            print(f"✗ 创建面试安排表失败: {e}")
            return False

def main():
    """主函数"""
    print("开始创建面试安排表...")
    print("=" * 50)
    
    success = create_interview_schedule_table()
    
    if success:
        print("\n✓ 数据库迁移完成！")
        print("\n现在您可以:")
        print("1. 在HR面试管理页面安排面试")
        print("2. 查看面试安排列表")
        print("3. 管理面试状态")
    else:
        print("\n✗ 数据库迁移失败！")
        sys.exit(1)

if __name__ == '__main__':
    main()
