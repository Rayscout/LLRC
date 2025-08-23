#!/usr/bin/env python3
"""
数据库迁移脚本：为Application表添加is_active字段
"""

import os
import sys

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def migrate_add_is_active():
    """为Application表添加is_active字段"""
    print("=== 数据库迁移：添加is_active字段 ===\n")
    
    try:
        from app import create_app, db
        from app.models import Application
        
        # 创建应用上下文
        app = create_app()
        with app.app_context():
            print("✅ 应用创建成功")
            
            # 检查数据库连接
            try:
                db.session.execute(db.text('SELECT 1'))
                print("✅ 数据库连接成功")
            except Exception as e:
                print(f"❌ 数据库连接失败: {e}")
                return
            
            # 检查is_active字段是否已存在
            try:
                # 尝试查询is_active字段
                result = db.session.execute(db.text("PRAGMA table_info(application)"))
                columns = [row[1] for row in result.fetchall()]
                
                if 'is_active' in columns:
                    print("✅ is_active字段已存在，跳过迁移")
                    return
                else:
                    print("📝 需要添加is_active字段")
            except Exception as e:
                print(f"⚠️ 检查字段时出错: {e}")
            
            # 添加is_active字段
            try:
                # 添加is_active字段，默认值为True
                db.session.execute(db.text("ALTER TABLE application ADD COLUMN is_active BOOLEAN DEFAULT 1"))
                db.session.commit()
                print("✅ 成功添加is_active字段")
                
                # 更新现有记录，将所有现有申请标记为活跃
                db.session.execute(db.text("UPDATE application SET is_active = 1 WHERE is_active IS NULL"))
                db.session.commit()
                print("✅ 成功更新现有申请记录")
                
                # 验证迁移结果
                total_applications = db.session.execute(db.text("SELECT COUNT(*) FROM application")).scalar()
                active_applications = db.session.execute(db.text("SELECT COUNT(*) FROM application WHERE is_active = 1")).scalar()
                
                print(f"📊 迁移结果:")
                print(f"   总申请数: {total_applications}")
                print(f"   活跃申请数: {active_applications}")
                
                print("✅ 数据库迁移完成")
                
            except Exception as e:
                print(f"❌ 迁移失败: {e}")
                db.session.rollback()
                
    except Exception as e:
        print(f"❌ 迁移脚本执行失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    migrate_add_is_active()
