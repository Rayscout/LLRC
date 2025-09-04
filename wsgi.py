"""
LLRC Header Start
文件功能: 通用 Python 脚本/模块：wsgi.py
创建时间: 2025-08-21 16:54
创建人: 苏杰
更新记录:
- 2025-08-26 10:47 by 谢佳悦
- 2025-08-27 10:02 by 侯东杨
- 2025-08-31 11:27 by 李雨梦
LLRC Header End
"""
#!/usr/bin/env python3
"""
FILE-HEADER-AUTO-ADDED
文件: wsgi.py
功能: WSGI 启动入口
创建时间: 2025-08-30 10:19
创建人: 潘显雨
更新记录:
- 2025-08-21 17:24 by 苏杰
- 2025-08-30 16:57 by 苏杰
"""
"""
WSGI入口文件 - 用于生产环境部署
"""

import os
import sys

# 设置环境变量
os.environ['FLASK_ENV'] = 'production'

# 添加项目根目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# 导入应用工厂函数
from app import create_app

# 创建应用实例
application = create_app()

if __name__ == "__main__":
    application.run()
