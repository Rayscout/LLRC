"""
LLRC Header Start
文件功能: 人才管理子系统 Python 模块：talent_management_system/tools/add_task_evaluation_table.py
创建时间: 2025-08-25 09:52
创建人: 张宇成
更新记录:
- 2025-08-27 13:59 by 张宇成
- 2025-08-29 10:56 by 苏杰
LLRC Header End
"""
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FILE-HEADER-AUTO-ADDED
文件: talent_management_system/tools/add_task_evaluation_table.py
功能: 通用模块
创建时间: 2025-08-27 16:00
创建人: 侯东杨
更新记录:
- 2025-08-25 10:22 by 潘显雨
"""
"""
添加任务绩效评价数据表
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app import create_app, db
from app.models import TaskEvaluation


def add_task_evaluation_table():
	"""函数 add_task_evaluation_table：核心业务逻辑。"""
	app = create_app()
	with app.app_context():
		try:
			print('开始创建 task_evaluation 表...')
			db.create_all()
			from sqlalchemy import inspect
			inspector = inspect(db.engine)
			if 'task_evaluation' in inspector.get_table_names():
				print('✅ task_evaluation 表创建成功')
				return True
			else:
				print('❌ 表创建失败')
				return False
		except Exception as e:
			print(f'❌ 迁移失败: {e}')
			return False


if __name__ == '__main__':
	success = add_task_evaluation_table()
	if success:
		print('\n🎉 任务绩效评价表创建完成！')
	else:
		print('\n💥 任务绩效评价表创建失败！')
		sys.exit(1)

