from flask import Blueprint, render_template, request, redirect, url_for, session, flash, g
from ..models import User, db

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/')
def root():
    """根路径 - 重定向到登录页面"""
    return redirect(url_for('common.auth.sign'))

@auth_bp.route('/sign', methods=['GET', 'POST'])
def sign():
    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'signup':
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            company_name = request.form['company_name']
            email = request.form['email']
            phone_number = request.form['phone_number']
            birthday = request.form['birthday']
            password = request.form['password']
            confirm_password = request.form['confirm_password']
            role = request.form.get('role', 'candidate')

            if password != confirm_password:
                flash('两次输入的密码不一致。', 'danger')
                return redirect(url_for('common.auth.sign'))

            # 检查邮箱是否已存在
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                flash('该邮箱已被注册。', 'danger')
                return redirect(url_for('common.auth.sign'))

            # 创建新用户
            user = User(
                first_name=first_name,
                last_name=last_name,
                company_name=company_name,
                email=email,
                phone_number=phone_number,
                birthday=birthday,
                password=password,
                is_hr=(role == 'recruiter')
            )
            db.session.add(user)
            db.session.commit()
            flash('注册成功！现在可以登录。', 'success')
            return redirect(url_for('common.auth.sign'))

        elif action == 'signin':
            email = request.form['email']
            password = request.form['password']
            desired_role = request.form.get('role', 'candidate')
            
            user = User.query.filter_by(email=email, password=password).first()
            if user:
                # 检查角色是否匹配
                user_is_hr = getattr(user, 'is_hr', False)
                if (desired_role == 'recruiter' and not user_is_hr) or (desired_role == 'candidate' and user_is_hr):
                    flash('您选择的身份与注册时的身份不匹配。', 'danger')
                    return redirect(url_for('common.auth.sign'))
                
                session['user_id'] = user.id
                flash('登录成功！', 'success')
                # 根据角色重定向到不同页面
                if user_is_hr:
                    # HR进入仪表盘
                    return redirect(url_for('smartrecruit.hr.dashboard.hr_dashboard'))
                else:
                    # 求职者进入首页
                    return redirect(url_for('smartrecruit.candidate.home'))
            else:
                flash('邮箱或密码错误。', 'danger')

    return render_template('common/1.html')

@auth_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    session.clear()
    flash('你已退出登录。', 'success')
    return redirect(url_for('common.auth.sign'))

@auth_bp.route('/home')
def home():
    """主页 - 根据用户角色重定向"""
    if g.user is None:
        return redirect(url_for('common.auth.sign'))
    
    if getattr(g.user, 'is_hr', False):
        return redirect(url_for('smartrecruit.hr.dashboard.hr_dashboard'))
    else:
        # 求职者：显示首页
        return redirect(url_for('smartrecruit.candidate.home'))
