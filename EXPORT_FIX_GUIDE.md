# 云服务器导出功能修复指南

## 问题描述

云服务器上的导出功能出现502错误，主要问题包括：

1. **人才流失预警** - 生成预警报告模块不会报错但无法生成报告，只会出现乱码
2. **薪酬分析模块** - 导出数据显示正在导出但一直没有最终结果
3. **组织健康度模块** - 导出对比报告和刷新数据都显示正在……
4. **职业发展追踪模块** - 导出发展报告、刷新数据、切换视图无响应
5. **团队管理模块** - 发送管理不支持折叠员工，反馈历史记录无法显示
6. **员工管理模块** - 系统功能导航所有交互均是返回当前页面顶部
7. **AI人才大盘** - 跳转出现报错"内部服务器错误，请检查日志"
8. **生成AI公司报告模块** - 显示"生成失败，请稍后再试"

## 根本原因分析

### 1. 超时设置过短
- nginx `proxy_read_timeout`: 30秒 → 需要增加到300秒
- gunicorn `timeout`: 30秒 → 需要增加到300秒

### 2. 依赖包问题
- 云服务器可能缺少 `openpyxl`, `pandas`, `reportlab` 等包
- 或者版本不匹配

### 3. 服务器配置问题
- 单进程worker无法处理大型文件生成
- 内存和缓冲区设置不当

### 4. 错误处理不完善
- 缺少详细的错误日志
- 前端没有正确的错误提示

## 修复方案

### 方案一：一键修复（推荐）

```bash
# 1. 上传修复脚本到云服务器
scp one_click_export_fix.sh user@your-server:/var/www/llrc/

# 2. 在云服务器上运行
cd /var/www/llrc
sudo chmod +x one_click_export_fix.sh
sudo ./one_click_export_fix.sh
```

### 方案二：手动修复

#### 1. 安装依赖包

```bash
cd /var/www/llrc
source venv/bin/activate

# 安装Excel处理库
pip install pandas==2.1.4 openpyxl==3.1.2 xlrd==2.0.1 xlwt==1.3.0

# 安装PDF生成库
pip install reportlab==4.1.0

# 安装数据处理库
pip install numpy==1.26.4 matplotlib==3.8.3

# 安装异步处理库
pip install gevent==23.9.1
```

#### 2. 更新nginx配置

```bash
# 备份原配置
sudo cp /etc/nginx/sites-available/llrc /etc/nginx/sites-available/llrc.backup

# 使用优化配置
sudo cp nginx_export_optimized.conf /etc/nginx/sites-available/llrc

# 测试配置
sudo nginx -t

# 重启nginx
sudo systemctl restart nginx
```

#### 3. 更新gunicorn配置

```bash
# 备份原配置
cp gunicorn.conf.py gunicorn.conf.py.backup

# 使用优化配置
cp gunicorn_export_optimized.conf.py gunicorn.conf.py

# 重启服务
sudo systemctl restart llrc
```

#### 4. 验证修复

```bash
# 运行功能测试
python3 test_export_functionality.py

# 运行Web测试
python3 test_web_export.py
```

## 配置优化详情

### nginx配置优化

```nginx
# 导出功能专用配置
location ~* /api/export|/api/generate_report|/api/export_data|/api/export_report {
    proxy_pass http://127.0.0.1:5000;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    
    # 增加超时时间到5分钟
    proxy_connect_timeout 60s;
    proxy_send_timeout 300s;
    proxy_read_timeout 300s;
    
    # 优化缓冲区设置
    proxy_buffering on;
    proxy_buffer_size 16k;
    proxy_buffers 32 16k;
    proxy_busy_buffers_size 32k;
    proxy_temp_file_write_size 32k;
    
    # 禁用代理缓存
    proxy_cache off;
    proxy_no_cache 1;
    proxy_cache_bypass 1;
}
```

### gunicorn配置优化

```python
# 服务器配置
bind = "127.0.0.1:5000"
workers = 2  # 增加到2个进程
worker_class = "gevent"  # 使用异步worker
worker_connections = 1000
timeout = 300  # 增加到5分钟
keepalive = 2
max_requests = 1000
max_requests_jitter = 100
preload_app = True

# 内存优化
worker_tmp_dir = "/dev/shm"  # 使用内存文件系统
```

## 测试验证

### 1. 本地功能测试

```bash
python3 test_export_functionality.py
```

预期输出：
```
🧪 测试Excel导出功能...
✅ Excel文件生成成功
   文件大小: 12345 bytes
   生成时间: 0.15秒

🧪 测试PDF导出功能...
✅ PDF文件生成成功
   文件大小: 6789 bytes
   生成时间: 0.08秒

✅ 所有导出功能测试通过！
```

### 2. Web端点测试

```bash
python3 test_web_export.py
```

预期输出：
```
🧪 测试Web导出端点...

测试 薪酬分析导出 (/talent/hr_admin/salary_analysis/api/export_data)...
  状态码: 401
  响应时间: 0.05秒
  响应大小: 45 bytes
  ⚠️  需要登录

测试 人才流失预警导出 (/talent/hr_admin/turnover_alert/api/export_data)...
  状态码: 401
  响应时间: 0.04秒
  响应大小: 45 bytes
  ⚠️  需要登录
```

## 故障排除

### 1. 如果仍然出现502错误

```bash
# 检查nginx错误日志
sudo tail -f /var/log/nginx/error.log

# 检查gunicorn错误日志
sudo journalctl -u llrc -f

# 检查服务状态
sudo systemctl status nginx
sudo systemctl status llrc
```

### 2. 如果依赖包安装失败

```bash
# 更新pip
python3 -m pip install --upgrade pip

# 清理缓存
pip cache purge

# 重新安装
pip install --no-cache-dir pandas openpyxl reportlab
```

### 3. 如果内存不足

```bash
# 检查内存使用
free -h

# 检查磁盘空间
df -h

# 清理临时文件
sudo rm -rf /tmp/*
```

## 监控和维护

### 1. 设置监控

```bash
# 创建监控脚本
cat > monitor_export.sh << 'EOF'
#!/bin/bash
while true; do
    echo "$(date): 检查导出功能..."
    curl -s -o /dev/null -w "%{http_code}" http://localhost:5000/health
    echo ""
    sleep 60
done
EOF

chmod +x monitor_export.sh
nohup ./monitor_export.sh > monitor.log 2>&1 &
```

### 2. 定期维护

```bash
# 每周清理日志
sudo find /var/log -name "*.log" -mtime +7 -delete

# 每月重启服务
sudo systemctl restart llrc
```

## 性能优化建议

### 1. 服务器配置

- **CPU**: 至少2核心
- **内存**: 至少4GB
- **磁盘**: 至少20GB可用空间
- **网络**: 稳定的网络连接

### 2. 应用优化

- 使用SSD存储
- 启用gzip压缩
- 配置CDN加速
- 使用Redis缓存

### 3. 数据库优化

- 定期清理无用数据
- 优化查询语句
- 添加适当索引
- 配置连接池

## 联系支持

如果修复过程中遇到问题，请：

1. 收集错误日志
2. 记录复现步骤
3. 提供系统信息
4. 联系技术支持

---

**注意**: 在生产环境中进行任何配置更改前，请务必备份重要数据和配置文件。
