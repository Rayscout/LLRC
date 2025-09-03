from . import db
from datetime import datetime
try:
    from flask_login import UserMixin
except Exception:
    # 如果Flask-Login不可用，提供兼容基类
    class UserMixin:
        pass  # Flask-Login 方法将在User模型中实现

class User(UserMixin, db.Model):
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
    
    # 账号状态管理字段
    is_active = db.Column(db.Boolean, default=True)  # 账号是否活跃
    deactivated_at = db.Column(db.DateTime)  # 注销时间
    deactivated_by = db.Column(db.Integer, db.ForeignKey('user.id'))  # 注销操作人ID
    
    # Flask-Login 所需的方法
    def get_id(self):
        return str(self.id)
    
    @property
    def is_authenticated(self):
        return True
    
    @property
    def is_anonymous(self):
        return False

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
    category = db.Column(db.String(50), nullable=False)  # skill, communication, performance, general
    feedback_type = db.Column(db.String(50), nullable=False)  # positive, constructive, improvement, request
    content = db.Column(db.Text, nullable=False)
    priority = db.Column(db.String(20), default='medium')  # high, medium, low
    status = db.Column(db.String(20), default='sent')  # sent, read, responded, archived
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    read_at = db.Column(db.DateTime)
    responded_at = db.Column(db.DateTime)
    response_content = db.Column(db.Text)  # 回复内容
    response_rating = db.Column(db.Integer)  # 回复评分 1-5
    
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

class TalentDemand(db.Model):
    """高管发布的人才需求（仅关键词/描述）"""
    id = db.Column(db.Integer, primary_key=True)
    executive_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    keyword = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # 关系
    executive = db.relationship('User', backref=db.backref('talent_demands', lazy=True))

class TalentDemandNotification(db.Model):
    """HR 消息通知：来自某高管的人才需求"""
    id = db.Column(db.Integer, primary_key=True)
    hr_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    demand_id = db.Column(db.Integer, db.ForeignKey('talent_demand.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # 关系
    hr_user = db.relationship('User', backref=db.backref('talent_demand_notifications', lazy=True))
    demand = db.relationship('TalentDemand', backref=db.backref('notifications', lazy=True))

class TalentDemandDraft(db.Model):
    """HR 需求暂存箱（从高管通知保存，便于发布职位时参考）"""
    id = db.Column(db.Integer, primary_key=True)
    hr_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    notification_id = db.Column(db.Integer, db.ForeignKey('talent_demand_notification.id'))
    executive_name = db.Column(db.String(200))
    executive_email = db.Column(db.String(200))
    keyword = db.Column(db.String(255))
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # 关系
    hr_user = db.relationship('User', backref=db.backref('talent_demand_drafts', lazy=True))
    notification = db.relationship('TalentDemandNotification', backref=db.backref('drafts', lazy=True))

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

class TalentDevelopmentData(db.Model):
    """人才发展数据表 - 存储员工详细信息用于AI分析"""
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # 基本信息
    position = db.Column(db.String(100), nullable=False)  # 职位
    department = db.Column(db.String(100), nullable=False)  # 部门
    salary = db.Column(db.Float, nullable=False)  # 薪资
    hire_date = db.Column(db.Date, nullable=False)  # 入职日期
    
    # 绩效相关
    performance_score = db.Column(db.Float, default=0.0)  # 绩效评分
    promotion_count = db.Column(db.Integer, default=0)  # 晋升次数
    last_promotion_date = db.Column(db.Date)  # 最近晋升日期
    
    # 技能发展
    skills_level = db.Column(db.Float, default=0.0)  # 技能水平评分
    training_hours = db.Column(db.Float, default=0.0)  # 培训时长
    certification_count = db.Column(db.Integer, default=0)  # 证书数量
    
    # 工作满意度
    satisfaction_score = db.Column(db.Float, default=0.0)  # 满意度评分
    work_life_balance = db.Column(db.Float, default=0.0)  # 工作生活平衡评分
    
    # 团队协作
    teamwork_score = db.Column(db.Float, default=0.0)  # 团队协作评分
    leadership_potential = db.Column(db.Float, default=0.0)  # 领导力潜力
    
    # 市场竞争力
    market_salary = db.Column(db.Float)  # 市场薪资
    market_demand = db.Column(db.Float, default=0.0)  # 市场需求度
    
    # 风险指标
    turnover_risk = db.Column(db.Float, default=0.0)  # 离职风险概率
    risk_factors = db.Column(db.Text)  # 风险因素（JSON格式）
    
    # 时间戳
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    employee = db.relationship('User', backref=db.backref('talent_data', lazy=True))

class MarketSalaryData(db.Model):
    """市场薪资数据表"""
    id = db.Column(db.Integer, primary_key=True)
    position = db.Column(db.String(100), nullable=False)  # 职位
    industry = db.Column(db.String(100), nullable=False)  # 行业
    location = db.Column(db.String(100), nullable=False)  # 地区
    experience_level = db.Column(db.String(50), nullable=False)  # 经验级别
    
    # 薪资数据
    min_salary = db.Column(db.Float, nullable=False)  # 最低薪资
    max_salary = db.Column(db.Float, nullable=False)  # 最高薪资
    avg_salary = db.Column(db.Float, nullable=False)  # 平均薪资
    median_salary = db.Column(db.Float, nullable=False)  # 中位数薪资
    
    # 市场趋势
    demand_trend = db.Column(db.Float, default=0.0)  # 需求趋势 (-1到1)
    supply_trend = db.Column(db.Float, default=0.0)  # 供应趋势 (-1到1)
    
    # 时间戳
    data_date = db.Column(db.Date, nullable=False)  # 数据日期
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class TalentAnalysisReport(db.Model):
    """人才分析报告表"""
    id = db.Column(db.Integer, primary_key=True)
    report_type = db.Column(db.String(50), nullable=False)  # 报告类型：individual, department, company
    target_id = db.Column(db.Integer)  # 目标ID（员工ID、部门ID等）
    
    # 报告内容
    analysis_data = db.Column(db.Text, nullable=False)  # 分析数据（JSON格式）
    risk_assessment = db.Column(db.Text)  # 风险评估
    market_comparison = db.Column(db.Text)  # 市场对比
    trend_forecast = db.Column(db.Text)  # 趋势预测
    recommendations = db.Column(db.Text)  # 建议
    
    # 文件路径
    pdf_path = db.Column(db.String(255))  # PDF文件路径
    
    # 时间戳
    generated_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # 关系
    creator = db.relationship('User', backref=db.backref('generated_reports', lazy=True))

class AIAnalysisLog(db.Model):
    """AI分析日志表"""
    id = db.Column(db.Integer, primary_key=True)
    analysis_type = db.Column(db.String(50), nullable=False)  # 分析类型
    input_data = db.Column(db.Text)  # 输入数据
    output_data = db.Column(db.Text)  # 输出数据
    processing_time = db.Column(db.Float)  # 处理时间（秒）
    status = db.Column(db.String(20), default='success')  # 状态：success, error
    error_message = db.Column(db.Text)  # 错误信息

    # 时间戳
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))

    # 关系
    user = db.relationship('User', backref=db.backref('ai_analysis_logs', lazy=True))

class SmartGoal(db.Model):
    """SMART目标数据模型"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # 基本信息
    title = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50), default='custom')  # technical, soft_skills, business, custom
    priority = db.Column(db.String(20), default='medium')  # high, medium, low

    # SMART原则字段
    specific = db.Column(db.Text, nullable=False)  # S - Specific
    measurable = db.Column(db.Text, nullable=False)  # M - Measurable
    achievable = db.Column(db.Text, nullable=False)  # A - Achievable
    relevant = db.Column(db.Text, nullable=False)  # R - Relevant
    time_bound = db.Column(db.Text, nullable=False)  # T - Time-bound

    # 进度跟踪
    target_date = db.Column(db.Date, nullable=False)
    estimated_hours = db.Column(db.Integer, default=0)  # 预计总学习小时数
    completed_hours = db.Column(db.Integer, default=0)  # 已完成的学习小时数
    progress = db.Column(db.Float, default=0.0)  # 进度百分比 (0-100)

    # 状态管理
    status = db.Column(db.String(20), default='active')  # active, completed, paused, cancelled
    notes = db.Column(db.Text)  # 进度备注

    # 时间戳
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关系
    user = db.relationship('User', backref=db.backref('smart_goals', lazy=True))

    @property
    def progress_percentage(self):
        """根据已学习小时数计算进度百分比"""
        if self.estimated_hours <= 0:
            return 0.0
        return min(100.0, (self.completed_hours / self.estimated_hours) * 100.0)

    @property
    def remaining_hours(self):
        """剩余学习小时数"""
        return max(0, self.estimated_hours - self.completed_hours)

    @property
    def is_overdue(self):
        """是否已过期"""
        return datetime.utcnow().date() > self.target_date

    def update_progress_from_hours(self, new_completed_hours):
        """根据新的已学习小时数更新进度"""
        self.completed_hours = max(0, min(self.estimated_hours, new_completed_hours))
        self.progress = self.progress_percentage
        self.last_updated = datetime.utcnow()
        self.updated_at = datetime.utcnow()

        # 如果进度达到100%，自动标记为完成
        if self.progress >= 100:
            self.status = 'completed'

class Project(db.Model):
    """项目经验数据模型"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # 基本信息
    name = db.Column(db.String(200), nullable=False)  # 项目名称
    role = db.Column(db.String(100), nullable=False)  # 担任角色
    description = db.Column(db.Text, nullable=False)  # 项目描述

    # 时间信息
    start_date = db.Column(db.Date, nullable=False)  # 开始日期
    end_date = db.Column(db.Date)  # 结束日期（可选，为进行中的项目）

    # 项目状态
    status = db.Column(db.String(20), default='进行中')  # 已完成、进行中、已暂停

    # 技术信息
    technologies = db.Column(db.Text)  # 使用的技术栈（JSON格式存储）
    team_size = db.Column(db.Integer, default=1)  # 团队规模

    # 项目贡献
    contribution = db.Column(db.Text)  # 主要贡献描述
    achievements = db.Column(db.Text)  # 项目成就（JSON格式存储）

    # 时间戳
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关系
    user = db.relationship('User', backref=db.backref('projects', lazy=True))

    @property
    def technologies_list(self):
        """获取技术栈列表"""
        if not self.technologies:
            return []
        try:
            import json
            return json.loads(self.technologies)
        except:
            return []

    @property
    def achievements_list(self):
        """获取成就列表"""
        if not self.achievements:
            return []
        try:
            import json
            return json.loads(self.achievements)
        except:
            return []

    def set_technologies(self, technologies_list):
        """设置技术栈"""
        import json
        self.technologies = json.dumps(technologies_list)

    def set_achievements(self, achievements_list):
        """设置成就列表"""
        import json
        self.achievements = json.dumps(achievements_list)

    @property
    def duration_months(self):
        """计算项目持续时间（月）"""
        if not self.end_date:
            # 进行中的项目计算到当前时间
            end_date = datetime.utcnow().date()
        else:
            end_date = self.end_date

        if self.start_date and end_date:
            delta = end_date - self.start_date
            return delta.days // 30  # 粗略计算月数
        return 0


class InterviewSchedule(db.Model):
    """面试安排数据模型"""
    id = db.Column(db.Integer, primary_key=True)
    
    # 关联字段
    hr_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # HR用户ID
    candidate_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # 候选人ID
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)  # 职位ID
    application_id = db.Column(db.Integer, db.ForeignKey('application.id'), nullable=False)  # 申请ID
    
    # 面试时间信息
    interview_date = db.Column(db.Date, nullable=False)  # 面试日期
    start_time = db.Column(db.Time, nullable=False)  # 开始时间
    end_time = db.Column(db.Time, nullable=False)  # 结束时间
    
    # 面试详情
    interview_type = db.Column(db.String(20), nullable=False)  # online, onsite, phone
    location = db.Column(db.String(200))  # 面试地点或在线链接
    interviewer_name = db.Column(db.String(100))  # 面试官姓名
    notes = db.Column(db.Text)  # 备注信息
    
    # 状态管理
    status = db.Column(db.String(20), default='scheduled')  # scheduled, completed, cancelled, rescheduled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    hr = db.relationship('User', foreign_keys=[hr_id], backref=db.backref('scheduled_interviews', lazy=True))
    candidate = db.relationship('User', foreign_keys=[candidate_id], backref=db.backref('my_interviews', lazy=True))
    job = db.relationship('Job', backref=db.backref('interview_schedules', lazy=True))
    application = db.relationship('Application', backref=db.backref('interview_schedules', lazy=True))
    
    def __repr__(self):
        return f'<InterviewSchedule {self.id}: {self.candidate_id} -> {self.job_id}>'
    
    @property
    def interview_datetime(self):
        """获取完整的面试日期时间"""
        from datetime import datetime
        return datetime.combine(self.interview_date, self.start_time)
    
    @property
    def duration_minutes(self):
        """计算面试时长（分钟）"""
        if self.start_time and self.end_time:
            start_minutes = self.start_time.hour * 60 + self.start_time.minute
            end_minutes = self.end_time.hour * 60 + self.end_time.minute
            return end_minutes - start_minutes
        return 0
    
    @property
    def is_today(self):
        """是否为今天的面试"""
        return self.interview_date == datetime.utcnow().date()
    
    @property
    def is_upcoming(self):
        """是否为即将到来的面试（今天或未来）"""
        return self.interview_date >= datetime.utcnow().date()
    
    @property
    def is_past(self):
        """是否为过去的面试"""
        return self.interview_date < datetime.utcnow().date()

