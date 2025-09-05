"""
LLRC Header Start
文件功能: SmartRecruit 子系统 Python 模块：smartrecruit_system/tools/add_user_fields.py
创建时间: 2025-08-20 12:13
创建人: 张宇成
更新记录:
- 2025-08-20 12:43 by 张宇成
- 2025-08-27 17:57 by 李雨梦
- 2025-09-03 13:24 by 谢佳悦
LLRC Header End
"""
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FILE-HEADER-AUTO-ADDED
文件: smartrecruit_system/tools/add_user_fields.py
功能: 通用模块
创建时间: 2025-08-27 09:02
创建人: 谢佳悦
更新记录:
- 2025-08-22 13:10 by 苏杰
- 2025-08-30 09:07 by 张宇成
- 2025-08-30 16:00 by 张宇成
"""

import sqlite3
import os

def add_user_fields():
    """添加User模型的缺失字段"""
    print("🔧 正在添加User模型的缺失字段...")
    
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
            ('department', 'TEXT'),
            ('employee_id', 'TEXT UNIQUE'),
            ('supervisor_id', 'INTEGER'),
            ('hire_date', 'DATE')
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
        
        print("✅ User模型字段添加完成")
        return True
        
    except Exception as e:
        print(f"❌ 添加字段失败: {e}")
        return False

if __name__ == "__main__":
    add_user_fields()
