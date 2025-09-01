#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调试AI面试数据的脚本
"""

import os
import sys

# 添加项目根目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from app import create_app, applications_collection
from app.models import User, Job, Application

def debug_ai_interview_data():
    """调试AI面试数据"""
    app = create_app()
    
    with app.app_context():
        print("🔍 开始调试AI面试数据...")
        print("=" * 50)
        
        # 1. 检查MongoDB中的所有AI面试结果
        print("1. 检查MongoDB中的AI面试结果:")
        print("-" * 30)
        
        try:
            # 查询所有AI面试结果
            all_results = list(applications_collection.find({'type': 'ai_interview_result'}))
            print(f"📊 总共找到 {len(all_results)} 条AI面试结果")
            
            for i, doc in enumerate(all_results):
                print(f"  记录 {i+1}:")
                print(f"    user_id: {doc.get('user_id')} (类型: {type(doc.get('user_id'))})")
                print(f"    job_id: {doc.get('job_id')} (类型: {type(doc.get('job_id'))})")
                print(f"    score: {doc.get('score')}")
                print(f"    status: {doc.get('status')}")
                print(f"    created_at: {doc.get('created_at')}")
                print()
                
        except Exception as e:
            print(f"❌ 查询MongoDB失败: {e}")
        
        # 2. 检查SQL数据库中的用户和职位
        print("2. 检查SQL数据库中的用户和职位:")
        print("-" * 30)
        
        try:
            users = User.query.all()
            jobs = Job.query.all()
            applications = Application.query.all()
            
            print(f"📊 用户数量: {len(users)}")
            print(f"📊 职位数量: {len(jobs)}")
            print(f"📊 申请数量: {len(applications)}")
            
            print("\n用户列表:")
            for user in users[:5]:  # 只显示前5个
                print(f"  ID: {user.id}, 姓名: {user.first_name} {user.last_name}, 邮箱: {user.email}")
            
            print("\n职位列表:")
            for job in jobs[:5]:  # 只显示前5个
                print(f"  ID: {job.id}, 标题: {job.title}, HR: {job.user_id}")
                
        except Exception as e:
            print(f"❌ 查询SQL数据库失败: {e}")
        
        # 3. 检查特定HR的职位
        print("\n3. 检查HR职位:")
        print("-" * 30)
        
        try:
            # 查找HR用户
            hr_users = User.query.filter_by(is_hr=True).all()
            print(f"📊 HR用户数量: {len(hr_users)}")
            
            for hr in hr_users:
                print(f"\nHR: {hr.first_name} {hr.last_name} (ID: {hr.id})")
                hr_jobs = Job.query.filter_by(user_id=hr.id).all()
                print(f"  职位数量: {len(hr_jobs)}")
                
                for job in hr_jobs:
                    print(f"    职位ID: {job.id}, 标题: {job.title}")
                    
                    # 检查该职位的AI面试结果
                    job_results = list(applications_collection.find({
                        'type': 'ai_interview_result',
                        'job_id': str(job.id)
                    }))
                    print(f"    该职位的AI面试结果: {len(job_results)} 条")
                    
        except Exception as e:
            print(f"❌ 查询HR职位失败: {e}")
        
        print("\n" + "=" * 50)
        print("🔍 调试完成")

if __name__ == '__main__':
    debug_ai_interview_data()
