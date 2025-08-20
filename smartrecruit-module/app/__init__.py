from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_migrate import Migrate # type: ignore
from flask_login import LoginManager
from pymongo import MongoClient
from .config import Config

db = SQLAlchemy()
migrate = Migrate()
sess = Session()
login_manager = LoginManager()

mongo_client = MongoClient('mongodb://localhost:27017/')
mongodb = mongo_client['applications']
applications_collection = mongodb['applications']

@login_manager.user_loader
def load_user(user_id):
    from .models import User
    return User.query.get(int(user_id))

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)  
    migrate.init_app(app, db)
    sess.init_app(app)
    login_manager.init_app(app)
    
    # 设置登录视图
    login_manager.login_view = 'main.auth'
    login_manager.login_message = '请先登录以访问此页面。'
    login_manager.login_message_category = 'info'

    with app.app_context():
        from .routes import main as main_blueprint
        app.register_blueprint(main_blueprint)

        return app
