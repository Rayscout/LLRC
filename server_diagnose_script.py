#!/usr/bin/env python3
"""
服务器端认证问题诊断脚本
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

def check_services():
    """检查服务状态"""
    print("\n🔍 检查服务状态...")
    
    import subprocess
    
    services = ['llrc', 'mongod', 'nginx']
    
    for service in services:
        try:
            result = subprocess.run(['systemctl', 'is-active', service], 
                                  capture_output=True, text=True)
            status = result.stdout.strip()
            print(f"   🔧 {service}: {status}")
        except Exception as e:
            print(f"   ❌ {service}: 检查失败 - {e}")

def test_web_endpoints():
    """测试Web端点"""
    print("\n🔍 测试Web端点...")
    
    import subprocess
    
    endpoints = [
        ('http://localhost/health', '健康检查'),
        ('http://localhost/auth/sign', '注册页面')
    ]
    
    for url, description in endpoints:
        try:
            result = subprocess.run(['curl', '-s', '-o', '/dev/null', '-w', '%{http_code}', url], 
                                  capture_output=True, text=True)
            status_code = result.stdout.strip()
            print(f"   🌐 {description}: {status_code}")
        except Exception as e:
            print(f"   ❌ {description}: 测试失败 - {e}")

def main():
    """主函数"""
    print("🚀 LLRC认证问题诊断工具")
    print("=" * 50)
    print(f"诊断时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 执行各项检查
    db_ok = check_database_connection()
    deps_ok = check_dependencies()
    check_file_permissions()
    check_environment()
    check_services()
    test_web_endpoints()
    
    # 生成诊断报告
    print("\n📊 诊断报告")
    print("=" * 50)
    
    checks = [
        ("数据库连接", db_ok),
        ("依赖包", deps_ok)
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
    
    return all_passed

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ 诊断脚本执行失败: {e}")
        traceback.print_exc()
        sys.exit(1)
