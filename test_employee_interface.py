#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试员工界面基本功能
"""

import requests
import time

def test_employee_interface():
    """测试员工界面"""
    base_url = "http://localhost:5000"
    
    print("🚀 开始测试员工界面...")
    print("=" * 50)
    
    # 测试员工认证页面
    print("1. 测试员工认证页面...")
    try:
        response = requests.get(f"{base_url}/talent/employee/auth")
        if response.status_code == 200:
            print("   ✅ 员工认证页面访问成功")
        else:
            print(f"   ❌ 员工认证页面访问失败: {response.status_code}")
    except Exception as e:
        print(f"   ❌ 员工认证页面访问异常: {e}")
    
    # 测试员工仪表板
    print("\n2. 测试员工仪表板...")
    try:
        response = requests.get(f"{base_url}/talent/employee/dashboard")
        if response.status_code == 200:
            print("   ✅ 员工仪表板访问成功")
        elif response.status_code == 302:  # 重定向到登录页面
            print("   ⚠️ 员工仪表板重定向到登录页面（正常，需要登录）")
        else:
            print(f"   ❌ 员工仪表板访问失败: {response.status_code}")
    except Exception as e:
        print(f"   ❌ 员工仪表板访问异常: {e}")
    
    # 测试个人资料页面
    print("\n3. 测试个人资料页面...")
    try:
        response = requests.get(f"{base_url}/talent/employee_manager/profile/")
        if response.status_code == 200:
            print("   ✅ 个人资料页面访问成功")
        elif response.status_code == 302:
            print("   ⚠️ 个人资料页面重定向到登录页面（正常，需要登录）")
        else:
            print(f"   ❌ 个人资料页面访问失败: {response.status_code}")
    except Exception as e:
        print(f"   ❌ 个人资料页面访问异常: {e}")
    
    # 测试绩效记录页面
    print("\n4. 测试绩效记录页面...")
    try:
        response = requests.get(f"{base_url}/talent/employee_manager/performance/")
        if response.status_code == 200:
            print("   ✅ 绩效记录页面访问成功")
        elif response.status_code == 302:
            print("   ⚠️ 绩效记录页面重定向到登录页面（正常，需要登录）")
        else:
            print(f"   ❌ 绩效记录页面访问失败: {response.status_code}")
    except Exception as e:
        print(f"   ❌ 绩效记录页面访问异常: {e}")
    
    # 测试项目经验页面
    print("\n5. 测试项目经验页面...")
    try:
        response = requests.get(f"{base_url}/talent/employee_manager/projects/")
        if response.status_code == 200:
            print("   ✅ 项目经验页面访问成功")
        elif response.status_code == 302:
            print("   ⚠️ 项目经验页面重定向到登录页面（正常，需要登录）")
        else:
            print(f"   ❌ 项目经验页面访问失败: {response.status_code}")
    except Exception as e:
        print(f"   ❌ 项目经验页面访问异常: {e}")
    
    # 测试学习推荐页面
    print("\n6. 测试学习推荐页面...")
    try:
        response = requests.get(f"{base_url}/talent/employee_manager/learning_recommendation/dashboard")
        if response.status_code == 200:
            print("   ✅ 学习推荐页面访问成功")
        elif response.status_code == 302:
            print("   ⚠️ 学习推荐页面重定向到登录页面（正常，需要登录）")
        else:
            print(f"   ❌ 学习推荐页面访问失败: {response.status_code}")
    except Exception as e:
        print(f"   ❌ 学习推荐页面访问异常: {e}")
    
    print("\n" + "=" * 50)
    print("🏁 测试完成")
    print("\n📝 说明:")
    print("   - 状态码200: 页面正常访问")
    print("   - 状态码302: 重定向到登录页面（正常行为，需要先登录）")
    print("   - 状态码404: 页面未找到（路由配置问题）")
    print("   - 状态码500: 内部服务器错误（需要检查日志）")

if __name__ == "__main__":
    # 等待应用程序启动
    print("⏳ 等待应用程序启动...")
    time.sleep(3)
    
    test_employee_interface()
