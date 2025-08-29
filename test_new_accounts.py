#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试新创建的账号登录功能
"""

import os
import sys

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from app import create_app, db
from app.models import User, Job, Application, InterviewSchedule
from werkzeug.security import check_password_hash

def test_new_accounts():
    """测试新创建的账号"""
    app = create_app()
    
    with app.app_context():
        try:
            print("=" * 60)
            print("测试新创建的账号")
            print("=" * 60)
            
            # 测试HR账号
            print("\n🔍 测试HR账号...")
            hr_email = 'hr_test@company.com'
            hr_password = '123456'
            
            hr_user = User.query.filter_by(email=hr_email).first()
            if hr_user:
                print(f"✓ 找到HR用户: {hr_user.email}")
                print(f"  姓名: {hr_user.first_name}{hr_user.last_name}")
                print(f"  部门: {hr_user.department}")
                print(f"  职位: {hr_user.position}")
                print(f"  是否HR: {hr_user.is_hr}")
                print(f"  用户类型: {hr_user.user_type}")
                print(f"  密码哈希: {hr_user.password[:30]}...")
                
                # 测试密码验证
                if check_password_hash(hr_user.password, hr_password):
                    print(f"✓ 密码验证成功！")
                else:
                    print(f"✗ 密码验证失败！")
            else:
                print(f"✗ 未找到HR用户: {hr_email}")
            
            # 测试求职者账号
            print("\n🔍 测试求职者账号...")
            candidate_email = 'candidate_test@email.com'
            candidate_password = '123456'
            
            candidate_user = User.query.filter_by(email=candidate_email).first()
            if candidate_user:
                print(f"✓ 找到求职者用户: {candidate_user.email}")
                print(f"  姓名: {candidate_user.first_name}{candidate_user.last_name}")
                print(f"  应聘职位: {candidate_user.position}")
                print(f"  是否HR: {candidate_user.is_hr}")
                print(f"  用户类型: {candidate_user.user_type}")
                print(f"  密码哈希: {candidate_user.password[:30]}...")
                
                # 测试密码验证
                if check_password_hash(candidate_user.password, candidate_password):
                    print(f"✓ 密码验证成功！")
                else:
                    print(f"✗ 密码验证失败！")
            else:
                print(f"✗ 未找到求职者用户: {candidate_email}")
            
            # 检查相关数据
            print("\n🔍 检查相关数据...")
            
            # 检查职位
            test_job = Job.query.filter_by(title='Python开发工程师').first()
            if test_job:
                print(f"✓ 找到测试职位: {test_job.title}")
                print(f"  公司: {test_job.company_name}")
                print(f"  发布者: {test_job.user_id}")
            else:
                print(f"✗ 未找到测试职位")
            
            # 检查申请记录
            application = Application.query.filter_by(user_id=candidate_user.id).first()
            if application:
                print(f"✓ 找到求职申请")
                print(f"  状态: {application.status}")
                print(f"  职位ID: {application.job_id}")
            else:
                print(f"✗ 未找到求职申请")
            
            # 检查面试安排
            schedule = InterviewSchedule.query.filter_by(candidate_id=candidate_user.id).first()
            if schedule:
                print(f"✓ 找到面试安排")
                print(f"  面试时间: {schedule.interview_date} {schedule.start_time}-{schedule.end_time}")
                print(f"  面试官: {schedule.interviewer_name}")
                print(f"  AI面试通过: {schedule.ai_interview_passed}")
            else:
                print(f"✗ 未找到面试安排")
            
            print(f"\n✅ 账号测试完成！")
            print(f"现在您可以使用以下账号登录:")
            print(f"1. HR账号: {hr_email} + 密码: {hr_password}")
            print(f"2. 求职者账号: {candidate_email} + 密码: {candidate_password}")
            
            return True
            
        except Exception as e:
            print(f"❌ 测试账号失败: {e}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == '__main__':
    test_new_accounts()
