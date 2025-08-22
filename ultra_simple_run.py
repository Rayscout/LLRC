#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
超简化的Flask启动脚本，完全独立，不依赖任何外部文件
"""

from flask import Flask, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
import os

# 创建Flask应用
app = Flask(__name__)
app.config['SECRET_KEY'] = 'TESTINGCHEATS123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ultra_simple.db'
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

# 登录页面HTML模板
LOGIN_HTML = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HR招聘系统 - 登录</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .container {
            background: white;
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            width: 100%;
            max-width: 400px;
        }
        .logo {
            text-align: center;
            margin-bottom: 30px;
        }
        .logo h1 {
            color: #333;
            font-size: 28px;
            margin-bottom: 10px;
        }
        .logo p {
            color: #666;
            font-size: 16px;
        }
        .form-group {
            margin-bottom: 20px;
        }
        .form-group label {
            display: block;
            margin-bottom: 8px;
            color: #333;
            font-weight: 500;
        }
        .form-group input, .form-group select {
            width: 100%;
            padding: 12px 16px;
            border: 2px solid #e1e5e9;
            border-radius: 10px;
            font-size: 16px;
            transition: border-color 0.3s;
        }
        .form-group input:focus, .form-group select:focus {
            outline: none;
            border-color: #667eea;
        }
        .btn {
            width: 100%;
            padding: 14px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s;
        }
        .btn:hover {
            transform: translateY(-2px);
        }
        .alert {
            padding: 12px 16px;
            border-radius: 8px;
            margin-bottom: 20px;
            font-size: 14px;
        }
        .alert-success { background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
        .alert-danger { background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
        .alert-info { background: #d1ecf1; color: #0c5460; border: 1px solid #bee5eb; }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">
            <h1>🚀 HR招聘系统</h1>
            <p>智能招聘管理平台</p>
        </div>
        
        {flash_messages}
        
        <form method="POST" action="/sign">
            <div class="form-group">
                <label for="email">邮箱地址</label>
                <input type="email" id="email" name="email" value="{email}" required>
            </div>
            
            <div class="form-group">
                <label for="password">密码</label>
                <input type="password" id="password" name="password" required>
            </div>
            
            <div class="form-group">
                <label for="role">身份选择</label>
                <select id="role" name="role" required>
                    <option value="recruiter" {recruiter_selected}>招聘者/HR</option>
                    <option value="candidate" {candidate_selected}>求职者</option>
                </select>
            </div>
            
            <button type="submit" name="action" value="signin" class="btn">登录</button>
        </form>
        
        <div style="text-align: center; margin-top: 20px; color: #666;">
            <p>测试账户：hr@smartrecruit.com / hr123456</p>
        </div>
    </div>
</body>
</html>
"""

# HR仪表板HTML模板
HR_DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HR招聘仪表板</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f8fafc;
            color: #333;
        }
        .header {
            background: white;
            padding: 20px 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .header-content {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .header h1 {
            color: #2d3748;
            font-size: 24px;
        }
        .logout-btn {
            background: #e53e3e;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            text-decoration: none;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .metric-card {
            background: white;
            padding: 24px;
            border-radius: 12px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            text-align: center;
        }
        .metric-value {
            font-size: 36px;
            font-weight: bold;
            color: #667eea;
            margin-bottom: 8px;
        }
        .metric-label {
            color: #718096;
            font-size: 14px;
        }
        .dashboard-section {
            background: white;
            padding: 24px;
            border-radius: 12px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        .section-title {
            font-size: 20px;
            font-weight: 600;
            margin-bottom: 20px;
            color: #2d3748;
        }
        .quick-actions {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 16px;
        }
        .action-card {
            background: #f7fafc;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            text-decoration: none;
            color: #4a5568;
            transition: transform 0.2s;
        }
        .action-card:hover {
            transform: translateY(-2px);
            background: #edf2f7;
        }
        .action-icon {
            font-size: 24px;
            margin-bottom: 12px;
        }
    </style>
</head>
<body>
    <div class="header">
        <div class="header-content">
            <h1>🎯 HR招聘仪表板</h1>
            <a href="/logout" class="logout-btn">退出登录</a>
        </div>
    </div>
    
    <div class="container">
        <div class="metrics-grid">
            <div class="metric-card">
                <div class="metric-value">{total_candidates}</div>
                <div class="metric-label">总候选人</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{total_jobs}</div>
                <div class="metric-label">发布职位</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">23</div>
                <div class="metric-label">面试安排</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">8</div>
                <div class="metric-label">录用通知</div>
            </div>
        </div>
        
        <div class="dashboard-section">
            <h2 class="section-title">📊 招聘阶段漏斗</h2>
            <div style="text-align: center; color: #718096;">
                <p>已申请: 156 → 已筛选: 89 → 已面试: 45 → 已录用: 12</p>
            </div>
        </div>
        
        <div class="dashboard-section">
            <h2 class="section-title">⚡ 快速操作</h2>
            <div class="quick-actions">
                <a href="#" class="action-card">
                    <div class="action-icon">➕</div>
                    <div>创建职位</div>
                </a>
                <a href="#" class="action-card">
                    <div class="action-icon">👥</div>
                    <div>查看候选人</div>
                </a>
                <a href="#" class="action-card">
                    <div class="action-icon">📅</div>
                    <div>面试管理</div>
                </a>
                <a href="#" class="action-card">
                    <div class="action-icon">📊</div>
                    <div>招聘报告</div>
                </a>
            </div>
        </div>
        
        <div class="dashboard-section">
            <h2 class="section-title">⏰ 最近活动</h2>
            <div style="color: #718096;">
                <p>• 张三申请了前端开发工程师职位 (2分钟前)</p>
                <p>• 李四的面试已安排在明天下午2点 (15分钟前)</p>
                <p>• 王五的面试反馈已提交 (1小时前)</p>
                <p>• 赵六接受了我们的录用通知 (2小时前)</p>
            </div>
        </div>
    </div>
</body>
</html>
"""

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
            email = request.form.get('email', '')
            password = request.form.get('password', '')
            desired_role = request.form.get('role', 'candidate')
            
            user = User.query.filter_by(email=email).first()
            
            if user and check_password_hash(user.password, password):
                user_is_hr = getattr(user, 'is_hr', False)
                
                if (desired_role == 'recruiter' and not user_is_hr) or (desired_role == 'candidate' and user_is_hr):
                    # 身份不匹配，显示错误信息
                    flash_message = '<div class="alert alert-danger">您选择的身份与注册时的身份不匹配。</div>'
                    return LOGIN_HTML.format(
                        flash_messages=flash_message,
                        email=email,
                        recruiter_selected='selected' if desired_role == 'recruiter' else '',
                        candidate_selected='selected' if desired_role == 'candidate' else ''
                    )
                
                session['user_id'] = user.id
                
                if user_is_hr:
                    return redirect(url_for('hr_dashboard'))
                else:
                    return "候选人仪表板 - 功能开发中..."
            else:
                # 登录失败，显示错误信息
                flash_message = '<div class="alert alert-danger">邮箱或密码错误。</div>'
                return LOGIN_HTML.format(
                    flash_messages=flash_message,
                    email=email,
                    recruiter_selected='selected' if desired_role == 'recruiter' else '',
                    candidate_selected='selected' if desired_role == 'candidate' else ''
                )
    
    # GET请求，显示登录页面
    return LOGIN_HTML.format(
        flash_messages='',
        email='',
        recruiter_selected='selected',
        candidate_selected=''
    )

# HR仪表板
@app.route('/hr_dashboard')
def hr_dashboard():
    if 'user_id' not in session:
        return redirect(url_for('sign'))
    
    user = User.query.get(session['user_id'])
    if not user or not user.is_hr:
        return redirect(url_for('sign'))
    
    # 获取统计数据
    total_candidates = User.query.filter_by(is_hr=False).count()
    total_jobs = Job.query.filter_by(user_id=user.id).count()
    
    return HR_DASHBOARD_HTML.format(
        total_candidates=total_candidates,
        total_jobs=total_jobs
    )

# 登出
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.clear()
    return redirect(url_for('sign'))

if __name__ == '__main__':
    print("🚀 启动超简化的Flask应用...")
    print("📧 HR账户: hr@smartrecruit.com")
    print("🔑 密码: hr123456")
    print("🌐 访问: http://127.0.0.1:5000")
    print("✅ 完全独立，无外部依赖")
    
    app.run(host='127.0.0.1', port=5000, debug=True)
