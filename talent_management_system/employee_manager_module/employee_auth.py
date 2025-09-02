from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.models import User, db
from datetime import datetime

employee_auth_bp = Blueprint('employee_auth', __name__, url_prefix='/employee')

@employee_auth_bp.route('/auth', methods=['GET', 'POST'])
def employee_auth():
    """员工认证（注册/登录）"""
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'signup':
            # 员工注册
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            email = request.form['email']
            password = request.form['password']
            phone_number = request.form.get('phone_number', '')
            birthday_str = request.form.get('birthday', '')
            hire_date = request.form.get('hire_date', '')
            
            # 验证必填字段
            if not all([first_name, last_name, email, password]):
                flash('请填写所有必填字段', 'danger')
                return redirect(url_for('talent_management.employee_auth.employee_auth'))
            
            # 验证邮箱格式
            if '@' not in email or '.' not in email:
                flash('请输入有效的邮箱地址', 'danger')
                return redirect(url_for('talent_management.employee_auth.employee_auth'))
            
            # 检查邮箱是否已存在
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                flash('该邮箱已被注册', 'danger')
                return redirect(url_for('talent_management.employee_auth.employee_auth'))
            
            # 处理日期字段
            birthday = None
            if birthday_str:
                try:
                    birthday = datetime.strptime(birthday_str, '%Y-%m-%d').date()
                except ValueError:
                    flash('生日日期格式错误', 'danger')
                    return redirect(url_for('talent_management.employee_auth.employee_auth'))
            
            hire_date_obj = None
            if hire_date:
                try:
                    hire_date_obj = datetime.strptime(hire_date, '%Y-%m-%d').date()
                except ValueError:
                    flash('入职日期格式错误', 'danger')
                    return redirect(url_for('talent_management.employee_auth.employee_auth'))
            
            # 创建新用户
            user = User(
                first_name=first_name,
                last_name=last_name,
                hire_date=hire_date_obj,
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
                
                # 验证用户是否成功创建
                saved_user = User.query.filter_by(email=email).first()
                if not saved_user:
                    db.session.rollback()
                    flash('注册失败，请稍后重试', 'danger')
                    return redirect(url_for('talent_management.employee_auth.employee_auth'))
                
                flash('员工注册成功！现在可以登录。', 'success')
                return redirect(url_for('talent_management.employee_auth.employee_auth'))
                
            except Exception as e:
                db.session.rollback()
                print(f"员工注册失败: {e}")
                flash('注册失败，请稍后重试。', 'danger')
                return redirect(url_for('talent_management.employee_auth.employee_auth'))
                
        elif action == 'signin':
            # 员工登录
            email = request.form.get('email', '')
            password = request.form.get('password', '')
            
            if not email or not password:
                flash('请输入邮箱和密码', 'danger')
                return redirect(url_for('talent_management.employee_auth.employee_auth'))
            
            try:
                user = User.query.filter_by(email=email, password=password, user_type='employee').first()
                if user:
                    # 设置会话
                    session['user_id'] = user.id
                    session['user_type'] = 'employee'
                    session['user_email'] = user.email
                    
                    flash('员工登录成功！', 'success')
                    # 重定向到员工仪表盘
                    return redirect(url_for('talent_management.employee_management.employee_dashboard'))
                else:
                    flash('邮箱或密码错误，或该账号不是员工账号。', 'danger')
                    return redirect(url_for('talent_management.employee_auth.employee_auth'))
            except Exception as e:
                print(f"员工登录失败: {e}")
                flash('登录失败，请稍后重试', 'danger')
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
