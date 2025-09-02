#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UI修复工具
整合所有UI相关的修复和优化功能
"""

import os
import re
from pathlib import Path

class UIFixTool:
    """UI修复工具类"""
    
    def __init__(self, project_root='.'):
        self.project_root = Path(project_root)
        self.templates_dir = self.project_root / 'app' / 'templates'
        
    def fix_hr_admin_dashboard(self):
        """修复HR管理员仪表板UI问题"""
        print("🔧 修复HR管理员仪表板UI问题...")
        
        dashboard_file = self.templates_dir / 'talent_management' / 'hr_admin' / 'feedback_dashboard.html'
        
        if not dashboard_file.exists():
            print(f"❌ 文件不存在: {dashboard_file}")
            return False
        
        try:
            # 读取文件内容
            with open(dashboard_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 修复CSS动画问题
            print("1. 修复CSS动画问题...")
            
            # 确保slide-in-right动画保持最终状态
            content = re.sub(
                r'\.slide-in-right\s*\{\s*animation:\s*slideInRight\s+[^}]*\}',
                '.slide-in-right {\n            animation: slideInRight 0.8s ease-out forwards;\n        }',
                content
            )
            
            # 添加CSS确保卡片始终可见
            if 'opacity: 1 !important;' not in content:
                content = re.sub(
                    r'(\.info-card\s*\{[^}]*\})',
                    r'\1\n            /* 确保卡片始终可见 */\n            opacity: 1 !important;\n            visibility: visible !important;\n            display: block !important;',
                    content
                )
            
            # 添加JavaScript修复
            print("2. 添加JavaScript修复...")
            
            if 'fixSidebarElements' not in content:
                # 在script标签结束前添加修复函数
                fix_script = '''
        // HR管理员仪表板修复脚本
        function fixSidebarElements() {
            const sidebarCards = document.querySelectorAll('.sidebar .info-card');
            console.log(`找到 ${sidebarCards.length} 个侧边栏卡片`);
            
            sidebarCards.forEach((card, index) => {
                // 强制设置可见性
                card.style.opacity = '1';
                card.style.visibility = 'visible';
                card.style.display = 'block';
                card.style.transform = 'translateX(0)';
                
                const title = card.querySelector('h3');
                if (title) {
                    console.log(`修复卡片 ${index + 1}: ${title.textContent.trim()}`);
                }
            });
        }
        
        // 立即修复
        fixSidebarElements();
        
        // 延迟修复（防止动画干扰）
        setTimeout(fixSidebarElements, 100);
        setTimeout(fixSidebarElements, 500);
        setTimeout(fixSidebarElements, 1000);
        
        // 定期检查元素可见性
        setInterval(() => {
            const sidebarCards = document.querySelectorAll('.sidebar .info-card');
            sidebarCards.forEach(card => {
                if (card.style.opacity === '0' || card.style.visibility === 'hidden') {
                    console.log('检测到隐藏的侧边栏卡片，正在修复...');
                    card.style.opacity = '1';
                    card.style.visibility = 'visible';
                    card.style.display = 'block';
                }
            });
        }, 2000);
'''
                
                # 在script标签结束前插入修复代码
                content = content.replace(
                    '    </script>',
                    fix_script + '\n    </script>'
                )
            
            # 写回文件
            with open(dashboard_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("✅ HR管理员仪表板UI修复完成")
            return True
            
        except Exception as e:
            print(f"❌ 修复失败: {e}")
            return False
    
    def fix_employee_feedback_dashboard(self):
        """修复员工反馈仪表板UI问题"""
        print("🔧 修复员工反馈仪表板UI问题...")
        
        dashboard_file = self.templates_dir / 'talent_management' / 'employee_management' / 'feedback_dashboard.html'
        
        if not dashboard_file.exists():
            print(f"❌ 文件不存在: {dashboard_file}")
            return False
        
        try:
            # 读取文件内容
            with open(dashboard_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查是否已有发送反馈按钮
            if '发送反馈' not in content:
                print("1. 添加发送反馈按钮...")
                
                # 在操作栏中添加发送反馈按钮
                action_bar_pattern = r'(<div class="action-bar">)'
                send_button = '''
            <a href="{{ url_for('talent_management.employee_manager.feedback.send_feedback') }}" class="action-btn">
                <i class="fas fa-paper-plane"></i> 发送反馈
            </a>
            <a href="{{ url_for('talent_management.employee_manager.feedback.sent_feedback') }}" class="action-btn secondary">
                <i class="fas fa-list"></i> 查看已发送
            </a>'''
                
                content = re.sub(action_bar_pattern, r'\1' + send_button, content)
            
            # 检查是否已有已发送反馈区域
            if '已发送的反馈' not in content:
                print("2. 添加已发送反馈区域...")
                
                # 在内容区域末尾添加已发送反馈区域
                sent_feedback_section = '''
            <!-- 已发送的反馈 -->
            <div class="content-card">
                <h2 class="section-title">
                    <i class="fas fa-paper-plane"></i> 已发送的反馈
                </h2>
                <div class="feedback-list">
                    {% if sent_feedback %}
                        {% for feedback in sent_feedback %}
                            <div class="feedback-item">
                                <div class="feedback-header">
                                    <div class="feedback-info">
                                        <h4>
                                            {% if feedback.category == 'skill' %}
                                                🚀 技能发展
                                            {% elif feedback.category == 'communication' %}
                                                💬 沟通协作
                                            {% elif feedback.category == 'performance' %}
                                                📈 绩效表现
                                            {% elif feedback.category == 'general' %}
                                                📝 一般反馈
                                            {% else %}
                                                📝 {{ feedback.category }}
                                            {% endif %}
                                            <span class="priority-badge priority-{{ feedback.priority }}">
                                                {% if feedback.priority == 'high' %}
                                                    高优先级
                                                {% elif feedback.priority == 'medium' %}
                                                    中优先级
                                                {% else %}
                                                    低优先级
                                                {% endif %}
                                            </span>
                                        </h4>
                                        <div class="feedback-meta">
                                            发送给: {{ feedback.recipient.first_name }} {{ feedback.recipient.last_name }} ({{ feedback.recipient.position or '未知职位' }})
                                            <br>
                                            {{ feedback.created_at.strftime('%Y年%m月%d日 %H:%M') }}
                                        </div>
                                    </div>
                                    <span class="feedback-status status-{{ feedback.status }}">
                                        {% if feedback.status == 'sent' %}
                                            待回复
                                        {% elif feedback.status == 'read' %}
                                            已读
                                        {% elif feedback.status == 'responded' %}
                                            已回复
                                        {% elif feedback.status == 'archived' %}
                                            已归档
                                        {% endif %}
                                    </span>
                                </div>
                                <div class="feedback-message">
                                    {{ feedback.content[:100] }}{% if feedback.content|length > 100 %}...{% endif %}
                                </div>
                                <div class="feedback-actions">
                                    <a href="{{ url_for('talent_management.employee_management.feedback.view_feedback', feedback_id=feedback.id) }}"
                                       class="btn-small btn-primary">
                                        <i class="fas fa-eye"></i> 查看详情
                                    </a>
                                    {% if feedback.status == 'responded' %}
                                        <span class="btn-small btn-success">
                                            <i class="fas fa-check"></i> 已回复
                                        </span>
                                    {% endif %}
                                </div>
                            </div>
                        {% endfor %}
                    {% else %}
                        <div class="empty-state">
                            <i class="fas fa-paper-plane"></i>
                            <p>您还没有发送任何反馈</p>
                            <p class="text-muted">点击"发送反馈"按钮开始向高管发送反馈</p>
                        </div>
                    {% endif %}
                </div>
            </div>'''
                
                # 在内容区域末尾添加
                content = content.replace('</div>', sent_feedback_section + '\n</div>', 1)
            
            # 写回文件
            with open(dashboard_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("✅ 员工反馈仪表板UI修复完成")
            return True
            
        except Exception as e:
            print(f"❌ 修复失败: {e}")
            return False
    
    def create_ui_fix_script(self):
        """创建UI修复脚本"""
        print("📝 创建UI修复脚本...")
        
        script_content = '''// UI修复脚本
// 解决"快速操作"和"反馈分类"元素消失的问题

document.addEventListener('DOMContentLoaded', function() {
    console.log('🔧 应用UI修复脚本...');
    
    // 修复函数
    function fixSidebarElements() {
        const sidebarCards = document.querySelectorAll('.sidebar .info-card');
        console.log(`找到 ${sidebarCards.length} 个侧边栏卡片`);
        
        sidebarCards.forEach((card, index) => {
            // 强制设置可见性
            card.style.opacity = '1';
            card.style.visibility = 'visible';
            card.style.display = 'block';
            card.style.transform = 'translateX(0)';
            
            // 移除可能导致问题的动画类
            card.classList.remove('slide-in-right');
            
            const title = card.querySelector('h3');
            if (title) {
                console.log(`修复卡片 ${index + 1}: ${title.textContent.trim()}`);
            }
        });
    }
    
    // 立即修复
    fixSidebarElements();
    
    // 延迟修复（防止动画干扰）
    setTimeout(fixSidebarElements, 100);
    setTimeout(fixSidebarElements, 500);
    setTimeout(fixSidebarElements, 1000);
    
    // 监听动画结束事件
    const animatedElements = document.querySelectorAll('.slide-in-right');
    animatedElements.forEach(el => {
        el.addEventListener('animationend', function() {
            console.log('动画结束，确保元素可见');
            this.style.opacity = '1';
            this.style.visibility = 'visible';
            this.style.transform = 'translateX(0)';
        });
    });
    
    // 定期检查元素可见性
    setInterval(() => {
        const sidebarCards = document.querySelectorAll('.sidebar .info-card');
        sidebarCards.forEach(card => {
            if (card.style.opacity === '0' || card.style.visibility === 'hidden') {
                console.log('检测到隐藏的侧边栏卡片，正在修复...');
                card.style.opacity = '1';
                card.style.visibility = 'visible';
                card.style.display = 'block';
            }
        });
    }, 2000);
    
    console.log('✅ UI修复脚本已应用');
});

// 添加CSS修复
const style = document.createElement('style');
style.textContent = `
    .sidebar .info-card {
        opacity: 1 !important;
        visibility: visible !important;
        display: block !important;
        transform: translateX(0) !important;
    }
    
    .sidebar .info-card h3 {
        opacity: 1 !important;
        visibility: visible !important;
    }
`;
document.head.appendChild(style);
'''
        
        # 保存到tools目录
        script_file = self.project_root / 'talent_management_system' / 'tools' / 'ui_fix_script.js'
        script_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(script_file, 'w', encoding='utf-8') as f:
            f.write(script_content)
        
        print(f"✅ UI修复脚本已创建: {script_file}")
        return True
    
    def generate_ui_report(self):
        """生成UI修复报告"""
        print("📊 生成UI修复报告...")
        
        report = []
        report.append("=" * 60)
        report.append("📋 UI修复报告")
        report.append("=" * 60)
        
        # 检查模板文件
        template_files = [
            'app/templates/talent_management/hr_admin/feedback_dashboard.html',
            'app/templates/talent_management/employee_management/feedback_dashboard.html',
            'app/templates/talent_management/employee_management/send_feedback.html',
            'app/templates/talent_management/employee_management/sent_feedback.html'
        ]
        
        report.append("\n📁 模板文件检查:")
        for template_file in template_files:
            file_path = self.project_root / template_file
            if file_path.exists():
                report.append(f"   ✅ {template_file}")
            else:
                report.append(f"   ❌ {template_file} (缺失)")
        
        # 检查工具文件
        tool_files = [
            'talent_management_system/tools/ui_fix_script.js',
            'talent_management_system/tools/ui_fix_tool.py'
        ]
        
        report.append("\n🔧 工具文件检查:")
        for tool_file in tool_files:
            file_path = self.project_root / tool_file
            if file_path.exists():
                report.append(f"   ✅ {tool_file}")
            else:
                report.append(f"   ❌ {tool_file} (缺失)")
        
        report.append("\n🎯 修复项目:")
        report.append("   1. HR管理员仪表板侧边栏元素消失问题")
        report.append("   2. 员工反馈仪表板发送反馈功能")
        report.append("   3. CSS动画导致的元素不可见问题")
        report.append("   4. JavaScript修复脚本集成")
        
        report.append("\n" + "=" * 60)
        report.append("✅ UI修复报告生成完成")
        
        # 保存报告
        report_file = self.project_root / 'talent_management_system' / 'tools' / 'ui_fix_report.txt'
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report))
        
        print('\n'.join(report))
        print(f"\n📄 报告已保存: {report_file}")

def main():
    """主函数"""
    tool = UIFixTool()
    
    print("🔧 UI修复工具")
    print("=" * 50)
    
    while True:
        print("\n请选择操作:")
        print("1. 修复HR管理员仪表板")
        print("2. 修复员工反馈仪表板")
        print("3. 创建UI修复脚本")
        print("4. 生成UI修复报告")
        print("5. 执行所有修复")
        print("0. 退出")
        
        choice = input("\n请输入选择 (0-5): ").strip()
        
        if choice == '1':
            tool.fix_hr_admin_dashboard()
        elif choice == '2':
            tool.fix_employee_feedback_dashboard()
        elif choice == '3':
            tool.create_ui_fix_script()
        elif choice == '4':
            tool.generate_ui_report()
        elif choice == '5':
            print("\n🔄 执行所有UI修复...")
            tool.fix_hr_admin_dashboard()
            tool.fix_employee_feedback_dashboard()
            tool.create_ui_fix_script()
            tool.generate_ui_report()
            print("\n✅ 所有UI修复完成！")
        elif choice == '0':
            print("👋 再见！")
            break
        else:
            print("❌ 无效选择，请重新输入")

if __name__ == "__main__":
    main()
