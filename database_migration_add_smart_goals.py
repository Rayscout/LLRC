#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库迁移脚本：添加SMART目标相关表
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from talent_management_system.models import SmartGoal, GoalProgress

def create_smart_goals_tables():
    """创建SMART目标相关的数据库表"""
    try:
        app = create_app()
        
        with app.app_context():
            print("正在创建SMART目标相关表...")
            
            # 创建SmartGoal表
            SmartGoal.__table__.create(db.engine, checkfirst=True)
            print("✓ SmartGoal表创建成功")
            
            # 创建GoalProgress表
            GoalProgress.__table__.create(db.engine, checkfirst=True)
            print("✓ GoalProgress表创建成功")
            
            print("\n所有表创建完成！")
            
    except Exception as e:
        print(f"创建表时发生错误: {e}")
        return False
    
    return True

def drop_smart_goals_tables():
    """删除SMART目标相关的数据库表（谨慎使用）"""
    try:
        app = create_app()
        
        with app.app_context():
            print("正在删除SMART目标相关表...")
            
            # 删除GoalProgress表（先删除，因为有外键依赖）
            GoalProgress.__table__.drop(db.engine, checkfirst=True)
            print("✓ GoalProgress表删除成功")
            
            # 删除SmartGoal表
            SmartGoal.__table__.drop(db.engine, checkfirst=True)
            print("✓ SmartGoal表删除成功")
            
            print("\n所有表删除完成！")
            
    except Exception as e:
        print(f"删除表时发生错误: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("SMART目标数据库迁移工具")
    print("=" * 40)
    
    while True:
        print("\n请选择操作：")
        print("1. 创建SMART目标表")
        print("2. 删除SMART目标表（谨慎使用）")
        print("3. 退出")
        
        choice = input("\n请输入选择 (1-3): ").strip()
        
        if choice == "1":
            if create_smart_goals_tables():
                print("\n迁移成功完成！")
            else:
                print("\n迁移失败！")
        elif choice == "2":
            confirm = input("确定要删除所有SMART目标数据吗？这将永久删除所有目标数据！(输入 'yes' 确认): ")
            if confirm.lower() == 'yes':
                if drop_smart_goals_tables():
                    print("\n删除成功完成！")
                else:
                    print("\n删除失败！")
            else:
                print("操作已取消")
        elif choice == "3":
            print("退出程序")
            break
        else:
            print("无效选择，请重新输入")
