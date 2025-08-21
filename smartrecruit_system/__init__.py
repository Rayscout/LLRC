from flask import Blueprint

smartrecruit_bp = Blueprint('smartrecruit', __name__, url_prefix='/smartrecruit')

from . import routes
