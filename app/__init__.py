from flask import Flask
from flask_sqlalchemy import SQLAlchemy
try:
    from flask_session import Session
except Exception:
    Session = None
from flask_migrate import Migrate
from pymongo import MongoClient
from .config import Config
import logging
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

db = SQLAlchemy()
migrate = Migrate()
sess = Session() if Session is not None else None

mongo_client = None
mongodb = None
applications_collection = None
try:
    mongo_client = MongoClient('mongodb://localhost:27017/')
    mongodb = mongo_client['applications']
    applications_collection = mongodb['applications']
    logging.info("MongoDB connected successfully.")
except Exception as e:
    logging.warning(f"Could not connect to MongoDB: {e}. MongoDB features will be disabled.")

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    if sess is not None:
        session_dir = app.config.get('SESSION_FILE_DIR')
        if session_dir:
            import os
            os.makedirs(session_dir, exist_ok=True)
        sess.init_app(app)

    from .utils import create_upload_folders
    create_upload_folders(app)

    with app.app_context():
        # 注册蓝图
        from .common import common_bp
        from smartrecruit_system.routes import smartrecruit_bp
        from talent_management_system.routes import talent_management_bp
        
        app.register_blueprint(common_bp)
        app.register_blueprint(smartrecruit_bp)
        app.register_blueprint(talent_management_bp)
        
        # 添加根路径路由
        @app.route('/')
        def root():
            """根路径 - 重定向到登录页面"""
            from flask import redirect, url_for
            return redirect(url_for('common.auth.sign'))
        
        # 添加全局模板助手
        @app.context_processor
        def inject_user():
            from flask import g
            return {'user': g.user}
        
        @app.before_request
        def load_user():
            from flask import g, session
            user_id = session.get('user_id')
            if user_id:
                from .models import User
                g.user = User.query.get(user_id)
            else:
                g.user = None
        
        return app
