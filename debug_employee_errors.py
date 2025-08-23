#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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

if __name__ == "__main__":
    debug_employee_errors()
