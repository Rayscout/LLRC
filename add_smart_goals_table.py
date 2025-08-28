#!/usr/bin/env python3
"""
添加SMART目标表到数据库
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db

def add_smart_goals_table():
    """添加SMART目标表"""
    app = create_app()

    with app.app_context():
        try:
            print("正在创建SMART目标表...")

            # 直接创建所有表，包括SmartGoal
            db.create_all()
            print("✅ 所有表创建成功！")

            # 导入SmartGoal模型来验证表结构
            from app.models import SmartGoal

            # 验证表结构
            inspector = db.inspect(db.engine)
            if SmartGoal.__tablename__ in inspector.get_table_names():
                columns = inspector.get_columns(SmartGoal.__tablename__)

                print("SMART目标表结构验证:")
                for col in columns:
                    print(f"  - {col['name']}: {col['type']}")
            else:
                print("❌ SMART目标表创建失败")
                return False

        except Exception as e:
            print(f"❌ 创建SMART目标表失败: {str(e)}")
            return False

    return True

if __name__ == "__main__":
    add_smart_goals_table()
