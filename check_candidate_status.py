#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查求职者的招聘流程状态
"""

import os
import sys

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from app import create_app, db
from app.models import User, Job, Application, InterviewSchedule

def check_candidate_status():
    """检查求职者的招聘流程状态"""
    app = create_app()
    
    with app.app_context():
        try:
            print("=" * 60)
            print("检查求职者招聘流程状态")
            print("=" * 60)
            
            candidate_email = 'candidate_test@email.com'
            
            # 查找求职者
            candidate = User.query.filter_by(email=candidate_email).first()
            if not candidate:
                print(f"❌ 未找到求职者: {candidate_email}")
                return False
            
            print(f"👤 求职者信息:")
            print(f"  姓名: {candidate.first_name}{candidate.last_name}")
            print(f"  邮箱: {candidate.email}")
            print(f"  应聘职位: {candidate.position}")
            print(f"  技能: {candidate.skills}")
            print(f"  教育背景: {candidate.education}")
            print(f"  工作经验: {candidate.experience}")
            
            # 查找求职申请
            applications = Application.query.filter_by(user_id=candidate.id).all()
            if not applications:
                print(f"\n❌ 未找到求职申请")
                return False
            
            print(f"\n📝 求职申请状态:")
            for i, app in enumerate(applications, 1):
                job = Job.query.get(app.job_id)
                print(f"  申请 {i}:")
                print(f"    职位: {job.title if job else '未知职位'}")
                print(f"    公司: {job.company_name if job else '未知公司'}")
                print(f"    申请状态: {app.status}")
                print(f"    是否激活: {app.is_active}")
                print(f"    申请消息: {app.message[:100]}...")
            
            # 查找面试安排
            interview_schedules = InterviewSchedule.query.filter_by(candidate_id=candidate.id).all()
            if not interview_schedules:
                print(f"\n❌ 未找到面试安排")
            else:
                print(f"\n📅 面试安排状态:")
                for i, schedule in enumerate(interview_schedules, 1):
                    job = Job.query.get(schedule.job_id)
                    hr = User.query.get(schedule.hr_id)
                    print(f"  面试安排 {i}:")
                    print(f"    职位: {job.title if job else '未知职位'}")
                    print(f"    面试时间: {schedule.interview_date} {schedule.start_time}-{schedule.end_time}")
                    print(f"    面试类型: {schedule.interview_type}")
                    print(f"    面试地点: {schedule.location}")
                    print(f"    面试官: {schedule.interviewer_name}")
                    print(f"    面试状态: {schedule.status}")
                    print(f"    AI面试通过: {'✅ 是' if schedule.ai_interview_passed else '❌ 否'}")
                    print(f"    HR手动设置: {'是' if schedule.hr_ai_interview_override else '否'}")
                    print(f"    HR备注: {schedule.hr_ai_interview_notes or '无'}")
                    print(f"    面试备注: {schedule.notes or '无'}")
                    print(f"    通知已发送: {'是' if schedule.notification_sent else '否'}")
            
            # 分析招聘流程状态
            print(f"\n🔍 招聘流程分析:")
            
            # 检查是否有申请
            if applications:
                print(f"  ✅ 第1步: 职位申请 - 已完成")
                
                # 检查申请状态
                pending_apps = [app for app in applications if app.status == 'Pending']
                if pending_apps:
                    print(f"  ✅ 第2步: 申请审核 - 状态: Pending (等待审核)")
                else:
                    print(f"  ✅ 第2步: 申请审核 - 已完成")
                
                # 检查AI面试状态
                if interview_schedules:
                    ai_passed = any(schedule.ai_interview_passed for schedule in interview_schedules)
                    if ai_passed:
                        print(f"  ✅ 第3步: AI面试 - 已完成 (通过)")
                    else:
                        print(f"  ❌ 第3步: AI面试 - 未通过")
                    
                    # 检查是否有面试安排
                    scheduled_interviews = [s for s in interview_schedules if s.status == 'scheduled']
                    if scheduled_interviews:
                        print(f"  ✅ 第4步: 面试安排 - 已完成")
                        print(f"  📋 下一步: 等待面试进行")
                    else:
                        print(f"  ⏳ 第4步: 面试安排 - 待完成")
                else:
                    print(f"  ❌ 第3步: AI面试 - 未找到记录")
                    print(f"  ❌ 第4步: 面试安排 - 无法进行")
            else:
                print(f"  ❌ 第1步: 职位申请 - 未完成")
            
            # 总结当前状态
            print(f"\n📊 当前招聘流程状态总结:")
            if applications and interview_schedules:
                latest_schedule = max(interview_schedules, key=lambda x: x.created_at)
                if latest_schedule.ai_interview_passed and latest_schedule.status == 'scheduled':
                    print(f"  🎯 状态: 已通过AI面试，面试已安排")
                    print(f"  📅 面试时间: {latest_schedule.interview_date} {latest_schedule.start_time}-{latest_schedule.end_time}")
                    print(f"  📍 面试地点: {latest_schedule.location}")
                    print(f"  👔 面试官: {latest_schedule.interviewer_name}")
                    print(f"  📋 下一步: 参加线下面试")
                elif latest_schedule.ai_interview_passed:
                    print(f"  🎯 状态: 已通过AI面试，等待面试安排")
                    print(f"  📋 下一步: HR安排面试时间")
                else:
                    print(f"  🎯 状态: AI面试未通过")
                    print(f"  📋 下一步: 重新参加AI面试或HR手动调整")
            elif applications:
                print(f"  🎯 状态: 申请已提交，等待AI面试")
                print(f"  📋 下一步: 参加AI面试")
            else:
                print(f"  🎯 状态: 未开始招聘流程")
                print(f"  📋 下一步: 提交职位申请")
            
            return True
            
        except Exception as e:
            print(f"❌ 检查失败: {e}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == '__main__':
    check_candidate_status()
