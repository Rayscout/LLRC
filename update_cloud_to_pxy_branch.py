#!/usr/bin/env python3
"""
云服务器更新到pxy分支脚本
用于将云服务器从RayScout分支更新到pxy分支
"""

import os
import sys
import subprocess
import shutil
import time

def run_command(command, description="", check_output=False):
    """运行命令并返回结果"""
    print(f"🔧 {description}")
    print(f"   执行: {command}")
    
    try:
        if check_output:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=60)
        else:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"   ✅ 成功")
            if result.stdout.strip():
                print(f"   输出: {result.stdout.strip()}")
            return result.stdout.strip() if check_output else True
        else:
            print(f"   ❌ 失败")
            if result.stderr.strip():
                print(f"   错误: {result.stderr.strip()}")
            return False
    except subprocess.TimeoutExpired:
        print(f"   ⏰ 命令超时")
        return False
    except Exception as e:
        print(f"   ❌ 异常: {e}")
        return False

def backup_current_version():
    """备份当前版本"""
    print("\n💾 备份当前版本...")
    
    backup_dir = f"/var/www/llrc_backup_rayscout_{int(time.time())}"
    run_command(f"sudo cp -r /var/www/llrc {backup_dir}", f"备份到 {backup_dir}")
    
    if os.path.exists(backup_dir):
        print(f"   ✅ 备份完成: {backup_dir}")
        return backup_dir
    else:
        print("   ❌ 备份失败")
        return None

def update_to_pxy_branch():
    """更新到pxy分支"""
    print("\n📥 更新到pxy分支...")
    
    # 切换到项目目录
    os.chdir("/var/www/llrc")
    
    # 保存当前分支
    current_branch = run_command("git branch --show-current", "获取当前分支", True)
    print(f"   🌿 当前分支: {current_branch}")
    
    # 拉取最新代码
    run_command("git fetch origin", "拉取最新代码")
    
    # 切换到pxy分支
    run_command("git checkout pxy", "切换到pxy分支")
    
    # 拉取pxy分支最新代码
    run_command("git pull origin pxy", "拉取pxy分支最新代码")
    
    # 检查更新结果
    latest_commit = run_command("git log --oneline -1", "获取最新提交", True)
    if latest_commit:
        print(f"   📝 最新提交: {latest_commit}")

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
                "werkzeug",
                "flask-sqlalchemy",
                "pymongo",
                "python-dotenv"
            ]
            
            for package in auth_packages:
                run_command(f"source {activate_script} && pip install {package}", f"安装 {package}")
        else:
            print("   ❌ 虚拟环境激活脚本不存在")
    else:
        print("   ❌ 虚拟环境不存在")

def fix_database_issues():
    """修复数据库问题"""
    print("\n🗄️ 修复数据库问题...")
    
    # 重启MongoDB服务
    run_command("sudo systemctl restart mongod", "重启MongoDB服务")
    
    # 检查MongoDB状态
    run_command("sudo systemctl status mongod --no-pager", "检查MongoDB状态")
    
    # 检查端口监听
    run_command("sudo netstat -tlnp | grep :27017", "检查MongoDB端口")
    
    # 初始化数据库
    run_command("cd /var/www/llrc && python3 init_db.py", "初始化数据库")

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

def fix_environment_config():
    """修复环境配置"""
    print("\n⚙️ 修复环境配置...")
    
    # 检查.env文件
    env_file = "/var/www/llrc/.env"
    if os.path.exists(env_file):
        print(f"   📁 找到.env文件: {env_file}")
        
        # 备份.env文件
        backup_file = f"{env_file}.backup.{int(time.time())}"
        shutil.copy2(env_file, backup_file)
        print(f"   💾 已备份到: {backup_file}")
        
        # 检查必要的环境变量
        with open(env_file, 'r') as f:
            content = f.read()
        
        required_vars = [
            'SECRET_KEY',
            'FLASK_ENV',
            'MONGODB_URI',
            'DATABASE_URL'
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
                f.write(f"DATABASE_URL=sqlite:///instance/site.db\n")
            
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

def test_application():
    """测试应用"""
    print("\n🧪 测试应用...")
    
    # 等待服务启动
    print("   ⏳ 等待服务启动...")
    time.sleep(10)
    
    # 测试健康检查
    health_result = run_command("curl -s http://localhost/health", "测试健康检查", True)
    if health_result:
        print(f"   ✅ 健康检查: {health_result}")
    
    # 测试注册页面
    sign_result = run_command("curl -s -o /dev/null -w '%{http_code}' http://localhost/auth/sign", "测试注册页面", True)
    if sign_result:
        print(f"   ✅ 注册页面: HTTP {sign_result}")
    
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

def check_logs():
    """检查日志"""
    print("\n📋 检查日志...")
    
    # 检查LLRC服务日志
    run_command("sudo journalctl -u llrc --no-pager -n 20", "检查LLRC服务日志")
    
    # 检查Nginx日志
    run_command("sudo tail -n 20 /var/log/nginx/error.log", "检查Nginx错误日志")
    
    # 检查应用日志
    if os.path.exists("/var/www/llrc/app.log"):
        run_command("tail -n 20 /var/www/llrc/app.log", "检查应用日志")

def main():
    """主函数"""
    print("🚀 LLRC云服务器更新到pxy分支工具")
    print("=" * 50)
    print(f"更新时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 检查是否为root用户
    if os.geteuid() == 0:
        print("❌ 请不要使用root用户运行此脚本")
        sys.exit(1)
    
    # 检查项目目录是否存在
    if not os.path.exists("/var/www/llrc"):
        print("❌ 项目目录不存在: /var/www/llrc")
        print("请先按照部署指南创建项目目录")
        sys.exit(1)
    
    # 执行更新步骤
    backup_dir = backup_current_version()
    update_to_pxy_branch()
    fix_dependencies()
    fix_database_issues()
    fix_file_permissions()
    fix_environment_config()
    restart_services()
    test_application()
    check_logs()
    
    print("\n🎉 更新完成！")
    print("\n📋 更新摘要:")
    if backup_dir:
        print(f"   💾 备份位置: {backup_dir}")
    print("   🔄 已更新到pxy分支")
    print("   📦 依赖已重新安装")
    print("   🗄️ 数据库已重新初始化")
    print("   🔐 权限已修复")
    print("   ⚙️ 环境配置已更新")
    print("   🔄 服务已重启")
    
    print("\n🌐 测试链接:")
    print("   - 主页: http://60.205.251.52/")
    print("   - 注册页面: http://60.205.251.52/auth/sign")
    print("   - 测试页面: http://60.205.251.52/test")
    
    print("\n📋 如果仍有问题:")
    print("1. 运行诊断脚本: python3 diagnose_auth_issues.py")
    print("2. 查看详细日志: sudo journalctl -u llrc -f")
    print("3. 检查Nginx配置: sudo nginx -t")
    print("4. 恢复备份: sudo cp -r {backup_dir} /var/www/llrc")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ 用户中断操作")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 更新脚本执行失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
