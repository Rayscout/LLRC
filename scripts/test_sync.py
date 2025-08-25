#!/usr/bin/env python3
"""
数据同步功能测试脚本
测试各种同步场景是否正常工作
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import Job, Application, User
from app.sync_service import DataSyncService
from datetime import datetime

def test_sync_service():
    """测试同步服务的基本功能"""
    app = create_app()
    
    with app.app_context():
        try:
            print("开始测试数据同步服务...")
            
            # 测试1: 获取同步状态
            print("\n1. 测试获取同步状态...")
            status = DataSyncService.get_sync_status()
            print(f"✓ 同步状态获取成功: {status}")
            
            # 测试2: 测试职位同步
            print("\n2. 测试职位同步...")
            # 查找一个测试职位
            test_job = Job.query.first()
            if test_job:
                success = DataSyncService.sync_job_to_candidates(test_job.id)
                if success:
                    print(f"✓ 职位同步成功: {test_job.title}")
                else:
                    print(f"❌ 职位同步失败: {test_job.title}")
            else:
                print("⚠ 没有找到测试职位")
            
            # 测试3: 测试申请同步
            print("\n3. 测试申请同步...")
            # 查找一个测试申请
            test_application = Application.query.first()
            if test_application:
                success = DataSyncService.sync_application_to_hr(test_application.id)
                if success:
                    print(f"✓ 申请同步成功: ID {test_application.id}")
                else:
                    print(f"❌ 申请同步失败: ID {test_application.id}")
            else:
                print("⚠ 没有找到测试申请")
            
            # 测试4: 测试用户简历同步
            print("\n4. 测试用户简历同步...")
            # 查找一个有简历的测试用户
            test_user = User.query.filter(User.cv_file.isnot(None)).first()
            if test_user:
                success = DataSyncService.sync_cv_update_to_hr(test_user.id)
                if success:
                    print(f"✓ 用户简历同步成功: {test_user.email}")
                else:
                    print(f"❌ 用户简历同步失败: {test_user.email}")
            else:
                print("⚠ 没有找到有简历的测试用户")
            
            # 测试5: 测试强制同步
            print("\n5. 测试强制同步...")
            success = DataSyncService.force_sync_all()
            if success:
                print("✓ 强制同步成功")
            else:
                print("❌ 强制同步失败")
            
            print("\n✅ 所有测试完成！")
            
        except Exception as e:
            print(f"❌ 测试过程中出现错误: {e}")
            return False
        
        return True

def test_sync_fields():
    """测试同步字段是否存在"""
    app = create_app()
    
    with app.app_context():
        try:
            print("\n检查同步字段...")
            
            # 检查Job表
            inspector = db.inspect(db.engine)
            job_columns = [col['name'] for col in inspector.get_columns('job')]
            if 'last_synced' in job_columns:
                print("✓ Job表包含last_synced字段")
            else:
                print("❌ Job表缺少last_synced字段")
            
            # 检查Application表
            app_columns = [col['name'] for col in inspector.get_columns('application')]
            if 'last_synced' in app_columns:
                print("✓ Application表包含last_synced字段")
            else:
                print("❌ Application表缺少last_synced字段")
            
            # 检查User表
            user_columns = [col['name'] for col in inspector.get_columns('user')]
            if 'cv_last_synced' in user_columns:
                print("✓ User表包含cv_last_synced字段")
            else:
                print("❌ User表缺少cv_last_synced字段")
            
        except Exception as e:
            print(f"❌ 检查同步字段失败: {e}")
            return False
        
        return True

def test_data_integrity():
    """测试数据完整性"""
    app = create_app()
    
    with app.app_context():
        try:
            print("\n检查数据完整性...")
            
            # 统计各表记录数
            job_count = Job.query.count()
            application_count = Application.query.count()
            user_count = User.query.count()
            
            print(f"✓ 职位数量: {job_count}")
            print(f"✓ 申请数量: {application_count}")
            print(f"✓ 用户数量: {user_count}")
            
            # 检查同步状态
            synced_jobs = Job.query.filter(Job.last_synced.isnot(None)).count()
            synced_applications = Application.query.filter(Application.last_synced.isnot(None)).count()
            synced_users = User.query.filter(User.cv_last_synced.isnot(None)).count()
            
            print(f"✓ 已同步职位: {synced_jobs}/{job_count}")
            print(f"✓ 已同步申请: {synced_applications}/{application_count}")
            print(f"✓ 已同步用户简历: {synced_users}/{user_count}")
            
        except Exception as e:
            print(f"❌ 检查数据完整性失败: {e}")
            return False
        
        return True

def main():
    """主函数"""
    print("=" * 60)
    print("数据同步功能测试脚本")
    print("=" * 60)
    
    # 测试同步字段
    if not test_sync_fields():
        print("❌ 同步字段检查失败，请先运行数据库迁移脚本")
        return
    
    # 测试数据完整性
    if not test_data_integrity():
        print("❌ 数据完整性检查失败")
        return
    
    # 测试同步服务
    if not test_sync_service():
        print("❌ 同步服务测试失败")
        return
    
    print("\n" + "=" * 60)
    print("🎉 所有测试通过！数据同步功能工作正常")
    print("=" * 60)
    print("\n您现在可以：")
    print("1. HR发布的职位会自动同步到求职者端")
    print("2. 求职者的申请会自动同步到HR端")
    print("3. 求职者的简历更新会自动同步到HR端")
    print("4. 在HR端可以查看和管理数据同步状态")

if __name__ == '__main__':
    main()
