#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创建简化测试账号脚本
包括HR账号、求职者账号、职位、申请记录和AI面试结果
"""

import os
import sys
from datetime import datetime, date, timedelta

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from app import create_app, db
from app.models import User, Job, Application, InterviewSchedule
from werkzeug.security import generate_password_hash

def main():
    """主函数"""
    app = create_app()
    
    with app.app_context():
        try:
            print("🚀 开始创建完整测试数据...")
            print("=" * 60)
            
            # 1. 创建HR账号
            print("创建HR测试账号...")
            hr_accounts = []
            
            # HR账号1 - 技术部HR
            hr1_email = 'hr_tech@company.com'
            existing_hr1 = User.query.filter_by(email=hr1_email).first()
            if existing_hr1:
                print(f"⚠️  HR账号 {hr1_email} 已存在，跳过创建")
                hr_accounts.append(existing_hr1)
            else:
                hr1 = User(
                    first_name='张',
                    last_name='技术HR',
                    company_name='科技公司A',
                    position='技术招聘经理',
                    email=hr1_email,
                    phone_number='13800138001',
                    birthday='1990-01-01',
                    password=generate_password_hash('123456'),
                    is_hr=True,
                    user_type='recruiter',
                    department='技术部',
                    employee_id='HR001',
                    bio='技术部HR，负责技术岗位招聘',
                    skills='技术招聘,面试,人才评估',
                    education='人力资源管理专业',
                    experience='5年技术招聘经验'
                )
                db.session.add(hr1)
                db.session.commit()
                hr_accounts.append(hr1)
                print(f"✓ HR账号1创建成功: {hr1.email} (密码: 123456)")
            
            # HR账号2 - 市场部HR
            hr2_email = 'hr_market@company.com'
            existing_hr2 = User.query.filter_by(email=hr2_email).first()
            if existing_hr2:
                print(f"⚠️  HR账号 {hr2_email} 已存在，跳过创建")
                hr_accounts.append(existing_hr2)
            else:
                hr2 = User(
                    first_name='李',
                    last_name='市场HR',
                    company_name='科技公司A',
                    position='市场招聘经理',
                    email=hr2_email,
                    phone_number='13800138002',
                    birthday='1990-02-01',
                    password=generate_password_hash('123456'),
                    is_hr=True,
                    user_type='recruiter',
                    department='市场部',
                    employee_id='HR002',
                    bio='市场部HR，负责市场岗位招聘',
                    skills='市场招聘,品牌推广,人才管理',
                    education='市场营销专业',
                    experience='4年市场招聘经验'
                )
                db.session.add(hr2)
                db.session.commit()
                hr_accounts.append(hr2)
                print(f"✓ HR账号2创建成功: {hr2.email} (密码: 123456)")
            
            # HR账号3 - 运营部HR
            hr3_email = 'hr_operation@company.com'
            existing_hr3 = User.query.filter_by(email=hr3_email).first()
            if existing_hr3:
                print(f"⚠️  HR账号 {hr3_email} 已存在，跳过创建")
                hr_accounts.append(existing_hr3)
            else:
                hr3 = User(
                    first_name='王',
                    last_name='运营HR',
                    company_name='科技公司A',
                    position='运营招聘经理',
                    email=hr3_email,
                    phone_number='13800138003',
                    birthday='1990-03-01',
                    password=generate_password_hash('123456'),
                    is_hr=True,
                    user_type='recruiter',
                    department='运营部',
                    employee_id='HR003',
                    bio='运营部HR，负责运营岗位招聘',
                    skills='运营招聘,数据分析,流程优化',
                    education='工商管理专业',
                    experience='6年运营招聘经验'
                )
                db.session.add(hr3)
                db.session.commit()
                hr_accounts.append(hr3)
                print(f"✓ HR账号3创建成功: {hr3.email} (密码: 123456)")
            
            print(f"✓ 共创建/获取 {len(hr_accounts)} 个HR账号")
            
            # 2. 创建职位
            print("\n创建测试职位...")
            jobs = []
            
            # 技术职位
            tech_job_title = 'Python高级开发工程师'
            existing_tech_job = Job.query.filter_by(title=tech_job_title).first()
            if existing_tech_job:
                print(f"⚠️  职位 {tech_job_title} 已存在，跳过创建")
                jobs.append(existing_tech_job)
            else:
                tech_job = Job(
                    title=tech_job_title,
                    company_name='科技公司A',
                    location='北京',
                    description='负责公司核心系统的Python开发工作，要求熟悉Django、Flask等框架，有微服务架构经验',
                    requirements='1. 本科及以上学历，计算机相关专业\n2. 5年以上Python开发经验\n3. 熟悉Django、Flask等Web框架\n4. 熟悉MySQL、MongoDB、Redis等数据库\n5. 有微服务架构和Docker经验',
                    salary='25k-40k',
                    job_type='全职',
                    experience_level='高级',
                    positions_needed=2,
                    min_age=25,
                    max_age=35,
                    education_requirement='本科及以上',
                    experience_years=5,
                    skills_required='Python,Django,Flask,MySQL,MongoDB,Redis,Docker,微服务',
                    benefits='五险一金,年终奖,带薪年假,股票期权',
                    contact_email=hr_accounts[0].email,
                    contact_phone=hr_accounts[0].phone_number,
                    department='技术部',
                    user_id=hr_accounts[0].id
                )
                db.session.add(tech_job)
                db.session.commit()
                jobs.append(tech_job)
                print(f"✓ 技术职位创建成功: {tech_job.title} (薪资: {tech_job.salary})")
            
            # 市场职位
            market_job_title = '市场推广经理'
            existing_market_job = Job.query.filter_by(title=market_job_title).first()
            if existing_market_job:
                print(f"⚠️  职位 {market_job_title} 已存在，跳过创建")
                jobs.append(existing_market_job)
            else:
                market_job = Job(
                    title=market_job_title,
                    company_name='科技公司A',
                    location='上海',
                    description='负责公司产品的市场推广策略制定和执行，包括品牌建设、渠道拓展、活动策划等',
                    requirements='1. 本科及以上学历，市场营销相关专业\n2. 3年以上市场推广经验\n3. 熟悉数字营销、社交媒体推广\n4. 有品牌建设和活动策划经验\n5. 良好的沟通协调能力',
                    salary='18k-30k',
                    job_type='全职',
                    experience_level='中级',
                    positions_needed=1,
                    min_age=24,
                    max_age=32,
                    education_requirement='本科及以上',
                    experience_years=3,
                    skills_required='市场推广,品牌建设,数字营销,活动策划,数据分析',
                    benefits='五险一金,年终奖,带薪年假,交通补贴',
                    contact_email=hr_accounts[1].email,
                    contact_phone=hr_accounts[1].phone_number,
                    department='市场部',
                    user_id=hr_accounts[1].id
                )
                db.session.add(market_job)
                db.session.commit()
                jobs.append(market_job)
                print(f"✓ 市场职位创建成功: {market_job.title} (薪资: {market_job.salary})")
            
            # 运营职位
            operation_job_title = '数据分析运营专员'
            existing_operation_job = Job.query.filter_by(title=operation_job_title).first()
            if existing_operation_job:
                print(f"⚠️  职位 {operation_job_title} 已存在，跳过创建")
                jobs.append(existing_operation_job)
            else:
                operation_job = Job(
                    title=operation_job_title,
                    company_name='科技公司A',
                    location='深圳',
                    description='负责公司运营数据的收集、分析和报告，为业务决策提供数据支持',
                    requirements='1. 本科及以上学历，统计学、数学或相关专业\n2. 2年以上数据分析经验\n3. 熟悉SQL、Python、Excel等工具\n4. 有运营数据分析经验\n5. 良好的逻辑思维和表达能力',
                    salary='15k-25k',
                    job_type='全职',
                    experience_level='初级',
                    positions_needed=2,
                    min_age=22,
                    max_age=30,
                    education_requirement='本科及以上',
                    experience_years=2,
                    skills_required='数据分析,SQL,Python,Excel,运营分析,报告撰写',
                    benefits='五险一金,年终奖,带薪年假,培训机会',
                    contact_email=hr_accounts[2].email,
                    contact_phone=hr_accounts[2].phone_number,
                    department='运营部',
                    user_id=hr_accounts[2].id
                )
                db.session.add(operation_job)
                db.session.commit()
                jobs.append(operation_job)
                print(f"✓ 运营职位创建成功: {operation_job.title} (薪资: {operation_job.salary})")
            
            print(f"✓ 共创建/获取 {len(jobs)} 个职位")
            
            # 3. 创建求职者和申请记录
            print("\n创建求职者账号和申请记录...")
            candidates = []
            applications = []
            
            # 技术岗位求职者
            tech_candidates_data = [
                {
                    'first_name': '陈',
                    'last_name': '技术强',
                    'email': 'tech_candidate1@email.com',
                    'phone': '13800138101',
                    'position': 'Python高级开发工程师',
                    'skills': 'Python,Django,Flask,MySQL,MongoDB,Redis,Docker,微服务',
                    'education': '计算机科学与技术 硕士',
                    'experience': '6年Python开发经验，有微服务架构设计经验'
                },
                {
                    'first_name': '刘',
                    'last_name': '代码王',
                    'email': 'tech_candidate2@email.com',
                    'phone': '13800138102',
                    'position': 'Python高级开发工程师',
                    'skills': 'Python,Django,Flask,MySQL,PostgreSQL,Redis,AWS',
                    'education': '软件工程 本科',
                    'experience': '5年Python开发经验，熟悉云服务部署'
                },
                {
                    'first_name': '张',
                    'last_name': '架构师',
                    'email': 'tech_candidate3@email.com',
                    'phone': '13800138103',
                    'position': 'Python高级开发工程师',
                    'skills': 'Python,Django,Flask,MySQL,MongoDB,Redis,Docker,Kubernetes',
                    'education': '计算机科学与技术 本科',
                    'experience': '7年Python开发经验，专注系统架构设计'
                }
            ]
            
            # 市场岗位求职者
            market_candidates_data = [
                {
                    'first_name': '赵',
                    'last_name': '市场达人',
                    'email': 'market_candidate1@email.com',
                    'phone': '13800138104',
                    'position': '市场推广经理',
                    'skills': '市场推广,品牌建设,数字营销,活动策划,数据分析',
                    'education': '市场营销 本科',
                    'experience': '4年市场推广经验，有成功品牌推广案例'
                },
                {
                    'first_name': '孙',
                    'last_name': '推广专家',
                    'email': 'market_candidate2@email.com',
                    'phone': '13800138105',
                    'position': '市场推广经理',
                    'skills': '市场推广,社交媒体,内容营销,用户增长,数据分析',
                    'education': '广告学 本科',
                    'experience': '3年市场推广经验，专注数字营销'
                }
            ]
            
            # 运营岗位求职者
            operation_candidates_data = [
                {
                    'first_name': '周',
                    'last_name': '数据专家',
                    'email': 'operation_candidate1@email.com',
                    'phone': '13800138106',
                    'position': '数据分析运营专员',
                    'skills': '数据分析,SQL,Python,Excel,运营分析,报告撰写',
                    'education': '统计学 本科',
                    'experience': '3年数据分析经验，有电商运营分析经验'
                },
                {
                    'first_name': '吴',
                    'last_name': '运营能手',
                    'email': 'operation_candidate2@email.com',
                    'phone': '13800138107',
                    'position': '数据分析运营专员',
                    'skills': '数据分析,SQL,Python,R,运营分析,可视化',
                    'education': '数学与应用数学 本科',
                    'experience': '2年数据分析经验，熟悉数据可视化'
                }
            ]
            
            all_candidates_data = tech_candidates_data + market_candidates_data + operation_candidates_data
            
            for i, candidate_data in enumerate(all_candidates_data, 1):
                existing_candidate = User.query.filter_by(email=candidate_data['email']).first()
                if existing_candidate:
                    print(f"⚠️  求职者账号 {candidate_data['email']} 已存在，跳过创建")
                    candidates.append(existing_candidate)
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
                    bio=f'求职者账号{i}，应聘{candidate_data["position"]}职位',
                    skills=candidate_data['skills'],
                    education=candidate_data['education'],
                    experience=candidate_data['experience']
                )
                db.session.add(candidate)
                db.session.commit()
                
                # 创建求职申请 - 根据职位类型分配
                if 'tech' in candidate_data['email']:
                    target_job = jobs[0]  # 技术职位
                elif 'market' in candidate_data['email']:
                    target_job = jobs[1]  # 市场职位
                else:
                    target_job = jobs[2]  # 运营职位
                
                application = Application(
                    user_id=candidate.id,
                    job_id=target_job.id,
                    message=f'我对{target_job.title}职位很感兴趣。我有{candidate_data["experience"]}，技能包括{candidate_data["skills"]}，相信能够胜任这个职位。',
                    status='Pending',
                    is_active=True
                )
                db.session.add(application)
                db.session.commit()
                
                candidates.append(candidate)
                applications.append(application)
                print(f"✓ 求职者账号 {i} 创建成功")
                print(f"  邮箱: {candidate.email}")
                print(f"  密码: 123456")
                print(f"  应聘职位: {target_job.title}")
                print(f"  申请状态: {application.status}")
            
            print(f"\n✓ 共创建/获取 {len(candidates)} 个求职者账号")
            print(f"✓ 共创建 {len(applications)} 个求职申请")
            
            # 4. 创建AI面试结果
            print("\n创建AI面试结果数据...")
            ai_results = []
            
            for i, candidate in enumerate(candidates):
                # 根据求职者类型分配不同的AI面试结果
                if 'tech' in candidate.email:
                    # 技术岗位 - 大部分通过
                    if i % 3 == 0:  # 每3个中1个不通过
                        status = 'failed'
                        score = 65 + (i % 20)  # 65-84分
                        feedback = '候选人技术基础一般，项目经验不足，建议加强学习后再考虑。'
                    else:
                        status = 'passed'
                        score = 75 + (i % 25)  # 75-99分
                        feedback = '候选人技术基础扎实，编程能力较强，项目经验丰富，建议进入下一轮面试。'
                        
                elif 'market' in candidate.email:
                    # 市场岗位 - 全部通过
                    status = 'passed'
                    score = 80 + (i % 20)  # 80-99分
                    feedback = '候选人市场推广经验丰富，沟通能力强，有成功案例，建议进入下一轮面试。'
                    
                elif 'operation' in candidate.email:
                    # 运营岗位 - 全部通过
                    status = 'passed'
                    score = 78 + (i % 22)  # 78-99分
                    feedback = '候选人数据分析能力强，逻辑思维清晰，有相关工作经验，建议进入下一轮面试。'
                    
                else:
                    # 默认情况
                    status = 'passed'
                    score = 75 + (i % 20)
                    feedback = '候选人综合素质良好，符合岗位要求，建议进入下一轮面试。'
                
                # 找到对应的职位
                if 'tech' in candidate.email:
                    target_job = jobs[0]  # 技术职位
                elif 'market' in candidate.email:
                    target_job = jobs[1]  # 市场职位
                else:
                    target_job = jobs[2]  # 运营职位
                
                # 创建AI面试结果
                ai_result = {
                    'user_id': str(candidate.id),
                    'job_id': str(target_job.id),
                    'type': 'ai_interview_result',
                    'status': status,
                    'score': score,
                    'feedback': feedback,
                    'created_at': datetime.utcnow() - timedelta(days=1),  # 1天前完成
                    'interview_questions': [
                        '请介绍一下你的相关工作经验',
                        '你熟悉哪些相关技能？',
                        '请描述一个你参与过的项目',
                        '你对这个岗位的理解是什么？'
                    ],
                    'candidate_responses': [
                        f'我有{candidate.experience}，主要专注于{candidate.position}相关工作。',
                        f'我熟悉{candidate.skills}等技能，有实际项目应用经验。',
                        '我参与过多个重要项目，负责核心功能的设计和实现。',
                        f'我认为{candidate.position}需要具备专业技能和良好的沟通能力。'
                    ],
                    'interview_duration': 25 + (i % 10),  # 25-34分钟
                    'confidence_score': 0.7 + (i % 3) * 0.1,  # 0.7-0.9
                    'technical_score': score / 100.0,
                    'communication_score': 0.6 + (i % 4) * 0.1,  # 0.6-0.9
                    'overall_rating': '优秀' if score >= 85 else '良好' if score >= 75 else '一般'
                }
                
                ai_results.append(ai_result)
                print(f"✓ {candidate.email} 的AI面试结果创建成功")
                print(f"  状态: {status}")
                print(f"  评分: {score}/100")
                print(f"  总体评级: {ai_result['overall_rating']}")
            
            print(f"\n✓ 共创建 {len(ai_results)} 个AI面试结果")
            
            # 5. 创建面试安排
            print("\n创建面试安排记录...")
            schedules = []
            
            # 为通过AI面试的候选人创建面试安排
            passed_candidates = [c for c in candidates if 'tech_candidate2' in c.email or 'market_candidate1' in c.email or 'operation_candidate1' in c.email]
            
            for i, candidate in enumerate(passed_candidates):
                # 找到对应的职位和HR
                if 'tech' in candidate.email:
                    target_job = jobs[0]  # 技术职位
                    target_hr = hr_accounts[0]  # 技术部HR
                elif 'market' in candidate.email:
                    target_job = jobs[1]  # 市场职位
                    target_hr = hr_accounts[1]  # 市场部HR
                elif 'operation' in candidate.email:
                    target_job = jobs[2]  # 运营职位
                    target_hr = hr_accounts[2]  # 运营部HR
                
                # 创建面试安排
                interview_date = date.today() + timedelta(days=3 + i)  # 3天后开始，每天一个
                start_time = datetime.strptime('14:00', '%H:%M').time()
                end_time = datetime.strptime('15:00', '%H:%M').time()
                
                schedule = InterviewSchedule(
                    application_id=candidate.id,  # 简化处理
                    candidate_id=candidate.id,
                    job_id=target_job.id,
                    hr_id=target_hr.id,
                    interview_date=interview_date,
                    start_time=start_time,
                    end_time=end_time,
                    interview_type='offline',
                    location='公司会议室A',
                    interviewer_name=f'{target_hr.first_name}{target_hr.last_name}',
                    notes=f'{candidate.first_name}{candidate.last_name}的面试安排',
                    status='scheduled',
                    ai_interview_passed=True,
                    hr_ai_interview_override=False,
                    hr_ai_interview_notes=''
                )
                
                db.session.add(schedule)
                db.session.commit()
                schedules.append(schedule)
                
                print(f"✓ {candidate.email} 的面试安排创建成功")
                print(f"  面试时间: {interview_date} {start_time}-{end_time}")
                print(f"  面试官: {schedule.interviewer_name}")
            
            print(f"\n✓ 共创建 {len(schedules)} 个面试安排")
            
            print("\n" + "=" * 60)
            print("🎉 完整测试数据创建完成！")
            print("=" * 60)
            
            print("\n📋 数据汇总:")
            print(f"HR账号数量: {len(hr_accounts)}")
            print(f"职位数量: {len(jobs)}")
            print(f"求职者数量: {len(candidates)}")
            print(f"申请记录数量: {len(applications)}")
            print(f"AI面试结果数量: {len(ai_results)}")
            print(f"面试安排数量: {len(schedules)}")
            
            print("\n🔐 登录信息:")
            print("\nHR账号:")
            for i, hr in enumerate(hr_accounts, 1):
                print(f"  {i}. {hr.email} (密码: 123456)")
                print(f"     部门: {hr.department}")
                print(f"     职位: {hr.position}")
            
            print("\n求职者账号:")
            for i, candidate in enumerate(candidates, 1):
                print(f"  {i}. {candidate.email} (密码: 123456)")
                print(f"     姓名: {candidate.first_name}{candidate.last_name}")
                print(f"     应聘职位: {candidate.position}")
            
            print("\n📝 测试步骤:")
            print("1. 启动Flask应用: python run.py")
            print("2. 使用任意HR账号登录系统")
            print("3. 进入候选人管理页面")
            print("4. 查看求职者申请和AI面试结果")
            print("5. 测试面试安排功能")
            
            print("\n🎯 功能验证要点:")
            print("- 检查AI面试结果是否正确显示")
            print("- 验证HR手动设置AI面试状态功能")
            print("- 测试面试安排表单提交")
            print("- 确认面试安排记录是否正确保存")
            
            return True
            
        except Exception as e:
            print(f"❌ 脚本执行失败: {e}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == '__main__':
    main()

