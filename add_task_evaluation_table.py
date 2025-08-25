#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
添加任务绩效评价数据表
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import TaskEvaluation


def add_task_evaluation_table():
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
