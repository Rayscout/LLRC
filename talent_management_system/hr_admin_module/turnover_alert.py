#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
人才流失预警系统
监控离职趋势，识别高风险岗位，生成预警报告
"""

from flask import Blueprint, render_template, request, jsonify, session
from app.models import User, db
from datetime import datetime, timedelta
import json
import random
import uuid

turnover_alert_bp = Blueprint('turnover_alert', __name__, url_prefix='/turnover_alert')

# 模拟离职数据存储
TURNOVER_DATA = {}
EMPLOYEE_RISK_SCORES = {}
DEPARTMENT_STATS = {}
POSITION_ANALYSIS = {}

def generate_mock_turnover_data():
    """生成模拟离职数据"""
    global TURNOVER_DATA, EMPLOYEE_RISK_SCORES, DEPARTMENT_STATS, POSITION_ANALYSIS
    
    # 模拟部门统计
    departments = ['技术部', '产品部', '设计部', '市场部', '销售部', '人事部', '财务部']
    positions = ['软件工程师', '产品经理', 'UI设计师', '市场专员', '销售代表', 'HR专员', '财务专员']
    
    # 生成部门离职统计
    for dept in departments:
        total_employees = random.randint(20, 100)
        turnover_rate = random.uniform(0.05, 0.25)  # 5%-25%的离职率
        turnover_count = int(total_employees * turnover_rate)
        
        DEPARTMENT_STATS[dept] = {
            'total_employees': total_employees,
            'turnover_count': turnover_count,
            'turnover_rate': turnover_rate,
            'avg_salary': random.randint(8000, 25000),
            'avg_tenure': random.uniform(1.5, 4.0),
            'risk_level': 'high' if turnover_rate > 0.15 else 'medium' if turnover_rate > 0.10 else 'low'
        }
    
    # 生成岗位分析数据
    for pos in positions:
        market_demand = random.uniform(0.7, 1.3)  # 市场需求系数
        skill_gap = random.uniform(0.1, 0.4)  # 技能差距
        salary_competitiveness = random.uniform(0.6, 1.2)  # 薪资竞争力
        
        POSITION_ANALYSIS[pos] = {
            'market_demand': market_demand,
            'skill_gap': skill_gap,
            'salary_competitiveness': salary_competitiveness,
            'turnover_risk': calculate_position_risk(market_demand, skill_gap, salary_competitiveness),
            'main_reasons': generate_turnover_reasons(market_demand, skill_gap, salary_competitiveness)
        }
    
    # 生成员工风险评分
    for i in range(50):
        employee_id = str(uuid.uuid4())
        risk_score = random.uniform(0.1, 0.9)
        
        EMPLOYEE_RISK_SCORES[employee_id] = {
            'id': employee_id,
            'name': f'员工{i+1}',
            'department': random.choice(departments),
            'position': random.choice(positions),
            'risk_score': risk_score,
            'risk_level': 'high' if risk_score > 0.7 else 'medium' if risk_score > 0.4 else 'low',
            'tenure': random.uniform(0.5, 5.0),
            'last_promotion': random.randint(0, 24),  # 月数
            'salary_growth': random.uniform(-0.1, 0.3),  # 薪资增长率
            'performance_rating': random.uniform(2.5, 5.0),
            'workload': random.uniform(0.6, 1.4),  # 工作负荷
            'satisfaction_score': random.uniform(3.0, 5.0)
        }
    
    # 生成离职记录
    for i in range(30):
        turnover_id = str(uuid.uuid4())
        dept = random.choice(departments)
        pos = random.choice(positions)
        
        TURNOVER_DATA[turnover_id] = {
            'id': turnover_id,
            'employee_name': f'离职员工{i+1}',
            'department': dept,
            'position': pos,
            'turnover_date': (datetime.now() - timedelta(days=random.randint(1, 365))).strftime('%Y-%m-%d'),
            'tenure': random.uniform(0.5, 4.0),
            'reason': random.choice(['薪资不足', '技能发展瓶颈', '企业要求过高', '工作压力大', '个人发展', '家庭原因']),
            'exit_interview': generate_exit_interview(),
            'replacement_difficulty': random.choice(['easy', 'medium', 'hard']),
            'cost_impact': random.randint(50000, 200000)  # 离职成本
        }

def calculate_position_risk(market_demand, skill_gap, salary_competitiveness):
    """计算岗位离职风险"""
    # 风险计算公式：市场需求高 + 技能差距大 + 薪资竞争力低 = 高风险
    risk = (market_demand * 0.3 + skill_gap * 0.4 + (1 - salary_competitiveness) * 0.3)
    return min(1.0, max(0.0, risk))

def generate_turnover_reasons(market_demand, skill_gap, salary_competitiveness):
    """生成离职原因分析"""
    reasons = []
    
    if market_demand > 1.1:
        reasons.append('市场需求旺盛，外部机会多')
    if skill_gap > 0.25:
        reasons.append('技能发展瓶颈，缺乏成长空间')
    if salary_competitiveness < 0.8:
        reasons.append('薪资竞争力不足，低于市场水平')
    
    if not reasons:
        reasons.append('工作环境或企业文化因素')
    
    return reasons

def generate_exit_interview():
    """生成离职面谈记录"""
    interview_templates = [
        "员工表示希望获得更好的职业发展机会，认为当前岗位缺乏挑战性。",
        "员工提到薪资待遇与工作强度不匹配，希望获得更公平的报酬。",
        "员工反映工作压力过大，工作生活平衡难以维持。",
        "员工认为公司对技能提升的支持不够，缺乏培训和发展机会。",
        "员工提到团队协作存在问题，沟通效率有待提升。"
    ]
    return random.choice(interview_templates)

def get_turnover_dashboard_data():
    """获取离职预警仪表板数据"""
    # 计算总体统计
    total_employees = sum(dept['total_employees'] for dept in DEPARTMENT_STATS.values())
    total_turnover = sum(dept['turnover_count'] for dept in DEPARTMENT_STATS.values())
    overall_turnover_rate = total_turnover / total_employees if total_employees > 0 else 0
    
    # 高风险部门
    high_risk_departments = [dept for dept, stats in DEPARTMENT_STATS.items() if stats['risk_level'] == 'high']
    
    # 高风险岗位
    high_risk_positions = [pos for pos, analysis in POSITION_ANALYSIS.items() if analysis['turnover_risk'] > 0.6]
    
    # 高风险员工
    high_risk_employees = [emp for emp in EMPLOYEE_RISK_SCORES.values() if emp['risk_level'] == 'high']
    
    return {
        'overall_stats': {
            'total_employees': total_employees,
            'total_turnover': total_turnover,
            'turnover_rate': overall_turnover_rate,
            'high_risk_count': len(high_risk_departments) + len(high_risk_positions)
        },
        'department_analysis': DEPARTMENT_STATS,
        'position_analysis': POSITION_ANALYSIS,
        'high_risk_employees': high_risk_employees[:10],  # 前10名高风险员工
        'recent_turnovers': list(TURNOVER_DATA.values())[:10]  # 最近10次离职
    }

def analyze_turnover_causes():
    """分析离职原因"""
    causes = {
        'salary': {'count': 0, 'percentage': 0, 'departments': {}},
        'skill_development': {'count': 0, 'percentage': 0, 'departments': {}},
        'workload': {'count': 0, 'percentage': 0, 'departments': {}},
        'culture': {'count': 0, 'percentage': 0, 'departments': {}},
        'career_growth': {'count': 0, 'percentage': 0, 'departments': {}}
    }
    
    total_turnovers = len(TURNOVER_DATA)
    
    for turnover in TURNOVER_DATA.values():
        reason = turnover['reason']
        dept = turnover['department']
        
        if '薪资' in reason:
            causes['salary']['count'] += 1
            causes['salary']['departments'][dept] = causes['salary']['departments'].get(dept, 0) + 1
        elif '技能' in reason:
            causes['skill_development']['count'] += 1
            causes['skill_development']['departments'][dept] = causes['skill_development']['departments'].get(dept, 0) + 1
        elif '压力' in reason:
            causes['workload']['count'] += 1
            causes['workload']['departments'][dept] = causes['workload']['departments'].get(dept, 0) + 1
        elif '发展' in reason:
            causes['career_growth']['count'] += 1
            causes['career_growth']['departments'][dept] = causes['career_growth']['departments'].get(dept, 0) + 1
        else:
            causes['culture']['count'] += 1
            causes['culture']['departments'][dept] = causes['culture']['departments'].get(dept, 0) + 1
    
    # 计算百分比
    for cause in causes.values():
        cause['percentage'] = (cause['count'] / total_turnovers * 100) if total_turnovers > 0 else 0
    
    return causes

def generate_prevention_recommendations():
    """生成预防建议"""
    recommendations = []
    
    # 基于部门分析的建议
    for dept, stats in DEPARTMENT_STATS.items():
        if stats['risk_level'] == 'high':
            if stats['turnover_rate'] > 0.2:
                recommendations.append({
                    'department': dept,
                    'priority': 'high',
                    'issue': f'{dept}离职率过高({stats["turnover_rate"]:.1%})',
                    'recommendation': '立即进行员工满意度调研，分析离职原因，制定挽留计划',
                    'action_items': ['员工访谈', '薪资调研', '工作环境改善']
                })
            elif stats['avg_salary'] < 12000:
                recommendations.append({
                    'department': dept,
                    'priority': 'medium',
                    'issue': f'{dept}平均薪资偏低',
                    'recommendation': '进行市场薪资调研，调整薪资结构，提升竞争力',
                    'action_items': ['市场调研', '薪资调整', '福利优化']
                })
    
    # 基于岗位分析的建议
    for pos, analysis in POSITION_ANALYSIS.items():
        if analysis['turnover_risk'] > 0.7:
            recommendations.append({
                'department': '全公司',
                'priority': 'high',
                'issue': f'{pos}岗位离职风险极高',
                'recommendation': '重点关注该岗位员工，提供发展机会和合理薪资',
                'action_items': ['员工关怀', '技能培训', '职业规划']
            })
    
    return recommendations

@turnover_alert_bp.route('/')
def turnover_dashboard():
    """离职预警仪表板"""
    try:
        if 'user_id' not in session:
            return jsonify({'error': '请先登录'}), 401
        
        user = User.query.get(session['user_id'])
        if not user or user.user_type != 'executive':
            return jsonify({'error': '权限不足'}), 403
        
        # 生成模拟数据（实际应用中从数据库获取）
        generate_mock_turnover_data()
        
        # 获取仪表板数据
        dashboard_data = get_turnover_dashboard_data()
        
        # 分析离职原因
        causes_analysis = analyze_turnover_causes()
        
        # 生成预防建议
        prevention_recommendations = generate_prevention_recommendations()
        
        return render_template('talent_management/hr_admin/turnover_dashboard.html',
                             user=user,
                             dashboard_data=dashboard_data,
                             causes_analysis=causes_analysis,
                             prevention_recommendations=prevention_recommendations)
                             
    except Exception as e:
        return jsonify({'error': f'加载页面时发生错误: {str(e)}'}), 500

@turnover_alert_bp.route('/api/department_trends')
def api_department_trends():
    """获取部门离职趋势数据"""
    try:
        # 生成月度趋势数据
        months = []
        trends = {}
        
        for i in range(12):
            month = (datetime.now() - timedelta(days=30*i)).strftime('%Y-%m')
            months.append(month)
            
            for dept in DEPARTMENT_STATS.keys():
                if dept not in trends:
                    trends[dept] = []
                
                # 模拟月度波动
                base_rate = DEPARTMENT_STATS[dept]['turnover_rate']
                monthly_rate = base_rate * random.uniform(0.5, 1.5)
                trends[dept].append(round(monthly_rate * 100, 2))
        
        return jsonify({
            'success': True,
            'months': months,
            'trends': trends
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@turnover_alert_bp.route('/api/risk_analysis')
def api_risk_analysis():
    """获取风险分析数据"""
    try:
        # 岗位风险分布
        position_risks = []
        for pos, analysis in POSITION_ANALYSIS.items():
            position_risks.append({
                'position': pos,
                'risk_score': round(analysis['turnover_risk'] * 100, 1),
                'market_demand': round(analysis['market_demand'], 2),
                'skill_gap': round(analysis['skill_gap'], 2),
                'salary_competitiveness': round(analysis['salary_competitiveness'], 2)
            })
        
        # 员工风险分布
        risk_distribution = {'low': 0, 'medium': 0, 'high': 0}
        for emp in EMPLOYEE_RISK_SCORES.values():
            risk_distribution[emp['risk_level']] += 1
        
        return jsonify({
            'success': True,
            'position_risks': position_risks,
            'risk_distribution': risk_distribution
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@turnover_alert_bp.route('/api/employee_details/<employee_id>')
def api_employee_details(employee_id):
    """获取员工详细信息"""
    try:
        if employee_id in EMPLOYEE_RISK_SCORES:
            employee = EMPLOYEE_RISK_SCORES[employee_id]
            
            # 生成详细的风险分析
            risk_factors = []
            if employee['tenure'] < 2.0:
                risk_factors.append('任职时间短，忠诚度待观察')
            if employee['last_promotion'] > 18:
                risk_factors.append('长期未晋升，发展受限')
            if employee['salary_growth'] < 0.05:
                risk_factors.append('薪资增长缓慢，激励不足')
            if employee['performance_rating'] < 3.5:
                risk_factors.append('绩效评分偏低，工作积极性不高')
            if employee['workload'] > 1.2:
                risk_factors.append('工作负荷过重，压力较大')
            if employee['satisfaction_score'] < 4.0:
                risk_factors.append('工作满意度偏低')
            
            employee['risk_factors'] = risk_factors
            
            return jsonify({
                'success': True,
                'employee': employee
            })
        else:
            return jsonify({'error': '员工不存在'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@turnover_alert_bp.route('/api/generate_report')
def api_generate_report():
    """生成离职预警报告"""
    try:
        # 生成报告数据
        report_data = {
            'report_id': str(uuid.uuid4()),
            'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'summary': {
                'total_employees': sum(dept['total_employees'] for dept in DEPARTMENT_STATS.values()),
                'high_risk_departments': len([d for d in DEPARTMENT_STATS.values() if d['risk_level'] == 'high']),
                'high_risk_positions': len([p for p in POSITION_ANALYSIS.values() if p['turnover_risk'] > 0.6]),
                'high_risk_employees': len([e for e in EMPLOYEE_RISK_SCORES.values() if e['risk_level'] == 'high'])
            },
            'department_analysis': DEPARTMENT_STATS,
            'position_analysis': POSITION_ANALYSIS,
            'causes_analysis': analyze_turnover_causes(),
            'recommendations': generate_prevention_recommendations()
        }
        
        return jsonify({
            'success': True,
            'report': report_data
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 初始化模拟数据
generate_mock_turnover_data()
