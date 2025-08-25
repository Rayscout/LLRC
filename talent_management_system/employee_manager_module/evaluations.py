from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from app.models import User, TaskEvaluation


evaluations_bp = Blueprint('evaluations', __name__, url_prefix='/evaluations')


@evaluations_bp.route('/')
def list():
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
