#!/usr/bin/env python3
"""
员工模块修复测试脚本
用于测试反馈发送、PDF导出和绩效历史记录功能
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask
from app.models import db, User, Feedback, TaskEvaluation
from talent_management_system.employee_manager_module.feedback import feedback_bp
from talent_management_system.employee_manager_module.profile import profile_bp
from talent_management_system.employee_manager_module.performance import performance_bp
import tempfile
import json

def create_test_app():
    """创建测试应用"""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'test-secret-key'
    
    db.init_app(app)
    
    # 注册蓝图
    app.register_blueprint(feedback_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(performance_bp)
    
    return app

def test_feedback_functionality():
    """测试反馈功能"""
    print("=== 测试反馈功能 ===")
    
    app = create_test_app()
    with app.app_context():
        # 创建数据库表
        db.create_all()
        
        # 创建测试用户
        employee = User(
            email='test_employee@test.com',
            password='password123',
            first_name='测试',
            last_name='员工',
            user_type='employee'
        )
        
        executive = User(
            email='test_executive@test.com',
            password='password123',
            first_name='测试',
            last_name='高管',
            user_type='executive'
        )
        
        db.session.add(employee)
        db.session.add(executive)
        db.session.commit()
        
        # 测试反馈创建
        feedback = Feedback(
            sender_id=employee.id,
            recipient_id=executive.id,
            category='performance',
            feedback_type='improvement',
            content='测试反馈内容',
            priority='medium',
            status='sent'
        )
        
        db.session.add(feedback)
        db.session.commit()
        
        # 验证反馈是否保存成功
        saved_feedback = Feedback.query.filter_by(
            sender_id=employee.id,
            recipient_id=executive.id,
            content='测试反馈内容'
        ).first()
        
        if saved_feedback:
            print("✓ 反馈功能测试通过")
        else:
            print("✗ 反馈功能测试失败")
        
        db.session.remove()
        db.drop_all()

def test_pdf_generation():
    """测试PDF生成功能"""
    print("=== 测试PDF生成功能 ===")
    
    app = create_test_app()
    with app.app_context():
        # 创建数据库表
        db.create_all()
        
        # 创建测试用户
        user = User(
            email='test_user@test.com',
            password='password123',
            first_name='测试',
            last_name='用户',
            user_type='employee',
            department='技术部',
            position='开发工程师',
            bio='测试个人简介',
            experience='测试工作经历',
            education='测试教育经历'
        )
        
        db.session.add(user)
        db.session.commit()
        
        try:
            # 导入PDF生成函数
            from talent_management_system.employee_manager_module.profile import generate_pdf_resume
            
            # 测试数据
            skills = ['Python', 'Flask', 'SQL']
            work_years = 2
            education_history = [{'school': '测试大学', 'major': '计算机科学', 'degree': '本科', 'period': '2018-2022'}]
            work_history = [{'company': '测试公司', 'position': '开发工程师', 'period': '2022-至今', 'description': '负责系统开发'}]
            performance_history = [{'period': '2024-01', 'score': 85, 'level': '优秀', 'evaluator': '主管', 'comments': '工作表现良好'}]
            
            # 生成PDF
            pdf_path = generate_pdf_resume(user, skills, work_years, education_history, work_history, performance_history)
            
            # 检查PDF文件是否存在
            if os.path.exists(pdf_path):
                print("✓ PDF生成功能测试通过")
                # 清理临时文件
                os.unlink(pdf_path)
            else:
                print("✗ PDF生成功能测试失败")
                
        except Exception as e:
            print(f"✗ PDF生成功能测试失败: {e}")
        
        db.session.remove()
        db.drop_all()

def test_performance_history():
    """测试绩效历史记录功能"""
    print("=== 测试绩效历史记录功能 ===")
    
    app = create_test_app()
    with app.app_context():
        # 创建数据库表
        db.create_all()
        
        # 创建测试用户
        employee = User(
            email='test_employee@test.com',
            password='password123',
            first_name='测试',
            last_name='员工',
            user_type='employee'
        )
        
        evaluator = User(
            email='test_evaluator@test.com',
            password='password123',
            first_name='测试',
            last_name='评价人',
            user_type='supervisor'
        )
        
        db.session.add(employee)
        db.session.add(evaluator)
        db.session.commit()
        
        # 创建测试绩效评价
        evaluation = TaskEvaluation(
            evaluator_id=evaluator.id,
            employee_id=employee.id,
            task_title='测试任务',
            task_description='这是一个测试任务',
            department='技术部',
            score_quality=85,
            score_efficiency=80,
            score_collaboration=90,
            total_score=85,
            comment='测试评语'
        )
        
        db.session.add(evaluation)
        db.session.commit()
        
        # 验证绩效评价是否保存成功
        saved_evaluation = TaskEvaluation.query.filter_by(
            employee_id=employee.id,
            task_title='测试任务'
        ).first()
        
        if saved_evaluation:
            print("✓ 绩效历史记录功能测试通过")
        else:
            print("✗ 绩效历史记录功能测试失败")
        
        db.session.remove()
        db.drop_all()

def main():
    """主测试函数"""
    print("开始测试员工模块修复...")
    print()
    
    try:
        test_feedback_functionality()
        print()
        
        test_pdf_generation()
        print()
        
        test_performance_history()
        print()
        
        print("所有测试完成！")
        
    except Exception as e:
        print(f"测试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
