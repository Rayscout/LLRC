#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查候选人数据脚本
"""

import os
import sys

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from app import create_app, db
from app.models import User, Job, Application, InterviewSchedule

def check_candidate_data():
    """检查候选人数据"""
    app = create_app()
    
    with app.app_context():
        try:
            print("=" * 60)
            print("检查候选人数据")
            print("=" * 60)
            
            # 1. 检查HR用户
            print("\n🔍 检查HR用户:")
            hr_users = User.query.filter_by(is_hr=True).all()
            print(f"找到 {len(hr_users)} 个HR用户:")
            for hr in hr_users:
                print(f"  - {hr.email} ({hr.first_name}{hr.last_name}) - 部门: {hr.department}")
            
            # 2. 检查职位
            print("\n🔍 检查职位:")
            jobs = Job.query.all()
            print(f"找到 {len(jobs)} 个职位:")
            for job in jobs:
                print(f"  - {job.title} (ID: {job.id}) - 发布者: {job.user_id}")
            
            # 3. 检查申请记录
            print("\n🔍 检查申请记录:")
            applications = Application.query.all()
            print(f"找到 {len(applications)} 个申请记录:")
            for app in applications:
                user = User.query.get(app.user_id)
                job = Job.query.get(app.job_id)
                print(f"  - 申请ID: {app.id}")
                print(f"    候选人: {user.first_name}{user.last_name} ({user.email})")
                print(f"    职位: {job.title if job else '未知职位'}")
                print(f"    状态: {app.status}")
                print()
            
            # 4. 检查面试安排
            print("\n🔍 检查面试安排:")
            interviews = InterviewSchedule.query.all()
            print(f"找到 {len(interviews)} 个面试安排:")
            for interview in interviews:
                user = User.query.get(interview.candidate_id)
                job = Job.query.get(interview.job_id)
                print(f"  - 面试ID: {interview.id}")
                print(f"    候选人: {user.first_name}{user.last_name} ({user.email})")
                print(f"    职位: {job.title if job else '未知职位'}")
                print(f"    AI面试通过: {interview.ai_interview_passed}")
                print(f"    面试日期: {interview.interview_date}")
                print()
            
            # 5. 检查求职者用户
            print("\n🔍 检查求职者用户:")
            candidates = User.query.filter_by(is_hr=False).limit(10).all()
            print(f"找到 {len(candidates)} 个求职者用户:")
            for candidate in candidates:
                print(f"  - {candidate.email} ({candidate.first_name}{candidate.last_name}) - 类型: {candidate.user_type}")
            
            # 6. 为HR创建测试数据
            print("\n🔍 为HR创建测试数据:")
            if hr_users and not applications:
                print("没有申请记录，需要创建测试数据...")
                create_test_data(hr_users[0])
            elif applications:
                print("已有申请记录，数据正常")
            
            return True
            
        except Exception as e:
            print(f"❌ 检查失败: {e}")
            import traceback
            traceback.print_exc()
            return False

def create_test_data(hr_user):
    """为HR创建测试数据"""
    try:
        # 创建测试职位
        test_job = Job(
            title="Python高级开发工程师",
            description="负责公司核心系统的开发和维护",
            requirements="Python, Django, 数据库设计",
            salary="15k-25k",
            location="北京",
            user_id=hr_user.id
        )
        db.session.add(test_job)
        db.session.commit()
        
        # 创建测试求职者
        test_candidate = User(
            first_name="陈",
            last_name="技术强",
            email="tech_candidate1@email.com",
            phone_number="13800138001",
            password="scrypt:32768:8:1$LogPTRoqrUEs5...",  # 123456的哈希
            user_type="candidate",
            is_hr=False
        )
        db.session.add(test_candidate)
        db.session.commit()
        
        # 创建申请记录
        application = Application(
            user_id=test_candidate.id,
            job_id=test_job.id,
            status="pending"
        )
        db.session.add(application)
        db.session.commit()
        
        # 创建面试安排
        interview = InterviewSchedule(
            application_id=application.id,
            candidate_id=test_candidate.id,
            job_id=test_job.id,
            hr_id=hr_user.id,
            interview_date="2024-01-15",
            start_time="14:00",
            end_time="15:00",
            interview_type="技术面试",
            location="会议室A",
            interviewer_name=hr_user.first_name + hr_user.last_name,
            status="scheduled",
            ai_interview_passed=True,
            notification_sent=True
        )
        db.session.add(interview)
        db.session.commit()
        
        print("✅ 测试数据创建成功！")
        print(f"  - 职位: {test_job.title}")
        print(f"  - 候选人: {test_candidate.first_name}{test_candidate.last_name}")
        print(f"  - 申请ID: {application.id}")
        print(f"  - 面试ID: {interview.id}")
        
    except Exception as e:
        print(f"❌ 创建测试数据失败: {e}")
        db.session.rollback()

if __name__ == '__main__':
    check_candidate_data()
