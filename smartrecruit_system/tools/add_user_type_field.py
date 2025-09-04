"""
LLRC Header Start
文件功能: SmartRecruit 子系统 Python 模块：smartrecruit_system/tools/add_user_type_field.py
创建时间: 2025-08-20 12:06
创建人: 潘显雨
更新记录:
- 2025-08-20 12:36 by 侯东杨
LLRC Header End
"""
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FILE-HEADER-AUTO-ADDED
文件: smartrecruit_system/tools/add_user_type_field.py
功能: 通用模块
创建时间: 2025-08-28 13:05
创建人: 潘显雨
更新记录:
- 2025-08-21 09:13 by 潘显雨
- 2025-08-23 09:25 by 苏杰
- 2025-08-25 15:41 by 侯东杨
"""

import sqlite3
import os

def add_user_type_field():
    """添加user_type字段到User表"""
    print("🔧 正在添加user_type字段到User表...")
    
    # 数据库路径
    db_path = 'instance/site.db'
    
    if not os.path.exists(db_path):
        print(f"❌ 数据库文件不存在: {db_path}")
        return False
    
    try:
        # 连接数据库
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 检查字段是否已存在
        cursor.execute("PRAGMA table_info(user)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'user_type' in columns:
            print("ℹ️ user_type字段已存在")
            conn.close()
            return True
        
        # 添加user_type字段
        cursor.execute("ALTER TABLE user ADD COLUMN user_type TEXT DEFAULT 'candidate'")
        
        # 更新现有用户的user_type
        # 根据is_hr字段设置用户类型
        cursor.execute("UPDATE user SET user_type = 'supervisor' WHERE is_hr = 1")
        cursor.execute("UPDATE user SET user_type = 'candidate' WHERE is_hr = 0")
        
        # 提交更改
        conn.commit()
        conn.close()
        
        print("✅ user_type字段添加成功")
        return True
        
    except Exception as e:
        print(f"❌ 添加字段失败: {e}")
        return False

if __name__ == "__main__":
    add_user_type_field()
