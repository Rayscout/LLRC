"""
LLRC Header Start
文件功能: 应用后端 Python 模块：app/run.py
创建时间: 2025-08-26 09:18
创建人: 谢佳悦
更新记录:
- 2025-09-03 17:13 by 张宇成
LLRC Header End
"""
#!/usr/bin/env python3
"""
FILE-HEADER-AUTO-ADDED
文件: app/run.py
功能: 应用启动入口
创建时间: 2025-08-20 17:12
创建人: 李雨梦
更新记录:
- 2025-08-26 09:48 by 张宇成
- 2025-08-29 14:17 by 张宇成
- 2025-09-01 15:14 by 李雨梦
"""
"""
启动应用并处理错误
"""

import sys
import os
import traceback
import logging

# 配置详细日志
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

def main():
    """主函数"""
    try:
        logger.info("🚀 开始启动应用...")
        
        # 添加项目根目录到Python路径
        current_dir = os.path.dirname(os.path.abspath(__file__))
        sys.path.insert(0, current_dir)
        logger.info(f"Python路径已设置: {current_dir}")
        
        # 导入应用
        logger.info("正在导入应用...")
        from app import create_app
        
        # 创建应用
        logger.info("正在创建应用...")
        app = create_app()
        logger.info("✅ 应用创建成功")
        
        # 测试数据库连接
        logger.info("正在测试数据库连接...")
        with app.app_context():
            from app.models import db
            from sqlalchemy import text
            try:
                db.session.execute(text('SELECT 1'))
                logger.info("数据库连接正常")
            except Exception as e:
                logger.error(f"数据库连接失败: {e}")
                logger.error(traceback.format_exc())
        
        # 启动应用
        logger.info("正在启动Flask应用...")
        logger.info("应用将在 http://localhost:5000 上运行")
        logger.info("按 Ctrl+C 停止应用")
        
        app.run(
            debug=True,
            host='0.0.0.0',
            port=5000,
            use_reloader=False  # 避免重复启动
        )
        
    except ImportError as e:
        logger.error(f"❌ 导入错误: {e}")
        logger.error(traceback.format_exc())
        print(f"\n❌ 导入错误: {e}")
        print("请检查模块路径和依赖是否正确安装")
        
    except Exception as e:
        logger.error(f"❌ 应用启动失败: {e}")
        logger.error(traceback.format_exc())
        print(f"\n❌ 应用启动失败: {e}")
        print("详细错误信息已写入 app.log 文件")
        
    finally:
        logger.info("应用已停止")

if __name__ == '__main__':
    main()
