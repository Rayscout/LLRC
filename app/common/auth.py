from flask import Blueprint, render_template, request, redirect, url_for, session, flash, g
from ..models import User, db
from datetime import datetime

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
            role = request.form.get('role')
            
            # 验证是否选择了角色
            if not role:
                flash('请选择注册身份。', 'danger')
                return redirect(url_for('common.auth.sign'))

            if password != confirm_password:
                flash('两次输入的密码不一致。', 'danger')
                return redirect(url_for('common.auth.sign'))

            # 检查邮箱是否已存在
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                flash('该邮箱已被注册。', 'danger')
                return redirect(url_for('common.auth.sign'))

            # 根据角色创建用户
            if role in ['executive', 'employee']:
                # 高管和员工需要额外字段
                department = request.form.get('department', '')
                position = request.form.get('position', '')
                
                if role == 'employee':
                    # 员工需要更多字段
                    employee_id = request.form.get('employee_id', '')
                    supervisor_email = request.form.get('supervisor_email', '')
                    hire_date = request.form.get('hire_date', '')
                    
                    if not all([employee_id, supervisor_email, hire_date]):
                        flash('员工注册需要填写所有必填字段。', 'danger')
                        return redirect(url_for('common.auth.sign'))
                    
                    # 查找高管
                    supervisor = User.query.filter_by(email=supervisor_email, user_type='executive').first()
                    if not supervisor:
                        flash('未找到指定的高管，请检查高管邮箱是否正确。', 'danger')
                        return redirect(url_for('common.auth.sign'))
                    
                    # 检查员工编号是否已存在
                    existing_employee = User.query.filter_by(employee_id=employee_id).first()
                    if existing_employee:
                        flash('该员工编号已被使用。', 'danger')
                        return redirect(url_for('common.auth.sign'))
                    
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
                else:
                    # 高管
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
            else:
                # 求职者和招聘者（HR）
                user = User(
                    first_name=first_name,
                    last_name=last_name,
                    company_name=company_name,
                    email=email,
                    phone_number=phone_number,
                    birthday=birthday,
                    password=password,
                    is_hr=(role == 'recruiter'),
                    user_type=role
                )
            
            db.session.add(user)
            db.session.commit()
            flash('注册成功！现在可以登录。', 'success')
            return redirect(url_for('common.auth.sign'))

        elif action == 'signin':
            email = request.form['email']
            password = request.form['password']
            desired_role = request.form.get('role')
            
            # 验证是否选择了角色
            if not desired_role:
                flash('请选择登录身份。', 'danger')
                return redirect(url_for('common.auth.sign'))
            
            user = User.query.filter_by(email=email, password=password).first()
            if user:
                # 检查用户是否有user_type字段，如果没有则设置默认值
                if not hasattr(user, 'user_type') or user.user_type is None:
                    # 根据is_hr字段设置默认用户类型
                    if user.is_hr:
                        user.user_type = 'supervisor'
                    else:
                        user.user_type = 'candidate'
                    db.session.commit()
                
                # 严格检查角色是否匹配
                if user.user_type != desired_role:
                    flash(f'您选择的身份（{desired_role}）与注册时的身份（{user.user_type}）不匹配。请选择正确的身份登录。', 'danger')
                    return redirect(url_for('common.auth.sign'))
                
                session['user_id'] = user.id
                session['user_type'] = user.user_type
                flash(f'登录成功！欢迎回来，{user.first_name}！', 'success')
                
                # 根据角色重定向到不同页面
                if user.user_type == 'executive':
                    return redirect(url_for('talent_management.hr_admin.executive_dashboard'))
                elif user.user_type == 'employee':
                    return redirect(url_for('talent_management.employee_management.employee_dashboard'))
                elif user.user_type == 'recruiter' or user.is_hr:
                    return redirect(url_for('smartrecruit.hr.dashboard.hr_dashboard'))
                else:
                    return redirect(url_for('smartrecruit.candidate.home'))
            else:
                flash('邮箱或密码错误。', 'danger')

    # 按你的要求使用简化版首页（无需模板），保证稳定可用
    return (
        """
        <!doctype html>
        <meta charset="utf-8" />
        <title>登录 / 注册</title>
        <div style="max-width:520px;margin:48px auto;font-family:Arial,sans-serif">
          <h2 style="margin-bottom:12px">智能招聘系统 · 简化版</h2>
          <p style="color:#555;margin:0 0 16px">请选择登录身份并输入邮箱与密码。</p>
          <form method="post" action="/auth/sign" style="padding:16px;border:1px solid #e5e7eb;border-radius:10px;background:#fff">
            <input type="hidden" name="action" value="signin" />
            <div style="margin:10px 0">
              <label>邮箱</label><br/>
              <input name="email" type="email" required style="width:100%;padding:10px;border:1px solid #ddd;border-radius:8px" />
            </div>
            <div style="margin:10px 0">
              <label>密码</label><br/>
              <input name="password" type="password" required style="width:100%;padding:10px;border:1px solid #ddd;border-radius:8px" />
            </div>
            <div style="margin:10px 0">
              <label>以身份登录</label><br/>
              <label style="margin-right:10px"><input type="radio" name="role" value="candidate" required /> 求职者</label>
              <label style="margin-right:10px"><input type="radio" name="role" value="recruiter" /> HR</label>
              <label style="margin-right:10px"><input type="radio" name="role" value="executive" /> 高管</label>
              <label style="margin-right:10px"><input type="radio" name="role" value="employee" /> 员工</label>
            </div>
            <button type="submit" style="width:100%;padding:12px;border:none;border-radius:8px;background:#2563eb;color:#fff">登录</button>
          </form>

          <details style="margin-top:16px">
            <summary>没有账号？点此注册</summary>
            <form method="post" action="/auth/sign" style="margin-top:12px;padding:16px;border:1px solid #e5e7eb;border-radius:10px;background:#fff">
              <input type="hidden" name="action" value="signup" />
              <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px">
                <div><label>名</label><br/><input name="first_name" required style="width:100%;padding:10px;border:1px solid #ddd;border-radius:8px" /></div>
                <div><label>姓</label><br/><input name="last_name" required style="width:100%;padding:10px;border:1px solid #ddd;border-radius:8px" /></div>
              </div>
              <div style="margin-top:10px"><label>公司名称</label><br/><input name="company_name" required style="width:100%;padding:10px;border:1px solid #ddd;border-radius:8px" /></div>
              <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:10px">
                <div><label>手机号</label><br/><input name="phone_number" required style="width:100%;padding:10px;border:1px solid #ddd;border-radius:8px" /></div>
                <div><label>生日</label><br/><input name="birthday" type="date" required style="width:100%;padding:10px;border:1px solid #ddd;border-radius:8px" /></div>
              </div>
              <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:10px">
                <div><label>密码</label><br/><input name="password" type="password" required style="width:100%;padding:10px;border:1px solid #ddd;border-radius:8px" /></div>
                <div><label>确认密码</label><br/><input name="confirm_password" type="password" required style="width:100%;padding:10px;border:1px solid #ddd;border-radius:8px" /></div>
              </div>
              <div style="margin-top:10px">
                <label>注册身份</label><br/>
                <label style="margin-right:10px"><input type="radio" name="role" value="candidate" required /> 求职者</label>
                <label style="margin-right:10px"><input type="radio" name="role" value="recruiter" /> HR</label>
                <label style="margin-right:10px"><input type="radio" name="role" value="executive" /> 高管</label>
                <label style="margin-right:10px"><input type="radio" name="role" value="employee" /> 员工</label>
              </div>
              <button type="submit" style="width:100%;margin-top:12px;padding:12px;border:none;border-radius:8px;background:#059669;color:#fff">注册</button>
            </form>
          </details>
        </div>
        """,
        200,
        {"Content-Type": "text/html; charset=utf-8"},
    )

@auth_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('user_type', None)
    session.clear()
    flash('你已退出登录。', 'success')
    return redirect(url_for('common.auth.sign'))

@auth_bp.route('/home')
def home():
    """主页 - 根据用户角色重定向"""
    if g.user is None:
        return redirect(url_for('common.auth.sign'))
    
    user_type = session.get('user_type')
    if user_type == 'executive':
        return redirect(url_for('talent_management.hr_admin.executive_dashboard'))
    elif user_type == 'employee':
        return redirect(url_for('talent_management.employee_management.employee_dashboard'))
    elif user_type == 'recruiter' or (hasattr(g.user, 'is_hr') and g.user.is_hr):
        return redirect(url_for('smartrecruit.hr.dashboard.hr_dashboard'))
    else:
        return redirect(url_for('smartrecruit.candidate.home'))
