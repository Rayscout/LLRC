#!/usr/bin/env python3
"""
测试SMART目标路由是否正确配置
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from flask import url_for

def test_smart_goals_routes():
    """测试SMART目标相关路由"""
    app = create_app()

    with app.app_context():
        try:
            # 测试路由是否存在
            print("正在测试SMART目标相关路由...")

            # 测试目标仪表板路由
            try:
                dashboard_url = url_for('talent_management.employee_management.smart_goals.goals_dashboard')
                print(f"✅ 目标仪表板路由: {dashboard_url}")
            except Exception as e:
                print(f"❌ 目标仪表板路由错误: {e}")

            # 测试创建目标路由
            try:
                create_url = url_for('talent_management.employee_management.smart_goals.create_goal')
                print(f"✅ 创建目标路由: {create_url}")
            except Exception as e:
                print(f"❌ 创建目标路由错误: {e}")

            # 检查所有注册的路由
            print("\n所有注册的路由:")
            for rule in app.url_map.iter_rules():
                if 'smart_goals' in rule.endpoint:
                    print(f"  - {rule.endpoint}: {rule.rule}")

        except Exception as e:
            print(f"测试路由时出错: {str(e)}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test_smart_goals_routes()
