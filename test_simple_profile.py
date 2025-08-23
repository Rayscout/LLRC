#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
简单测试个人资料页面
"""

import requests
import json

def test_simple_profile():
    """简单测试个人资料页面"""
    base_url = "http://localhost:5000"
    
    print("🔍 简单测试个人资料页面...")
    print("=" * 50)
    
    # 测试1: 基本访问
    print("1. 测试基本访问...")
    try:
        response = requests.get(f"{base_url}/talent/employee_manager/profile/")
        print(f"   状态码: {response.status_code}")
        print(f"   响应头: {dict(response.headers)}")
        
        if response.status_code == 500:
            print("   ❌ 500内部服务器错误")
            print(f"   响应内容: {response.text}")
        elif response.status_code == 302:
            print("   ⚠️ 302重定向（需要登录）")
            print(f"   重定向到: {response.headers.get('Location', '未知')}")
        else:
            print(f"   📄 响应内容: {response.text[:200]}...")
            
    except Exception as e:
        print(f"   ❌ 请求异常: {e}")
    
    # 测试2: 检查应用程序状态
    print("\n2. 检查应用程序状态...")
    try:
        response = requests.get(f"{base_url}/")
        print(f"   根路径状态码: {response.status_code}")
    except Exception as e:
        print(f"   ❌ 根路径访问异常: {e}")
    
    # 测试3: 检查员工仪表板
    print("\n3. 检查员工仪表板...")
    try:
        response = requests.get(f"{base_url}/talent/employee/dashboard")
        print(f"   员工仪表板状态码: {response.status_code}")
    except Exception as e:
        print(f"   ❌ 员工仪表板访问异常: {e}")
    
    print("\n" + "=" * 50)
    print("🏁 简单测试完成")

if __name__ == "__main__":
    test_simple_profile()
