from flask import Blueprint
from .profile import profile_bp
from .jobs import jobs_bp
from .applications import applications_bp

# 创建求职者主蓝图
candidate_bp = Blueprint('candidate', __name__, url_prefix='/candidate')

# 注册求职者子蓝图
candidate_bp.register_blueprint(profile_bp)
candidate_bp.register_blueprint(jobs_bp)
candidate_bp.register_blueprint(applications_bp)
