#!/usr/bin/env python3
"""
诊断申请同步问题
分析为什么求职者的申请无法在HR端看到
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import Application, Job, User
from app.sync_service import DataSyncService

def diagnose_applications():
    """诊断申请同步问题"""
    app = create_app()
    
    with app.app_context():
        try:
            print("🔍 开始诊断申请同步问题...")
            print("=" * 60)
            
            # 1. 检查数据库状态
            print("1. 数据库状态检查")
            print("-" * 30)
            
            total_applications = Application.query.count()
            active_applications = Application.query.filter_by(is_active=True).count()
            total_jobs = Job.query.count()
            total_users = User.query.count()
            hr_users = User.query.filter_by(is_hr=True).count()
            
            print(f"✅ 申请总数: {total_applications}")
            print(f"✅ 活跃申请: {active_applications}")
            print(f"✅ 职位总数: {total_jobs}")
            print(f"✅ 用户总数: {total_users}")
            print(f"✅ HR用户数: {hr_users}")
            
            # 2. 检查申请记录详情
            print("\n2. 申请记录详情")
            print("-" * 30)
            
            applications = Application.query.all()
            for app in applications:
                user = User.query.get(app.user_id)
                job = Job.query.get(app.job_id)
                hr_user = User.query.get(job.user_id) if job else None
                
                print(f"申请ID: {app.id}")
                print(f"  求职者: {user.first_name} {user.last_name} (ID: {app.user_id})")
                print(f"  职位: {job.title if job else '未知'} (ID: {app.job_id})")
                print(f"  HR用户: {hr_user.first_name} {hr_user.last_name} (ID: {job.user_id if job else 'N/A'})")
                print(f"  状态: {app.status}")
                print(f"  活跃: {app.is_active}")
                print(f"  时间: {app.timestamp}")
                print(f"  同步时间: {app.last_synced}")
                print()
            
            # 3. 检查HR端查看申请的逻辑
            print("3. HR端查看申请逻辑检查")
            print("-" * 30)
            
            # 检查HR用户4的职位和申请
            hr_user_4 = User.query.get(4)
            if hr_user_4 and hr_user_4.is_hr:
                print(f"HR用户: {hr_user_4.first_name} {hr_user_4.last_name}")
                
                # 获取该HR发布的职位
                hr_jobs = Job.query.filter_by(user_id=4).all()
                print(f"发布的职位数量: {len(hr_jobs)}")
                
                for job in hr_jobs:
                    print(f"  职位: {job.title} (ID: {job.id})")
                    
                    # 获取申请该职位的申请记录
                    job_applications = Application.query.filter_by(job_id=job.id).all()
                    print(f"    申请数量: {len(job_applications)}")
                    
                    for app in job_applications:
                        user = User.query.get(app.user_id)
                        print(f"      申请者: {user.first_name} {user.last_name} (状态: {app.status}, 活跃: {app.is_active})")
            
            # 4. 检查数据同步状态
            print("\n4. 数据同步状态检查")
            print("-" * 30)
            
            # 检查MongoDB连接
            try:
                from app import applications_collection
                if applications_collection:
                    print("✅ MongoDB连接正常")
                    # 检查MongoDB中的数据
                    mongo_count = applications_collection.count_documents({})
                    print(f"✅ MongoDB中的申请记录数: {mongo_count}")
                else:
                    print("⚠️ MongoDB未配置")
            except Exception as e:
                print(f"❌ MongoDB检查失败: {e}")
            
            # 5. 问题分析和建议
            print("\n5. 问题分析和建议")
            print("-" * 30)
            
            if active_applications > 0:
                print("✅ 有活跃的申请记录")
                
                # 检查是否有申请状态为'Pending'的记录
                pending_apps = Application.query.filter_by(status='Pending', is_active=True).all()
                if pending_apps:
                    print(f"✅ 有 {len(pending_apps)} 个待处理的申请")
                    
                    for app in pending_apps:
                        job = Job.query.get(app.job_id)
                        if job:
                            print(f"  申请 {app.id}: 职位 '{job.title}' (HR用户: {job.user_id})")
                else:
                    print("⚠️ 没有待处理的申请")
            else:
                print("❌ 没有活跃的申请记录")
            
            print("\n" + "=" * 60)
            print("诊断完成！")
            
        except Exception as e:
            print(f"❌ 诊断过程中出现错误: {e}")
            import traceback
            print(f"错误追踪:\n{traceback.format_exc()}")

def test_sync_service():
    """测试同步服务"""
    app = create_app()
    
    with app.app_context():
        try:
            print("\n🧪 测试同步服务...")
            print("-" * 30)
            
            # 获取一个活跃的申请
            application = Application.query.filter_by(is_active=True).first()
            if application:
                print(f"测试申请: ID {application.id}")
                
                # 测试同步到HR端
                result = DataSyncService.sync_application_to_hr(application.id)
                if result:
                    print("✅ 同步服务测试成功")
                else:
                    print("❌ 同步服务测试失败")
            else:
                print("⚠️ 没有找到可测试的申请")
                
        except Exception as e:
            print(f"❌ 同步服务测试失败: {e}")

def main():
    """主函数"""
    print("申请同步问题诊断工具")
    print("=" * 60)
    
    # 运行诊断
    diagnose_applications()
    
    # 测试同步服务
    test_sync_service()
    
    print("\n💡 建议:")
    print("1. 检查HR用户是否正确登录")
    print("2. 确认HR用户查看的是自己发布的职位")
    print("3. 检查申请状态是否为'Pending'")
    print("4. 验证数据同步服务是否正常工作")

if __name__ == '__main__':
    main()
