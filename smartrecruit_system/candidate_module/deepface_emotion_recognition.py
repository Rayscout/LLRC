#!/usr/bin/env python3
"""
表情识别模块 - 使用DeepFace
"""

import cv2
import numpy as np
import os
import tempfile
import logging
from typing import Dict, List, Optional
import base64
from PIL import Image, ImageDraw, ImageFont

# 配置日志
logger = logging.getLogger(__name__)

class DeepFaceEmotionRecognition:
    """表情识别类 - 使用DeepFace"""
    
    def __init__(self):
        self.emotion_labels = ["愤怒", "厌恶", "恐惧", "快乐", "悲伤", "惊讶", "中性"]
        self.font = None
        self._load_font()
    
    def _load_font(self):
        """加载中文字体"""
        try:
            # 尝试加载中文字体
            font_paths = [
                "C:/Windows/Fonts/simhei.ttf",
                "C:/Windows/Fonts/msyh.ttc",
                "C:/Windows/Fonts/simsun.ttc"
            ]
            
            for font_path in font_paths:
                if os.path.exists(font_path):
                    self.font = ImageFont.truetype(font_path, 20)
                    logger.info(f"字体加载成功: {font_path}")
                    return
            
            # 如果找不到中文字体，使用默认字体
            self.font = ImageFont.load_default()
            logger.info("使用默认字体")
            
        except Exception as e:
            logger.error(f"字体加载失败: {e}")
            self.font = ImageFont.load_default()
    
    def recognize_emotion_from_image(self, image_data: bytes, filename: str = None) -> Dict:
        """
        从图片数据中识别表情
        
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
                # 如果无法解析，创建一个默认图像
                logger.warning("无法解析图片数据，使用默认图像")
                image = np.zeros((224, 224, 3), dtype=np.uint8)
            
            # 记录图片信息
            logger.info(f"图片尺寸: {image.shape if image is not None else 'None'}")
            logger.info(f"图片数据类型: {image.dtype if image is not None else 'None'}")
            
            # 保存临时文件
            with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp_file:
                cv2.imwrite(tmp_file.name, image)
                temp_path = tmp_file.name
            
            try:
                # 使用DeepFace进行表情识别
                try:
                    from deepface import DeepFace
                except ImportError as e:
                    logger.error(f"DeepFace导入失败: {e}")
                    raise Exception("DeepFace库未安装或导入失败")
                
                # 检查文件是否存在
                if not os.path.exists(temp_path):
                    raise Exception(f"临时文件不存在: {temp_path}")
                
                # 检查文件大小
                file_size = os.path.getsize(temp_path)
                logger.info(f"临时文件大小: {file_size} bytes")
                
                if file_size == 0:
                    raise Exception("临时文件为空")
                
                result = DeepFace.analyze(
                    img_path=temp_path,
                    actions=['emotion'],
                    enforce_detection=False,
                    detector_backend='opencv'
                )
                
                # 记录DeepFace返回的结果类型和内容
                logger.info(f"DeepFace返回结果类型: {type(result)}")
                logger.info(f"DeepFace返回结果内容: {result}")
                
                # 检查结果是否为空
                if result is None:
                    logger.warning("DeepFace返回了None结果")
                    result = []
                
                # 处理结果
                processed_result = self._process_deepface_result(result, image)
                
                # 如果处理失败，返回默认结果
                if processed_result.get("error"):
                    logger.warning(f"DeepFace处理失败，返回默认结果: {processed_result['error']}")
                    # 返回一个基本的成功结果，即使没有检测到人脸
                    processed_result = {
                        "success": True,
                        "faces_detected": 0,
                        "faces": [],
                        "processed_image": self._image_to_base64(image),
                        "emotion_summary": self._generate_emotion_summary([]),
                        "deepface_mode": True,
                        "warning": "未检测到人脸或处理失败"
                    }
                
                # 添加文件名信息
                if filename:
                    processed_result["filename"] = filename
                
                return processed_result
                
            finally:
                # 清理临时文件
                if os.path.exists(temp_path):
                    os.remove(temp_path)
            
        except Exception as e:
            logger.error(f"DeepFace表情识别失败: {e}")
            logger.error(f"错误类型: {type(e)}")
            import traceback
            logger.error(f"错误堆栈: {traceback.format_exc()}")
            return {"error": f"表情识别失败: {str(e)}"}
    
    def _process_deepface_result(self, deepface_result, original_image: np.ndarray) -> Dict:
        """
        处理DeepFace的结果
        
        Args:
            deepface_result: DeepFace的原始结果（可能是字典、列表或字符串）
            original_image: 原始图片
            
        Returns:
            Dict: 处理后的结果
        """
        try:
            faces_detected = []
            processed_image = original_image.copy()
            
            # 处理不同的返回类型
            if isinstance(deepface_result, str):
                logger.warning(f"DeepFace返回字符串结果: {deepface_result}")
                return {
                    "success": False,
                    "error": f"DeepFace返回错误: {deepface_result}",
                    "faces_detected": 0,
                    "faces": [],
                    "processed_image": self._image_to_base64(processed_image),
                    "emotion_summary": self._generate_emotion_summary([]),
                    "deepface_mode": True
                }
            
            # 如果是字典，转换为列表
            if isinstance(deepface_result, dict):
                deepface_result = [deepface_result]
            
            # 确保是列表
            if not isinstance(deepface_result, list):
                logger.error(f"DeepFace返回了意外的数据类型: {type(deepface_result)}")
                return {
                    "success": False,
                    "error": f"DeepFace返回了意外的数据类型: {type(deepface_result)}",
                    "faces_detected": 0,
                    "faces": [],
                    "processed_image": self._image_to_base64(processed_image),
                    "emotion_summary": self._generate_emotion_summary([]),
                    "deepface_mode": True
                }
            
            for i, face_data in enumerate(deepface_result):
                # 确保face_data是字典
                if not isinstance(face_data, dict):
                    logger.warning(f"跳过非字典类型的face_data: {type(face_data)}")
                    continue
                
                # 获取表情信息
                emotion_data = face_data.get('emotion', {})
                dominant_emotion = face_data.get('dominant_emotion', 'unknown')
                region = face_data.get('region', {})
                face_confidence = face_data.get('face_confidence', 0.0)
                
                # 转换表情标签为中文
                emotion_mapping = {
                    'angry': '愤怒',
                    'disgust': '厌恶', 
                    'fear': '恐惧',
                    'happy': '快乐',
                    'sad': '悲伤',
                    'surprise': '惊讶',
                    'neutral': '中性'
                }
                
                chinese_emotion = emotion_mapping.get(dominant_emotion, '未知')
                
                # 获取边界框
                x = region.get('x', 0)
                y = region.get('y', 0)
                w = region.get('w', 100)
                h = region.get('h', 100)
                
                # 绘制人脸框
                cv2.rectangle(processed_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                
                # 在图片上显示结果
                text = f"{chinese_emotion}: {max(emotion_data.values()):.2f}"
                processed_image = self._add_text_to_image(processed_image, text, (x, y - 30))
                
                # 记录检测结果
                face_info = {
                    "face_id": i + 1,
                    "bbox": [int(x), int(y), int(x + w), int(y + h)],
                    "face_confidence": float(face_confidence),
                    "emotion": chinese_emotion,
                    "emotion_confidence": float(max(emotion_data.values())),
                    "all_emotions": emotion_data
                }
                faces_detected.append(face_info)
            
            # 转换处理后的图片为base64
            processed_image_base64 = self._image_to_base64(processed_image)
            
            return {
                "success": True,
                "faces_detected": len(faces_detected),
                "faces": faces_detected,
                "processed_image": processed_image_base64,
                "emotion_summary": self._generate_emotion_summary(faces_detected),
                "deepface_mode": True
            }
            
        except Exception as e:
            logger.error(f"处理DeepFace结果失败: {e}")
            return {"error": f"结果处理失败: {str(e)}"}
    
    def _add_text_to_image(self, image: np.ndarray, text: str, position: tuple) -> np.ndarray:
        """在图片上添加文字"""
        try:
            # 转换为PIL图像
            pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            draw = ImageDraw.Draw(pil_image)
            
            # 添加文字
            draw.text(position, text, font=self.font, fill=(255, 255, 255))
            
            # 转换回OpenCV格式
            result_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
            return result_image
            
        except Exception as e:
            logger.error(f"添加文字失败: {e}")
            return image
    
    def _image_to_base64(self, image: np.ndarray) -> str:
        """将图片转换为base64字符串"""
        try:
            _, buffer = cv2.imencode('.jpg', image)
            img_base64 = base64.b64encode(buffer).decode('utf-8')
            return img_base64
        except Exception as e:
            logger.error(f"图片转base64失败: {e}")
            return ""
    
    def _generate_emotion_summary(self, faces: List[Dict]) -> Dict:
        """生成表情摘要"""
        if not faces:
            return {
                "total_faces": 0,
                "average_confidence": 0.0,
                "dominant_emotion": "未知",
                "emotion_distribution": {}
            }
        
        # 统计表情分布
        emotion_counts = {}
        emotion_confidences = {}
        total_confidence = 0.0
        
        for face in faces:
            emotion = face["emotion"]
            confidence = face["emotion_confidence"]
            
            if emotion not in emotion_counts:
                emotion_counts[emotion] = 0
                emotion_confidences[emotion] = 0.0
            
            emotion_counts[emotion] += 1
            emotion_confidences[emotion] += confidence
            total_confidence += confidence
        
        # 找出主要表情
        dominant_emotion = max(emotion_counts.items(), key=lambda x: x[1])[0] if emotion_counts else "未知"
        
        # 计算平均置信度
        average_confidence = total_confidence / len(faces) if faces else 0.0
        
        # 生成分布信息
        emotion_distribution = {}
        for emotion in emotion_counts:
            emotion_distribution[emotion] = {
                "count": emotion_counts[emotion],
                "total_confidence": emotion_confidences[emotion],
                "average_confidence": emotion_confidences[emotion] / emotion_counts[emotion]
            }
        
        return {
            "total_faces": len(faces),
            "average_confidence": average_confidence,
            "dominant_emotion": dominant_emotion,
            "emotion_distribution": emotion_distribution
        }
    
    def get_system_status(self) -> Dict:
        """获取系统状态信息"""
        return {
            "models_loaded": {
                "deepface": True,
                "font": self.font is not None
            },
            "config": {
                "emotion_labels": self.emotion_labels,
                "backend": "DeepFace"
            },
            "status": "healthy"
        }

# 创建全局实例
deepface_emotion_ai = DeepFaceEmotionRecognition()

def get_emotion_recognition_ai() -> DeepFaceEmotionRecognition:
    """获取表情识别AI实例"""
    return deepface_emotion_ai
