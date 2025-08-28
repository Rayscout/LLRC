#!/usr/bin/env python3
"""
简单的表情识别模型训练脚本
"""

import os
import sys
from pathlib import Path
import subprocess

def simple_train():
    """简单训练"""
    print("🚀 开始简单训练...")
    
    # 获取项目路径
    current_dir = Path(__file__).parent
    yolo_dir = current_dir.parent.parent.parent / "YOLO" / "Facial-Expression-Recognition"
    
    # 切换到YOLO目录
    os.chdir(yolo_dir)
    
    # 数据集配置文件路径
    data_yaml = yolo_dir / "datasets" / "fer2013_yolo" / "data.yaml"
    
    if not data_yaml.exists():
        print(f"❌ 数据集配置文件不存在: {data_yaml}")
        return False
    
    print(f"📁 使用数据集配置: {data_yaml}")
    
    # 创建训练脚本
    train_script = f'''from ultralytics import YOLO

# 加载模型
model = YOLO("yolo11n-cls.yaml")

# 简单训练
results = model.train(
    data="{data_yaml}",
    epochs=20,       # 减少训练轮数
    batch=4,         # 小批次
    imgsz=224,
    workers=1,
    optimizer="AdamW",
    lr0=0.001,
    device="cpu",
    project="runs/classify",
    name="emotion_simple_train",
    exist_ok=True,
    verbose=True
)

print("✅ 训练完成！")
'''
    
    # 保存训练脚本
    with open("simple_train.py", "w", encoding="utf-8") as f:
        f.write(train_script)
    
    # 运行训练
    try:
        result = subprocess.run([
            sys.executable, "simple_train.py"
        ], capture_output=True, text=True, timeout=3600)  # 1小时超时
        
        if result.returncode == 0:
            print("✅ 训练成功完成！")
            print("训练输出:")
            print(result.stdout)
            
            # 查找训练好的模型
            model_path = yolo_dir / "runs" / "classify" / "emotion_simple_train" / "weights" / "best.pt"
            if model_path.exists():
                print(f"📁 模型文件: {model_path}")
                print(f"📏 模型大小: {model_path.stat().st_size / (1024*1024):.1f} MB")
                
                # 复制到模块目录
                target_dir = current_dir / "trained_models"
                target_dir.mkdir(exist_ok=True)
                
                import shutil
                target_path = target_dir / "emotion_simple_train.pt"
                shutil.copy2(model_path, target_path)
                
                print(f"📦 模型已复制到: {target_path}")
                print("\n🎉 训练完成！现在可以在虚拟面试系统中使用这个模型了。")
                
                return True
            else:
                print("❌ 未找到训练好的模型文件")
                return False
        else:
            print("❌ 训练失败")
            print("错误信息:")
            print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ 训练超时（超过1小时）")
        return False
    except Exception as e:
        print(f"❌ 训练过程中出现错误: {e}")
        return False

if __name__ == "__main__":
    success = simple_train()
    
    if success:
        print("\n" + "=" * 50)
        print("🎉 简单训练成功！")
        print("📁 模型文件: trained_models/emotion_simple_train.pt")
        print("🔧 可以在虚拟面试系统中使用")
        print("=" * 50)
    else:
        print("\n" + "=" * 50)
        print("❌ 简单训练失败")
        print("💡 请检查数据集和环境配置")
        print("=" * 50)
