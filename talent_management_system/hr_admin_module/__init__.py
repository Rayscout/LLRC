from flask import Blueprint

hr_admin_bp = Blueprint('hr_admin', __name__, url_prefix='/hr_admin')

from . import routes
