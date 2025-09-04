"""
LLRC Header Start
文件功能: 通用 Python 脚本/模块：database/update_interview_schedule_table.py
创建时间: 2025-08-20 11:43
创建人: 谢佳悦
更新记录:
- 2025-08-26 13:00 by 侯东杨
- 2025-08-27 17:44 by 潘显雨
LLRC Header End
"""
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FILE-HEADER-AUTO-ADDED
文件: database/update_interview_schedule_table.py
功能: 通用模块
创建时间: 2025-08-27 18:54
创建人: 侯东杨
更新记录:
- 2025-08-20 12:13 by 侯东杨
- 2025-08-26 17:36 by 潘显雨
- 2025-09-02 16:17 by 潘显雨
"""
"""
更新InterviewSchedule表，添加HR手动设置AI面试状态的字段
"""

import os
import sys

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from app import create_app, db
from sqlalchemy import text

def update_interview_schedule_table():
    """更新InterviewSchedule表结构"""
    app = create_app()
    
    with app.app_context():
        try:
            print("正在更新InterviewSchedule表...")
            
            # 检查新字段是否已存在
            result = db.session.execute(text("PRAGMA table_info(interview_schedule)"))
            columns = [row[1] for row in result.fetchall()]
            
            print(f"当前表字段: {columns}")
            
            # 添加新字段（如果不存在）
            if 'hr_ai_interview_override' not in columns:
                print("添加 hr_ai_interview_override 字段...")
                db.session.execute(text("""
                    ALTER TABLE interview_schedule 
                    ADD COLUMN hr_ai_interview_override BOOLEAN DEFAULT FALSE
                """))
                print("✓ hr_ai_interview_override 字段添加成功")
            else:
                print("✓ hr_ai_interview_override 字段已存在")
            
            if 'hr_ai_interview_notes' not in columns:
                print("添加 hr_ai_interview_notes 字段...")
                db.session.execute(text("""
                    ALTER TABLE interview_schedule 
                    ADD COLUMN hr_ai_interview_notes TEXT
                """))
                print("✓ hr_ai_interview_notes 字段添加成功")
            else:
                print("✓ hr_ai_interview_notes 字段已存在")
            
            # 提交更改
            db.session.commit()
            print("✓ 表结构更新完成")
            
            # 验证更新结果
            result = db.session.execute(text("PRAGMA table_info(interview_schedule)"))
            updated_columns = [row[1] for row in result.fetchall()]
            print(f"更新后表字段: {updated_columns}")
            
            # 检查新字段是否成功添加
            required_fields = ['hr_ai_interview_override', 'hr_ai_interview_notes']
            missing_fields = [field for field in required_fields if field not in updated_columns]
            
            if missing_fields:
                print(f"✗ 以下字段添加失败: {missing_fields}")
                return False
            else:
                print("✓ 所有新字段添加成功")
                return True
                
        except Exception as e:
            print(f"✗ 更新表结构失败: {e}")
            db.session.rollback()
            return False

def test_interview_schedule_functionality():
    """测试面试安排功能"""
    app = create_app()
    
    with app.app_context():
        try:
            print("\n正在测试面试安排功能...")
            
            # 测试查询InterviewSchedule表
            result = db.session.execute(text("SELECT COUNT(*) FROM interview_schedule"))
            count = result.fetchone()[0]
            print(f"✓ InterviewSchedule表记录数: {count}")
            
            # 测试新字段的默认值
            result = db.session.execute(text("""
                SELECT hr_ai_interview_override, hr_ai_interview_notes 
                FROM interview_schedule 
                LIMIT 1
            """))
            row = result.fetchone()
            if row:
                print(f"✓ 新字段默认值: hr_ai_interview_override={row[0]}, hr_ai_interview_notes={row[1]}")
            else:
                print("✓ 新字段默认值测试通过（表为空）")
            
            print("✓ 面试安排功能测试完成")
            return True
            
        except Exception as e:
            print(f"✗ 功能测试失败: {e}")
            return False

if __name__ == '__main__':
    print("=" * 60)
    print("InterviewSchedule表更新脚本")
    print("=" * 60)
    
    # 更新表结构
    if update_interview_schedule_table():
        print("\n" + "=" * 40)
        print("表结构更新成功！")
        print("=" * 40)
        
        # 测试功能
        if test_interview_schedule_functionality():
            print("\n🎉 所有操作完成！")
            print("\n新增功能说明:")
            print("1. hr_ai_interview_override: HR手动设置的AI面试状态开关")
            print("2. hr_ai_interview_notes: HR设置AI面试状态的备注信息")
            print("3. 支持HR手动覆盖系统自动检测的AI面试结果")
        else:
            print("\n⚠️  表结构更新成功，但功能测试失败")
    else:
        print("\n❌ 表结构更新失败")
        sys.exit(1)



