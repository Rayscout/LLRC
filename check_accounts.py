#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查数据库中的实际账号数据
"""

import os
import sys

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from app import create_app, db
from app.models import User, Job, Application, InterviewSchedule

def check_accounts():
    """检查数据库中的账号数据"""
    app = create_app()
    
    with app.app_context():
        try:
            print("=" * 60)
            print("检查数据库中的实际账号数据")
            print("=" * 60)
            
            # 检查HR账号
            print("\n🔍 检查HR账号:")
            hr_users = User.query.filter_by(is_hr=True).all()
            if hr_users:
                for i, hr in enumerate(hr_users, 1):
                    print(f"  {i}. ID: {hr.id}")
                    print(f"     邮箱: {hr.email}")
                    print(f"     姓名: {hr.first_name}{hr.last_name}")
                    print(f"     部门: {hr.department}")
                    print(f"     职位: {hr.position}")
                    print(f"     密码哈希: {hr.password[:20]}...")
                    print(f"     是否HR: {hr.is_hr}")
                    print()
            else:
                print("  ❌ 没有找到HR账号")
            
            # 检查求职者账号
            print("\n🔍 检查求职者账号:")
            candidate_users = User.query.filter_by(is_hr=False).all()
            if candidate_users:
                for i, candidate in enumerate(candidate_users, 1):
                    print(f"  {i}. ID: {candidate.id}")
                    print(f"     邮箱: {candidate.email}")
                    print(f"     姓名: {candidate.first_name}{candidate.last_name}")
                    print(f"     应聘职位: {candidate.position}")
                    print(f"     密码哈希: {candidate.password[:20]}...")
                    print(f"     是否HR: {candidate.is_hr}")
                    print()
            else:
                print("  ❌ 没有找到求职者账号")
            
            # 检查职位
            print("\n🔍 检查职位:")
            jobs = Job.query.all()
            if jobs:
                for i, job in enumerate(jobs, 1):
                    print(f"  {i}. ID: {job.id}")
                    print(f"     职位: {job.title}")
                    print(f"     公司: {job.company_name}")
                    print(f"     发布者ID: {job.user_id}")
                    print()
            else:
                print("  ❌ 没有找到职位")
            
            # 检查申请记录
            print("\n🔍 检查申请记录:")
            applications = Application.query.all()
            if applications:
                for i, app in enumerate(applications, 1):
                    print(f"  {i}. ID: {app.id}")
                    print(f"     求职者ID: {app.user_id}")
                    print(f"     职位ID: {app.job_id}")
                    print(f"     状态: {app.status}")
                    print()
            else:
                print("  ❌ 没有找到申请记录")
            
            # 检查面试安排
            print("\n🔍 检查面试安排:")
            schedules = InterviewSchedule.query.all()
            if schedules:
                for i, schedule in enumerate(schedules, 1):
                    print(f"  {i}. ID: {schedule.id}")
                    print(f"     求职者ID: {schedule.candidate_id}")
                    print(f"     职位ID: {schedule.job_id}")
                    print(f"     HR ID: {schedule.hr_id}")
                    print(f"     面试时间: {schedule.interview_date} {schedule.start_time}-{schedule.end_time}")
                    print()
            else:
                print("  ❌ 没有找到面试安排")
            
            # 统计信息
            print("\n📊 数据统计:")
            print(f"  总用户数: {User.query.count()}")
            print(f"  HR用户数: {User.query.filter_by(is_hr=True).count()}")
            print(f"  求职者用户数: {User.query.filter_by(is_hr=False).count()}")
            print(f"  职位数: {Job.query.count()}")
            print(f"  申请记录数: {Application.query.count()}")
            print(f"  面试安排数: {InterviewSchedule.query.count()}")
            
            return True
            
        except Exception as e:
            print(f"❌ 检查账号失败: {e}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == '__main__':
    check_accounts()
