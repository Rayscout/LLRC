#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
简单的HTTP测试脚本
"""

import requests

def test_simple_http():
    """简单的HTTP测试"""
    print("🔍 简单HTTP测试...")
    print("=" * 50)
    
    base_url = "http://localhost:5000"
    
    try:
        # 测试1: 检查应用是否响应
        print("\n1. 检查应用响应...")
        response = requests.get(f"{base_url}/", timeout=5)
        print(f"   ✅ 应用响应正常: {response.status_code}")
        
        # 测试2: 测试个人资料页面（应该重定向到登录页面）
        print("\n2. 测试个人资料页面...")
        profile_url = f"{base_url}/talent/employee_manager/profile/"
        
        # 使用session来保持cookies
        session = requests.Session()
        
        # 先访问登录页面
        print("   📋 访问登录页面...")
        login_response = session.get(f"{base_url}/common/auth/sign", timeout=5)
        print(f"   📋 登录页面状态码: {login_response.status_code}")
        
        # 然后测试个人资料页面
        print("   📋 测试个人资料页面...")
        profile_response = session.get(profile_url, timeout=5, allow_redirects=False)
        print(f"   📋 状态码: {profile_response.status_code}")
        print(f"   📋 响应头: {dict(profile_response.headers)}")
        
        if profile_response.status_code == 302:  # 重定向
            print("   ✅ 正确重定向到登录页面")
            print(f"   📋 重定向到: {profile_response.headers.get('Location', '未知')}")
        elif profile_response.status_code == 500:
            print("   ❌ 内部服务器错误")
            print(f"   📋 响应内容: {profile_response.text[:500]}...")
        else:
            print(f"   ⚠️ 意外状态码: {profile_response.status_code}")
            print(f"   📋 响应内容: {profile_response.text[:200]}...")
        
        print("\n✅ 简单HTTP测试完成")
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到Flask应用，请确保应用正在运行")
        return False
    except requests.exceptions.Timeout:
        print("❌ 请求超时")
        return False
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_simple_http()
