"""
LLRC Header Start
文件功能: SmartRecruit 子系统 Python 模块：smartrecruit_system/candidate_module/ai_config.py
创建时间: 2025-08-25 10:31
创建人: 李雨梦
更新记录:
- 2025-08-25 11:01 by 谢佳悦
- 2025-08-28 10:03 by 李雨梦
LLRC Header End
"""
"""
FILE-HEADER-AUTO-ADDED
文件: smartrecruit_system/candidate_module/ai_config.py
功能: 通用模块
创建时间: 2025-08-23 15:50
创建人: 苏杰
更新记录:
- 2025-08-30 18:30 by 谢佳悦
"""
import os
from pathlib import Path

class AIConfig:
    """AI模块配置文件"""
    
    def __init__(self):
        """函数 __init__：核心业务逻辑。"""
        # 获取项目根目录
        self.project_root = Path(__file__).parent.parent.parent.parent
        
        # YOLO模型路径配置（允许通过环境变量覆盖）
        env_yolo_base = os.getenv("YOLO_BASE_PATH")
        self.yolo_base_path = Path(env_yolo_base) if env_yolo_base else self.project_root / "YOLO" / "Facial-Expression-Recognition"
        
        # 人脸检测模型路径
        # 优先使用环境变量 YOLO_FACE_WEIGHTS，其次使用默认路径
        env_face_weights = os.getenv("YOLO_FACE_WEIGHTS")
        self.face_detection_model = Path(env_face_weights) if env_face_weights else self.yolo_base_path / "yolov11n-face.pt"
        
        # 表情识别模型路径（优先使用训练好的模型）
        self.emotion_model_paths = [
            # 环境变量指定的权重（最高优先级）
            Path(os.getenv("EMOTION_MODEL_PATH")) if os.getenv("EMOTION_MODEL_PATH") else None,
            
            # 本地训练的表情识别模型（最高优先级）
            self.yolo_base_path / "runs" / "classify" / "fer2013_plus_optimized" / "weights" / "best.pt",
            self.yolo_base_path / "runs" / "classify" / "emotion_quick_train" / "weights" / "best.pt",
            self.yolo_base_path / "runs" / "classify" / "emotion_simple_train" / "weights" / "best.pt",
            self.yolo_base_path / "runs" / "classify" / "emotion_minimal_train" / "weights" / "best.pt",
            
            # 训练好的表情识别模型
            Path(__file__).parent / "trained_models" / "emotion_recognition_model.pt",
            Path(__file__).parent / "trained_models" / "emotion_recognition_best.pt",
            Path(__file__).parent / "trained_models" / "emotion_quick_train.pt",
            
            # 备选：使用通用分类模型（如果本地模型不可用）
            self.yolo_base_path / "yolo11n-cls.pt",  # 通用分类模型
        ]
        
        # 字体配置
        env_font_path = os.getenv("FONT_PATH")
        self.font_paths = [
            env_font_path if env_font_path else None,
            "C:/Windows/Fonts/simhei.ttf",
            "C:/Windows/Fonts/simsun.ttc", 
            "C:/Windows/Fonts/msyh.ttc",
            str(self.yolo_base_path / "fonts" / "font.ttf")
        ]
        
        # 模型配置
        self.model_config = {
            "face_detection_confidence": 0.5,
            "emotion_recognition_confidence": 0.3,
            "max_faces_per_image": 10,
            "image_processing_size": (640, 640),
            "video_analysis_interval": 10  # 每10帧分析一次
        }
        
        # 文件处理配置
        self.file_config = {
            "max_image_size": 10 * 1024 * 1024,  # 10MB
            "max_video_size": 100 * 1024 * 1024,  # 100MB
            "allowed_image_extensions": {'.png', '.jpg', '.jpeg', '.gif', '.bmp'},
            "allowed_video_extensions": {'.mp4', '.avi', '.mov', '.wmv', '.flv', '.mkv'}
        }
        
        # 表情标签配置
        self.emotion_labels = {
            "chinese": ['愤怒', '厌恶', '恐惧', '高兴', '悲伤', '惊讶', '中性'],
            "english": ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral'],
            "fer2013": ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']
        }
        
        # 职业评估配置
        self.career_evaluation_config = {
            "positive_emotions": ['高兴', '中性', '惊讶'],
            "negative_emotions": ['愤怒', '厌恶', '恐惧', '悲伤'],
            "confidence_thresholds": {
                "high": 0.8,
                "medium": 0.6,
                "low": 0.4
            },
            "score_weights": {
                "emotional_stability": 0.4,
                "confidence": 0.3,
                "professionalism": 0.3
            }
        }
    
    def get_face_detection_model_path(self) -> str:
        """获取人脸检测模型路径"""
        return str(self.face_detection_model)
    
    def get_emotion_recognition_model_path(self) -> str:
        """获取表情识别模型路径，返回第一个存在的路径"""
        for path in self.emotion_model_paths:
            if path and Path(path).exists():
                return str(path)
        return None
    
    def get_font_path(self) -> str:
        """获取字体路径，返回第一个存在的路径"""
        for path in self.font_paths:
            if path and os.path.exists(path):
                return path
        return None
    
    def check_models_availability(self) -> dict:
        """检查模型可用性"""
        status = {
            "face_detection_model": self.face_detection_model.exists(),
            "emotion_recognition_model": self.get_emotion_recognition_model_path() is not None,
            "font": self.get_font_path() is not None,
            "yolo_base_path": self.yolo_base_path.exists()
        }
        
        status["all_available"] = all([
            status["face_detection_model"],
            status["emotion_recognition_model"],
            status["font"]
        ])
        
        return status
    
    def get_model_config(self, key: str = None):
        """获取模型配置"""
        if key:
            return self.model_config.get(key)
        return self.model_config
    
    def get_file_config(self, key: str = None):
        """获取文件配置"""
        if key:
            return self.file_config.get(key)
        return self.file_config
    
    def get_emotion_labels(self, language: str = "chinese") -> list:
        """获取表情标签"""
        return self.emotion_labels.get(language, self.emotion_labels["chinese"])
    
    def get_career_evaluation_config(self, key: str = None):
        """获取职业评估配置"""
        if key:
            return self.career_evaluation_config.get(key)
        return self.career_evaluation_config
    
    def validate_file_upload(self, filename: str, file_size: int, file_type: str) -> dict:
        """
        验证文件上传
        
        Args:
            filename: 文件名
            file_size: 文件大小（字节）
            file_type: 文件类型（'image' 或 'video'）
            
        Returns:
            dict: 验证结果
        """
        result = {
            "valid": True,
            "errors": [],
            "warnings": []
        }
        
        # 检查文件扩展名
        file_ext = Path(filename).suffix.lower()
        if file_type == "image":
            allowed_exts = self.file_config["allowed_image_extensions"]
            max_size = self.file_config["max_image_size"]
        else:
            allowed_exts = self.file_config["allowed_video_extensions"]
            max_size = self.file_config["max_video_size"]
        
        if file_ext not in allowed_exts:
            result["valid"] = False
            result["errors"].append(f"不支持的文件类型: {file_ext}")
        
        # 检查文件大小
        if file_size > max_size:
            result["valid"] = False
            result["errors"].append(f"文件大小超过限制: {file_size / (1024*1024):.1f}MB > {max_size / (1024*1024):.1f}MB")
        
        # 检查文件名安全性
        if not filename or filename.strip() == "":
            result["valid"] = False
            result["errors"].append("文件名不能为空")
        
        return result
    
    def get_system_info(self) -> dict:
        """获取系统信息"""
        import platform
        import sys
        
        return {
            "python_version": sys.version,
            "platform": platform.platform(),
            "architecture": platform.architecture(),
            "processor": platform.processor(),
            "project_root": str(self.project_root),
            "yolo_base_path": str(self.yolo_base_path),
            "models_status": self.check_models_availability()
        }

# 创建全局配置实例
ai_config = AIConfig()

def get_ai_config() -> AIConfig:
    """获取AI配置实例"""
    return ai_config
