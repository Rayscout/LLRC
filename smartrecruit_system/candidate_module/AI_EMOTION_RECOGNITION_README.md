# AI表情识别模块集成说明

## 概述

本模块将YOLO中的表情识别功能集成到candidate_module中，为智能招聘系统提供基于AI的候选人表情分析和面试表现评估功能。

## 功能特性

### 1. 表情识别分析
- **照片表情识别**: 分析候选人照片中的表情，识别7种基本情绪
- **多脸检测**: 支持同时检测和分析多个人脸
- **置信度评估**: 提供表情识别的置信度评分
- **职业洞察**: 基于表情分析生成职业素养评估

### 2. 面试视频分析
- **视频表情追踪**: 分析面试视频中的表情变化
- **情绪稳定性评估**: 评估候选人的情绪管理能力
- **表现评分**: 提供综合的候选人评分系统
- **时间线分析**: 生成表情变化的时间线数据

### 3. 智能评估系统
- **职业匹配度**: 基于表情特征推荐适合的岗位
- **面试建议**: 提供个性化的面试改进建议
- **风险评估**: 识别可能影响工作表现的情绪问题

## 技术架构

### 核心组件

1. **EmotionRecognitionAI类**: 主要的表情识别AI引擎
2. **AIConfig类**: 配置管理，包括模型路径、参数设置等
3. **API路由**: RESTful API接口，支持图片和视频上传分析
4. **集成模块**: 与现有candidate_ai.py的深度集成

### 依赖关系

```
candidate_module/
├── emotion_recognition.py      # 表情识别核心模块
├── ai_config.py               # AI配置管理
├── candidate_ai.py            # 增强的AI分析功能
├── ai_analysis_routes.py     # API路由接口
└── __init__.py               # 模块初始化
```

## 安装和配置

### 1. 安装依赖

```bash
# 安装AI模块依赖
pip install -r requirements_ai.txt

# 或者单独安装核心包
pip install ultralytics opencv-python torch torchvision
```

### 2. 模型文件配置

确保以下YOLO模型文件存在于正确路径：

```
YOLO/Facial-Expression-Recognition/
├── yolov11n-face.pt                    # 人脸检测模型
├── runs/classify/fer2013_plus_optimized/weights/best.pt  # 表情识别模型
└── fonts/font.ttf                      # 中文字体文件
```

### 3. 环境配置

```python
# 在ai_config.py中配置模型路径
yolo_base_path = "path/to/YOLO/Facial-Expression-Recognition"
```

## API接口说明

### 1. 表情识别接口

**POST** `/candidate/ai-analysis/emotion-analysis`

**请求参数:**
- `image`: 图片文件 (支持: png, jpg, jpeg, gif, bmp)

**响应示例:**
```json
{
  "success": true,
  "message": "表情分析完成",
  "data": {
    "faces_detected": 1,
    "faces": [
      {
        "face_id": 1,
        "bbox": [100, 100, 200, 200],
        "emotion": "高兴",
        "emotion_confidence": 0.85
      }
    ],
    "career_insights": {
      "confidence_level": "高",
      "professional_appearance": "积极",
      "emotional_stability": "稳定"
    }
  }
}
```

### 2. 面试分析接口

**POST** `/candidate/ai-analysis/interview-analysis`

**请求参数:**
- `video`: 视频文件 (支持: mp4, avi, mov, wmv, flv, mkv)

**响应示例:**
```json
{
  "success": true,
  "message": "面试分析完成",
  "data": {
    "total_frames": 3000,
    "duration": 100.0,
    "performance_analysis": {
      "emotional_consistency": "高",
      "stress_management": "优秀",
      "overall_impression": "优秀候选人"
    },
    "candidate_score": {
      "overall_score": 88,
      "grade": "A"
    }
  }
}
```

### 3. 系统状态接口

**GET** `/candidate/ai-analysis/health-check`

**响应示例:**
```json
{
  "success": true,
  "status": "healthy",
  "models": {
    "face_detection_model": true,
    "emotion_recognition_model": true,
    "font_loaded": true
  }
}
```

## 使用示例

### 1. Python代码调用

```python
from smartrecruit_system.candidate_module.candidate_ai import (
    analyze_candidate_emotion_from_image,
    analyze_interview_performance
)

# 分析候选人照片
with open('candidate_photo.jpg', 'rb') as f:
    image_data = f.read()
    
result = analyze_candidate_emotion_from_image(image_data, 'candidate_photo.jpg')
print(f"检测到 {result['faces_detected']} 个人脸")
print(f"主要表情: {result['emotion_summary']['dominant_emotion']}")

# 分析面试视频
with open('interview_video.mp4', 'rb') as f:
    video_data = f.read()
    
result = analyze_interview_performance(video_data, 'interview_video.mp4')
print(f"候选人评分: {result['candidate_score']['grade']}")
```

### 2. 前端JavaScript调用

```javascript
// 表情识别
const formData = new FormData();
formData.append('image', imageFile);

fetch('/candidate/ai-analysis/emotion-analysis', {
    method: 'POST',
    body: formData
})
.then(response => response.json())
.then(data => {
    if (data.success) {
        console.log('分析结果:', data.data);
        displayResults(data.data);
    }
});

// 面试分析
const videoFormData = new FormData();
videoFormData.append('video', videoFile);

fetch('/candidate/ai-analysis/interview-analysis', {
    method: 'POST',
    body: videoFormData
})
.then(response => response.json())
.then(data => {
    if (data.success) {
        console.log('面试分析:', data.data);
        displayInterviewResults(data.data);
    }
});
```

## 配置选项

### 模型参数配置

```python
# 在ai_config.py中调整
model_config = {
    "face_detection_confidence": 0.5,      # 人脸检测置信度阈值
    "emotion_recognition_confidence": 0.3,  # 表情识别置信度阈值
    "max_faces_per_image": 10,             # 每张图片最大检测人脸数
    "image_processing_size": (640, 640),   # 图像处理尺寸
    "video_analysis_interval": 10          # 视频分析帧间隔
}
```

### 文件处理配置

```python
file_config = {
    "max_image_size": 10 * 1024 * 1024,    # 图片最大大小 (10MB)
    "max_video_size": 100 * 1024 * 1024,   # 视频最大大小 (100MB)
    "allowed_image_extensions": {'.png', '.jpg', '.jpeg', '.gif', '.bmp'},
    "allowed_video_extensions": {'.mp4', '.avi', '.mov', '.wmv', '.flv', '.mkv'}
}
```

## 性能优化

### 1. 模型加载优化
- 模型在首次使用时加载，后续复用
- 支持模型热重载，无需重启服务

### 2. 视频处理优化
- 按配置间隔分析帧，减少计算量
- 支持多线程处理，提高并发性能

### 3. 内存管理
- 自动清理临时文件
- 图片处理完成后释放内存

## 错误处理

### 常见错误及解决方案

1. **模型文件不存在**
   - 检查YOLO模型文件路径
   - 确保模型文件已下载

2. **字体加载失败**
   - 检查系统字体路径
   - 使用默认字体作为备选

3. **GPU内存不足**
   - 降低批处理大小
   - 使用CPU模式运行

4. **文件格式不支持**
   - 检查文件扩展名
   - 转换文件格式

## 安全考虑

### 1. 文件上传安全
- 文件类型验证
- 文件大小限制
- 文件名安全处理

### 2. 用户权限控制
- 登录状态验证
- 用户身份验证
- API访问权限控制

### 3. 数据隐私
- 临时文件自动清理
- 敏感信息不记录日志
- 用户数据隔离

## 扩展功能

### 1. 自定义模型
- 支持加载自定义训练的YOLO模型
- 可配置不同的表情标签集

### 2. 批量处理
- 支持批量图片分析
- 批量视频处理队列

### 3. 实时分析
- 摄像头实时表情识别
- 视频流实时分析

### 4. 多语言支持
- 支持中英文表情标签
- 国际化界面支持

## 维护和监控

### 1. 日志监控
- 详细的错误日志记录
- 性能指标监控
- 用户使用统计

### 2. 健康检查
- 模型状态监控
- 系统资源监控
- 自动故障恢复

### 3. 版本管理
- 模型版本控制
- 配置版本管理
- 向后兼容性保证

## 联系和支持

如有问题或建议，请联系开发团队或查看项目文档。

---

**注意**: 本模块需要足够的计算资源支持，建议在GPU环境下运行以获得最佳性能。
