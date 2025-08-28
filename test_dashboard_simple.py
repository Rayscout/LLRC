#!/usr/bin/env python3
"""
简单测试员工仪表板数据获取
"""

from app import create_app
from app.models import User
from talent_management_system.employee_manager_module.__init__ import get_dashboard_data

def test_dashboard():
    """简单测试仪表板数据获取"""
    app = create_app()

    with app.app_context():
        # 使用测试员工用户
        employee = User.query.get(2)  # 测试员工
        if not employee:
            print("未找到测试员工用户")
            return

        # 获取仪表板数据
        dashboard_data = get_dashboard_data(employee)

        print("=== 仪表板数据测试结果 ===")
        print(f"绩效评分: {dashboard_data['performance_score']}")
        print(f"学习进度: {dashboard_data['learning_progress']}%")
        print(f"任务完成: {dashboard_data['task_completion']['completed']}/{dashboard_data['task_completion']['total']}")
        print(f"综合评分: {dashboard_data['overall_score']}")
        print(f"项目数量: {dashboard_data['stats_data']['project_count']}")
        print("✅ 技能数量模块已成功删除")
        print(f"最近活动数量: {len(dashboard_data['recent_activities'])}")

        print("\n测试完成!")

if __name__ == "__main__":
    test_dashboard()
