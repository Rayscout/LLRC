#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import time

def test_with_login():
    """带登录的测试"""
    print("🔍 测试带登录的页面访问...")
    
    # 创建会话
    session = requests.Session()
    
    try:
        # 1. 访问登录页面
        print("🔍 访问登录页面...")
        response = session.get('http://localhost:5000/auth/sign', timeout=10)
        
        if response.status_code == 200:
            print("✅ 登录页面访问成功")
            
            # 2. 尝试登录（使用测试账号）
            print("🔍 尝试登录...")
            login_data = {
                'action': 'signin',
                'email': 'test@example.com',
                'password': 'password123',
                'role': 'candidate'
            }
            
            response = session.post('http://localhost:5000/auth/sign', data=login_data, timeout=10)
            
            if response.status_code == 302:
                print("✅ 登录重定向成功")
                
                # 3. 访问求职者首页
                print("🔍 访问求职者首页...")
                response = session.get('http://localhost:5000/smartrecruit/candidate/', timeout=10)
                
                print(f"状态码: {response.status_code}")
                
                if response.status_code == 200:
                    content = response.text
                    print("✅ 求职者页面加载成功")
                    
                    # 检查关键元素
                    checks = [
                        ('candidate_ios_style.css', 'CSS文件引用'),
                        ('navbar', '导航栏'),
                        ('智能推荐', '导航文本'),
                        ('为您推荐', '页面内容'),
                        ('快速操作', '页面内容')
                    ]
                    
                    for element, description in checks:
                        if element in content:
                            print(f"✅ {description}: 找到")
                        else:
                            print(f"❌ {description}: 未找到")
                    
                    # 检查页面长度
                    print(f"页面长度: {len(content)} 字符")
                    
                else:
                    print(f"❌ 求职者页面加载失败: {response.status_code}")
                    
            else:
                print(f"❌ 登录失败: {response.status_code}")
                print("可能需要先注册测试用户")
                
        else:
            print(f"❌ 登录页面访问失败: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 测试出错: {e}")

if __name__ == "__main__":
    test_with_login()
