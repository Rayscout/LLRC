#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库迁移脚本：添加项目经验相关表
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from talent_management_system.models import EmployeeProjectExperience

def create_project_experience_tables():
    """创建项目经验相关的数据库表"""
    try:
        app = create_app()
        
        with app.app_context():
            print("正在创建项目经验相关表...")
            
            # 创建EmployeeProjectExperience表
            EmployeeProjectExperience.__table__.create(db.engine, checkfirst=True)
            print("✓ EmployeeProjectExperience表创建成功")
            
            print("\n所有表创建完成！")
            
    except Exception as e:
        print(f"创建表时发生错误: {e}")
        return False
    
    return True

def drop_project_experience_tables():
    """删除项目经验相关的数据库表（谨慎使用）"""
    try:
        app = create_app()
        
        with app.app_context():
            print("正在删除项目经验相关表...")
            
            # 删除EmployeeProjectExperience表
            EmployeeProjectExperience.__table__.drop(db.engine, checkfirst=True)
            print("✓ EmployeeProjectExperience表删除成功")
            
            print("\n所有表删除完成！")
            
    except Exception as e:
        print(f"删除表时发生错误: {e}")
        return False
    
    return True

def main():
    """主函数"""
    print("项目经验数据库迁移工具")
    print("=" * 40)
    print()
    print("1. 创建项目经验表")
    print("2. 删除项目经验表（谨慎使用）")
    print("3. 退出")
    print()
    
    while True:
        try:
            choice = input("请选择操作 (1-3): ").strip()
            
            if choice == '1':
                if create_project_experience_tables():
                    print("\n✅ 迁移成功完成！")
                else:
                    print("\n❌ 迁移失败！")
                    
            elif choice == '2':
                confirm = input("⚠️  确定要删除项目经验表吗？这将丢失所有数据！(y/N): ").strip().lower()
                if confirm == 'y':
                    if drop_project_experience_tables():
                        print("\n✅ 表删除成功！")
                    else:
                        print("\n❌ 表删除失败！")
                else:
                    print("操作已取消")
                    
            elif choice == '3':
                print("退出程序")
                break
                
            else:
                print("无效选择，请输入1-3")
                
        except KeyboardInterrupt:
            print("\n\n程序被用户中断")
            break
        except Exception as e:
            print(f"发生错误: {e}")
            break

if __name__ == "__main__":
    main()
