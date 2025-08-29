#!/usr/bin/env python3
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
