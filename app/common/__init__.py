from flask import Blueprint
from .auth import auth_bp
from .files import files_bp

# 创建主蓝图
common_bp = Blueprint('common', __name__)

# 注册子蓝图
common_bp.register_blueprint(auth_bp)
common_bp.register_blueprint(files_bp)
