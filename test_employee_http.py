#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
HTTP测试员工界面
"""

import requests
import json

def test_employee_interface():
    """测试员工界面HTTP访问"""
    print("🌐 测试员工界面HTTP访问...")
    print("=" * 50)
    
    base_url = "http://localhost:5000"
    
    # 创建会话以保持登录状态
    session = requests.Session()
    
    try:
        # 1. 测试首页访问
        print("\n1. 测试首页访问...")
        response = session.get(f"{base_url}/")
        print(f"   📋 状态码: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ 首页访问成功")
        else:
            print("   ❌ 首页访问失败")
        
        # 2. 测试登录页面
        print("\n2. 测试登录页面...")
        response = session.get(f"{base_url}/auth/sign")
        print(f"   📋 状态码: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ 登录页面访问成功")
        else:
            print("   ❌ 登录页面访问失败")
        
        # 3. 测试员工登录
        print("\n3. 测试员工登录...")
        login_data = {
            'action': 'signin',
            'email': 'employee@test.com',
            'password': '123456',
            'role': 'employee'
        }
        
        response = session.post(f"{base_url}/auth/sign", data=login_data)
        print(f"   📋 状态码: {response.status_code}")
        
        if response.status_code == 302:  # 重定向到仪表板
            print("   ✅ 员工登录成功")
            
            # 获取重定向URL
            redirect_url = response.headers.get('Location')
            if redirect_url:
                print(f"   📋 重定向到: {redirect_url}")
                
                # 4. 测试员工仪表板
                print("\n4. 测试员工仪表板...")
                if redirect_url.startswith('/'):
                    dashboard_url = f"{base_url}{redirect_url}"
                else:
                    dashboard_url = redirect_url
                
                response = session.get(dashboard_url)
                print(f"   📋 状态码: {response.status_code}")
                
                if response.status_code == 200:
                    print("   ✅ 员工仪表板访问成功")
                    
                    # 检查页面内容
                    content = response.text
                    if "员工仪表板" in content:
                        print("   ✅ 页面内容正确")
                    else:
                        print("   ⚠️ 页面内容可能有问题")
                        
                    # 检查是否有错误信息
                    if "error" in content.lower() or "exception" in content.lower():
                        print("   ⚠️ 页面可能包含错误信息")
                    else:
                        print("   ✅ 页面无错误信息")
                        
                else:
                    print("   ❌ 员工仪表板访问失败")
                    print(f"   📋 响应内容: {response.text[:200]}...")
        else:
            print("   ❌ 员工登录失败")
            print(f"   📋 响应内容: {response.text[:200]}...")
        
        # 5. 测试其他员工功能页面
        print("\n5. 测试其他员工功能页面...")
        
        # 测试个人资料页面
        profile_url = f"{base_url}/talent/employee_manager/profile/"
        response = session.get(profile_url)
        print(f"   📋 个人资料页面状态码: {response.status_code}")
        
        # 测试学习推荐页面
        learning_url = f"{base_url}/talent/employee_manager/learning_recommendation/dashboard"
        response = session.get(learning_url)
        print(f"   📋 学习推荐页面状态码: {response.status_code}")
        
        # 测试绩效页面
        performance_url = f"{base_url}/talent/employee_manager/performance/"
        response = session.get(performance_url)
        print(f"   📋 绩效页面状态码: {response.status_code}")
        
        # 测试项目页面
        projects_url = f"{base_url}/talent/employee_manager/projects/"
        response = session.get(projects_url)
        print(f"   📋 项目页面状态码: {response.status_code}")
        
        print("\n✅ HTTP测试完成")
        
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到Flask应用，请确保应用正在运行")
        print("   运行命令: python run_app.py")
    except Exception as e:
        print(f"❌ 测试失败: {e}")

if __name__ == "__main__":
    test_employee_interface()
