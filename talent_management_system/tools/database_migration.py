#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库迁移工具
整合所有数据库相关的迁移和检查功能
"""

import sqlite3
import os
from datetime import datetime

class DatabaseMigrationTool:
    """数据库迁移工具类"""
    
    def __init__(self, db_path='instance/site.db'):
        self.db_path = db_path
        
    def check_database_structure(self):
        """检查数据库表结构"""
        print("🔍 检查数据库表结构...")
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 检查用户表结构
            print("\n📊 用户表结构:")
            cursor.execute("PRAGMA table_info(user)")
            user_columns = cursor.fetchall()
            
            for column in user_columns:
                print(f"  - {column[1]} ({column[2]})")
            
            # 检查反馈表结构
            print("\n📝 反馈表结构:")
            cursor.execute("PRAGMA table_info(feedback)")
            feedback_columns = cursor.fetchall()
            
            for column in feedback_columns:
                print(f"  - {column[1]} ({column[2]})")
            
            conn.close()
            print("\n✅ 数据库结构检查完成")
            
        except Exception as e:
            print(f"❌ 检查失败: {e}")
    
    def migrate_feedback_table(self):
        """迁移反馈表结构"""
        print("🔧 迁移反馈表结构...")
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 检查反馈表是否存在
            cursor.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name='feedback'
            """)
            
            if cursor.fetchone():
                print("✅ 反馈表已存在")
                
                # 检查并添加新列
                columns_to_add = [
                    ('response_content', 'TEXT'),
                    ('response_rating', 'INTEGER'),
                ]
                
                for column_name, column_type in columns_to_add:
                    try:
                        cursor.execute(f"ALTER TABLE feedback ADD COLUMN {column_name} {column_type}")
                        print(f"✅ 添加列: {column_name}")
                    except sqlite3.OperationalError as e:
                        if "duplicate column name" in str(e):
                            print(f"ℹ️ 列已存在: {column_name}")
                        else:
                            print(f"❌ 添加列失败: {column_name} - {e}")
                
                # 更新现有记录的feedback_type
                cursor.execute("""
                    UPDATE feedback 
                    SET feedback_type = 'positive' 
                    WHERE feedback_type IS NULL OR feedback_type = ''
                """)
                print("✅ 更新现有记录的feedback_type")
                
            else:
                print("❌ 反馈表不存在，请先创建表")
            
            conn.commit()
            conn.close()
            print("✅ 反馈表迁移完成")
            
        except Exception as e:
            print(f"❌ 迁移失败: {e}")
    
    def create_test_feedback_data(self):
        """创建测试反馈数据"""
        print("🔧 创建测试反馈数据...")
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 获取用户数据
            cursor.execute("SELECT id, first_name, last_name, user_type FROM user")
            users = cursor.fetchall()
            
            employees = []
            executives = []
            
            for user in users:
                user_id, first_name, last_name, user_type = user
                if user_type == 'employee':
                    employees.append(user_id)
                elif user_type in ['executive', 'supervisor']:
                    executives.append(user_id)
            
            print(f"找到 {len(employees)} 个员工")
            print(f"找到 {len(executives)} 个高管/主管")
            
            if not employees or not executives:
                print("❌ 没有足够的用户数据来创建反馈")
                return
            
            # 反馈分类和类型
            categories = ['skill', 'communication', 'performance', 'general']
            feedback_types = ['positive', 'constructive', 'improvement', 'request']
            priorities = ['high', 'medium', 'low']
            
            # 创建员工发送给高管的反馈
            print("\n📝 创建员工发送给高管的反馈...")
            
            feedback_contents = [
                "希望公司能够提供更多的技术培训机会，特别是关于新技术的培训。",
                "建议改进团队沟通机制，定期召开项目进度会议。",
                "对当前的工作流程有一些优化建议，希望能够提高工作效率。",
                "感谢领导的指导和支持，在工作中学习到了很多。",
                "希望公司能够考虑增加一些员工福利，比如弹性工作时间。",
                "对项目进度安排有一些疑问，希望能够得到更详细的说明。",
                "建议增加团队建设活动，促进同事之间的交流。",
                "对个人职业发展有一些想法，希望能够得到指导。",
                "工作中遇到了一些技术难题，希望能够得到帮助。",
                "对公司的发展方向很感兴趣，希望能够了解更多信息。"
            ]
            
            # 创建10条员工发送给高管的反馈
            for i in range(10):
                import random
                sender_id = random.choice(employees)
                recipient_id = random.choice(executives)
                category = random.choice(categories)
                feedback_type = random.choice(feedback_types)
                priority = random.choice(priorities)
                content = random.choice(feedback_contents)
                
                # 创建随机时间（最近30天内）
                from datetime import timedelta
                days_ago = random.randint(0, 30)
                created_at = datetime.now() - timedelta(days=days_ago)
                
                cursor.execute("""
                    INSERT INTO feedback (sender_id, recipient_id, category, feedback_type, 
                                        content, priority, status, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (sender_id, recipient_id, category, feedback_type, content, priority, 'sent', created_at))
                
                print(f"  - 员工 {sender_id} → 高管 {recipient_id}: {content[:30]}...")
            
            # 创建高管发送给员工的反馈
            print("\n📝 创建高管发送给员工的反馈...")
            
            executive_feedback_contents = [
                "你在项目中的表现很出色，继续保持这种工作态度。",
                "建议你在团队协作方面可以更加积极主动一些。",
                "你的技术能力很强，建议可以多分享经验给其他同事。",
                "希望你在时间管理方面能够更加高效。",
                "你的创新思维很有价值，建议可以提出更多改进建议。",
                "在沟通表达方面还有提升空间，建议多参加相关培训。",
                "你的责任心很强，这是很好的品质。",
                "建议你可以承担更多有挑战性的任务。",
                "你的学习能力很强，继续保持这种学习热情。",
                "在项目管理方面表现不错，希望再接再厉。"
            ]
            
            # 创建5条高管发送给员工的反馈
            for i in range(5):
                sender_id = random.choice(executives)
                recipient_id = random.choice(employees)
                category = random.choice(categories)
                feedback_type = random.choice(feedback_types)
                priority = random.choice(priorities)
                content = random.choice(executive_feedback_contents)
                
                # 创建随机时间（最近30天内）
                days_ago = random.randint(0, 30)
                created_at = datetime.now() - timedelta(days=days_ago)
                
                cursor.execute("""
                    INSERT INTO feedback (sender_id, recipient_id, category, feedback_type, 
                                        content, priority, status, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (sender_id, recipient_id, category, feedback_type, content, priority, 'sent', created_at))
                
                print(f"  - 高管 {sender_id} → 员工 {recipient_id}: {content[:30]}...")
            
            # 提交事务
            conn.commit()
            
            # 验证创建的数据
            cursor.execute("SELECT COUNT(*) FROM feedback")
            total_feedback = cursor.fetchone()[0]
            print(f"\n✅ 成功创建反馈数据，总计: {total_feedback} 条")
            
            conn.close()
            print("🎉 测试反馈数据创建完成！")
            
        except Exception as e:
            print(f"❌ 创建失败: {e}")
    
    def check_feedback_data(self):
        """检查反馈数据"""
        print("🔍 检查反馈数据...")
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 检查反馈总数
            cursor.execute("SELECT COUNT(*) FROM feedback")
            total_feedback = cursor.fetchone()[0]
            print(f"总反馈数量: {total_feedback}")
            
            # 检查员工发送给高管的反馈
            cursor.execute("""
                SELECT COUNT(*) FROM feedback f
                JOIN user sender ON f.sender_id = sender.id
                JOIN user recipient ON f.recipient_id = recipient.id
                WHERE sender.user_type = 'employee' 
                AND recipient.user_type IN ('executive', 'supervisor')
            """)
            employee_to_executive = cursor.fetchone()[0]
            print(f"员工发送给高管的反馈: {employee_to_executive}")
            
            # 检查高管发送给员工的反馈
            cursor.execute("""
                SELECT COUNT(*) FROM feedback f
                JOIN user sender ON f.sender_id = sender.id
                JOIN user recipient ON f.recipient_id = recipient.id
                WHERE sender.user_type IN ('executive', 'supervisor')
                AND recipient.user_type = 'employee'
            """)
            executive_to_employee = cursor.fetchone()[0]
            print(f"高管发送给员工的反馈: {executive_to_employee}")
            
            # 显示最近的反馈记录
            print("\n最近的反馈记录:")
            cursor.execute("""
                SELECT f.id, 
                       sender.first_name || ' ' || sender.last_name as sender_name,
                       sender.user_type as sender_type,
                       recipient.first_name || ' ' || recipient.last_name as recipient_name,
                       recipient.user_type as recipient_type,
                       f.category, f.feedback_type, f.status, f.created_at
                FROM feedback f
                JOIN user sender ON f.sender_id = sender.id
                JOIN user recipient ON f.recipient_id = recipient.id
                ORDER BY f.created_at DESC
                LIMIT 10
            """)
            
            recent_feedbacks = cursor.fetchall()
            for feedback in recent_feedbacks:
                feedback_id, sender_name, sender_type, recipient_name, recipient_type, category, feedback_type, status, created_at = feedback
                print(f"  - ID: {feedback_id}")
                print(f"    {sender_name} ({sender_type}) → {recipient_name} ({recipient_type})")
                print(f"    分类: {category}, 类型: {feedback_type}, 状态: {status}")
                print(f"    时间: {created_at}")
                print()
            
            conn.close()
            print("✅ 检查完成")
            
        except Exception as e:
            print(f"❌ 检查失败: {e}")

def main():
    """主函数"""
    tool = DatabaseMigrationTool()
    
    print("🚀 数据库迁移工具")
    print("=" * 50)
    
    while True:
        print("\n请选择操作:")
        print("1. 检查数据库结构")
        print("2. 迁移反馈表")
        print("3. 创建测试反馈数据")
        print("4. 检查反馈数据")
        print("5. 执行完整迁移流程")
        print("0. 退出")
        
        choice = input("\n请输入选择 (0-5): ").strip()
        
        if choice == '1':
            tool.check_database_structure()
        elif choice == '2':
            tool.migrate_feedback_table()
        elif choice == '3':
            tool.create_test_feedback_data()
        elif choice == '4':
            tool.check_feedback_data()
        elif choice == '5':
            print("\n🔄 执行完整迁移流程...")
            tool.check_database_structure()
            tool.migrate_feedback_table()
            tool.create_test_feedback_data()
            tool.check_feedback_data()
            print("\n✅ 完整迁移流程完成！")
        elif choice == '0':
            print("👋 再见！")
            break
        else:
            print("❌ 无效选择，请重新输入")

if __name__ == "__main__":
    main()
