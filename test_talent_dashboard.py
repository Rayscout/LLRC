#!/usr/bin/env python3
"""
人才发展大盘功能测试脚本
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_talent_analysis():
    """测试人才分析功能"""
    try:
        from app import create_app, db
        from app.models import User, TalentDevelopmentData, MarketSalaryData
        from app.talent_analysis_service import TalentAnalysisService
        
        app = create_app()
        
        with app.app_context():
            print("=" * 50)
            print("人才发展大盘功能测试")
            print("=" * 50)
            
            # 测试数据统计
            total_employees = TalentDevelopmentData.query.count()
            total_market_data = MarketSalaryData.query.count()
            executive_users = User.query.filter_by(user_type='executive').count()
            
            print(f"✓ 员工数据: {total_employees} 条")
            print(f"✓ 市场数据: {total_market_data} 条")
            print(f"✓ 高管用户: {executive_users} 个")
            
            # 测试分析服务
            analysis_service = TalentAnalysisService()
            
            # 获取一个员工进行测试
            talent_data = TalentDevelopmentData.query.first()
            if talent_data:
                print(f"\n测试员工: {talent_data.employee.first_name} {talent_data.employee.last_name}")
                print(f"职位: {talent_data.position}")
                print(f"部门: {talent_data.department}")
                print(f"薪资: ¥{talent_data.salary:,.2f}")
                
                # 测试离职风险分析
                print("\n--- 离职风险分析 ---")
                risk_result = analysis_service.analyze_employee_turnover_risk(talent_data.employee_id)
                if 'error' not in risk_result:
                    print(f"风险概率: {risk_result.get('turnover_risk', 0):.1%}")
                    print(f"风险等级: {risk_result.get('risk_level', '未知')}")
                    print(f"风险因素: {risk_result.get('risk_factors', [])}")
                else:
                    print(f"分析失败: {risk_result['error']}")
                
                # 测试市场对比分析
                print("\n--- 市场对比分析 ---")
                market_result = analysis_service.analyze_market_comparison(talent_data.position, talent_data.salary)
                if 'error' not in market_result:
                    print(f"薪资竞争力: {market_result.get('salary_competitiveness', 0):.2f}")
                    print(f"市场位置: {market_result.get('market_position', '未知')}")
                else:
                    print(f"分析失败: {market_result['error']}")
                
                # 测试趋势预测
                print("\n--- 趋势预测 ---")
                trend_result = analysis_service.analyze_trend_forecast(talent_data.position)
                if 'error' not in trend_result:
                    print(f"预测摘要: {trend_result.get('forecast_summary', '未知')}")
                else:
                    print(f"分析失败: {trend_result['error']}")
            
            print("\n" + "=" * 50)
            print("测试完成！")
            print("=" * 50)
            
    except Exception as e:
        print(f"测试失败: {e}")
        import traceback
        traceback.print_exc()

def test_pdf_generation():
    """测试PDF生成功能"""
    try:
        from app import create_app
        from app.models import TalentDevelopmentData
        from app.pdf_generator import TalentReportGenerator
        
        app = create_app()
        
        with app.app_context():
            print("\n--- PDF生成测试 ---")
            
            # 获取一个员工数据
            talent_data = TalentDevelopmentData.query.first()
            if talent_data:
                # 创建报告生成器
                generator = TalentReportGenerator()
                
                # 模拟报告数据
                report_data = {
                    "employee_info": {
                        "name": f"{talent_data.employee.first_name} {talent_data.employee.last_name}",
                        "position": talent_data.position,
                        "department": talent_data.department,
                        "salary": talent_data.salary,
                        "hire_date": talent_data.hire_date.strftime("%Y-%m-%d") if talent_data.hire_date else None
                    },
                    "turnover_analysis": {
                        "turnover_risk": talent_data.turnover_risk,
                        "risk_level": "中风险" if talent_data.turnover_risk < 0.6 else "高风险",
                        "risk_factors": ["薪资低于市场水平", "绩效评分较低"],
                        "recommendations": ["考虑调整薪资", "制定绩效改进计划"]
                    },
                    "market_analysis": {
                        "salary_competitiveness": 0.95,
                        "market_position": "接近平均",
                        "advantages": ["工作环境良好"],
                        "disadvantages": ["薪资略低于市场"]
                    },
                    "performance_summary": {
                        "performance_score": talent_data.performance_score,
                        "skills_level": talent_data.skills_level,
                        "satisfaction_score": talent_data.satisfaction_score,
                        "teamwork_score": talent_data.teamwork_score,
                        "leadership_potential": talent_data.leadership_potential
                    }
                }
                
                # 生成PDF报告
                pdf_path = generator.generate_individual_report(report_data, talent_data.employee.first_name)
                print(f"✓ PDF报告生成成功: {pdf_path}")
                
                # 检查文件是否存在
                if os.path.exists(pdf_path):
                    file_size = os.path.getsize(pdf_path)
                    print(f"✓ 文件大小: {file_size} 字节")
                else:
                    print("✗ PDF文件未找到")
            else:
                print("✗ 没有找到员工数据")
                
    except Exception as e:
        print(f"PDF生成测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_talent_analysis()
    test_pdf_generation()
