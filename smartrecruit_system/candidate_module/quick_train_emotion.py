#!/usr/bin/env python3
"""
快速训练表情识别模型脚本
简化版本，适合快速测试和开发
"""

import os
import sys
from pathlib import Path
import subprocess
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def quick_train_emotion_model():
    """快速训练表情识别模型"""
    print("🚀 快速训练表情识别模型")
    print("=" * 50)
    
    # 获取项目路径
    current_dir = Path(__file__).parent
    yolo_dir = current_dir.parent.parent.parent / "YOLO" / "Facial-Expression-Recognition"
    
    if not yolo_dir.exists():
        print("❌ YOLO项目目录不存在，请先下载数据集")
        return False
    
    # 切换到YOLO目录
    os.chdir(yolo_dir)
    
    try:
        # 使用简化的训练命令
        print("📊 开始训练（简化版本，50个epoch）...")
        
        # 创建简化的训练脚本
        simple_train_script = '''from ultralytics import YOLO

# 加载模型
model = YOLO("yolo11n-cls.yaml")

# 快速训练（50个epoch）
results = model.train(
    data="datasets/fer2013_yolo/data.yaml",  # 使用处理好的FER2013数据集
    epochs=50,       # 减少训练轮数
    batch=8,         # 减少批次大小（CPU训练）
    imgsz=224,
    workers=1,       # 减少工作进程
    
    # 优化器设置
    optimizer="AdamW",
    lr0=0.001,
    warmup_epochs=3,
    
    # 数据增强
    augment=True,
    
    # 项目设置
    project="runs/classify",
    name="emotion_quick_train",
    exist_ok=True,
    
    # 其他设置
    verbose=True,
    device="cpu"     # 强制使用CPU
)

print("✅ 快速训练完成！")
'''
        
        # 保存简化训练脚本
        with open("quick_train.py", "w", encoding="utf-8") as f:
            f.write(simple_train_script)
        
        # 运行训练
        result = subprocess.run([
            sys.executable, "quick_train.py"
        ], capture_output=True, text=True, timeout=1800)  # 30分钟超时
        
        if result.returncode == 0:
            print("✅ 快速训练成功完成！")
            print("训练输出:")
            print(result.stdout)
            
            # 查找训练好的模型
            model_path = yolo_dir / "runs" / "classify" / "emotion_quick_train" / "weights" / "best.pt"
            if model_path.exists():
                print(f"📁 模型文件: {model_path}")
                print(f"📏 模型大小: {model_path.stat().st_size / (1024*1024):.1f} MB")
                
                # 复制到模块目录
                target_dir = current_dir / "trained_models"
                target_dir.mkdir(exist_ok=True)
                
                import shutil
                target_path = target_dir / "emotion_quick_train.pt"
                shutil.copy2(model_path, target_path)
                
                print(f"📦 模型已复制到: {target_path}")
                print("\n🎉 快速训练完成！现在可以在虚拟面试系统中使用这个模型了。")
                
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

def main():
    """主函数"""
    success = quick_train_emotion_model()
    
    if success:
        print("\n" + "=" * 50)
        print("🎉 快速训练成功！")
        print("📁 模型文件: trained_models/emotion_quick_train.pt")
        print("🔧 可以在虚拟面试系统中使用")
        print("=" * 50)
    else:
        print("\n" + "=" * 50)
        print("❌ 快速训练失败")
        print("💡 请检查数据集和环境配置")
        print("=" * 50)

if __name__ == "__main__":
    main()
