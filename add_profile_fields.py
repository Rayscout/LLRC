#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import os

def add_profile_fields():
    """添加个人资料相关字段到User表"""
    print("🔧 正在添加个人资料相关字段...")
    
    # 数据库路径
    db_path = 'instance/site.db'
    
    if not os.path.exists(db_path):
        print(f"❌ 数据库文件不存在: {db_path}")
        return False
    
    try:
        # 连接数据库
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 检查并添加字段
        cursor.execute("PRAGMA table_info(user)")
        columns = [column[1] for column in cursor.fetchall()]
        
        fields_to_add = [
            ('bio', 'TEXT'),
            ('skills', 'TEXT'),
            ('education', 'TEXT'),
            ('experience', 'TEXT')
        ]
        
        for field_name, field_type in fields_to_add:
            if field_name not in columns:
                print(f"➕ 添加字段 {field_name}...")
                cursor.execute(f"ALTER TABLE user ADD COLUMN {field_name} {field_type}")
            else:
                print(f"ℹ️ 字段 {field_name} 已存在")
        
        # 提交更改
        conn.commit()
        conn.close()
        
        print("✅ 个人资料字段添加完成")
        return True
        
    except Exception as e:
        print(f"❌ 添加字段失败: {e}")
        return False

if __name__ == "__main__":
    add_profile_fields()
