#!/usr/bin/env python3
"""
检查Application表结构
"""

import os
import sys

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

def check_table_structure():
    """检查Application表结构"""
    print("=== 检查Application表结构 ===\n")
    
    try:
        from app import create_app, db
        
        # 创建应用上下文
        app = create_app()
        with app.app_context():
            print("✅ 应用创建成功")
            
            # 检查表信息
            try:
                result = db.session.execute(db.text("PRAGMA table_info(application)"))
                columns = result.fetchall()
                print("📋 表结构:")
                for col in columns:
                    print(f"  列名: {col[1]}, 类型: {col[2]}, 非空: {col[3]}, 默认值: {col[4]}, 主键: {col[5]}")
                
                # 检查索引
                result = db.session.execute(db.text("PRAGMA index_list(application)"))
                indexes = result.fetchall()
                print("\n📋 索引列表:")
                for index in indexes:
                    print(f"  索引名: {index[1]}, 唯一: {index[2]}")
                
                # 检查外键
                result = db.session.execute(db.text("PRAGMA foreign_key_list(application)"))
                foreign_keys = result.fetchall()
                print("\n📋 外键列表:")
                for fk in foreign_keys:
                    print(f"  外键: {fk[3]} -> {fk[4]}.{fk[5]}")
                
                # 检查约束
                result = db.session.execute(db.text("PRAGMA table_info(application)"))
                columns = result.fetchall()
                
                # 检查是否有唯一约束
                print("\n🔍 检查唯一约束:")
                try:
                    # 尝试插入重复数据来测试约束
                    db.session.execute(db.text("""
                        INSERT INTO application (user_id, job_id, message, timestamp, status, is_active) 
                        VALUES (999, 999, 'test', datetime('now'), 'test', 1)
                    """))
                    db.session.commit()
                    print("✅ 可以插入重复数据，没有唯一约束")
                    
                    # 清理测试数据
                    db.session.execute(db.text("DELETE FROM application WHERE user_id = 999"))
                    db.session.commit()
                    
                except Exception as e:
                    print(f"❌ 存在唯一约束: {e}")
                    db.session.rollback()
                    
            except Exception as e:
                print(f"❌ 检查表结构时出错: {e}")
                
    except Exception as e:
        print(f"❌ 脚本执行失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_table_structure()
