@turnover_alert_bp.route('/api/generate_report')
def api_generate_report():
    """生成离职预警报告PDF"""
    try:
        if 'user_id' not in session:
            return jsonify({'error': '请先登录'}), 401
        
        user = User.query.get(session['user_id'])
        if not user or user.user_type != 'executive':
            return jsonify({'error': '权限不足'}), 403
        
        # 检查reportlab是否可用
        try:
            from reportlab.lib.pagesizes import letter, A4
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.units import inch
            from reportlab.lib import colors
            from reportlab.pdfgen import canvas
        except ImportError as e:
            print(f"缺少reportlab依赖: {e}")
            return jsonify({'error': '服务器缺少PDF生成库，请联系管理员安装'}), 500
        
        # 生成模拟数据
        generate_mock_turnover_data()
        
        # 生成报告数据
        report_id = str(uuid.uuid4())
        report_data = {
            'report_id': report_id,
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
        
        # 创建PDF文件
        output = io.BytesIO()
        doc = SimpleDocTemplate(output, pagesize=A4)
        styles = getSampleStyleSheet()
        story = []
        
        # 标题
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=1,
            textColor=colors.darkblue
        )
        story.append(Paragraph("人才流失预警报告", title_style))
        story.append(Spacer(1, 20))
        
        # 报告信息
        info_style = ParagraphStyle(
            'Info',
            parent=styles['Normal'],
            fontSize=12,
            spaceAfter=20
        )
        story.append(Paragraph(f"报告ID: {report_id}", info_style))
        story.append(Paragraph(f"生成时间: {report_data['generated_at']}", info_style))
        story.append(Paragraph(f"生成人员: {user.first_name} {user.last_name}", info_style))
        story.append(Spacer(1, 20))
        
        # 总体概览
        story.append(Paragraph("总体概览", styles['Heading2']))
        story.append(Spacer(1, 12))
        
        summary_data = [
            ['指标', '数值'],
            ['总员工数', str(report_data['summary']['total_employees'])],
            ['高风险部门数', str(report_data['summary']['high_risk_departments'])],
            ['高风险岗位数', str(report_data['summary']['high_risk_positions'])],
            ['高风险员工数', str(report_data['summary']['high_risk_employees'])]
        ]
        
        summary_table = Table(summary_data, colWidths=[2*inch, 2*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(summary_table)
        story.append(Spacer(1, 20))
        
        # 部门分析
        story.append(Paragraph("部门分析", styles['Heading2']))
        story.append(Spacer(1, 12))
        
        dept_data = [['部门名称', '员工总数', '离职人数', '离职率', '风险等级']]
        for dept_name, dept_info in report_data['department_analysis'].items():
            dept_data.append([
                dept_name,
                str(dept_info['total_employees']),
                str(dept_info['turnover_count']),
                f"{dept_info['turnover_rate']*100:.1f}%",
                dept_info['risk_level']
            ])
        
        dept_table = Table(dept_data, colWidths=[1.2*inch, 1*inch, 1*inch, 1*inch, 1*inch])
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
        
        # 高风险岗位
        story.append(Paragraph("高风险岗位分析", styles['Heading2']))
        story.append(Spacer(1, 12))
        
        pos_data = [['岗位名称', '离职风险', '市场需求', '技能差距']]
        high_risk_positions = [(name, info) for name, info in report_data['position_analysis'].items() 
                              if info['turnover_risk'] > 0.6]
        high_risk_positions.sort(key=lambda x: x[1]['turnover_risk'], reverse=True)
        
        for pos_name, pos_info in high_risk_positions[:10]:  # 只显示前10个
            pos_data.append([
                pos_name,
                f"{pos_info['turnover_risk']*100:.1f}%",
                f"{pos_info['market_demand']:.2f}",
                f"{pos_info['skill_gap']:.2f}"
            ])
        
        pos_table = Table(pos_data, colWidths=[1.5*inch, 1*inch, 1*inch, 1*inch])
        pos_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(pos_table)
        story.append(Spacer(1, 20))
        
        # 预防建议
        story.append(Paragraph("预防建议", styles['Heading2']))
        story.append(Spacer(1, 12))
        
        for i, recommendation in enumerate(report_data['recommendations'], 1):
            story.append(Paragraph(f"{i}. {recommendation}", styles['Normal']))
            story.append(Spacer(1, 6))
        
        # 生成PDF
        doc.build(story)
        output.seek(0)
        
        # 使用英文文件名避免编码问题
        safe_filename = f"turnover_alert_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        
        return send_file(
            output,
            as_attachment=True,
            download_name=safe_filename,
            mimetype='application/pdf'
        )
        
    except Exception as e:
        print(f"生成报告错误: {e}")
        return jsonify({'error': f'生成报告失败: {str(e)}'}), 500
