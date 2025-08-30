#!/usr/bin/env python3
"""
快速修复登录问题脚本
专门解决云服务器上的登录"内部服务器错误"问题
"""

import os
import sys
import subprocess
import time

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
            return True
        else:
            print(f"   ❌ 失败")
            if result.stderr.strip():
                print(f"   错误: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"   ❌ 异常: {e}")
        return False

def check_current_status():
    """检查当前状态"""
    print("🔍 检查当前状态...")
    
    # 检查服务状态
    run_command("sudo systemctl status llrc --no-pager", "检查LLRC服务状态")
    run_command("sudo systemctl status nginx --no-pager", "检查Nginx服务状态")
    run_command("sudo systemctl status mongod --no-pager", "检查MongoDB服务状态")
    
    # 检查端口监听
    run_command("sudo netstat -tlnp | grep :80", "检查HTTP端口")
    run_command("sudo netstat -tlnp | grep :27017", "检查MongoDB端口")

def fix_critical_issues():
    """修复关键问题"""
    print("\n🔧 修复关键问题...")
    
    # 1. 重启MongoDB
    print("   🗄️ 重启MongoDB...")
    run_command("sudo systemctl restart mongod", "重启MongoDB")
    time.sleep(3)
    
    # 2. 检查并创建必要的目录
    print("   📁 检查必要目录...")
    critical_dirs = [
        "/var/www/llrc/instance",
        "/var/www/llrc/flask_session_data"
    ]
    
    for dir_path in critical_dirs:
        if not os.path.exists(dir_path):
            run_command(f"sudo mkdir -p {dir_path}", f"创建目录: {dir_path}")
        run_command(f"sudo chmod 755 {dir_path}", f"设置权限: {dir_path}")
        run_command(f"sudo chown llrcuser:llrcuser {dir_path}", f"设置所有者: {dir_path}")
    
    # 3. 修复.env文件
    print("   ⚙️ 修复环境配置...")
    env_file = "/var/www/llrc/.env"
    if not os.path.exists(env_file):
        env_content = """# LLRC环境配置
SECRET_KEY=llrc-secret-key-2024-production
FLASK_ENV=production
MONGODB_URI=mongodb://localhost:27017/llrc
DATABASE_URL=sqlite:///instance/site.db
"""
        with open(env_file, 'w') as f:
            f.write(env_content)
        run_command(f"sudo chown llrcuser:llrcuser {env_file}", "设置.env文件权限")
        print("   ✅ 已创建.env文件")
    
    # 4. 初始化数据库
    print("   🗄️ 初始化数据库...")
    run_command("cd /var/www/llrc && python3 init_db.py", "初始化数据库")

def restart_services():
    """重启服务"""
    print("\n🔄 重启服务...")
    
    # 重启LLRC服务
    run_command("sudo systemctl restart llrc", "重启LLRC服务")
    time.sleep(5)
    
    # 重启Nginx服务
    run_command("sudo systemctl restart nginx", "重启Nginx服务")
    time.sleep(3)
    
    # 检查服务状态
    run_command("sudo systemctl status llrc --no-pager", "检查LLRC服务状态")
    run_command("sudo systemctl status nginx --no-pager", "检查Nginx服务状态")

def test_login_page():
    """测试登录页面"""
    print("\n🧪 测试登录页面...")
    
    # 等待服务完全启动
    print("   ⏳ 等待服务启动...")
    time.sleep(10)
    
    # 测试注册页面
    result = run_command("curl -s -o /dev/null -w '%{http_code}' http://localhost/auth/sign", "测试注册页面")
    if result:
        print("   ✅ 注册页面可访问")
    else:
        print("   ❌ 注册页面无法访问")
    
    # 测试主页
    result = run_command("curl -s -o /dev/null -w '%{http_code}' http://localhost/", "测试主页")
    if result:
        print("   ✅ 主页可访问")
    else:
        print("   ❌ 主页无法访问")

def check_error_logs():
    """检查错误日志"""
    print("\n📋 检查错误日志...")
    
    # 检查LLRC服务日志
    run_command("sudo journalctl -u llrc --no-pager -n 10", "检查LLRC服务日志")
    
    # 检查Nginx错误日志
    run_command("sudo tail -n 10 /var/log/nginx/error.log", "检查Nginx错误日志")
    
    # 检查应用日志
    if os.path.exists("/var/www/llrc/app.log"):
        run_command("tail -n 10 /var/www/llrc/app.log", "检查应用日志")

def main():
    """主函数"""
    print("🚀 LLRC登录问题快速修复工具")
    print("=" * 50)
    print(f"修复时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 检查是否为root用户
    if os.geteuid() == 0:
        print("❌ 请不要使用root用户运行此脚本")
        sys.exit(1)
    
    # 检查项目目录是否存在
    if not os.path.exists("/var/www/llrc"):
        print("❌ 项目目录不存在: /var/www/llrc")
        sys.exit(1)
    
    # 执行修复步骤
    check_current_status()
    fix_critical_issues()
    restart_services()
    test_login_page()
    check_error_logs()
    
    print("\n🎉 快速修复完成！")
    print("\n🌐 请测试以下链接:")
    print("   - 主页: http://60.205.251.52/")
    print("   - 注册页面: http://60.205.251.52/auth/sign")
    
    print("\n📋 如果仍有问题:")
    print("1. 运行完整诊断: python3 diagnose_auth_issues.py")
    print("2. 查看实时日志: sudo journalctl -u llrc -f")
    print("3. 运行完整更新: python3 cloud_server_update.py")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ 用户中断操作")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 修复脚本执行失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
