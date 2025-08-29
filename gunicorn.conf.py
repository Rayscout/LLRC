# Gunicorn配置文件
import multiprocessing

# 服务器配置
bind = "127.0.0.1:8000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000

# 超时设置
timeout = 30
keepalive = 2

# 请求限制
max_requests = 1000
max_requests_jitter = 100

# 预加载应用
preload_app = True

# 日志配置
accesslog = "/var/log/llrc/access.log"
errorlog = "/var/log/llrc/error.log"
loglevel = "info"

# 进程名称
proc_name = "llrc"

# 用户和组
user = "www-data"
group = "www-data"
