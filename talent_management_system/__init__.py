from flask import Blueprint

talent_management_bp = Blueprint('talent_management', __name__, url_prefix='/talent')

from . import routes
