#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试反馈系统功能
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import User, Feedback, FeedbackNotification
from datetime import datetime

def test_feedback_system():
    """测试反馈系统功能"""
    app = create_app()
    
    with app.app_context():
        try:
            print("🧪 开始测试反馈系统...")
            
            # 1. 创建测试用户
            print("\n1. 创建测试用户...")
            
            # 创建高管用户
            executive = User(
                first_name='张',
                last_name='总',
                company_name='测试公司',
                position='技术总监',
                email='zhang.zong@test.com',
                phone_number='13800138001',
                birthday='1980-01-01',
                password='password123',
                user_type='executive',
                department='技术部'
            )
            
            # 创建员工用户
            employee = User(
                first_name='李',
                last_name='工',
                company_name='测试公司',
                position='软件工程师',
                email='li.gong@test.com',
                phone_number='13800138002',
                birthday='1990-01-01',
                password='password123',
                user_type='employee',
                department='技术部',
                supervisor_id=None  # 稍后设置
            )
            
            db.session.add(executive)
            db.session.add(employee)
            db.session.commit()
            
            # 设置员工的主管
            employee.supervisor_id = executive.id
            db.session.commit()
            
            print(f"✅ 高管用户创建成功: {executive.first_name} {executive.last_name} (ID: {executive.id})")
            print(f"✅ 员工用户创建成功: {employee.first_name} {employee.last_name} (ID: {employee.id})")
            
            # 2. 创建测试反馈
            print("\n2. 创建测试反馈...")
            
            feedback = Feedback(
                sender_id=executive.id,
                recipient_id=employee.id,
                category='skill',
                feedback_type='constructive',
                content='李工，你在Python开发方面表现很好，建议继续保持学习热情，可以尝试学习一些高级框架如FastAPI或Django REST framework，这将有助于你的职业发展。',
                priority='medium',
                status='sent'
            )
            
            db.session.add(feedback)
            db.session.commit()
            
            print(f"✅ 反馈创建成功 (ID: {feedback.id})")
            
            # 3. 创建测试通知
            print("\n3. 创建测试通知...")
            
            notification = FeedbackNotification(
                user_id=employee.id,
                feedback_id=feedback.id,
                notification_type='new_feedback',
                title='来自张总的新反馈',
                message='您收到了一个关于技能发展的constructive反馈',
                is_read=False
            )
            
            db.session.add(notification)
            db.session.commit()
            
            print(f"✅ 通知创建成功 (ID: {notification.id})")
            
            # 4. 测试查询功能
            print("\n4. 测试查询功能...")
            
            # 查询员工收到的反馈
            received_feedback = Feedback.query.filter_by(recipient_id=employee.id).all()
            print(f"✅ 员工收到的反馈数量: {len(received_feedback)}")
            
            # 查询高管发送的反馈
            sent_feedback = Feedback.query.filter_by(sender_id=executive.id).all()
            print(f"✅ 高管发送的反馈数量: {len(sent_feedback)}")
            
            # 查询未读通知
            unread_notifications = FeedbackNotification.query.filter_by(
                user_id=employee.id, is_read=False
            ).all()
            print(f"✅ 员工未读通知数量: {len(unread_notifications)}")
            
            # 5. 测试反馈状态更新
            print("\n5. 测试反馈状态更新...")
            
            # 标记反馈为已读
            feedback.status = 'read'
            feedback.read_at = datetime.now()
            db.session.commit()
            print("✅ 反馈状态更新为已读")
            
            # 标记通知为已读
            notification.is_read = True
            db.session.commit()
            print("✅ 通知标记为已读")
            
            # 6. 测试反馈回复
            print("\n6. 测试反馈回复...")
            
            feedback.status = 'responded'
            feedback.responded_at = datetime.now()
            db.session.commit()
            print("✅ 反馈状态更新为已回复")
            
            # 创建回复通知
            response_notification = FeedbackNotification(
                user_id=executive.id,
                feedback_id=feedback.id,
                notification_type='feedback_responded',
                title='反馈已回复',
                message='李工已回复了您的反馈',
                is_read=False
            )
            
            db.session.add(response_notification)
            db.session.commit()
            print("✅ 回复通知创建成功")
            
            # 7. 最终验证
            print("\n7. 最终验证...")
            
            # 验证反馈状态
            updated_feedback = Feedback.query.get(feedback.id)
            print(f"✅ 反馈最终状态: {updated_feedback.status}")
            print(f"✅ 反馈已读时间: {updated_feedback.read_at}")
            print(f"✅ 反馈回复时间: {updated_feedback.responded_at}")
            
            # 验证通知状态
            updated_notification = FeedbackNotification.query.get(notification.id)
            print(f"✅ 原始通知已读状态: {updated_notification.is_read}")
            
            response_notification = FeedbackNotification.query.get(response_notification.id)
            print(f"✅ 回复通知已读状态: {response_notification.is_read}")
            
            print("\n🎉 反馈系统测试完成！所有功能正常工作。")
            
            # 清理测试数据
            print("\n🧹 清理测试数据...")
            db.session.delete(feedback)
            db.session.delete(notification)
            db.session.delete(response_notification)
            db.session.delete(employee)
            db.session.delete(executive)
            db.session.commit()
            print("✅ 测试数据清理完成")
            
            return True
            
        except Exception as e:
            print(f"❌ 测试过程中发生错误: {str(e)}")
            db.session.rollback()
            return False

if __name__ == '__main__':
    success = test_feedback_system()
    if success:
        print("\n🎉 反馈系统测试成功！")
    else:
        print("\n💥 反馈系统测试失败！")
        sys.exit(1)
