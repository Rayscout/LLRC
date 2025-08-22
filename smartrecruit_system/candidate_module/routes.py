from flask import Blueprint, render_template, g
from .profile import profile_bp
from .jobs import jobs_bp
from .applications import applications_bp

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

    return render_template('smartrecruit/candidate/home.html', user_skills=user_skills)

# 注册求职者子蓝图
candidate_bp.register_blueprint(profile_bp)
candidate_bp.register_blueprint(jobs_bp)
candidate_bp.register_blueprint(applications_bp)
