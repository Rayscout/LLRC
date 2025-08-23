from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from app.models import User, db
from datetime import datetime, timedelta
import json
import random

compensation_bp = Blueprint('compensation', __name__, url_prefix='/compensation')

# 模拟薪酬数据
COMPENSATION_DATA = {
    'departments': {
        '技术部': {
            'avg_base_salary': 15000,
            'avg_bonus': 8000,
            'avg_total': 23000,
            'salary_range': (12000, 20000),
            'bonus_range': (5000, 12000)
        },
        '市场部': {
            'avg_base_salary': 12000,
            'avg_bonus': 6000,
            'avg_total': 18000,
            'salary_range': (10000, 16000),
            'bonus_range': (4000, 9000)
        },
        '人事部': {
            'avg_base_salary': 10000,
            'avg_bonus': 4000,
            'avg_total': 14000,
            'salary_range': (8000, 14000),
            'bonus_range': (3000, 6000)
        },
        '财务部': {
            'avg_base_salary': 11000,
            'avg_bonus': 5000,
            'avg_total': 16000,
            'salary_range': (9000, 15000),
            'bonus_range': (3500, 7000)
        }
    },
    'positions': {
        'python开发工程师': {
            'base_salary_range': (13000, 18000),
            'bonus_range': (6000, 10000),
            'market_percentile': 75
        },
        'java开发工程师': {
            'base_salary_range': (14000, 19000),
            'bonus_range': (7000, 11000),
            'market_percentile': 80
        },
        '前端开发工程师': {
            'base_salary_range': (12000, 17000),
            'bonus_range': (5000, 9000),
            'market_percentile': 70
        },
        '产品经理': {
            'base_salary_range': (15000, 22000),
            'bonus_range': (8000, 15000),
            'market_percentile': 85
        }
    }
}

@compensation_bp.route('/')
def compensation_dashboard():
    """薪酬管理仪表板"""
    try:
        if 'user_id' not in session:
            flash('请先登录', 'warning')
            return redirect(url_for('common.auth.sign'))
        
        user = User.query.get(session['user_id'])
        if not user or user.user_type != 'employee':
            flash('用户信息获取失败', 'warning')
            return redirect(url_for('common.auth.sign'))
        
        # 获取用户薪酬信息
        user_compensation = get_user_compensation(user)
        
        # 获取部门对比数据
        department_comparison = get_department_comparison(user)
        
        # 获取公司百分位数据
        company_percentile = get_company_percentile(user)
        
        # 获取薪酬趋势数据
        salary_trends = get_salary_trends(user)
        
        # 获取薪酬结构分析
        compensation_structure = analyze_compensation_structure(user)
        
        return render_template('talent_management/employee_management/compensation_dashboard.html',
                             user=user,
                             user_compensation=user_compensation,
                             department_comparison=department_comparison,
                             company_percentile=company_percentile,
                             salary_trends=salary_trends,
                             compensation_structure=compensation_structure)
                             
    except Exception as e:
        flash(f'加载薪酬页面时发生错误: {str(e)}', 'danger')
        return redirect(url_for('talent_management.employee_auth.employee_dashboard'))

@compensation_bp.route('/api/salary_trends')
def api_salary_trends():
    """获取薪酬趋势数据API"""
    try:
        if 'user_id' not in session:
            return jsonify({'success': False, 'message': '请先登录'})
        
        user = User.query.get(session['user_id'])
        if not user:
            return jsonify({'success': False, 'message': '用户信息获取失败'})
        
        trends = get_salary_trends(user)
        return jsonify({'success': True, 'data': trends})
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'获取数据失败: {str(e)}'})

@compensation_bp.route('/api/compensation_analysis')
def api_compensation_analysis():
    """获取薪酬分析数据API"""
    try:
        if 'user_id' not in session:
            return jsonify({'success': False, 'message': '请先登录'})
        
        user = User.query.get(session['user_id'])
        if not user:
            return jsonify({'success': False, 'message': '用户信息获取失败'})
        
        analysis = {
            'department_comparison': get_department_comparison(user),
            'company_percentile': get_company_percentile(user),
            'compensation_structure': analyze_compensation_structure(user)
        }
        
        return jsonify({'success': True, 'data': analysis})
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'获取数据失败: {str(e)}'})

def get_user_compensation(user):
    """获取用户薪酬信息"""
    # 模拟用户薪酬数据
    base_salary = random.randint(13000, 18000)
    bonus = random.randint(6000, 10000)
    total = base_salary + bonus
    
    return {
        'base_salary': base_salary,
        'bonus': bonus,
        'total': total,
        'currency': 'CNY',
        'last_updated': datetime.now().strftime('%Y-%m-%d'),
        'next_review': (datetime.now() + timedelta(days=90)).strftime('%Y-%m-%d'),
        'performance_rating': random.choice(['优秀', '良好', '合格']),
        'bonus_multiplier': random.uniform(0.8, 1.2)
    }

def get_department_comparison(user):
    """获取部门对比数据"""
    department = getattr(user, 'department', '技术部')
    dept_data = COMPENSATION_DATA['departments'].get(department, COMPENSATION_DATA['departments']['技术部'])
    
    user_comp = get_user_compensation(user)
    
    return {
        'department': department,
        'department_avg': {
            'base_salary': dept_data['avg_base_salary'],
            'bonus': dept_data['avg_bonus'],
            'total': dept_data['avg_total']
        },
        'user_data': {
            'base_salary': user_comp['base_salary'],
            'bonus': user_comp['bonus'],
            'total': user_comp['total']
        },
        'comparison': {
            'base_salary_diff': user_comp['base_salary'] - dept_data['avg_base_salary'],
            'bonus_diff': user_comp['bonus'] - dept_data['avg_bonus'],
            'total_diff': user_comp['total'] - dept_data['avg_total'],
            'base_salary_percentile': calculate_percentile(user_comp['base_salary'], dept_data['salary_range']),
            'bonus_percentile': calculate_percentile(user_comp['bonus'], dept_data['bonus_range'])
        }
    }

def get_company_percentile(user):
    """获取公司百分位数据"""
    # 模拟公司薪酬分布数据
    company_salary_data = generate_company_salary_distribution()
    
    user_comp = get_user_compensation(user)
    total_comp = user_comp['total']
    
    # 计算百分位
    percentile = calculate_company_percentile(total_comp, company_salary_data)
    
    return {
        'total_compensation': total_comp,
        'percentile': percentile,
        'percentile_label': get_percentile_label(percentile),
        'company_avg': sum(company_salary_data) / len(company_salary_data),
        'company_median': sorted(company_salary_data)[len(company_salary_data) // 2],
        'company_min': min(company_salary_data),
        'company_max': max(company_salary_data)
    }

def get_salary_trends(user):
    """获取薪酬趋势数据"""
    # 生成过去12个月的薪酬趋势
    trends = []
    base_salary = get_user_compensation(user)['base_salary']
    
    for i in range(12):
        month = datetime.now() - timedelta(days=30 * i)
        # 模拟薪酬变化（小幅波动）
        variation = random.uniform(0.95, 1.05)
        month_salary = int(base_salary * variation)
        
        trends.append({
            'month': month.strftime('%Y-%m'),
            'base_salary': month_salary,
            'bonus': int(get_user_compensation(user)['bonus'] * random.uniform(0.8, 1.2)),
            'total': month_salary + int(get_user_compensation(user)['bonus'] * random.uniform(0.8, 1.2))
        })
    
    return list(reversed(trends))

def analyze_compensation_structure(user):
    """分析薪酬结构"""
    user_comp = get_user_compensation(user)
    
    return {
        'base_salary_ratio': round(user_comp['base_salary'] / user_comp['total'] * 100, 1),
        'bonus_ratio': round(user_comp['bonus'] / user_comp['total'] * 100, 1),
        'market_positioning': get_market_positioning(user),
        'growth_potential': analyze_growth_potential(user),
        'recommendations': generate_compensation_recommendations(user)
    }

def calculate_percentile(value, range_tuple):
    """计算在给定范围内的百分位"""
    min_val, max_val = range_tuple
    if max_val == min_val:
        return 50
    
    percentile = ((value - min_val) / (max_val - min_val)) * 100
    return max(0, min(100, percentile))

def calculate_company_percentile(value, data_list):
    """计算在公司数据中的百分位"""
    if not data_list:
        return 50
    
    sorted_data = sorted(data_list)
    position = 0
    
    for i, data_point in enumerate(sorted_data):
        if value <= data_point:
            position = i
            break
        position = i + 1
    
    percentile = (position / len(sorted_data)) * 100
    return round(percentile, 1)

def get_percentile_label(percentile):
    """获取百分位标签"""
    if percentile >= 90:
        return '顶级 (Top 10%)'
    elif percentile >= 80:
        return '优秀 (Top 20%)'
    elif percentile >= 70:
        return '良好 (Top 30%)'
    elif percentile >= 50:
        return '中等 (Top 50%)'
    elif percentile >= 30:
        return '偏低 (Bottom 30%)'
    else:
        return '较低 (Bottom 20%)'

def generate_company_salary_distribution():
    """生成公司薪酬分布数据"""
    # 模拟真实的薪酬分布（正态分布）
    distribution = []
    
    # 基础薪酬范围
    base_range = (8000, 25000)
    
    # 生成1000个样本点
    for _ in range(1000):
        # 使用正态分布生成更真实的薪酬分布
        import math
        mean = (base_range[0] + base_range[1]) / 2
        std_dev = (base_range[1] - base_range[0]) / 6
        
        # Box-Muller变换生成正态分布
        u1 = random.random()
        u2 = random.random()
        z0 = math.sqrt(-2 * math.log(u1)) * math.cos(2 * math.pi * u2)
        
        salary = mean + z0 * std_dev
        salary = max(base_range[0], min(base_range[1], salary))
        
        # 添加奖金
        bonus = salary * random.uniform(0.3, 0.6)
        total = salary + bonus
        
        distribution.append(int(total))
    
    return distribution

def get_market_positioning(user):
    """获取市场定位分析"""
    position = getattr(user, 'position', '开发工程师')
    market_data = COMPENSATION_DATA['positions'].get(position, {})
    
    return {
        'position': position,
        'market_percentile': market_data.get('market_percentile', 70),
        'market_avg': market_data.get('base_salary_range', (12000, 18000)),
        'competitiveness': '高' if market_data.get('market_percentile', 70) >= 75 else '中等',
        'recommendation': '保持竞争力' if market_data.get('market_percentile', 70) >= 75 else '考虑提升'
    }

def analyze_growth_potential(user):
    """分析薪酬增长潜力"""
    user_comp = get_user_compensation(user)
    department = getattr(user, 'department', '技术部')
    dept_data = COMPENSATION_DATA['departments'].get(department, COMPENSATION_DATA['departments']['技术部'])
    
    # 计算增长空间
    max_potential = dept_data['salary_range'][1] + dept_data['bonus_range'][1]
    current_total = user_comp['total']
    growth_space = max_potential - current_total
    
    return {
        'current_level': '初级' if current_total < dept_data['avg_total'] * 0.8 else '中级' if current_total < dept_data['avg_total'] * 1.2 else '高级',
        'growth_space': growth_space,
        'growth_percentage': round(growth_space / current_total * 100, 1),
        'next_level_target': dept_data['avg_total'] * 1.2,
        'time_to_next_level': '6-12个月' if growth_space < 5000 else '12-24个月'
    }

def generate_compensation_recommendations(user):
    """生成薪酬建议"""
    recommendations = []
    
    # 基于百分位的建议
    company_percentile = get_company_percentile(user)
    if company_percentile['percentile'] < 50:
        recommendations.append({
            'type': '提升建议',
            'title': '薪酬水平偏低',
            'description': '您的薪酬水平低于公司平均水平，建议与主管讨论薪酬调整',
            'priority': 'high'
        })
    
    # 基于部门对比的建议
    dept_comparison = get_department_comparison(user)
    if dept_comparison['comparison']['total_diff'] < -2000:
        recommendations.append({
            'type': '部门对比',
            'title': '部门薪酬差距',
            'description': '您的薪酬低于部门平均水平，建议关注技能提升和绩效表现',
            'priority': 'medium'
        })
    
    # 基于增长潜力的建议
    growth_potential = analyze_growth_potential(user)
    if growth_potential['growth_percentage'] > 30:
        recommendations.append({
            'type': '发展机会',
            'title': '薪酬增长空间大',
            'description': '您有较大的薪酬增长空间，建议制定明确的职业发展计划',
            'priority': 'low'
        })
    
    return recommendations
