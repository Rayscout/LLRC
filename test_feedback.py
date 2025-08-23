#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试反馈管理功能
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_feedback():
    """测试反馈管理功能"""
    print("💬 测试反馈管理功能...")
    print("=" * 60)
    
    try:
        from app import create_app, db
        from app.models import User
        from talent_management_system.employee_manager_module.feedback import (
            get_available_recipients, create_feedback_request, get_user_feedback_requests,
            get_received_feedback_requests, get_pending_feedback_responses, get_feedback_statistics,
            create_feedback_response, archive_feedback_request, get_user_notifications
        )
        
        print("✅ 模块导入成功")
        
        # 创建应用上下文
        app = create_app()
        with app.app_context():
            print("✅ 应用上下文创建成功")
            
            # 测试数据库连接
            try:
                from sqlalchemy import text
                db.session.execute(text("SELECT 1"))
                print("✅ 数据库连接正常")
            except Exception as e:
                print(f"❌ 数据库连接失败: {e}")
                return False
            
            # 测试用户查询
            try:
                users = User.query.filter_by(user_type='employee').limit(1).all()
                if users:
                    user = users[0]
                    print(f"✅ 找到员工用户: {user.email}")
                else:
                    print("⚠️  未找到员工用户，创建模拟用户")
                    user = User(
                        email='test_employee@example.com',
                        user_type='employee',
                        department='技术部',
                        position='python开发工程师'
                    )
            except Exception as e:
                print(f"❌ 用户查询失败: {e}")
                return False
            
            # 测试获取可用接收者
            print("\n👥 测试获取可用接收者...")
            try:
                recipients = get_available_recipients(user.id)
                print(f"✅ 可用接收者数量: {len(recipients)}")
                if recipients:
                    print(f"✅ 第一个接收者: {recipients[0]['name']} ({recipients[0]['email']})")
            except Exception as e:
                print(f"❌ 获取接收者失败: {e}")
                return False
            
            # 测试创建反馈请求
            print("\n📝 测试创建反馈请求...")
            try:
                if recipients:
                    recipient = recipients[0]
                    request_id = create_feedback_request(
                        user.id, recipient['id'], '工作表现', '请对我的工作表现给予反馈', 'medium', '2025-01-15'
                    )
                    if request_id:
                        print(f"✅ 反馈请求创建成功: {request_id}")
                    else:
                        print("❌ 反馈请求创建失败")
                        return False
                else:
                    print("⚠️  没有可用接收者，跳过测试")
            except Exception as e:
                print(f"❌ 创建反馈请求失败: {e}")
                return False
            
            # 测试获取用户反馈请求
            print("\n📤 测试获取用户反馈请求...")
            try:
                user_requests = get_user_feedback_requests(user.id)
                print(f"✅ 用户反馈请求数量: {len(user_requests)}")
                if user_requests:
                    print(f"✅ 第一个请求类型: {user_requests[0]['feedback_type']}")
            except Exception as e:
                print(f"❌ 获取用户反馈请求失败: {e}")
                return False
            
            # 测试获取收到的反馈请求
            print("\n📥 测试获取收到的反馈请求...")
            try:
                received_requests = get_received_feedback_requests(user.id)
                print(f"✅ 收到的反馈请求数量: {len(received_requests)}")
            except Exception as e:
                print(f"❌ 获取收到的反馈请求失败: {e}")
                return False
            
            # 测试获取待回复反馈
            print("\n⏰ 测试获取待回复反馈...")
            try:
                pending_responses = get_pending_feedback_responses(user.id)
                print(f"✅ 待回复反馈数量: {len(pending_responses)}")
            except Exception as e:
                print(f"❌ 获取待回复反馈失败: {e}")
                return False
            
            # 测试获取反馈统计
            print("\n📊 测试获取反馈统计...")
            try:
                feedback_stats = get_feedback_statistics(user.id)
                print(f"✅ 已发送请求: {feedback_stats['total_sent']}")
                print(f"✅ 收到的请求: {feedback_stats['total_received']}")
                print(f"✅ 待回复: {feedback_stats['pending_responses']}")
                print(f"✅ 已完成: {feedback_stats['completed']}")
                print(f"✅ 已归档: {feedback_stats['archived']}")
            except Exception as e:
                print(f"❌ 获取反馈统计失败: {e}")
                return False
            
            # 测试创建反馈回复
            print("\n💬 测试创建反馈回复...")
            try:
                if user_requests:
                    request_id = user_requests[0]['id']
                    if create_feedback_response(request_id, user.id, '感谢您的反馈请求，我会认真考虑您的建议', '5', '建议继续保持当前的工作状态'):
                        print("✅ 反馈回复创建成功")
                    else:
                        print("❌ 反馈回复创建失败")
                else:
                    print("⚠️  没有反馈请求，跳过测试")
            except Exception as e:
                print(f"❌ 创建反馈回复失败: {e}")
                return False
            
            # 测试获取用户通知
            print("\n🔔 测试获取用户通知...")
            try:
                notifications = get_user_notifications(user.id)
                print(f"✅ 用户通知数量: {len(notifications)}")
                if notifications:
                    print(f"✅ 第一个通知: {notifications[0]['title']}")
            except Exception as e:
                print(f"❌ 获取用户通知失败: {e}")
                return False
            
            # 测试归档反馈请求
            print("\n📁 测试归档反馈请求...")
            try:
                if user_requests:
                    request_id = user_requests[0]['id']
                    if archive_feedback_request(request_id):
                        print("✅ 反馈请求归档成功")
                    else:
                        print("❌ 反馈请求归档失败")
                else:
                    print("⚠️  没有反馈请求，跳过测试")
            except Exception as e:
                print(f"❌ 归档反馈请求失败: {e}")
                return False
            
            # 测试蓝图路由
            print("\n🌐 测试蓝图路由...")
            try:
                from talent_management_system.employee_manager_module.feedback import feedback_bp
                print(f"✅ 蓝图名称: {feedback_bp.name}")
                print(f"✅ URL前缀: {feedback_bp.url_prefix}")
                print(f"✅ 蓝图已成功导入")
                
            except Exception as e:
                print(f"❌ 蓝图路由测试失败: {e}")
                return False
            
            print("\n🎉 所有测试通过！反馈管理功能正常工作")
            return True
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_feedback()
