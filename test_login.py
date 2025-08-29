#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试登录功能
"""

import os
import sys

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from app import create_app, db
from app.models import User
from werkzeug.security import check_password_hash

def test_login():
    """测试登录功能"""
    app = create_app()
    
    with app.app_context():
        try:
            print("=" * 60)
            print("测试登录功能")
            print("=" * 60)
            
            # 测试HR账号登录
            print("\n🔍 测试HR账号登录...")
            hr_email = 'hr_tech@company.com'
            hr_password = '123456'
            
            hr_user = User.query.filter_by(email=hr_email).first()
            if hr_user:
                print(f"✓ 找到HR用户: {hr_user.email}")
                print(f"  姓名: {hr_user.first_name}{hr_user.last_name}")
                print(f"  部门: {hr_user.department}")
                print(f"  是否HR: {hr_user.is_hr}")
                print(f"  密码哈希: {hr_user.password[:30]}...")
                
                # 测试密码验证
                if check_password_hash(hr_user.password, hr_password):
                    print(f"✓ 密码验证成功！")
                else:
                    print(f"✗ 密码验证失败！")
            else:
                print(f"✗ 未找到HR用户: {hr_email}")
            
            # 测试求职者账号登录
            print("\n🔍 测试求职者账号登录...")
            candidate_email = 'tech_candidate1@email.com'
            candidate_password = '123456'
            
            candidate_user = User.query.filter_by(email=candidate_email).first()
            if candidate_user:
                print(f"✓ 找到求职者用户: {candidate_user.email}")
                print(f"  姓名: {candidate_user.first_name}{candidate_user.last_name}")
                print(f"  应聘职位: {candidate_user.position}")
                print(f"  是否HR: {candidate_user.is_hr}")
                print(f"  密码哈希: {candidate_user.password[:30]}...")
                
                # 测试密码验证
                if check_password_hash(candidate_user.password, candidate_password):
                    print(f"✓ 密码验证成功！")
                else:
                    print(f"✗ 密码验证失败！")
            else:
                print(f"✗ 未找到求职者用户: {candidate_email}")
            
            # 测试错误的密码
            print("\n🔍 测试错误密码...")
            wrong_password = 'wrong_password'
            
            if hr_user and check_password_hash(hr_user.password, wrong_password):
                print(f"✗ 错误密码验证成功（这是错误的！）")
            else:
                print(f"✓ 错误密码验证失败（这是正确的！）")
            
            print(f"\n✅ 登录功能测试完成！")
            print(f"现在您可以使用以下账号登录:")
            print(f"1. HR账号: {hr_email} + 密码: {hr_password}")
            print(f"2. 求职者账号: {candidate_email} + 密码: {candidate_password}")
            
            return True
            
        except Exception as e:
            print(f"❌ 测试登录失败: {e}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == '__main__':
    test_login()
