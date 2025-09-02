#!/bin/bash
# 人才流失预警报告生成功能快速修复

echo "🚀 开始快速修复人才流失预警报告生成功能..."

# 检查是否在云服务器环境
if [ -f "/etc/systemd/system/llrc.service" ]; then
    echo "ℹ️ 检测到云服务器环境"
    SERVER_ENV="cloud"
else
    echo "ℹ️ 检测到本地环境"
    SERVER_ENV="local"
fi

# 步骤1: 备份当前文件
echo "ℹ️ 步骤1: 备份当前文件..."
BACKUP_DIR="backup_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

if [ -f "talent_management_system/hr_admin_module/turnover_alert.py" ]; then
    cp talent_management_system/hr_admin_module/turnover_alert.py "$BACKUP_DIR/"
    echo "✅ 已备份后端模块"
fi

if [ -f "app/templates/talent_management/hr_admin/turnover_dashboard.html" ]; then
    cp app/templates/talent_management/hr_admin/turnover_dashboard.html "$BACKUP_DIR/"
    echo "✅ 已备份前端模板"
fi

# 步骤2: 修复后端模块 - 使用sed命令替换关键部分
echo "ℹ️ 步骤2: 修复后端模块..."

# 替换函数注释
sed -i 's/"""生成离职预警报告"""/"""生成离职预警报告PDF"""/g' talent_management_system/hr_admin_module/turnover_alert.py

# 添加reportlab依赖检查（在函数开始处）
sed -i '/if '\''user_id'\'' not in session:/i\        # 检查reportlab是否可用\n        try:\n            from reportlab.lib.pagesizes import letter, A4\n            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle\n            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle\n            from reportlab.lib.units import inch\n            from reportlab.lib import colors\n            from reportlab.pdfgen import canvas\n        except ImportError as e:\n            print(f"缺少reportlab依赖: {e}")\n            return jsonify({\"error\": \"服务器缺少PDF生成库，请联系管理员安装\"}), 500\n' talent_management_system/hr_admin_module/turnover_alert.py

# 替换返回语句为PDF生成
sed -i '/return jsonify({/,$d' talent_management_system/hr_admin_module/turnover_alert.py
cat >> talent_management_system/hr_admin_module/turnover_alert.py << 'EOF'
        
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
EOF

echo "✅ 后端模块修复完成"

# 步骤3: 修复前端模板
echo "ℹ️ 步骤3: 修复前端模板..."

# 替换generateReport函数
sed -i '/function generateReport() {/,/}/c\        // 生成预警报告\n        function generateReport() {\n            const btn = event.target.closest(\"button\");\n            if (btn) {\n                btn.style.transform = \"scale(0.95)\";\n                setTimeout(() => {\n                    btn.style.transform = \"scale(1)\";\n                }, 150);\n            }\n            \n            // 显示加载状态\n            const originalText = btn.innerHTML;\n            btn.innerHTML = \"<i class=\\\"fas fa-spinner fa-spin\\\"></i> 生成中...\";\n            btn.disabled = true;\n            \n            fetch(\"/talent/hr_admin/turnover_alert/api/generate_report\")\n                .then(response => {\n                    if (response.ok) {\n                        return response.blob();\n                    } else {\n                        return response.text().then(text => {\n                            throw new Error(`生成失败: ${response.status} ${response.statusText}`);\n                        });\n                    }\n                })\n                .then(blob => {\n                    // 创建下载链接\n                    const url = window.URL.createObjectURL(blob);\n                    const a = document.createElement(\"a\");\n                    a.href = url;\n                    a.download = `turnover_alert_report_${new Date().toISOString().slice(0,10)}.pdf`;\n                    document.body.appendChild(a);\n                    a.click();\n                    window.URL.revokeObjectURL(url);\n                    document.body.removeChild(a);\n                    \n                    // 显示成功通知\n                    showNotification(\"预警报告生成成功！\", \"success\");\n                })\n                .catch(error => {\n                    console.error(\"生成报告失败:\", error);\n                    \n                    // 显示详细错误信息\n                    let errorMessage = \"生成报告失败，请重试。\";\n                    if (error.message.includes(\"502\")) {\n                        errorMessage = \"服务器暂时不可用，请稍后重试。错误信息: \" + error.message;\n                    } else if (error.message.includes(\"500\")) {\n                        errorMessage = \"服务器内部错误，请联系管理员。错误信息: \" + error.message;\n                    } else if (error.message.includes(\"404\")) {\n                        errorMessage = \"生成接口不存在，请联系管理员。错误信息: \" + error.message;\n                    } else if (error.message.includes(\"403\")) {\n                        errorMessage = \"权限不足，请检查登录状态。错误信息: \" + error.message;\n                    } else if (error.message.includes(\"401\")) {\n                        errorMessage = \"请先登录系统。错误信息: \" + error.message;\n                    } else {\n                        errorMessage = \"生成报告失败，请重试。错误信息: \" + error.message;\n                    }\n                    \n                    showNotification(errorMessage, \"error\");\n                })\n                .finally(() => {\n                    // 恢复按钮状态\n                    btn.innerHTML = originalText;\n                    btn.disabled = false;\n                });\n        }' app/templates/talent_management/hr_admin/turnover_dashboard.html

echo "✅ 前端模板修复完成"

# 步骤4: 重启服务
if [ "$SERVER_ENV" = "cloud" ]; then
    echo "ℹ️ 步骤4: 重启服务..."
    sudo systemctl restart llrc
    if [ $? -eq 0 ]; then
        echo "✅ llrc服务重启成功"
    else
        echo "❌ llrc服务重启失败"
    fi
fi

# 步骤5: 验证修复
echo "ℹ️ 步骤5: 验证修复..."
echo "📋 修复内容检查:"

if grep -q "生成离职预警报告PDF" talent_management_system/hr_admin_module/turnover_alert.py; then
    echo "✅ 后端PDF生成功能已添加"
else
    echo "❌ 后端PDF生成功能未添加"
fi

if grep -q "生成中..." app/templates/talent_management/hr_admin/turnover_dashboard.html; then
    echo "✅ 前端下载功能已修复"
else
    echo "❌ 前端下载功能未修复"
fi

echo ""
echo "🎉 人才流失预警报告生成功能快速修复完成！"
echo ""
echo "📋 修复总结:"
echo "- 后端现在生成PDF文件而不是JSON数据"
echo "- 前端现在下载PDF文件而不是显示弹窗"
echo "- 添加了完整的错误处理和用户通知"
echo "- 使用英文文件名避免编码问题"
echo ""
echo "🔄 如果是在云服务器上，建议:"
echo "sudo systemctl restart llrc"
echo ""
echo "📁 备份文件保存在: $BACKUP_DIR"
echo ""
echo "🧪 现在可以测试'生成预警报告'功能了！"
