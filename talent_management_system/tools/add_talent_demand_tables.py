#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创建人才需求相关新表（如果不存在）。
安全：不会删除任何现有数据，仅在缺表时创建。
使用方式：
  python -m talent_management_system.tools.add_talent_demand_tables
"""

import os
import sys

# 将项目根目录加入路径
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, '..', '..'))
sys.path.insert(0, PROJECT_ROOT)

def main():
    from app import create_app, db
    # 导入模型以确保元数据包含新表
    from app.models import TalentDemand, TalentDemandNotification, TalentDemandDraft  # noqa: F401
    from sqlalchemy import text

    app = create_app()
    with app.app_context():
        print('Checking and creating talent demand tables if missing...')
        # 列出现有表
        existing = set()
        try:
            rows = db.session.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))
            existing = {r[0] for r in rows}
        except Exception:
            pass
        print(f'Existing tables: {sorted(existing)}')

        # 创建缺失表
        db.create_all()  # 安全：仅创建缺失表

        # 再次列出以确认
        rows = db.session.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))
        now_tables = sorted({r[0] for r in rows})
        print(f'Create-all done. Current tables: {now_tables}')
        if 'talent_demand' in now_tables and 'talent_demand_notification' in now_tables:
            print('Talent demand tables are ready.')
        else:
            print('Target tables not found. Please check models or DB config.')

if __name__ == '__main__':
    main()


