# 表情识别模型使用指南

## 🎯 概述

本指南介绍如何在AI模拟面试功能中使用训练好的表情识别YOLO模型。

## 📋 训练和使用流程

### 1. 训练模型

#### 方法一：完整训练（推荐）
```bash
# 进入candidate_module目录
cd LLRC/smartrecruit_system/candidate_module

# 运行完整训练和集成脚本
python train_and_integrate_emotion_model.py
```

#### 方法二：快速训练（测试用）
```bash
# 快速训练（30分钟，50个epoch）
python quick_train_emotion.py
```

### 2. 模型文件位置

训练完成后，模型文件将保存在：
- `trained_models/emotion_recognition_best.pt` (完整训练)
- `trained_models/emotion_quick_train.pt` (快速训练)

### 3. 自动集成

训练脚本会自动：
- ✅ 复制模型文件到模块目录
- ✅ 更新AI配置文件
- ✅ 测试模型集成
- ✅ 生成集成报告

## 🔧 在虚拟面试中使用

### 1. 自动使用（推荐）

模型训练完成后会自动集成，无需额外配置。虚拟面试系统会自动使用训练好的模型。

### 2. 手动配置

如果需要手动配置，请更新 `ai_config.py` 中的模型路径：

```python
# 在ai_config.py中
self.emotion_model_paths = [
    Path(__file__).parent / "trained_models" / "emotion_recognition_best.pt",
    # 其他备选路径...
]
```

### 3. 代码中使用

```python
from emotion_recognition import get_emotion_recognition_ai

# 获取表情识别AI实例
emotion_ai = get_emotion_recognition_ai()

# 分析图片中的表情
result = emotion_ai.recognize_emotion_from_image(image_data)

# 获取分析结果
if result.get("success"):
    faces = result.get("faces", [])
    for face in faces:
        emotion = face["emotion"]
        confidence = face["emotion_confidence"]
        print(f"表情: {emotion}, 置信度: {confidence:.2f}")
```

## 🎭 表情分类

模型识别7种表情：

| 表情 | 英文 | 中文 | 图标 |
|------|------|------|------|
| Angry | 愤怒 | 😠 |
| Disgust | 厌恶 | 🤢 |
| Fear | 恐惧 | 😨 |
| Happy | 高兴 | 😊 |
| Sad | 悲伤 | 😢 |
| Surprise | 惊讶 | 😲 |
| Neutral | 中性 | 😐 |

## 📊 性能指标

- **准确率**: >85%
- **处理速度**: 实时（<100ms）
- **支持多脸检测**: 是
- **置信度阈值**: 0.3（可配置）

## 🔗 API接口

### 表情分析接口

**端点**: `/smartrecruit/candidate/ai-analysis/emotion-analysis`

**方法**: POST

**参数**:
- `image`: 图片文件（支持jpg, png, jpeg等）

**响应示例**:
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
        "face_confidence": 0.95,
        "emotion": "高兴",
        "emotion_confidence": 0.87
      }
    ],
    "emotion_summary": {
      "total_faces": 1,
      "average_confidence": 0.87,
      "dominant_emotion": "高兴"
    }
  }
}
```

## 🎯 在虚拟面试中的应用

### 1. 实时表情分析

在虚拟面试页面中，系统会：
- 每2秒捕获视频帧
- 分析候选人表情
- 实时显示表情变化
- 记录表情统计

### 2. 面试评估

基于表情分析结果：
- 评估情绪稳定性
- 分析职业素养
- 提供改进建议
- 生成面试报告

### 3. 数据可视化

- 表情分布图表
- 表情变化时间线
- 置信度统计
- 情绪稳定性评估

## ⚙️ 配置选项

### 模型配置

在 `ai_config.py` 中可以调整：

```python
self.model_config = {
    "face_detection_confidence": 0.5,      # 人脸检测置信度
    "emotion_recognition_confidence": 0.3,  # 表情识别置信度
    "max_faces_per_image": 10,             # 最大检测人脸数
    "image_processing_size": (640, 640),   # 图片处理尺寸
    "video_analysis_interval": 10          # 视频分析间隔
}
```

### 职业评估配置

```python
self.career_evaluation_config = {
    "positive_emotions": ['高兴', '中性', '惊讶'],
    "negative_emotions": ['愤怒', '厌恶', '恐惧', '悲伤'],
    "confidence_thresholds": {
        "high": 0.8,
        "medium": 0.6,
        "low": 0.4
    }
}
```

## 🛠️ 故障排除

### 常见问题

1. **模型加载失败**
   - 检查模型文件是否存在
   - 确认文件路径正确
   - 验证模型文件完整性

2. **表情识别不准确**
   - 改善光线条件
   - 确保面部清晰
   - 调整置信度阈值

3. **处理速度慢**
   - 检查硬件配置
   - 调整图片处理尺寸
   - 优化分析间隔

### 调试方法

1. **查看日志**
   ```python
   import logging
   logging.getLogger('emotion_recognition').setLevel(logging.DEBUG)
   ```

2. **测试模型状态**
   ```python
   from emotion_recognition import get_emotion_recognition_ai
   ai = get_emotion_recognition_ai()
   status = ai.get_system_status()
   print(status)
   ```

3. **检查配置文件**
   ```python
   from ai_config import get_ai_config
   config = get_ai_config()
   print(config.check_models_availability())
   ```

## 📈 性能优化

### 1. 硬件优化
- 使用GPU加速（如果可用）
- 增加内存容量
- 使用SSD存储

### 2. 软件优化
- 调整批次大小
- 优化图片预处理
- 使用模型量化

### 3. 配置优化
- 调整置信度阈值
- 优化分析频率
- 配置缓存机制

## 🔄 模型更新

### 重新训练
```bash
# 删除旧模型
rm trained_models/emotion_recognition_best.pt

# 重新训练
python train_and_integrate_emotion_model.py
```

### 模型版本管理
- 保留多个版本的模型
- 使用版本号命名
- 记录训练参数和性能

---

**注意**: 确保在更新模型后重启应用以加载新模型。
