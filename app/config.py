import os
from dotenv import load_dotenv # type: ignore

load_dotenv()

class Config:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 项目根目录
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'TESTINGCHEATS123'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_TYPE = 'filesystem'
    SESSION_FILE_DIR = os.path.join(os.getcwd(), 'flask_session_data')
    UPLOAD_FOLDER_CV = os.path.join(BASE_DIR, 'app', 'static', 'uploads', 'cv')
    UPLOAD_FOLDER_PHOTOS = os.path.join(BASE_DIR, 'app', 'static', 'uploads', 'photos')
    # 外部服务
    MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/applications')
    API_TOKEN = os.environ.get('API_TOKEN', 'default_api_token')
    API_URL = os.environ.get('API_URL', 'https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct')
    
    # 生产环境配置
    DEBUG = False
    HOST = '0.0.0.0'
    PORT = 5000

class DevelopmentConfig(Config):
    DEBUG = True
    HOST = '127.0.0.1'
    PORT = 5000

class ProductionConfig(Config):
    DEBUG = False
    HOST = '0.0.0.0'
    PORT = 5000
    
    # 生产环境特定配置
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///site.db'
    SESSION_FILE_DIR = '/var/www/llrc/flask_session_data'

# 配置字典
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

# 根据环境变量选择配置
def get_config():
    env = os.environ.get('FLASK_ENV', 'development')
    return config.get(env, config['default'])
