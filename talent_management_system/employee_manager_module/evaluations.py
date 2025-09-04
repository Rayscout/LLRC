"""
LLRC Header Start
文件功能: 人才管理子系统 Python 模块：talent_management_system/employee_manager_module/evaluations.py
创建时间: 2025-08-23 09:05
创建人: 苏杰
更新记录:
- 2025-08-27 10:26 by 谢佳悦
- 2025-09-03 16:26 by 李雨梦
LLRC Header End
"""
"""
FILE-HEADER-AUTO-ADDED
文件: talent_management_system/employee_manager_module/evaluations.py
功能: 通用模块
创建时间: 2025-08-20 16:23
创建人: 张宇成
更新记录:
- 2025-08-23 09:35 by 侯东杨
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from app.models import User, TaskEvaluation


evaluations_bp = Blueprint('evaluations', __name__, url_prefix='/evaluations')


@evaluations_bp.route('/')
def list():
	"""函数 list：核心业务逻辑。"""
	try:
		if 'user_id' not in session:
			flash('请先登录', 'warning')
			return redirect(url_for('common.auth.sign'))
		user = User.query.get(session['user_id'])
		if not user or user.user_type != 'employee':
			flash('用户信息获取失败', 'warning')
			return redirect(url_for('common.auth.sign'))

		# 支持按日期/总分筛选（简化）
		records = TaskEvaluation.query.filter_by(employee_id=user.id)\
			.order_by(TaskEvaluation.created_at.desc()).all()

		return render_template(
			'talent_management/employee_management/evaluations_list.html',
			user=user,
			records=records
		)
	except Exception as e:
		flash(f'加载绩效评价时发生错误: {str(e)}', 'danger')
		return redirect(url_for('talent_management.employee_management.employee_dashboard'))


@evaluations_bp.route('/view/<int:eval_id>')
def view(eval_id):
	"""函数 view：处理 eval_id 相关逻辑。"""
	try:
		if 'user_id' not in session:
			flash('请先登录', 'warning')
			return redirect(url_for('common.auth.sign'))
		user = User.query.get(session['user_id'])
		if not user or user.user_type != 'employee':
			flash('用户信息获取失败', 'warning')
			return redirect(url_for('common.auth.sign'))

		record = TaskEvaluation.query.get(eval_id)
		if not record or record.employee_id != user.id:
			flash('您无权查看该评价', 'warning')
			return redirect(url_for('talent_management.employee_management.evaluations.list'))

		return render_template(
			'talent_management/employee_management/evaluations_view.html',
			user=user,
			record=record
		)
	except Exception as e:
		flash(f'查看绩效评价时发生错误: {str(e)}', 'danger')
		return redirect(url_for('talent_management.employee_management.evaluations.list'))

