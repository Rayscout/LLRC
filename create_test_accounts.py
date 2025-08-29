#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创建测试账号脚本
用于验证HR手动设置AI面试状态功能
"""

import os
import sys
from datetime import datetime, date

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from app import create_app, db
from app.models import User, Job, Application
from werkzeug.security import generate_password_hash

def create_test_accounts():
    """创建测试账号"""
    app = create_app()
    
    with app.app_context():
        try:
            print("=" * 60)
            print("创建测试账号脚本")
            print("=" * 60)
            
            # 检查是否已存在测试账号
            existing_hr = User.query.filter_by(email='hr_test@company.com').first()
            if existing_hr:
                print("⚠️  测试HR账号已存在，跳过创建")
                hr_user = existing_hr
            else:
                # 创建HR测试账号
                print("创建HR测试账号...")
                hr_user = User(
                    first_name='张',
                    last_name='HR',
                    company_name='测试公司',
                    position='人力资源经理',
                    email='hr_test@company.com',
                    phone_number='13800138001',
                    birthday='1990-01-01',
                    password=generate_password_hash('123456'),
                    is_hr=True,
                    user_type='employee',
                    department='人力资源部',
                    employee_id='HR001',
                    bio='测试用HR账号，用于验证面试安排功能',
                    skills='招聘,面试,人才管理',
                    education='人力资源管理专业',
                    experience='5年HR经验'
                )
                db.session.add(hr_user)
                db.session.commit()
                print("✓ HR测试账号创建成功")
                print(f"  邮箱: {hr_user.email}")
                print(f"  密码: 123456")
            
            # 创建测试职位
            existing_job = Job.query.filter_by(title='Python开发工程师').first()
            if existing_job:
                print("⚠️  测试职位已存在，跳过创建")
                test_job = existing_job
            else:
                print("创建测试职位...")
                test_job = Job(
                    title='Python开发工程师',
                    company_name='测试公司',
                    location='北京',
                    description='负责公司核心系统的Python开发工作，要求熟悉Django、Flask等框架',
                    requirements='1. 本科及以上学历，计算机相关专业\n2. 3年以上Python开发经验\n3. 熟悉Django、Flask等Web框架\n4. 熟悉MySQL、MongoDB等数据库',
                    salary='15k-25k',
                    job_type='全职',
                    experience_level='中级',
                    positions_needed=2,
                    min_age=22,
                    max_age=35,
                    education_requirement='本科及以上',
                    experience_years=3,
                    skills_required='Python,Django,Flask,MySQL,MongoDB',
                    benefits='五险一金,年终奖,带薪年假',
                    contact_email='hr_test@company.com',
                    contact_phone='13800138001',
                    department='技术部',
                    user_id=hr_user.id
                )
                db.session.add(test_job)
                db.session.commit()
                print("✓ 测试职位创建成功")
                print(f"  职位: {test_job.title}")
                print(f"  薪资: {test_job.salary}")
            
            # 创建求职者测试账号
            candidates_data = [
                {
                    'first_name': '李',
                    'last_name': '小明',
                    'email': 'candidate1@email.com',
                    'phone': '13800138002',
                    'position': 'Python开发工程师',
                    'skills': 'Python,Django,MySQL,JavaScript',
                    'education': '计算机科学与技术 本科',
                    'experience': '3年Python开发经验，熟悉Web开发流程'
                },
                {
                    'first_name': '王',
                    'last_name': '小红',
                    'email': 'candidate2@email.com',
                    'phone': '13800138003',
                    'position': 'Python开发工程师',
                    'skills': 'Python,Flask,MongoDB,React',
                    'education': '软件工程 本科',
                    'experience': '2年Python开发经验，有前端开发基础'
                },
                {
                    'first_name': '陈',
                    'last_name': '小华',
                    'email': 'candidate3@email.com',
                    'phone': '13800138004',
                    'position': 'Python开发工程师',
                    'skills': 'Python,数据分析,机器学习',
                    'education': '数据科学 硕士',
                    'experience': '4年Python开发经验，专注数据分析和机器学习'
                }
            ]
            
            created_candidates = []
            for i, candidate_data in enumerate(candidates_data, 1):
                existing_candidate = User.query.filter_by(email=candidate_data['email']).first()
                if existing_candidate:
                    print(f"⚠️  求职者账号 {candidate_data['email']} 已存在，跳过创建")
                    created_candidates.append(existing_candidate)
                    continue
                
                print(f"创建求职者账号 {i}...")
                candidate = User(
                    first_name=candidate_data['first_name'],
                    last_name=candidate_data['last_name'],
                    company_name='待业',
                    position=candidate_data['position'],
                    email=candidate_data['email'],
                    phone_number=candidate_data['phone'],
                    birthday='1995-01-01',
                    password=generate_password_hash('123456'),
                    is_hr=False,
                    user_type='candidate',
                    bio=f'测试用求职者账号{i}，用于验证面试安排功能',
                    skills=candidate_data['skills'],
                    education=candidate_data['education'],
                    experience=candidate_data['experience']
                )
                db.session.add(candidate)
                db.session.commit()
                
                # 创建求职申请
                application = Application(
                    user_id=candidate.id,
                    job_id=test_job.id,
                    message=f'我对{test_job.title}职位很感兴趣，希望能有机会面试。我有{candidate_data["experience"]}，相信能够胜任这个职位。',
                    status='Pending',
                    is_active=True
                )
                db.session.add(application)
                db.session.commit()
                
                created_candidates.append(candidate)
                print(f"✓ 求职者账号 {i} 创建成功")
                print(f"  邮箱: {candidate.email}")
                print(f"  密码: 123456")
                print(f"  申请状态: {application.status}")
            
            print("\n" + "=" * 40)
            print("测试账号创建完成！")
            print("=" * 40)
            
            print("\n📋 账号信息汇总:")
            print(f"HR账号: {hr_user.email} (密码: 123456)")
            print(f"测试职位: {test_job.title}")
            print(f"求职者账号数量: {len(created_candidates)}")
            
            print("\n🔐 登录信息:")
            print("HR账号:")
            print(f"  邮箱: {hr_user.email}")
            print(f"  密码: 123456")
            print(f"  权限: HR用户")
            
            print("\n求职者账号:")
            for i, candidate in enumerate(created_candidates, 1):
                print(f"  {i}. 邮箱: {candidate.email}")
                print(f"     密码: 123456")
                print(f"     姓名: {candidate.first_name}{candidate.last_name}")
            
            print("\n📝 测试步骤:")
            print("1. 使用HR账号登录系统")
            print("2. 进入候选人管理页面")
            print("3. 查看求职者申请")
            print("4. 点击'安排面试'按钮")
            print("5. 测试HR手动设置AI面试状态功能")
            
            print("\n🎯 功能验证要点:")
            print("- 检查HR手动设置AI面试状态开关是否正常")
            print("- 验证状态选择和备注输入功能")
            print("- 测试面试安排表单提交")
            print("- 确认数据库记录是否正确保存")
            
            return True
            
        except Exception as e:
            print(f"✗ 创建测试账号失败: {e}")
            db.session.rollback()
            return False

def create_ai_interview_results():
    """创建模拟的AI面试结果数据"""
    app = create_app()
    
    with app.app_context():
        try:
            print("\n创建模拟AI面试结果...")
            
            # 获取所有求职者
            candidates = User.query.filter_by(is_hr=False).all()
            test_job = Job.query.filter_by(title='Python开发工程师').first()
            
            if not candidates or not test_job:
                print("⚠️  没有找到求职者或测试职位，跳过AI面试结果创建")
                return False
            
            from app import applications_collection
            
            # 为每个求职者创建AI面试结果
            for i, candidate in enumerate(candidates):
                # 模拟不同的AI面试结果
                if i == 0:  # 第一个候选人通过
                    status = 'passed'
                    score = 85
                    feedback = '候选人技术基础扎实，Python编程能力较强，沟通表达清晰，建议进入下一轮面试。'
                elif i == 1:  # 第二个候选人未通过
                    status = 'failed'
                    score = 62
                    feedback = '候选人技术基础一般，项目经验不足，建议加强学习后再考虑。'
                else:  # 第三个候选人通过
                    status = 'passed'
                    score = 78
                    feedback = '候选人学习能力强，有数据分析背景，技术栈匹配度较高，建议进入下一轮面试。'
                
                # 创建AI面试结果文档
                ai_result = {
                    'user_id': str(candidate.id),
                    'job_id': str(test_job.id),
                    'type': 'ai_interview_result',
                    'status': status,
                    'score': score,
                    'feedback': feedback,
                    'created_at': datetime.utcnow(),
                    'interview_questions': [
                        '请介绍一下你的Python开发经验',
                        '你熟悉哪些Web框架？',
                        '请描述一个你参与过的项目',
                        '你对数据库优化有什么了解？'
                    ],
                    'candidate_responses': [
                        f'我有{candidate.experience}，主要使用Python进行Web开发。',
                        '我熟悉Django和Flask框架，有实际项目经验。',
                        '我参与过电商平台的开发，负责后端API设计和实现。',
                        '我了解MySQL索引优化和查询性能调优。'
                    ]
                }
                
                # 检查是否已存在
                existing = applications_collection.find_one({
                    'user_id': str(candidate.id),
                    'job_id': str(test_job.id),
                    'type': 'ai_interview_result'
                })
                
                if existing:
                    print(f"⚠️  {candidate.email} 的AI面试结果已存在，跳过创建")
                else:
                    applications_collection.insert_one(ai_result)
                    print(f"✓ {candidate.email} 的AI面试结果创建成功")
                    print(f"  状态: {status}")
                    print(f"  评分: {score}/100")
            
            print("✓ 模拟AI面试结果创建完成")
            return True
            
        except Exception as e:
            print(f"✗ 创建AI面试结果失败: {e}")
            return False

if __name__ == '__main__':
    try:
        # 创建测试账号
        if create_test_accounts():
            print("\n🎉 测试账号创建成功！")
            
            # 创建模拟AI面试结果
            if create_ai_interview_results():
                print("🎉 模拟AI面试结果创建成功！")
            else:
                print("⚠️  模拟AI面试结果创建失败，但不影响基本功能测试")
            
            print("\n📋 下一步操作:")
            print("1. 启动Flask应用: python run.py")
            print("2. 使用HR账号登录: hr_test@company.com / 123456")
            print("3. 进入候选人管理页面测试功能")
            
        else:
            print("❌ 测试账号创建失败")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ 脚本执行失败: {e}")
        sys.exit(1)



