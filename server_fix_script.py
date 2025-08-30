#!/usr/bin/env python3
"""
服务器端认证问题修复脚本
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(command, description=""):
    """运行命令并返回结果"""
    print(f"🔧 {description}")
    print(f"   执行: {command}")
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"   ✅ 成功")
            if result.stdout.strip():
                print(f"   输出: {result.stdout.strip()}")
        else:
            print(f"   ❌ 失败")
            if result.stderr.strip():
                print(f"   错误: {result.stderr.strip()}")
        return result.returncode == 0
    except Exception as e:
        print(f"   ❌ 异常: {e}")
        return False

def fix_file_permissions():
    """修复文件权限"""
    print("\n🔐 修复文件权限...")
    
    # 修复项目目录权限
    run_command("sudo chown -R llrcuser:llrcuser /var/www/llrc", "修复项目目录权限")
    
    # 修复关键目录权限
    critical_dirs = [
        "/var/www/llrc/instance",
        "/var/www/llrc/flask_session_data",
        "/var/www/llrc/venv"
    ]
    
    for dir_path in critical_dirs:
        if os.path.exists(dir_path):
            run_command(f"sudo chmod -R 755 {dir_path}", f"修复目录权限: {dir_path}")
            run_command(f"sudo chown -R llrcuser:llrcuser {dir_path}", f"修复目录所有者: {dir_path}")

def fix_database_issues():
    """修复数据库问题"""
    print("\n🗄️ 修复数据库问题...")
    
    # 重启MongoDB服务
    run_command("sudo systemctl restart mongod", "重启MongoDB服务")
    
    # 检查MongoDB状态
    run_command("sudo systemctl status mongod --no-pager", "检查MongoDB状态")
    
    # 检查端口监听
    run_command("sudo netstat -tlnp | grep :27017", "检查MongoDB端口")

def fix_dependencies():
    """修复依赖问题"""
    print("\n📦 修复依赖问题...")
    
    # 激活虚拟环境
    venv_path = "/var/www/llrc/venv"
    if os.path.exists(venv_path):
        activate_script = os.path.join(venv_path, "bin", "activate")
        if os.path.exists(activate_script):
            print("   🐍 激活虚拟环境...")
            
            # 升级pip
            run_command(f"source {activate_script} && pip install --upgrade pip", "升级pip")
            
            # 安装/更新依赖
            run_command(f"source {activate_script} && pip install -r requirements.txt", "安装项目依赖")
            
            # 安装认证相关依赖
            auth_packages = [
                "bcrypt",
                "flask-login",
                "flask-session",
                "werkzeug"
            ]
            
            for package in auth_packages:
                run_command(f"source {activate_script} && pip install {package}", f"安装 {package}")

def fix_environment_config():
    """修复环境配置"""
    print("\n⚙️ 修复环境配置...")
    
    # 检查.env文件
    env_file = "/var/www/llrc/.env"
    if os.path.exists(env_file):
        print(f"   📁 找到.env文件: {env_file}")
        
        # 备份.env文件
        backup_file = f"{env_file}.backup.{int(os.time.time())}"
        shutil.copy2(env_file, backup_file)
        print(f"   💾 已备份到: {backup_file}")
        
        # 检查必要的环境变量
        with open(env_file, 'r') as f:
            content = f.read()
        
        required_vars = [
            'SECRET_KEY',
            'FLASK_ENV',
            'MONGODB_URI'
        ]
        
        missing_vars = []
        for var in required_vars:
            if var not in content:
                missing_vars.append(var)
        
        if missing_vars:
            print(f"   ⚠️ 缺失环境变量: {missing_vars}")
            
            # 添加缺失的环境变量
            with open(env_file, 'a') as f:
                f.write(f"\n# 自动添加的环境变量\n")
                f.write(f"SECRET_KEY=your-secret-key-here-{os.urandom(16).hex()}\n")
                f.write(f"FLASK_ENV=production\n")
                f.write(f"MONGODB_URI=mongodb://localhost:27017/llrc\n")
            
            print("   ✅ 已添加缺失的环境变量")
    else:
        print("   ❌ 未找到.env文件，创建默认配置...")
        
        # 创建默认.env文件
        env_content = f"""# LLRC环境配置
SECRET_KEY=your-secret-key-here-{os.urandom(16).hex()}
FLASK_ENV=production
MONGODB_URI=mongodb://localhost:27017/llrc
DATABASE_URL=sqlite:///instance/site.db
"""
        
        with open(env_file, 'w') as f:
            f.write(env_content)
        
        print("   ✅ 已创建默认.env文件")

def restart_services():
    """重启服务"""
    print("\n🔄 重启服务...")
    
    # 重启LLRC服务
    run_command("sudo systemctl restart llrc", "重启LLRC服务")
    
    # 重启Nginx服务
    run_command("sudo systemctl restart nginx", "重启Nginx服务")
    
    # 检查服务状态
    run_command("sudo systemctl status llrc --no-pager", "检查LLRC服务状态")
    run_command("sudo systemctl status nginx --no-pager", "检查Nginx服务状态")

def test_fix():
    """测试修复结果"""
    print("\n🧪 测试修复结果...")
    
    # 测试健康检查
    run_command("curl -s http://localhost/health", "测试健康检查")
    
    # 测试注册页面
    run_command("curl -s -o /dev/null -w '%{http_code}' http://localhost/auth/sign", "测试注册页面")
    
    # 测试数据库连接
    test_script = """
import pymongo
try:
    client = pymongo.MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=5000)
    client.server_info()
    print("✅ MongoDB连接正常")
    db = client.llrc
    collections = db.list_collection_names()
    print(f"📁 集合: {collections}")
except Exception as e:
    print(f"❌ MongoDB连接失败: {e}")
"""
    
    with open("/tmp/test_db.py", "w") as f:
        f.write(test_script)
    
    run_command("python3 /tmp/test_db.py", "测试数据库连接")
    run_command("rm /tmp/test_db.py", "清理测试文件")

def main():
    """主函数"""
    print("🚀 LLRC认证问题修复工具")
    print("=" * 50)
    
    # 检查是否为root用户
    if os.geteuid() == 0:
        print("❌ 请不要使用root用户运行此脚本")
        sys.exit(1)
    
    # 执行修复步骤
    fix_file_permissions()
    fix_database_issues()
    fix_dependencies()
    fix_environment_config()
    restart_services()
    test_fix()
    
    print("\n🎉 修复完成！")
    print("\n📋 下一步操作:")
    print("1. 访问 http://60.205.251.52/auth/sign 测试注册功能")
    print("2. 如果仍有问题，运行诊断脚本: python3 diagnose_auth_issues.py")
    print("3. 查看详细日志: sudo journalctl -u llrc -f")

if __name__ == "__main__":
    main()
