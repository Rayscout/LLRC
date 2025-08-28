#!/usr/bin/env python3
"""
添加项目表到数据库
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db

def add_project_table():
    """添加项目表"""
    app = create_app()

    with app.app_context():
        try:
            print("正在创建项目表...")

            # 创建所有表，包括Project
            db.create_all()
            print("✅ 所有表创建成功！")

            # 导入Project模型来验证表结构
            from app.models import Project

            # 验证表结构
            inspector = db.inspect(db.engine)
            if Project.__tablename__ in inspector.get_table_names():
                columns = inspector.get_columns(Project.__tablename__)

                print("项目表结构验证:")
                for col in columns:
                    print(f"  - {col['name']}: {col['type']}")
            else:
                print("❌ 项目表创建失败")
                return False

        except Exception as e:
            print(f"❌ 创建项目表失败: {str(e)}")
            return False

    return True

if __name__ == "__main__":
    add_project_table()
