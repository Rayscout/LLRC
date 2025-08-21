#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json

def test_demo_page():
    """测试演示页面功能"""
    base_url = "http://localhost:5000"
    
    print("=== 智能搜索演示页面测试 ===")
    
    # 测试演示页面
    print("\n1. 测试演示页面...")
    try:
        response = requests.get(f"{base_url}/demo/job_search", timeout=10)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ 演示页面访问成功")
            
            # 检查页面内容
            content = response.text
            checks = [
                ("页面标题", "智能岗位搜索" in content),
                ("技能标签", "python" in content.lower()),
                ("推荐职位", "为您推荐" in content),
                ("所有职位", "所有可用职位" in content),
                ("匹配度", "% 匹配" in content),
                ("登录提示", "立即登录" in content)
            ]
            
            print("\n页面内容检查:")
            for check_name, result in checks:
                status = "✅" if result else "❌"
                print(f"  {status} {check_name}")
                
        else:
            print(f"❌ 演示页面访问失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 测试失败: {e}")
    
    # 测试主页面
    print("\n2. 测试主页面...")
    try:
        response = requests.get(f"{base_url}/", timeout=10)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ 主页面访问成功")
            if "登录" in response.text:
                print("✅ 登录页面正常显示")
        else:
            print(f"❌ 主页面访问失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 测试失败: {e}")
    
    print("\n=== 测试完成 ===")
    print("\n🎉 现在您可以访问以下页面:")
    print("  📱 演示页面: http://localhost:5000/demo/job_search")
    print("  🏠 主页面: http://localhost:5000")

if __name__ == "__main__":
    test_demo_page()
