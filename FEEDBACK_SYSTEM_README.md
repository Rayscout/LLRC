# 员工与高管联通反馈系统

## 系统概述

本反馈系统实现了员工与高管之间的双向沟通，支持高管向员工发送反馈，员工接收、查看和回复反馈的完整流程。

## 主要功能

### 高管端功能
1. **团队成员管理** - 查看和管理下属员工
2. **发送反馈** - 向员工发送技能发展、沟通协作、绩效表现等类型的反馈
3. **反馈历史** - 查看已发送的反馈记录和统计
4. **反馈模板** - 提供预设的反馈模板，提高反馈质量
5. **优先级管理** - 支持高、中、低优先级反馈

### 员工端功能
1. **接收反馈** - 查看来自高管和主管的反馈
2. **反馈详情** - 查看完整的反馈内容和发送者信息
3. **回复反馈** - 对收到的反馈进行回复和评价
4. **通知系统** - 实时接收新反馈通知
5. **反馈归档** - 管理已处理的反馈

## 数据库设计

### Feedback 表（反馈表）
```sql
CREATE TABLE feedback (
    id INTEGER PRIMARY KEY,
    sender_id INTEGER NOT NULL,           -- 发送者ID
    recipient_id INTEGER NOT NULL,        -- 接收者ID
    category VARCHAR(50) NOT NULL,        -- 反馈分类 (skill/communication/performance)
    feedback_type VARCHAR(50) NOT NULL,   -- 反馈类型 (positive/constructive/improvement)
    content TEXT NOT NULL,                -- 反馈内容
    priority VARCHAR(20) DEFAULT 'medium', -- 优先级 (high/medium/low)
    status VARCHAR(20) DEFAULT 'sent',    -- 状态 (sent/read/responded/archived)
    created_at DATETIME DEFAULT NOW(),    -- 创建时间
    read_at DATETIME,                     -- 阅读时间
    responded_at DATETIME                 -- 回复时间
);
```

### FeedbackNotification 表（反馈通知表）
```sql
CREATE TABLE feedback_notification (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,             -- 用户ID
    feedback_id INTEGER NOT NULL,         -- 反馈ID
    notification_type VARCHAR(50) NOT NULL, -- 通知类型
    title VARCHAR(200) NOT NULL,          -- 通知标题
    message TEXT NOT NULL,                -- 通知内容
    is_read BOOLEAN DEFAULT FALSE,        -- 是否已读
    created_at DATETIME DEFAULT NOW()     -- 创建时间
);
```

## 系统架构

### 路由结构
```
高管端路由：
/talent/hr_admin/feedback_system/dashboard          # 反馈系统仪表板
/talent/hr_admin/feedback_system/send_feedback      # 发送反馈
/talent/hr_admin/feedback_system/feedback_history   # 反馈历史

员工端路由：
/talent/employee_management/feedback/               # 反馈管理仪表板
/talent/employee_management/feedback/view/<id>      # 查看反馈详情
/talent/employee_management/feedback/respond/<id>   # 回复反馈
/talent/employee_management/feedback/archive/<id>   # 归档反馈
```

### API接口
```
GET  /api/team_members              # 获取团队成员列表
GET  /api/feedback_categories       # 获取反馈分类
GET  /api/feedback_templates/<cat>  # 获取反馈模板
GET  /api/feedback_stats           # 获取反馈统计
GET  /api/notifications            # 获取通知列表
POST /api/mark_read/<id>           # 标记通知已读
POST /api/mark_all_read            # 标记所有通知已读
```

## 使用流程

### 高管发送反馈流程
1. 登录高管账户
2. 进入"团队成员反馈"系统
3. 选择要发送反馈的员工
4. 选择反馈分类和类型
5. 填写反馈内容
6. 设置优先级
7. 发送反馈

### 员工接收反馈流程
1. 登录员工账户
2. 在反馈管理页面查看新反馈通知
3. 点击查看反馈详情
4. 阅读反馈内容
5. 可选择回复反馈
6. 归档已处理的反馈

## 权限控制

### 高管权限
- 可以查看所有员工（user_type = 'employee' 或 'supervisor'）
- 可以发送反馈给任何员工
- 可以查看自己发送的反馈历史

### 主管权限
- 只能查看自己的下属员工
- 可以发送反馈给下属
- 可以查看自己发送的反馈历史

### 员工权限
- 只能查看发给自己的反馈
- 可以回复收到的反馈
- 可以归档自己的反馈

## 反馈分类

### 技能发展 (skill)
- 专业技能提升建议
- 技术能力评估
- 学习成长指导

### 沟通协作 (communication)
- 团队合作表现
- 沟通表达技巧
- 人际关系建议

### 绩效表现 (performance)
- 工作成果评价
- 效率质量反馈
- 目标达成情况

## 反馈类型

### 正面反馈 (positive)
- 表扬优秀表现
- 肯定工作成果
- 鼓励继续努力

### 建设性反馈 (constructive)
- 提供改进建议
- 指出发展机会
- 设定发展目标

### 改进反馈 (improvement)
- 指出需要改进的地方
- 提供具体改进方案
- 设定改进时间表

## 优先级说明

### 高优先级 (high)
- 需要立即关注的问题
- 影响工作进度的重要事项
- 紧急的改进建议

### 中优先级 (medium)
- 一般性的反馈和建议
- 可以逐步改进的事项
- 常规的发展指导

### 低优先级 (low)
- 非紧急的建议
- 长期发展目标
- 一般性的鼓励

## 状态说明

### sent (已发送)
- 反馈已发送给员工
- 员工尚未查看

### read (已读)
- 员工已查看反馈
- 尚未回复

### responded (已回复)
- 员工已回复反馈
- 反馈流程完成

### archived (已归档)
- 反馈已归档
- 不再显示在活跃列表中

## 安装和部署

### 1. 数据库迁移
```bash
python add_feedback_tables.py
```

### 2. 测试系统
```bash
python test_feedback_system.py
```

### 3. 启动应用
```bash
python run.py
```

## 技术栈

- **后端**: Flask + SQLAlchemy
- **数据库**: SQLite/MySQL/PostgreSQL
- **前端**: HTML5 + CSS3 + JavaScript
- **UI框架**: 自定义iOS风格设计
- **通知**: 实时通知系统

## 扩展功能

### 计划中的功能
1. **反馈模板管理** - 允许高管创建自定义反馈模板
2. **反馈评分系统** - 员工对反馈质量进行评分
3. **反馈分析报告** - 生成反馈效果分析报告
4. **移动端支持** - 开发移动端应用
5. **邮件通知** - 集成邮件通知功能

### 可扩展的模块
1. **反馈标签系统** - 为反馈添加标签分类
2. **反馈搜索功能** - 支持按关键词搜索反馈
3. **反馈导出功能** - 支持导出反馈记录
4. **反馈统计图表** - 可视化反馈数据

## 注意事项

1. **数据安全** - 所有反馈数据都经过权限验证
2. **隐私保护** - 员工只能查看发给自己的反馈
3. **数据备份** - 建议定期备份反馈数据
4. **性能优化** - 大量数据时建议添加分页功能

## 故障排除

### 常见问题
1. **数据库连接失败** - 检查数据库配置
2. **权限验证失败** - 确认用户类型设置正确
3. **通知不显示** - 检查通知表是否正确创建

### 日志查看
系统会在控制台输出详细的日志信息，包括：
- 数据库操作日志
- 用户操作日志
- 错误信息日志

## 联系支持

如有问题或建议，请联系开发团队。
