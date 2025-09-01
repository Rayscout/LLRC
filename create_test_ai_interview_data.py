#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创建测试AI面试数据的脚本
"""

import os
import sys
from datetime import datetime

# 添加项目根目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from app import create_app, applications_collection
from app.models import User, Job, Application

def create_test_ai_interview_data():
    """创建测试AI面试数据"""
    app = create_app()
    
    with app.app_context():
        print("🔧 开始创建测试AI面试数据...")
        print("=" * 50)
        
        try:
            # 1. 获取HR用户和职位
            hr_users = User.query.filter_by(is_hr=True).all()
            if not hr_users:
                print("❌ 没有找到HR用户")
                return
            
            hr = hr_users[0]  # 使用第一个HR用户
            print(f"📋 使用HR用户: {hr.first_name} {hr.last_name} (ID: {hr.id})")
            
            # 获取该HR的职位
            hr_jobs = Job.query.filter_by(user_id=hr.id).all()
            if not hr_jobs:
                print("❌ 该HR没有发布职位")
                return
            
            print(f"📋 找到 {len(hr_jobs)} 个职位")
            
            # 2. 获取候选人用户
            candidates = User.query.filter_by(is_hr=False).limit(10).all()
            if not candidates:
                print("❌ 没有找到候选人用户")
                return
            
            print(f"📋 找到 {len(candidates)} 个候选人")
            
            # 3. 创建AI面试结果数据
            test_data = []
            scores = [85, 72, 45, 90, 58, 78, 92, 65, 88, 55]  # 不同分数
            
            for i, candidate in enumerate(candidates):
                job = hr_jobs[i % len(hr_jobs)]  # 循环分配职位
                score = scores[i % len(scores)]   # 循环分配分数
                
                # 确保有申请记录
                application = Application.query.filter_by(
                    user_id=candidate.id, 
                    job_id=job.id
                ).first()
                
                if not application:
                    application = Application(
                        user_id=candidate.id,
                        job_id=job.id,
                        message=f'测试申请 - {candidate.first_name}',
                        status='Pending',
                        timestamp=datetime.utcnow()
                    )
                    from app import db
                    db.session.add(application)
                    db.session.commit()
                    print(f"✅ 创建申请记录: {candidate.first_name} -> {job.title}")
                
                # 创建AI面试结果数据
                ai_interview_data = {
                    'user_id': str(candidate.id),
                    'job_id': str(job.id),
                    'type': 'ai_interview_result',
                    'status': 'passed' if score >= 60 else 'failed',
                    'score': score,
                    'technical_score': min(100, score + 2),
                    'communication_score': min(100, int(round(score * 0.9))),
                    'logic_score': min(100, int(round(score * 0.88))),
                    'learning_score': min(100, int(round(score * 0.92))),
                    'feedback': f'测试AI面试反馈 - 候选人{candidate.first_name}表现{"良好" if score >= 60 else "需要改进"}',
                    'created_at': datetime.utcnow(),
                    'interview_date': datetime.utcnow()
                }
                
                test_data.append(ai_interview_data)
                print(f"📝 准备AI面试数据: {candidate.first_name} -> {job.title} (分数: {score})")
            
            # 4. 尝试存储到MongoDB
            print("\n📊 尝试存储到MongoDB...")
            try:
                for data in test_data:
                    applications_collection.insert_one(data)
                print(f"✅ 成功存储 {len(test_data)} 条AI面试数据到MongoDB")
            except Exception as e:
                print(f"⚠️ MongoDB存储失败: {e}")
                print("📝 数据已准备就绪，但MongoDB不可用")
            
            # 5. 显示统计信息
            print("\n📊 测试数据统计:")
            print("-" * 30)
            total_candidates = len(test_data)
            passed_candidates = sum(1 for data in test_data if data['score'] >= 60)
            avg_score = sum(data['score'] for data in test_data) / total_candidates
            pass_rate = (passed_candidates / total_candidates) * 100
            
            print(f"总候选人: {total_candidates}")
            print(f"通过面试: {passed_candidates}")
            print(f"通过率: {pass_rate:.1f}%")
            print(f"平均分数: {avg_score:.1f}")
            
            print("\n" + "=" * 50)
            print("✅ 测试AI面试数据创建完成！")
            print("\n💡 提示:")
            print("1. 如果MongoDB可用，数据已存储到MongoDB")
            print("2. 如果MongoDB不可用，系统会显示模拟数据")
            print("3. 现在可以访问HR AI面试审核页面查看结果")
            
        except Exception as e:
            print(f"❌ 创建测试数据失败: {e}")

if __name__ == '__main__':
    create_test_ai_interview_data()
