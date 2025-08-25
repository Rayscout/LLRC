from flask import Blueprint, render_template, request, jsonify, session, send_file
from app.models import User, db
from datetime import datetime, timedelta
import random
import json
import pandas as pd
import io
import os

org_health_bp = Blueprint('org_health', __name__, url_prefix='/org_health')

def generate_org_health_data():
    """生成组织健康度评估模拟数据"""
    departments = {
        '技术部': {
            'employee_count': 45,
            'turnover_rate': 0.12,
            'reserve_rate': 0.85,
            'stability_rate': 0.78,
            'satisfaction': 0.82,
            'growth_rate': 0.15
        },
        '市场部': {
            'employee_count': 28,
            'turnover_rate': 0.08,
            'reserve_rate': 0.92,
            'stability_rate': 0.88,
            'satisfaction': 0.85,
            'growth_rate': 0.12
        },
        '销售部': {
            'employee_count': 35,
            'turnover_rate': 0.15,
            'reserve_rate': 0.75,
            'stability_rate': 0.72,
            'satisfaction': 0.78,
            'growth_rate': 0.18
        },
        '人事部': {
            'employee_count': 12,
            'turnover_rate': 0.05,
            'reserve_rate': 0.95,
            'stability_rate': 0.92,
            'satisfaction': 0.88,
            'growth_rate': 0.08
        },
        '财务部': {
            'employee_count': 18,
            'turnover_rate': 0.03,
            'reserve_rate': 0.98,
            'stability_rate': 0.95,
            'satisfaction': 0.92,
            'growth_rate': 0.05
        },
        '行政部': {
            'employee_count': 18,
            'turnover_rate': 0.06,
            'reserve_rate': 0.88,
            'stability_rate': 0.85,
            'satisfaction': 0.85,
            'growth_rate': 0.10
        }
    }
    
    # 生成12个月的历史数据
    months = []
    historical_data = {}
    
    for i in range(12):
        month = (datetime.now() - timedelta(days=30*(11-i))).strftime('%Y-%m')
        months.append(month)
        
        for dept, data in departments.items():
            if dept not in historical_data:
                historical_data[dept] = {
                    'turnover_rate': [],
                    'reserve_rate': [],
                    'stability_rate': [],
                    'satisfaction': [],
                    'growth_rate': []
                }
            
            # 添加随机波动
            variation = random.uniform(0.95, 1.05)
            historical_data[dept]['turnover_rate'].append(round(data['turnover_rate'] * variation, 3))
            historical_data[dept]['reserve_rate'].append(round(data['reserve_rate'] * variation, 3))
            historical_data[dept]['stability_rate'].append(round(data['stability_rate'] * variation, 3))
            historical_data[dept]['satisfaction'].append(round(data['satisfaction'] * variation, 3))
            historical_data[dept]['growth_rate'].append(round(data['growth_rate'] * variation, 3))
    
    # 计算综合评分
    for dept, data in departments.items():
        # 综合评分 = (储备率 * 0.3 + 稳定性 * 0.3 + 满意度 * 0.2 + 增长率 * 0.2) * 100
        # 流失率作为负向指标，超过阈值会扣分
        base_score = (data['reserve_rate'] * 0.3 + 
                     data['stability_rate'] * 0.3 + 
                     data['satisfaction'] * 0.2 + 
                     data['growth_rate'] * 0.2) * 100
        
        # 流失率扣分：超过3%开始扣分
        if data['turnover_rate'] > 0.03:
            penalty = (data['turnover_rate'] - 0.03) * 200  # 每超过1%扣2分
            base_score -= penalty
        
        data['comprehensive_score'] = max(0, round(base_score, 1))
        
        # 风险等级评估
        if data['comprehensive_score'] >= 85:
            data['risk_level'] = '低风险'
            data['risk_color'] = 'success'
        elif data['comprehensive_score'] >= 70:
            data['risk_level'] = '中等风险'
            data['risk_color'] = 'warning'
        else:
            data['risk_level'] = '高风险'
            data['risk_color'] = 'danger'
    
    # 生成改进建议
    improvement_suggestions = {
        '技术部': [
            '加强员工职业发展规划，提供更多晋升机会',
            '优化工作环境，减少工作压力',
            '提高薪酬竞争力，特别是关键岗位',
            '加强团队建设活动，提升员工归属感'
        ],
        '市场部': [
            '保持现有良好状态，继续优化工作流程',
            '加强技能培训，提升员工专业能力',
            '建立激励机制，鼓励创新思维'
        ],
        '销售部': [
            '优化销售激励机制，提高员工积极性',
            '加强销售技能培训，提升业绩表现',
            '改善工作环境，减少高压工作状态',
            '建立职业发展通道，提供晋升机会'
        ],
        '人事部': [
            '继续保持优秀表现，作为其他部门学习榜样',
            '分享最佳实践，帮助其他部门提升',
            '持续优化人事政策，提升员工体验'
        ],
        '财务部': [
            '继续保持优秀表现，维持高稳定性',
            '加强财务知识培训，提升专业能力',
            '优化财务流程，提高工作效率'
        ],
        '行政部': [
            '继续保持良好状态，优化服务流程',
            '加强服务意识培训，提升服务质量',
            '建立服务标准，提升员工满意度'
        ]
    }
    
    return {
        'departments': departments,
        'months': months,
        'historical_data': historical_data,
        'improvement_suggestions': improvement_suggestions,
        'summary': {
            'total_employees': sum([dept['employee_count'] for dept in departments.values()]),
            'avg_comprehensive_score': round(sum([dept['comprehensive_score'] for dept in departments.values()]) / len(departments), 1),
            'high_risk_depts': len([dept for dept in departments.values() if dept['risk_level'] == '高风险']),
            'medium_risk_depts': len([dept for dept in departments.values() if dept['risk_level'] == '中等风险']),
            'low_risk_depts': len([dept for dept in departments.values() if dept['risk_level'] == '低风险'])
        }
    }

@org_health_bp.route('/dashboard')
def org_health_dashboard():
    """组织健康度评估仪表板"""
    if 'user_id' not in session:
        return jsonify({'error': '请先登录'}), 401
    
    user = User.query.get(session['user_id'])
    if not user or user.user_type != 'executive':
        return jsonify({'error': '权限不足'}), 403
    
    # 获取筛选参数
    department_filter = request.args.get('department', '')
    time_filter = request.args.get('time', '12')  # 默认12个月
    
    org_health_data = generate_org_health_data()
    
    # 应用筛选
    if department_filter:
        filtered_departments = {k: v for k, v in org_health_data['departments'].items() 
                              if department_filter.lower() in k.lower()}
        org_health_data['departments'] = filtered_departments
    
    # 时间筛选
    if time_filter != '12':
        months_to_show = int(time_filter)
        org_health_data['months'] = org_health_data['months'][-months_to_show:]
        for dept in org_health_data['historical_data']:
            for metric in org_health_data['historical_data'][dept]:
                org_health_data['historical_data'][dept][metric] = \
                    org_health_data['historical_data'][dept][metric][-months_to_show:]
    
    return render_template(
        'talent_management/hr_admin/org_health_dashboard.html',
        user=user,
        org_health_data=org_health_data,
        department_filter=department_filter,
        time_filter=time_filter
    )

@org_health_bp.route('/api/export_report', methods=['POST'])
def export_org_health_report():
    """导出组织健康度对比报告"""
    try:
        if 'user_id' not in session:
            return jsonify({'error': '请先登录'}), 401
        
        user = User.query.get(session['user_id'])
        if not user or user.user_type != 'executive':
            return jsonify({'error': '权限不足'}), 403
        
        if pd is None:
            return jsonify({'error': 'pandas库未安装，无法导出Excel文件'}), 500
        
        org_health_data = generate_org_health_data()
        
        # 创建Excel文件
        output = io.BytesIO()
        
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            # 部门健康度对比表
            dept_data = []
            for dept_name, dept_info in org_health_data['departments'].items():
                dept_data.append({
                    '部门': dept_name,
                    '员工数量': dept_info['employee_count'],
                    '流失率': f"{dept_info['turnover_rate']*100:.1f}%",
                    '储备率': f"{dept_info['reserve_rate']*100:.1f}%",
                    '稳定性': f"{dept_info['stability_rate']*100:.1f}%",
                    '满意度': f"{dept_info['satisfaction']*100:.1f}%",
                    '增长率': f"{dept_info['growth_rate']*100:.1f}%",
                    '综合评分': dept_info['comprehensive_score'],
                    '风险等级': dept_info['risk_level']
                })
            
            df_dept = pd.DataFrame(dept_data)
            df_dept.to_excel(writer, sheet_name='部门健康度对比', index=False)
            
            # 12个月趋势数据
            trend_data = []
            for i, month in enumerate(org_health_data['months']):
                for dept in org_health_data['historical_data'].keys():
                    trend_data.append({
                        '月份': month,
                        '部门': dept,
                        '流失率': org_health_data['historical_data'][dept]['turnover_rate'][i],
                        '储备率': org_health_data['historical_data'][dept]['reserve_rate'][i],
                        '稳定性': org_health_data['historical_data'][dept]['stability_rate'][i],
                        '满意度': org_health_data['historical_data'][dept]['satisfaction'][i],
                        '增长率': org_health_data['historical_data'][dept]['growth_rate'][i]
                    })
            
            df_trends = pd.DataFrame(trend_data)
            df_trends.to_excel(writer, sheet_name='12个月趋势', index=False)
            
            # 改进建议
            suggestion_data = []
            for dept, suggestions in org_health_data['improvement_suggestions'].items():
                for i, suggestion in enumerate(suggestions, 1):
                    suggestion_data.append({
                        '部门': dept,
                        '建议序号': i,
                        '改进建议': suggestion
                    })
            
            df_suggestions = pd.DataFrame(suggestion_data)
            df_suggestions.to_excel(writer, sheet_name='改进建议', index=False)
            
            # 汇总统计
            summary_data = [
                ['总员工数', org_health_data['summary']['total_employees']],
                ['平均综合评分', f"{org_health_data['summary']['avg_comprehensive_score']}分"],
                ['高风险部门数', org_health_data['summary']['high_risk_depts']],
                ['中等风险部门数', org_health_data['summary']['medium_risk_depts']],
                ['低风险部门数', org_health_data['summary']['low_risk_depts']]
            ]
            
            df_summary = pd.DataFrame(summary_data, columns=['指标', '数值'])
            df_summary.to_excel(writer, sheet_name='汇总统计', index=False)
        
        output.seek(0)
        
        filename = f"组织健康度评估报告_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        return send_file(
            output,
            as_attachment=True,
            download_name=filename,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        
    except Exception as e:
        return jsonify({'error': f'导出报告时发生错误: {str(e)}'}), 500

@org_health_bp.route('/api/org_health_data', methods=['GET'])
def get_org_health_data():
    """获取组织健康度数据API"""
    try:
        if 'user_id' not in session:
            return jsonify({'error': '请先登录'}), 401
        
        user = User.query.get(session['user_id'])
        if not user or user.user_type != 'executive':
            return jsonify({'error': '权限不足'}), 403
        
        org_health_data = generate_org_health_data()
        return jsonify(org_health_data)
        
    except Exception as e:
        return jsonify({'error': f'获取数据时发生错误: {str(e)}'}), 500
