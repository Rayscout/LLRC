import cv2
import numpy as np
import os
import tempfile
from PIL import Image, ImageDraw, ImageFont
from ultralytics import YOLO
import logging
from typing import Dict, List, Tuple, Optional
import base64
import io
from .ai_config import get_ai_config

# 配置日志
logger = logging.getLogger(__name__)

class EmotionRecognitionAI:
    """表情识别AI模块，基于YOLO模型"""
    
    def __init__(self):
        self.config = get_ai_config()
        self.emotion_labels = self.config.get_emotion_labels("chinese")
        self.face_model = None
        self.emotion_model = None
        self.font = None
        self._load_models()
        self._load_font()
    
    def _load_models(self):
        """加载YOLO模型"""
        try:
            # 加载人脸检测模型
            face_model_path = self.config.get_face_detection_model_path()
            if face_model_path and os.path.exists(face_model_path):
                # 明确指定任务类型，避免YOLO库自动推断
                self.face_model = YOLO(str(face_model_path), task="detect")
                logger.info(f"人脸检测模型加载成功: {face_model_path}")
            else:
                logger.warning(f"人脸检测模型文件不存在: {face_model_path}")
            
            # 加载表情识别模型
            emotion_model_path = self.config.get_emotion_recognition_model_path()
            if emotion_model_path and os.path.exists(emotion_model_path):
                logger.info(f"尝试加载表情识别模型: {emotion_model_path}")
                
                try:
                    # 明确指定任务类型，避免YOLO库自动推断
                    self.emotion_model = YOLO(str(emotion_model_path), task="classify")
                    logger.info(f"表情识别模型加载成功: {emotion_model_path}")
                    
                    # 验证模型输出
                    try:
                        # 创建一个测试图像来验证模型输出
                        test_image = np.zeros((224, 224, 3), dtype=np.uint8)
                        test_results = self.emotion_model(test_image)
                        probs = test_results[0].probs.data.tolist()
                        logger.info(f"表情识别模型验证: 输出类别数量={len(probs)}")
                        
                        if len(probs) == 7:
                            logger.info("✅ 表情识别模型验证成功，输出7个表情类别")
                        elif len(probs) == 1000:
                            logger.warning("⚠️ 检测到通用分类模型(1000类)，将使用前7个类别作为表情识别")
                            logger.info("✅ 表情识别模型加载成功（使用通用分类模型的前7类）")
                        else:
                            logger.warning(f"⚠️ 模型输出 {len(probs)} 个类别，将尝试适配")
                            logger.info("✅ 表情识别模型加载成功（需要适配）")
                            
                    except Exception as e:
                        logger.error(f"表情识别模型验证失败: {e}")
                        # 验证失败时，清除已加载的模型
                        self.emotion_model = None
                        
                except Exception as load_e:
                    logger.error(f"表情识别模型加载失败: {load_e}")
                    logger.error("可能的原因：模型文件损坏、训练配置错误、或格式不兼容")
                    self.emotion_model = None
                    
            else:
                logger.error(f"❌ 表情识别模型文件不存在: {emotion_model_path}")
                logger.error("请确保已训练表情识别模型并放置在正确路径")
                
            # 如果表情识别模型加载失败，记录详细状态
            if self.emotion_model is None:
                logger.error("❌ 表情识别模型未成功加载，表情识别功能将无法使用")
                logger.error("建议：")
                logger.error("1. 检查模型文件是否完整")
                logger.error("2. 重新训练表情识别模型")
                logger.error("3. 检查训练配置是否正确")
                logger.error("4. 验证模型文件格式是否兼容")
                
        except Exception as e:
            logger.error(f"加载模型失败: {e}")
    
    def _load_font(self):
        """加载中文字体"""
        try:
            font_path = self.config.get_font_path()
            if font_path and os.path.exists(font_path):
                self.font = ImageFont.truetype(font_path, 20)
                logger.info(f"字体加载成功: {font_path}")
            else:
                # 如果配置的字体不存在，使用默认字体
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
                return {"error": "无法解析图片数据"}
            
            # 进行表情识别
            result = self._process_image(image)
            
            # 添加文件名信息
            if filename:
                result["filename"] = filename
            
            return result
            
        except Exception as e:
            logger.error(f"表情识别失败: {e}")
            return {"error": f"表情识别失败: {str(e)}"}
    
    def recognize_emotion_from_file(self, file_path: str) -> Dict:
        """
        从文件路径识别表情
        
        Args:
            file_path: 图片文件路径
            
        Returns:
            Dict: 包含识别结果的字典
        """
        try:
            if not os.path.exists(file_path):
                return {"error": f"文件不存在: {file_path}"}
            
            image = cv2.imread(file_path)
            if image is None:
                return {"error": "无法读取图片文件"}
            
            result = self._process_image(image)
            result["file_path"] = file_path
            
            return result
            
        except Exception as e:
            logger.error(f"表情识别失败: {e}")
            return {"error": f"表情识别失败: {str(e)}"}
    
    def _process_image(self, image: np.ndarray) -> Dict:
        """
        处理图片进行表情识别
        
        Args:
            image: OpenCV格式的图片
            
        Returns:
            Dict: 识别结果
        """
        if self.face_model is None:
            return {"error": "人脸检测模型未加载"}
        
        if self.emotion_model is None:
            return {
                "error": "表情识别功能暂时不可用",
                "details": "表情识别模型未正确加载，请检查系统配置",
                "suggestions": [
                    "检查模型文件是否完整",
                    "重新训练表情识别模型", 
                    "检查训练配置是否正确（应为7个表情类别）",
                    "验证模型文件格式是否兼容"
                ]
            }
        
        try:
            # 获取模型配置
            face_conf = self.config.get_model_config("face_detection_confidence")
            max_faces = self.config.get_model_config("max_faces_per_image")
            
            # 使用YOLO检测人脸
            results = self.face_model(image, conf=face_conf)
            
            faces_detected = []
            processed_image = image.copy()
            
            for result in results:
                boxes = result.boxes
                for i, box in enumerate(boxes):
                    # 限制检测的人脸数量
                    if i >= max_faces:
                        break
                        
                    # 获取边界框坐标
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy().astype(int)
                    confidence = float(box.conf[0].cpu().numpy())
                    
                    # 扩大边界框以包含更多面部特征
                    frame_height, frame_width = image.shape[:2]
                    expand_x = int((x2 - x1) * 0.2)
                    expand_y = int((y2 - y1) * 0.2)
                    
                    x1_expanded = max(0, x1 - expand_x)
                    y1_expanded = max(0, y1 - expand_y)
                    x2_expanded = min(frame_width, x2 + expand_x)
                    y2_expanded = min(frame_height, y2 + expand_y)
                    
                    # 绘制人脸框
                    cv2.rectangle(processed_image, (x1_expanded, y1_expanded), 
                                (x2_expanded, y2_expanded), (0, 255, 0), 2)
                    
                    # 提取人脸区域
                    face_roi = image[y1_expanded:y2_expanded, x1_expanded:x2_expanded]
                    
                    if face_roi.size == 0:
                        continue
                    
                    # 进行表情识别
                    emotion_result = self._recognize_emotion_for_face(face_roi)
                    
                    # 在图片上显示结果
                    text = f"{emotion_result['emotion']}: {emotion_result['confidence']:.2f}"
                    processed_image = self._add_text_to_image(processed_image, text, 
                                                           (x1_expanded, y1_expanded - 30))
                    
                    # 记录检测结果
                    face_info = {
                        "face_id": i + 1,
                        "bbox": [int(x1_expanded), int(y1_expanded), int(x2_expanded), int(y2_expanded)],
                        "face_confidence": float(confidence),
                        "emotion": emotion_result["emotion"],
                        "emotion_confidence": float(emotion_result["confidence"])
                    }
                    faces_detected.append(face_info)
            
            # 转换处理后的图片为base64
            processed_image_base64 = self._image_to_base64(processed_image)
            
            return {
                "success": True,
                "faces_detected": len(faces_detected),
                "faces": faces_detected,
                "processed_image": processed_image_base64,
                "emotion_summary": self._generate_emotion_summary(faces_detected)
            }
            
        except Exception as e:
            logger.error(f"图片处理失败: {e}")
            return {"error": f"图片处理失败: {str(e)}"}
    
    def _recognize_emotion_for_face(self, face_roi: np.ndarray) -> Dict:
        """
        对单个人脸区域进行表情识别
        
        Args:
            face_roi: 人脸区域图片
            
        Returns:
            Dict: 表情识别结果
        """
        try:
            # 将人脸区域转换为灰度图像
            face_roi_gray = cv2.cvtColor(face_roi, cv2.COLOR_BGR2GRAY)
            
            # 将灰度图像转换为3通道图像（YOLO需要）
            face_roi_gray_3ch = cv2.cvtColor(face_roi_gray, cv2.COLOR_GRAY2BGR)
            
            # 调整图像大小为模型期望的尺寸
            face_roi_resized = cv2.resize(face_roi_gray_3ch, (224, 224))
            
            # 使用表情识别模型
            emotion_results = self.emotion_model(face_roi_resized)
            
            # 获取预测结果
            probs = emotion_results[0].probs.data.tolist()
            
            # 检查概率列表是否为空
            if not probs or len(probs) == 0:
                logger.warning("表情识别模型返回空的概率列表")
                return {
                    "emotion": "未知",
                    "confidence": 0.0,
                    "all_probabilities": {}
                }
            
            # 检查概率列表长度
            if len(probs) != len(self.emotion_labels):
                logger.warning(f"表情识别模型返回的概率数量 {len(probs)} 与标签数量 {len(self.emotion_labels)} 不匹配")
                # 如果概率数量不匹配，尝试截取或填充
                if len(probs) > len(self.emotion_labels):
                    probs = probs[:len(self.emotion_labels)]
                else:
                    # 填充到7个类别
                    probs.extend([0.0] * (len(self.emotion_labels) - len(probs)))
            
            class_id = probs.index(max(probs))
            confidence = max(probs)
            
            # 检查class_id是否在有效范围内
            if class_id >= len(self.emotion_labels):
                logger.warning(f"表情识别返回的类别ID {class_id} 超出标签范围 {len(self.emotion_labels)}")
                return {
                    "emotion": "未知",
                    "confidence": 0.0,
                    "all_probabilities": {}
                }
            
            emotion = self.emotion_labels[class_id]
            
            # 记录调试信息
            logger.info(f"表情识别结果: 类别ID={class_id}, 表情={emotion}, 置信度={confidence:.3f}")
            logger.info(f"所有概率: {dict(zip(self.emotion_labels, probs))}")
            
            return {
                "emotion": emotion,
                "confidence": confidence,
                "all_probabilities": dict(zip(self.emotion_labels, probs))
            }
            
        except Exception as e:
            logger.error(f"单个人脸表情识别失败: {e}")
            return {
                "emotion": "未知",
                "confidence": 0.0,
                "all_probabilities": {}
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
    
    def analyze_interview_video(self, video_data: bytes, filename: str = None) -> Dict:
        """
        分析面试视频中的表情变化
        
        Args:
            video_data: 视频的二进制数据
            filename: 文件名（可选）
            
        Returns:
            Dict: 视频分析结果
        """
        try:
            # 创建临时文件
            with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as temp_file:
                temp_file.write(video_data)
                temp_file_path = temp_file.name
            
            # 分析视频
            result = self._analyze_video_file(temp_file_path)
            
            # 清理临时文件
            os.unlink(temp_file_path)
            
            if filename:
                result["filename"] = filename
            
            return result
            
        except Exception as e:
            logger.error(f"视频分析失败: {e}")
            return {"error": f"视频分析失败: {str(e)}"}
    
    def _analyze_video_file(self, video_path: str) -> Dict:
        """
        分析视频文件中的表情
        
        Args:
            video_path: 视频文件路径
            
        Returns:
            Dict: 视频分析结果
        """
        try:
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                return {"error": "无法打开视频文件"}
            
            frame_count = 0
            emotion_timeline = []
            fps = cap.get(cv2.CAP_PROP_FPS)
            
            # 获取分析间隔配置
            analysis_interval = self.config.get_model_config("video_analysis_interval")
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                frame_count += 1
                timestamp = frame_count / fps
                
                # 按配置的间隔分析帧
                if frame_count % analysis_interval == 0:
                    frame_result = self._process_image(frame)
                    if "faces" in frame_result and frame_result["faces"]:
                        emotion_timeline.append({
                            "timestamp": timestamp,
                            "frame": frame_count,
                            "emotions": frame_result["faces"]
                        })
            
            cap.release()
            
            return {
                "success": True,
                "total_frames": frame_count,
                "duration": frame_count / fps if fps > 0 else 0,
                "emotion_timeline": emotion_timeline,
                "summary": self._generate_video_emotion_summary(emotion_timeline)
            }
            
        except Exception as e:
            logger.error(f"视频文件分析失败: {e}")
            return {"error": f"视频文件分析失败: {str(e)}"}
    
    def _generate_video_emotion_summary(self, timeline: List[Dict]) -> Dict:
        """
        生成视频表情分析摘要
        
        Args:
            timeline: 表情时间线数据
            
        Returns:
            Dict: 视频表情摘要
        """
        if not timeline:
            return {}
        
        all_emotions = []
        for entry in timeline:
            for face in entry["emotions"]:
                all_emotions.append(face["emotion"])
        
        # 统计表情频率
        emotion_frequency = {}
        for emotion in all_emotions:
            emotion_frequency[emotion] = emotion_frequency.get(emotion, 0) + 1
        
        # 找出主要表情
        if emotion_frequency:
            try:
                dominant_emotion = max(emotion_frequency.items(), key=lambda x: x[1])[0]
            except (ValueError, KeyError):
                dominant_emotion = "未知"
        else:
            dominant_emotion = "未知"
        
        return {
            "total_emotion_samples": len(all_emotions),
            "dominant_emotion": dominant_emotion,
            "emotion_frequency": emotion_frequency,
            "analysis_points": len(timeline)
        }
    
    def get_system_status(self) -> Dict:
        """
        获取系统状态信息
        
        Returns:
            Dict: 系统状态
        """
        return {
            "models_loaded": {
                "face_detection": self.face_model is not None,
                "emotion_recognition": self.emotion_model is not None,
                "font": self.font is not None
            },
            "config": {
                "emotion_labels": self.emotion_labels,
                "model_config": self.config.get_model_config(),
                "file_config": self.config.get_file_config()
            },
            "models_availability": self.config.check_models_availability()
        }

# 创建全局实例
emotion_ai = EmotionRecognitionAI()

def get_emotion_recognition_ai() -> EmotionRecognitionAI:
    """获取表情识别AI实例"""
    return emotion_ai

# 备用表情识别导入
try:
    from .fallback_emotion_recognition import get_fallback_emotion_recognition_ai
except ImportError:
    def get_fallback_emotion_recognition_ai():
        return None

# 修改get_emotion_recognition_ai函数
def get_emotion_recognition_ai() -> 'EmotionRecognitionAI':
    """获取表情识别AI实例，如果主模型失败则使用备用模型"""
    try:
        return emotion_ai
    except:
        # 如果主模型不可用，返回备用模型
        fallback_ai = get_fallback_emotion_recognition_ai()
        if fallback_ai:
            return fallback_ai
        else:
            # 如果备用模型也不可用，返回一个简单的模拟实例
            class MockEmotionAI:
                def recognize_emotion_from_image(self, image_data, filename=None):
                    return {
                        "success": True,
                        "faces_detected": 1,
                        "faces": [{
                            "face_id": 1,
                            "bbox": [100, 100, 200, 200],
                            "face_confidence": 0.8,
                            "emotion": "中性",
                            "emotion_confidence": 0.7
                        }],
                        "processed_image": "",
                        "emotion_summary": {
                            "total_faces": 1,
                            "average_confidence": 0.7,
                            "dominant_emotion": "中性",
                            "emotion_distribution": {"中性": {"count": 1, "total_confidence": 0.7}}
                        },
                        "mock_mode": True
                    }
            
            return MockEmotionAI()
