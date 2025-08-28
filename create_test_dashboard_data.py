#!/usr/bin/env python3
"""
创建测试数据用于员工仪表板演示
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.models import User, SmartGoal, Project, TaskEvaluation, TalentDevelopmentData, Feedback, db
from datetime import datetime, timedelta
import random

def create_test_data():
    """创建测试数据"""
    app = create_app()

    with app.app_context():
        # 查找测试员工用户
        employee = User.query.get(2)  # 测试员工
        if not employee:
            print("未找到测试员工用户")
            return

        print(f"为用户 {employee.first_name} {employee.last_name} 创建测试数据...")

        # 1. 创建SMART目标数据
        print("创建SMART目标...")
        goals = [
            SmartGoal(
                user_id=employee.id,
                title="提升Python编程技能",
                category="technical",
                specific="通过学习Python进阶课程，提升编程能力至高级水平",
                measurable="完成100小时的学习，掌握高级Python特性",
                achievable="利用工作时间和周末时间学习，每天至少2小时",
                relevant="提升编程技能有助于工作效率和职业发展",
                time_bound="计划在3个月内完成",
                target_date=(datetime.utcnow() + timedelta(days=60)).date(),
                estimated_hours=100,
                completed_hours=75,
                progress=75.0,
                status="active",
                notes="已完成面向对象编程和装饰器学习"
            ),
            SmartGoal(
                user_id=employee.id,
                title="完成项目管理认证",
                category="business",
                specific="获得PMP项目管理专业认证",
                measurable="通过PMP考试，获得认证证书",
                achievable="参加培训课程，利用业余时间准备",
                relevant="项目管理技能对职业发展至关重要",
                time_bound="计划在2个月内完成考试",
                target_date=(datetime.utcnow() + timedelta(days=30)).date(),
                estimated_hours=80,
                completed_hours=80,
                progress=100.0,
                status="completed",
                notes="已成功通过PMP考试，获得认证"
            )
        ]

        for goal in goals:
            db.session.add(goal)

        # 2. 创建项目经验数据
        print("创建项目经验...")
        projects = [
            Project(
                user_id=employee.id,
                name="电商平台开发",
                role="后端开发工程师",
                description="负责电商平台的后端API开发和数据库设计",
                start_date=datetime(2023, 1, 1).date(),
                end_date=datetime(2023, 6, 30).date(),
                status="已完成",
                team_size=8,
                contribution="负责用户认证模块、订单处理系统和数据统计功能"
            ),
            Project(
                user_id=employee.id,
                name="数据分析系统",
                role="数据分析师",
                description="构建公司内部数据分析平台",
                start_date=datetime(2023, 7, 1).date(),
                status="进行中",
                team_size=5,
                contribution="负责数据采集、清洗和可视化展示"
            )
        ]

        for project in projects:
            db.session.add(project)

        # 3. 创建绩效评估数据
        print("创建绩效评估...")
        evaluations = [
            TaskEvaluation(
                evaluator_id=1,  # 假设主管ID为1
                employee_id=employee.id,
                task_title="Q1项目开发任务",
                task_description="完成电商平台的订单模块开发",
                department="技术部",
                score_quality=4,
                score_efficiency=5,
                score_collaboration=4,
                total_score=13,
                comment="工作质量优秀，效率很高，团队协作良好",
                created_at=datetime.utcnow() - timedelta(days=30)
            ),
            TaskEvaluation(
                evaluator_id=1,
                employee_id=employee.id,
                task_title="数据分析优化",
                task_description="优化数据分析系统的查询性能",
                department="技术部",
                score_quality=5,
                score_efficiency=4,
                score_collaboration=5,
                total_score=14,
                comment="数据分析能力突出，协作能力优秀",
                created_at=datetime.utcnow() - timedelta(days=15)
            )
        ]

        for evaluation in evaluations:
            db.session.add(evaluation)

        # 4. 更新人才发展数据
        print("更新人才发展数据...")
        talent_data = TalentDevelopmentData.query.filter_by(employee_id=employee.id).first()
        if not talent_data:
            talent_data = TalentDevelopmentData(
                employee_id=employee.id,
                position="高级开发工程师",
                department="技术部",
                salary=15000.0,
                hire_date=datetime(2022, 1, 1).date()
            )
            db.session.add(talent_data)

        talent_data.performance_score = 92.5
        talent_data.skills_level = 85.0
        talent_data.training_hours = 120.0
        talent_data.certification_count = 3
        talent_data.satisfaction_score = 88.0

        # 5. 添加技能数据到用户
        print("添加技能数据...")
        employee.skills = '["Python", "JavaScript", "SQL", "数据分析", "项目管理"]'

        # 提交所有更改
        db.session.commit()

        print("测试数据创建完成！")
        print("\n创建的数据包括:")
        print("- 2个SMART目标（1个进行中，1个已完成）")
        print("- 2个项目经验")
        print("- 2个绩效评估记录")
        print("- 人才发展数据更新")
        print("- 5个技能标签")

if __name__ == "__main__":
    create_test_data()
