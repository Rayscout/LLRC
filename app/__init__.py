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
from jinja2 import ChoiceLoader, FileSystemLoader

# 配置日志
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

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
    logger.info("MongoDB connected successfully.")
except Exception as e:
    logger.warning(f"Could not connect to MongoDB: {e}. MongoDB features will be disabled.")

def create_app():
    # 显式指定模板与静态资源目录，避免路径解析异常导致找不到模板
    base_dir = os.path.dirname(os.path.abspath(__file__))
    templates_dir = os.path.join(base_dir, 'templates')
    static_dir = os.path.join(base_dir, 'static')
    app = Flask(__name__, template_folder=templates_dir, static_folder=static_dir)
    # 兼容多种工作目录的模板搜索路径
    try:
        search_paths = [
            templates_dir,
            os.path.join(os.getcwd(), 'LLRC', 'app', 'templates'),
            os.path.join(os.getcwd(), 'app', 'templates'),
        ]
        app.jinja_loader = ChoiceLoader([
            FileSystemLoader(path) for path in search_paths if os.path.isdir(path)
        ])
        logger.debug(f"Jinja search paths: {search_paths}")
    except Exception as e:
        logger.warning(f"Failed to set custom Jinja loader: {e}")
    app.config.from_object(Config)

    # 初始化扩展
    try:
        db.init_app(app)
        logger.info("SQLAlchemy initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize SQLAlchemy: {e}")
        raise
    
    try:
        migrate.init_app(app, db)
        logger.info("Flask-Migrate initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize Flask-Migrate: {e}")
        raise
    
    if sess is not None:
        try:
            session_dir = app.config.get('SESSION_FILE_DIR')
            if session_dir:
                os.makedirs(session_dir, exist_ok=True)
            sess.init_app(app)
            logger.info("Flask-Session initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Flask-Session: {e}")
            raise

    try:
        from .utils import create_upload_folders
        create_upload_folders(app)
        logger.info("Upload folders created successfully")
    except Exception as e:
        logger.error(f"Failed to create upload folders: {e}")
        raise

    with app.app_context():
        # 注册蓝图
        try:
            from .common import common_bp
            logger.info("Common blueprint imported successfully")
        except Exception as e:
            logger.error(f"Failed to import common blueprint: {e}")
            raise
        
        try:
            from smartrecruit_system.routes import smartrecruit_bp
            logger.info("SmartRecruit blueprint imported successfully")
        except Exception as e:
            logger.error(f"Failed to import smartrecruit blueprint: {e}")
            raise
        
        try:
            from talent_management_system.routes import talent_management_bp
            logger.info("Talent management blueprint imported successfully")
        except Exception as e:
            logger.error(f"Failed to import talent management blueprint: {e}")
            raise
        
        # 注册蓝图
        try:
            app.register_blueprint(common_bp)
            logger.info("Common blueprint registered successfully")
        except Exception as e:
            logger.error(f"Failed to register common blueprint: {e}")
            raise
        
        try:
            app.register_blueprint(smartrecruit_bp)
            logger.info("SmartRecruit blueprint registered successfully")
        except Exception as e:
            logger.error(f"Failed to register smartrecruit blueprint: {e}")
            raise
        
        try:
            app.register_blueprint(talent_management_bp)
            logger.info("Talent management blueprint registered successfully")
        except Exception as e:
            logger.error(f"Failed to register talent management blueprint: {e}")
            raise
        
        # 添加根路径路由
        @app.route('/')
        def root():
            """根路径 - 重定向到登录页面"""
            from flask import redirect, url_for
            return redirect(url_for('common.auth.sign'))
        
        # 避免浏览器请求 /favicon.ico 导致 404 噪音
        @app.route('/favicon.ico')
        def favicon():
            from flask import Response
            return Response(status=204)

        # 添加全局模板助手
        @app.context_processor
        def inject_user():
            from flask import g
            try:
                return {'user': getattr(g, 'user', None)}
            except Exception as e:
                logger.error(f"Error in inject_user: {e}")
                return {'user': None}
        
        @app.before_request
        def load_user():
            from flask import g, session
            try:
                user_id = session.get('user_id')
                if user_id:
                    try:
                        from .models import User
                        g.user = User.query.get(user_id)
                        if g.user is None:
                            logger.warning(f"User with ID {user_id} not found in database")
                    except Exception as e:
                        logger.error(f"Failed to load user: {e}")
                        g.user = None
                else:
                    g.user = None
            except Exception as e:
                logger.error(f"Error in before_request hook: {e}")
                g.user = None
        
        # 添加错误处理器
        @app.errorhandler(500)
        def internal_error(error):
            logger.error(f"Internal server error: {error}")
            return "内部服务器错误，请检查日志", 500
        
        @app.errorhandler(404)
        def not_found_error(error):
            logger.error(f"Page not found: {error}")
            return "页面未找到", 404
        
        logger.info("Application created successfully")
        return app
