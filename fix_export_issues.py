#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
云服务器导出功能修复脚本
解决502错误和导出功能问题
"""

import os
import sys
import subprocess
import importlib
from pathlib import Path

def check_dependencies():
    """检查导出功能所需的依赖包"""
    print("🔍 检查导出功能依赖包...")
    
    required_packages = {
        'pandas': '2.1.4',
        'openpyxl': '3.1.2', 
        'xlrd': '2.0.1',
        'xlwt': '1.3.0',
        'reportlab': '4.1.0',
        'numpy': '1.26.4',
        'matplotlib': '3.8.3'
    }
    
    missing_packages = []
    
    for package, expected_version in required_packages.items():
        try:
            module = importlib.import_module(package)
            version = getattr(module, '__version__', 'unknown')
            print(f"✅ {package}: {version}")
        except ImportError:
            print(f"❌ {package}: 未安装")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️  缺少依赖包: {', '.join(missing_packages)}")
        return False
    else:
        print("\n✅ 所有依赖包已正确安装")
        return True

def test_export_functionality():
    """测试导出功能"""
    print("\n🧪 测试导出功能...")
    
    try:
        import pandas as pd
        import openpyxl
        from io import BytesIO
        
        # 创建测试数据
        test_data = {
            '姓名': ['张三', '李四', '王五'],
            '部门': ['技术部', '市场部', '销售部'],
            '薪资': [15000, 12000, 18000]
        }
        
        # 测试Excel生成
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df = pd.DataFrame(test_data)
            df.to_excel(writer, sheet_name='测试数据', index=False)
        
        output.seek(0)
        file_size = len(output.getvalue())
        
        print(f"✅ Excel文件生成成功，大小: {file_size} bytes")
        return True
        
    except Exception as e:
        print(f"❌ 导出功能测试失败: {e}")
        return False

def update_nginx_config():
    """更新nginx配置以支持长时间导出"""
    print("\n🔧 更新nginx配置...")
    
    nginx_config = """server {
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

    # 导出功能专用配置 - 增加超时时间
    location ~* /api/export|/api/generate_report {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # 导出功能专用超时设置 - 增加到5分钟
        proxy_connect_timeout 60s;
        proxy_send_timeout 300s;
        proxy_read_timeout 300s;
        
        # 缓冲设置
        proxy_buffering on;
        proxy_buffer_size 8k;
        proxy_buffers 16 8k;
        proxy_busy_buffers_size 16k;
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
        return 200 "healthy\\n";
        add_header Content-Type text/plain;
    }

    # 安全头
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
}"""
    
    try:
        with open('/etc/nginx/sites-available/llrc', 'w', encoding='utf-8') as f:
            f.write(nginx_config)
        
        # 测试nginx配置
        result = subprocess.run(['nginx', '-t'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ nginx配置更新成功")
            return True
        else:
            print(f"❌ nginx配置测试失败: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ 更新nginx配置失败: {e}")
        return False

def update_gunicorn_config():
    """更新gunicorn配置"""
    print("\n🔧 更新gunicorn配置...")
    
    gunicorn_config = """# Gunicorn配置文件
import multiprocessing

# 服务器配置
bind = "127.0.0.1:5000"
workers = 2  # 增加到2个进程
worker_class = "sync"
worker_connections = 1000
timeout = 300  # 增加到5分钟
keepalive = 2
max_requests = 1000
max_requests_jitter = 100
preload_app = True

# 内存和进程限制
worker_tmp_dir = "/dev/shm"  # 使用内存文件系统
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

# 导出功能优化
worker_class = "gevent"  # 使用异步worker
worker_connections = 1000
"""
    
    try:
        with open('/var/www/llrc/gunicorn.conf.py', 'w', encoding='utf-8') as f:
            f.write(gunicorn_config)
        
        print("✅ gunicorn配置更新成功")
        return True
        
    except Exception as e:
        print(f"❌ 更新gunicorn配置失败: {e}")
        return False

def install_missing_dependencies():
    """安装缺失的依赖包"""
    print("\n📦 安装缺失的依赖包...")
    
    try:
        # 升级pip
        subprocess.run([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'], 
                      check=True, capture_output=True)
        
        # 安装依赖包
        packages = [
            'pandas==2.1.4',
            'openpyxl==3.1.2',
            'xlrd==2.0.1', 
            'xlwt==1.3.0',
            'reportlab==4.1.0',
            'numpy==1.26.4',
            'matplotlib==3.8.3'
        ]
        
        for package in packages:
            print(f"安装 {package}...")
            subprocess.run([sys.executable, '-m', 'pip', 'install', package], 
                          check=True, capture_output=True)
        
        print("✅ 依赖包安装完成")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ 安装依赖包失败: {e}")
        return False

def create_export_test_script():
    """创建导出功能测试脚本"""
    print("\n📝 创建导出功能测试脚本...")
    
    test_script = """#!/usr/bin/env python3
# -*- coding: utf-8 -*-
\"\"\"
导出功能测试脚本
\"\"\"

import requests
import time
import json

def test_export_endpoints():
    \"\"\"测试各个导出端点\"\"\"
    
    base_url = "http://localhost:5000"
    
    # 需要登录的端点
    export_endpoints = [
        "/talent/hr_admin/salary_analysis/api/export_data",
        "/talent/hr_admin/turnover_alert/api/export_data", 
        "/talent/hr_admin/org_health/api/export_report",
        "/talent/hr_admin/career_tracking/api/export_report"
    ]
    
    print("🧪 测试导出端点...")
    
    for endpoint in export_endpoints:
        print(f"\\n测试 {endpoint}...")
        try:
            start_time = time.time()
            
            # 发送POST请求
            response = requests.post(
                f"{base_url}{endpoint}",
                headers={'Content-Type': 'application/json'},
                timeout=60  # 60秒超时
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
            else:
                print(f"  ❌ 错误: {response.status_code}")
                
        except requests.exceptions.Timeout:
            print("  ❌ 请求超时")
        except Exception as e:
            print(f"  ❌ 请求失败: {e}")

if __name__ == "__main__":
    test_export_endpoints()
"""
    
    try:
        with open('/var/www/llrc/test_export.py', 'w', encoding='utf-8') as f:
            f.write(test_script)
        
        # 设置执行权限
        os.chmod('/var/www/llrc/test_export.py', 0o755)
        
        print("✅ 测试脚本创建成功")
        return True
        
    except Exception as e:
        print(f"❌ 创建测试脚本失败: {e}")
        return False

def restart_services():
    """重启相关服务"""
    print("\n🔄 重启服务...")
    
    services = ['nginx', 'llrc']
    
    for service in services:
        try:
            print(f"重启 {service}...")
            subprocess.run(['sudo', 'systemctl', 'restart', service], 
                          check=True, capture_output=True)
            print(f"✅ {service} 重启成功")
        except subprocess.CalledProcessError as e:
            print(f"❌ 重启 {service} 失败: {e}")
            return False
    
    return True

def main():
    """主函数"""
    print("🚀 开始修复云服务器导出功能...")
    
    # 检查当前用户权限
    if os.geteuid() != 0:
        print("⚠️  建议以root权限运行此脚本")
    
    # 1. 检查依赖包
    if not check_dependencies():
        print("\\n📦 安装缺失的依赖包...")
        if not install_missing_dependencies():
            print("❌ 依赖包安装失败，请手动安装")
            return False
    
    # 2. 测试导出功能
    if not test_export_functionality():
        print("❌ 导出功能测试失败")
        return False
    
    # 3. 更新nginx配置
    if not update_nginx_config():
        print("❌ nginx配置更新失败")
        return False
    
    # 4. 更新gunicorn配置
    if not update_gunicorn_config():
        print("❌ gunicorn配置更新失败")
        return False
    
    # 5. 创建测试脚本
    if not create_export_test_script():
        print("❌ 测试脚本创建失败")
        return False
    
    # 6. 重启服务
    if not restart_services():
        print("❌ 服务重启失败")
        return False
    
    print("\\n✅ 导出功能修复完成！")
    print("\\n📋 修复内容:")
    print("  - 增加了nginx和gunicorn的超时时间")
    print("  - 优化了导出功能的nginx配置")
    print("  - 增加了gunicorn worker数量")
    print("  - 安装了必要的依赖包")
    print("  - 创建了测试脚本")
    
    print("\\n🧪 运行测试:")
    print("  python3 /var/www/llrc/test_export.py")
    
    return True

if __name__ == "__main__":
    main()
