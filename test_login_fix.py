#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import time

def test_login_fix():
    """测试登录修复是否有效"""
    print("🔧 测试登录修复...")
    
    try:
        # 等待应用启动
        time.sleep(2)
        
        # 测试首页访问
        print("🔍 测试首页访问...")
        response = requests.get('http://localhost:5000/', timeout=10)
        
        if response.status_code == 302:
            print("✅ 首页重定向正常")
        elif response.status_code == 200:
            print("✅ 首页访问正常")
        else:
            print(f"❌ 首页访问异常: {response.status_code}")
            return False
        
        # 测试登录页面访问
        print("🔍 测试登录页面访问...")
        response = requests.get('http://localhost:5000/auth/sign', timeout=10)
        
        if response.status_code == 200:
            print("✅ 登录页面访问正常")
            
            # 检查页面内容
            content = response.text
            if '登录' in content and '注册' in content:
                print("✅ 登录页面内容正常")
            else:
                print("❌ 登录页面内容异常")
                return False
        else:
            print(f"❌ 登录页面访问异常: {response.status_code}")
            return False
        
        # 测试求职者页面访问（需要登录）
        print("🔍 测试求职者页面访问...")
        response = requests.get('http://localhost:5000/smartrecruit/candidate/', timeout=10)
        
        if response.status_code == 302:
            print("✅ 求职者页面重定向到登录页面（正常）")
        elif response.status_code == 200:
            print("✅ 求职者页面访问正常")
        else:
            print(f"❌ 求职者页面访问异常: {response.status_code}")
            return False
        
        print("🎉 登录修复测试通过！")
        return True
        
    except Exception as e:
        print(f"❌ 测试出错: {e}")
        return False

if __name__ == "__main__":
    test_login_fix()
