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
    is_active = db.Column(db.Boolean, default=True)  # 添加活跃状态字段

    user = db.relationship('User', backref=db.backref('applications', lazy=True))
    job = db.relationship('Job', backref=db.backref('applications', lazy=True))
    __table_args__ = (db.UniqueConstraint('user_id', 'job_id', name='unique_user_job_application'),)

class Feedback(db.Model):
    """反馈系统数据模型"""
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category = db.Column(db.String(50), nullable=False)  # skill, communication, performance
    feedback_type = db.Column(db.String(50), nullable=False)  # positive, constructive, improvement
    content = db.Column(db.Text, nullable=False)
    priority = db.Column(db.String(20), default='medium')  # high, medium, low
    status = db.Column(db.String(20), default='sent')  # sent, read, responded, archived
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    read_at = db.Column(db.DateTime)
    responded_at = db.Column(db.DateTime)
    
    # 关系
    sender = db.relationship('User', foreign_keys=[sender_id], backref=db.backref('sent_feedback', lazy=True))
    recipient = db.relationship('User', foreign_keys=[recipient_id], backref=db.backref('received_feedback', lazy=True))

class FeedbackNotification(db.Model):
    """反馈通知数据模型"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    feedback_id = db.Column(db.Integer, db.ForeignKey('feedback.id'), nullable=False)
    notification_type = db.Column(db.String(50), nullable=False)  # new_feedback, feedback_read, feedback_responded
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 关系
    user = db.relationship('User', backref=db.backref('feedback_notifications', lazy=True))
    feedback = db.relationship('Feedback', backref=db.backref('notifications', lazy=True))

class TaskEvaluation(db.Model):
    """任务绩效评价数据模型"""
    id = db.Column(db.Integer, primary_key=True)
    evaluator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # 评价人（高管/主管）
    employee_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)   # 被评价员工
    task_title = db.Column(db.String(200), nullable=False)  # 任务名称
    task_description = db.Column(db.Text)  # 任务描述
    department = db.Column(db.String(100))  # 部门（冗余便于统计）
    score_quality = db.Column(db.Integer, nullable=False)  # 质量评分 1-5
    score_efficiency = db.Column(db.Integer, nullable=False)  # 效率评分 1-5
    score_collaboration = db.Column(db.Integer, nullable=False)  # 协作评分 1-5
    total_score = db.Column(db.Integer, nullable=False)  # 总分（可按权重计算）
    comment = db.Column(db.Text)  # 评语
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    evaluator = db.relationship('User', foreign_keys=[evaluator_id], backref=db.backref('given_evaluations', lazy=True))
    employee = db.relationship('User', foreign_keys=[employee_id], backref=db.backref('task_evaluations', lazy=True))

