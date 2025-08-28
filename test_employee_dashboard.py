#!/usr/bin/env python3
"""
测试员工仪表板数据获取功能
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.models import User, SmartGoal, Project, TaskEvaluation, TalentDevelopmentData, Feedback
from talent_management_system.employee_manager_module.__init__ import get_dashboard_data

def test_dashboard_data():
    """测试仪表板数据获取"""
    app = create_app()

    with app.app_context():
        # 使用具体的员工用户ID进行测试
        employee = User.query.get(2)  # 测试员工
        if not employee:
            print("未找到ID为2的员工用户")
            return

        print(f"测试用户: {employee.first_name} {employee.last_name} (ID: {employee.id})")

        # 获取仪表板数据
        dashboard_data = get_dashboard_data(employee)

        print("\n=== 仪表板数据测试结果 ===")
        print(f"绩效评分: {dashboard_data['performance_score']}")
        print(f"学习进度: {dashboard_data['learning_progress']}%")
        print(f"任务完成: {dashboard_data['task_completion']['completed']}/{dashboard_data['task_completion']['total']}")
        print(f"综合评分: {dashboard_data['overall_score']}")
        print(f"项目数量: {dashboard_data['stats_data']['project_count']}")
        print(f"技能数量: {dashboard_data['stats_data']['skills_count']}")
        print(f"最近活动数量: {len(dashboard_data['recent_activities'])}")

        if dashboard_data['recent_activities']:
            print("\n最近活动:")
            for i, activity in enumerate(dashboard_data['recent_activities'], 1):
                print(f"{i}. {activity['title']} - {activity['time_ago']}")
        else:
            print("\n暂无最近活动")

        print("\n测试完成!")

if __name__ == "__main__":
    test_dashboard_data()
