#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
为测试求职者创建AI面试结果
"""

import os
import sys
from datetime import datetime

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from app import create_app, db
from app.models import User, Job, Application
from pymongo import MongoClient

def create_ai_interview_results():
    """为测试求职者创建AI面试结果"""
    app = create_app()
    
    with app.app_context():
        try:
            print("=" * 60)
            print("为测试求职者创建AI面试结果")
            print("=" * 60)
            
            # 连接MongoDB
            try:
                client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=5000)
                db_mongo = client['smartrecruit']
                applications_collection = db_mongo['applications']
                print("✓ MongoDB连接成功")
            except Exception as e:
                print(f"❌ MongoDB连接失败: {e}")
                return False
            
            # 查找测试求职者
            candidate_email = 'candidate_test@email.com'
            candidate = User.query.filter_by(email=candidate_email).first()
            if not candidate:
                print(f"❌ 未找到测试求职者: {candidate_email}")
                return False
            
            print(f"✓ 找到测试求职者: {candidate.first_name}{candidate.last_name}")
            
            # 查找测试职位
            test_job = Job.query.filter_by(title='Python开发工程师').first()
            if not test_job:
                print(f"❌ 未找到测试职位")
                return False
            
            print(f"✓ 找到测试职位: {test_job.title}")
            
            # 查找求职申请
            application = Application.query.filter_by(
                user_id=candidate.id, 
                job_id=test_job.id
            ).first()
            if not application:
                print(f"❌ 未找到求职申请")
                return False
            
            print(f"✓ 找到求职申请，ID: {application.id}")
            
            # 创建AI面试结果
            ai_interview_result = {
                'user_id': str(candidate.id),
                'job_id': str(test_job.id),
                'application_id': str(application.id),
                'type': 'ai_interview_result',
                'status': 'passed',  # 通过AI面试
                'score': 85,  # AI面试分数
                'feedback': '候选人表现出色，技术能力符合要求，沟通能力良好，建议进入下一轮面试。',
                'interview_duration': 25,  # 面试时长（分钟）
                'questions_answered': 8,  # 回答问题数量
                'correct_answers': 7,  # 正确答案数量
                'confidence_score': 0.87,  # 置信度分数
                'emotion_analysis': {
                    'overall_mood': 'positive',
                    'confidence': 'high',
                    'engagement': 'high',
                    'stress_level': 'low'
                },
                'technical_assessment': {
                    'python_knowledge': 'excellent',
                    'framework_experience': 'good',
                    'problem_solving': 'excellent',
                    'code_quality': 'good'
                },
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow()
            }
            
            # 检查是否已存在AI面试结果
            existing_result = applications_collection.find_one({
                'user_id': str(candidate.id),
                'job_id': str(test_job.id),
                'type': 'ai_interview_result'
            })
            
            if existing_result:
                print("✓ AI面试结果已存在，更新结果...")
                applications_collection.update_one(
                    {'_id': existing_result['_id']},
                    {'$set': ai_interview_result}
                )
            else:
                print("✓ 创建新的AI面试结果...")
                applications_collection.insert_one(ai_interview_result)
            
            # 验证结果
            result = applications_collection.find_one({
                'user_id': str(candidate.id),
                'job_id': str(test_job.id),
                'type': 'ai_interview_result'
            })
            
            if result:
                print(f"✓ AI面试结果创建/更新成功！")
                print(f"  状态: {result['status']}")
                print(f"  分数: {result['score']}")
                print(f"  反馈: {result['feedback'][:50]}...")
                print(f"  面试时长: {result['interview_duration']}分钟")
                print(f"  技术评估: Python知识-{result['technical_assessment']['python_knowledge']}")
            else:
                print(f"❌ AI面试结果创建失败")
                return False
            
            # 创建其他几个测试求职者的AI面试结果
            print(f"\n🔧 为其他测试求职者创建AI面试结果...")
            
            other_candidates = [
                'tech_candidate2@email.com',
                'tech_candidate3@email.com',
                'market_candidate1@email.com',
                'market_candidate2@email.com',
                'operation_candidate1@email.com',
                'operation_candidate2@email.com'
            ]
            
            for email in other_candidates:
                candidate = User.query.filter_by(email=email).first()
                if candidate:
                    # 随机生成不同的AI面试结果
                    import random
                    status = random.choice(['passed', 'failed'])
                    score = random.randint(60, 95) if status == 'passed' else random.randint(30, 59)
                    
                    ai_result = {
                        'user_id': str(candidate.id),
                        'job_id': str(test_job.id),
                        'type': 'ai_interview_result',
                        'status': status,
                        'score': score,
                        'feedback': f'候选人{status}，分数{score}分。',
                        'interview_duration': random.randint(20, 30),
                        'questions_answered': random.randint(6, 10),
                        'correct_answers': random.randint(4, 8) if status == 'passed' else random.randint(2, 5),
                        'confidence_score': random.uniform(0.6, 0.95),
                        'created_at': datetime.utcnow(),
                        'updated_at': datetime.utcnow()
                    }
                    
                    # 检查是否已存在
                    existing = applications_collection.find_one({
                        'user_id': str(candidate.id),
                        'job_id': str(test_job.id),
                        'type': 'ai_interview_result'
                    })
                    
                    if existing:
                        applications_collection.update_one(
                            {'_id': existing['_id']},
                            {'$set': ai_result}
                        )
                    else:
                        applications_collection.insert_one(ai_result)
                    
                    print(f"✓ {candidate.first_name}{candidate.last_name}: {status}, 分数{score}")
            
            print(f"\n✅ AI面试结果创建完成！")
            print(f"现在HR可以在候选人管理页面看到AI面试成绩了。")
            
            return True
            
        except Exception as e:
            print(f"❌ 创建AI面试结果失败: {e}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == '__main__':
    create_ai_interview_results()
