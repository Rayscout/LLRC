"""
LLRC Header Start
文件功能: 通用 Python 脚本/模块：database/create_tables.py
创建时间: 2025-08-20 16:32
创建人: 谢佳悦
更新记录:
- 2025-09-02 11:18 by 李雨梦
LLRC Header End
"""
#!/usr/bin/env python3
"""
FILE-HEADER-AUTO-ADDED
文件: database/create_tables.py
功能: 通用模块
创建时间: 2025-08-31 16:29
创建人: 苏杰
更新记录:
- 2025-08-20 17:02 by 潘显雨
- 2025-08-27 11:08 by 李雨梦
- 2025-08-31 11:58 by 李雨梦
"""
"""
创建人才发展大盘数据表
"""

import sys
import os
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def create_tables():
    """创建数据表"""
    try:
        # 只导入必要的模块
        from app import create_app, db
        from app.models import User, TalentDevelopmentData, MarketSalaryData, TalentAnalysisReport, AIAnalysisLog
        
        app = create_app()
        
        with app.app_context():
            print("开始创建数据表...")
            
            # 创建所有表
            db.create_all()
            
            print("数据表创建完成！")
            
            # 检查是否已有executive用户
            existing_user = User.query.filter_by(email="executive@example.com").first()
            if not existing_user:
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
            else:
                print("高管用户已存在")
            
            print("\n迁移完成！")
            
    except Exception as e:
        print(f"迁移失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    create_tables()
