"""
LLRC Header Start
文件功能: 通用 Python 脚本/模块：config/gunicorn.conf.py
创建时间: 2025-08-21 14:44
创建人: 侯东杨
更新记录:
- 2025-08-22 16:50 by 张宇成
- 2025-08-27 15:14 by 张宇成
LLRC Header End
"""
"""
FILE-HEADER-AUTO-ADDED
文件: config/gunicorn.conf.py
功能: 通用模块
创建时间: 2025-09-02 15:43
创建人: 张宇成
更新记录:
- 2025-08-21 15:14 by 潘显雨
- 2025-08-21 17:47 by 潘显雨
- 2025-08-27 15:48 by 张宇成
"""
# Gunicorn配置文件
import multiprocessing

# 服务器配置
bind = "127.0.0.1:5000"
workers = 1  # 使用单进程避免权限问题
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2
max_requests = 1000
max_requests_jitter = 100
preload_app = True

# 日志配置
accesslog = "/var/log/llrc/access.log"
errorlog = "/var/log/llrc/error.log"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# 进程配置
pidfile = "/var/run/llrc/gunicorn.pid"
# user = "www-data"  # 注释掉，让systemd管理用户权限
# group = "www-data"  # 注释掉，让systemd管理用户权限

# 安全配置
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190
