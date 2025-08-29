# Gunicorn配置文件
import multiprocessing

# 服务器配置
bind = "127.0.0.1:5000"
workers = multiprocessing.cpu_count() * 2 + 1
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
user = "www-data"
group = "www-data"

# 安全配置
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190
