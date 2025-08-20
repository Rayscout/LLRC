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
    

    
    MONGO_URI = 'mongodb://localhost:27017/applications'
