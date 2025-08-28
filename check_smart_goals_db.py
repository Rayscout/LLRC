#!/usr/bin/env python3
"""
检查SMART目标数据库表是否存在
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import SmartGoal

def check_smart_goals_table():
    """检查SMART目标表是否存在"""
    app = create_app()

    with app.app_context():
        try:
            # 检查表是否存在
            inspector = db.inspect(db.engine)
            table_exists = SmartGoal.__tablename__ in inspector.get_table_names()

            print(f"SmartGoal table exists: {table_exists}")

            if table_exists:
                # 显示表结构
                columns = inspector.get_columns(SmartGoal.__tablename__)
                print("SMART目标表结构:")
                for col in columns:
                    print(f"  - {col['name']}: {col['type']}")

                # 检查是否有数据
                goal_count = SmartGoal.query.count()
                print(f"SMART目标记录数量: {goal_count}")

                if goal_count > 0:
                    # 显示前几条记录
                    goals = SmartGoal.query.limit(3).all()
                    print("前3条记录:")
                    for goal in goals:
                        print(f"  - ID: {goal.id}, Title: {goal.title}, Status: {goal.status}")
            else:
                print("SMART目标表不存在，正在创建...")
                db.create_all()
                print("表创建完成")

        except Exception as e:
            print(f"检查数据库时出错: {str(e)}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    check_smart_goals_table()
