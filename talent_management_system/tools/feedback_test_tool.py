#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
反馈系统测试工具
整合所有反馈相关的测试和验证功能
"""

import sqlite3
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.models import User, Feedback, db
from datetime import datetime

class FeedbackTestTool:
    """反馈系统测试工具类"""
    
    def __init__(self, db_path='instance/site.db'):
        self.db_path = db_path
        
    def test_feedback_system(self):
        """测试反馈系统功能"""
        print("🧪 测试反馈系统功能...")
        
        try:
            # 测试用户数据
            print("\n1. 测试用户数据...")
            users = User.query.all()
            print(f"✅ 找到 {len(users)} 个用户")
            
            employees = [u for u in users if u.user_type == 'employee']
            executives = [u for u in users if u.user_type in ['executive', 'supervisor']]
            
            print(f"   - 员工: {len(employees)} 个")
            print(f"   - 高管/主管: {len(executives)} 个")
            
            if not employees or not executives:
                print("❌ 用户数据不足，无法进行测试")
                return False
            
            # 测试反馈表结构
            print("\n2. 测试反馈表结构...")
            feedbacks = Feedback.query.all()
            print(f"✅ 找到 {len(feedbacks)} 条反馈记录")
            
            # 测试创建新反馈
            print("\n3. 测试创建新反馈...")
            test_employee = employees[0]
            test_executive = executives[0]
            
            new_feedback = Feedback(
                sender_id=test_employee.id,
                recipient_id=test_executive.id,
                category='skill',
                feedback_type='request',
                content='这是一条测试反馈，用于验证系统功能。',
                priority='medium',
                status='sent'
            )
            
            db.session.add(new_feedback)
            db.session.commit()
            
            print(f"✅ 成功创建测试反馈 (ID: {new_feedback.id})")
            
            # 测试查询反馈
            print("\n4. 测试查询反馈...")
            
            # 查询员工发送的反馈
            sent_feedback = Feedback.query.filter_by(sender_id=test_employee.id).all()
            print(f"   - 员工发送的反馈: {len(sent_feedback)} 条")
            
            # 查询高管接收的反馈
            received_feedback = Feedback.query.filter_by(recipient_id=test_executive.id).all()
            print(f"   - 高管接收的反馈: {len(received_feedback)} 条")
            
            # 测试更新反馈状态
            print("\n5. 测试更新反馈状态...")
            new_feedback.status = 'read'
            new_feedback.read_at = datetime.now()
            db.session.commit()
            
            print("✅ 成功更新反馈状态为已读")
            
            # 测试添加回复
            print("\n6. 测试添加回复...")
            new_feedback.response_content = "感谢您的反馈，我们会认真考虑您的建议。"
            new_feedback.response_rating = 5
            new_feedback.status = 'responded'
            new_feedback.responded_at = datetime.now()
            db.session.commit()
            
            print("✅ 成功添加回复内容")
            
            # 验证最终结果
            print("\n7. 验证最终结果...")
            final_feedback = Feedback.query.get(new_feedback.id)
            
            print(f"   - 反馈ID: {final_feedback.id}")
            print(f"   - 发送者: {final_feedback.sender.first_name} {final_feedback.sender.last_name}")
            print(f"   - 接收者: {final_feedback.recipient.first_name} {final_feedback.recipient.last_name}")
            print(f"   - 分类: {final_feedback.category}")
            print(f"   - 类型: {final_feedback.feedback_type}")
            print(f"   - 状态: {final_feedback.status}")
            print(f"   - 回复内容: {final_feedback.response_content}")
            print(f"   - 回复评分: {final_feedback.response_rating}")
            
            # 清理测试数据
            print("\n8. 清理测试数据...")
            db.session.delete(new_feedback)
            db.session.commit()
            print("✅ 测试数据清理完成")
            
            print("\n🎉 反馈系统测试完成！所有功能正常")
            return True
            
        except Exception as e:
            print(f"❌ 测试失败: {e}")
            return False
    
    def test_employee_feedback(self):
        """测试员工反馈功能"""
        print("🧪 测试员工反馈功能...")
        
        try:
            # 获取员工和高管
            employees = User.query.filter_by(user_type='employee').all()
            executives = User.query.filter(User.user_type.in_(['executive', 'supervisor'])).all()
            
            if not employees or not executives:
                print("❌ 没有足够的用户数据进行测试")
                return False
            
            print(f"✅ 找到 {len(employees)} 个员工和 {len(executives)} 个高管")
            
            # 测试员工发送反馈给高管
            test_employee = employees[0]
            test_executive = executives[0]
            
            print(f"\n测试员工: {test_employee.first_name} {test_employee.last_name}")
            print(f"测试高管: {test_executive.first_name} {test_executive.last_name}")
            
            # 创建测试反馈
            test_feedback = Feedback(
                sender_id=test_employee.id,
                recipient_id=test_executive.id,
                category='communication',
                feedback_type='improvement',
                content='希望改进团队沟通机制，定期召开项目进度会议。',
                priority='high',
                status='sent'
            )
            
            db.session.add(test_feedback)
            db.session.commit()
            
            print(f"✅ 员工成功发送反馈 (ID: {test_feedback.id})")
            
            # 验证反馈数据
            sent_count = Feedback.query.filter_by(sender_id=test_employee.id).count()
            received_count = Feedback.query.filter_by(recipient_id=test_executive.id).count()
            
            print(f"   - 员工发送的反馈总数: {sent_count}")
            print(f"   - 高管接收的反馈总数: {received_count}")
            
            # 清理测试数据
            db.session.delete(test_feedback)
            db.session.commit()
            
            print("✅ 员工反馈功能测试完成")
            return True
            
        except Exception as e:
            print(f"❌ 员工反馈测试失败: {e}")
            return False
    
    def test_executive_feedback(self):
        """测试高管反馈功能"""
        print("🧪 测试高管反馈功能...")
        
        try:
            # 获取员工和高管
            employees = User.query.filter_by(user_type='employee').all()
            executives = User.query.filter(User.user_type.in_(['executive', 'supervisor'])).all()
            
            if not employees or not executives:
                print("❌ 没有足够的用户数据进行测试")
                return False
            
            # 测试高管发送反馈给员工
            test_executive = executives[0]
            test_employee = employees[0]
            
            print(f"\n测试高管: {test_executive.first_name} {test_executive.last_name}")
            print(f"测试员工: {test_employee.first_name} {test_employee.last_name}")
            
            # 创建测试反馈
            test_feedback = Feedback(
                sender_id=test_executive.id,
                recipient_id=test_employee.id,
                category='performance',
                feedback_type='positive',
                content='你在项目中的表现很出色，继续保持这种工作态度。',
                priority='medium',
                status='sent'
            )
            
            db.session.add(test_feedback)
            db.session.commit()
            
            print(f"✅ 高管成功发送反馈 (ID: {test_feedback.id})")
            
            # 验证反馈数据
            sent_count = Feedback.query.filter_by(sender_id=test_executive.id).count()
            received_count = Feedback.query.filter_by(recipient_id=test_employee.id).count()
            
            print(f"   - 高管发送的反馈总数: {sent_count}")
            print(f"   - 员工接收的反馈总数: {received_count}")
            
            # 清理测试数据
            db.session.delete(test_feedback)
            db.session.commit()
            
            print("✅ 高管反馈功能测试完成")
            return True
            
        except Exception as e:
            print(f"❌ 高管反馈测试失败: {e}")
            return False
    
    def generate_test_report(self):
        """生成测试报告"""
        print("📊 生成反馈系统测试报告...")
        
        try:
            # 统计用户数据
            total_users = User.query.count()
            employees = User.query.filter_by(user_type='employee').count()
            executives = User.query.filter(User.user_type.in_(['executive', 'supervisor'])).count()
            
            # 统计反馈数据
            total_feedback = Feedback.query.count()
            sent_feedback = Feedback.query.filter(Feedback.sender_id.isnot(None)).count()
            received_feedback = Feedback.query.filter(Feedback.recipient_id.isnot(None)).count()
            
            # 按状态统计
            sent_status = Feedback.query.filter_by(status='sent').count()
            read_status = Feedback.query.filter_by(status='read').count()
            responded_status = Feedback.query.filter_by(status='responded').count()
            
            # 按分类统计
            skill_feedback = Feedback.query.filter_by(category='skill').count()
            communication_feedback = Feedback.query.filter_by(category='communication').count()
            performance_feedback = Feedback.query.filter_by(category='performance').count()
            general_feedback = Feedback.query.filter_by(category='general').count()
            
            print("\n" + "="*50)
            print("📋 反馈系统测试报告")
            print("="*50)
            
            print(f"\n👥 用户统计:")
            print(f"   - 总用户数: {total_users}")
            print(f"   - 员工数: {employees}")
            print(f"   - 高管/主管数: {executives}")
            
            print(f"\n💬 反馈统计:")
            print(f"   - 总反馈数: {total_feedback}")
            print(f"   - 发送反馈数: {sent_feedback}")
            print(f"   - 接收反馈数: {received_feedback}")
            
            print(f"\n📈 状态分布:")
            print(f"   - 已发送: {sent_status}")
            print(f"   - 已读: {read_status}")
            print(f"   - 已回复: {responded_status}")
            
            print(f"\n🏷️ 分类分布:")
            print(f"   - 技能发展: {skill_feedback}")
            print(f"   - 沟通协作: {communication_feedback}")
            print(f"   - 绩效表现: {performance_feedback}")
            print(f"   - 一般反馈: {general_feedback}")
            
            print("\n" + "="*50)
            print("✅ 测试报告生成完成")
            
        except Exception as e:
            print(f"❌ 生成测试报告失败: {e}")

def main():
    """主函数"""
    tool = FeedbackTestTool()
    
    print("🧪 反馈系统测试工具")
    print("=" * 50)
    
    while True:
        print("\n请选择测试:")
        print("1. 完整反馈系统测试")
        print("2. 员工反馈功能测试")
        print("3. 高管反馈功能测试")
        print("4. 生成测试报告")
        print("5. 执行所有测试")
        print("0. 退出")
        
        choice = input("\n请输入选择 (0-5): ").strip()
        
        if choice == '1':
            tool.test_feedback_system()
        elif choice == '2':
            tool.test_employee_feedback()
        elif choice == '3':
            tool.test_executive_feedback()
        elif choice == '4':
            tool.generate_test_report()
        elif choice == '5':
            print("\n🔄 执行所有测试...")
            tool.test_feedback_system()
            tool.test_employee_feedback()
            tool.test_executive_feedback()
            tool.generate_test_report()
            print("\n✅ 所有测试完成！")
        elif choice == '0':
            print("👋 再见！")
            break
        else:
            print("❌ 无效选择，请重新输入")

if __name__ == "__main__":
    main()
