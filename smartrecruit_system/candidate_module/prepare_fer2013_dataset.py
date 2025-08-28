#!/usr/bin/env python3
"""
FER2013数据集预处理脚本
将CSV格式转换为YOLO训练格式
"""

import pandas as pd
import numpy as np
import os
import shutil
from pathlib import Path
import cv2
from PIL import Image
import io
import base64

def prepare_fer2013_dataset():
    """准备FER2013数据集"""
    print("🔧 准备FER2013数据集...")
    
    # 获取项目路径
    current_dir = Path(__file__).parent
    yolo_dir = current_dir.parent.parent.parent / "YOLO" / "Facial-Expression-Recognition"
    csv_file = yolo_dir / "datasets" / "fer2013" / "fer2013.csv"
    
    if not csv_file.exists():
        print(f"❌ FER2013 CSV文件不存在: {csv_file}")
        return False
    
    # 创建YOLO格式数据集目录
    dataset_dir = yolo_dir / "datasets" / "fer2013_yolo"
    train_dir = dataset_dir / "train"
    val_dir = dataset_dir / "val"
    
    # 创建目录
    for dir_path in [train_dir, val_dir]:
        dir_path.mkdir(parents=True, exist_ok=True)
    
    # 表情标签映射
    emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']
    
    # 为每个表情创建子目录
    for emotion in emotion_labels:
        (train_dir / emotion).mkdir(exist_ok=True)
        (val_dir / emotion).mkdir(exist_ok=True)
    
    try:
        # 读取CSV文件
        print("📖 读取FER2013 CSV文件...")
        df = pd.read_csv(csv_file)
        
        print(f"📊 数据集信息:")
        print(f"   - 总样本数: {len(df)}")
        print(f"   - 表情分布:")
        print(df['emotion'].value_counts().sort_index())
        
        # 处理每个样本
        processed_count = 0
        for idx, row in df.iterrows():
            if idx % 1000 == 0:
                print(f"   - 处理进度: {idx}/{len(df)}")
            
            emotion = emotion_labels[row['emotion']]
            pixels = row['pixels']
            usage = row['Usage']  # 'Training' 或 'PublicTest'
            
            # 选择目标目录
            if usage == 'Training':
                target_dir = train_dir / emotion
            else:
                target_dir = val_dir / emotion
            
            # 将像素字符串转换为图像
            pixel_list = [int(p) for p in pixels.split()]
            image_array = np.array(pixel_list, dtype=np.uint8).reshape(48, 48)
            
            # 转换为PIL图像并调整大小
            image = Image.fromarray(image_array)
            image = image.resize((224, 224), Image.Resampling.LANCZOS)
            
            # 保存图像
            image_path = target_dir / f"sample_{idx:06d}.jpg"
            image.save(image_path, 'JPEG', quality=95)
            
            processed_count += 1
        
        print(f"✅ 数据集准备完成！")
        print(f"   - 处理样本数: {processed_count}")
        print(f"   - 训练集目录: {train_dir}")
        print(f"   - 验证集目录: {val_dir}")
        
        # 创建数据集配置文件
        config_content = f"""# FER2013 YOLO格式数据集配置
path: {dataset_dir}  # 数据集根目录
train: train  # 训练集目录
val: val      # 验证集目录

# 类别数量和名称
nc: 7  # 类别数量
names: {emotion_labels}  # 类别名称
"""
        
        config_path = dataset_dir / "data.yaml"
        with open(config_path, 'w', encoding='utf-8') as f:
            f.write(config_content)
        
        print(f"📝 配置文件已创建: {config_path}")
        
        return str(config_path)
        
    except Exception as e:
        print(f"❌ 数据集准备失败: {e}")
        return False

def main():
    """主函数"""
    config_path = prepare_fer2013_dataset()
    
    if config_path:
        print("\n" + "=" * 50)
        print("🎉 FER2013数据集准备成功！")
        print(f"📁 配置文件: {config_path}")
        print("🔧 现在可以使用这个数据集进行训练了")
        print("=" * 50)
    else:
        print("\n" + "=" * 50)
        print("❌ 数据集准备失败")
        print("💡 请检查CSV文件是否存在")
        print("=" * 50)

if __name__ == "__main__":
    main()
