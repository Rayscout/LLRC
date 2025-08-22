#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化的Flask启动脚本，避免复杂的导入问题
"""

from flask import Flask, render_template, redirect, url_for, request, session, flash, g
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
import os
from datetime import datetime

# 创建Flask应用
app = Flask(__name__)
app.config['SECRET_KEY'] = 'TESTINGCHEATS123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 初始化数据库
db = SQLAlchemy(app)

# 简化的用户模型
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    company_name = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    birthday = db.Column(db.String(10), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    is_hr = db.Column(db.Boolean, default=False)

# 简化的职位模型
class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    company_name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    salary = db.Column(db.String(50), nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# 简化的申请模型
class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='Pending')

# 创建数据库表
with app.app_context():
    db.create_all()
    
    # 检查是否已存在HR用户，如果不存在则创建
    hr_user = User.query.filter_by(email='hr@smartrecruit.com').first()
    if not hr_user:
        hr_user = User(
            first_name="张",
            last_name="HR",
            company_name="智能招聘科技有限公司",
            position="人力资源总监",
            email="hr@smartrecruit.com",
            phone_number="13800138000",
            birthday="1985-06-15",
            password=generate_password_hash("hr123456"),
            is_hr=True
        )
        db.session.add(hr_user)
        db.session.commit()
        print("✅ 已创建HR用户账户")

# 根路径 - 重定向到登录页面
@app.route('/')
def root():
    return redirect(url_for('sign'))

# 登录页面
@app.route('/sign', methods=['GET', 'POST'])
def sign():
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'signin':
            email = request.form['email']
            password = request.form['password']
            desired_role = request.form.get('role', 'candidate')
            
            user = User.query.filter_by(email=email).first()
            
            if user and check_password_hash(user.password, password):
                user_is_hr = getattr(user, 'is_hr', False)
                
                if (desired_role == 'recruiter' and not user_is_hr) or (desired_role == 'candidate' and user_is_hr):
                    flash('您选择的身份与注册时的身份不匹配。', 'danger')
                    return redirect(url_for('sign'))
                
                session['user_id'] = user.id
                flash('登录成功！', 'success')
                
                if user_is_hr:
                    return redirect(url_for('hr_dashboard'))
                else:
                    return redirect(url_for('candidate_dashboard'))
            else:
                flash('邮箱或密码错误。', 'danger')
        
        elif action == 'signup':
            # 简化的注册逻辑
            flash('注册功能暂未实现，请使用现有账户登录', 'info')
    
    return render_template('common/sign.html')

# HR仪表板
@app.route('/hr_dashboard')
def hr_dashboard():
    if 'user_id' not in session:
        flash('请先登录。', 'danger')
        return redirect(url_for('sign'))
    
    user = User.query.get(session['user_id'])
    if not user or not user.is_hr:
        flash('只有HR用户才能访问此页面。', 'danger')
        return redirect(url_for('sign'))
    
    # 获取统计数据
    total_candidates = User.query.filter_by(is_hr=False).count()
    total_jobs = Job.query.filter_by(user_id=user.id).count()
    
    return render_template('smartrecruit/hr/hr_dashboard.html',
                         total_candidates=total_candidates,
                         total_jobs=total_jobs)

# 候选人仪表板
@app.route('/candidate_dashboard')
def candidate_dashboard():
    if 'user_id' not in session:
        flash('请先登录。', 'danger')
        return redirect(url_for('sign'))
    
    user = User.query.get(session['user_id'])
    if user and user.is_hr:
        flash('只有求职者才能访问此页面。', 'danger')
        return redirect(url_for('sign'))
    
    return "候选人仪表板 - 功能开发中..."

# 登出
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.clear()
    flash('你已退出登录。', 'success')
    return redirect(url_for('sign'))

if __name__ == '__main__':
    print("🚀 启动简化的Flask应用...")
    print("📧 HR账户: hr@smartrecruit.com")
    print("🔑 密码: hr123456")
    print("🌐 访问: http://127.0.0.1:5000")
    
    app.run(host='127.0.0.1', port=5000, debug=True)
