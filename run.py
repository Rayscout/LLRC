"""
LLRC Header Start
文件功能: 通用 Python 脚本/模块：run.py
创建时间: 2025-08-23 15:39
创建人: 张宇成
更新记录:
- 2025-08-23 16:09 by 张宇成
- 2025-08-29 15:49 by 苏杰
LLRC Header End
"""
"""
FILE-HEADER-AUTO-ADDED
文件: run.py
功能: 应用启动入口
创建时间: 2025-08-28 11:28
创建人: 谢佳悦
更新记录:
- 2025-08-30 16:16 by 苏杰
- 2025-09-02 09:09 by 侯东杨
"""
import os
import sys

# Ensure the project root (this directory) is on the Python path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)
3
from app import create_app

app = create_app()

if __name__ == '__main__':
    
    import os
    try:
        port = int(os.environ.get('PORT', '5000'))
    except Exception:
        port = 5000
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False, threaded=True)
