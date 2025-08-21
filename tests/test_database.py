#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from app import create_app, db
from app.models import User, Job, Application

def test_database():
    """测试数据库中的数据"""
    print("=== 数据库测试 ===")
    
    app = create_app()
    with app.app_context():
        # 测试用户数据
        print("\n1. 用户数据:")
        users = User.query.all()
        print(f"找到 {len(users)} 个用户")
        for user in users:
            print(f"  - {user.first_name} ({user.email}) - {user.company_name}")
        
        # 测试职位数据
        print("\n2. 职位数据:")
        jobs = Job.query.all()
        print(f"找到 {len(jobs)} 个职位")
        for job in jobs:
            print(f"  - {job.title} - {job.company_name} - {job.location} - {job.salary}")
            print(f"    类型: {job.job_type}, 经验: {job.experience_level}")
            if job.requirements:
                print(f"    要求: {job.requirements}")
        
        # 测试智能匹配算法
        print("\n3. 智能匹配测试:")
        demo_skills = ['python', 'javascript', 'react', 'sql', 'git']
        print(f"模拟用户技能: {demo_skills}")
        
        for job in jobs:
            # 计算匹配度
            job_text = f"{job.title} {job.description}"
            if job.requirements:
                job_text += f" {job.requirements}"
            job_text = job_text.lower()
            
            matched_skills = sum(1 for skill in demo_skills if skill.lower() in job_text)
            match_score = (matched_skills / len(demo_skills)) * 100 if demo_skills else 0
            
            print(f"  - {job.title}: {match_score:.1f}% 匹配")
        
        print("\n=== 数据库测试完成 ===")

if __name__ == "__main__":
    test_database()
