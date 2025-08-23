#!/usr/bin/env python3
"""
测试员工学习推荐功能
"""

import os
import sys

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_learning_recommendation():
    """测试学习推荐功能"""
    print("=== 测试员工学习推荐功能 ===\n")
    
    try:
        from app import create_app, db
        from app.models import User, Job
        from talent_management_system.employee_manager_module.learning_recommendation import (
            extract_user_skills, analyze_job_requirements, calculate_skill_gap,
            recommend_courses, generate_learning_plan
        )
        
        # 创建应用上下文
        app = create_app()
        with app.app_context():
            print("✅ 应用创建成功")
            
            # 测试用户资料
            test_user_profile = {
                'bio': '我是一名有3年经验的Python开发工程师，熟悉Django和Flask框架，有MySQL数据库经验。',
                'experience': '在ABC公司担任Python开发工程师，负责后端API开发和数据库设计。',
                'education': '计算机科学学士学位，主修软件工程。'
            }
            
            print("\n=== 测试1：技能提取 ===")
            user_skills = extract_user_skills(test_user_profile)
            print(f"✅ 提取到用户技能: {user_skills}")
            
            # 测试职位描述
            test_job_description = """
            我们正在寻找一名高级Python开发工程师，需要具备以下技能：
            - Python编程经验
            - Django和Flask框架
            - MySQL和PostgreSQL数据库
            - Docker容器化
            - 微服务架构
            - 团队协作能力
            - 项目管理经验
            """
            
            print("\n=== 测试2：职位要求分析 ===")
            job_requirements = analyze_job_requirements(test_job_description)
            print(f"✅ 分析到职位要求: {job_requirements}")
            
            print("\n=== 测试3：技能差距计算 ===")
            skill_gap = calculate_skill_gap(user_skills, job_requirements)
            print(f"✅ 技能匹配度: {skill_gap['match_rate']:.2%}")
            print(f"✅ 匹配技能: {skill_gap['matched_skills']}")
            print(f"✅ 缺失技能: {skill_gap['missing_skills']}")
            
            print("\n=== 测试4：课程推荐 ===")
            recommended_courses = recommend_courses(skill_gap)
            print(f"✅ 推荐课程数量: {len(recommended_courses)}")
            for i, course_rec in enumerate(recommended_courses[:3], 1):
                print(f"   课程{i}: {course_rec['course']['name']} - {course_rec['target_skill']}")
            
            print("\n=== 测试5：学习计划生成 ===")
            learning_plan = generate_learning_plan(user_skills, job_requirements)
            print(f"✅ 学习目标数量: {len(learning_plan['learning_objectives'])}")
            print(f"✅ 预计学习时长: {learning_plan['estimated_duration']} 周")
            print(f"✅ 优先级技能: {learning_plan['priority_skills']}")
            
            # 测试数据库中的职位
            print("\n=== 测试6：数据库职位分析 ===")
            jobs = Job.query.limit(3).all()
            if jobs:
                for i, job in enumerate(jobs, 1):
                    print(f"\n职位{i}: {job.title}")
                    job_reqs = analyze_job_requirements(job.description)
                    plan = generate_learning_plan(user_skills, job_reqs)
                    print(f"   技能匹配度: {plan['current_status']['match_rate']:.2%}")
                    print(f"   推荐课程数: {len(plan['recommended_courses'])}")
            else:
                print("⚠️ 数据库中没有职位数据")
            
            print("\n=== 测试7：不同用户水平的课程推荐 ===")
            for level in ['beginner', 'intermediate', 'advanced']:
                courses = recommend_courses(skill_gap, level)
                level_courses = [c for c in courses if c['course']['level'] == level]
                print(f"✅ {level}级别课程: {len(level_courses)} 门")
            
            print("\n✅ 所有测试完成！")
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_learning_recommendation()
