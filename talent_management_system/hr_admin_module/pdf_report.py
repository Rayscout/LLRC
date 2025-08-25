from flask import Blueprint, render_template, request, jsonify, send_file, session
from app.models import User, db
from datetime import datetime, timedelta
import random
import json
# from reportlab.lib.pagesizes import letter, A4
# from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
# from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
# from reportlab.lib.units import inch
# from reportlab.lib import colors
# from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
import io
import os

pdf_report_bp = Blueprint('pdf_report', __name__, url_prefix='/pdf_report')

def generate_mock_data():
    """生成模拟数据用于PDF报告"""
    return {
        'company_name': '林理人才开发团队',
        'report_date': datetime.now().strftime('%Y年%m月%d日'),
        'total_employees': 156,
        'departments': {
            '技术部': {'count': 45, 'turnover_rate': 0.12, 'avg_salary': 18500},
            '市场部': {'count': 28, 'turnover_rate': 0.08, 'avg_salary': 12500},
            '销售部': {'count': 35, 'turnover_rate': 0.15, 'avg_salary': 15800},
            '人事部': {'count': 12, 'turnover_rate': 0.05, 'avg_salary': 9800},
            '财务部': {'count': 18, 'turnover_rate': 0.03, 'avg_salary': 11200},
            '行政部': {'count': 18, 'turnover_rate': 0.06, 'avg_salary': 8500}
        },
        'risk_analysis': {
            'high_risk': [
                {'position': '高级工程师', 'risk': 85, 'reason': '薪资竞争力不足、职业发展受限'},
                {'position': '产品经理', 'risk': 72, 'reason': '工作压力大、缺乏资源支持'},
                {'position': '销售总监', 'risk': 68, 'reason': '业绩压力、激励机制不完善'}
            ],
            'medium_risk': [
                {'position': 'UI设计师', 'risk': 45, 'reason': '技能发展瓶颈'},
                {'position': '市场专员', 'risk': 38, 'reason': '薪酬水平偏低'},
                {'position': '人事专员', 'risk': 35, 'reason': '工作内容单一'}
            ]
        },
        'salary_comparison': {
            'technical': {'company': 18000, 'industry': 16700, 'difference': '+8%'},
            'management': {'company': 25000, 'industry': 25000, 'difference': '持平'},
            'sales': {'company': 12000, 'industry': 12600, 'difference': '-5%'},
            'admin': {'company': 8000, 'industry': 7800, 'difference': '+3%'}
        },
        'supply_demand_trend': {
            'months': ['1月', '2月', '3月', '4月', '5月', '6月'],
            'demand': [100, 110, 125, 135, 150, 175],
            'supply': [90, 95, 100, 105, 110, 115]
        },
        'recommendations': [
            '增加关键岗位的薪酬竞争力，特别是技术岗位',
            '建立完善的职业发展通道和晋升机制',
            '优化工作环境，减少员工工作压力',
            '加强员工培训和技能发展计划',
            '完善激励机制，提高员工满意度'
        ]
    }

@pdf_report_bp.route('/generate_executive_report', methods=['POST'])
def generate_executive_report():
    """生成高管人才发展报告PDF"""
    try:
        if 'user_id' not in session:
            return jsonify({'error': '请先登录'}), 401
        
        user = User.query.get(session['user_id'])
        if not user or user.user_type != 'executive':
            return jsonify({'error': '权限不足'}), 403
        
        # 获取模拟数据
        data = generate_mock_data()
        
        # 创建PDF文档
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
        
        # 获取样式
        styles = getSampleStyleSheet()
        
        # 创建自定义样式
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.darkblue
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            spaceAfter=12,
            spaceBefore=20,
            textColor=colors.darkblue
        )
        
        normal_style = ParagraphStyle(
            'CustomNormal',
            parent=styles['Normal'],
            fontSize=12,
            spaceAfter=6
        )
        
        # 构建PDF内容
        story = []
        
        # 标题页
        story.append(Paragraph(f"{data['company_name']}", title_style))
        story.append(Paragraph("人才发展分析报告", title_style))
        story.append(Paragraph(f"报告日期：{data['report_date']}", normal_style))
        story.append(Paragraph(f"生成人：{user.first_name} {user.last_name}", normal_style))
        story.append(Paragraph(f"职位：{user.position}", normal_style))
        story.append(PageBreak())
        
        # 执行摘要
        story.append(Paragraph("执行摘要", heading_style))
        story.append(Paragraph(f"本报告分析了{data['company_name']}的人才发展现状，包括员工总数{data['total_employees']}人，涵盖6个主要部门。", normal_style))
        story.append(Paragraph("报告重点关注离职风险分析、薪酬竞争力对比、人才供需趋势以及相应的战略建议。", normal_style))
        story.append(Spacer(1, 20))
        
        # 部门概况
        story.append(Paragraph("1. 部门概况", heading_style))
        dept_data = [['部门', '员工数量', '离职率', '平均薪酬']]
        for dept, info in data['departments'].items():
            dept_data.append([
                dept,
                str(info['count']),
                f"{info['turnover_rate']*100:.1f}%",
                f"¥{info['avg_salary']:,}"
            ])
        
        dept_table = Table(dept_data)
        dept_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(dept_table)
        story.append(Spacer(1, 20))
        
        # 离职风险分析
        story.append(Paragraph("2. 离职风险分析", heading_style))
        
        # 高风险岗位
        story.append(Paragraph("2.1 高风险岗位", styles['Heading3']))
        for position in data['risk_analysis']['high_risk']:
            story.append(Paragraph(f"• {position['position']}: 离职风险 {position['risk']}% - {position['reason']}", normal_style))
        
        story.append(Spacer(1, 10))
        
        # 中等风险岗位
        story.append(Paragraph("2.2 中等风险岗位", styles['Heading3']))
        for position in data['risk_analysis']['medium_risk']:
            story.append(Paragraph(f"• {position['position']}: 离职风险 {position['risk']}% - {position['reason']}", normal_style))
        
        story.append(Spacer(1, 20))
        
        # 薪酬对比分析
        story.append(Paragraph("3. 薪酬对比分析", heading_style))
        salary_data = [['岗位类型', '公司薪酬', '行业平均', '差异']]
        for pos_type, info in data['salary_comparison'].items():
            salary_data.append([
                pos_type.title(),
                f"¥{info['company']:,}",
                f"¥{info['industry']:,}",
                info['difference']
            ])
        
        salary_table = Table(salary_data)
        salary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(salary_table)
        story.append(Spacer(1, 20))
        
        # 供需趋势
        story.append(Paragraph("4. 未来6个月供需趋势", heading_style))
        story.append(Paragraph("根据市场分析，未来6个月技术人才需求将增长25%，而市场供给仅增长10%，供需缺口将达到35%。", normal_style))
        story.append(Paragraph("建议提前制定招聘计划，加强内部人才培养，并考虑提高技术岗位的薪酬竞争力。", normal_style))
        story.append(Spacer(1, 20))
        
        # 战略建议
        story.append(Paragraph("5. 战略建议", heading_style))
        for i, recommendation in enumerate(data['recommendations'], 1):
            story.append(Paragraph(f"{i}. {recommendation}", normal_style))
        
        story.append(Spacer(1, 20))
        
        # 结论
        story.append(Paragraph("结论", heading_style))
        story.append(Paragraph("通过本次人才发展分析，我们发现公司在人才保留和薪酬竞争力方面存在一定挑战。", normal_style))
        story.append(Paragraph("建议采取积极的措施来改善员工满意度，提高薪酬竞争力，并建立完善的人才发展体系。", normal_style))
        story.append(Paragraph("这些措施将有助于降低离职率，提高员工忠诚度，为公司的长期发展奠定坚实的人才基础。", normal_style))
        
        # 生成PDF
        doc.build(story)
        buffer.seek(0)
        
        # 返回PDF文件
        filename = f"人才发展报告_{data['report_date'].replace('/', '')}.pdf"
        return send_file(
            buffer,
            as_attachment=True,
            download_name=filename,
            mimetype='application/pdf'
        )
        
    except Exception as e:
        return jsonify({'error': f'生成PDF报告时发生错误: {str(e)}'}), 500

@pdf_report_bp.route('/api/generate-pdf-report', methods=['POST'])
def api_generate_pdf_report():
    """API接口：生成PDF报告"""
    try:
        if 'user_id' not in session:
            return jsonify({'error': '请先登录'}), 401
        
        user = User.query.get(session['user_id'])
        if not user or user.user_type != 'executive':
            return jsonify({'error': '权限不足'}), 403
        
        # 返回PDF下载链接
        return jsonify({
            'success': True,
            'message': 'PDF报告生成成功',
            'download_url': '/talent/hr_admin/pdf_report/generate_executive_report'
        })
        
    except Exception as e:
        return jsonify({'error': f'生成PDF报告时发生错误: {str(e)}'}), 500
