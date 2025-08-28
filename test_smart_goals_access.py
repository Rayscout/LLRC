#!/usr/bin/env python3
"""
测试SMART目标界面访问
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from flask import session, url_for
from app.models import User, SmartGoal, db
from datetime import datetime

def test_smart_goals_access():
    """测试SMART目标界面访问"""
    app = create_app()

    with app.app_context():
        try:
            print("正在测试SMART目标界面访问...")

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

            # 模拟用户登录 - 直接设置session
            with app.test_client() as client:
                with client.session_transaction() as sess:
                    sess['user_id'] = test_user.id
                    sess['user_type'] = 'employee'
                    sess.permanent = True

                print("✅ 直接设置session完成")

                # 测试访问目标仪表板
                response = client.get('/talent/employee_management/smart_goals/')
                print(f"目标仪表板响应状态码: {response.status_code}")

                if response.status_code == 200:
                    print("✅ 目标仪表板访问成功")
                    # 检查响应内容是否包含期望的元素
                    response_text = response.get_data(as_text=True)
                    if 'SMART目标管理' in response_text:
                        print("✅ 页面内容正确")
                    else:
                        print("❌ 页面内容异常")
                        print("页面内容预览:", response_text[:500])
                else:
                    print("❌ 目标仪表板访问失败")
                    print("错误响应:", response.get_data(as_text=True))

                # 测试创建目标页面
                response = client.get('/talent/employee_management/smart_goals/create')
                print(f"创建目标页面响应状态码: {response.status_code}")

                if response.status_code == 200:
                    print("✅ 创建目标页面访问成功")
                else:
                    print("❌ 创建目标页面访问失败")
                    print("错误响应:", response.get_data(as_text=True))

        except Exception as e:
            print(f"测试时出错: {str(e)}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test_smart_goals_access()
