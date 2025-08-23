#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import time

def create_test_user():
    """创建测试用户"""
    print("🔧 创建测试用户...")
    
    # 创建会话
    session = requests.Session()
    
    try:
        # 1. 访问注册页面
        print("🔍 访问注册页面...")
        response = session.get('http://localhost:5000/auth/sign', timeout=10)
        
        if response.status_code == 200:
            print("✅ 注册页面访问成功")
            
            # 2. 注册测试用户
            print("🔍 注册测试用户...")
            register_data = {
                'action': 'signup',
                'first_name': '测试',
                'last_name': '用户',
                'company_name': '测试公司',
                'email': 'test@example.com',
                'phone_number': '13800138000',
                'birthday': '1990-01-01',
                'password': 'password123',
                'confirm_password': 'password123',
                'role': 'candidate'
            }
            
            response = session.post('http://localhost:5000/auth/sign', data=register_data, timeout=10)
            
            if response.status_code == 302:
                print("✅ 用户注册成功")
                
                # 3. 尝试登录
                print("🔍 尝试登录...")
                login_data = {
                    'action': 'signin',
                    'email': 'test@example.com',
                    'password': 'password123',
                    'role': 'candidate'
                }
                
                response = session.post('http://localhost:5000/auth/sign', data=login_data, timeout=10)
                
                if response.status_code == 302:
                    print("✅ 登录成功")
                    
                    # 4. 访问求职者首页
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
                        
                        return True
                        
                    else:
                        print(f"❌ 求职者页面加载失败: {response.status_code}")
                        
                else:
                    print(f"❌ 登录失败: {response.status_code}")
                    
            else:
                print(f"❌ 注册失败: {response.status_code}")
                print("可能用户已存在，尝试直接登录...")
                
                # 尝试直接登录
                login_data = {
                    'action': 'signin',
                    'email': 'test@example.com',
                    'password': 'password123',
                    'role': 'candidate'
                }
                
                response = session.post('http://localhost:5000/auth/sign', data=login_data, timeout=10)
                
                if response.status_code == 302:
                    print("✅ 登录成功")
                    
                    # 访问求职者首页
                    response = session.get('http://localhost:5000/smartrecruit/candidate/', timeout=10)
                    
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
                        
                        return True
                
        else:
            print(f"❌ 注册页面访问失败: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 测试出错: {e}")
    
    return False

if __name__ == "__main__":
    create_test_user()
