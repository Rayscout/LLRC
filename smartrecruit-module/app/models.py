from . import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    company_name = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100))  # 新增职位字段
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    birthday = db.Column(db.String(10), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    cv_file = db.Column(db.String(120)) 
    profile_photo = db.Column(db.String(120)) 
    is_hr = db.Column(db.Boolean, default=False)  # 新增HR标识字段
    
    # Flask-Login 所需的方法
    @property
    def is_authenticated(self):
        return True
    
    @property
    def is_active(self):
        return True
    
    @property
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return str(self.id)

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    salary = db.Column(db.String(50), nullable=False)  
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # 新增招聘要求字段
    positions_needed = db.Column(db.Integer, nullable=False, default=1)  # 招聘人数
    min_age = db.Column(db.Integer)  # 最小年龄要求
    max_age = db.Column(db.Integer)  # 最大年龄要求
    education_requirement = db.Column(db.String(100))  # 学历要求
    experience_years = db.Column(db.Integer)  # 工作经验年限要求
    skills_required = db.Column(db.Text)  # 技能要求
    benefits = db.Column(db.Text)  # 福利待遇
    contact_email = db.Column(db.String(120))  # 联系邮箱
    contact_phone = db.Column(db.String(15))  # 联系电话
    application_deadline = db.Column(db.DateTime)  # 申请截止日期
    job_type = db.Column(db.String(50))  # 工作类型（全职/兼职/实习）
    department = db.Column(db.String(100))  # 部门

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
