"""
LLRC Header Start
文件功能: SmartRecruit 子系统 Python 模块：smartrecruit_system/tools/migrate_add_is_active.py
创建时间: 2025-08-21 11:18
创建人: 苏杰
更新记录:
- 2025-08-21 11:48 by 潘显雨
- 2025-08-28 09:33 by 李雨梦
- 2025-08-30 16:28 by 苏杰
LLRC Header End
"""
#!/usr/bin/env python3
"""
FILE-HEADER-AUTO-ADDED
文件: smartrecruit_system/tools/migrate_add_is_active.py
功能: 通用模块
创建时间: 2025-08-23 16:22
创建人: 李雨梦
更新记录:
- 2025-09-03 11:58 by 李雨梦
"""
"""
数据库迁移脚本：
1) 为 user 表添加账号状态字段：is_active, deactivated_at, deactivated_by
2) 为 application 表添加 is_active 字段（若缺失）
"""

import os
import sys

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

def migrate_add_is_active():
    """为 user 与 application 表添加缺失字段"""
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
            
            # 1) user 表新增账号状态字段
            try:
                user_cols = [row[1] for row in db.session.execute(db.text("PRAGMA table_info(user)")).fetchall()]
                print(f"当前 user 表字段: {user_cols}")

                # 依次补齐
                if 'is_active' not in user_cols:
                    db.session.execute(db.text("ALTER TABLE user ADD COLUMN is_active BOOLEAN DEFAULT 1"))
                    print("✅ user.is_active 添加完成")
                else:
                    print("ℹ️ user.is_active 已存在")

                if 'deactivated_at' not in user_cols:
                    db.session.execute(db.text("ALTER TABLE user ADD COLUMN deactivated_at DATETIME"))
                    print("✅ user.deactivated_at 添加完成")
                else:
                    print("ℹ️ user.deactivated_at 已存在")

                if 'deactivated_by' not in user_cols:
                    db.session.execute(db.text("ALTER TABLE user ADD COLUMN deactivated_by INTEGER REFERENCES user(id)"))
                    print("✅ user.deactivated_by 添加完成")
                else:
                    print("ℹ️ user.deactivated_by 已存在")

                db.session.commit()
            except Exception as e:
                print(f"❌ 更新 user 表失败: {e}")
                db.session.rollback()

            # 2) application 表新增 is_active 字段
            try:
                app_cols = [row[1] for row in db.session.execute(db.text("PRAGMA table_info(application)")).fetchall()]
                if 'is_active' not in app_cols:
                    db.session.execute(db.text("ALTER TABLE application ADD COLUMN is_active BOOLEAN DEFAULT 1"))
                    db.session.commit()
                    print("✅ application.is_active 添加完成")
                    db.session.execute(db.text("UPDATE application SET is_active = 1 WHERE is_active IS NULL"))
                    db.session.commit()
                    print("✅ application 现有记录初始化完成")
                else:
                    print("ℹ️ application.is_active 已存在")

                # 验证迁移结果
                total_applications = db.session.execute(db.text("SELECT COUNT(*) FROM application")).scalar()
                active_applications = db.session.execute(db.text("SELECT COUNT(*) FROM application WHERE is_active = 1")).scalar()
                print("📊 迁移结果:")
                print(f"   总申请数: {total_applications}")
                print(f"   活跃申请数: {active_applications}")
                print("✅ 数据库迁移完成")
            except Exception as e:
                print(f"❌ 更新 application 表失败: {e}")
                db.session.rollback()
                
    except Exception as e:
        print(f"❌ 迁移脚本执行失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    migrate_add_is_active()
