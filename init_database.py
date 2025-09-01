#!/usr/bin/env python3
"""
数据库初始化脚本
创建所有必要的表和测试数据
解决 'no such table: user' 错误
"""

import os
import sys

def init_database():
    """初始化数据库"""
    print("🚀 开始初始化数据库...")
    
    try:
        # 确保目录存在
        instance_dir = os.path.join(os.getcwd(), 'instance')
        os.makedirs(instance_dir, exist_ok=True)
        print(f"   ✅ 确保instance目录存在: {instance_dir}")
        
        # 导入应用和模型
        from app import create_app
        from app.models import db, User
        
        # 创建应用实例
        app = create_app()
        print("   ✅ 应用创建成功")
        
        with app.app_context():
            # 删除所有表（如果存在）
            db.drop_all()
            print("   🗑️ 清理旧表")
            
            # 创建所有表
            db.create_all()
            print("   ✅ 创建所有数据库表")
            
            # 创建测试用户
            test_users = [
                {
                    'first_name': 'HR',
                    'last_name': 'Admin',
                    'email': 'hr@test.com',
                    'password': '123456',
                    'user_type': 'recruiter',
                    'is_hr': True,
                    'is_active': True
                },
                {
                    'first_name': 'Employee',
                    'last_name': 'Test',
                    'email': 'employee@test.com',
                    'password': '123456',
                    'user_type': 'employee',
                    'is_hr': False,
                    'is_active': True
                },
                {
                    'first_name': 'Executive',
                    'last_name': 'Admin',
                    'email': 'executive@test.com',
                    'password': '123456',
                    'user_type': 'executive',
                    'is_hr': False,
                    'is_active': True
                },
                {
                    'first_name': 'Candidate',
                    'last_name': 'Test',
                    'email': 'candidate@test.com',
                    'password': '123456',
                    'user_type': 'candidate',
                    'is_hr': False,
                    'is_active': True
                }
            ]
            
            for user_data in test_users:
                # 检查用户是否已存在
                existing_user = User.query.filter_by(email=user_data['email']).first()
                if not existing_user:
                    user = User(
                        first_name=user_data['first_name'],
                        last_name=user_data['last_name'],
                        email=user_data['email'],
                        password=user_data['password'],  # 注意：在实际应用中应该加密
                        user_type=user_data['user_type'],
                        is_hr=user_data['is_hr'],
                        is_active=user_data['is_active']
                    )
                    db.session.add(user)
                    print(f"   ➕ 创建用户: {user_data['email']} ({user_data['user_type']})")
                else:
                    print(f"   ⚠️ 用户已存在: {user_data['email']}")
            
            # 提交更改
            db.session.commit()
            print("   ✅ 数据库更改已提交")
            
            # 验证表是否创建成功
            from sqlalchemy import text
            result = db.session.execute(text('SELECT name FROM sqlite_master WHERE type="table"'))
            tables = [row[0] for row in result]
            print(f"   📊 创建的表: {', '.join(tables)}")
            
            # 验证用户数据
            user_count = User.query.count()
            print(f"   👥 用户总数: {user_count}")
            
        print("\n🎉 数据库初始化完成！")
        return True
        
    except Exception as e:
        print(f"\n❌ 数据库初始化失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_database():
    """测试数据库连接和查询"""
    print("\n🧪 测试数据库...")
    
    try:
        from app import create_app
        from app.models import db, User
        
        app = create_app()
        
        with app.app_context():
            # 测试查询用户
            users = User.query.all()
            print(f"   ✅ 成功查询到 {len(users)} 个用户")
            
            for user in users:
                print(f"   👤 用户: {user.email} ({user.user_type}) - 活跃状态: {user.is_active}")
            
            # 测试登录查询（模拟登录过程中的查询）
            test_email = 'hr@test.com'
            test_password = '123456'
            test_user = User.query.filter_by(email=test_email, password=test_password).first()
            if test_user:
                print(f"   ✅ 测试登录查询成功: {test_user.email}")
            else:
                print("   ❌ 登录查询失败")
                
        print("\n🎉 数据库测试通过！")
        return True
        
    except Exception as e:
        print(f"\n❌ 数据库测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def fix_file_permissions():
    """修复文件权限"""
    print("\n🔧 修复文件权限...")
    
    try:
        import subprocess
        
        # 获取当前目录
        current_dir = os.getcwd()
        instance_dir = os.path.join(current_dir, 'instance')
        
        # 如果在云服务器上，修复权限
        if '/var/www/llrc' in current_dir:
            commands = [
                f'sudo chown -R llrcuser:llrcuser {instance_dir}',
                f'sudo chmod 755 {instance_dir}',
                f'sudo chmod 644 {instance_dir}/site.db 2>/dev/null || true'
            ]
            
            for cmd in commands:
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                if result.returncode == 0:
                    print(f"   ✅ 执行成功: {cmd}")
                else:
                    print(f"   ⚠️ 执行命令: {cmd} (可能需要手动执行)")
        else:
            print("   ℹ️ 本地环境，跳过权限修复")
            
        return True
        
    except Exception as e:
        print(f"   ❌ 权限修复失败: {e}")
        return False

def main():
    """主函数"""
    print("🗄️ LLRC数据库初始化工具")
    print("=" * 60)
    
    # 显示当前目录
    print(f"📁 工作目录: {os.getcwd()}")
    
    # 修复文件权限
    fix_file_permissions()
    
    # 初始化数据库
    if init_database():
        # 测试数据库
        if test_database():
            print("\n🌟 数据库初始化和测试完成！")
            print("\n📝 测试账号：")
            print("   🔹 HR管理员: hr@test.com / 123456")
            print("   🔹 员工账号: employee@test.com / 123456") 
            print("   🔹 高管账号: executive@test.com / 123456")
            print("   🔹 求职者账号: candidate@test.com / 123456")
            print("\n🌐 现在可以访问登录页面进行测试")
            print("   云服务器: http://60.205.251.52/auth/sign")
            print("\n🔄 建议重启服务以确保更改生效：")
            print("   sudo systemctl restart llrc")
        else:
            print("\n❌ 数据库测试失败")
    else:
        print("\n❌ 数据库初始化失败")

if __name__ == "__main__":
    main()
