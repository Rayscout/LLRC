#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
为HR创建测试数据脚本
"""

import os
import sys

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from app import create_app, db
from app.models import User, Job, Application, InterviewSchedule
from datetime import datetime, date

def create_hr_test_data():
    """为HR创建测试数据"""
    app = create_app()
    
    with app.app_context():
        try:
            print("=" * 60)
            print("为HR创建测试数据")
            print("=" * 60)
            
            # 1. 获取HR用户
            hr_user = User.query.filter_by(email='hr_tech@company.com').first()
            if not hr_user:
                print("❌ 未找到HR用户 hr_tech@company.com")
                return False
            
            print(f"✅ 找到HR用户: {hr_user.first_name}{hr_user.last_name}")
            
            # 2. 创建测试职位
            test_jobs = [
                {
                    'title': 'Python高级开发工程师',
                    'description': '负责公司核心系统的开发和维护，需要扎实的Python基础和系统设计能力',
                    'requirements': 'Python, Django, 数据库设计, 系统架构',
                    'salary': '15k-25k',
                    'location': '北京'
                },
                {
                    'title': '前端开发工程师',
                    'description': '负责公司产品的前端界面开发和用户体验优化',
                    'requirements': 'JavaScript, React, Vue, CSS, HTML',
                    'salary': '12k-20k',
                    'location': '上海'
                },
                {
                    'title': '数据分析师',
                    'description': '负责公司业务数据的分析和挖掘，为决策提供数据支持',
                    'requirements': 'Python, SQL, 统计学, 机器学习',
                    'salary': '10k-18k',
                    'location': '深圳'
                }
            ]
            
            created_jobs = []
            for job_data in test_jobs:
                job = Job(
                    title=job_data['title'],
                    description=job_data['description'],
                    requirements=job_data['requirements'],
                    salary=job_data['salary'],
                    location=job_data['location'],
                    user_id=hr_user.id
                )
                db.session.add(job)
                db.session.commit()
                created_jobs.append(job)
                print(f"✅ 创建职位: {job.title} (ID: {job.id})")
            
            # 3. 创建测试候选人
            test_candidates = [
                {
                    'first_name': '陈',
                    'last_name': '技术强',
                    'email': 'tech_candidate1@email.com',
                    'phone': '13800138001',
                    'position': 'Python高级开发工程师'
                },
                {
                    'first_name': '李',
                    'last_name': '前端王',
                    'email': 'frontend_candidate@email.com',
                    'phone': '13800138002',
                    'position': '前端开发工程师'
                },
                {
                    'first_name': '王',
                    'last_name': '数据专家',
                    'email': 'data_candidate@email.com',
                    'phone': '13800138003',
                    'position': '数据分析师'
                }
            ]
            
            created_candidates = []
            for candidate_data in test_candidates:
                # 检查候选人是否已存在
                existing_candidate = User.query.filter_by(email=candidate_data['email']).first()
                if existing_candidate:
                    created_candidates.append(existing_candidate)
                    print(f"✅ 使用现有候选人: {existing_candidate.first_name}{existing_candidate.last_name}")
                else:
                    candidate = User(
                        first_name=candidate_data['first_name'],
                        last_name=candidate_data['last_name'],
                        company_name='求职者',  # 添加必需的company_name字段
                        email=candidate_data['email'],
                        phone_number=candidate_data['phone'],
                        birthday=date(1990, 1, 1),  # 添加必需的birthday字段
                        password='scrypt:32768:8:1$LogPTRoqrUEs5...',  # 123456的哈希
                        user_type='candidate',
                        is_hr=False
                    )
                    db.session.add(candidate)
                    db.session.commit()
                    created_candidates.append(candidate)
                    print(f"✅ 创建候选人: {candidate.first_name}{candidate.last_name}")
            
            # 4. 创建申请记录和面试安排
            for i, candidate in enumerate(created_candidates):
                if i < len(created_jobs):
                    job = created_jobs[i]
                    
                    # 创建申请记录
                    application = Application(
                        user_id=candidate.id,
                        job_id=job.id,
                        message='我对这个职位很感兴趣，希望能有机会面试。',  # 添加必需的message字段
                        status='pending'
                    )
                    db.session.add(application)
                    db.session.commit()
                    print(f"✅ 创建申请: {candidate.first_name}{candidate.last_name} → {job.title}")
                    
                    # 创建面试安排
                    interview = InterviewSchedule(
                        application_id=application.id,
                        candidate_id=candidate.id,
                        job_id=job.id,
                        hr_id=hr_user.id,
                        interview_date=date(2024, 1, 15 + i),  # 不同的面试日期
                        start_time=datetime.strptime('14:00', '%H:%M').time(),
                        end_time=datetime.strptime('15:00', '%H:%M').time(),
                        interview_type='技术面试',
                        location='会议室A',
                        interviewer_name=hr_user.first_name + hr_user.last_name,
                        status='scheduled',
                        ai_interview_passed=True if i % 2 == 0 else False,  # 交替通过/不通过
                        notification_sent=True
                    )
                    db.session.add(interview)
                    db.session.commit()
                    print(f"✅ 创建面试: {candidate.first_name}{candidate.last_name} - AI面试{'通过' if interview.ai_interview_passed else '不通过'}")
            
            # 5. 验证创建的数据
            print(f"\n🔍 验证创建的数据:")
            hr_jobs = Job.query.filter_by(user_id=hr_user.id).all()
            print(f"  - HR发布的职位: {len(hr_jobs)} 个")
            
            total_applications = 0
            for job in hr_jobs:
                applications = Application.query.filter_by(job_id=job.id).all()
                total_applications += len(applications)
                print(f"    {job.title}: {len(applications)} 个申请")
            
            interviews = InterviewSchedule.query.filter_by(hr_id=hr_user.id).all()
            print(f"  - 面试安排: {len(interviews)} 个")
            
            print(f"\n🎯 现在您可以:")
            print(f"1. 使用 hr_tech@company.com / 123456 登录")
            print(f"2. 选择 'HR' 用户类型")
            print(f"3. 进入候选人管理页面查看候选人")
            print(f"4. 查看AI面试成绩和审核状态")
            
            return True
            
        except Exception as e:
            print(f"❌ 创建测试数据失败: {e}")
            import traceback
            traceback.print_exc()
            db.session.rollback()
            return False

if __name__ == '__main__':
    create_hr_test_data()
