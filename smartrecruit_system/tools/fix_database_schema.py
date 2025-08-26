#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import os

def fix_database_schema():
    """修复数据库架构，添加缺失的字段"""
    print("🔧 正在修复数据库架构...")
    
    # 数据库路径
    db_path = 'instance/site.db'
    
    if not os.path.exists(db_path):
        print(f"❌ 数据库文件不存在: {db_path}")
        return False
    
    try:
        # 连接数据库
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 1. 检查并添加user_type字段到user表
        cursor.execute("PRAGMA table_info(user)")
        user_columns = [column[1] for column in cursor.fetchall()]
        
        if 'user_type' not in user_columns:
            print("➕ 添加user_type字段到user表...")
            cursor.execute("ALTER TABLE user ADD COLUMN user_type TEXT DEFAULT 'candidate'")
        else:
            print("ℹ️ user_type字段已存在")
        
        # 2. 检查并添加is_active字段到application表
        cursor.execute("PRAGMA table_info(application)")
        application_columns = [column[1] for column in cursor.fetchall()]
        
        if 'is_active' not in application_columns:
            print("➕ 添加is_active字段到application表...")
            cursor.execute("ALTER TABLE application ADD COLUMN is_active BOOLEAN DEFAULT 1")
        else:
            print("ℹ️ is_active字段已存在")
        
        # 3. 更新现有用户的user_type
        print("🔄 更新现有用户的user_type...")
        
        # 根据is_hr字段设置用户类型
        cursor.execute("UPDATE user SET user_type = 'supervisor' WHERE is_hr = 1 AND (user_type IS NULL OR user_type = 'candidate')")
        
        # 确保所有用户都有user_type
        cursor.execute("UPDATE user SET user_type = 'candidate' WHERE user_type IS NULL")
        
        # 4. 显示当前用户状态
        cursor.execute("SELECT user_type, COUNT(*) FROM user GROUP BY user_type")
        user_counts = cursor.fetchall()
        
        print("📊 当前用户分布:")
        for user_type, count in user_counts:
            print(f"   {user_type}: {count} 人")
        
        # 提交更改
        conn.commit()
        conn.close()
        
        print("✅ 数据库架构修复完成")
        return True
        
    except Exception as e:
        print(f"❌ 修复失败: {e}")
        return False

if __name__ == "__main__":
    fix_database_schema()
