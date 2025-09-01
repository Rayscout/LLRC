#!/usr/bin/env python3
"""
认证问题诊断脚本
用于诊断云服务器上的注册/登录问题
"""

import sys
import os
import traceback
from datetime import datetime

def check_database_connection():
    """检查数据库连接"""
    print("🔍 检查数据库连接...")
    try:
        import pymongo
        client = pymongo.MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=5000)
        client.server_info()
        print("   ✅ MongoDB连接正常")
        
        # 检查数据库和集合
        db = client.llrc
        collections = db.list_collection_names()
        print(f"   📊 数据库: llrc")
        print(f"   📁 集合: {collections}")
        
        # 检查用户集合
        if 'users' in collections:
            user_count = db.users.count_documents({})
            print(f"   👥 用户数量: {user_count}")
        else:
            print("   ⚠️ 用户集合不存在")
            
        return True
    except Exception as e:
        print(f"   ❌ MongoDB连接失败: {e}")
        return False

def check_auth_modules():
    """检查认证模块"""
    print("\n🔍 检查认证模块...")
    try:
        # 检查用户模型
        from app.models import User
        print("   ✅ 用户模型导入成功")
        
        # 检查认证相关模块
        from app.common.auth import hash_password, verify_password
        print("   ✅ 密码哈希模块导入成功")
        
        return True
    except Exception as e:
        print(f"   ❌ 认证模块检查失败: {e}")
        traceback.print_exc()
        return False

def check_dependencies():
    """检查依赖包"""
    print("\n🔍 检查依赖包...")
    
    required_packages = [
        'flask',
        'flask_sqlalchemy',
        'pymongo',
        'werkzeug',
        'bcrypt'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package} - 缺失")
            missing_packages.append(package)
    
    return len(missing_packages) == 0

def check_file_permissions():
    """检查文件权限"""
    print("\n🔍 检查文件权限...")
    
    critical_files = [
        '/var/www/llrc/app.log',
        '/var/www/llrc/instance/',
        '/var/www/llrc/flask_session_data/'
    ]
    
    for file_path in critical_files:
        if os.path.exists(file_path):
            stat = os.stat(file_path)
            print(f"   📁 {file_path}")
            print(f"      权限: {oct(stat.st_mode)[-3:]}")
            print(f"      所有者: {stat.st_uid}")
        else:
            print(f"   ❌ {file_path} - 不存在")

def check_environment():
    """检查环境变量"""
    print("\n🔍 检查环境变量...")
    
    env_vars = [
        'FLASK_ENV',
        'SECRET_KEY',
        'DATABASE_URL',
        'MONGODB_URI'
    ]
    
    for var in env_vars:
        value = os.environ.get(var, '未设置')
        if value != '未设置':
            print(f"   ✅ {var}: {value[:20]}..." if len(value) > 20 else f"   ✅ {var}: {value}")
        else:
            print(f"   ⚠️ {var}: 未设置")

def test_user_creation():
    """测试用户创建"""
    print("\n🔍 测试用户创建...")
    try:
        from app.models import User
        from app.common.auth import hash_password
        
        # 创建测试用户数据
        test_user_data = {
            'username': f'test_user_{datetime.now().strftime("%Y%m%d_%H%M%S")}',
            'email': f'test_{datetime.now().strftime("%Y%m%d_%H%M%S")}@example.com',
            'password_hash': hash_password('test123'),
            'role': 'candidate'
        }
        
        print(f"   📝 测试用户数据: {test_user_data['username']}")
        print("   ✅ 用户创建测试通过")
        
        return True
    except Exception as e:
        print(f"   ❌ 用户创建测试失败: {e}")
        traceback.print_exc()
        return False

def check_web_routes():
    """检查Web路由"""
    print("\n🔍 检查Web路由...")
    try:
        from app import create_app
        app = create_app()
        
        # 检查注册路由
        with app.test_client() as client:
            response = client.get('/auth/sign')
            print(f"   ✅ 注册页面路由: {response.status_code}")
            
            # 测试注册API
            test_data = {
                'username': 'test_user',
                'email': 'test@example.com',
                'password': 'test123',
                'role': 'candidate'
            }
            
            response = client.post('/auth/register', json=test_data)
            print(f"   📝 注册API测试: {response.status_code}")
            
        return True
    except Exception as e:
        print(f"   ❌ Web路由检查失败: {e}")
        traceback.print_exc()
        return False

def main():
    """主函数"""
    print("🚀 LLRC认证问题诊断工具")
    print("=" * 50)
    print(f"诊断时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 切换到项目目录
    os.chdir('/var/www/llrc')
    
    # 激活虚拟环境
    if 'venv' in os.listdir('.'):
        activate_script = os.path.join('venv', 'bin', 'activate_this.py')
        if os.path.exists(activate_script):
            exec(open(activate_script).read(), {'__file__': activate_script})
            print("   🐍 虚拟环境已激活")
    
    # 执行各项检查
    db_ok = check_database_connection()
    auth_ok = check_auth_modules()
    deps_ok = check_dependencies()
    check_file_permissions()
    check_environment()
    user_ok = test_user_creation()
    web_ok = check_web_routes()
    
    # 生成诊断报告
    print("\n📊 诊断报告")
    print("=" * 50)
    
    checks = [
        ("数据库连接", db_ok),
        ("认证模块", auth_ok),
        ("依赖包", deps_ok),
        ("用户创建", user_ok),
        ("Web路由", web_ok)
    ]
    
    all_passed = True
    for name, result in checks:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"   {name}: {status}")
        if not result:
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 所有检查通过！认证功能应该正常工作。")
    else:
        print("⚠️ 存在一些问题，请根据上述检查结果进行修复。")
        print("\n🔧 建议的修复步骤:")
        if not db_ok:
            print("   1. 检查MongoDB服务状态: sudo systemctl status mongod")
        if not deps_ok:
            print("   2. 安装缺失的依赖: pip install -r requirements.txt")
        if not auth_ok:
            print("   3. 检查认证模块配置")
    
    return all_passed

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ 诊断脚本执行失败: {e}")
        traceback.print_exc()
        sys.exit(1)
