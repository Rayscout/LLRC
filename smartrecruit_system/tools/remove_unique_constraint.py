#!/usr/bin/env python3
"""
删除Application表的唯一约束
"""

import os
import sys

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

def remove_unique_constraint():
    """删除Application表的唯一约束"""
    print("=== 删除Application表的唯一约束 ===\n")
    
    try:
        from app import create_app, db
        
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
            
            # 检查约束是否存在
            try:
                result = db.session.execute(db.text("PRAGMA index_list(application)"))
                indexes = result.fetchall()
                print("📋 当前索引列表:")
                for index in indexes:
                    print(f"  索引名: {index[1]}, 唯一: {index[2]}")
                
                # 查找唯一约束
                unique_constraint = None
                for index in indexes:
                    if index[1] == 'unique_user_job_application':
                        unique_constraint = index
                        break
                
                if unique_constraint:
                    print(f"🔍 找到唯一约束: {unique_constraint[1]}")
                    
                    # 删除唯一约束
                    try:
                        db.session.execute(db.text("DROP INDEX unique_user_job_application"))
                        db.session.commit()
                        print("✅ 成功删除唯一约束")
                    except Exception as e:
                        print(f"❌ 删除约束失败: {e}")
                        db.session.rollback()
                else:
                    print("✅ 未找到唯一约束，无需删除")
                    
            except Exception as e:
                print(f"❌ 检查约束时出错: {e}")
                
            # 验证删除结果
            try:
                result = db.session.execute(db.text("PRAGMA index_list(application)"))
                indexes = result.fetchall()
                print("\n📋 删除后的索引列表:")
                for index in indexes:
                    print(f"  索引名: {index[1]}, 唯一: {index[2]}")
                    
                # 检查是否还有唯一约束
                has_unique = any(index[2] for index in indexes if 'user_id' in str(index) and 'job_id' in str(index))
                if not has_unique:
                    print("✅ 确认唯一约束已删除")
                else:
                    print("⚠️ 仍存在唯一约束")
                    
            except Exception as e:
                print(f"❌ 验证删除结果时出错: {e}")
                
    except Exception as e:
        print(f"❌ 脚本执行失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    remove_unique_constraint()
