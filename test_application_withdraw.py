#!/usr/bin/env python3
"""
测试撤销后重新申请功能
"""

import os
import sys

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_application_withdraw():
    """测试撤销后重新申请功能"""
    print("=== 测试撤销后重新申请功能 ===\n")
    
    try:
        from app import create_app, db
        from app.models import User, Job, Application
        
        # 创建应用上下文
        app = create_app()
        with app.app_context():
            print("✅ 应用创建成功")
            
            # 获取测试用户和职位
            test_user = User.query.filter_by(user_type='candidate').first()
            test_job = Job.query.first()
            
            if not test_user or not test_job:
                print("❌ 未找到测试用户或职位")
                return
            
            print(f"👤 测试用户: {test_user.first_name} {test_user.last_name}")
            print(f"💼 测试职位: {test_job.title}")
            
            # 清理之前的测试申请
            old_applications = Application.query.filter_by(
                user_id=test_user.id, 
                job_id=test_job.id
            ).all()
            
            for app in old_applications:
                db.session.delete(app)
            db.session.commit()
            print(f"🧹 清理了 {len(old_applications)} 个旧申请")
            
            # 测试1：创建第一个申请
            print("\n=== 测试1：创建第一个申请 ===")
            application1 = Application(
                user_id=test_user.id,
                job_id=test_job.id,
                status='Pending',
                message='测试申请1',
                is_active=True
            )
            db.session.add(application1)
            db.session.commit()
            print(f"✅ 创建申请1，ID: {application1.id}")
            
            # 检查活跃申请数量
            active_count = Application.query.filter_by(
                user_id=test_user.id, 
                job_id=test_job.id, 
                is_active=True
            ).count()
            print(f"📊 活跃申请数量: {active_count}")
            
            # 测试2：尝试创建第二个申请（应该失败）
            print("\n=== 测试2：尝试创建第二个申请（应该失败） ===")
            try:
                application2 = Application(
                    user_id=test_user.id,
                    job_id=test_job.id,
                    status='Pending',
                    message='测试申请2',
                    is_active=True
                )
                db.session.add(application2)
                db.session.commit()
                print("❌ 错误：应该不允许创建第二个活跃申请")
            except Exception as e:
                print(f"✅ 正确：无法创建第二个活跃申请 - {e}")
                db.session.rollback()
            
            # 测试3：撤销第一个申请
            print("\n=== 测试3：撤销第一个申请 ===")
            application1.is_active = False
            application1.status = 'Withdrawn'
            application1.message = f'{application1.message} (已撤销)'
            db.session.commit()
            print(f"✅ 撤销申请1")
            
            # 检查活跃申请数量
            active_count = Application.query.filter_by(
                user_id=test_user.id, 
                job_id=test_job.id, 
                is_active=True
            ).count()
            print(f"📊 撤销后活跃申请数量: {active_count}")
            
            # 测试4：撤销后重新申请（应该成功）
            print("\n=== 测试4：撤销后重新申请（应该成功） ===")
            application3 = Application(
                user_id=test_user.id,
                job_id=test_job.id,
                status='Pending',
                message='测试申请3（重新申请）',
                is_active=True
            )
            db.session.add(application3)
            db.session.commit()
            print(f"✅ 成功创建重新申请，ID: {application3.id}")
            
            # 检查活跃申请数量
            active_count = Application.query.filter_by(
                user_id=test_user.id, 
                job_id=test_job.id, 
                is_active=True
            ).count()
            print(f"📊 重新申请后活跃申请数量: {active_count}")
            
            # 测试5：查看所有申请历史
            print("\n=== 测试5：查看所有申请历史 ===")
            all_applications = Application.query.filter_by(
                user_id=test_user.id, 
                job_id=test_job.id
            ).order_by(Application.timestamp).all()
            
            for i, app in enumerate(all_applications, 1):
                print(f"申请{i}: ID={app.id}, 状态={app.status}, 活跃={app.is_active}, 消息={app.message}")
            
            # 测试6：验证申请计数函数
            print("\n=== 测试6：验证申请计数函数 ===")
            from smartrecruit_system.candidate_module.applications import get_user_applications_count
            count = get_user_applications_count(test_user.id)
            print(f"📊 用户活跃申请总数: {count}")
            
            print("\n✅ 所有测试完成")
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_application_withdraw()
