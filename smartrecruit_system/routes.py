from flask import Blueprint
from .hr_module import hr_bp
from .candidate_module import candidate_bp

# 创建智能招聘系统主蓝图
smartrecruit_bp = Blueprint('smartrecruit', __name__, url_prefix='/smartrecruit')

# 注册子蓝图
smartrecruit_bp.register_blueprint(hr_bp)
smartrecruit_bp.register_blueprint(candidate_bp)
