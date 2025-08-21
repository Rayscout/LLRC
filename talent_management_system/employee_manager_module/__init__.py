from flask import Blueprint

employee_manager_bp = Blueprint('employee_manager', __name__, url_prefix='/employee_manager')

from . import routes
