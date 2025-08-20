from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_migrate import Migrate # type: ignore
from pymongo import MongoClient
from .config import Config
from sqlalchemy import inspect, text

db = SQLAlchemy()
migrate = Migrate()
sess = Session()

mongo_client = MongoClient('mongodb://localhost:27017/')
mongodb = mongo_client['applications']
applications_collection = mongodb['applications']

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)  
    migrate.init_app(app, db)
    sess.init_app(app)

    with app.app_context():
        # 自动修复：若缺少 user.cv_data 列，则在 SQLite 中添加该列
        try:
            inspector = inspect(db.engine)
            columns = [col['name'] for col in inspector.get_columns('user')]
            if 'cv_data' not in columns:
                with db.engine.connect() as conn:
                    conn.execute(text('ALTER TABLE user ADD COLUMN cv_data BLOB'))
                    conn.commit()
        except Exception:
            # 忽略启动时的修复异常，避免影响应用正常启动
            pass

        from .routes import main as main_blueprint
        app.register_blueprint(main_blueprint)

        return app
