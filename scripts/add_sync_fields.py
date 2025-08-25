#!/usr/bin/env python3
"""
数据库迁移脚本：添加同步相关字段
为现有的Job、Application、User表添加同步时间字段
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import Job, Application, User
from datetime import datetime

def add_sync_fields():
    """为现有表添加同步相关字段"""
    app = create_app()
    
    with app.app_context():
        try:
            print("开始添加同步字段...")
            
            # 检查字段是否已存在
            inspector = db.inspect(db.engine)
            
            # 检查User表
            user_columns = [col['name'] for col in inspector.get_columns('user')]
            if 'cv_last_synced' not in user_columns:
                print("为User表添加cv_last_synced字段...")
                with db.engine.connect() as conn:
                    conn.execute(db.text('ALTER TABLE user ADD COLUMN cv_last_synced DATETIME'))
                    conn.commit()
                print("✓ User表字段添加成功")
            else:
                print("✓ User表字段已存在")
            
            # 检查Job表
            job_columns = [col['name'] for col in inspector.get_columns('job')]
            if 'last_synced' not in job_columns:
                print("为Job表添加last_synced字段...")
                with db.engine.connect() as conn:
                    conn.execute(db.text('ALTER TABLE job ADD COLUMN last_synced DATETIME'))
                    conn.commit()
                print("✓ Job表字段添加成功")
            else:
                print("✓ Job表字段已存在")
            
            # 检查Application表
            app_columns = [col['name'] for col in inspector.get_columns('application')]
            if 'last_synced' not in app_columns:
                print("为Application表添加last_synced字段...")
                with db.engine.connect() as conn:
                    conn.execute(db.text('ALTER TABLE application ADD COLUMN last_synced DATETIME'))
                    conn.commit()
                print("✓ Application表字段添加成功")
            else:
                print("✓ Application表字段已存在")
            
            print("\n所有同步字段添加完成！")
            
            # 显示表结构
            print("\n当前表结构：")
            for table_name in ['user', 'job', 'application']:
                print(f"\n{table_name}表:")
                columns = inspector.get_columns(table_name)
                for col in columns:
                    print(f"  - {col['name']}: {col['type']}")
            
        except Exception as e:
            print(f"添加同步字段失败: {e}")
            return False
        
        return True

def update_existing_records():
    """更新现有记录的同步时间"""
    app = create_app()
    
    with app.app_context():
        try:
            print("\n开始更新现有记录的同步时间...")
            
            # 更新所有现有职位
            jobs = Job.query.all()
            for job in jobs:
                if not job.last_synced:
                    job.last_synced = job.created_at or datetime.utcnow()
            print(f"✓ 更新了 {len(jobs)} 个职位记录")
            
            # 更新所有现有申请
            applications = Application.query.all()
            for app in applications:
                if not app.last_synced:
                    app.last_synced = app.timestamp or datetime.utcnow()
            print(f"✓ 更新了 {len(applications)} 个申请记录")
            
            # 更新所有现有用户
            users = User.query.all()
            for user in users:
                if not user.cv_last_synced and user.cv_file:
                    user.cv_last_synced = datetime.utcnow()
            print(f"✓ 更新了 {len(users)} 个用户记录")
            
            db.session.commit()
            print("✓ 所有记录更新完成")
            
        except Exception as e:
            print(f"更新现有记录失败: {e}")
            db.session.rollback()
            return False
        
        return True

def main():
    """主函数"""
    print("=" * 50)
    print("数据库同步字段迁移脚本")
    print("=" * 50)
    
    # 添加同步字段
    if not add_sync_fields():
        print("❌ 添加同步字段失败")
        return
    
    # 更新现有记录
    if not update_existing_records():
        print("❌ 更新现有记录失败")
        return
    
    print("\n" + "=" * 50)
    print("✅ 数据库迁移完成！")
    print("=" * 50)
    print("\n现在您可以：")
    print("1. HR发布的职位会自动同步到求职者端")
    print("2. 求职者的申请会自动同步到HR端")
    print("3. 求职者的简历更新会自动同步到HR端")
    print("4. 在HR端可以查看和管理数据同步状态")

if __name__ == '__main__':
    main()
