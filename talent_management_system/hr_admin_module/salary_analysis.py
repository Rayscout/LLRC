from flask import Blueprint, render_template, request, jsonify, session, send_file
from app.models import User, db
from datetime import datetime, timedelta
import random
import json
# try:
#     import pandas as pd
# except ImportError:
#     pd = None
pd = None
import io
import os

salary_analysis_bp = Blueprint('salary_analysis', __name__, url_prefix='/salary_analysis')

def generate_salary_data():
    """生成薪酬分析模拟数据"""
    positions = {
        '技术岗位': {
            'positions': ['软件工程师', '高级工程师', '技术经理', '架构师', '测试工程师'],
            'company_avg': 18500,
            'industry_avg': 16700,
            'growth_rate': 0.08
        },
        '管理岗位': {
            'positions': ['项目经理', '部门经理', '总监', 'VP', 'CEO'],
            'company_avg': 25000,
            'industry_avg': 25000,
            'growth_rate': 0.05
        },
        '销售岗位': {
            'positions': ['销售代表', '销售经理', '大客户经理', '销售总监'],
            'company_avg': 12000,
            'industry_avg': 12600,
            'growth_rate': 0.06
        },
        '行政岗位': {
            'positions': ['行政专员', '人事专员', '财务专员', '前台'],
            'company_avg': 8000,
            'industry_avg': 7800,
            'growth_rate': 0.03
        },
        '市场岗位': {
            'positions': ['市场专员', '品牌经理', '市场总监', '产品经理'],
            'company_avg': 15000,
            'industry_avg': 14500,
            'growth_rate': 0.07
        }
    }
    
    # 生成12个月的趋势数据
    months = []
    company_trends = {}
    industry_trends = {}
    
    for i in range(12):
        month = (datetime.now() - timedelta(days=30*(11-i))).strftime('%Y-%m')
        months.append(month)
        
        for category, data in positions.items():
            if category not in company_trends:
                company_trends[category] = []
                industry_trends[category] = []
            
            # 添加随机波动
            company_variation = random.uniform(0.95, 1.05)
            industry_variation = random.uniform(0.96, 1.04)
            
            company_trends[category].append(int(data['company_avg'] * company_variation))
            industry_trends[category].append(int(data['industry_avg'] * industry_variation))
    
    # 生成详细岗位数据
    detailed_positions = []
    for category, data in positions.items():
        for position in data['positions']:
            # 为每个岗位生成具体薪酬数据
            base_salary = data['company_avg'] * random.uniform(0.8, 1.2)
            industry_salary = data['industry_avg'] * random.uniform(0.85, 1.15)
            gap_percentage = ((base_salary - industry_salary) / industry_salary) * 100
            
            detailed_positions.append({
                'category': category,
                'position': position,
                'company_salary': int(base_salary),
                'industry_salary': int(industry_salary),
                'gap_percentage': round(gap_percentage, 1),
                'gap_status': '高于行业' if gap_percentage > 0 else '低于行业' if gap_percentage < 0 else '持平',
                'employee_count': random.randint(5, 25),
                'turnover_rate': round(random.uniform(0.05, 0.25), 2)
            })
    
    return {
        'positions': positions,
        'detailed_positions': detailed_positions,
        'months': months,
        'company_trends': company_trends,
        'industry_trends': industry_trends,
        'summary': {
            'total_positions': len(detailed_positions),
            'above_industry': len([p for p in detailed_positions if p['gap_percentage'] > 0]),
            'below_industry': len([p for p in detailed_positions if p['gap_percentage'] < 0]),
            'average_gap': round(sum([p['gap_percentage'] for p in detailed_positions]) / len(detailed_positions), 1)
        }
    }

@salary_analysis_bp.route('/dashboard')
def salary_dashboard():
    """薪酬分析仪表板"""
    if 'user_id' not in session:
        return jsonify({'error': '请先登录'}), 401
    
    user = User.query.get(session['user_id'])
    if not user or user.user_type != 'executive':
        return jsonify({'error': '权限不足'}), 403
    
    salary_data = generate_salary_data()
    
    return render_template(
        'talent_management/hr_admin/salary_dashboard.html',
        user=user,
        salary_data=salary_data
    )

@salary_analysis_bp.route('/api/export_data', methods=['POST'])
def export_salary_data():
    """导出薪酬数据报表"""
    try:
        if 'user_id' not in session:
            return jsonify({'error': '请先登录'}), 401
        
        user = User.query.get(session['user_id'])
        if not user or user.user_type != 'executive':
            return jsonify({'error': '权限不足'}), 403
        
        if pd is None:
            return jsonify({'error': 'pandas库未安装，无法导出Excel文件'}), 500
        
        salary_data = generate_salary_data()
        
        # 创建Excel文件
        output = io.BytesIO()
        
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            # 岗位薪酬对比表
            df_positions = pd.DataFrame(salary_data['detailed_positions'])
            df_positions = df_positions[['category', 'position', 'company_salary', 'industry_salary', 'gap_percentage', 'gap_status', 'employee_count', 'turnover_rate']]
            df_positions.columns = ['岗位类别', '具体岗位', '公司薪酬', '行业平均', '差距百分比', '差距状态', '员工数量', '离职率']
            df_positions.to_excel(writer, sheet_name='岗位薪酬对比', index=False)
            
            # 12个月趋势数据
            trend_data = []
            for i, month in enumerate(salary_data['months']):
                for category in salary_data['company_trends'].keys():
                    trend_data.append({
                        '月份': month,
                        '岗位类别': category,
                        '公司薪酬': salary_data['company_trends'][category][i],
                        '行业平均': salary_data['industry_trends'][category][i],
                        '差距': salary_data['company_trends'][category][i] - salary_data['industry_trends'][category][i]
                    })
            
            df_trends = pd.DataFrame(trend_data)
            df_trends.to_excel(writer, sheet_name='12个月趋势', index=False)
            
            # 汇总统计
            summary_data = [
                ['总岗位数', salary_data['summary']['total_positions']],
                ['高于行业岗位数', salary_data['summary']['above_industry']],
                ['低于行业岗位数', salary_data['summary']['below_industry']],
                ['平均差距百分比', f"{salary_data['summary']['average_gap']}%"]
            ]
            
            df_summary = pd.DataFrame(summary_data, columns=['指标', '数值'])
            df_summary.to_excel(writer, sheet_name='汇总统计', index=False)
        
        output.seek(0)
        
        filename = f"薪酬分析报告_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        return send_file(
            output,
            as_attachment=True,
            download_name=filename,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        
    except Exception as e:
        return jsonify({'error': f'导出数据时发生错误: {str(e)}'}), 500

@salary_analysis_bp.route('/api/salary_data', methods=['GET'])
def get_salary_data():
    """获取薪酬数据API"""
    try:
        if 'user_id' not in session:
            return jsonify({'error': '请先登录'}), 401
        
        user = User.query.get(session['user_id'])
        if not user or user.user_type != 'executive':
            return jsonify({'error': '权限不足'}), 403
        
        salary_data = generate_salary_data()
        return jsonify(salary_data)
        
    except Exception as e:
        return jsonify({'error': f'获取数据时发生错误: {str(e)}'}), 500
