#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复HR账号用户类型脚本
"""

import os
import sys

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from app import create_app, db
from app.models import User

def fix_hr_user_types():
    """修复HR账号的用户类型"""
    app = create_app()
    
    with app.app_context():
        try:
            print("=" * 60)
            print("修复HR账号用户类型")
            print("=" * 60)
            
            # 查找所有HR账号
            hr_users = User.query.filter_by(is_hr=True).all()
            
            print(f"\n🔍 找到 {len(hr_users)} 个HR账号:")
            
            fixed_count = 0
            for i, hr in enumerate(hr_users, 1):
                print(f"\n  {i}. {hr.email}")
                print(f"     姓名: {hr.first_name}{hr.last_name}")
                print(f"     当前用户类型: {hr.user_type}")
                print(f"     部门: {hr.department}")
                
                # 检查是否需要修复
                if hr.user_type != 'recruiter':
                    print(f"     ✗ 需要修复: {hr.user_type} → recruiter")
                    hr.user_type = 'recruiter'
                    fixed_count += 1
                else:
                    print(f"     ✓ 用户类型正确")
            
            if fixed_count > 0:
                # 提交更改
                db.session.commit()
                print(f"\n✅ 成功修复 {fixed_count} 个HR账号的用户类型")
            else:
                print(f"\n✅ 所有HR账号的用户类型都是正确的")
            
            # 验证修复结果
            print(f"\n🔍 验证修复结果:")
            hr_users_after = User.query.filter_by(is_hr=True).all()
            for hr in hr_users_after:
                print(f"  - {hr.email}: {hr.user_type}")
            
            print(f"\n📋 登录说明:")
            print("现在所有HR账号都应该选择 'HR' 角色登录:")
            print("\nHR账号 (密码: 123456):")
            for hr in hr_users_after[:5]:  # 显示前5个
                print(f"  - {hr.email} ({hr.first_name}{hr.last_name})")
            
            print(f"\n🌐 访问地址: http://localhost:5000")
            print("登录时选择 'HR' 角色")
            
            return True
            
        except Exception as e:
            print(f"❌ 修复失败: {e}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == '__main__':
    fix_hr_user_types()
