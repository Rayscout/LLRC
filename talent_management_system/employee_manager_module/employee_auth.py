from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.models import User, db
from datetime import datetime

employee_auth_bp = Blueprint('employee_auth', __name__, url_prefix='/employee')

@employee_auth_bp.route('/auth', methods=['GET', 'POST'])
def employee_auth():
    """员工登录和注册"""
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'signup':
            # 员工注册
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            company_name = request.form['company_name']
            department = request.form['department']
            position = request.form['position']
            employee_id = request.form['employee_id']
            supervisor_email = request.form['supervisor_email']
            hire_date = request.form['hire_date']
            email = request.form['email']
            phone_number = request.form['phone_number']
            birthday = request.form['birthday']
            password = request.form['password']
            confirm_password = request.form['confirm_password']
            
            if password != confirm_password:
                flash('两次输入的密码不一致。', 'danger')
                return redirect(url_for('talent_management.employee_auth.employee_auth'))
            
            # 检查邮箱是否已存在
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                flash('该邮箱已被注册。', 'danger')
                return redirect(url_for('talent_management.employee_auth.employee_auth'))
            
            # 检查员工编号是否已存在
            existing_employee = User.query.filter_by(employee_id=employee_id).first()
            if existing_employee:
                flash('该员工编号已被使用。', 'danger')
                return redirect(url_for('talent_management.employee_auth.employee_auth'))
            
            # 查找高管
            supervisor = User.query.filter_by(email=supervisor_email, user_type='executive').first()
            if not supervisor:
                flash('未找到指定的高管，请检查高管邮箱是否正确。', 'danger')
                return redirect(url_for('talent_management.employee_auth.employee_auth'))
            
            # 创建新员工用户
            user = User(
                first_name=first_name,
                last_name=last_name,
                company_name=company_name,
                department=department,
                position=position,
                employee_id=employee_id,
                supervisor_id=supervisor.id,
                hire_date=datetime.strptime(hire_date, '%Y-%m-%d').date(),
                email=email,
                phone_number=phone_number,
                birthday=birthday,
                password=password,
                user_type='employee',
                is_hr=False
            )
            
            try:
                db.session.add(user)
                db.session.commit()
                flash('员工注册成功！现在可以登录。', 'success')
                return redirect(url_for('talent_management.employee_auth.employee_auth'))
            except Exception as e:
                db.session.rollback()
                flash('注册失败，请稍后重试。', 'danger')
                return redirect(url_for('talent_management.employee_auth.employee_auth'))
                
        elif action == 'signin':
            # 员工登录
            email = request.form['email']
            password = request.form['password']
            
            user = User.query.filter_by(email=email, password=password, user_type='employee').first()
            if user:
                session['user_id'] = user.id
                session['user_type'] = 'employee'
                flash('员工登录成功！', 'success')
                # 重定向到员工仪表盘
                return redirect(url_for('talent_management.employee_management.employee_dashboard'))
            else:
                flash('邮箱或密码错误，或该账号不是员工账号。', 'danger')
                return redirect(url_for('talent_management.employee_auth.employee_auth'))
    
    # GET请求显示登录页面
    return render_template('talent_management/employee_management/employee_auth.html')

@employee_auth_bp.route('/dashboard')
def employee_dashboard():
    """员工仪表盘"""
    if 'user_id' not in session or session.get('user_type') != 'employee':
        flash('请先登录员工账号。', 'danger')
        return redirect(url_for('talent_management.employee_auth.employee_auth'))
    
    user = User.query.get(session['user_id'])
    if not user or user.user_type != 'employee':
        session.clear()
        flash('账号验证失败，请重新登录。', 'danger')
        return redirect(url_for('talent_management.employee_auth.employee_auth'))
    
    # 获取主管信息
    supervisor = None
    if user.supervisor_id:
        supervisor = User.query.get(user.supervisor_id)

    # 获取任务完成情况
    try:
        from app.models import SmartGoal
        smart_goals = SmartGoal.query.filter_by(user_id=user.id).all()
        completed_tasks = len([goal for goal in smart_goals if goal.status == 'completed'])
        total_tasks = len(smart_goals)

        task_completion = {
            'completed': completed_tasks,
            'total': total_tasks
        }
    except Exception as e:
        print(f"获取任务完成情况失败: {e}")
        task_completion = {
            'completed': 0,
            'total': 0
        }

    # 计算综合评分
    overall_score = 0
    try:
        if total_tasks > 0:
            # 基于任务完成率计算评分
            completion_rate = completed_tasks / total_tasks
            overall_score = min(100, completion_rate * 80 + 20)  # 基础分20分，完成率占80分
        else:
            overall_score = 20  # 没有任务时的基础分
    except Exception as e:
        print(f"计算综合评分失败: {e}")
        overall_score = 0

    # 模拟数据用于展示界面效果
    dashboard_data = {
        'profile_completeness': 85,
        'performance_score': 92,
        'project_count': 5,
        'learning_progress': 78,
        'skills_count': 12,
        'task_completion': task_completion,
        'overall_score': overall_score
    }

    return render_template('talent_management/employee_management/employee_dashboard.html',
                         user=user, supervisor=supervisor, **dashboard_data)

@employee_auth_bp.route('/logout')
def employee_logout():
    """员工退出登录 - 重定向到通用退出登录"""
    return redirect(url_for('common.auth.logout'))
