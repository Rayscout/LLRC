#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
高管任务绩效评价模块
"""

from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for, flash
from app.models import User, TaskEvaluation, db
from datetime import datetime

# 调整到反馈系统下的子路径
task_evaluation_bp = Blueprint('task_evaluation', __name__, url_prefix='/feedback_system/evaluation')


def require_exec_login():
    if 'user_id' not in session:
        return False, (jsonify({'error': '请先登录'}), 401)
    user = User.query.get(session['user_id'])
    if not user or user.user_type not in ['executive', 'supervisor']:
        return False, (jsonify({'error': '权限不足'}), 403)
    return True, user


def get_team_members(executive_id):
    user = User.query.get(executive_id)
    if not user:
        return {}
    if user.user_type == 'executive':
        members = User.query.filter(User.user_type == 'employee').all()
    else:
        members = User.query.filter(User.supervisor_id == executive_id, User.user_type == 'employee').all()
    return members


@task_evaluation_bp.route('/dashboard')
def evaluation_dashboard():
    ok, val = require_exec_login()
    if not ok:
        return val
    user = val

    # 最近评价记录
    recent_evals = TaskEvaluation.query.filter_by(evaluator_id=user.id)\
        .order_by(TaskEvaluation.created_at.desc()).limit(10).all()

    # 团队成员
    members = get_team_members(user.id)

    return render_template(
        'talent_management/hr_admin/task_evaluation_dashboard.html',
        user=user,
        members=members,
        recent_evals=recent_evals
    )


@task_evaluation_bp.route('/new', methods=['GET', 'POST'])
def create_evaluation():
    ok, val = require_exec_login()
    if not ok:
        return val
    user = val

    if request.method == 'POST':
        try:
            employee_id = int(request.form.get('employee_id'))
            task_title = request.form.get('task_title')
            task_description = request.form.get('task_description', '')
            score_quality = int(request.form.get('score_quality'))
            score_efficiency = int(request.form.get('score_efficiency'))
            score_collaboration = int(request.form.get('score_collaboration'))
            comment = request.form.get('comment', '')

            employee = User.query.get(employee_id)
            if not employee or employee.user_type != 'employee':
                flash('选择的员工无效', 'error')
                return redirect(url_for('talent_management.hr_admin.task_evaluation.create_evaluation'))

            # 简单总分（后续可按权重）
            total_score = score_quality + score_efficiency + score_collaboration

            eval_record = TaskEvaluation(
                evaluator_id=user.id,
                employee_id=employee_id,
                task_title=task_title,
                task_description=task_description,
                department=employee.department,
                score_quality=score_quality,
                score_efficiency=score_efficiency,
                score_collaboration=score_collaboration,
                total_score=total_score,
                comment=comment
            )
            db.session.add(eval_record)
            db.session.commit()

            flash('绩效评价已提交', 'success')
            return redirect(url_for('talent_management.hr_admin.task_evaluation.evaluation_history'))
        except Exception as e:
            db.session.rollback()
            flash(f'提交失败: {str(e)}', 'error')
            return redirect(url_for('talent_management.hr_admin.task_evaluation.create_evaluation'))

    members = get_team_members(user.id)
    return render_template(
        'talent_management/hr_admin/task_evaluation_new.html',
        user=user,
        members=members
    )


@task_evaluation_bp.route('/history')
def evaluation_history():
    ok, val = require_exec_login()
    if not ok:
        return val
    user = val

    # 支持按员工、部门、日期筛选
    employee_id = request.args.get('employee_id')
    department = request.args.get('department')
    date = request.args.get('date')

    query = TaskEvaluation.query.filter_by(evaluator_id=user.id)
    if employee_id:
        query = query.filter_by(employee_id=employee_id)
    if department:
        query = query.filter_by(department=department)
    if date:
        try:
            from datetime import datetime, timedelta
            s = datetime.strptime(date, '%Y-%m-%d')
            e = s + timedelta(days=1)
            query = query.filter(TaskEvaluation.created_at >= s, TaskEvaluation.created_at < e)
        except Exception:
            pass

    records = query.order_by(TaskEvaluation.created_at.desc()).all()

    members = get_team_members(user.id)
    return render_template(
        'talent_management/hr_admin/task_evaluation_history.html',
        user=user,
        members=members,
        records=records,
        employee_id=employee_id or '',
        department=department or '',
        date=date or ''
    )
