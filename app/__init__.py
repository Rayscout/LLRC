from flask import Flask
from flask_sqlalchemy import SQLAlchemy
try:
    from flask_session import Session
except Exception:
    Session = None
from flask_migrate import Migrate
try:
    from flask_login import LoginManager
except Exception:
    LoginManager = None
from pymongo import MongoClient
from .config import Config
import logging
import sys
import os
from jinja2 import ChoiceLoader, FileSystemLoader
try:
    from dotenv import load_dotenv
except Exception:
    load_dotenv = None

# 配置日志
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

db = SQLAlchemy()
migrate = Migrate()
sess = Session() if Session is not None else None
login_manager = LoginManager() if LoginManager is not None else None

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
    # 加载 .env 本地环境变量（如果可用）
    try:
        if load_dotenv is not None:
            load_dotenv()
    except Exception as e:
        logger.warning(f"Failed to load .env: {e}")
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
    
    # 初始化Flask-Login
    if login_manager is not None:
        try:
            login_manager.init_app(app)
            login_manager.login_view = 'common.auth.sign'
            login_manager.login_message = '请登录以访问此页面'
            login_manager.login_message_category = 'info'
            
            @login_manager.user_loader
            def load_user(user_id):
                try:
                    from .models import User
                    return User.query.get(int(user_id))
                except Exception as e:
                    logger.error(f"Failed to load user {user_id}: {e}")
                    return None
                    
            logger.info("Flask-Login initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Flask-Login: {e}")
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
        
        try:
            from .talent_dashboard import talent_dashboard
            logger.info("Talent dashboard blueprint imported successfully")
        except Exception as e:
            logger.warning(f"Failed to import talent dashboard blueprint: {e}")
            talent_dashboard = None
        
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
        
        if talent_dashboard:
            try:
                app.register_blueprint(talent_dashboard)
                logger.info("Talent dashboard blueprint registered successfully")
            except Exception as e:
                logger.error(f"Failed to register talent dashboard blueprint: {e}")
        else:
            logger.warning("Talent dashboard blueprint not available")
        
        # 添加根路径路由
        @app.route('/')
        def root():
            """根路径 - 直接渲染登录页面"""
            from flask import render_template
            return render_template('common/sign.html')
        
        # 添加简单测试路由
        @app.route('/test')
        def test_page():
            """简单测试页面"""
            return """
            <!DOCTYPE html>
            <html lang="zh-CN">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>测试页面</title>
            </head>
            <body>
                <h1>测试页面</h1>
                <p>如果您能看到这个页面，说明Flask应用正在正常运行。</p>
                <p><a href="/jobs">访问岗位页面</a></p>
                <p><a href="/">返回首页</a></p>
            </body>
            </html>
            """
        
        # 添加公开岗位展示路由
        @app.route('/jobs')
        def public_jobs():
            """公开岗位展示页面 - 无需登录"""
            from flask import render_template
            try:
                from app.models import Job
                # 获取所有岗位，按发布时间排序
                all_jobs = Job.query.order_by(Job.date_posted.desc()).limit(20).all()
                
                # 按公司分组
                jobs_by_company = {}
                for job in all_jobs:
                    company = getattr(job, 'company_name', '未知公司') or '未知公司'
                    if company not in jobs_by_company:
                        jobs_by_company[company] = []
                    jobs_by_company[company].append(job)
                
                logger.info(f"成功获取 {len(all_jobs)} 个岗位，来自 {len(jobs_by_company)} 家公司")
                
            except Exception as e:
                logger.error(f"获取公开岗位失败: {e}")
                # 返回空数据而不是错误
                all_jobs = []
                jobs_by_company = {}
            
            try:
                return render_template('common/public_jobs_simple.html', 
                                    jobs_by_company=jobs_by_company,
                                    total_jobs=len(all_jobs))
            except Exception as e:
                logger.error(f"渲染岗位页面模板失败: {e}")
                # 如果模板渲染失败，返回简单的错误页面
                return f"""
                <!DOCTYPE html>
                <html lang="zh-CN">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>岗位页面 - 智能招聘系统</title>
                    <style>
                        body {{ font-family: Arial, sans-serif; padding: 40px; text-align: center; }}
                        .error {{ color: #d32f2f; margin: 20px 0; }}
                        .info {{ color: #1976d2; margin: 20px 0; }}
                    </style>
                </head>
                <body>
                    <h1>岗位页面</h1>
                    <div class="info">共找到 {len(all_jobs)} 个岗位</div>
                    <div class="error">模板渲染出现问题，请联系管理员</div>
                    <p><a href="/">返回首页</a></p>
                </body>
                </html>
                """, 200
        
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
        
        # 暂时注释掉全局账号状态检查，避免重定向循环
        # 改用页面级别的状态显示和操作时检查
        # @app.before_request
        # def check_user_status():
        #     """检查已登录用户的账号状态"""
        #     from flask import session, redirect, url_for, flash
        #     try:
        #         # 只检查已登录用户
        #         if 'user_id' in session and g.user:
        #             if hasattr(g.user, 'is_active') and g.user.is_active is False:
        #                 # 账号已被注销，强制退出
        #                 session.clear()
        #                 flash('您的账号已被注销，已自动退出登录。请联系管理员。', 'warning')
        #                 return redirect(url_for('common.auth.sign'))
        #     except Exception as e:
        #         # 如果查询失败，记录错误但不重定向，避免循环
        #         logger.error(f"Error in check_user_status: {e}")
        #         # 不重定向，让请求继续处理
        #         pass

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
