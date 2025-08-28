import cv2
import numpy as np
import os
import tempfile
from PIL import Image, ImageDraw, ImageFont
import logging
from typing import Dict, List, Tuple, Optional
import base64
import io
import random
import time

# 配置日志
logger = logging.getLogger(__name__)

class SimpleEmotionRecognition:
    """简化版表情识别模块，用于测试和演示"""
    
    def __init__(self):
        self.emotion_labels = ['愤怒', '厌恶', '恐惧', '高兴', '悲伤', '惊讶', '中性']
        self.font = None
        self._load_font()
        
    def _load_font(self):
        """加载中文字体"""
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
            
            if not self.font:
                self.font = ImageFont.load_default()
                logger.info("使用默认字体")
                
        except Exception as e:
            logger.error(f"字体加载失败: {e}")
            self.font = ImageFont.load_default()
    
    def recognize_emotion_from_image(self, image_data: bytes, filename: str = None) -> Dict:
        """
        从图片数据中识别表情（模拟版本）
        
        Args:
            image_data: 图片的二进制数据
            filename: 文件名（可选）
            
        Returns:
            Dict: 包含识别结果的字典
        """
        try:
            # 将二进制数据转换为numpy数组
            nparr = np.frombuffer(image_data, np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            if image is None:
                return {"error": "无法解析图片数据"}
            
            # 进行模拟表情识别
            result = self._process_image_simple(image)
            
            # 添加文件名信息
            if filename:
                result["filename"] = filename
            
            return result
            
        except Exception as e:
            logger.error(f"表情识别失败: {e}")
            return {"error": f"表情识别失败: {str(e)}"}
    
    def _process_image_simple(self, image: np.ndarray) -> Dict:
        """
        处理图片进行模拟表情识别
        
        Args:
            image: OpenCV格式的图片
            
        Returns:
            Dict: 识别结果
        """
        try:
            # 获取图片尺寸
            height, width = image.shape[:2]
            
            # 模拟检测到的人脸（在图片中心区域）
            center_x, center_y = width // 2, height // 2
            face_size = min(width, height) // 4
            
            x1 = max(0, center_x - face_size)
            y1 = max(0, center_y - face_size)
            x2 = min(width, center_x + face_size)
            y2 = min(height, center_y + face_size)
            
            # 模拟表情识别结果
            emotion_result = self._simulate_emotion_recognition()
            
            # 在图片上绘制人脸框和结果
            processed_image = image.copy()
            cv2.rectangle(processed_image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
            # 添加文本
            text = f"{emotion_result['emotion']}: {emotion_result['confidence']:.2f}"
            processed_image = self._add_text_to_image(processed_image, text, (x1, y1 - 30))
            
            # 记录检测结果
            face_info = {
                "face_id": 1,
                "bbox": [int(x1), int(y1), int(x2), int(y2)],
                "face_confidence": 0.95,
                "emotion": emotion_result["emotion"],
                "emotion_confidence": float(emotion_result["confidence"])
            }
            
            # 转换处理后的图片为base64
            processed_image_base64 = self._image_to_base64(processed_image)
            
            return {
                "success": True,
                "faces_detected": 1,
                "faces": [face_info],
                "processed_image": processed_image_base64,
                "emotion_summary": self._generate_emotion_summary([face_info])
            }
            
        except Exception as e:
            logger.error(f"图片处理失败: {e}")
            return {"error": f"图片处理失败: {str(e)}"}
    
    def _simulate_emotion_recognition(self) -> Dict:
        """
        模拟表情识别结果
        
        Returns:
            Dict: 模拟的表情识别结果
        """
        # 随机选择一个表情，但偏向于积极情绪
        weights = [0.1, 0.05, 0.05, 0.4, 0.1, 0.1, 0.2]  # 高兴和中性概率更高
        emotion_idx = random.choices(range(len(self.emotion_labels)), weights=weights)[0]
        emotion = self.emotion_labels[emotion_idx]
        
        # 生成合理的置信度
        if emotion in ['高兴', '中性']:
            confidence = random.uniform(0.7, 0.95)  # 积极情绪置信度较高
        else:
            confidence = random.uniform(0.5, 0.85)  # 其他情绪置信度适中
        
        return {
            "emotion": emotion,
            "confidence": confidence,
            "all_probabilities": {label: random.uniform(0.1, 0.3) for label in self.emotion_labels}
        }
    
    def _add_text_to_image(self, image: np.ndarray, text: str, position: Tuple[int, int]) -> np.ndarray:
        """
        在图片上添加中文文本
        
        Args:
            image: OpenCV格式图片
            text: 要添加的文本
            position: 文本位置 (x, y)
            
        Returns:
            np.ndarray: 添加文本后的图片
        """
        try:
            if self.font and self.font != ImageFont.load_default():
                # 使用PIL绘制中文
                img_pil = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
                draw = ImageDraw.Draw(img_pil)
                draw.text(position, text, font=self.font, fill=(255, 255, 255))
                return cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
            else:
                # 使用OpenCV默认方法
                cv2.putText(image, text, position, cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                return image
        except Exception as e:
            logger.error(f"添加文本失败: {e}")
            return image
    
    def _image_to_base64(self, image: np.ndarray) -> str:
        """
        将OpenCV图片转换为base64字符串
        
        Args:
            image: OpenCV格式图片
            
        Returns:
            str: base64编码的图片字符串
        """
        try:
            # 编码为JPEG格式
            _, buffer = cv2.imencode('.jpg', image)
            # 转换为base64
            img_base64 = base64.b64encode(buffer).decode('utf-8')
            return f"data:image/jpeg;base64,{img_base64}"
        except Exception as e:
            logger.error(f"图片转base64失败: {e}")
            return ""
    
    def _generate_emotion_summary(self, faces: List[Dict]) -> Dict:
        """
        生成表情统计摘要
        
        Args:
            faces: 检测到的人脸列表
            
        Returns:
            Dict: 表情统计摘要
        """
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
        
        # 计算平均置信度
        avg_confidence = total_confidence / len(faces) if faces else 0
        
        # 找出主要表情
        if emotion_counts:
            try:
                dominant_emotion = max(emotion_counts.items(), key=lambda x: x[1]["count"])[0]
            except (ValueError, KeyError):
                dominant_emotion = "未知"
        else:
            dominant_emotion = "未知"
        
        return {
            "total_faces": len(faces),
            "average_confidence": avg_confidence,
            "dominant_emotion": dominant_emotion,
            "emotion_distribution": emotion_counts
        }
    
    def get_system_status(self) -> Dict:
        """
        获取系统状态信息
        
        Returns:
            Dict: 系统状态
        """
        return {
            "models_loaded": {
                "face_detection": True,  # 模拟版本总是可用
                "emotion_recognition": True,  # 模拟版本总是可用
                "font": self.font is not None
            },
            "config": {
                "emotion_labels": self.emotion_labels,
                "model_config": {
                    "face_detection_confidence": 0.5,
                    "emotion_recognition_confidence": 0.3,
                    "max_faces_per_image": 10,
                    "image_processing_size": (640, 640),
                    "video_analysis_interval": 10
                },
                "file_config": {
                    "max_image_size": 10 * 1024 * 1024,
                    "max_video_size": 100 * 1024 * 1024,
                    "allowed_image_extensions": {'.png', '.jpg', '.jpeg', '.gif', '.bmp'},
                    "allowed_video_extensions": {'.mp4', '.avi', '.mov', '.wmv', '.flv', '.mkv'}
                }
            },
            "models_availability": {
                "face_detection_model": True,
                "emotion_recognition_model": True,
                "font": self.font is not None,
                "yolo_base_path": False,  # 模拟版本不需要YOLO路径
                "all_available": True
            },
            "note": "这是模拟版本的表情识别模块，用于测试和演示"
        }

# 创建全局实例
simple_emotion_ai = SimpleEmotionRecognition()

def get_simple_emotion_recognition_ai() -> SimpleEmotionRecognition:
    """获取简化版表情识别AI实例"""
    return simple_emotion_ai
