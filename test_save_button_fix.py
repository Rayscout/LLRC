#!/usr/bin/env python3
"""
测试保存按钮修复
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from flask import session
from app.models import User, SmartGoal, db
from datetime import datetime

def test_save_button_fix():
    """测试保存按钮是否可以交互"""
    app = create_app()

    with app.app_context():
        try:
            print("正在测试保存按钮修复...")

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

            # 测试访问目标仪表板
            with app.test_client() as client:
                with client.session_transaction() as sess:
                    sess['user_id'] = test_user.id
                    sess['user_type'] = 'employee'

                print("✅ 模拟用户登录完成")

                # 测试访问目标仪表板，检查保存按钮是否正确显示
                response = client.get('/talent/employee_management/smart_goals/')
                if response.status_code == 200:
                    response_text = response.get_data(as_text=True)

                    # 查找保存按钮的HTML
                    import re
                    save_button_pattern = r'<button[^>]*save-progress-btn[^>]*>(.*?)</button>'
                    save_buttons = re.findall(save_button_pattern, response_text, re.DOTALL | re.IGNORECASE)

                    if save_buttons:
                        print(f"找到 {len(save_buttons)} 个保存按钮")
                        for i, button_html in enumerate(save_buttons):
                            print(f"按钮 {i+1} HTML: {button_html[:200]}...")

                            if 'disabled' in button_html:
                                print(f"❌ 按钮 {i+1} 被禁用")
                            else:
                                print(f"✅ 按钮 {i+1} 可交互")

                            if '保存' in button_html:
                                print(f"✅ 按钮 {i+1} 包含'保存'文字")
                            else:
                                print(f"❌ 按钮 {i+1} 不包含'保存'文字")
                    else:
                        print("❌ 未找到保存按钮")

                    # 检查完整的按钮标签
                    button_pattern = r'<button[^>]*>.*?</button>'
                    all_buttons = re.findall(button_pattern, response_text, re.DOTALL | re.IGNORECASE)
                    print(f"页面总共有 {len(all_buttons)} 个按钮")

                    print("✅ 目标仪表板访问成功")
                else:
                    print("❌ 目标仪表板访问失败")
                    print(f"错误响应: {response.get_data(as_text=True)}")

        except Exception as e:
            print(f"测试时出错: {str(e)}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test_save_button_fix()
