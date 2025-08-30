# 🔐 LLRC 认证问题修复指南

## 🚨 问题描述

在云服务器上注册账号时出现"内部服务器错误"，访问 [http://60.205.251.52/auth/sign](http://60.205.251.52/auth/sign) 页面时遇到问题。

## 🔍 问题诊断

### 1. 运行诊断脚本

首先运行诊断脚本来识别具体问题：

```bash
cd /var/www/llrc
python3 diagnose_auth_issues.py
```

### 2. 检查服务状态

```bash
# 检查LLRC服务状态
sudo systemctl status llrc

# 检查MongoDB服务状态
sudo systemctl status mongod

# 检查Nginx服务状态
sudo systemctl status nginx
```

### 3. 查看错误日志

```bash
# 查看应用日志
sudo journalctl -u llrc -f

# 查看应用日志文件
tail -f /var/www/llrc/app.log

# 查看Nginx错误日志
sudo tail -f /var/log/nginx/error.log
```

## 🛠️ 快速修复方案

### 方案1：运行自动修复脚本

```bash
cd /var/www/llrc
python3 fix_auth_issues.py
```

### 方案2：手动修复步骤

#### 步骤1：修复文件权限

```bash
# 修复项目目录权限
sudo chown -R llrcuser:llrcuser /var/www/llrc

# 修复关键目录权限
sudo chmod -R 755 /var/www/llrc/instance
sudo chmod -R 755 /var/www/llrc/flask_session_data
sudo chmod -R 755 /var/www/llrc/venv
```

#### 步骤2：修复数据库问题

```bash
# 重启MongoDB服务
sudo systemctl restart mongod

# 检查MongoDB状态
sudo systemctl status mongod

# 检查端口监听
sudo netstat -tlnp | grep :27017
```

#### 步骤3：修复依赖问题

```bash
# 激活虚拟环境
cd /var/www/llrc
source venv/bin/activate

# 安装认证相关依赖
pip install bcrypt flask-login flask-session werkzeug

# 重新安装项目依赖
pip install -r requirements.txt
```

#### 步骤4：修复环境配置

```bash
# 检查.env文件
cat /var/www/llrc/.env

# 如果.env文件不存在或配置不完整，创建默认配置
cat > /var/www/llrc/.env << EOF
# LLRC环境配置
SECRET_KEY=your-secret-key-here-$(openssl rand -hex 16)
FLASK_ENV=production
MONGODB_URI=mongodb://localhost:27017/llrc
DATABASE_URL=sqlite:///instance/site.db
EOF
```

#### 步骤5：重启服务

```bash
# 重启LLRC服务
sudo systemctl restart llrc

# 重启Nginx服务
sudo systemctl restart nginx

# 检查服务状态
sudo systemctl status llrc
sudo systemctl status nginx
```

## 🔧 常见问题及解决方案

### 问题1：MongoDB连接失败

**症状**：日志显示"MongoDB连接失败"或"Connection refused"

**解决方案**：
```bash
# 启动MongoDB服务
sudo systemctl start mongod
sudo systemctl enable mongod

# 检查MongoDB状态
sudo systemctl status mongod

# 检查端口监听
sudo netstat -tlnp | grep :27017
```

### 问题2：权限不足

**症状**：日志显示"Permission denied"或"Access denied"

**解决方案**：
```bash
# 修复文件权限
sudo chown -R llrcuser:llrcuser /var/www/llrc
sudo chmod -R 755 /var/www/llrc

# 修复虚拟环境权限
sudo chown -R llrcuser:llrcuser /var/www/llrc/venv
```

### 问题3：依赖包缺失

**症状**：日志显示"ModuleNotFoundError"或"ImportError"

**解决方案**：
```bash
# 激活虚拟环境
cd /var/www/llrc
source venv/bin/activate

# 安装缺失的依赖
pip install -r requirements.txt

# 安装认证相关依赖
pip install bcrypt flask-login flask-session werkzeug
```

### 问题4：环境变量缺失

**症状**：日志显示"SECRET_KEY not set"或配置相关错误

**解决方案**：
```bash
# 创建或更新.env文件
cat > /var/www/llrc/.env << EOF
SECRET_KEY=your-secret-key-here-$(openssl rand -hex 16)
FLASK_ENV=production
MONGODB_URI=mongodb://localhost:27017/llrc
DATABASE_URL=sqlite:///instance/site.db
EOF

# 设置文件权限
chmod 600 /var/www/llrc/.env
chown llrcuser:llrcuser /var/www/llrc/.env
```

## 🧪 测试修复结果

### 1. 测试健康检查

```bash
curl http://localhost/health
```

**预期输出**：`healthy`

### 2. 测试注册页面

```bash
curl -s -o /dev/null -w '%{http_code}' http://localhost/auth/sign
```

**预期输出**：`200`

### 3. 测试数据库连接

```bash
python3 -c "
import pymongo
try:
    client = pymongo.MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=5000)
    client.server_info()
    print('✅ MongoDB连接正常')
    db = client.llrc
    collections = db.list_collection_names()
    print(f'📁 集合: {collections}')
except Exception as e:
    print(f'❌ MongoDB连接失败: {e}')
"
```

## 📞 获取帮助

### 如果问题仍然存在

1. **运行完整诊断**：
   ```bash
   python3 diagnose_auth_issues.py
   ```

2. **查看详细日志**：
   ```bash
   sudo journalctl -u llrc -f
   ```

3. **检查系统资源**：
   ```bash
   # 检查内存使用
   free -h
   
   # 检查磁盘空间
   df -h
   
   # 检查进程状态
   ps aux | grep python
   ```

### 联系技术支持

- 项目仓库：https://github.com/Rayscout/LLRC
- 问题反馈：通过GitHub Issues

## 🎯 预防措施

### 1. 定期检查服务状态

```bash
# 创建监控脚本
sudo nano /usr/local/bin/monitor-llrc.sh

#!/bin/bash
echo "检查时间: $(date)"
echo "LLRC服务状态:"
sudo systemctl status llrc --no-pager
echo "MongoDB服务状态:"
sudo systemctl status mongod --no-pager
echo "Nginx服务状态:"
sudo systemctl status nginx --no-pager
```

### 2. 设置自动重启

```bash
# 编辑服务配置
sudo nano /etc/systemd/system/llrc.service

# 添加自动重启配置
[Service]
Restart=always
RestartSec=10
```

### 3. 日志轮转

```bash
# 配置日志轮转
sudo nano /etc/logrotate.d/llrc

/var/www/llrc/app.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
    create 644 llrcuser llrcuser
}
```

---

**🎉 修复完成后，你的注册功能应该可以正常工作了！**

如果还有问题，请运行诊断脚本并提供错误日志，我会继续帮你解决。
