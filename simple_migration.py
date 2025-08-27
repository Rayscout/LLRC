#!/usr/bin/env python3
"""
简化的人才发展大盘数据库迁移脚本
"""

import sys
import os
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def create_tables():
    """创建数据表"""
    try:
        from app import create_app, db
        from app.models import User, TalentDevelopmentData, MarketSalaryData, TalentAnalysisReport, AIAnalysisLog
        
        app = create_app()
        
        with app.app_context():
            print("开始创建数据表...")
            
            # 创建所有表
            db.create_all()
            
            print("数据表创建完成！")
            
            # 创建示例高管用户
            executive_user = User(
                first_name="高管",
                last_name="示例",
                company_name="示例公司",
                position="CEO",
                email="executive@example.com",
                phone_number="13800000000",
                birthday="1980-01-01",
                password="password123",
                user_type='executive',
                department="总裁办",
                employee_id="EXE001",
                hire_date=datetime.now().date()
            )
            
            db.session.add(executive_user)
            db.session.commit()
            
            print("示例高管用户创建成功！")
            print("登录信息: executive@example.com / password123")
            
    except Exception as e:
        print(f"迁移失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    create_tables()
