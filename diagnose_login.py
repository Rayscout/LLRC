#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
登录问题诊断脚本
"""

import os
import sys

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from app import create_app, db
from app.models import User
from werkzeug.security import check_password_hash

def diagnose_login():
    """诊断登录问题"""
    app = create_app()
    
    with app.app_context():
        try:
            print("=" * 60)
            print("登录问题诊断")
            print("=" * 60)
            
            # 1. 检查所有HR账号
            print("\n🔍 检查所有HR账号:")
            hr_users = User.query.filter_by(is_hr=True).all()
            for i, hr in enumerate(hr_users, 1):
                print(f"  {i}. {hr.email}")
                print(f"     姓名: {hr.first_name}{hr.last_name}")
                print(f"     部门: {hr.department}")
                print(f"     用户类型: {hr.user_type}")
                print(f"     密码哈希: {hr.password[:30]}...")
                print(f"     是否有效哈希: {'是' if hr.password.startswith('scrypt:') else '否'}")
                
                # 测试密码验证
                if check_password_hash(hr.password, '123456'):
                    print(f"     ✓ 密码验证成功")
                else:
                    print(f"     ✗ 密码验证失败")
                print()
            
            # 2. 检查所有求职者账号
            print("\n🔍 检查所有求职者账号:")
            candidate_users = User.query.filter_by(is_hr=False).limit(10).all()
            for i, candidate in enumerate(candidate_users, 1):
                print(f"  {i}. {candidate.email}")
                print(f"     姓名: {candidate.first_name}{candidate.last_name}")
                print(f"     用户类型: {candidate.user_type}")
                print(f"     密码哈希: {candidate.password[:30]}...")
                print(f"     是否有效哈希: {'是' if candidate.password.startswith('scrypt:') else '否'}")
                
                # 测试密码验证
                if check_password_hash(candidate.password, '123456'):
                    print(f"     ✓ 密码验证成功")
                else:
                    print(f"     ✗ 密码验证失败")
                print()
            
            # 3. 检查登录路由
            print("\n🔍 检查登录路由配置:")
            try:
                from app.common.auth import auth_bp
                print(f"  ✓ auth_bp 已注册")
                
                # 检查路由
                routes = []
                for rule in app.url_map.iter_rules():
                    if 'auth' in rule.endpoint:
                        routes.append(f"  {rule.endpoint}: {rule.rule}")
                
                if routes:
                    print("  ✓ 认证路由:")
                    for route in routes:
                        print(f"    {route}")
                else:
                    print("  ✗ 未找到认证路由")
                    
            except Exception as e:
                print(f"  ✗ 检查认证路由失败: {e}")
            
            # 4. 检查Flask应用配置
            print("\n🔍 检查Flask应用配置:")
            print(f"  DEBUG模式: {app.config.get('DEBUG', '未设置')}")
            print(f"  SECRET_KEY: {'已设置' if app.config.get('SECRET_KEY') else '未设置'}")
            print(f"  数据库URI: {app.config.get('SQLALCHEMY_DATABASE_URI', '未设置')}")
            
            # 5. 检查数据库连接
            print("\n🔍 检查数据库连接:")
            try:
                # 测试数据库查询
                user_count = User.query.count()
                print(f"  ✓ 数据库连接正常，用户总数: {user_count}")
            except Exception as e:
                print(f"  ✗ 数据库连接失败: {e}")
            
            # 6. 提供登录建议
            print("\n" + "=" * 60)
            print("📋 登录建议:")
            print("=" * 60)
            
            print("\n🔐 可用的测试账号:")
            print("\nHR账号 (密码: 123456):")
            for hr in hr_users[:3]:  # 只显示前3个
                print(f"  - {hr.email} ({hr.first_name}{hr.last_name})")
            
            print("\n求职者账号 (密码: 123456):")
            for candidate in candidate_users[:3]:  # 只显示前3个
                print(f"  - {candidate.email} ({candidate.first_name}{candidate.last_name})")
            
            print("\n🌐 访问地址:")
            print("  - 本地访问: http://localhost:5000")
            print("  - 登录页面: http://localhost:5000/auth/sign")
            
            print("\n🔧 如果仍然无法登录，请检查:")
            print("  1. 浏览器是否访问了正确的地址")
            print("  2. 是否选择了正确的用户类型（HR/求职者）")
            print("  3. 邮箱和密码是否输入正确")
            print("  4. 浏览器控制台是否有错误信息")
            print("  5. Flask应用是否正常运行")
            
            return True
            
        except Exception as e:
            print(f"❌ 诊断失败: {e}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == '__main__':
    diagnose_login()
