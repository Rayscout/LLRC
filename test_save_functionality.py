#!/usr/bin/env python3
"""
测试SMART目标保存功能
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from flask import session
from app.models import User, SmartGoal, db
from datetime import datetime

def test_save_functionality():
    """测试保存功能"""
    app = create_app()

    with app.app_context():
        try:
            print("正在测试SMART目标保存功能...")

            # 创建测试用户
            test_user = User.query.filter_by(email='test@example.com').first()
            if test_user:
                # 更新现有用户
                test_user.user_type = 'employee'
                test_user.department = '技术部'
                test_user.employee_id = 'EMP001'
                test_user.hire_date = datetime(2023, 1, 1).date()
                db.session.commit()
                print("✅ 更新测试用户")
            else:
                test_user = User(
                    first_name='测试',
                    last_name='用户',
                    company_name='测试公司',
                    position='python开发工程师',
                    email='test@example.com',
                    phone_number='12345678901',
                    birthday='1990-01-01',
                    password='password',
                    user_type='employee',
                    department='技术部',
                    employee_id='EMP001',
                    hire_date=datetime(2023, 1, 1).date()
                )
                db.session.add(test_user)
                db.session.commit()
                print("✅ 创建测试用户")

            # 创建测试目标
            test_goal = SmartGoal.query.filter_by(user_id=test_user.id).first()
            if not test_goal:
                test_goal = SmartGoal(
                    user_id=test_user.id,
                    title='测试目标',
                    specific='完成测试功能',
                    measurable='通过所有测试用例',
                    achievable='每天投入2小时',
                    relevant='提升代码质量',
                    time_bound='本周内完成',
                    category='technical',
                    priority='high',
                    target_date=datetime(2024, 12, 31).date(),
                    estimated_hours=40,
                    completed_hours=10,
                    progress=25.0,
                    status='active'
                )
                db.session.add(test_goal)
                db.session.commit()
                print("✅ 创建测试目标")

            # 模拟用户登录并测试保存功能
            with app.test_client() as client:
                with client.session_transaction() as sess:
                    sess['user_id'] = test_user.id
                    sess['user_type'] = 'employee'

                print("✅ 模拟用户登录完成")

                # 测试更新小时数功能（保存功能的核心）
                new_completed_hours = 15
                response = client.post(f'/talent/employee_management/smart_goals/{test_goal.id}/update_hours',
                                     json={
                                         'completed_hours': new_completed_hours
                                     })

                print(f"保存响应状态码: {response.status_code}")

                if response.status_code == 200:
                    response_data = response.get_json()
                    print(f"响应数据: {response_data}")

                    if response_data.get('success'):
                        print("✅ 保存功能正常工作")
                        print(f"新的进度: {response_data.get('progress')}%")
                        print(f"完成小时数: {response_data.get('completed_hours')}")
                        print(f"剩余小时数: {response_data.get('remaining_hours')}")
                    else:
                        print(f"❌ 保存失败: {response_data.get('message')}")
                else:
                    print("❌ 保存请求失败")
                    print(f"错误响应: {response.get_data(as_text=True)}")

                # 测试访问目标仪表板，验证UI是否正确显示
                response = client.get('/talent/employee_management/smart_goals/')
                if response.status_code == 200:
                    response_text = response.get_data(as_text=True)
                    if 'SMART目标管理' in response_text and '保存' in response_text:
                        print("✅ 目标仪表板显示正确")
                        print("✅ 保存按钮已正确显示")
                    else:
                        print("❌ 目标仪表板显示异常")
                else:
                    print("❌ 目标仪表板访问失败")

        except Exception as e:
            print(f"测试时出错: {str(e)}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test_save_functionality()
