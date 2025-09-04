"""
LLRC Header Start
文件功能: 人才管理子系统 Python 模块：talent_management_system/employee_manager_module/debug_tools.py
创建时间: 2025-08-19 12:21
创建人: 李雨梦
更新记录:
- 2025-08-19 12:51 by 李雨梦
- 2025-08-24 17:23 by 谢佳悦
- 2025-08-31 13:26 by 苏杰
LLRC Header End
"""
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FILE-HEADER-AUTO-ADDED
文件: talent_management_system/employee_manager_module/debug_tools.py
功能: 通用模块
创建时间: 2025-08-25 11:23
创建人: 李雨梦
更新记录:
- 2025-08-25 10:49 by 潘显雨
- 2025-08-25 18:40 by 谢佳悦
- 2025-08-27 15:17 by 潘显雨
"""

"""
调试员工界面错误
"""

import requests
import json

def debug_employee_errors():
    """调试员工界面错误"""
    base_url = "http://localhost:5000"
    
    print("🔍 开始调试员工界面错误...")
    print("=" * 50)
    
    # 测试个人资料页面并获取详细错误信息
    print("1. 调试个人资料页面500错误...")
    try:
        response = requests.get(f"{base_url}/talent/employee_manager/profile/")
        print(f"   状态码: {response.status_code}")
        print(f"   响应头: {dict(response.headers)}")
        
        if response.status_code == 500:
            print("   ❌ 500内部服务器错误")
            print(f"   响应内容: {response.text[:500]}...")
        elif response.status_code == 302:
            print("   ⚠️ 302重定向（需要登录）")
            print(f"   重定向到: {response.headers.get('Location', '未知')}")
        else:
            print(f"   📄 响应内容: {response.text[:200]}...")
            
    except Exception as e:
        print(f"   ❌ 请求异常: {e}")
    
    print("\n2. 调试学习推荐页面404错误...")
    try:
        response = requests.get(f"{base_url}/talent/employee_manager/learning_recommendation/dashboard")
        print(f"   状态码: {response.status_code}")
        print(f"   响应头: {dict(response.headers)}")
        
        if response.status_code == 404:
            print("   ❌ 404页面未找到")
            print(f"   响应内容: {response.text[:500]}...")
        elif response.status_code == 302:
            print("   ⚠️ 302重定向（需要登录）")
            print(f"   重定向到: {response.headers.get('Location', '未知')}")
        else:
            print(f"   📄 响应内容: {response.text[:200]}...")
            
    except Exception as e:
        print(f"   ❌ 请求异常: {e}")
    
    # 检查应用程序状态
    print("\n3. 检查应用程序状态...")
    try:
        response = requests.get(f"{base_url}/")
        print(f"   根路径状态码: {response.status_code}")
        if response.status_code == 302:
            print(f"   重定向到: {response.headers.get('Location', '未知')}")
    except Exception as e:
        print(f"   ❌ 根路径访问异常: {e}")
    
    print("\n" + "=" * 50)
    print("🏁 调试完成")

def debug_employee_routes():
    """调试员工路由"""
    base_url = "http://localhost:5000"
    
    print("🔍 开始调试员工路由...")
    print("=" * 50)
    
    routes_to_test = [
        "/talent/employee_manager/profile/",
        "/talent/employee_manager/learning_recommendation/dashboard",
        "/talent/employee_manager/performance/",
        "/talent/employee_manager/projects/",
        "/talent/employee_manager/feedback/",
        "/talent/employee_manager/compensation/",
        "/talent/employee_manager/smart_goals/"
    ]
    
    for route in routes_to_test:
        try:
            response = requests.get(f"{base_url}{route}", timeout=5)
            print(f"路由: {route}")
            print(f"   状态码: {response.status_code}")
            
            if response.status_code == 200:
                print("   ✅ 正常")
            elif response.status_code == 302:
                print(f"   ⚠️ 重定向到: {response.headers.get('Location', '未知')}")
            elif response.status_code == 404:
                print("   ❌ 页面未找到")
            elif response.status_code == 500:
                print("   ❌ 内部服务器错误")
            else:
                print(f"   ❓ 未知状态: {response.status_code}")
                
        except Exception as e:
            print(f"路由: {route}")
            print(f"   ❌ 请求异常: {e}")
        
        print()

def debug_employee_auth():
    """调试员工认证"""
    base_url = "http://localhost:5000"
    
    print("🔍 开始调试员工认证...")
    print("=" * 50)
    
    # 测试登录页面
    try:
        response = requests.get(f"{base_url}/auth/sign")
        print(f"登录页面状态码: {response.status_code}")
        if response.status_code == 200:
            print("✅ 登录页面可访问")
        else:
            print("❌ 登录页面不可访问")
    except Exception as e:
        print(f"❌ 登录页面访问异常: {e}")
    
    # 测试员工登录
    login_data = {
        'action': 'signin',
        'email': 'employee@test.com',
        'password': '123456',
        'role': 'employee'
    }
    
    try:
        response = requests.post(f"{base_url}/auth/sign", data=login_data, allow_redirects=False)
        print(f"员工登录状态码: {response.status_code}")
        
        if response.status_code == 302:
            location = response.headers.get('Location', '')
            print(f"✅ 登录成功，重定向到: {location}")
            
            if 'talent/employee_manager' in location:
                print("✅ 正确重定向到员工管理页面")
            else:
                print("❌ 重定向目标不正确")
        else:
            print("❌ 登录失败")
            
    except Exception as e:
        print(f"❌ 员工登录异常: {e}")

if __name__ == "__main__":
    debug_employee_errors()
    print("\n" + "=" * 50)
    debug_employee_routes()
    print("\n" + "=" * 50)
    debug_employee_auth()
