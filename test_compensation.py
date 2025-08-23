#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试薪酬管理功能
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_compensation():
    """测试薪酬管理功能"""
    print("💰 测试薪酬管理功能...")
    print("=" * 60)
    
    try:
        from app import create_app, db
        from app.models import User
        from talent_management_system.employee_manager_module.compensation import (
            get_user_compensation, get_department_comparison, get_company_percentile,
            get_salary_trends, analyze_compensation_structure, calculate_percentile,
            calculate_company_percentile, get_percentile_label, generate_company_salary_distribution,
            get_market_positioning, analyze_growth_potential, generate_compensation_recommendations
        )
        
        print("✅ 模块导入成功")
        
        # 创建应用上下文
        app = create_app()
        with app.app_context():
            print("✅ 应用上下文创建成功")
            
            # 测试数据库连接
            try:
                # 使用新的SQLAlchemy语法
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
            
            # 测试薪酬信息获取
            print("\n📊 测试薪酬信息获取...")
            try:
                user_comp = get_user_compensation(user)
                print(f"✅ 基本工资: ¥{user_comp['base_salary']:,}")
                print(f"✅ 奖金: ¥{user_comp['bonus']:,}")
                print(f"✅ 总薪酬: ¥{user_comp['total']:,}")
            except Exception as e:
                print(f"❌ 薪酬信息获取失败: {e}")
                return False
            
            # 测试部门对比
            print("\n⚖️ 测试部门对比...")
            try:
                dept_comp = get_department_comparison(user)
                print(f"✅ 部门: {dept_comp['department']}")
                print(f"✅ 部门平均基本工资: ¥{dept_comp['department_avg']['base_salary']:,}")
                print(f"✅ 部门平均奖金: ¥{dept_comp['department_avg']['bonus']:,}")
                print(f"✅ 基本工资差异: ¥{dept_comp['comparison']['base_salary_diff']:,}")
            except Exception as e:
                print(f"❌ 部门对比失败: {e}")
                return False
            
            # 测试公司百分位
            print("\n📈 测试公司百分位...")
            try:
                company_percentile = get_company_percentile(user)
                print(f"✅ 公司百分位: {company_percentile['percentile']}%")
                print(f"✅ 百分位标签: {company_percentile['percentile_label']}")
                print(f"✅ 公司平均: ¥{company_percentile['company_avg']:,.0f}")
            except Exception as e:
                print(f"❌ 公司百分位计算失败: {e}")
                return False
            
            # 测试薪酬趋势
            print("\n📉 测试薪酬趋势...")
            try:
                trends = get_salary_trends(user)
                print(f"✅ 趋势数据点数: {len(trends)}")
                print(f"✅ 最新月份: {trends[-1]['month']}")
                print(f"✅ 最新总薪酬: ¥{trends[-1]['total']:,}")
            except Exception as e:
                print(f"❌ 薪酬趋势获取失败: {e}")
                return False
            
            # 测试薪酬结构分析
            print("\n🔍 测试薪酬结构分析...")
            try:
                structure = analyze_compensation_structure(user)
                print(f"✅ 基本工资比例: {structure['base_salary_ratio']}%")
                print(f"✅ 奖金比例: {structure['bonus_ratio']}%")
                print(f"✅ 建议数量: {len(structure['recommendations'])}")
            except Exception as e:
                print(f"❌ 薪酬结构分析失败: {e}")
                return False
            
            # 测试辅助函数
            print("\n🛠️ 测试辅助函数...")
            try:
                # 测试百分位计算
                percentile = calculate_percentile(15000, (10000, 20000))
                print(f"✅ 百分位计算: {percentile}%")
                
                # 测试百分位标签
                label = get_percentile_label(85)
                print(f"✅ 百分位标签: {label}")
                
                # 测试公司薪酬分布生成
                distribution = generate_company_salary_distribution()
                print(f"✅ 薪酬分布样本数: {len(distribution)}")
                print(f"✅ 分布范围: ¥{min(distribution):,} - ¥{max(distribution):,}")
                
            except Exception as e:
                print(f"❌ 辅助函数测试失败: {e}")
                return False
            
            # 测试蓝图路由
            print("\n🌐 测试蓝图路由...")
            try:
                from talent_management_system.employee_manager_module.compensation import compensation_bp
                print(f"✅ 蓝图名称: {compensation_bp.name}")
                print(f"✅ URL前缀: {compensation_bp.url_prefix}")
                
                # 检查蓝图注册
                print(f"✅ 蓝图已成功导入")
                print(f"✅ 蓝图URL前缀: {compensation_bp.url_prefix}")
                
            except Exception as e:
                print(f"❌ 蓝图路由测试失败: {e}")
                return False
            
            print("\n🎉 所有测试通过！薪酬管理功能正常工作")
            return True
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_compensation()
