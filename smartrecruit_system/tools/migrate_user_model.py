#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
迁移User模型，添加员工管理所需的字段
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

def migrate_user_model():
    """迁移User模型"""
    try:
        from app import create_app, db
        from sqlalchemy import text
        
        print("🚀 开始迁移User模型...")
        print("=" * 50)
        
        app = create_app()
        
        with app.app_context():
            # 检查数据库连接
            try:
                db.session.execute(text("SELECT 1"))
                print("✅ 数据库连接正常")
            except Exception as e:
                print(f"❌ 数据库连接失败: {e}")
                return False
            
            # 检查User表结构
            try:
                result = db.session.execute(text("PRAGMA table_info(user)"))
                columns = result.fetchall()
                print(f"✅ 当前User表有 {len(columns)} 个字段")
                
                column_names = [col[1] for col in columns]
                print(f"   字段列表: {column_names}")
                
            except Exception as e:
                print(f"❌ 检查User表结构失败: {e}")
                return False
            
            # 添加新字段
            new_columns = [
                ('user_type', 'VARCHAR(20) DEFAULT "candidate"'),
                ('employee_id', 'VARCHAR(50) UNIQUE'),
                ('department', 'VARCHAR(100)'),
                ('hire_date', 'DATE'),
                ('supervisor_id', 'INTEGER REFERENCES user(id)'),
                ('bio', 'TEXT'),
                ('experience', 'TEXT'),
                ('education', 'TEXT'),
                ('skills', 'TEXT')
            ]
            
            for column_name, column_def in new_columns:
                if column_name not in column_names:
                    try:
                        sql = f"ALTER TABLE user ADD COLUMN {column_name} {column_def}"
                        db.session.execute(text(sql))
                        print(f"✅ 添加字段: {column_name}")
                    except Exception as e:
                        print(f"⚠️ 添加字段 {column_name} 失败: {e}")
                else:
                    print(f"ℹ️ 字段 {column_name} 已存在")
            
            # 提交更改
            try:
                db.session.commit()
                print("✅ 数据库更改已提交")
            except Exception as e:
                print(f"❌ 提交数据库更改失败: {e}")
                db.session.rollback()
                return False
            
            # 检查更新后的表结构
            try:
                result = db.session.execute(text("PRAGMA table_info(user)"))
                columns = result.fetchall()
                print(f"\n✅ 更新后User表有 {len(columns)} 个字段")
                
                column_names = [col[1] for col in columns]
                print(f"   字段列表: {column_names}")
                
            except Exception as e:
                print(f"❌ 检查更新后User表结构失败: {e}")
                return False
            
            print("\n✅ User模型迁移完成")
            return True
            
    except Exception as e:
        print(f"❌ 迁移失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    migrate_user_model()
