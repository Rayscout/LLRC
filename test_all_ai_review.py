#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试所有AI面试审核功能
"""

import os
import sys

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from app import create_app, db
from app.models import User, Job, Application, InterviewSchedule

def test_all_ai_review():
    """测试所有AI面试审核功能"""
    app = create_app()
    
    with app.app_context():
        try:
            print("=" * 60)
            print("测试所有AI面试审核功能")
            print("=" * 60)
            
            # 1. 检查HR用户
            hr_user = User.query.filter_by(email='hr_tech@company.com').first()
            if not hr_user:
                print("❌ 未找到HR用户 hr_tech@company.com")
                return False
            
            print(f"✅ 找到HR用户: {hr_user.first_name}{hr_user.last_name}")
            
            # 2. 检查HR发布的职位
            hr_jobs = Job.query.filter_by(user_id=hr_user.id).all()
            if not hr_jobs:
                print("❌ HR没有发布职位")
                return False
            
            print(f"✅ HR发布了 {len(hr_jobs)} 个职位")
            
            # 3. 检查每个职位的AI面试通过情况
            for job in hr_jobs:
                print(f"\n🔍 检查职位: {job.title}")
                
                # 获取该职位的申请
                applications = Application.query.filter_by(job_id=job.id).all()
                print(f"  总申请数: {len(applications)}")
                
                # 获取通过AI面试的候选人
                passed_count = 0
                for app in applications:
                    interview_schedule = InterviewSchedule.query.filter_by(
                        application_id=app.id
                    ).first()
                    
                    if interview_schedule and interview_schedule.ai_interview_passed:
                        passed_count += 1
                        candidate = User.query.get(app.user_id)
                        print(f"    ✅ {candidate.first_name}{candidate.last_name} - 通过AI面试")
                
                print(f"  通过AI面试: {passed_count} 人")
                
                if passed_count > 0:
                    print(f"  🌐 访问地址: http://localhost:5000/smartrecruit/hr/candidates/review_all_ai_interviews/{job.id}")
            
            # 4. 提供功能说明
            print("\n" + "=" * 60)
            print("🎯 功能说明")
            print("=" * 60)
            
            print(f"\n📋 功能特点:")
            print(f"✅ 在候选人列表页面右上角添加了紫色的'审核AI面试结果'按钮")
            print(f"✅ 点击按钮后显示所有通过AI面试的候选人")
            print(f"✅ 包含统计信息：通过人数、总人数、通过率、平均分数")
            print(f"✅ 详细的候选人列表：姓名、邮箱、电话、AI面试分数、各项评分")
            print(f"✅ 筛选功能：按分数范围、姓名搜索")
            print(f"✅ 操作按钮：详细审核、安排面试")
            
            print(f"\n🎨 界面特色:")
            print(f"• 紫色主题的'审核AI面试结果'按钮")
            print(f"• 统计卡片显示关键数据")
            print(f"• 筛选功能帮助快速找到目标候选人")
            print(f"• 分数徽章用颜色区分不同分数段")
            print(f"• 响应式设计，支持移动端")
            
            print(f"\n🔍 使用流程:")
            print(f"1. 登录HR账号: hr_tech@company.com / 123456")
            print(f"2. 进入候选人管理页面")
            print(f"3. 点击右上角紫色的'审核AI面试结果'按钮")
            print(f"4. 查看所有通过AI面试的候选人成绩")
            print(f"5. 使用筛选功能找到特定候选人")
            print(f"6. 点击'详细审核'或'安排面试'进行操作")
            
            return True
            
        except Exception as e:
            print(f"❌ 测试失败: {e}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == '__main__':
    test_all_ai_review()
