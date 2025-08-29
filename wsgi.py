#!/usr/bin/env python3
"""
WSGI入口文件
"""

import sys
import os

# 添加项目根目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# 导入并创建Flask应用
from app import create_app

# 创建应用实例
app = create_app()

if __name__ == "__main__":
    app.run()
