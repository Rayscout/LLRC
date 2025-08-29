#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试HR导航脚本
"""

import os
import sys

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from app import create_app, db
from app.models import User, Job, Application, InterviewSchedule

def test_hr_navigation():
    """测试HR导航"""
    app = create_app()
    
    with app.app_context():
        try:
            print("=" * 60)
            print("HR导航测试")
            print("=" * 60)
            
            # 1. 检查HR用户
            hr_user = User.query.filter_by(email='hr_tech@company.com').first()
            if not hr_user:
                print("❌ 未找到HR用户 hr_tech@company.com")
                return False
            
            print(f"✅ 找到HR用户: {hr_user.first_name}{hr_user.last_name}")
            print(f"   邮箱: {hr_user.email}")
            print(f"   部门: {hr_user.department}")
            print(f"   用户类型: {hr_user.user_type}")
            print(f"   是否HR: {hr_user.is_hr}")
            
            # 2. 检查HR发布的职位
            print(f"\n🔍 检查HR发布的职位:")
            hr_jobs = Job.query.filter_by(user_id=hr_user.id).all()
            print(f"找到 {len(hr_jobs)} 个职位:")
            for job in hr_jobs:
                print(f"  - {job.title} (ID: {job.id})")
            
            # 3. 检查这些职位的申请
            print(f"\n🔍 检查职位申请:")
            for job in hr_jobs:
                applications = Application.query.filter_by(job_id=job.id).all()
                print(f"  职位 '{job.title}' 有 {len(applications)} 个申请:")
                for app in applications:
                    user = User.query.get(app.user_id)
                    print(f"    - {user.first_name}{user.last_name} ({user.email}) - 状态: {app.status}")
            
            # 4. 检查面试安排
            print(f"\n🔍 检查面试安排:")
            interviews = InterviewSchedule.query.filter_by(hr_id=hr_user.id).all()
            print(f"找到 {len(interviews)} 个面试安排:")
            for interview in interviews:
                candidate = User.query.get(interview.candidate_id)
                job = Job.query.get(interview.job_id)
                print(f"  - 候选人: {candidate.first_name}{candidate.last_name}")
                print(f"    职位: {job.title if job else '未知'}")
                print(f"    AI面试通过: {interview.ai_interview_passed}")
                print(f"    面试日期: {interview.interview_date}")
                print()
            
            # 5. 提供访问指南
            print("=" * 60)
            print("📋 HR访问指南")
            print("=" * 60)
            
            print(f"\n🌐 访问地址:")
            print(f"1. 主页: http://localhost:5000")
            print(f"2. HR仪表板: http://localhost:5000/smartrecruit/hr/dashboard/")
            print(f"3. 候选人列表: http://localhost:5000/smartrecruit/hr/dashboard/candidates")
            print(f"4. 面试管理: http://localhost:5000/smartrecruit/hr/dashboard/interviews")
            
            print(f"\n🔐 登录信息:")
            print(f"  邮箱: hr_tech@company.com")
            print(f"  密码: 123456")
            print(f"  用户类型: 选择 'HR'")
            
            print(f"\n📊 数据统计:")
            print(f"  - HR发布的职位: {len(hr_jobs)} 个")
            print(f"  - 总申请数: {sum(len(Application.query.filter_by(job_id=job.id).all()) for job in hr_jobs)} 个")
            print(f"  - 面试安排: {len(interviews)} 个")
            
            print(f"\n🎯 下一步操作:")
            print(f"1. 使用HR账号登录")
            print(f"2. 进入候选人管理页面")
            print(f"3. 查看候选人列表和AI面试成绩")
            print(f"4. 审核AI面试结果")
            print(f"5. 安排面试")
            
            return True
            
        except Exception as e:
            print(f"❌ 测试失败: {e}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == '__main__':
    test_hr_navigation()
