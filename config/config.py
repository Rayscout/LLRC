"""
LLRC Header Start
文件功能: 通用 Python 脚本/模块：config/config.py
创建时间: 2025-08-21 12:11
创建人: 李雨梦
更新记录:
- 2025-08-21 12:41 by 侯东杨
- 2025-08-27 17:22 by 苏杰
- 2025-08-28 09:26 by 谢佳悦
LLRC Header End
"""
"""
FILE-HEADER-AUTO-ADDED
文件: config/config.py
功能: 通用模块
创建时间: 2025-08-27 09:13
创建人: 张宇成
更新记录:
- 2025-08-29 10:19 by 李雨梦
"""
import os
from dotenv import load_dotenv # type: ignore

load_dotenv()

class Config:
    """类 Config：封装与该模块相关的数据与行为。"""
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
    """类 DevelopmentConfig：封装与该模块相关的数据与行为。"""
    DEBUG = True
    HOST = '127.0.0.1'
    PORT = 5000

class ProductionConfig(Config):
    """类 ProductionConfig：封装与该模块相关的数据与行为。"""
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
    """函数 get_config：核心业务逻辑。"""
    env = os.environ.get('FLASK_ENV', 'development')
    return config.get(env, config['default'])
