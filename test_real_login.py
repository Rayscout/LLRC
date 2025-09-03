#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试真实登录的脚本
"""

import os
import sys
import traceback

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_real_login():
    """测试真实登录"""
    try:
        print("=== 测试真实登录 ===")
        from app import create_app
        app = create_app()
        
        with app.test_client() as client:
            print("1. 检查数据库中的用户")
            with app.app_context():
                from app.models import User
                
                # 查找所有候选人用户
                candidates = User.query.filter_by(user_type='candidate').all()
                print(f"   找到 {len(candidates)} 个候选人用户:")
                for user in candidates:
                    print(f"     ID: {user.id}, 邮箱: {user.email}, 姓名: {user.first_name} {user.last_name}")
                
                # 查找所有用户
                all_users = User.query.limit(5).all()
                print(f"\n   前5个用户:")
                for user in all_users:
                    print(f"     ID: {user.id}, 邮箱: {user.email}, 类型: {getattr(user, 'user_type', 'N/A')}, 姓名: {user.first_name} {user.last_name}")
            
            print("\n2. 尝试使用真实用户登录")
            
            # 使用第一个候选人用户
            if candidates:
                test_user = candidates[0]
                print(f"   使用用户: {test_user.email}")
                
                login_data = {
                    'email': test_user.email,
                    'password': 'password123',  # 假设密码
                    'role': 'candidate'
                }
                
                # 尝试登录
                response = client.post('/auth/sign', data=login_data, follow_redirects=False)
                print(f"   登录POST状态码: {response.status_code}")
                
                if response.status_code == 302:
                    print(f"   登录后重定向到: {response.headers.get('Location', 'Unknown')}")
                
                # 检查会话状态
                with client.session_transaction() as sess:
                    print(f"   会话内容: {dict(sess)}")
                    user_id = sess.get('user_id')
                    user_type = sess.get('user_type')
                    print(f"   user_id: {user_id}")
                    print(f"   user_type: {user_type}")
                
                # 如果登录成功，测试申请路由
                if user_id and user_type:
                    print("\n3. 测试已登录状态下的申请路由")
                    response = client.get('/smartrecruit/candidate/applications/pre_apply/4')
                    print(f"   状态码: {response.status_code}")
                    
                    if response.status_code == 500:
                        print("❌ 500错误 - 分析错误内容...")
                        error_content = response.data.decode('utf-8', errors='ignore')
                        print(f"   错误响应长度: {len(error_content)}")
                        print(f"   错误响应前1000字符: {error_content[:1000]}")
                    elif response.status_code == 200:
                        print("✅ 200成功")
                        print(f"   响应长度: {len(response.data)}")
                    else:
                        print(f"   其他状态码: {response.status_code}")
                else:
                    print("❌ 登录失败，无法测试申请路由")
                    
            else:
                print("❌ 没有找到候选人用户")
                
    except Exception as e:
        print(f"❌ 真实登录测试失败: {e}")
        traceback.print_exc()

def test_password_verification():
    """测试密码验证"""
    try:
        print("\n=== 测试密码验证 ===")
        from app import create_app
        app = create_app()
        
        with app.app_context():
            from app.models import User
            
            # 查找候选人用户
            candidates = User.query.filter_by(user_type='candidate').all()
            if candidates:
                test_user = candidates[0]
                print(f"   测试用户: {test_user.email}")
                print(f"   用户类型: {test_user.user_type}")
                print(f"   密码字段: {hasattr(test_user, 'password')}")
                
                if hasattr(test_user, 'password'):
                    print(f"   密码值: {test_user.password}")
                    print(f"   密码长度: {len(test_user.password) if test_user.password else 0}")
                else:
                    print("   用户没有密码字段")
                    
    except Exception as e:
        print(f"❌ 密码验证测试失败: {e}")
        traceback.print_exc()

def main():
    """主函数"""
    print("开始测试真实登录...")
    
    # 测试真实登录
    test_real_login()
    
    # 测试密码验证
    test_password_verification()
    
    print("\n=== 真实登录测试完成 ===")

if __name__ == "__main__":
    main()
