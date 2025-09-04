"""
LLRC Header Start
文件功能: 通用 Python 脚本/模块：database/init_db.py
创建时间: 2025-08-23 10:01
创建人: 谢佳悦
更新记录:
- 2025-09-03 10:36 by 李雨梦
LLRC Header End
"""
#!/usr/bin/env python3
"""
FILE-HEADER-AUTO-ADDED
文件: database/init_db.py
功能: 通用模块
创建时间: 2025-08-20 10:25
创建人: 侯东杨
更新记录:
- 2025-08-23 10:31 by 谢佳悦
- 2025-09-01 16:03 by 潘显雨
"""
"""
数据库初始化脚本 - 增强版
包含测试用户创建和完整错误处理
"""

import os
from datetime import datetime
from app import create_app
from app.models import db, User

def init_database():
    """初始化数据库"""
    try:
        # 确保目录存在
        os.makedirs('instance', exist_ok=True)
        
        app = create_app()
        with app.app_context():
            # 创建所有表
            db.create_all()
            print("✅ 数据库表创建完成")
            
            # 创建测试用户
            test_users = [
                {
                    'first_name': 'HR',
                    'last_name': 'Admin',
                    'email': 'hr@test.com',
                    'password': '123456',
                    'user_type': 'recruiter',
                    'is_hr': True,
                    'is_active': True,
                    'company_name': 'LLRC Company',
                    'position': 'HR Manager',
                    'phone_number': '13800138000',
                    'department': 'Human Resources',
                    'birthday': '1990-01-01',
                    'hire_date': datetime.now().date(),
                    'employee_id': 'HR001',
                    'bio': 'HR Administrator',
                    'skills': 'Management, HR',
                    'education': 'Bachelor Degree',
                    'experience': '5 years'
                },
                {
                    'first_name': 'Employee',
                    'last_name': 'Test',
                    'email': 'employee@test.com',
                    'password': '123456',
                    'user_type': 'employee',
                    'is_hr': False,
                    'is_active': True,
                    'company_name': 'LLRC Company',
                    'position': 'Software Engineer',
                    'phone_number': '13800138001',
                    'department': 'Engineering',
                    'birthday': '1992-05-15',
                    'hire_date': datetime.now().date(),
                    'employee_id': 'EMP001',
                    'bio': 'Software Engineer',
                    'skills': 'Python, Flask, SQL',
                    'education': 'Computer Science',
                    'experience': '3 years'
                }
            ]
            
            for user_data in test_users:
                if not User.query.filter_by(email=user_data['email']).first():
                    user = User(**user_data)
                    db.session.add(user)
                    print(f"➕ 创建用户: {user_data['email']}")
            
            db.session.commit()
            print("✅ 测试用户创建完成")
            print(f"👥 用户总数: {User.query.count()}")
            
    except Exception as e:
        print(f"❌ 数据库初始化失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    init_database()
