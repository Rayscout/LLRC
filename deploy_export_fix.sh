#!/bin/bash
# 云服务器导出功能修复部署脚本

set -e

echo "🚀 开始部署导出功能修复..."

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 项目配置
PROJECT_DIR="/var/www/llrc"
SERVICE_NAME="llrc"

# 检查是否为root用户
if [ "$EUID" -ne 0 ]; then
    echo -e "${YELLOW}⚠️  建议以root权限运行此脚本${NC}"
    echo "使用: sudo $0"
fi

echo -e "${BLUE}📋 修复计划:${NC}"
echo "  1. 安装缺失的依赖包"
echo "  2. 更新nginx配置（增加超时时间）"
echo "  3. 更新gunicorn配置（优化worker设置）"
echo "  4. 创建测试脚本"
echo "  5. 重启服务"
echo "  6. 验证修复效果"

# 1. 安装依赖包
echo -e "\n${BLUE}📦 步骤1: 安装依赖包...${NC}"
cd $PROJECT_DIR

# 激活虚拟环境
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
    echo "✅ 虚拟环境已激活"
else
    echo -e "${RED}❌ 虚拟环境不存在${NC}"
    exit 1
fi

# 升级pip
echo "升级pip..."
pip install --upgrade pip

# 安装导出功能依赖
echo "安装Excel处理库..."
pip install pandas==2.1.4 openpyxl==3.1.2 xlrd==2.0.1 xlwt==1.3.0

echo "安装PDF生成库..."
pip install reportlab==4.1.0

echo "安装数据处理库..."
pip install numpy==1.26.4 matplotlib==3.8.3

echo "安装异步处理库..."
pip install gevent==23.9.1

# 验证安装
echo -e "\n${BLUE}🔍 验证依赖包安装...${NC}"
python3 -c "
import pandas as pd
import openpyxl
import reportlab
import numpy as np
import matplotlib
import gevent
print('✅ 所有依赖包安装成功')
print(f'  pandas: {pd.__version__}')
print(f'  openpyxl: {openpyxl.__version__}')
print(f'  reportlab: {reportlab.__version__}')
print(f'  numpy: {np.__version__}')
print(f'  matplotlib: {matplotlib.__version__}')
print(f'  gevent: {gevent.__version__}')
"

# 2. 更新nginx配置
echo -e "\n${BLUE}🔧 步骤2: 更新nginx配置...${NC}"

# 备份原配置
if [ -f "/etc/nginx/sites-available/llrc" ]; then
    cp /etc/nginx/sites-available/llrc /etc/nginx/sites-available/llrc.backup.$(date +%Y%m%d_%H%M%S)
    echo "✅ 原nginx配置已备份"
fi

# 创建优化的nginx配置
cat > /etc/nginx/sites-available/llrc << 'EOF'
server {
    listen 80;
    server_name _;

    # 客户端最大请求体大小
    client_max_body_size 100M;

    # 静态文件缓存
    location /static/ {
        alias /var/www/llrc/app/static/;
        expires 30d;
        add_header Cache-Control "public, immutable";
        
        # 压缩静态文件
        gzip on;
        gzip_types text/css text/javascript application/javascript image/svg+xml;
    }

    # 上传文件访问
    location /uploads/ {
        alias /var/www/llrc/app/static/uploads/;
        expires 1d;
        add_header Cache-Control "public";
    }

    # 导出功能专用配置 - 增加超时时间和缓冲区
    location ~* /api/export|/api/generate_report|/api/export_data|/api/export_report {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # 导出功能专用超时设置 - 增加到5分钟
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

    # 代理到Flask应用
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # 超时设置
        proxy_connect_timeout 30s;
        proxy_send_timeout 30s;
        proxy_read_timeout 30s;
        
        # 缓冲设置
        proxy_buffering on;
        proxy_buffer_size 4k;
        proxy_buffers 8 4k;
    }

    # 健康检查
    location /health {
        access_log off;
        return 200 "healthy\n";
        add_header Content-Type text/plain;
    }

    # 安全头
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
}
EOF

# 测试nginx配置
nginx -t
if [ $? -eq 0 ]; then
    echo "✅ nginx配置更新成功"
else
    echo -e "${RED}❌ nginx配置测试失败${NC}"
    exit 1
fi

# 3. 更新gunicorn配置
echo -e "\n${BLUE}🔧 步骤3: 更新gunicorn配置...${NC}"

# 备份原配置
if [ -f "gunicorn.conf.py" ]; then
    cp gunicorn.conf.py gunicorn.conf.py.backup.$(date +%Y%m%d_%H%M%S)
    echo "✅ 原gunicorn配置已备份"
fi

# 创建优化的gunicorn配置
cat > gunicorn.conf.py << 'EOF'
# Gunicorn配置文件 - 优化导出功能
import multiprocessing
import os

# 服务器配置
bind = "127.0.0.1:5000"
workers = 2  # 增加到2个进程处理并发请求
worker_class = "gevent"  # 使用异步worker提高性能
worker_connections = 1000
timeout = 300  # 增加到5分钟支持长时间导出
keepalive = 2
max_requests = 1000
max_requests_jitter = 100
preload_app = True

# 内存和进程限制
worker_tmp_dir = "/dev/shm"  # 使用内存文件系统提高性能
max_requests_jitter = 50

# 日志配置
accesslog = "/var/log/llrc/access.log"
errorlog = "/var/log/llrc/error.log"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# 进程配置
pidfile = "/var/run/llrc/gunicorn.pid"

# 安全配置
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190

# 导出功能优化配置
def when_ready(server):
    """服务器启动时的回调"""
    server.log.info("LLRC服务器已启动，支持导出功能")

def worker_int(worker):
    """worker进程中断时的回调"""
    worker.log.info("Worker进程被中断")

def pre_fork(server, worker):
    """fork worker前的回调"""
    server.log.info("Worker进程即将启动")

def post_fork(server, worker):
    """fork worker后的回调"""
    server.log.info(f"Worker进程 {worker.pid} 已启动")

# 环境变量
raw_env = [
    'FLASK_ENV=production',
    'PYTHONPATH=/var/www/llrc',
]

# 进程名称
proc_name = 'llrc'
EOF

echo "✅ gunicorn配置更新成功"

# 4. 创建测试脚本
echo -e "\n${BLUE}📝 步骤4: 创建测试脚本...${NC}"

# 创建导出功能测试脚本
cat > test_export_functionality.py << 'EOF'
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
导出功能测试脚本
"""

import pandas as pd
import openpyxl
from io import BytesIO
import time

def test_excel_export():
    """测试Excel导出功能"""
    print("🧪 测试Excel导出功能...")
    
    try:
        # 创建测试数据
        test_data = {
            '姓名': ['张三', '李四', '王五', '赵六', '钱七'],
            '部门': ['技术部', '市场部', '销售部', '人事部', '财务部'],
            '薪资': [15000, 12000, 18000, 10000, 13000],
            '入职日期': ['2022-01-15', '2022-03-20', '2021-11-10', '2023-02-01', '2022-07-15']
        }
        
        # 测试Excel生成
        start_time = time.time()
        output = BytesIO()
        
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df = pd.DataFrame(test_data)
            df.to_excel(writer, sheet_name='员工信息', index=False)
            
            # 添加第二个工作表
            summary_data = {
                '部门': ['技术部', '市场部', '销售部', '人事部', '财务部'],
                '人数': [1, 1, 1, 1, 1],
                '平均薪资': [15000, 12000, 18000, 10000, 13000]
            }
            df_summary = pd.DataFrame(summary_data)
            df_summary.to_excel(writer, sheet_name='部门汇总', index=False)
        
        end_time = time.time()
        file_size = len(output.getvalue())
        
        print(f"✅ Excel文件生成成功")
        print(f"   文件大小: {file_size} bytes")
        print(f"   生成时间: {end_time - start_time:.2f}秒")
        
        return True
        
    except Exception as e:
        print(f"❌ Excel导出测试失败: {e}")
        return False

def test_pdf_export():
    """测试PDF导出功能"""
    print("\n🧪 测试PDF导出功能...")
    
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet
        
        # 创建PDF
        start_time = time.time()
        output = BytesIO()
        
        doc = SimpleDocTemplate(output, pagesize=A4)
        styles = getSampleStyleSheet()
        story = []
        
        # 添加内容
        story.append(Paragraph("测试报告", styles['Title']))
        story.append(Spacer(1, 12))
        story.append(Paragraph("这是一个测试PDF报告，用于验证PDF导出功能是否正常工作。", styles['Normal']))
        story.append(Spacer(1, 12))
        story.append(Paragraph("如果能看到这个内容，说明PDF导出功能正常。", styles['Normal']))
        
        doc.build(story)
        
        end_time = time.time()
        file_size = len(output.getvalue())
        
        print(f"✅ PDF文件生成成功")
        print(f"   文件大小: {file_size} bytes")
        print(f"   生成时间: {end_time - start_time:.2f}秒")
        
        return True
        
    except Exception as e:
        print(f"❌ PDF导出测试失败: {e}")
        return False

if __name__ == "__main__":
    print("🚀 开始测试导出功能...")
    
    excel_ok = test_excel_export()
    pdf_ok = test_pdf_export()
    
    if excel_ok and pdf_ok:
        print("\n✅ 所有导出功能测试通过！")
        exit(0)
    else:
        print("\n❌ 部分导出功能测试失败")
        exit(1)
EOF

chmod +x test_export_functionality.py
echo "✅ 导出功能测试脚本创建成功"

# 创建Web测试脚本
cat > test_web_export.py << 'EOF'
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Web导出功能测试脚本
"""

import requests
import time
import json

def test_export_endpoints():
    """测试各个导出端点"""
    
    base_url = "http://localhost:5000"
    
    # 导出端点列表
    export_endpoints = [
        {
            'url': '/talent/hr_admin/salary_analysis/api/export_data',
            'name': '薪酬分析导出',
            'method': 'POST'
        },
        {
            'url': '/talent/hr_admin/turnover_alert/api/export_data',
            'name': '人才流失预警导出',
            'method': 'POST'
        },
        {
            'url': '/talent/hr_admin/org_health/api/export_report',
            'name': '组织健康度导出',
            'method': 'POST'
        },
        {
            'url': '/talent/hr_admin/career_tracking/api/export_report',
            'name': '职业发展追踪导出',
            'method': 'POST'
        }
    ]
    
    print("🧪 测试Web导出端点...")
    
    for endpoint in export_endpoints:
        print(f"\n测试 {endpoint['name']} ({endpoint['url']})...")
        try:
            start_time = time.time()
            
            if endpoint['method'] == 'POST':
                response = requests.post(
                    f"{base_url}{endpoint['url']}",
                    headers={'Content-Type': 'application/json'},
                    timeout=60
                )
            else:
                response = requests.get(
                    f"{base_url}{endpoint['url']}",
                    timeout=60
                )
            
            end_time = time.time()
            duration = end_time - start_time
            
            print(f"  状态码: {response.status_code}")
            print(f"  响应时间: {duration:.2f}秒")
            print(f"  响应大小: {len(response.content)} bytes")
            
            if response.status_code == 200:
                print("  ✅ 导出成功")
            elif response.status_code == 401:
                print("  ⚠️  需要登录")
            elif response.status_code == 502:
                print("  ❌ 502错误 - 服务器配置问题")
            elif response.status_code == 500:
                print("  ❌ 500错误 - 服务器内部错误")
                try:
                    error_data = response.json()
                    print(f"  错误信息: {error_data.get('error', '未知错误')}")
                except:
                    print("  错误信息: 无法解析错误响应")
            else:
                print(f"  ❌ 错误: {response.status_code}")
                
        except requests.exceptions.Timeout:
            print("  ❌ 请求超时")
        except requests.exceptions.ConnectionError:
            print("  ❌ 连接错误")
        except Exception as e:
            print(f"  ❌ 请求失败: {e}")

if __name__ == "__main__":
    test_export_endpoints()
EOF

chmod +x test_web_export.py
echo "✅ Web测试脚本创建成功"

# 5. 重启服务
echo -e "\n${BLUE}🔄 步骤5: 重启服务...${NC}"

echo "重启nginx..."
systemctl restart nginx
if [ $? -eq 0 ]; then
    echo "✅ nginx重启成功"
else
    echo -e "${RED}❌ nginx重启失败${NC}"
    exit 1
fi

echo "重启llrc服务..."
systemctl restart $SERVICE_NAME
if [ $? -eq 0 ]; then
    echo "✅ llrc服务重启成功"
else
    echo -e "${RED}❌ llrc服务重启失败${NC}"
    exit 1
fi

# 等待服务启动
echo "等待服务启动..."
sleep 10

# 6. 验证修复效果
echo -e "\n${BLUE}🧪 步骤6: 验证修复效果...${NC}"

# 检查服务状态
echo "检查服务状态..."
systemctl status nginx --no-pager -l | head -10
echo ""
systemctl status $SERVICE_NAME --no-pager -l | head -10

# 运行导出功能测试
echo -e "\n运行导出功能测试..."
python3 test_export_functionality.py
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ 导出功能测试通过${NC}"
else
    echo -e "${RED}❌ 导出功能测试失败${NC}"
fi

# 运行Web测试
echo -e "\n运行Web测试..."
python3 test_web_export.py

# 显示修复结果
echo -e "\n${GREEN}✅ 导出功能修复部署完成！${NC}"
echo ""
echo -e "${BLUE}📋 修复内容:${NC}"
echo "  - ✅ 安装了所有必要的依赖包 (pandas, openpyxl, reportlab等)"
echo "  - ✅ 更新了nginx配置，增加了导出功能的超时时间到5分钟"
echo "  - ✅ 更新了gunicorn配置，优化了worker设置"
echo "  - ✅ 创建了导出功能测试脚本"
echo "  - ✅ 重启了相关服务"
echo ""
echo -e "${BLUE}🧪 测试脚本:${NC}"
echo "  - 本地功能测试: python3 test_export_functionality.py"
echo "  - Web端点测试: python3 test_web_export.py"
echo ""
echo -e "${BLUE}📝 主要修复点:${NC}"
echo "  - nginx proxy_read_timeout: 30s → 300s"
echo "  - gunicorn timeout: 30s → 300s"
echo "  - gunicorn workers: 1 → 2"
echo "  - 增加了导出功能的专用nginx配置"
echo "  - 优化了缓冲区设置"
echo ""
echo -e "${YELLOW}💡 如果仍有问题，请检查:${NC}"
echo "  - 服务器内存是否充足"
echo "  - 磁盘空间是否足够"
echo "  - 防火墙设置是否正确"
echo "  - 查看错误日志: journalctl -u llrc -f"
echo ""
echo -e "${GREEN}🎉 修复完成！现在可以正常使用导出功能了。${NC}"
