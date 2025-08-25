from flask import Blueprint
from .dashboard import dashboard_bp
from .recruitment import recruitment_bp
from .candidates import candidates_bp
from .profile import profile_bp
from .sync_management import sync_management_bp

# 创建HR主蓝图
hr_bp = Blueprint('hr', __name__, url_prefix='/hr')

# 注册HR子蓝图
hr_bp.register_blueprint(dashboard_bp)
hr_bp.register_blueprint(recruitment_bp)
hr_bp.register_blueprint(candidates_bp)
hr_bp.register_blueprint(profile_bp)
hr_bp.register_blueprint(sync_management_bp)
