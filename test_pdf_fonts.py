#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF字体测试脚本
用于测试中文字体在PDF生成中是否正常工作
"""

import os
import tempfile
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

def test_chinese_font():
    """测试中文字体功能"""
    print("=== PDF中文字体测试 ===")
    
    # 创建临时PDF文件
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
    doc = SimpleDocTemplate(temp_file.name, pagesize=A4)
    
    # 尝试注册中文字体
    font_name = setup_test_font()
    
    # 创建样式
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'TestTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=20,
        alignment=TA_CENTER,
        textColor=colors.darkblue,
        fontName=font_name
    )
    
    normal_style = ParagraphStyle(
        'TestNormal',
        parent=styles['Normal'],
        fontSize=12,
        spaceAfter=10,
        fontName=font_name
    )
    
    # 测试内容
    story = []
    
    # 标题
    story.append(Paragraph("中文字体测试报告", title_style))
    story.append(Spacer(1, 20))
    
    # 基本信息
    story.append(Paragraph("基本信息", normal_style))
    story.append(Paragraph("姓名：张三", normal_style))
    story.append(Paragraph("职位：软件工程师", normal_style))
    story.append(Paragraph("部门：技术部", normal_style))
    story.append(Paragraph("邮箱：zhangsan@company.com", normal_style))
    story.append(Spacer(1, 20))
    
    # 技能列表
    story.append(Paragraph("技能列表", normal_style))
    skills = ["Python编程", "Java开发", "数据库设计", "前端开发", "项目管理"]
    for skill in skills:
        story.append(Paragraph(f"• {skill}", normal_style))
    story.append(Spacer(1, 20))
    
    # 工作经历
    story.append(Paragraph("工作经历", normal_style))
    story.append(Paragraph("2020-2022 某科技公司 - 初级开发工程师", normal_style))
    story.append(Paragraph("负责公司核心产品的开发和维护工作", normal_style))
    story.append(Paragraph("2022-至今 当前公司 - 软件工程师", normal_style))
    story.append(Paragraph("参与多个重要项目的开发，具备丰富的实战经验", normal_style))
    story.append(Spacer(1, 20))
    
    # 教育背景
    story.append(Paragraph("教育背景", normal_style))
    story.append(Paragraph("2016-2020 某大学 - 计算机科学与技术 - 本科", normal_style))
    story.append(Paragraph("主修课程：数据结构、算法设计、软件工程等", normal_style))
    
    # 生成PDF
    try:
        doc.build(story)
        print(f"✓ PDF生成成功: {temp_file.name}")
        print(f"✓ 使用的字体: {font_name}")
        return temp_file.name
    except Exception as e:
        print(f"✗ PDF生成失败: {e}")
        return None

def setup_test_font():
    """设置测试字体"""
    print("正在设置中文字体...")
    
    # 字体候选列表
    font_candidates = []
    
    # 1. 系统字体路径
    system_fonts = [
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Medium.ttc",
        "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
        "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    
    # 2. 项目内字体
    project_fonts = [
        os.path.join(os.path.dirname(__file__), 'fonts', 'NotoSansCJK-Regular.otf'),
        os.path.join(os.path.dirname(__file__), 'fonts', 'NotoSansCJK-Medium.otf'),
    ]
    
    font_candidates.extend(system_fonts)
    font_candidates.extend(project_fonts)
    
    # 尝试注册字体
    for font_path in font_candidates:
        if os.path.exists(font_path):
            try:
                pdfmetrics.registerFont(TTFont('ChineseFont', font_path))
                print(f"✓ 成功注册字体: {font_path}")
                return 'ChineseFont'
            except Exception as e:
                print(f"✗ 字体注册失败 {font_path}: {e}")
                continue
    
    # 尝试使用内置字体
    try:
        from reportlab.pdfbase.cidfonts import UnicodeCIDFont
        pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))
        print("✓ 使用内置UnicodeCIDFont字体")
        return 'STSong-Light'
    except Exception as e:
        print(f"✗ 内置字体注册失败: {e}")
    
    # 使用默认字体
    print("⚠ 使用默认字体（可能不支持中文）")
    return 'Helvetica'

def main():
    """主函数"""
    print("开始PDF中文字体测试...")
    
    # 测试字体设置
    font_name = setup_test_font()
    print(f"最终使用的字体: {font_name}")
    
    # 生成测试PDF
    pdf_path = test_chinese_font()
    
    if pdf_path:
        print(f"\n✓ 测试完成！")
        print(f"PDF文件位置: {pdf_path}")
        print("请打开PDF文件检查中文字体是否正确显示")
    else:
        print(f"\n✗ 测试失败！")
        print("请检查字体安装情况")

if __name__ == '__main__':
    main()
