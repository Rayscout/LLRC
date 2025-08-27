#!/usr/bin/env python3
"""
人才发展大盘数据库迁移脚本
添加新的数据表和相关字段
"""

import sys
import os
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import User, TalentDevelopmentData, MarketSalaryData, TalentAnalysisReport, AIAnalysisLog

def create_talent_dashboard_tables():
    """创建人才发展大盘相关的数据表"""
    
    app = create_app()
    
    with app.app_context():
        try:
            print("开始创建人才发展大盘数据表...")
            
            # 创建新表
            db.create_all()
            
            print("数据表创建完成！")
            
            # 验证表是否创建成功
            tables = [
                'talent_development_data',
                'market_salary_data', 
                'talent_analysis_report',
                'ai_analysis_log'
            ]
            
            for table in tables:
                try:
                    # 检查表是否存在
                    result = db.session.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'")
                    if result.fetchone():
                        print(f"✓ 表 {table} 创建成功")
                    else:
                        print(f"✗ 表 {table} 创建失败")
                except Exception as e:
                    print(f"✗ 检查表 {table} 时出错: {e}")
            
            print("\n数据库迁移完成！")
            
        except Exception as e:
            print(f"数据库迁移失败: {e}")
            raise

def add_executive_user_type():
    """为现有用户添加executive用户类型支持"""
    
    app = create_app()
    
    with app.app_context():
        try:
            print("检查用户类型字段...")
            
            # 检查是否有executive类型的用户
            executive_users = User.query.filter_by(user_type='executive').all()
            
            if not executive_users:
                print("未找到executive用户，创建一个示例高管用户...")
                
                # 创建一个示例高管用户
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
                print("登录信息:")
                print("  邮箱: executive@example.com")
                print("  密码: password123")
            else:
                print(f"找到 {len(executive_users)} 个executive用户")
            
        except Exception as e:
            print(f"处理用户类型时出错: {e}")

def main():
    """主函数"""
    print("=" * 50)
    print("人才发展大盘数据库迁移工具")
    print("=" * 50)
    
    try:
        # 创建数据表
        create_talent_dashboard_tables()
        
        # 添加executive用户类型支持
        add_executive_user_type()
        
        print("\n" + "=" * 50)
        print("迁移完成！")
        print("=" * 50)
        print("\n下一步操作:")
        print("1. 运行数据初始化脚本生成示例数据:")
        print("   python scripts/init_talent_data.py")
        print("2. 启动应用程序:")
        print("   python run.py")
        print("3. 使用高管账号登录访问人才发展大盘:")
        print("   邮箱: executive@example.com")
        print("   密码: password123")
        print("4. 访问人才发展大盘: http://localhost:5000/talent-dashboard")
        
    except Exception as e:
        print(f"\n迁移失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
