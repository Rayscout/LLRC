"""
LLRC Header Start
文件功能: 通用 Python 脚本/模块：scripts/init_talent_data.py
创建时间: 2025-08-22 09:28
创建人: 潘显雨
更新记录:
- 2025-08-22 09:58 by 苏杰
- 2025-08-22 17:49 by 李雨梦
LLRC Header End
"""
#!/usr/bin/env python3
"""
FILE-HEADER-AUTO-ADDED
文件: scripts/init_talent_data.py
功能: 通用模块
创建时间: 2025-08-23 17:25
创建人: 潘显雨
更新记录:
- 2025-08-24 09:48 by 苏杰
"""
"""
人才发展数据初始化脚本
生成100组示例数据用于测试和演示
"""

import sys
import os
import random
from datetime import datetime, timedelta
import json

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import User, TalentDevelopmentData, MarketSalaryData

def generate_sample_data():
    """生成示例数据"""
    
    # 职位列表
    positions = [
        "软件工程师", "产品经理", "UI设计师", "数据分析师", "运营专员",
        "市场专员", "销售代表", "人力资源专员", "财务专员", "法务专员",
        "项目经理", "技术总监", "产品总监", "市场总监", "销售总监",
        "人力资源总监", "财务总监", "法务总监", "CEO", "CTO"
    ]
    
    # 部门列表
    departments = [
        "技术部", "产品部", "设计部", "数据分析部", "运营部",
        "市场部", "销售部", "人力资源部", "财务部", "法务部",
        "总裁办", "战略部"
    ]
    
    # 行业列表
    industries = [
        "互联网", "金融", "教育", "医疗", "制造业",
        "零售", "房地产", "咨询", "媒体", "游戏"
    ]
    
    # 地区列表
    locations = [
        "北京", "上海", "深圳", "广州", "杭州",
        "成都", "武汉", "西安", "南京", "苏州"
    ]
    
    # 经验级别
    experience_levels = ["初级", "中级", "高级", "专家"]
    
    app = create_app()
    
    with app.app_context():
        # 清空现有数据
        TalentDevelopmentData.query.delete()
        MarketSalaryData.query.delete()
        db.session.commit()
        
        print("开始生成示例数据...")
        
        # 生成市场薪资数据
        print("生成市场薪资数据...")
        for position in positions:
            for industry in industries[:3]:  # 每个职位选择3个行业
                for location in locations[:3]:  # 每个职位选择3个地区
                    for exp_level in experience_levels:
                        # 根据职位和经验级别生成薪资范围
                        base_salary = generate_base_salary(position, exp_level)
                        min_salary = base_salary * 0.8
                        max_salary = base_salary * 1.3
                        avg_salary = (min_salary + max_salary) / 2
                        median_salary = base_salary * 1.05
                        
                        # 生成趋势数据
                        demand_trend = random.uniform(-0.2, 0.8)
                        supply_trend = random.uniform(-0.3, 0.6)
                        
                        market_data = MarketSalaryData(
                            position=position,
                            industry=industry,
                            location=location,
                            experience_level=exp_level,
                            min_salary=min_salary,
                            max_salary=max_salary,
                            avg_salary=avg_salary,
                            median_salary=median_salary,
                            demand_trend=demand_trend,
                            supply_trend=supply_trend,
                            data_date=datetime.now().date()
                        )
                        db.session.add(market_data)
        
        db.session.commit()
        print(f"已生成 {len(positions) * 3 * 3 * 4} 条市场薪资数据")
        
        # 生成员工数据
        print("生成员工数据...")
        
        # 获取现有用户或创建新用户
        existing_users = User.query.filter_by(user_type='employee').all()
        
        if len(existing_users) < 100:
            # 创建新用户
            for i in range(100 - len(existing_users)):
                user = User(
                    first_name=f"员工{i+1}",
                    last_name="",
                    company_name="示例公司",
                    position=random.choice(positions),
                    email=f"employee{i+1}@example.com",
                    phone_number=f"138{random.randint(10000000, 99999999)}",
                    birthday="1990-01-01",
                    password="password123",
                    user_type='employee',
                    department=random.choice(departments),
                    employee_id=f"EMP{str(i+1).zfill(3)}",
                    hire_date=datetime.now().date() - timedelta(days=random.randint(30, 365*5))
                )
                db.session.add(user)
            
            db.session.commit()
            existing_users = User.query.filter_by(user_type='employee').all()
        
        # 为每个员工生成人才发展数据
        for user in existing_users[:100]:  # 确保只处理100个用户
            # 获取对应的市场数据
            market_data = MarketSalaryData.query.filter_by(
                position=user.position
            ).first()
            
            if not market_data:
                # 如果没有对应的市场数据，创建一个默认的
                base_salary = generate_base_salary(user.position, "中级")
                market_data = MarketSalaryData(
                    position=user.position,
                    industry="互联网",
                    location="北京",
                    experience_level="中级",
                    min_salary=base_salary * 0.8,
                    max_salary=base_salary * 1.3,
                    avg_salary=base_salary,
                    median_salary=base_salary * 1.05,
                    demand_trend=0.5,
                    supply_trend=0.3,
                    data_date=datetime.now().date()
                )
                db.session.add(market_data)
                db.session.commit()
            
            # 生成员工薪资（基于市场数据）
            salary_variation = random.uniform(0.7, 1.4)
            salary = market_data.avg_salary * salary_variation
            
            # 生成绩效相关数据
            performance_score = random.uniform(2.5, 5.0)
            promotion_count = random.randint(0, 3)
            last_promotion_date = None
            if promotion_count > 0:
                last_promotion_date = user.hire_date + timedelta(days=random.randint(365, 365*3))
            
            # 生成技能发展数据
            skills_level = random.uniform(2.0, 5.0)
            training_hours = random.uniform(0, 200)
            certification_count = random.randint(0, 5)
            
            # 生成工作满意度数据
            satisfaction_score = random.uniform(2.0, 5.0)
            work_life_balance = random.uniform(2.0, 5.0)
            
            # 生成团队协作数据
            teamwork_score = random.uniform(2.5, 5.0)
            leadership_potential = random.uniform(1.0, 5.0)
            
            # 生成市场竞争力数据
            market_salary = market_data.avg_salary
            market_demand = market_data.demand_trend
            
            # 计算离职风险（简化计算）
            risk_factors = []
            risk_score = 0.0
            
            # 薪资满意度
            salary_ratio = salary / market_salary
            if salary_ratio < 0.8:
                risk_factors.append("薪资低于市场水平")
                risk_score += 0.3
            elif salary_ratio > 1.2:
                risk_score += 0.1
            
            # 绩效评分
            if performance_score < 3.0:
                risk_factors.append("绩效评分较低")
                risk_score += 0.2
            
            # 工作满意度
            if satisfaction_score < 3.0:
                risk_factors.append("工作满意度较低")
                risk_score += 0.25
            
            # 晋升机会
            years_employed = (datetime.now().date() - user.hire_date).days / 365
            if years_employed > 3 and promotion_count == 0:
                risk_factors.append("长期无晋升机会")
                risk_score += 0.2
            
            # 技能发展
            if skills_level < 3.0:
                risk_factors.append("技能发展受限")
                risk_score += 0.15
            
            # 工作生活平衡
            if work_life_balance < 3.0:
                risk_factors.append("工作生活平衡差")
                risk_score += 0.1
            
            # 限制风险分数
            risk_score = min(max(risk_score, 0.0), 1.0)
            
            # 创建人才发展数据
            talent_data = TalentDevelopmentData(
                employee_id=user.id,
                position=user.position,
                department=user.department,
                salary=salary,
                hire_date=user.hire_date,
                performance_score=performance_score,
                promotion_count=promotion_count,
                last_promotion_date=last_promotion_date,
                skills_level=skills_level,
                training_hours=training_hours,
                certification_count=certification_count,
                satisfaction_score=satisfaction_score,
                work_life_balance=work_life_balance,
                teamwork_score=teamwork_score,
                leadership_potential=leadership_potential,
                market_salary=market_salary,
                market_demand=market_demand,
                turnover_risk=risk_score,
                risk_factors=json.dumps(risk_factors, ensure_ascii=False)
            )
            
            db.session.add(talent_data)
        
        db.session.commit()
        print(f"已生成 {len(existing_users[:100])} 条员工人才发展数据")
        
        print("示例数据生成完成！")
        
        # 打印统计信息
        print("\n数据统计:")
        print(f"市场薪资数据: {MarketSalaryData.query.count()} 条")
        print(f"人才发展数据: {TalentDevelopmentData.query.count()} 条")
        
        # 按部门统计
        dept_stats = db.session.query(
            TalentDevelopmentData.department,
            db.func.count(TalentDevelopmentData.id)
        ).group_by(TalentDevelopmentData.department).all()
        
        print("\n部门分布:")
        for dept, count in dept_stats:
            print(f"  {dept}: {count} 人")
        
        # 风险分布
        low_risk = TalentDevelopmentData.query.filter(TalentDevelopmentData.turnover_risk < 0.3).count()
        medium_risk = TalentDevelopmentData.query.filter(
            TalentDevelopmentData.turnover_risk >= 0.3,
            TalentDevelopmentData.turnover_risk < 0.6
        ).count()
        high_risk = TalentDevelopmentData.query.filter(TalentDevelopmentData.turnover_risk >= 0.6).count()
        
        print(f"\n风险分布:")
        print(f"  低风险: {low_risk} 人 ({low_risk/100*100:.1f}%)")
        print(f"  中风险: {medium_risk} 人 ({medium_risk/100*100:.1f}%)")
        print(f"  高风险: {high_risk} 人 ({high_risk/100*100:.1f}%)")

def generate_base_salary(position, experience_level):
    """根据职位和经验级别生成基础薪资"""
    base_salaries = {
        "软件工程师": {"初级": 8000, "中级": 15000, "高级": 25000, "专家": 40000},
        "产品经理": {"初级": 10000, "中级": 18000, "高级": 30000, "专家": 50000},
        "UI设计师": {"初级": 7000, "中级": 12000, "高级": 20000, "专家": 35000},
        "数据分析师": {"初级": 9000, "中级": 16000, "高级": 28000, "专家": 45000},
        "运营专员": {"初级": 6000, "中级": 10000, "高级": 18000, "专家": 30000},
        "市场专员": {"初级": 7000, "中级": 12000, "高级": 22000, "专家": 38000},
        "销售代表": {"初级": 5000, "中级": 10000, "高级": 20000, "专家": 35000},
        "人力资源专员": {"初级": 6000, "中级": 11000, "高级": 20000, "专家": 32000},
        "财务专员": {"初级": 7000, "中级": 13000, "高级": 22000, "专家": 35000},
        "法务专员": {"初级": 8000, "中级": 15000, "高级": 25000, "专家": 40000},
        "项目经理": {"初级": 12000, "中级": 20000, "高级": 35000, "专家": 55000},
        "技术总监": {"初级": 25000, "中级": 40000, "高级": 60000, "专家": 80000},
        "产品总监": {"初级": 30000, "中级": 45000, "高级": 65000, "专家": 90000},
        "市场总监": {"初级": 25000, "中级": 40000, "高级": 60000, "专家": 80000},
        "销售总监": {"初级": 20000, "中级": 35000, "高级": 55000, "专家": 75000},
        "人力资源总监": {"初级": 20000, "中级": 35000, "高级": 55000, "专家": 75000},
        "财务总监": {"初级": 25000, "中级": 40000, "高级": 60000, "专家": 80000},
        "法务总监": {"初级": 25000, "中级": 40000, "高级": 60000, "专家": 80000},
        "CEO": {"初级": 50000, "中级": 80000, "高级": 120000, "专家": 200000},
        "CTO": {"初级": 40000, "中级": 60000, "高级": 90000, "专家": 150000}
    }
    
    return base_salaries.get(position, {"中级": 15000}).get(experience_level, 15000)

if __name__ == "__main__":
    generate_sample_data()
