#!/usr/bin/env python3
"""
修复现有用户密码问题
为现有用户添加密码哈希加密
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash, check_password_hash

def fix_existing_passwords():
    """修复现有用户的密码问题"""
    app = create_app()
    
    with app.app_context():
        try:
            print("开始修复现有用户密码问题...")
            
            # 获取所有用户
            users = User.query.all()
            print(f"✓ 找到 {len(users)} 个用户")
            
            fixed_count = 0
            skipped_count = 0
            
            for user in users:
                try:
                    # 检查密码是否已经加密
                    if user.password and not user.password.startswith('pbkdf2:sha256:'):
                        print(f"修复用户 {user.email} 的密码...")
                        
                        # 如果密码是明文，需要重新设置
                        # 这里我们设置一个默认密码，用户需要重新设置
                        default_password = "123456"  # 默认密码
                        user.password = generate_password_hash(default_password)
                        
                        fixed_count += 1
                        print(f"  ✓ 密码已修复，默认密码: {default_password}")
                    else:
                        skipped_count += 1
                        print(f"跳过用户 {user.email}（密码已加密）")
                        
                except Exception as e:
                    print(f"❌ 修复用户 {user.email} 失败: {e}")
                    continue
            
            # 提交更改
            try:
                db.session.commit()
                print(f"\n✅ 密码修复完成！")
                print(f"   修复了 {fixed_count} 个用户")
                print(f"   跳过了 {skipped_count} 个用户")
                
                if fixed_count > 0:
                    print(f"\n⚠️  重要提醒：")
                    print(f"   已修复的用户默认密码为: 123456")
                    print(f"   请通知这些用户尽快修改密码！")
                    
            except Exception as e:
                print(f"❌ 保存更改失败: {e}")
                db.session.rollback()
                return False
            
            return True
            
        except Exception as e:
            print(f"❌ 修复密码过程中出现错误: {e}")
            return False

def create_test_user():
    """创建一个测试用户来验证修复效果"""
    app = create_app()
    
    with app.app_context():
        try:
            print("\n创建测试用户...")
            
            # 检查是否已存在测试用户
            test_email = "test@example.com"
            existing_user = User.query.filter_by(email=test_email).first()
            if existing_user:
                print(f"⚠ 测试用户已存在: {test_email}")
                return True
            
            # 创建测试用户
            test_user = User(
                first_name="测试",
                last_name="用户",
                company_name="测试公司",
                email=test_email,
                phone_number="13800138000",
                birthday="1990-01-01",
                password=generate_password_hash("test123"),
                user_type="candidate",
                is_hr=False
            )
            
            db.session.add(test_user)
            db.session.commit()
            
            print(f"✓ 测试用户创建成功: {test_email}")
            print(f"   密码: test123")
            
            return True
            
        except Exception as e:
            print(f"❌ 创建测试用户失败: {e}")
            return False

def test_password_verification():
    """测试密码验证功能"""
    app = create_app()
    
    with app.app_context():
        try:
            print("\n测试密码验证功能...")
            
            # 查找测试用户
            test_user = User.query.filter_by(email="test@example.com").first()
            if not test_user:
                print("⚠ 未找到测试用户")
                return False
            
            # 测试正确密码
            if check_password_hash(test_user.password, "test123"):
                print("✓ 正确密码验证成功")
            else:
                print("❌ 正确密码验证失败")
                return False
            
            # 测试错误密码
            if not check_password_hash(test_user.password, "wrongpassword"):
                print("✓ 错误密码验证失败（正确行为）")
            else:
                print("❌ 错误密码验证成功（错误行为）")
                return False
            
            print("✅ 密码验证功能正常")
            return True
            
        except Exception as e:
            print(f"❌ 测试密码验证失败: {e}")
            return False

def main():
    """主函数"""
    print("=" * 60)
    print("修复现有用户密码问题脚本")
    print("=" * 60)
    
    # 修复现有密码
    if not fix_existing_passwords():
        print("❌ 修复密码失败")
        return
    
    # 创建测试用户
    if not create_test_user():
        print("❌ 创建测试用户失败")
        return
    
    # 测试密码验证
    if not test_password_verification():
        print("❌ 密码验证测试失败")
        return
    
    print("\n" + "=" * 60)
    print("🎉 密码问题修复完成！")
    print("=" * 60)
    print("\n现在您可以：")
    print("1. 新用户注册时密码会自动加密")
    print("2. 现有用户可以使用默认密码登录")
    print("3. 密码验证功能正常工作")
    print("4. 系统安全性得到提升")
    print("\n⚠️  重要提醒：")
    print("   请通知所有用户尽快修改默认密码！")

if __name__ == '__main__':
    main()
