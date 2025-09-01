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

# 用户和组（由systemd管理）
# user = "llrcuser"
# group = "llrcuser"
