import os
from dotenv import load_dotenv # type: ignore

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'TESTINGCHEATS123'
    
    # 数据库配置 - 支持本地和云端
    DATABASE_URL = os.environ.get('DATABASE_URL')
    if DATABASE_URL:
        # 云端PostgreSQL数据库
        SQLALCHEMY_DATABASE_URI = DATABASE_URL
    else:
        # 本地SQLite数据库（开发环境）
        SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_TYPE = 'filesystem'
    UPLOAD_FOLDER_CV = os.path.join('app', 'static', 'uploads', 'cv')
    UPLOAD_FOLDER_PHOTOS = os.path.join('app', 'static', 'uploads', 'photos')
    API_TOKEN = os.environ.get('API_TOKEN', 'default_api_token')
    API_URL = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct"
    
    # MongoDB配置 - 支持本地和云端
    MONGO_URI = os.environ.get('MONGO_URI') or 'mongodb://localhost:27017/applications'
    
    # 云数据库连接信息（用于数据迁移）
    CLOUD_DB_HOST = os.environ.get('CLOUD_DB_HOST', 'postgres-service.smartrecruit-system.svc.cluster.local')
    CLOUD_DB_PORT = os.environ.get('CLOUD_DB_PORT', '5432')
    CLOUD_DB_NAME = os.environ.get('CLOUD_DB_NAME', 'smartrecruit')
    CLOUD_DB_USER = os.environ.get('CLOUD_DB_USER', 'admin')
    CLOUD_DB_PASSWORD = os.environ.get('CLOUD_DB_PASSWORD', 'SmartRecruit2024!')
