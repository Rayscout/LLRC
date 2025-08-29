#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试面试安排功能的脚本
"""

import os
import sys

# 添加项目根目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from app import create_app, db
from app.models import User, Job, Application, InterviewSchedule
from app import applications_collection
from sqlalchemy import text

def test_interview_scheduling():
    """测试面试安排功能"""
    app = create_app()
    
    with app.app_context():
        print("开始测试面试安排功能...")
        print("=" * 50)
        
        try:
            # 1. 检查表是否存在
            print("1. 检查面试安排表...")
            result = db.session.execute(text("SELECT name FROM sqlite_master WHERE type='table' AND name='interview_schedule'"))
            if result.fetchone():
                print("✓ 面试安排表存在")
            else:
                print("✗ 面试安排表不存在")
                return False
            
            # 2. 检查模型导入
            print("\n2. 检查模型导入...")
            try:
                interview_schedule = InterviewSchedule()
                print("✓ InterviewSchedule模型导入成功")
            except Exception as e:
                print(f"✗ InterviewSchedule模型导入失败: {e}")
                return False
            
            # 3. 检查路由注册
            print("\n3. 检查路由注册...")
            try:
                from smartrecruit_system.hr_module.candidates import candidates_bp
                routes = [rule.rule for rule in app.url_map.iter_rules() if 'schedule_interview' in rule.rule]
                if routes:
                    print(f"✓ 面试安排路由已注册: {routes}")
                else:
                    print("✗ 面试安排路由未找到")
                    return False
            except Exception as e:
                print(f"✗ 检查路由失败: {e}")
                return False
            
            # 4. 检查模板文件
            print("\n4. 检查模板文件...")
            template_path = os.path.join(app.template_folder, 'smartrecruit', 'hr', 'schedule_interview.html')
            if os.path.exists(template_path):
                print("✓ 面试安排模板文件存在")
            else:
                print("✗ 面试安排模板文件不存在")
                return False
            
            # 5. 检查MongoDB连接（可选）
            print("\n5. 检查MongoDB连接...")
            try:
                # 尝试插入测试数据
                test_data = {
                    'user_id': '999999',
                    'job_id': '999999',
                    'type': 'test_interview_result',
                    'status': 'passed',
                    'created_at': '2024-01-01T00:00:00Z'
                }
                result = applications_collection.insert_one(test_data)
                if result.inserted_id:
                    print("✓ MongoDB连接正常，可以插入数据")
                    # 删除测试数据
                    applications_collection.delete_one({'_id': result.inserted_id})
                else:
                    print("✗ MongoDB插入数据失败")
                    return False
            except Exception as e:
                print(f"⚠ MongoDB连接失败: {e}")
                print("   MongoDB连接失败不影响面试安排功能，可以继续使用")
                print("   面试安排功能将使用SQLite数据库存储面试信息")
            
            print("\n" + "=" * 50)
            print("✓ 核心功能测试通过！面试安排功能已准备就绪")
            print("\n现在您可以:")
            print("1. 启动应用: python run.py")
            print("2. 访问HR面试管理页面: /smartrecruit/hr/dashboard/interviews")
            print("3. 为通过AI面试的候选人安排面试")
            print("\n注意: MongoDB连接失败不影响面试安排功能")
            print("面试安排信息将保存在SQLite数据库中")
            
            return True
            
        except Exception as e:
            print(f"✗ 测试过程中发生错误: {e}")
            return False

def main():
    """主函数"""
    try:
        success = test_interview_scheduling()
        if not success:
            sys.exit(1)
    except ImportError as e:
        print(f"✗ 导入错误: {e}")
        print("请确保已安装所有必要的依赖包")
        sys.exit(1)

if __name__ == '__main__':
    main()
