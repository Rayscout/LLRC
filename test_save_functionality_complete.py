#!/usr/bin/env python3
"""
完整测试SMART目标保存功能
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from flask import session
from app.models import User, SmartGoal, db
from datetime import datetime

def test_save_functionality_complete():
    """完整测试保存功能"""
    app = create_app()

    with app.app_context():
        try:
            print("正在完整测试SMART目标保存功能...")

            # 创建测试用户
            test_user = User.query.filter_by(email='test@example.com').first()
            if test_user:
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

            # 记录初始状态
            initial_completed_hours = test_goal.completed_hours
            initial_progress = test_goal.progress

            print(f"初始状态: 完成小时数={initial_completed_hours}, 进度={initial_progress}%")

            # 模拟用户登录并测试保存功能
            with app.test_client() as client:
                with client.session_transaction() as sess:
                    sess['user_id'] = test_user.id
                    sess['user_type'] = 'employee'

                print("✅ 模拟用户登录完成")

                # 测试保存功能 - 增加完成小时数
                new_completed_hours = 20  # 从10小时增加到20小时
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

                        # 验证数据库中的数据是否真的被更新了
                        updated_goal = SmartGoal.query.get(test_goal.id)
                        if updated_goal:
                            print("\n数据库验证:")
                            print(f"  数据库完成小时数: {updated_goal.completed_hours}")
                            print(f"  数据库进度: {updated_goal.progress}%")
                            print(f"  数据是否更新: {updated_goal.completed_hours != initial_completed_hours}")

                            if updated_goal.completed_hours == new_completed_hours:
                                print("✅ 数据库数据成功更新")
                            else:
                                print("❌ 数据库数据更新失败")
                        else:
                            print("❌ 无法从数据库获取更新后的目标")
                    else:
                        print(f"❌ 保存失败: {response_data.get('message')}")
                else:
                    print("❌ 保存请求失败")
                    print(f"错误响应: {response.get_data(as_text=True)}")

                # 测试页面访问，验证按钮状态
                response = client.get('/talent/employee_management/smart_goals/')
                if response.status_code == 200:
                    response_text = response.get_data(as_text=True)

                    # 检查保存按钮是否正确显示
                    if '保存' in response_text:
                        print("✅ 保存按钮正确显示在页面中")

                        # 检查是否有JavaScript代码
                        if 'saveProgress' in response_text:
                            print("✅ 保存功能JavaScript代码存在")

                        if 'pendingChanges' in response_text:
                            print("✅ 待保存更改跟踪代码存在")

                        if 'showSaveSuccess' in response_text:
                            print("✅ 保存成功提示代码存在")

                        if 'showNoChangesMessage' in response_text:
                            print("✅ 无更改提示代码存在")

                        if 'updateSaveButtonState' in response_text:
                            print("✅ 按钮状态管理代码存在")
                    else:
                        print("❌ 保存按钮未找到")
                else:
                    print("❌ 目标仪表板访问失败")

        except Exception as e:
            print(f"测试时出错: {str(e)}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test_save_functionality_complete()
