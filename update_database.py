#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sqlite3
from app import create_app, db
from app.models import User, Job, Application

def update_database():
    """更新数据库结构"""
    print("开始更新数据库...")
    
    # 删除旧的数据库文件
    db_path = os.path.join('instance', 'site.db')
    if os.path.exists(db_path):
        print(f"删除旧数据库文件: {db_path}")
        os.remove(db_path)
    
    # 创建应用上下文
    app = create_app()
    with app.app_context():
        # 创建所有表
        print("创建新的数据库表...")
        db.create_all()
        
        # 创建一些示例数据
        print("创建示例数据...")
        
        # 创建示例用户
        user1 = User(
            first_name='张三',
            last_name='',
            company_name='示例公司',
            email='zhangsan@example.com',
            phone_number='13800138000',
            birthday='1990-01-01',
            password='password123'
        )
        
        user2 = User(
            first_name='李四',
            last_name='',
            company_name='测试公司',
            email='lisi@example.com',
            phone_number='13900139000',
            birthday='1992-05-15',
            password='password123'
        )
        
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()
        
        # 创建示例职位
        jobs = [
            Job(
                title='Python开发工程师',
                company_name='科技公司A',
                location='北京',
                description='负责Python后端开发，熟悉Django、Flask框架，有数据库设计经验。',
                requirements='Python, Django, Flask, SQL, Git',
                salary='15000',
                job_type='全职',
                experience_level='中级',
                user_id=user1.id
            ),
            Job(
                title='前端开发工程师',
                company_name='互联网公司B',
                location='上海',
                description='精通JavaScript、React、Vue等前端技术，有良好的UI/UX设计能力。',
                requirements='JavaScript, React, Vue, HTML, CSS',
                salary='18000',
                job_type='全职',
                experience_level='初级',
                user_id=user1.id
            ),
            Job(
                title='全栈开发工程师',
                company_name='创业公司C',
                location='深圳',
                description='熟悉前后端开发，掌握Python、JavaScript、SQL等技术栈。',
                requirements='Python, JavaScript, SQL, React, Node.js',
                salary='20000',
                job_type='全职',
                experience_level='高级',
                user_id=user2.id
            ),
            Job(
                title='DevOps工程师',
                company_name='云服务公司D',
                location='杭州',
                description='负责云基础设施管理，熟悉Docker、Kubernetes、AWS等技术。',
                requirements='Docker, Kubernetes, AWS, Linux, Git',
                salary='25000',
                job_type='全职',
                experience_level='高级',
                user_id=user2.id
            ),
            Job(
                title='数据分析师',
                company_name='金融公司E',
                location='广州',
                description='负责数据分析和报表制作，熟悉SQL、Python、Excel等工具。',
                requirements='SQL, Python, Excel, 数据分析',
                salary='12000',
                job_type='全职',
                experience_level='初级',
                user_id=user1.id
            )
        ]
        
        for job in jobs:
            db.session.add(job)
        
        db.session.commit()
        
        print("数据库更新完成！")
        print(f"创建了 {len(jobs)} 个示例职位")
        print(f"创建了 2 个示例用户")

if __name__ == "__main__":
    update_database()
