# 人才管理系统 - 反馈系统

## 📋 系统概述

人才管理系统的反馈模块是一个完整的双向反馈系统，支持员工向高管发送反馈，以及高管向员工发送反馈。系统提供了丰富的功能，包括反馈发送、接收、查看、回复等。

## 🏗️ 系统架构

### 目录结构
```
talent_management_system/
├── hr_admin_module/           # HR管理员模块
│   ├── feedback_system.py     # 反馈系统后端
│   └── ...
├── employee_manager_module/   # 员工管理模块
│   ├── feedback.py           # 员工反馈功能
│   └── ...
├── tools/                    # 工具模块
│   ├── database_migration.py # 数据库迁移工具
│   ├── feedback_test_tool.py # 反馈测试工具
│   ├── ui_fix_tool.py        # UI修复工具
│   └── ...
└── templates/                # 模板文件
    ├── hr_admin/             # HR管理员模板
    └── employee_management/  # 员工管理模板
```

## 🚀 快速开始

### 1. 环境准备
```bash
# 安装依赖
pip install -r requirements.txt

# 设置环境变量
export FLASK_APP=run_app.py
export FLASK_ENV=development
```

### 2. 数据库迁移
```bash
# 使用启动脚本
python start_talent_management.py

# 选择选项 1: 数据库迁移
```

### 3. 启动系统
```bash
# 使用启动脚本
python start_talent_management.py

# 选择选项 5: 完整启动流程
```

## 📊 功能特性

### 员工反馈功能
- ✅ 发送反馈给高管
- ✅ 查看已发送的反馈
- ✅ 查看接收到的反馈
- ✅ 回复反馈
- ✅ 反馈状态跟踪

### 高管反馈功能
- ✅ 发送反馈给员工
- ✅ 查看员工发送的反馈
- ✅ 查看已发送的反馈
- ✅ 反馈统计和分析
- ✅ 团队管理

### 系统功能
- ✅ 反馈分类管理
- ✅ 优先级设置
- ✅ 状态跟踪
- ✅ 通知系统
- ✅ 数据统计

## 🛠️ 工具模块

### 数据库迁移工具 (`tools/database_migration.py`)
```python
from talent_management_system.tools.database_migration import DatabaseMigrationTool

tool = DatabaseMigrationTool()
tool.check_database_structure()      # 检查数据库结构
tool.migrate_feedback_table()        # 迁移反馈表
tool.create_test_feedback_data()     # 创建测试数据
tool.check_feedback_data()           # 检查反馈数据
```

### 反馈测试工具 (`tools/feedback_test_tool.py`)
```python
from talent_management_system.tools.feedback_test_tool import FeedbackTestTool

tool = FeedbackTestTool()
tool.test_feedback_system()          # 测试反馈系统
tool.test_employee_feedback()        # 测试员工反馈
tool.test_executive_feedback()       # 测试高管反馈
tool.generate_test_report()          # 生成测试报告
```

### UI修复工具 (`tools/ui_fix_tool.py`)
```python
from talent_management_system.tools.ui_fix_tool import UIFixTool

tool = UIFixTool()
tool.fix_hr_admin_dashboard()        # 修复HR管理员仪表板
tool.fix_employee_feedback_dashboard() # 修复员工反馈仪表板
tool.create_ui_fix_script()          # 创建UI修复脚本
tool.generate_ui_report()            # 生成UI修复报告
```

## 📝 API接口

### 员工反馈接口
- `GET /talent/employee_management/feedback/` - 反馈仪表板
- `GET /talent/employee_management/feedback/send` - 发送反馈页面
- `POST /talent/employee_management/feedback/send` - 发送反馈
- `GET /talent/employee_management/feedback/sent` - 已发送反馈
- `GET /talent/employee_management/feedback/view/<id>` - 查看反馈详情
- `GET /talent/employee_management/feedback/respond/<id>` - 回复反馈页面
- `POST /talent/employee_management/feedback/respond/<id>` - 回复反馈

### 高管反馈接口
- `GET /talent/hr_admin/feedback_system/dashboard` - 反馈系统仪表板
- `GET /talent/hr_admin/feedback_system/send_feedback` - 发送反馈页面
- `POST /talent/hr_admin/feedback_system/send_feedback` - 发送反馈
- `GET /talent/hr_admin/feedback_system/feedback_history` - 反馈历史

## 🗄️ 数据库模型

### Feedback 模型
```python
class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category = db.Column(db.String(50), nullable=False)  # skill, communication, performance, general
    feedback_type = db.Column(db.String(50), nullable=False)  # positive, constructive, improvement, request
    content = db.Column(db.Text, nullable=False)
    priority = db.Column(db.String(20), default='medium')  # high, medium, low
    status = db.Column(db.String(20), default='sent')  # sent, read, responded, archived
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    read_at = db.Column(db.DateTime)
    responded_at = db.Column(db.DateTime)
    response_content = db.Column(db.Text)
    response_rating = db.Column(db.Integer)
```

## 🎨 UI组件

### 反馈卡片组件
```html
<div class="feedback-item">
    <div class="feedback-icon {{ feedback.category }}">
        <!-- 分类图标 -->
    </div>
    <div class="feedback-content">
        <div class="feedback-recipient">
            <!-- 发送/接收信息 -->
        </div>
        <div class="feedback-text">
            <!-- 反馈内容 -->
        </div>
    </div>
    <div class="feedback-meta">
        <!-- 时间、优先级、状态 -->
    </div>
</div>
```

### 统计卡片组件
```html
<div class="header-stat">
    <div class="header-stat-number">{{ total_feedback }}</div>
    <div class="header-stat-label">总反馈数</div>
</div>
```

## 🔧 配置选项

### 反馈分类配置
```python
FEEDBACK_CATEGORIES = {
    'skill': {
        'name': '技能发展',
        'icon': '🚀',
        'description': '专业技能、技术能力、学习成长'
    },
    'communication': {
        'name': '沟通协作',
        'icon': '💬',
        'description': '团队合作、沟通表达、人际关系'
    },
    'performance': {
        'name': '绩效表现',
        'icon': '📈',
        'description': '工作成果、效率质量、目标达成'
    },
    'general': {
        'name': '一般反馈',
        'icon': '📝',
        'description': '其他建议和意见'
    }
}
```

### 反馈类型配置
```python
FEEDBACK_TYPES = {
    'positive': '正面反馈',
    'constructive': '建设性反馈',
    'improvement': '改进建议',
    'request': '请求和建议'
}
```

## 🧪 测试

### 运行测试
```bash
# 使用测试工具
python talent_management_system/tools/feedback_test_tool.py

# 或使用启动脚本
python start_talent_management.py
# 选择选项 2: 系统测试
```

### 测试覆盖
- ✅ 数据库连接测试
- ✅ 用户认证测试
- ✅ 反馈创建测试
- ✅ 反馈查询测试
- ✅ 反馈状态更新测试
- ✅ UI组件测试

## 🐛 故障排除

### 常见问题

#### 1. 侧边栏元素消失
**问题**: HR管理员仪表板中"快速操作"和"反馈分类"元素消失
**解决方案**: 运行UI修复工具
```bash
python talent_management_system/tools/ui_fix_tool.py
```

#### 2. 数据库连接错误
**问题**: 无法连接到数据库
**解决方案**: 检查数据库文件是否存在
```bash
python talent_management_system/tools/database_migration.py
```

#### 3. 反馈数据不显示
**问题**: 高管看不到员工发送的反馈
**解决方案**: 检查反馈查询逻辑和数据库数据
```bash
python talent_management_system/tools/feedback_test_tool.py
```

### 日志查看
```bash
# 查看应用日志
tail -f app.log

# 查看Flask日志
export FLASK_DEBUG=1
```

## 📈 性能优化

### 数据库优化
- 为 `sender_id` 和 `recipient_id` 添加索引
- 为 `created_at` 添加索引以优化时间查询
- 定期清理过期数据

### 前端优化
- 使用懒加载减少初始加载时间
- 实现分页显示大量反馈数据
- 使用缓存减少重复请求

## 🔒 安全考虑

### 权限控制
- 用户只能查看自己发送和接收的反馈
- 高管可以查看团队成员的反馈
- 敏感操作需要二次确认

### 数据验证
- 输入内容长度限制
- XSS防护
- SQL注入防护

## 📞 支持

### 联系方式
- 项目维护者: [维护者姓名]
- 邮箱: [邮箱地址]
- 问题反馈: [GitHub Issues链接]

### 文档更新
- 最后更新: 2025年8月26日
- 版本: 1.0.0
- 状态: 生产就绪

---

**注意**: 本系统仅供内部使用，请勿在生产环境中直接部署，建议根据实际需求进行定制化开发。
