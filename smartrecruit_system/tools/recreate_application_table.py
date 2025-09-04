"""
LLRC Header Start
文件功能: SmartRecruit 子系统 Python 模块：smartrecruit_system/tools/recreate_application_table.py
创建时间: 2025-08-19 15:40
创建人: 李雨梦
更新记录:
- 2025-08-19 16:10 by 潘显雨
LLRC Header End
"""
#!/usr/bin/env python3
"""
FILE-HEADER-AUTO-ADDED
文件: smartrecruit_system/tools/recreate_application_table.py
功能: 通用模块
创建时间: 2025-08-29 14:50
创建人: 苏杰
更新记录:
- 2025-08-26 10:15 by 李雨梦
"""
"""
重新创建Application表，移除唯一约束
"""

import os
import sys

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

def recreate_application_table():
    """重新创建Application表"""
    print("=== 重新创建Application表 ===\n")
    
    try:
        from app import create_app, db
        from app.models import Application
        
        # 创建应用上下文
        app = create_app()
        with app.app_context():
            print("✅ 应用创建成功")
            
            # 备份现有数据
            try:
                result = db.session.execute(db.text("SELECT * FROM application"))
                existing_data = result.fetchall()
                print(f"📊 备份了 {len(existing_data)} 条现有数据")
            except Exception as e:
                print(f"⚠️ 备份数据时出错: {e}")
                existing_data = []
            
            # 删除现有表
            try:
                db.session.execute(db.text("DROP TABLE IF EXISTS application"))
                db.session.commit()
                print("✅ 删除现有表")
            except Exception as e:
                print(f"❌ 删除表失败: {e}")
                return
            
            # 重新创建表
            try:
                # 创建新表，不包含唯一约束
                create_table_sql = """
                CREATE TABLE application (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    job_id INTEGER NOT NULL,
                    message TEXT NOT NULL,
                    timestamp DATETIME,
                    status VARCHAR(20) NOT NULL,
                    is_active BOOLEAN DEFAULT 1,
                    FOREIGN KEY (user_id) REFERENCES user (id),
                    FOREIGN KEY (job_id) REFERENCES job (id)
                )
                """
                db.session.execute(db.text(create_table_sql))
                db.session.commit()
                print("✅ 重新创建表成功")
                
                # 恢复数据（如果有的话）
                if existing_data:
                    try:
                        for row in existing_data:
                            # 假设数据格式为 (id, user_id, job_id, message, timestamp, status, is_active)
                            if len(row) >= 6:
                                insert_sql = """
                                INSERT INTO application (id, user_id, job_id, message, timestamp, status, is_active)
                                VALUES (?, ?, ?, ?, ?, ?, ?)
                                """
                                is_active = row[6] if len(row) > 6 else 1
                                db.session.execute(db.text(insert_sql), 
                                                 (row[0], row[1], row[2], row[3], row[4], row[5], is_active))
                        
                        db.session.commit()
                        print(f"✅ 恢复了 {len(existing_data)} 条数据")
                    except Exception as e:
                        print(f"⚠️ 恢复数据时出错: {e}")
                        db.session.rollback()
                
                # 验证表结构
                result = db.session.execute(db.text("PRAGMA table_info(application)"))
                columns = result.fetchall()
                print("\n📋 新表结构:")
                for col in columns:
                    print(f"  列名: {col[1]}, 类型: {col[2]}, 非空: {col[3]}, 默认值: {col[4]}, 主键: {col[5]}")
                
                # 检查索引
                result = db.session.execute(db.text("PRAGMA index_list(application)"))
                indexes = result.fetchall()
                print("\n📋 索引列表:")
                for index in indexes:
                    print(f"  索引名: {index[1]}, 唯一: {index[2]}")
                
                # 测试插入重复数据
                print("\n🔍 测试重复数据插入:")
                try:
                    # 插入测试数据
                    db.session.execute(db.text("""
                        INSERT INTO application (user_id, job_id, message, timestamp, status, is_active)
                        VALUES (1, 1, 'test1', datetime('now'), 'test', 1)
                    """))
                    db.session.commit()
                    
                    # 尝试插入重复数据
                    db.session.execute(db.text("""
                        INSERT INTO application (user_id, job_id, message, timestamp, status, is_active)
                        VALUES (1, 1, 'test2', datetime('now'), 'test', 1)
                    """))
                    db.session.commit()
                    print("✅ 可以插入重复数据，没有唯一约束")
                    
                    # 清理测试数据
                    db.session.execute(db.text("DELETE FROM application WHERE message LIKE 'test%'"))
                    db.session.commit()
                    
                except Exception as e:
                    print(f"❌ 仍然存在唯一约束: {e}")
                    db.session.rollback()
                
            except Exception as e:
                print(f"❌ 重新创建表失败: {e}")
                db.session.rollback()
                
    except Exception as e:
        print(f"❌ 脚本执行失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    recreate_application_table()
