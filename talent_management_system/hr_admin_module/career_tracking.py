from flask import Blueprint, render_template, request, jsonify, session, send_file
from app.models import User, db
from datetime import datetime, timedelta
import random
import json
import pandas as pd
import io
import os

career_tracking_bp = Blueprint('career_tracking', __name__, url_prefix='/career_tracking')

def generate_career_tracking_data():
    """生成职业发展追踪模拟数据"""
    # 模拟团队成员数据
    team_members = {
        '张工程师': {
            'position': '高级软件工程师',
            'department': '技术部',
            'join_date': '2022-03-15',
            'current_level': 'P5',
            'target_level': 'P6',
            'skills': {
                'Python': {'current': 85, 'target': 90, 'growth_rate': 0.12},
                'React': {'current': 78, 'target': 85, 'growth_rate': 0.15},
                'Docker': {'current': 72, 'target': 80, 'growth_rate': 0.18},
                '系统设计': {'current': 68, 'target': 75, 'growth_rate': 0.10}
            },
            'training_progress': {
                '技术领导力培训': {'status': 'completed', 'score': 88, 'completion_date': '2024-01-15'},
                '高级架构设计': {'status': 'in_progress', 'score': 0, 'completion_date': None},
                '团队管理技能': {'status': 'not_started', 'score': 0, 'completion_date': None}
            },
            'performance_score': 82,
            'career_goals': ['技术专家', '团队领导', '架构师'],
            'last_review_date': '2024-01-20'
        },
        '李产品经理': {
            'position': '产品经理',
            'department': '产品部',
            'join_date': '2021-08-10',
            'current_level': 'P4',
            'target_level': 'P5',
            'skills': {
                '产品规划': {'current': 88, 'target': 92, 'growth_rate': 0.08},
                '用户研究': {'current': 82, 'target': 88, 'growth_rate': 0.12},
                '数据分析': {'current': 75, 'target': 82, 'growth_rate': 0.15},
                '项目管理': {'current': 80, 'target': 85, 'growth_rate': 0.10}
            },
            'training_progress': {
                '高级产品管理': {'status': 'completed', 'score': 92, 'completion_date': '2024-02-01'},
                '数据分析进阶': {'status': 'in_progress', 'score': 0, 'completion_date': None},
                '领导力发展': {'status': 'not_started', 'score': 0, 'completion_date': None}
            },
            'performance_score': 85,
            'career_goals': ['高级产品经理', '产品总监', '创业'],
            'last_review_date': '2024-02-15'
        },
        '王设计师': {
            'position': 'UI/UX设计师',
            'department': '设计部',
            'join_date': '2023-01-20',
            'current_level': 'P3',
            'target_level': 'P4',
            'skills': {
                'Figma': {'current': 90, 'target': 95, 'growth_rate': 0.05},
                '用户研究': {'current': 70, 'target': 80, 'growth_rate': 0.20},
                '交互设计': {'current': 75, 'target': 85, 'growth_rate': 0.15},
                '设计系统': {'current': 65, 'target': 75, 'growth_rate': 0.18}
            },
            'training_progress': {
                '高级设计技能': {'status': 'completed', 'score': 85, 'completion_date': '2024-01-30'},
                '用户研究方法论': {'status': 'in_progress', 'score': 0, 'completion_date': None},
                '设计思维': {'status': 'not_started', 'score': 0, 'completion_date': None}
            },
            'performance_score': 78,
            'career_goals': ['高级设计师', '设计主管', '设计专家'],
            'last_review_date': '2024-01-25'
        },
        '陈运营': {
            'position': '运营专员',
            'department': '运营部',
            'join_date': '2023-06-01',
            'current_level': 'P2',
            'target_level': 'P3',
            'skills': {
                '数据分析': {'current': 65, 'target': 75, 'growth_rate': 0.25},
                '内容运营': {'current': 80, 'target': 85, 'growth_rate': 0.10},
                '用户增长': {'current': 70, 'target': 80, 'growth_rate': 0.20},
                '活动策划': {'current': 75, 'target': 82, 'growth_rate': 0.15}
            },
            'training_progress': {
                '运营基础技能': {'status': 'completed', 'score': 78, 'completion_date': '2024-01-10'},
                '数据分析入门': {'status': 'in_progress', 'score': 0, 'completion_date': None},
                '用户增长策略': {'status': 'not_started', 'score': 0, 'completion_date': None}
            },
            'performance_score': 72,
            'career_goals': ['运营经理', '增长专家', '产品运营'],
            'last_review_date': '2024-01-15'
        },
        '刘销售': {
            'position': '销售代表',
            'department': '销售部',
            'join_date': '2022-11-01',
            'current_level': 'P3',
            'target_level': 'P4',
            'skills': {
                '客户关系管理': {'current': 85, 'target': 90, 'growth_rate': 0.08},
                '谈判技巧': {'current': 78, 'target': 85, 'growth_rate': 0.12},
                '产品知识': {'current': 80, 'target': 88, 'growth_rate': 0.10},
                '销售策略': {'current': 75, 'target': 82, 'growth_rate': 0.15}
            },
            'training_progress': {
                '销售技巧进阶': {'status': 'completed', 'score': 82, 'completion_date': '2024-02-10'},
                '高级谈判技巧': {'status': 'in_progress', 'score': 0, 'completion_date': None},
                '客户成功管理': {'status': 'not_started', 'score': 0, 'completion_date': None}
            },
            'performance_score': 80,
            'career_goals': ['销售经理', '大客户经理', '销售总监'],
            'last_review_date': '2024-02-20'
        }
    }
    
    # 生成12个月的技能成长数据
    months = []
    skill_growth_data = {}
    
    for i in range(12):
        month = (datetime.now() - timedelta(days=30*(11-i))).strftime('%Y-%m')
        months.append(month)
        
        for member_name, member_data in team_members.items():
            if member_name not in skill_growth_data:
                skill_growth_data[member_name] = {}
            
            for skill_name, skill_data in member_data['skills'].items():
                if skill_name not in skill_growth_data[member_name]:
                    skill_growth_data[member_name][skill_name] = []
                
                # 计算历史技能水平
                if i == 0:
                    # 第一个月使用当前水平
                    current_level = skill_data['current']
                else:
                    # 后续月份基于增长率计算
                    growth_months = 11 - i
                    current_level = max(0, skill_data['current'] - (skill_data['growth_rate'] * 100 * growth_months))
                
                # 添加随机波动
                variation = random.uniform(0.95, 1.05)
                skill_growth_data[member_name][skill_name].append(max(0, min(100, round(current_level * variation))))
    
    # 计算发展进度和生成建议
    for member_name, member_data in team_members.items():
        # 计算整体技能发展进度
        total_skills = len(member_data['skills'])
        completed_skills = 0
        total_progress = 0
        
        for skill_name, skill_data in member_data['skills'].items():
            progress = (skill_data['current'] / skill_data['target']) * 100
            total_progress += progress
            if progress >= 100:
                completed_skills += 1
        
        member_data['overall_progress'] = round(total_progress / total_skills, 1)
        member_data['completed_skills'] = completed_skills
        
        # 计算培训完成率
        total_trainings = len(member_data['training_progress'])
        completed_trainings = len([t for t in member_data['training_progress'].values() if t['status'] == 'completed'])
        member_data['training_completion_rate'] = round((completed_trainings / total_trainings) * 100, 1)
        
        # 生成发展建议
        member_data['development_suggestions'] = generate_development_suggestions(member_data)
        
        # 判断是否滞后
        member_data['is_lagging'] = member_data['overall_progress'] < 70 or member_data['training_completion_rate'] < 50
        
        # 计算风险等级
        if member_data['overall_progress'] >= 80 and member_data['training_completion_rate'] >= 80:
            member_data['risk_level'] = '低风险'
            member_data['risk_color'] = 'success'
        elif member_data['overall_progress'] >= 60 and member_data['training_completion_rate'] >= 60:
            member_data['risk_level'] = '中等风险'
            member_data['risk_color'] = 'warning'
        else:
            member_data['risk_level'] = '高风险'
            member_data['risk_color'] = 'danger'
    
    return {
        'team_members': team_members,
        'months': months,
        'skill_growth_data': skill_growth_data,
        'summary': {
            'total_members': len(team_members),
            'avg_progress': round(sum([m['overall_progress'] for m in team_members.values()]) / len(team_members), 1),
            'lagging_members': len([m for m in team_members.values() if m['is_lagging']]),
            'high_risk_members': len([m for m in team_members.values() if m['risk_level'] == '高风险'])
        }
    }

def generate_development_suggestions(member_data):
    """生成个性化发展建议"""
    suggestions = []
    
    # 基于技能差距的建议
    for skill_name, skill_data in member_data['skills'].items():
        if skill_data['current'] < skill_data['target']:
            gap = skill_data['target'] - skill_data['current']
            if gap > 15:
                suggestions.append(f"重点关注{skill_name}技能提升，当前差距较大({gap}分)")
            elif gap > 8:
                suggestions.append(f"继续提升{skill_name}技能，距离目标还有{gap}分")
            else:
                suggestions.append(f"即将达成{skill_name}技能目标，继续保持")
    
    # 基于培训进度的建议
    if member_data['training_completion_rate'] < 50:
        suggestions.append("培训完成率较低，建议制定详细的学习计划")
    elif member_data['training_completion_rate'] < 80:
        suggestions.append("培训进度良好，建议加快未完成培训的学习")
    else:
        suggestions.append("培训完成情况优秀，可以考虑更高阶的培训课程")
    
    # 基于绩效的建议
    if member_data['performance_score'] < 75:
        suggestions.append("绩效表现需要提升，建议与直接上级进行一对一沟通")
    elif member_data['performance_score'] < 85:
        suggestions.append("绩效表现良好，建议设定更具挑战性的目标")
    else:
        suggestions.append("绩效表现优秀，建议分享最佳实践给团队成员")
    
    # 基于职业目标的建议
    if member_data['current_level'] == member_data['target_level']:
        suggestions.append("已达到目标职级，建议设定新的职业发展目标")
    else:
        level_gap = ord(member_data['target_level'][1]) - ord(member_data['current_level'][1])
        if level_gap > 1:
            suggestions.append(f"目标职级差距较大({level_gap}级)，建议分阶段设定目标")
        else:
            suggestions.append("距离目标职级较近，建议重点提升关键技能")
    
    return suggestions[:5]  # 返回前5条建议

@career_tracking_bp.route('/dashboard')
def career_tracking_dashboard():
    """职业发展追踪仪表板"""
    if 'user_id' not in session:
        return jsonify({'error': '请先登录'}), 401
    
    user = User.query.get(session['user_id'])
    if not user or user.user_type != 'executive':
        return jsonify({'error': '权限不足'}), 403
    
    # 获取筛选参数
    department_filter = request.args.get('department', '')
    progress_filter = request.args.get('progress', 'all')  # all, lagging, on_track
    
    career_data = generate_career_tracking_data()
    
    # 应用筛选
    if department_filter:
        filtered_members = {k: v for k, v in career_data['team_members'].items() 
                          if department_filter.lower() in v['department'].lower()}
        career_data['team_members'] = filtered_members
    
    if progress_filter == 'lagging':
        filtered_members = {k: v for k, v in career_data['team_members'].items() 
                          if v['is_lagging']}
        career_data['team_members'] = filtered_members
    elif progress_filter == 'on_track':
        filtered_members = {k: v for k, v in career_data['team_members'].items() 
                          if not v['is_lagging']}
        career_data['team_members'] = filtered_members
    
    return render_template(
        'talent_management/hr_admin/career_tracking_dashboard.html',
        user=user,
        career_data=career_data,
        department_filter=department_filter,
        progress_filter=progress_filter
    )

@career_tracking_bp.route('/api/export_report', methods=['POST'])
def export_career_report():
    """导出职业发展追踪报告"""
    try:
        if 'user_id' not in session:
            return jsonify({'error': '请先登录'}), 401
        
        user = User.query.get(session['user_id'])
        if not user or user.user_type != 'executive':
            return jsonify({'error': '权限不足'}), 403
        
        if pd is None:
            return jsonify({'error': 'pandas库未安装，无法导出Excel文件'}), 500
        
        career_data = generate_career_tracking_data()
        
        # 创建Excel文件
        output = io.BytesIO()
        
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            # 团队成员发展概览
            member_overview = []
            for member_name, member_data in career_data['team_members'].items():
                member_overview.append({
                    '姓名': member_name,
                    '职位': member_data['position'],
                    '部门': member_data['department'],
                    '当前职级': member_data['current_level'],
                    '目标职级': member_data['target_level'],
                    '整体进度': f"{member_data['overall_progress']}%",
                    '培训完成率': f"{member_data['training_completion_rate']}%",
                    '绩效评分': member_data['performance_score'],
                    '风险等级': member_data['risk_level'],
                    '是否滞后': '是' if member_data['is_lagging'] else '否'
                })
            
            df_overview = pd.DataFrame(member_overview)
            df_overview.to_excel(writer, sheet_name='团队成员发展概览', index=False)
            
            # 技能发展详情
            skill_details = []
            for member_name, member_data in career_data['team_members'].items():
                for skill_name, skill_data in member_data['skills'].items():
                    skill_details.append({
                        '姓名': member_name,
                        '技能名称': skill_name,
                        '当前水平': skill_data['current'],
                        '目标水平': skill_data['target'],
                        '差距': skill_data['target'] - skill_data['current'],
                        '增长率': f"{skill_data['growth_rate']*100:.1f}%"
                    })
            
            df_skills = pd.DataFrame(skill_details)
            df_skills.to_excel(writer, sheet_name='技能发展详情', index=False)
            
            # 培训完成情况
            training_details = []
            for member_name, member_data in career_data['team_members'].items():
                for training_name, training_data in member_data['training_progress'].items():
                    training_details.append({
                        '姓名': member_name,
                        '培训课程': training_name,
                        '状态': training_data['status'],
                        '得分': training_data['score'],
                        '完成日期': training_data['completion_date'] or '未完成'
                    })
            
            df_training = pd.DataFrame(training_details)
            df_training.to_excel(writer, sheet_name='培训完成情况', index=False)
            
            # 发展建议
            suggestion_details = []
            for member_name, member_data in career_data['team_members'].items():
                for i, suggestion in enumerate(member_data['development_suggestions'], 1):
                    suggestion_details.append({
                        '姓名': member_name,
                        '建议序号': i,
                        '发展建议': suggestion
                    })
            
            df_suggestions = pd.DataFrame(suggestion_details)
            df_suggestions.to_excel(writer, sheet_name='发展建议', index=False)
            
            # 汇总统计
            summary_data = [
                ['总团队成员数', career_data['summary']['total_members']],
                ['平均发展进度', f"{career_data['summary']['avg_progress']}%"],
                ['滞后成员数', career_data['summary']['lagging_members']],
                ['高风险成员数', career_data['summary']['high_risk_members']]
            ]
            
            df_summary = pd.DataFrame(summary_data, columns=['指标', '数值'])
            df_summary.to_excel(writer, sheet_name='汇总统计', index=False)
        
        output.seek(0)
        
        filename = f"职业发展追踪报告_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        return send_file(
            output,
            as_attachment=True,
            download_name=filename,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        
    except Exception as e:
        return jsonify({'error': f'导出报告时发生错误: {str(e)}'}), 500

@career_tracking_bp.route('/api/career_data', methods=['GET'])
def get_career_data():
    """获取职业发展数据API"""
    try:
        if 'user_id' not in session:
            return jsonify({'error': '请先登录'}), 401
        
        user = User.query.get(session['user_id'])
        if not user or user.user_type != 'executive':
            return jsonify({'error': '权限不足'}), 403
        
        career_data = generate_career_tracking_data()
        return jsonify(career_data)
        
    except Exception as e:
        return jsonify({'error': f'获取数据时发生错误: {str(e)}'}), 500
