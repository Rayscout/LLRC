# 人才管理系统数据模型
# 包含人才管理相关的所有数据模型定义

from datetime import datetime
from app import db

class Employee(db.Model):
    """员工模型"""
    __tablename__ = 'employee'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    employee_id = db.Column(db.String(50), unique=True, nullable=False)
    department = db.Column(db.String(100))
    position = db.Column(db.String(100))
    supervisor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    hire_date = db.Column(db.Date)
    salary = db.Column(db.Float)
    performance_score = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class SmartGoal(db.Model):
    """SMART目标模型"""
    __tablename__ = 'smart_goal'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    specific = db.Column(db.Text, nullable=False)
    measurable = db.Column(db.Text, nullable=False)
    achievable = db.Column(db.Text, nullable=False)
    relevant = db.Column(db.Text, nullable=False)
    time_bound = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), default='custom')
    priority = db.Column(db.String(20), default='medium')
    target_date = db.Column(db.Date, nullable=False)
    estimated_hours = db.Column(db.Integer, default=0)
    status = db.Column(db.String(20), default='active')  # active, completed, paused, cancelled
    progress = db.Column(db.Float, default=0.0)  # 0-100
    completed_hours = db.Column(db.Float, default=0.0)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    user = db.relationship('User', backref='smart_goals')

class GoalProgress(db.Model):
    """目标进度历史记录模型"""
    __tablename__ = 'goal_progress'
    
    id = db.Column(db.Integer, primary_key=True)
    goal_id = db.Column(db.Integer, db.ForeignKey('smart_goal.id'), nullable=False)
    progress = db.Column(db.Float, nullable=False)
    completed_hours = db.Column(db.Float, nullable=False)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 关系
    goal = db.relationship('SmartGoal', backref='progress_history')

class EmployeeProjectExperience(db.Model):
    """员工项目经验模型"""
    __tablename__ = 'employee_project_experience'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)
    estimated_end_date = db.Column(db.Date)
    status = db.Column(db.String(20), default='active')  # active, completed, suspended
    team_size = db.Column(db.Integer)
    technologies = db.Column(db.Text)  # 存储为逗号分隔的字符串
    achievements = db.Column(db.Text)  # 存储为JSON字符串
    contribution = db.Column(db.Text)
    project_url = db.Column(db.String(500))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    user = db.relationship('User', backref='project_experiences')

class Performance(db.Model):
    """绩效模型"""
    __tablename__ = 'performance'
    
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    period = db.Column(db.String(20))  # 绩效周期，如 "2024-Q1"
    score = db.Column(db.Float)
    evaluation = db.Column(db.Text)
    evaluator_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Project(db.Model):
    """项目模型"""
    __tablename__ = 'project'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    status = db.Column(db.String(20), default='active')  # active, completed, suspended
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class EmployeeProject(db.Model):
    """员工项目关联模型"""
    __tablename__ = 'employee_project'
    
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    role = db.Column(db.String(100))
    contribution = db.Column(db.Text)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class LearningPath(db.Model):
    """学习路径模型"""
    __tablename__ = 'learning_path'
    
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    progress = db.Column(db.Float, default=0.0)  # 0-100
    status = db.Column(db.String(20), default='active')  # active, completed, paused
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Course(db.Model):
    """课程模型"""
    __tablename__ = 'course'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(100))
    difficulty = db.Column(db.String(20))  # beginner, intermediate, advanced
    duration = db.Column(db.Integer)  # 分钟
    url = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class EmployeeCourse(db.Model):
    """员工课程关联模型"""
    __tablename__ = 'employee_course'
    
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    progress = db.Column(db.Float, default=0.0)  # 0-100
    status = db.Column(db.String(20), default='enrolled')  # enrolled, in_progress, completed
    completed_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Feedback模型已在app/models.py中定义，此处移除重复定义

class Goal(db.Model):
    """目标模型"""
    __tablename__ = 'goal'
    
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    goal_type = db.Column(db.String(50))  # performance, learning, career
    target_value = db.Column(db.Float)
    current_value = db.Column(db.Float, default=0.0)
    deadline = db.Column(db.Date)
    status = db.Column(db.String(20), default='active')  # active, completed, overdue
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Compensation(db.Model):
    """薪酬模型"""
    __tablename__ = 'compensation'
    
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    base_salary = db.Column(db.Float, nullable=False)
    bonus = db.Column(db.Float, default=0.0)
    allowance = db.Column(db.Float, default=0.0)
    effective_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)
    reason = db.Column(db.String(200))
    approved_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# 关系定义
def init_relationships():
    """初始化模型关系"""
    from app.models import User
    
    # Employee 关系
    Employee.user = db.relationship('User', foreign_keys=[Employee.user_id], backref='employee_profile')
    Employee.supervisor = db.relationship('User', foreign_keys=[Employee.supervisor_id], backref='subordinates')
    
    # SmartGoal 关系
    SmartGoal.user = db.relationship('User', backref='smart_goals')

    # Performance 关系
    Performance.employee = db.relationship('Employee', backref='performances')
    Performance.evaluator = db.relationship('User', foreign_keys=[Performance.evaluator_id])
    
    # Project 关系
    Project.employees = db.relationship('Employee', secondary='employee_project', backref='projects')
    
    # EmployeeProject 关系
    EmployeeProject.employee = db.relationship('Employee', backref='project_assignments')
    EmployeeProject.project = db.relationship('Project', backref='employee_assignments')
    
    # LearningPath 关系
    LearningPath.employee = db.relationship('Employee', backref='learning_paths')
    
    # Course 关系
    Course.employees = db.relationship('Employee', secondary='employee_course', backref='courses')
    
    # EmployeeCourse 关系
    EmployeeCourse.employee = db.relationship('Employee', backref='course_enrollments')
    EmployeeCourse.course = db.relationship('Course', backref='enrollments')
    
    # Feedback关系已在app/models.py中定义
    
    # Goal 关系
    Goal.employee = db.relationship('Employee', backref='goals')
    
    # Compensation 关系
    Compensation.employee = db.relationship('Employee', backref='compensations')
    Compensation.approver = db.relationship('User', foreign_keys=[Compensation.approved_by])
