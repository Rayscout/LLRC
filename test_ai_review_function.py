#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试AI面试审核功能
"""

import os
import sys

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from app import create_app, db
from app.models import User, Job, Application, InterviewSchedule

def test_ai_review_function():
    """测试AI面试审核功能"""
    app = create_app()
    
    with app.app_context():
        try:
            print("=" * 60)
            print("测试AI面试审核功能")
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
            
            # 3. 检查申请记录
            applications = []
            for job in hr_jobs:
                job_applications = Application.query.filter_by(job_id=job.id).all()
                applications.extend(job_applications)
            
            if not applications:
                print("❌ 没有申请记录")
                return False
            
            print(f"✅ 找到 {len(applications)} 个申请记录")
            
            # 4. 检查面试安排
            interviews = InterviewSchedule.query.filter_by(hr_id=hr_user.id).all()
            print(f"✅ 找到 {len(interviews)} 个面试安排")
            
            # 5. 显示测试数据
            print(f"\n📊 测试数据概览:")
            for i, interview in enumerate(interviews[:3], 1):  # 只显示前3个
                candidate = User.query.get(interview.candidate_id)
                job = Job.query.get(interview.job_id)
                print(f"  {i}. 候选人: {candidate.first_name}{candidate.last_name}")
                print(f"     职位: {job.title}")
                print(f"     AI面试通过: {interview.ai_interview_passed}")
                print(f"     申请ID: {interview.application_id}")
                print()
            
            # 6. 提供测试指南
            print("=" * 60)
            print("🎯 功能测试指南")
            print("=" * 60)
            
            print(f"\n🌐 访问地址:")
            print(f"1. 主页: http://localhost:5000")
            print(f"2. 登录HR账号: hr_tech@company.com / 123456")
            print(f"3. 选择用户类型: HR")
            print(f"4. 进入候选人管理页面")
            print(f"5. 点击'审核AI面试结果'按钮")
            
            print(f"\n🔍 测试步骤:")
            print(f"1. 在候选人列表页面，您会看到绿色的'审核AI面试结果'按钮")
            print(f"2. 点击按钮进入审核页面")
            print(f"3. 查看候选人的AI面试成绩和详细评分")
            print(f"4. 选择审核结果（通过/不通过）")
            print(f"5. 添加审核备注")
            print(f"6. 提交审核结果")
            
            print(f"\n📋 功能特点:")
            print(f"✅ 简洁清晰的界面设计")
            print(f"✅ 直观的AI面试成绩显示")
            print(f"✅ 简单的审核操作流程")
            print(f"✅ 详细的候选人信息展示")
            print(f"✅ 响应式设计，支持移动端")
            
            print(f"\n🎨 界面特色:")
            print(f"• 圆形分数显示，颜色区分不同分数段")
            print(f"• 清晰的状态标签（通过/不通过）")
            print(f"• 简洁的表单设计")
            print(f"• 友好的用户交互")
            
            return True
            
        except Exception as e:
            print(f"❌ 测试失败: {e}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == '__main__':
    test_ai_review_function()
