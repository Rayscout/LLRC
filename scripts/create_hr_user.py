#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创建HR权限账户的脚本
"""

import sys
import os
from werkzeug.security import generate_password_hash

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import User

def create_hr_user():
    """创建HR权限账户"""
    app = create_app()
    
    with app.app_context():
        try:
            # 检查是否已存在HR用户
            existing_hr = User.query.filter_by(is_hr=True).first()
            if existing_hr:
                print(f"✅ 已存在HR用户: {existing_hr.email}")
                print(f"   姓名: {existing_hr.first_name} {existing_hr.last_name}")
                print(f"   公司: {existing_hr.company_name}")
                print(f"   职位: {existing_hr.position}")
                return existing_hr
            
            # 创建新的HR用户
            hr_user = User(
                first_name="张",
                last_name="HR",
                company_name="智能招聘科技有限公司",
                position="人力资源总监",
                email="hr@smartrecruit.com",
                phone_number="13800138000",
                birthday="1985-06-15",
                password=generate_password_hash("hr123456"),
                is_hr=True
            )
            
            # 保存到数据库
            db.session.add(hr_user)
            db.session.commit()
            
            print("✅ 成功创建HR用户账户！")
            print(f"   邮箱: {hr_user.email}")
            print(f"   密码: hr123456")
            print(f"   姓名: {hr_user.first_name} {hr_user.last_name}")
            print(f"   公司: {hr_user.company_name}")
            print(f"   职位: {hr_user.position}")
            print(f"   HR权限: {'是' if hr_user.is_hr else '否'}")
            
            return hr_user
            
        except Exception as e:
            print(f"❌ 创建HR用户失败: {e}")
            db.session.rollback()
            return None

def create_test_hr_users():
    """创建多个测试HR用户"""
    app = create_app()
    
    with app.app_context():
        test_users = [
            {
                "first_name": "李",
                "last_name": "招聘",
                "company_name": "互联网科技有限公司",
                "position": "招聘经理",
                "email": "recruit@tech.com",
                "phone_number": "13900139000",
                "birthday": "1990-03-20",
                "password": "recruit123"
            },
            {
                "first_name": "王",
                "last_name": "人事",
                "company_name": "金融投资集团",
                "position": "人事主管",
                "email": "hr@finance.com",
                "phone_number": "13700137000",
                "birthday": "1988-09-10",
                "password": "hr888888"
            },
            {
                "first_name": "陈",
                "last_name": "管理",
                "company_name": "制造业集团",
                "position": "人力资源经理",
                "email": "hr@manufacture.com",
                "phone_number": "13600136000",
                "birthday": "1987-12-05",
                "password": "hr666666"
            }
        ]
        
        created_users = []
        
        for user_data in test_users:
            try:
                # 检查是否已存在
                existing_user = User.query.filter_by(email=user_data["email"]).first()
                if existing_user:
                    print(f"⚠️  用户已存在: {user_data['email']}")
                    continue
                
                # 创建新用户
                new_user = User(
                    first_name=user_data["first_name"],
                    last_name=user_data["last_name"],
                    company_name=user_data["company_name"],
                    position=user_data["position"],
                    email=user_data["email"],
                    phone_number=user_data["phone_number"],
                    birthday=user_data["birthday"],
                    password=generate_password_hash(user_data["password"]),
                    is_hr=True
                )
                
                db.session.add(new_user)
                created_users.append(new_user)
                
            except Exception as e:
                print(f"❌ 创建用户 {user_data['email']} 失败: {e}")
        
        try:
            db.session.commit()
            print(f"✅ 成功创建 {len(created_users)} 个HR用户")
            
            for user in created_users:
                print(f"   📧 {user.email} | 🔑 {user.password.replace(generate_password_hash(''), '')} | 👤 {user.first_name}{user.last_name}")
                
        except Exception as e:
            print(f"❌ 保存用户失败: {e}")
            db.session.rollback()

def list_hr_users():
    """列出所有HR用户"""
    app = create_app()
    
    with app.app_context():
        try:
            hr_users = User.query.filter_by(is_hr=True).all()
            
            if not hr_users:
                print("📭 暂无HR用户")
                return
            
            print(f"👥 找到 {len(hr_users)} 个HR用户:")
            print("-" * 80)
            
            for user in hr_users:
                print(f"ID: {user.id}")
                print(f"姓名: {user.first_name} {user.last_name}")
                print(f"邮箱: {user.email}")
                print(f"公司: {user.company_name}")
                print(f"职位: {user.position}")
                print(f"电话: {user.phone_number}")
                print(f"HR权限: {'是' if user.is_hr else '否'}")
                print("-" * 80)
                
        except Exception as e:
            print(f"❌ 查询HR用户失败: {e}")

if __name__ == "__main__":
    print("🚀 HR用户管理脚本")
    print("=" * 50)
    
    while True:
        print("\n请选择操作:")
        print("1. 创建单个HR用户")
        print("2. 创建多个测试HR用户")
        print("3. 查看所有HR用户")
        print("4. 退出")
        
        choice = input("\n请输入选择 (1-4): ").strip()
        
        if choice == "1":
            print("\n正在创建HR用户...")
            create_hr_user()
            
        elif choice == "2":
            print("\n正在创建测试HR用户...")
            create_test_hr_users()
            
        elif choice == "3":
            print("\n正在查询HR用户...")
            list_hr_users()
            
        elif choice == "4":
            print("👋 再见！")
            break
            
        else:
            print("❌ 无效选择，请重新输入")
        
        input("\n按回车键继续...")

