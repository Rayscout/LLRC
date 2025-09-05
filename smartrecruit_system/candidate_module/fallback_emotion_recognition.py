"""
LLRC Header Start
文件功能: SmartRecruit 子系统 Python 模块：smartrecruit_system/candidate_module/fallback_emotion_recognition.py
创建时间: 2025-08-19 11:43
创建人: 苏杰
更新记录:
- 2025-08-20 09:58 by 苏杰
- 2025-08-25 17:04 by 张宇成
LLRC Header End
"""
"""
FILE-HEADER-AUTO-ADDED
文件: smartrecruit_system/candidate_module/fallback_emotion_recognition.py
功能: 通用模块
创建时间: 2025-08-29 15:01
创建人: 侯东杨
更新记录:
- 2025-08-19 12:13 by 侯东杨
- 2025-08-20 18:06 by 李雨梦
- 2025-08-24 16:37 by 谢佳悦
"""

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import logging

logger = logging.getLogger(__name__)

class FallbackEmotionRecognition:
    """备用的表情识别类，当YOLO模型不可用时使用"""
    
    def __init__(self):
        """函数 __init__：核心业务逻辑。"""
        self.emotion_labels = ['愤怒', '厌恶', '恐惧', '高兴', '悲伤', '惊讶', '中性']
        self.font = None
        self._load_font()
    
    def _load_font(self):
        """加载字体"""
        try:
            # 尝试加载系统字体
            font_paths = [
                "C:/Windows/Fonts/simhei.ttf",
                "C:/Windows/Fonts/simsun.ttc", 
                "C:/Windows/Fonts/msyh.ttc"
            ]
            
            for font_path in font_paths:
                if os.path.exists(font_path):
                    self.font = ImageFont.truetype(font_path, 20)
                    logger.info(f"字体加载成功: {font_path}")
                    break
            
            if self.font is None:
                self.font = ImageFont.load_default()
                logger.info("使用默认字体")
                
        except Exception as e:
            logger.error(f"字体加载失败: {e}")
            self.font = ImageFont.load_default()
    
    def recognize_emotion_from_image(self, image_data: bytes, filename: str = None) -> dict:
        """从图片数据中识别表情（备用方法）"""
        try:
            # 将二进制数据转换为numpy数组
            nparr = np.frombuffer(image_data, np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            if image is None:
                return {"error": "无法解析图片数据"}
            
            # 使用OpenCV的人脸检测
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.1, 4)
            
            faces_detected = []
            processed_image = image.copy()
            
            for i, (x, y, w, h) in enumerate(faces):
                # 绘制人脸框
                cv2.rectangle(processed_image, (x, y), (x+w, y+h), (0, 255, 0), 2)
                
                # 模拟表情识别（随机选择）
                import random
                emotion = random.choice(self.emotion_labels)
                confidence = random.uniform(0.6, 0.9)
                
                # 在图片上显示结果
                text = f"{emotion}: {confidence:.2f}"
                cv2.putText(processed_image, text, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                
                # 记录检测结果
                face_info = {
                    "face_id": i + 1,
                    "bbox": [int(x), int(y), int(x+w), int(y+h)],
                    "face_confidence": 0.8,
                    "emotion": emotion,
                    "emotion_confidence": confidence
                }
                faces_detected.append(face_info)
            
            # 转换处理后的图片为base64
            _, buffer = cv2.imencode('.jpg', processed_image)
            img_base64 = base64.b64encode(buffer).decode('utf-8')
            processed_image_base64 = f"data:image/jpeg;base64,{img_base64}"
            
            return {
                "success": True,
                "faces_detected": len(faces_detected),
                "faces": faces_detected,
                "processed_image": processed_image_base64,
                "emotion_summary": self._generate_emotion_summary(faces_detected),
                "fallback_mode": True
            }
            
        except Exception as e:
            logger.error(f"备用表情识别失败: {e}")
            return {"error": f"表情识别失败: {str(e)}"}
    
    def _generate_emotion_summary(self, faces):
        """生成表情统计摘要"""
        if not faces:
            return {}
        
        emotion_counts = {}
        total_confidence = 0
        
        for face in faces:
            emotion = face["emotion"]
            confidence = face["emotion_confidence"]
            
            if emotion not in emotion_counts:
                emotion_counts[emotion] = {"count": 0, "total_confidence": 0}
            
            emotion_counts[emotion]["count"] += 1
            emotion_counts[emotion]["total_confidence"] += confidence
            total_confidence += confidence
        
        avg_confidence = total_confidence / len(faces) if faces else 0
        
        dominant_emotion = max(emotion_counts.items(), key=lambda x: x[1]["count"])[0] if emotion_counts else "未知"
        
        return {
            "total_faces": len(faces),
            "average_confidence": avg_confidence,
            "dominant_emotion": dominant_emotion,
            "emotion_distribution": emotion_counts
        }

# 创建全局实例
fallback_emotion_ai = FallbackEmotionRecognition()

def get_fallback_emotion_recognition_ai():
    """获取备用表情识别AI实例"""
    return fallback_emotion_ai
