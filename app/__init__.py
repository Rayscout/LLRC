from flask import Flask
from flask_sqlalchemy import SQLAlchemy
try:
    from flask_session import Session
except Exception:  # Fallback if package not importable for any reason
    Session = None  # type: ignore
from flask_migrate import Migrate # type: ignore
from pymongo import MongoClient
from .config import Config

db = SQLAlchemy()
migrate = Migrate()
sess = Session() if Session is not None else None

mongo_client = MongoClient('mongodb://localhost:27017/')
mongodb = mongo_client['applications']
applications_collection = mongodb['applications']

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)  
    migrate.init_app(app, db)
    # Initialize Flask-Session only if available
    if sess is not None:
        # Ensure session dir exists when using filesystem
        session_dir = app.config.get('SESSION_FILE_DIR')
        if session_dir:
            import os
            os.makedirs(session_dir, exist_ok=True)
        sess.init_app(app)

    # Ensure upload folders exist
    from .utils import create_upload_folders
    create_upload_folders(app)

    with app.app_context():
        from .routes import main as main_blueprint
        app.register_blueprint(main_blueprint)

        return app
