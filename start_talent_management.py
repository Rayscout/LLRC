#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
人才管理系统启动脚本
整合数据库迁移、测试和系统启动功能
"""

import os
import sys
import subprocess
from pathlib import Path

def setup_environment():
    """设置环境"""
    print("🔧 设置环境...")
    
    # 添加项目根目录到Python路径
    project_root = Path(__file__).parent
    sys.path.insert(0, str(project_root))
    
    # 设置环境变量
    os.environ['FLASK_APP'] = 'run_app.py'
    os.environ['FLASK_ENV'] = 'development'
    
    print("✅ 环境设置完成")

def run_database_migration():
    """运行数据库迁移"""
    print("\n🗄️ 运行数据库迁移...")
    
    try:
        # 导入迁移工具
        from talent_management_system.tools.database_migration import DatabaseMigrationTool
        
        tool = DatabaseMigrationTool()
        
        # 执行完整迁移流程
        print("1. 检查数据库结构...")
        tool.check_database_structure()
        
        print("2. 迁移反馈表...")
        tool.migrate_feedback_table()
        
        print("3. 创建测试反馈数据...")
        tool.create_test_feedback_data()
        
        print("4. 检查反馈数据...")
        tool.check_feedback_data()
        
        print("✅ 数据库迁移完成")
        return True
        
    except Exception as e:
        print(f"❌ 数据库迁移失败: {e}")
        return False

def run_system_tests():
    """运行系统测试"""
    print("\n🧪 运行系统测试...")
    
    try:
        # 导入测试工具
        from talent_management_system.tools.feedback_test_tool import FeedbackTestTool
        
        tool = FeedbackTestTool()
        
        # 执行测试
        print("1. 测试反馈系统功能...")
        tool.test_feedback_system()
        
        print("2. 测试员工反馈功能...")
        tool.test_employee_feedback()
        
        print("3. 测试高管反馈功能...")
        tool.test_executive_feedback()
        
        print("4. 生成测试报告...")
        tool.generate_test_report()
        
        print("✅ 系统测试完成")
        return True
        
    except Exception as e:
        print(f"❌ 系统测试失败: {e}")
        return False

def fix_ui_issues():
    """修复UI问题"""
    print("\n🎨 修复UI问题...")
    
    try:
        # 导入UI修复工具
        from talent_management_system.tools.ui_fix_tool import UIFixTool
        
        tool = UIFixTool()
        
        # 执行UI修复
        print("1. 修复HR管理员仪表板...")
        tool.fix_hr_admin_dashboard()
        
        print("2. 修复员工反馈仪表板...")
        tool.fix_employee_feedback_dashboard()
        
        print("3. 创建UI修复脚本...")
        tool.create_ui_fix_script()
        
        print("4. 生成UI修复报告...")
        tool.generate_ui_report()
        
        print("✅ UI修复完成")
        return True
        
    except Exception as e:
        print(f"❌ UI修复失败: {e}")
        return False

def start_application():
    """启动应用程序"""
    print("\n🚀 启动人才管理系统...")
    
    try:
        # 检查Flask应用是否存在
        if not Path('run_app.py').exists():
            print("❌ 找不到 run_app.py 文件")
            return False
        
        # 启动Flask应用
        print("正在启动Flask应用...")
        print("访问地址: http://127.0.0.1:5000")
        print("按 Ctrl+C 停止应用")
        
        # 使用subprocess启动应用
        process = subprocess.Popen([sys.executable, 'run_app.py'])
        
        try:
            process.wait()
        except KeyboardInterrupt:
            print("\n🛑 正在停止应用...")
            process.terminate()
            process.wait()
            print("✅ 应用已停止")
        
        return True
        
    except Exception as e:
        print(f"❌ 启动应用失败: {e}")
        return False

def main():
    """主函数"""
    print("🎯 人才管理系统启动工具")
    print("=" * 60)
    
    # 设置环境
    setup_environment()
    
    while True:
        print("\n请选择操作:")
        print("1. 数据库迁移")
        print("2. 系统测试")
        print("3. UI修复")
        print("4. 启动应用")
        print("5. 完整启动流程")
        print("0. 退出")
        
        choice = input("\n请输入选择 (0-5): ").strip()
        
        if choice == '1':
            run_database_migration()
        elif choice == '2':
            run_system_tests()
        elif choice == '3':
            fix_ui_issues()
        elif choice == '4':
            start_application()
        elif choice == '5':
            print("\n🔄 执行完整启动流程...")
            
            print("\n步骤 1: 数据库迁移")
            if not run_database_migration():
                print("❌ 数据库迁移失败，停止启动")
                continue
            
            print("\n步骤 2: 系统测试")
            if not run_system_tests():
                print("⚠️ 系统测试失败，但继续启动")
            
            print("\n步骤 3: UI修复")
            if not fix_ui_issues():
                print("⚠️ UI修复失败，但继续启动")
            
            print("\n步骤 4: 启动应用")
            start_application()
            
            print("\n✅ 完整启动流程完成！")
        elif choice == '0':
            print("👋 再见！")
            break
        else:
            print("❌ 无效选择，请重新输入")

if __name__ == "__main__":
    main()
