#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试员工注销功能
"""

import requests
import json

def test_deactivate_function():
    """测试员工注销功能"""
    base_url = "http://127.0.0.1:5000"
    
    print("=" * 50)
    print("测试员工注销功能")
    print("=" * 50)
    
    # 1. 测试API端点是否可访问
    print("\n1. 测试API端点可访问性...")
    
    # 测试注销端点
    deactivate_url = f"{base_url}/talent/hr_admin/employee-management/deactivate/1"
    print(f"测试注销端点: {deactivate_url}")
    try:
        response = requests.post(deactivate_url, timeout=5)
        print(f"注销端点状态码: {response.status_code}")
        if response.status_code == 401:
            print("✅ 端点可访问，需要认证（正常）")
        elif response.status_code == 404:
            print("❌ 端点不存在，路由可能有问题")
        else:
            print(f"⚠️  端点返回状态码: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到服务器，请确保应用正在运行")
        return
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return
    print("注销端点测试完成")
    
    # 测试重新激活端点
    reactivate_url = f"{base_url}/talent/hr_admin/employee-management/reactivate/1"
    try:
        response = requests.post(reactivate_url, timeout=5)
        print(f"重新激活端点状态码: {response.status_code}")
        if response.status_code == 401:
            print("✅ 端点可访问，需要认证（正常）")
        elif response.status_code == 404:
            print("❌ 端点不存在，路由可能有问题")
        else:
            print(f"⚠️  端点返回状态码: {response.status_code}")
    except Exception as e:
        print(f"❌ 测试失败: {e}")
    
    # 2. 检查路由注册
    print("\n2. 检查路由注册...")
    
    # 测试员工列表页面
    list_url = f"{base_url}/talent/hr_admin/employee-management/list"
    try:
        response = requests.get(list_url, timeout=5)
        print(f"员工列表页面状态码: {response.status_code}")
        if response.status_code == 302:
            print("✅ 页面存在，重定向到登录（正常）")
        elif response.status_code == 200:
            print("✅ 页面可访问")
        else:
            print(f"⚠️  页面返回状态码: {response.status_code}")
    except Exception as e:
        print(f"❌ 测试失败: {e}")
    
    # 3. 检查高管仪表板
    print("\n3. 检查高管仪表板...")
    
    dashboard_url = f"{base_url}/talent/hr_admin/executive_dashboard"
    try:
        response = requests.get(dashboard_url, timeout=5)
        print(f"高管仪表板状态码: {response.status_code}")
        if response.status_code == 302:
            print("✅ 页面存在，重定向到登录（正常）")
        elif response.status_code == 200:
            print("✅ 页面可访问")
        else:
            print(f"⚠️  页面返回状态码: {response.status_code}")
    except Exception as e:
        print(f"❌ 测试失败: {e}")
    
    print("\n" + "=" * 50)
    print("测试完成")
    print("=" * 50)
    
    print("\n📋 问题诊断:")
    print("1. 如果端点返回404，说明路由没有正确注册")
    print("2. 如果端点返回401，说明路由正常，需要认证")
    print("3. 如果页面返回200，说明可以直接访问（可能不需要认证）")
    print("4. 如果页面返回302，说明重定向到登录页面（正常）")

if __name__ == "__main__":
    test_deactivate_function()
