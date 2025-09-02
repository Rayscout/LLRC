#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
人才管理系统工具脚本
用于运行各种调试、状态检查和维护功能
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def show_menu():
    """显示工具菜单"""
    print("🔧 人才管理系统工具")
    print("=" * 50)
    print("1. 员工界面状态检查")
    print("2. 员工错误调试")
    print("3. 员工路由调试")
    print("4. 员工认证调试")
    print("5. 高管认证测试")
    print("6. 完整系统检查")
    print("0. 退出")
    print("=" * 50)

def run_employee_interface_status():
    """运行员工界面状态检查"""
    print("\n📊 员工界面状态检查")
    print("-" * 30)
    from employee_manager_module.status_check import employee_interface_status
    employee_interface_status()

def run_debug_employee_errors():
    """运行员工错误调试"""
    print("\n🔍 员工错误调试")
    print("-" * 30)
    from employee_manager_module.debug_tools import debug_employee_errors
    debug_employee_errors()

def run_debug_employee_routes():
    """运行员工路由调试"""
    print("\n🔍 员工路由调试")
    print("-" * 30)
    from employee_manager_module.debug_tools import debug_employee_routes
    debug_employee_routes()

def run_debug_employee_auth():
    """运行员工认证调试"""
    print("\n🔍 员工认证调试")
    print("-" * 30)
    from employee_manager_module.debug_tools import debug_employee_auth
    debug_employee_auth()

def run_executive_auth_test():
    """运行高管认证测试"""
    print("\n🔍 高管认证测试")
    print("-" * 30)
    from test_executive_auth import test_executive_auth
    test_executive_auth()

def run_full_system_check():
    """运行完整系统检查"""
    print("\n🔍 完整系统检查")
    print("-" * 30)
    
    # 员工界面状态检查
    print("1. 员工界面状态检查...")
    run_employee_interface_status()
    
    print("\n" + "=" * 50)
    
    # 员工错误调试
    print("2. 员工错误调试...")
    run_debug_employee_errors()
    
    print("\n" + "=" * 50)
    
    # 员工路由调试
    print("3. 员工路由调试...")
    run_debug_employee_routes()
    
    print("\n" + "=" * 50)
    
    # 员工认证调试
    print("4. 员工认证调试...")
    run_debug_employee_auth()
    
    print("\n" + "=" * 50)
    
    # 高管认证测试
    print("5. 高管认证测试...")
    run_executive_auth_test()
    
    print("\n" + "=" * 50)
    print("✅ 完整系统检查完成")

def main():
    """主函数"""
    while True:
        show_menu()
        
        try:
            choice = input("请选择功能 (0-5): ").strip()
            
            if choice == '0':
                print("👋 再见！")
                break
            elif choice == '1':
                run_employee_interface_status()
            elif choice == '2':
                run_debug_employee_errors()
            elif choice == '3':
                run_debug_employee_routes()
            elif choice == '4':
                run_debug_employee_auth()
            elif choice == '5':
                run_executive_auth_test()
            elif choice == '6':
                run_full_system_check()
            else:
                print("❌ 无效选择，请重新输入")
                
        except KeyboardInterrupt:
            print("\n👋 再见！")
            break
        except Exception as e:
            print(f"❌ 执行出错: {e}")
        
        input("\n按回车键继续...")

if __name__ == "__main__":
    main()
