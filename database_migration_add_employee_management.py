#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
员工管理功能数据库迁移脚本
用于向 user 表添加账号状态管理字段
"""

import os
import sys
from datetime import datetime

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from app import create_app, db
from app.models import User

def migrate_database():
    """执行数据库迁移"""
    print("开始数据库迁移...")
    
    try:
        # 获取数据库连接
        with db.engine.connect() as connection:
            # 检查现有字段
            result = connection.execute(db.text("PRAGMA table_info(user)"))
            existing_columns = [row[1] for row in result.fetchall()]
            print(f"现有字段: {existing_columns}")
            
            # 需要添加的字段
            new_columns = []
            
            if 'is_active' not in existing_columns:
                new_columns.append('is_active')
                print("添加字段: is_active")
                connection.execute(db.text("ALTER TABLE user ADD COLUMN is_active BOOLEAN DEFAULT 1"))
                connection.commit()
            
            if 'deactivated_at' not in existing_columns:
                new_columns.append('deactivated_at')
                print("添加字段: deactivated_at")
                connection.execute(db.text("ALTER TABLE user ADD COLUMN deactivated_at DATETIME"))
                connection.commit()
            
            if 'deactivated_by' not in existing_columns:
                new_columns.append('deactivated_by')
                print("添加字段: deactivated_by")
                connection.execute(db.text("ALTER TABLE user ADD COLUMN deactivated_by INTEGER REFERENCES user(id)"))
                connection.commit()
            
            if new_columns:
                print(f"成功添加字段: {new_columns}")
                
                # 更新现有用户的 is_active 状态
                print("更新现有用户状态...")
                connection.execute(db.text("UPDATE user SET is_active = 1 WHERE is_active IS NULL"))
                connection.commit()
                print("现有用户状态更新完成")
            else:
                print("所有必要字段已存在，无需迁移")
            
            return True
            
    except Exception as e:
        print(f"迁移失败: {e}")
        return False

def verify_migration():
    """验证迁移结果"""
    print("\n验证迁移结果...")
    
    try:
        with db.engine.connect() as connection:
            # 检查字段是否存在
            result = connection.execute(db.text("PRAGMA table_info(user)"))
            columns = [row[1] for row in result.fetchall()]
            
            required_columns = ['is_active', 'deactivated_at', 'deactivated_by']
            missing_columns = [col for col in required_columns if col not in columns]
            
            if missing_columns:
                print(f"❌ 缺少字段: {missing_columns}")
                return False
            
            print("✅ 所有必要字段已添加")
            
            # 检查数据
            result = connection.execute(db.text("SELECT COUNT(*) FROM user WHERE is_active = 1"))
            active_count = result.fetchone()[0]
            
            result = connection.execute(db.text("SELECT COUNT(*) FROM user"))
            total_count = result.fetchone()[0]
            
            print(f"总用户数: {total_count}")
            print(f"活跃用户数: {active_count}")
            
            return True
            
    except Exception as e:
        print(f"验证失败: {e}")
        return False

def main():
    """主函数"""
    print("=" * 50)
    print("员工管理功能数据库迁移脚本")
    print("=" * 50)
    
    # 创建Flask应用上下文
    app = create_app()
    
    with app.app_context():
        try:
            # 执行迁移
            if migrate_database():
                print("\n✅ 数据库迁移成功完成！")
                
                # 验证迁移
                if verify_migration():
                    print("\n🎉 迁移验证通过！")
                    print("\n现在你可以：")
                    print("1. 重启Flask应用")
                    print("2. 访问高管页面")
                    print("3. 使用员工管理功能")
                else:
                    print("\n⚠️  迁移验证失败，请检查数据库状态")
            else:
                print("\n❌ 数据库迁移失败！")
                print("请检查错误信息并手动修复，或联系技术支持")
                
        except Exception as e:
            print(f"\n💥 迁移过程中发生错误: {e}")
            print("请检查错误信息并手动修复，或联系技术支持")

if __name__ == "__main__":
    main()
