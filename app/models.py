from . import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    company_name = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100))  # 可选职位字段
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    birthday = db.Column(db.String(10), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    cv_file = db.Column(db.String(120))
    profile_photo = db.Column(db.String(120))
    cv_data = db.Column(db.LargeBinary)  # 可选的简历二进制
    is_hr = db.Column(db.Boolean, default=False)  # HR标识
    user_type = db.Column(db.String(20), default='candidate')  # candidate, employee, supervisor, executive
    # 员工和高管相关字段
    department = db.Column(db.String(100))  # 部门
    employee_id = db.Column(db.String(50), unique=True)  # 员工编号
    supervisor_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 主管ID
    hire_date = db.Column(db.Date)  # 入职日期
    # 个人资料相关字段
    bio = db.Column(db.Text)  # 个人简介
    skills = db.Column(db.Text)  # 技能标签（JSON格式存储）
    education = db.Column(db.Text)  # 教育经历
    experience = db.Column(db.Text)  # 工作经历

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    company_name = db.Column(db.String(100), nullable=False, default='未知公司')
    location = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    requirements = db.Column(db.Text, nullable=True)
    salary = db.Column(db.String(50), nullable=False)
    job_type = db.Column(db.String(20), nullable=True, default='全职')  # 全职、兼职、实习、远程
    experience_level = db.Column(db.String(20), nullable=True, default='不限')  # 初级、中级、高级、专家
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # HR 扩展字段
    positions_needed = db.Column(db.Integer, nullable=False, default=1)
    min_age = db.Column(db.Integer)
    max_age = db.Column(db.Integer)
    education_requirement = db.Column(db.String(100))
    experience_years = db.Column(db.Integer)
    skills_required = db.Column(db.Text)
    benefits = db.Column(db.Text)
    contact_email = db.Column(db.String(120))
    contact_phone = db.Column(db.String(15))
    application_deadline = db.Column(db.DateTime)
    department = db.Column(db.String(100))

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), nullable=False, default='Pending')

    user = db.relationship('User', backref=db.backref('applications', lazy=True))
    job = db.relationship('Job', backref=db.backref('applications', lazy=True))
    __table_args__ = (db.UniqueConstraint('user_id', 'job_id', name='unique_user_job_application'),)

