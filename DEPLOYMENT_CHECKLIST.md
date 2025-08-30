# 📋 LLRC 云服务器部署检查清单

## 🎯 部署前检查

### ✅ 本地环境确认
- [ ] 表情识别功能正常（使用DeepFace）
- [ ] 所有代码已提交到GitHub
- [ ] requirements.txt包含DeepFace依赖
- [ ] 部署脚本已创建

### ✅ 服务器环境准备
- [ ] 服务器操作系统：Ubuntu 18.04+ 或 CentOS 7+
- [ ] 内存：至少 2GB RAM
- [ ] 存储：至少 20GB 可用空间
- [ ] 网络：公网IP地址可访问

## 🚀 部署步骤

### 第一步：服务器基础环境
```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装基础软件
sudo apt install -y python3 python3-pip python3-venv git nginx supervisor curl

# 安装MongoDB
sudo apt install -y mongodb
sudo systemctl start mongodb
sudo systemctl enable mongodb

# 创建项目目录
sudo mkdir -p /var/www/llrc
sudo chown $USER:$USER /var/www/llrc
```

### 第二步：克隆项目代码
```bash
cd /var/www/llrc
git clone https://github.com/Rayscout/LLRC.git .
git checkout pxy
```

### 第三步：创建虚拟环境
```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 第四步：运行部署脚本
```bash
chmod +x deploy.sh
chmod +x cloud_deploy.sh
./deploy.sh
```

## 🔍 部署后验证

### 环境检查
```bash
# 运行环境检查脚本
python3 cloud_check.py

# 预期输出：
# ✅ DeepFace导入成功
# ✅ 表情识别模块正常
# 🎉 环境检查通过！
```

### 服务状态检查
```bash
# 检查LLRC服务
sudo systemctl status llrc

# 检查Nginx服务
sudo systemctl status nginx

# 检查MongoDB服务
sudo systemctl status mongodb
```

### 端口检查
```bash
# 检查端口监听
sudo netstat -tlnp | grep :80    # HTTP
sudo netstat -tlnp | grep :5000  # Flask应用
sudo netstat -tlnp | grep :27017 # MongoDB
```

### 功能测试
```bash
# 1. 基础访问测试
curl http://localhost/health

# 2. 表情识别测试
curl http://localhost/smartrecruit/candidate/ai-analysis/health-check

# 3. 数据库连接测试
python3 -c "
import pymongo
client = pymongo.MongoClient('mongodb://localhost:27017/')
client.server_info()
print('MongoDB连接正常')
"
```

## 🚨 常见问题解决

### 问题1：DeepFace安装失败
```bash
# 解决方案
sudo apt install -y libgl1-mesa-glx libglib2.0-0
pip uninstall deepface
pip install deepface==0.0.79
```

### 问题2：表情识别模块导入失败
```bash
# 解决方案
python3 -c "import sys; print(sys.path)"
ls -la smartrecruit_system/candidate_module/
pip install -r requirements.txt
```

### 问题3：MongoDB连接失败
```bash
# 解决方案
sudo systemctl start mongodb
sudo systemctl enable mongodb
sudo netstat -tlnp | grep :27017
```

### 问题4：服务启动失败
```bash
# 解决方案
sudo journalctl -u llrc -n 50
sudo nginx -t
sudo netstat -tlnp | grep :5000
```

### 问题5：内存不足
```bash
# 解决方案
free -h
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

## 📊 性能优化

### 系统优化
```bash
# 优化系统参数
echo 'vm.swappiness=10' | sudo tee -a /etc/sysctl.conf
echo 'vm.vfs_cache_pressure=50' | sudo tee -a /etc/sysctl.conf
sudo sysctl -p
```

### Nginx优化
```bash
# 编辑Nginx配置
sudo nano /etc/nginx/nginx.conf

# 添加优化配置
worker_processes auto;
worker_connections 1024;
keepalive_timeout 65;
gzip on;
gzip_types text/plain text/css application/json application/javascript;
```

### Gunicorn优化
```bash
# 编辑Gunicorn配置
sudo nano /var/www/llrc/gunicorn.conf.py

# 优化配置
workers = 4
worker_class = 'gevent'
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 100
```

## 🔒 安全配置

### 防火墙配置
```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable
```

### SSH安全
```bash
sudo nano /etc/ssh/sshd_config
# 设置：PermitRootLogin no, PasswordAuthentication no
sudo systemctl restart ssh
```

## 📝 维护命令

### 服务管理
```bash
# 启动服务
sudo systemctl start llrc

# 停止服务
sudo systemctl stop llrc

# 重启服务
sudo systemctl restart llrc

# 查看状态
sudo systemctl status llrc

# 启用自启
sudo systemctl enable llrc
```

### 日志查看
```bash
# 应用日志
sudo journalctl -u llrc -f

# Nginx日志
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log

# 应用日志文件
tail -f /var/www/llrc/app.log
```

### 代码更新
```bash
cd /var/www/llrc

# 自动更新
./cloud_deploy.sh

# 手动更新
git fetch origin
git reset --hard origin/pxy
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart llrc
```

## 🎉 部署完成检查

### 最终验证
- [ ] 环境检查脚本通过
- [ ] 所有服务正常运行
- [ ] 端口监听正常
- [ ] 功能测试通过
- [ ] 外部访问正常
- [ ] 表情识别功能正常

### 访问信息
- 本地访问: `http://localhost`
- 外部访问: `http://你的服务器IP`
- 健康检查: `http://你的服务器IP/health`
- 表情识别测试: `http://你的服务器IP/smartrecruit/candidate/applications/emotion_demo`

## 📞 技术支持

### 获取帮助
1. 查看日志：`sudo journalctl -u llrc -f`
2. 检查状态：`sudo systemctl status llrc`
3. 运行诊断：`python3 cloud_check.py`
4. 查看错误：`tail -f /var/www/llrc/app.log`

### 联系信息
- 项目仓库：https://github.com/Rayscout/LLRC
- 问题反馈：通过GitHub Issues

---

**🎉 恭喜！部署完成！**

现在你的LLRC应用已经成功部署到云服务器，支持：
- ✅ DeepFace表情识别
- ✅ GitHub自动同步
- ✅ 其他同学访问
- ✅ 生产环境稳定运行
