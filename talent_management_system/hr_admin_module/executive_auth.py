from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.models import User, db
from datetime import datetime

executive_auth_bp = Blueprint('executive_auth', __name__, url_prefix='/executive')

@executive_auth_bp.route('/auth', methods=['GET', 'POST'])
def executive_auth():
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'signup':
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            company_name = request.form['company_name']
            department = request.form['department']
            position = request.form['position']
            email = request.form['email']
            phone_number = request.form['phone_number']
            birthday = request.form['birthday']
            password = request.form['password']
            
            # 检查邮箱是否已存在
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                flash('该邮箱已被注册。', 'danger')
                return redirect(url_for('talent_management.executive_auth.executive_auth'))
            
            # 创建高管用户
            user = User(
                first_name=first_name,
                last_name=last_name,
                company_name=company_name,
                department=department,
                position=position,
                email=email,
                phone_number=phone_number,
                birthday=birthday,
                password=password,
                user_type='executive',
                is_hr=False
            )
            
            db.session.add(user)
            db.session.commit()
            flash('高管注册成功！现在可以登录。', 'success')
            return redirect(url_for('talent_management.executive_auth.executive_auth'))
            
        elif action == 'signin':
            email = request.form['email']
            password = request.form['password']
            
            user = User.query.filter_by(email=email, password=password, user_type='executive').first()
            if user:
                session['user_id'] = user.id
                session['user_type'] = 'executive'
                flash('登录成功！', 'success')
                return redirect(url_for('talent_management.hr_admin.executive_dashboard'))
            else:
                flash('邮箱或密码错误，或您不是高管用户。', 'danger')
    
    return render_template('talent_management/hr_admin/executive_auth.html')

@executive_auth_bp.route('/dashboard')
def executive_dashboard():
    if 'user_id' not in session or session.get('user_type') != 'executive':
        flash('请先登录高管账户。', 'danger')
        return redirect(url_for('talent_management.executive_auth.executive_auth'))
    
    user = User.query.get(session['user_id'])
    if not user or user.user_type != 'executive':
        flash('权限不足。', 'danger')
        return redirect(url_for('talent_management.executive_auth.executive_auth'))
    
    # 获取下属员工
    subordinates = User.query.filter_by(supervisor_id=user.id, user_type='employee').all()
    
    return render_template('talent_management/hr_admin/executive_dashboard.html', 
                         user=user, subordinates=subordinates)

@executive_auth_bp.route('/logout')
def executive_logout():
    session.pop('user_id', None)
    session.pop('user_type', None)
    flash('您已退出登录。', 'success')
    return redirect(url_for('talent_management.executive_auth.executive_auth'))
