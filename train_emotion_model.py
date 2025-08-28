#!/usr/bin/env python3
"""
表情识别模型训练脚本
"""

from ultralytics import YOLO
import os
from pathlib import Path

def train_emotion_model():
    """训练表情识别模型"""
    
    # 获取数据集路径
    dataset_path = Path(__file__).parent / "YOLO" / "Facial-Expression-Recognition" / "dataset" / "dataset.yaml"
    
    if not dataset_path.exists():
        print(f"❌ 数据集配置文件不存在: {dataset_path}")
        return False
    
    # 加载预训练模型
    model = YOLO('YOLO/Facial-Expression-Recognition/yolo11n-cls.pt')
    
    # 训练参数
    training_args = {
        'data': str(dataset_path),
        'epochs': 50,           # 训练轮数
        'imgsz': 224,           # 图像大小
        'batch': 16,            # 批次大小
        'name': 'emotion_recognition_model',  # 实验名称
        'patience': 10,         # 早停耐心值
        'save': True,           # 保存模型
        'save_period': 10,      # 每10轮保存一次
        'device': 'cpu',        # 使用CPU训练（如果有GPU可以改为'0'）
        'workers': 4,           # 数据加载器工作进程数
        'project': 'YOLO/Facial-Expression-Recognition/runs/classify',  # 项目目录
        'exist_ok': True,       # 允许覆盖现有实验
        'pretrained': True,     # 使用预训练权重
        'optimizer': 'Adam',    # 优化器
        'lr0': 0.001,          # 初始学习率
        'lrf': 0.01,           # 最终学习率
        'momentum': 0.937,      # SGD动量
        'weight_decay': 0.0005, # 权重衰减
        'warmup_epochs': 3.0,   # 预热轮数
        'warmup_momentum': 0.8, # 预热动量
        'warmup_bias_lr': 0.1,  # 预热偏置学习率
        'box': 7.5,            # 框损失增益
        'cls': 0.5,            # 分类损失增益
        'dfl': 1.5,            # DFL损失增益
        'pose': 12.0,          # 姿态损失增益
        'kobj': 1.0,           # 关键点目标损失增益
        'label_smoothing': 0.0, # 标签平滑
        'nbs': 64,             # 标称批量大小
        'overlap_mask': True,   # 掩码重叠
        'mask_ratio': 4,       # 掩码下采样比率
        'dropout': 0.0,        # 使用分类器dropout
        'val': True,           # 验证
        'plots': True,         # 保存训练图表
    }
    
    try:
        print("🚀 开始训练表情识别模型...")
        print(f"📊 训练参数: {training_args}")
        
        # 开始训练
        results = model.train(**training_args)
        
        print("✅ 模型训练完成!")
        print(f"📈 训练结果: {results}")
        
        # 验证模型
        print("🔍 验证模型性能...")
        val_results = model.val()
        print(f"📊 验证结果: {val_results}")
        
        return True
        
    except Exception as e:
        print(f"❌ 训练失败: {e}")
        return False

if __name__ == "__main__":
    train_emotion_model()
