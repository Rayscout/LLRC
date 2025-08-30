# 🚀 LLRC 完整远程修复操作指南

## 🎯 **目标**
修复云服务器上的认证问题，将修复代码从`pxy`分支合并到`RayScout`主分支，并完成最终部署。

## 📋 **操作步骤总览**

### **第一阶段：问题诊断和修复**
1. 连接到远程服务器
2. 运行诊断脚本
3. 执行修复操作
4. 验证修复结果

### **第二阶段：代码管理和部署**
5. 提交修复代码到pxy分支
6. 合并pxy分支到RayScout分支
7. 最终验证和测试

---

## 🔧 **第一阶段：问题诊断和修复**

### **步骤1：连接到远程服务器**
```bash
ssh llrcuser@60.205.251.52
# 输入密码: pxy221850
```

### **步骤2：检查当前状态**
```bash
# 检查当前目录
pwd
ls -la

# 进入项目目录
cd /var/www/llrc
ls -la

# 检查Git状态
git status
git branch -a
```

### **步骤3：创建诊断脚本**
```bash
# 创建诊断脚本
cat > diagnose_auth_issues.py << 'EOF'
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
EOF

# 设置执行权限
chmod +x diagnose_auth_issues.py
```

### **步骤4：运行诊断脚本**
```bash
# 运行诊断脚本
python3 diagnose_auth_issues.py
```

### **步骤5：创建修复脚本**
```bash
# 创建修复脚本
cat > fix_auth_issues.py << 'EOF'
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
EOF

# 设置执行权限
chmod +x fix_auth_issues.py
```

### **步骤6：运行修复脚本**
```bash
# 运行修复脚本
python3 fix_auth_issues.py
```

### **步骤7：验证修复结果**
```bash
# 再次运行诊断脚本验证
python3 diagnose_auth_issues.py

# 手动测试Web功能
curl -s http://localhost/health
curl -s -o /dev/null -w '%{http_code}' http://localhost/auth/sign
```

---

## 🌿 **第二阶段：代码管理和部署**

### **步骤8：检查Git状态**
```bash
# 检查当前分支和状态
git status
git branch -a
git log --oneline -5
```

### **步骤9：切换到pxy分支并提交修复**
```bash
# 切换到pxy分支
git checkout pxy

# 拉取最新代码
git pull origin pxy

# 添加修复脚本
git add diagnose_auth_issues.py fix_auth_issues.py

# 提交修复
git commit -m "修复认证问题：添加诊断和修复脚本"

# 推送到pxy分支
git push origin pxy
```

### **步骤10：合并到RayScout主分支**
```bash
# 切换到RayScout分支
git checkout RayScout

# 拉取最新代码
git pull origin RayScout

# 合并pxy分支
git merge pxy

# 推送到RayScout分支
git push origin RayScout

# 切换回pxy分支继续开发
git checkout pxy
```

### **步骤11：最终验证**
```bash
# 验证服务状态
sudo systemctl is-active llrc
sudo systemctl is-active mongod
sudo systemctl is-active nginx

# 验证端口监听
sudo netstat -tlnp | grep -E ':(80|5000|27017)'

# 验证Web功能
curl -s http://localhost/health
curl -s -o /dev/null -w '%{http_code}' http://localhost/auth/sign

# 验证数据库连接
python3 -c "import pymongo; client = pymongo.MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=5000); client.server_info(); print('✅ MongoDB连接正常')"

# 验证表情识别功能
python3 -c "from smartrecruit_system.candidate_module.emotion_recognition import get_emotion_recognition_ai; ai = get_emotion_recognition_ai(); print('✅ 表情识别模块正常')"
```

---

## 🎉 **完成后的验证**

### **访问测试地址**
- **主页**: http://60.205.251.52
- **注册页面**: http://60.205.251.52/auth/sign
- **健康检查**: http://60.205.251.52/health

### **预期结果**
- ✅ 注册页面正常显示（HTTP 200）
- ✅ 可以成功创建新用户账号
- ✅ 登录功能正常工作
- ✅ 表情识别功能正常

---

## 🚨 **如果遇到问题**

### **查看日志**
```bash
# 查看应用日志
sudo journalctl -u llrc -f

# 查看应用日志文件
tail -f /var/www/llrc/app.log

# 查看Nginx错误日志
sudo tail -f /var/log/nginx/error.log
```

### **常见问题解决**
1. **权限问题**: `sudo chown -R llrcuser:llrcuser /var/www/llrc`
2. **依赖问题**: `source venv/bin/activate && pip install -r requirements.txt`
3. **服务问题**: `sudo systemctl restart llrc mongod nginx`

---

## 📞 **获取帮助**

如果在任何步骤遇到问题，请：
1. 复制错误信息
2. 告诉我执行到哪一步
3. 我会继续帮你解决

---

**🎯 现在开始执行！请按照上述步骤一步步操作，如果遇到任何问题，请告诉我！**
