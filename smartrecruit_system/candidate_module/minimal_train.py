#!/usr/bin/env python3
"""
最简单的表情识别模型训练脚本
"""

import os
import sys
from pathlib import Path
import subprocess

def minimal_train():
    """最简单训练"""
    print("🚀 开始最简单训练...")
    
    # 获取项目路径
    current_dir = Path(__file__).parent
    yolo_dir = current_dir.parent.parent.parent / "YOLO" / "Facial-Expression-Recognition"
    
    # 切换到YOLO目录
    os.chdir(yolo_dir)
    
    print(f"📁 当前工作目录: {os.getcwd()}")
    
    # 创建最简单的训练脚本
    train_script = '''from ultralytics import YOLO

# 加载模型
model = YOLO("yolo11n-cls.yaml")

# 最简单训练
results = model.train(
    data="fer2013_yolo/data.yaml",
    epochs=5,        # 很少的训练轮数
    batch=1,         # 最小批次
    imgsz=224,
    workers=1,
    device="cpu",
    project="runs/classify",
    name="emotion_minimal_train",
    exist_ok=True,
    verbose=True
)

print("✅ 训练完成！")
'''
    
    # 保存训练脚本
    with open("minimal_train.py", "w", encoding="utf-8") as f:
        f.write(train_script)
    
    # 运行训练
    try:
        print("📊 开始训练...")
        result = subprocess.run([
            sys.executable, "minimal_train.py"
        ], capture_output=True, text=True, timeout=900)  # 15分钟超时
        
        if result.returncode == 0:
            print("✅ 训练成功完成！")
            print("训练输出:")
            print(result.stdout)
            
            # 查找训练好的模型
            model_path = yolo_dir / "runs" / "classify" / "emotion_minimal_train" / "weights" / "best.pt"
            if model_path.exists():
                print(f"📁 模型文件: {model_path}")
                print(f"📏 模型大小: {model_path.stat().st_size / (1024*1024):.1f} MB")
                
                # 复制到模块目录
                target_dir = current_dir / "trained_models"
                target_dir.mkdir(exist_ok=True)
                
                import shutil
                target_path = target_dir / "emotion_minimal_train.pt"
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
        print("❌ 训练超时（超过15分钟）")
        return False
    except Exception as e:
        print(f"❌ 训练过程中出现错误: {e}")
        return False

if __name__ == "__main__":
    success = minimal_train()
    
    if success:
        print("\n" + "=" * 50)
        print("🎉 最简单训练成功！")
        print("📁 模型文件: trained_models/emotion_minimal_train.pt")
        print("🔧 可以在虚拟面试系统中使用")
        print("=" * 50)
    else:
        print("\n" + "=" * 50)
        print("❌ 最简单训练失败")
        print("💡 请检查数据集和环境配置")
        print("=" * 50)
