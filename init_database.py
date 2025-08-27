#!/usr/bin/env python3
"""
初始化数据库
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def init_database():
    """初始化数据库"""
    try:
        print("🚀 开始初始化数据库...")
        
        # 导入应用
        from app import create_app, db
        from app.models import User
        
        # 创建应用
        app = create_app()
        
        with app.app_context():
            print("✅ 应用创建成功")
            
            # 删除所有表（如果存在）
            print("正在删除现有表...")
            db.drop_all()
            
            # 创建所有表
            print("正在创建新表...")
            db.create_all()
            
            print("✅ 数据库表创建成功")
            
            # 验证表是否创建成功
            from sqlalchemy import text
            result = db.session.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))
            tables = [row[0] for row in result]
            print(f"✅ 已创建的表: {tables}")
            
            # 测试User模型
            user_count = User.query.count()
            print(f"✅ User模型正常，当前用户数量: {user_count}")
            
            print("🎉 数据库初始化完成！")
            
    except Exception as e:
        print(f"❌ 数据库初始化失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    init_database()
