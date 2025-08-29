#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复账号密码问题
重新设置正确的密码哈希
"""

import os
import sys

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

def fix_accounts():
    """修复账号密码问题"""
    app = create_app()
    
    with app.app_context():
        try:
            print("=" * 60)
            print("修复账号密码问题")
            print("=" * 60)
            
            # 修复HR账号密码
            print("\n🔧 修复HR账号密码...")
            hr_users = User.query.filter_by(is_hr=True).all()
            for hr in hr_users:
                if not hr.password.startswith('scrypt:'):
                    old_password = hr.password
                    hr.password = generate_password_hash('123456')
                    db.session.commit()
                    print(f"✓ 修复HR账号 {hr.email} 的密码")
                    print(f"  旧密码: {old_password}")
                    print(f"  新密码哈希: {hr.password[:30]}...")
                else:
                    print(f"✓ HR账号 {hr.email} 密码已正确")
            
            # 修复求职者账号密码
            print("\n🔧 修复求职者账号密码...")
            candidate_users = User.query.filter_by(is_hr=False).all()
            fixed_count = 0
            for candidate in candidate_users:
                if not candidate.password.startswith('scrypt:'):
                    old_password = candidate.password
                    candidate.password = generate_password_hash('123456')
                    fixed_count += 1
                else:
                    print(f"✓ 求职者账号 {candidate.email} 密码已正确")
            
            if fixed_count > 0:
                db.session.commit()
                print(f"✓ 修复了 {fixed_count} 个求职者账号的密码")
            
            # 验证修复结果
            print("\n🔍 验证修复结果...")
            hr_users = User.query.filter_by(is_hr=True).all()
            print(f"\nHR账号 (共 {len(hr_users)} 个):")
            for i, hr in enumerate(hr_users, 1):
                print(f"  {i}. {hr.email}")
                print(f"     密码哈希: {hr.password[:30]}...")
                print(f"     是否有效哈希: {'是' if hr.password.startswith('scrypt:') else '否'}")
            
            # 显示可用的测试账号
            print(f"\n🎯 可用的测试账号:")
            print("\nHR账号 (密码: 123456):")
            for i, hr in enumerate(hr_users, 1):
                print(f"  {i}. {hr.email} - {hr.first_name}{hr.last_name} ({hr.department})")
            
            # 显示新创建的求职者账号
            new_candidates = [
                'tech_candidate1@email.com',
                'tech_candidate2@email.com', 
                'tech_candidate3@email.com',
                'market_candidate1@email.com',
                'market_candidate2@email.com',
                'operation_candidate1@email.com',
                'operation_candidate2@email.com'
            ]
            
            print(f"\n求职者账号 (密码: 123456):")
            for email in new_candidates:
                candidate = User.query.filter_by(email=email).first()
                if candidate:
                    print(f"  - {email} - {candidate.first_name}{candidate.last_name}")
            
            print(f"\n✅ 密码修复完成！")
            print(f"现在您可以使用以下账号登录:")
            print(f"1. HR账号: 任意HR邮箱 + 密码: 123456")
            print(f"2. 求职者账号: 任意求职者邮箱 + 密码: 123456")
            
            return True
            
        except Exception as e:
            print(f"❌ 修复账号失败: {e}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == '__main__':
    fix_accounts()
