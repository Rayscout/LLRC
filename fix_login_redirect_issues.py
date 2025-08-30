#!/usr/bin/env python3
"""
修复登录后跳转页面问题的脚本
解决数据库连接、权限和路由问题
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(cmd, description="", capture_output=False):
    """执行命令"""
    print(f"🔄 {description}...")
    try:
        if capture_output:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            return result.stdout.strip()
        else:
            subprocess.run(cmd, shell=True, check=True)
            print(f"   ✅ {description}完成")
            return True
    except subprocess.CalledProcessError as e:
        print(f"   ❌ {description}失败: {e}")
        return False

def fix_database_issues():
    """修复数据库问题"""
    print("\n🔧 修复数据库问题...")
    
    # 检查数据库文件
    db_path = "/var/www/llrc/instance/site.db"
    if os.path.exists(db_path):
        print(f"   📁 数据库文件存在: {db_path}")
        # 修复权限
        run_command(f"sudo chown llrcuser:llrcuser {db_path}", "修复数据库文件权限")
        run_command(f"sudo chmod 644 {db_path}", "设置数据库文件权限")
    else:
        print("   ⚠️ 数据库文件不存在，将创建新数据库")
    
    # 确保instance目录存在
    instance_dir = "/var/www/llrc/instance"
    if not os.path.exists(instance_dir):
        run_command(f"mkdir -p {instance_dir}", "创建instance目录")
        run_command(f"sudo chown llrcuser:llrcuser {instance_dir}", "设置instance目录权限")
    
    # 初始化数据库
    print("   🔄 初始化数据库...")
    os.chdir("/var/www/llrc")
    
    # 激活虚拟环境
    activate_cmd = "source venv/bin/activate"
    
    # 运行数据库初始化
    init_cmd = f"{activate_cmd} && python3 -c \"from app import create_app; from app.models import db; app = create_app(); app.app_context().push(); db.create_all(); print('数据库初始化完成')\""
    run_command(init_cmd, "初始化数据库表")

def fix_file_permissions():
    """修复文件权限"""
    print("\n🔧 修复文件权限...")
    
    # 修复项目目录权限
    run_command("sudo chown -R llrcuser:llrcuser /var/www/llrc", "修复项目目录权限")
    run_command("sudo chmod -R 755 /var/www/llrc", "设置项目目录权限")
    
    # 修复特定目录权限
    run_command("sudo chmod -R 777 /var/www/llrc/flask_session_data", "设置session目录权限")
    run_command("sudo chmod -R 777 /var/www/llrc/instance", "设置instance目录权限")

def fix_environment():
    """修复环境配置"""
    print("\n🔧 修复环境配置...")
    
    env_file = "/var/www/llrc/.env"
    env_content = """GOOGLE_API_KEY=AIzaSyDdOylv0bq8q1UypVG-r4m2yHxHNf_CsMo
GEMINI_MODEL=gemini-1.5-flash
DEEPSEEK_API_KEY=
DEEPSEEK_MODEL=deepseek-chat

# 生产环境配置
FLASK_ENV=production
SECRET_KEY=llrc-secret-key-production-2025
MONGODB_URI=mongodb://localhost:27017/llrc
DATABASE_URL=sqlite:///instance/site.db
"""
    
    with open(env_file, 'w') as f:
        f.write(env_content)
    
    run_command(f"sudo chown llrcuser:llrcuser {env_file}", "设置.env文件权限")
    run_command(f"sudo chmod 644 {env_file}", "设置.env文件权限")
    print("   ✅ 环境配置已更新")

def create_test_users():
    """创建测试用户"""
    print("\n👥 创建测试用户...")
    
    os.chdir("/var/www/llrc")
    activate_cmd = "source venv/bin/activate"
    
    # 创建测试用户的Python脚本
    test_users_script = '''
from app import create_app
from app.models import User, db
from datetime import datetime

app = create_app()
with app.app_context():
    # 检查是否已有用户
    existing_users = User.query.all()
    if existing_users:
        print(f"已有 {len(existing_users)} 个用户")
        for user in existing_users[:3]:
            print(f"  - {user.email}: {user.user_type}")
        return
    
    # 创建测试用户
    users_data = [
        {
            'first_name': '测试',
            'last_name': '求职者',
            'company_name': '测试公司',
            'email': 'candidate@test.com',
            'phone_number': '13800138001',
            'birthday': '1990-01-01',
            'password': '123456',
            'user_type': 'candidate',
            'is_hr': False
        },
        {
            'first_name': '测试',
            'last_name': 'HR',
            'company_name': '测试公司',
            'email': 'hr@test.com',
            'phone_number': '13800138002',
            'birthday': '1985-01-01',
            'password': '123456',
            'user_type': 'recruiter',
            'is_hr': True
        },
        {
            'first_name': '测试',
            'last_name': '高管',
            'company_name': '测试公司',
            'email': 'executive@test.com',
            'phone_number': '13800138003',
            'birthday': '1980-01-01',
            'password': '123456',
            'user_type': 'executive',
            'is_hr': False
        },
        {
            'first_name': '测试',
            'last_name': '员工',
            'company_name': '测试公司',
            'email': 'employee@test.com',
            'phone_number': '13800138004',
            'birthday': '1992-01-01',
            'password': '123456',
            'user_type': 'employee',
            'is_hr': False,
            'employee_id': 'EMP001',
            'supervisor_id': None,
            'hire_date': datetime.now().date()
        }
    ]
    
    for user_data in users_data:
        user = User(**user_data)
        db.session.add(user)
    
    db.session.commit()
    print("测试用户创建完成")
'''
    
    # 写入临时脚本文件
    with open('create_test_users.py', 'w') as f:
        f.write(test_users_script)
    
    # 执行脚本
    run_command(f"{activate_cmd} && python3 create_test_users.py", "创建测试用户")
    
    # 清理临时文件
    os.remove('create_test_users.py')

def restart_services():
    """重启服务"""
    print("\n🔄 重启服务...")
    
    run_command("sudo systemctl restart llrc", "重启LLRC服务")
    run_command("sudo systemctl restart nginx", "重启Nginx服务")
    run_command("sudo systemctl restart mongod", "重启MongoDB服务")

def test_routes():
    """测试路由"""
    print("\n🧪 测试路由...")
    
    # 等待服务启动
    import time
    time.sleep(3)
    
    # 测试主页
    result = run_command("curl -s -o /dev/null -w '%{http_code}' http://localhost/", "测试主页", True)
    print(f"   主页状态码: {result}")
    
    # 测试登录页面
    result = run_command("curl -s -o /dev/null -w '%{http_code}' http://localhost/auth/sign", "测试登录页面", True)
    print(f"   登录页面状态码: {result}")

def main():
    """主函数"""
    print("🚀 LLRC登录跳转问题修复工具")
    print("=" * 50)
    
    # 检查是否在正确的目录
    if not os.path.exists("/var/www/llrc"):
        print("❌ 请在云服务器上运行此脚本")
        return
    
    # 执行修复步骤
    fix_database_issues()
    fix_file_permissions()
    fix_environment()
    create_test_users()
    restart_services()
    test_routes()
    
    print("\n🎉 修复完成！")
    print("\n📋 测试账号信息：")
    print("   求职者: candidate@test.com / 123456")
    print("   HR: hr@test.com / 123456")
    print("   高管: executive@test.com / 123456")
    print("   员工: employee@test.com / 123456")
    print("\n🌐 访问地址: http://60.205.251.52/auth/sign")
    print("\n⚠️ 如果仍有问题，请检查日志:")
    print("   sudo journalctl -u llrc -f")

if __name__ == "__main__":
    main()
