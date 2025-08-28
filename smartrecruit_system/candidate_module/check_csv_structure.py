#!/usr/bin/env python3
"""
检查FER2013 CSV文件结构
"""

import pandas as pd
from pathlib import Path

def check_csv_structure():
    """检查CSV文件结构"""
    current_dir = Path(__file__).parent
    yolo_dir = current_dir.parent.parent.parent / "YOLO" / "Facial-Expression-Recognition"
    csv_file = yolo_dir / "datasets" / "fer2013" / "fer2013.csv"
    
    if not csv_file.exists():
        print(f"❌ CSV文件不存在: {csv_file}")
        return
    
    # 读取CSV文件
    df = pd.read_csv(csv_file)
    
    print("📊 CSV文件结构:")
    print(f"   - 列名: {list(df.columns)}")
    print(f"   - 形状: {df.shape}")
    print(f"   - 前5行:")
    print(df.head())
    print(f"   - 数据类型:")
    print(df.dtypes)

if __name__ == "__main__":
    check_csv_structure()
