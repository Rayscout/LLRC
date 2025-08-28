#!/usr/bin/env python3
"""
直接训练表情识别模型
"""

import os
import sys
from pathlib import Path
import subprocess

def direct_train():
    """直接训练"""
    print("🚀 开始直接训练...")
    
    # 获取项目路径
    current_dir = Path(__file__).parent
    yolo_dir = current_dir.parent.parent.parent / "YOLO" / "Facial-Expression-Recognition"
    
    # 切换到YOLO目录
    os.chdir(yolo_dir)
    
    print(f"📁 当前工作目录: {os.getcwd()}")
    
    # 检查数据集是否存在
    dataset_dir = yolo_dir / "datasets" / "fer2013_yolo"
    if not dataset_dir.exists():
        print(f"❌ 数据集目录不存在: {dataset_dir}")
        return False
    
    print(f"✅ 数据集目录存在: {dataset_dir}")
    
    # 创建训练脚本
    train_script = '''from ultralytics import YOLO
import os

# 加载模型
model = YOLO("yolo11n-cls.yaml")

# 直接训练
results = model.train(
    data="datasets/fer2013_yolo/data.yaml",
    epochs=10,       # 很少的训练轮数
    batch=2,         # 很小的批次
    imgsz=224,
    workers=1,
    optimizer="AdamW",
    lr0=0.001,
    device="cpu",
    project="runs/classify",
    name="emotion_direct_train",
    exist_ok=True,
    verbose=True
)

print("✅ 训练完成！")
'''
    
    # 保存训练脚本
    with open("direct_train.py", "w", encoding="utf-8") as f:
        f.write(train_script)
    
    # 运行训练
    try:
        print("📊 开始训练...")
        result = subprocess.run([
            sys.executable, "direct_train.py"
        ], capture_output=True, text=True, timeout=1800)  # 30分钟超时
        
        if result.returncode == 0:
            print("✅ 训练成功完成！")
            print("训练输出:")
            print(result.stdout)
            
            # 查找训练好的模型
            model_path = yolo_dir / "runs" / "classify" / "emotion_direct_train" / "weights" / "best.pt"
            if model_path.exists():
                print(f"📁 模型文件: {model_path}")
                print(f"📏 模型大小: {model_path.stat().st_size / (1024*1024):.1f} MB")
                
                # 复制到模块目录
                target_dir = current_dir / "trained_models"
                target_dir.mkdir(exist_ok=True)
                
                import shutil
                target_path = target_dir / "emotion_direct_train.pt"
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
        print("❌ 训练超时（超过30分钟）")
        return False
    except Exception as e:
        print(f"❌ 训练过程中出现错误: {e}")
        return False

if __name__ == "__main__":
    success = direct_train()
    
    if success:
        print("\n" + "=" * 50)
        print("🎉 直接训练成功！")
        print("📁 模型文件: trained_models/emotion_direct_train.pt")
        print("🔧 可以在虚拟面试系统中使用")
        print("=" * 50)
    else:
        print("\n" + "=" * 50)
        print("❌ 直接训练失败")
        print("💡 请检查数据集和环境配置")
        print("=" * 50)
