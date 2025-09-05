"""
LLRC Header Start
文件功能: SmartRecruit 子系统 Python 模块：smartrecruit_system/run.py
创建时间: 2025-08-20 12:08
创建人: 潘显雨
更新记录:
- 2025-08-20 12:38 by 侯东杨
- 2025-08-28 11:17 by 谢佳悦
LLRC Header End
"""
"""
FILE-HEADER-AUTO-ADDED
文件: smartrecruit_system/run.py
功能: 应用启动入口
创建时间: 2025-08-27 15:52
创建人: 谢佳悦
更新记录:
- 2025-08-24 16:20 by 谢佳悦
- 2025-08-27 13:47 by 侯东杨
- 2025-09-02 11:19 by 李雨梦
"""
import os
import sys

# Ensure the project root (this directory) is on the Python path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)
from app import create_app

app = create_app()

if __name__ == '__main__':
    try:
        port = int(os.environ.get('PORT', '5000'))
    except Exception:
        port = 5000
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False, threaded=True)
