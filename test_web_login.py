#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Web登录测试脚本
"""

import requests
import json

def test_web_login():
    """测试Web登录功能"""
    print("=" * 60)
    print("Web登录测试")
    print("=" * 60)
    
    # 测试URL
    base_url = "http://localhost:5000"
    login_url = f"{base_url}/auth/sign"
    
    # 测试账号
    test_accounts = [
        {
            "email": "hr_tech@company.com",
            "password": "123456",
            "role": "recruiter",
            "name": "张技术HR"
        },
        {
            "email": "hr_test@company.com", 
            "password": "123456",
            "role": "recruiter",
            "name": "测试HR"
        },
        {
            "email": "tech_candidate1@email.com",
            "password": "123456", 
            "role": "candidate",
            "name": "陈技术强"
        }
    ]
    
    print(f"\n🌐 测试地址: {base_url}")
    print(f"📝 登录页面: {login_url}")
    
    print(f"\n🔐 测试账号:")
    for i, account in enumerate(test_accounts, 1):
        print(f"  {i}. {account['name']}")
        print(f"     邮箱: {account['email']}")
        print(f"     密码: {account['password']}")
        print(f"     角色: {account['role']}")
        print()
    
    print("📋 登录步骤:")
    print("1. 打开浏览器访问: http://localhost:5000")
    print("2. 点击右上角的'登录'按钮")
    print("3. 输入邮箱和密码")
    print("4. 选择正确的用户类型:")
    print("   - HR账号选择: 'HR'")
    print("   - 求职者账号选择: '求职者'")
    print("5. 点击'登录'按钮")
    
    print("\n⚠️  重要提醒:")
    print("- 必须选择用户类型（role），否则无法登录")
    print("- HR账号选择'HR'角色")
    print("- 求职者账号选择'求职者'角色")
    print("- 确保邮箱和密码输入正确")
    
    print("\n🔧 如果仍然无法登录，请检查:")
    print("1. 浏览器控制台是否有错误信息（F12打开）")
    print("2. 网络请求是否正常（Network标签）")
    print("3. Flask应用是否正常运行")
    print("4. 数据库连接是否正常")
    
    return True

if __name__ == '__main__':
    test_web_login()
