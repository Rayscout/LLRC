import json
import os
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.linecharts import HorizontalLineChart
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics import renderPDF
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # 使用非交互式后端
import numpy as np
from io import BytesIO
from PIL import Image

class TalentReportGenerator:
    """人才分析报告生成器"""
    
    def __init__(self, output_dir: str = "reports"):
        # 优先使用环境变量配置的绝对目录
        preferred = os.getenv('TALENT_REPORT_DIR') or os.getenv('REPORT_DIR')
        if preferred:
            output_dir = preferred
        # 若传入相对路径，则锚定到当前文件所在目录，转换为绝对路径
        if not os.path.isabs(output_dir):
            base_dir = os.path.dirname(os.path.abspath(__file__))
            output_dir = os.path.join(base_dir, output_dir)
        # 确保输出目录存在
        os.makedirs(output_dir, exist_ok=True)
        self.output_dir = output_dir
        
        # 字体加载
        self.base_font = self._ensure_cjk_font()
        
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _ensure_cjk_font(self) -> str:
        """确保中文字体可用，返回字体名称。优先使用环境变量指定的ttf/ttc。"""
        font_path = os.getenv('REPORT_FONT') or os.getenv('TALENT_REPORT_FONT')
        candidates = []
        if font_path and os.path.isfile(font_path):
            candidates.append(font_path)
        # 常见Windows中文字体
        candidates += [
            r"C:\\Windows\\Fonts\\msyh.ttc",    # 微软雅黑
            r"C:\\Windows\\Fonts\\simsun.ttc",  # 宋体
            r"C:\\Windows\\Fonts\\simhei.ttf",  # 黑体
        ]
        for p in candidates:
            try:
                if os.path.isfile(p):
                    pdfmetrics.registerFont(TTFont('CJKBase', p))
                    return 'CJKBase'
            except Exception:
                continue
        # 兜底：使用内置Helvetica
        return 'Helvetica'
    
    def _setup_custom_styles(self):
        """设置自定义样式"""
        # 标题样式
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontName=self.base_font,
            fontSize=18,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.darkblue
        )
        
        # 副标题样式
        self.subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=self.styles['Heading2'],
            fontName=self.base_font,
            fontSize=14,
            spaceAfter=20,
            textColor=colors.darkblue
        )
        
        # 正文样式
        self.body_style = ParagraphStyle(
            'CustomBody',
            parent=self.styles['Normal'],
            fontName=self.base_font,
            fontSize=10,
            spaceAfter=12,
            alignment=TA_LEFT
        )
        
        # 强调样式
        self.emphasis_style = ParagraphStyle(
            'CustomEmphasis',
            parent=self.styles['Normal'],
            fontName=self.base_font,
            fontSize=11,
            spaceAfter=12,
            textColor=colors.darkred
        )
    
    def generate_individual_report(self, report_data: dict, employee_name: str) -> str:
        """生成个人分析报告"""
        filename = f"individual_report_{employee_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        filepath = os.path.join(self.output_dir, filename)
        
        doc = SimpleDocTemplate(filepath, pagesize=A4)
        story = []
        
        # 添加标题
        story.append(Paragraph(f"人才发展分析报告 - {employee_name}", self.title_style))
        story.append(Spacer(1, 10))
        
        # 分析摘要（AI）
        narrative = report_data.get('narrative') or report_data.get('summary')
        if narrative:
            story.append(Paragraph("分析摘要", self.subtitle_style))
            story.append(Paragraph(narrative, self.body_style))
            story.append(Spacer(1, 10))
        
        # 基本信息
        story.append(Paragraph("基本信息", self.subtitle_style))
        employee_info = report_data.get("employee_info", {})
        basic_info_data = [
            ["姓名", employee_info.get("name", "未知")],
            ["职位", employee_info.get("position", "未知")],
            ["部门", employee_info.get("department", "未知")],
            ["薪资", f"¥{employee_info.get('salary', 0):,.2f}"],
            ["入职日期", employee_info.get("hire_date", "未知")]
        ]
        
        basic_info_table = Table(basic_info_data, colWidths=[2*inch, 4*inch])
        basic_info_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), self.base_font),
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(basic_info_table)
        story.append(Spacer(1, 10))
        
        # 离职风险分析
        story.append(Paragraph("离职风险分析", self.subtitle_style))
        turnover_analysis = report_data.get("turnover_analysis", {})
        risk_score = turnover_analysis.get("turnover_risk", 0)
        risk_level = turnover_analysis.get("risk_level", "未知")
        
        risk_text = f"离职风险概率: {risk_score:.1%} ({risk_level})"
        story.append(Paragraph(risk_text, self.emphasis_style))
        
        # 风险因素
        risk_factors = turnover_analysis.get("risk_factors", [])
        if risk_factors:
            story.append(Paragraph("主要风险因素:", self.body_style))
            for factor in risk_factors:
                story.append(Paragraph(f"• {factor}", self.body_style))
        
        # AI 建议
        recs = report_data.get('recommendations') or turnover_analysis.get("recommendations", [])
        if recs:
            story.append(Spacer(1, 6))
            story.append(Paragraph("AI 建议", self.subtitle_style))
            for rec in recs:
                story.append(Paragraph(f"• {rec}", self.body_style))
        
        story.append(Spacer(1, 10))
        
        # 市场对比分析
        story.append(Paragraph("市场对比分析", self.subtitle_style))
        market_analysis = report_data.get("market_analysis", {})
        competitiveness = market_analysis.get("salary_competitiveness", 1.0)
        market_position = market_analysis.get("market_position", "未知")
        
        comp_text = f"薪资竞争力: {competitiveness:.2f} ({market_position})"
        story.append(Paragraph(comp_text, self.emphasis_style))
        
        # 优势劣势
        advantages = market_analysis.get("advantages", [])
        disadvantages = market_analysis.get("disadvantages", [])
        
        if advantages:
            story.append(Paragraph("优势:", self.body_style))
            for adv in advantages:
                story.append(Paragraph(f"• {adv}", self.body_style))
        
        if disadvantages:
            story.append(Paragraph("劣势:", self.body_style))
            for dis in disadvantages:
                story.append(Paragraph(f"• {dis}", self.body_style))
        
        story.append(Spacer(1, 10))
        
        # 绩效总结
        story.append(Paragraph("绩效总结", self.subtitle_style))
        performance_summary = report_data.get("performance_summary", {})
        
        performance_data = [
            ["评估项目", "评分"],
            ["绩效评分", f"{performance_summary.get('performance_score', 0):.1f}/5.0"],
            ["技能水平", f"{performance_summary.get('skills_level', 0):.1f}/5.0"],
            ["工作满意度", f"{performance_summary.get('satisfaction_score', 0):.1f}/5.0"],
            ["团队协作", f"{performance_summary.get('teamwork_score', 0):.1f}/5.0"],
            ["领导力潜力", f"{performance_summary.get('leadership_potential', 0):.1f}/5.0"]
        ]
        
        performance_table = Table(performance_data, colWidths=[3*inch, 2*inch])
        performance_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), self.base_font),
            ('BACKGROUND', (0, 0), (0, 0), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(performance_table)
        
        # 生成PDF
        doc.build(story)
        return filepath
    
    def generate_department_report(self, report_data: dict, department_name: str) -> str:
        """生成部门分析报告"""
        filename = f"department_report_{department_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        filepath = os.path.join(self.output_dir, filename)
        
        doc = SimpleDocTemplate(filepath, pagesize=A4)
        story = []
        
        # 标题与摘要
        story.append(Paragraph(f"部门人才发展分析报告 - {department_name}", self.title_style))
        story.append(Spacer(1, 10))
        narrative = report_data.get('narrative') or report_data.get('summary')
        if narrative:
            story.append(Paragraph("分析摘要", self.subtitle_style))
            story.append(Paragraph(narrative, self.body_style))
            story.append(Spacer(1, 10))
        
        # 部门概览
        story.append(Paragraph("部门概览", self.subtitle_style))
        overview_data = [
            ["总员工数", str(report_data.get("total_employees", 0))],
            ["平均薪资", f"¥{report_data.get('average_salary', 0):,.2f}"],
            ["平均绩效", f"{report_data.get('average_performance', 0):.1f}/5.0"],
            ["高风险员工数", str(report_data.get("high_risk_count", 0))]
        ]
        
        overview_table = Table(overview_data, colWidths=[2*inch, 2*inch])
        overview_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), self.base_font),
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(overview_table)
        story.append(Spacer(1, 10))
        
        # 员工详细分析
        story.append(Paragraph("员工详细分析", self.subtitle_style))
        employee_analyses = report_data.get("employee_analyses", [])
        
        if employee_analyses:
            # 表头
            employee_data = [["姓名", "职位", "薪资", "绩效评分", "离职风险"]]
            
            for emp in employee_analyses:
                employee_data.append([
                    emp.get("name", "未知"),
                    emp.get("position", "未知"),
                    f"¥{emp.get('salary', 0):,.2f}",
                    f"{emp.get('performance_score', 0):.1f}",
                    f"{emp.get('turnover_risk', 0):.1%}"
                ])
            
            employee_table = Table(employee_data, colWidths=[1.2*inch, 1.5*inch, 1.2*inch, 1*inch, 1*inch])
            employee_table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (-1, -1), self.base_font),
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(employee_table)
        
        # 建议
        recs = report_data.get('recommendations') or []
        if recs:
            story.append(Spacer(1, 10))
            story.append(Paragraph("AI 建议", self.subtitle_style))
            for rec in recs:
                story.append(Paragraph(f"• {rec}", self.body_style))
        
        # 生成PDF
        doc.build(story)
        return filepath
    
    def generate_company_report(self, report_data: dict) -> str:
        """生成公司分析报告"""
        filename = f"company_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        filepath = os.path.join(self.output_dir, filename)
        
        doc = SimpleDocTemplate(filepath, pagesize=A4)
        story = []
        
        # 标题与摘要
        story.append(Paragraph("公司人才发展分析报告", self.title_style))
        story.append(Spacer(1, 10))
        narrative = report_data.get('narrative') or report_data.get('summary')
        if narrative:
            story.append(Paragraph("分析摘要", self.subtitle_style))
            story.append(Paragraph(narrative, self.body_style))
            story.append(Spacer(1, 10))
        
        # 公司概览
        story.append(Paragraph("公司概览", self.subtitle_style))
        overall_metrics = report_data.get("overall_metrics", {})
        overview_data = [
            ["总员工数", str(report_data.get("total_employees", 0))],
            ["平均薪资", f"¥{overall_metrics.get('average_salary', 0):,.2f}"],
            ["平均绩效", f"{overall_metrics.get('average_performance', 0):.1f}/5.0"],
            ["高风险员工比例", f"{overall_metrics.get('high_risk_percentage', 0):.1f}%"]
        ]
        
        overview_table = Table(overview_data, colWidths=[2*inch, 2*inch])
        overview_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), self.base_font),
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(overview_table)
        story.append(Spacer(1, 10))
        
        # 部门分析
        story.append(Paragraph("部门分析", self.subtitle_style))
        departments = report_data.get("departments", {})
        
        if departments:
            dept_data = [["部门", "员工数", "平均薪资", "平均绩效"]]
            
            for dept_name, dept_info in departments.items():
                dept_data.append([
                    dept_name,
                    str(dept_info.get("count", 0)),
                    f"¥{dept_info.get('avg_salary', 0):,.2f}",
                    f"{dept_info.get('avg_performance', 0):.1f}"
                ])
            
            dept_table = Table(dept_data, colWidths=[1.5*inch, 1*inch, 1.5*inch, 1*inch])
            dept_table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (-1, -1), self.base_font),
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(dept_table)
            story.append(Spacer(1, 10))
        
        # 风险分布
        story.append(Paragraph("风险分布", self.subtitle_style))
        risk_distribution = report_data.get("risk_distribution", {})
        risk_data = [
            ["风险等级", "员工数量"],
            ["低风险", str(risk_distribution.get("low_risk", 0))],
            ["中风险", str(risk_distribution.get("medium_risk", 0))],
            ["高风险", str(risk_distribution.get("high_risk", 0))]
        ]
        
        risk_table = Table(risk_data, colWidths=[2*inch, 2*inch])
        risk_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), self.base_font),
            ('BACKGROUND', (0, 0), (0, 0), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(risk_table)
        
        # AI 建议
        recs = report_data.get('recommendations') or []
        if recs:
            story.append(Spacer(1, 10))
            story.append(Paragraph("AI 建议", self.subtitle_style))
            for rec in recs:
                story.append(Paragraph(f"• {rec}", self.body_style))
        
        # 生成PDF
        doc.build(story)
        return filepath
    
    def create_chart_image(self, chart_data: dict, chart_type: str) -> str:
        """创建图表图片"""
        plt.figure(figsize=(10, 6))
        
        if chart_type == "pie":
            labels = list(chart_data.keys())
            sizes = list(chart_data.values())
            plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
            plt.axis('equal')
        
        elif chart_type == "bar":
            labels = list(chart_data.keys())
            values = list(chart_data.values())
            plt.bar(labels, values)
            plt.xlabel('类别')
            plt.ylabel('数值')
            plt.xticks(rotation=45)
        
        elif chart_type == "line":
            months = list(chart_data.keys())
            values = list(chart_data.values())
            plt.plot(months, values, marker='o')
            plt.xlabel('月份')
            plt.ylabel('数值')
            plt.xticks(rotation=45)
        
        # 保存图片
        img_filename = f"chart_{chart_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        img_path = os.path.join(self.output_dir, img_filename)
        plt.savefig(img_path, bbox_inches='tight', dpi=300)
        plt.close()
        
        return img_path
