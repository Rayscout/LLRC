#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试HR用户登录的脚本
"""

import sys
import os
from werkzeug.security import check_password_hash

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import User

def test_hr_login():
    """测试HR用户登录"""
    app = create_app()
    
    with app.app_context():
        try:
            # 查找HR用户
            hr_user = User.query.filter_by(email='hr@smartrecruit.com').first()
            
            if not hr_user:
                print("❌ 未找到HR用户 hr@smartrecruit.com")
                print("请先运行 create_hr_user.py 创建HR用户")
                return False
            
            print(f"✅ 找到HR用户: {hr_user.email}")
            print(f"   姓名: {hr_user.first_name} {hr_user.last_name}")
            print(f"   公司: {hr_user.company_name}")
            print(f"   职位: {hr_user.position}")
            print(f"   HR权限: {'是' if hr_user.is_hr else '否'}")
            
            # 测试密码验证
            test_password = "hr123456"
            if check_password_hash(hr_user.password, test_password):
                print(f"✅ 密码验证成功: {test_password}")
                return True
            else:
                print(f"❌ 密码验证失败: {test_password}")
                print(f"   当前密码哈希: {hr_user.password}")
                return False
                
        except Exception as e:
            print(f"❌ 测试失败: {e}")
            return False

def check_all_users():
    """检查所有用户"""
    app = create_app()
    
    with app.app_context():
        try:
            users = User.query.all()
            print(f"\n👥 系统中所有用户 ({len(users)} 个):")
            print("-" * 80)
            
            for user in users:
                print(f"ID: {user.id}")
                print(f"邮箱: {user.email}")
                print(f"姓名: {user.first_name} {user.last_name}")
                print(f"公司: {user.company_name}")
                print(f"HR权限: {'是' if user.is_hr else '否'}")
                print(f"密码长度: {len(user.password) if user.password else 0}")
                print("-" * 80)
                
        except Exception as e:
            print(f"❌ 查询用户失败: {e}")

def fix_hr_password():
    """修复HR用户密码"""
    app = create_app()
    
    with app.app_context():
        try:
            from werkzeug.security import generate_password_hash
            
            hr_user = User.query.filter_by(email='hr@smartrecruit.com').first()
            if not hr_user:
                print("❌ 未找到HR用户")
                return False
            
            # 重新设置密码
            new_password = "hr123456"
            hr_user.password = generate_password_hash(new_password)
            db.session.commit()
            
            print(f"✅ 密码已重置为: {new_password}")
            return True
            
        except Exception as e:
            print(f"❌ 重置密码失败: {e}")
            db.session.rollback()
            return False

if __name__ == "__main__":
    print("🔍 HR用户登录测试脚本")
    print("=" * 50)
    
    while True:
        print("\n请选择操作:")
        print("1. 测试HR用户登录")
        print("2. 查看所有用户")
        print("3. 修复HR用户密码")
        print("4. 退出")
        
        choice = input("\n请输入选择 (1-4): ").strip()
        
        if choice == "1":
            print("\n正在测试HR用户登录...")
            test_hr_login()
            
        elif choice == "2":
            print("\n正在查询所有用户...")
            check_all_users()
            
        elif choice == "3":
            print("\n正在修复HR用户密码...")
            fix_hr_password()
            
        elif choice == "4":
            print("👋 再见！")
            break
            
        else:
            print("❌ 无效选择，请重新输入")
        
        input("\n按回车键继续...")

