#!/usr/bin/env python3
"""
快速测试用户注册功能
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash, check_password_hash

def quick_test():
    """快速测试注册功能"""
    app = create_app()
    
    with app.app_context():
        try:
            print("🚀 开始快速测试用户注册功能...")
            
            # 测试1: 检查数据库连接
            print("\n1. 测试数据库连接...")
            try:
                # 使用新版本的SQLAlchemy语法
                with db.engine.connect() as conn:
                    conn.execute(db.text('SELECT 1'))
                print("✅ 数据库连接正常")
            except Exception as e:
                print(f"❌ 数据库连接失败: {e}")
                return False
            
            # 测试2: 检查User模型
            print("\n2. 测试User模型...")
            try:
                # 检查表是否存在
                inspector = db.inspect(db.engine)
                tables = inspector.get_table_names()
                if 'user' in tables:
                    print("✅ User表存在")
                else:
                    print("❌ User表不存在")
                    return False
                
                # 检查字段
                columns = inspector.get_columns('user')
                required_fields = ['first_name', 'last_name', 'email', 'password']
                for field in required_fields:
                    if any(col['name'] == field for col in columns):
                        print(f"✅ 字段 {field} 存在")
                    else:
                        print(f"❌ 字段 {field} 不存在")
                        return False
                        
            except Exception as e:
                print(f"❌ 检查User模型失败: {e}")
                return False
            
            # 测试3: 创建测试用户
            print("\n3. 测试创建用户...")
            try:
                # 删除可能存在的测试用户
                test_email = "quick_test@example.com"
                existing_user = User.query.filter_by(email=test_email).first()
                if existing_user:
                    db.session.delete(existing_user)
                    db.session.commit()
                    print("⚠️ 删除已存在的测试用户")
                
                # 创建新测试用户
                test_user = User(
                    first_name="快速",
                    last_name="测试",
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
                
                print(f"✅ 测试用户创建成功: {test_user.email}")
                print(f"   用户ID: {test_user.id}")
                print(f"   密码哈希: {test_user.password[:50]}...")
                
            except Exception as e:
                print(f"❌ 创建测试用户失败: {e}")
                print(f"   错误类型: {type(e).__name__}")
                print(f"   错误详情: {str(e)}")
                return False
            
            # 测试4: 验证密码
            print("\n4. 测试密码验证...")
            try:
                if check_password_hash(test_user.password, "test123"):
                    print("✅ 密码验证成功")
                else:
                    print("❌ 密码验证失败")
                    return False
            except Exception as e:
                print(f"❌ 密码验证测试失败: {e}")
                return False
            
            # 测试5: 清理测试数据
            print("\n5. 清理测试数据...")
            try:
                db.session.delete(test_user)
                db.session.commit()
                print("✅ 测试数据清理完成")
            except Exception as e:
                print(f"⚠️ 清理测试数据失败: {e}")
            
            print("\n🎉 所有测试通过！用户注册功能工作正常")
            return True
            
        except Exception as e:
            print(f"❌ 测试过程中出现未预期的错误: {e}")
            print(f"   错误类型: {type(e).__name__}")
            import traceback
            print(f"   错误追踪:\n{traceback.format_exc()}")
            return False

def check_environment():
    """检查运行环境"""
    print("🔍 检查运行环境...")
    
    # 检查Python版本
    print(f"Python版本: {sys.version}")
    
    # 检查当前工作目录
    print(f"当前工作目录: {os.getcwd()}")
    
    # 检查关键文件
    key_files = [
        'app/__init__.py',
        'app/models.py',
        'app/common/auth.py',
        'run.py'
    ]
    
    for file_path in key_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path} 存在")
        else:
            print(f"❌ {file_path} 不存在")
    
    # 检查数据库文件
    db_files = [
        'instance/site.db',
        'site.db'
    ]
    
    for db_file in db_files:
        if os.path.exists(db_file):
            print(f"✅ 数据库文件 {db_file} 存在")
            # 检查文件大小
            size = os.path.getsize(db_file)
            print(f"   文件大小: {size} 字节")
        else:
            print(f"⚠️ 数据库文件 {db_file} 不存在")

def main():
    """主函数"""
    print("=" * 60)
    print("用户注册功能快速测试")
    print("=" * 60)
    
    # 检查环境
    check_environment()
    
    print("\n" + "=" * 60)
    
    # 运行测试
    if quick_test():
        print("\n✅ 测试结果: 用户注册功能正常")
        print("\n现在您可以:")
        print("1. 重新启动Flask应用 (python run.py)")
        print("2. 在网页上尝试注册新用户")
        print("3. 如果还有错误，查看控制台输出的详细错误信息")
    else:
        print("\n❌ 测试结果: 用户注册功能存在问题")
        print("\n请检查:")
        print("1. 数据库连接是否正常")
        print("2. 数据库表结构是否正确")
        print("3. 模型定义是否有问题")
        print("4. 依赖包是否正确安装")

if __name__ == '__main__':
    main()
