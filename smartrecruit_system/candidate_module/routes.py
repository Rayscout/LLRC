from flask import Blueprint, render_template, g, session, redirect, url_for, flash
from .profile import profile_bp
from .jobs import jobs_bp
from .applications import applications_bp
from .interview import interview_bp
from app.utils import extract_text_from_resume, ai_analyze_resume_text

# 创建求职者主蓝图
candidate_bp = Blueprint('candidate', __name__, url_prefix='/candidate')

@candidate_bp.route('/')
def home():
    """候选人首页 - 智能推荐"""
    if g.user is None:
        from flask import redirect, url_for, flash
        flash('请先登录。', 'danger')
        return redirect(url_for('common.auth.sign'))

    try:
        from .jobs import extract_user_skills
        user_skills = extract_user_skills(g.user)
    except Exception:
        user_skills = []

    # 生成简历AI分析（轻量运行，失败忽略）
    resume_analysis = None
    try:
        cv_text = ''
        if getattr(g.user, 'cv_data', None) and getattr(g.user, 'cv_file', None):
            cv_text = extract_text_from_resume(g.user.cv_data, g.user.cv_file) or ''
        if cv_text:
            resume_analysis = ai_analyze_resume_text(cv_text)
    except Exception:
        resume_analysis = None

    return render_template('smartrecruit/candidate/home.html', user=g.user, user_skills=user_skills, resume_analysis=resume_analysis)

@candidate_bp.route('/dashboard')
def dashboard():
    """候选人仪表盘 - 综合功能"""
    if g.user is None:
        from flask import redirect, url_for, flash
        flash('请先登录。', 'danger')
        return redirect(url_for('common.auth.sign'))

    try:
        from .jobs import extract_user_skills
        user_skills = extract_user_skills(g.user)
    except Exception:
        user_skills = []

    # 获取统计数据
    try:
        from .applications import get_user_applications_count
        applications_count = get_user_applications_count(g.user.id)
    except Exception:
        applications_count = 0

    try:
        from .jobs import get_user_saved_jobs_count
        saved_jobs_count = get_user_saved_jobs_count(g.user.id)
    except Exception:
        saved_jobs_count = 0

    # 计算资料完整度
    profile_completion = calculate_profile_completion(g.user)

    return render_template('smartrecruit/candidate/candidate_dashboard.html', 
                         user=g.user,
                         user_skills=user_skills,
                         applications_count=applications_count,
                         saved_jobs_count=saved_jobs_count,
                         profile_completion=profile_completion)

def calculate_profile_completion(user):
    """计算用户资料完整度"""
    fields = [
        user.first_name, user.last_name, user.email, user.phone_number,
        user.birthday, user.company_name, user.position, user.cv_file
    ]
    
    filled_fields = sum(1 for field in fields if field)
    total_fields = len(fields)
    
    return int((filled_fields / total_fields) * 100)

@candidate_bp.route('/logout')
def logout():
    """求职者登出"""
    session.pop('user_id', None)
    session.pop('user_type', None)
    session.clear()
    flash('您已退出登录。', 'success')
    return redirect(url_for('common.auth.logout'))

@candidate_bp.route('/settings')
def settings():
    """求职者设置页面"""
    if g.user is None:
        flash('请先登录。', 'danger')
        return redirect(url_for('common.auth.sign'))
    
    return render_template('smartrecruit/candidate/settings.html', user=g.user)

# 注册求职者子蓝图
candidate_bp.register_blueprint(profile_bp)
candidate_bp.register_blueprint(jobs_bp)
candidate_bp.register_blueprint(applications_bp)
candidate_bp.register_blueprint(interview_bp)
