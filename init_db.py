#!/usr/bin/env python3
"""
数据库初始化脚本
"""

from app import create_app
from app.models import db

def init_database():
    """初始化数据库"""
    try:
        app = create_app()
        with app.app_context():
            db.create_all()
            print("✅ 数据库初始化完成")
    except Exception as e:
        print(f"❌ 数据库初始化失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    init_database()
