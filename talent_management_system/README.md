# 人才管理系统 (Talent Management System)

## 系统概述

人才管理系统是一个综合的员工管理平台，提供员工全生命周期的管理功能，包括个人资料管理、绩效评估、学习发展、项目管理、薪酬管理等。

## 系统架构

```
talent_management_system/
├── __init__.py                 # 系统初始化
├── routes.py                   # 主路由配置
├── models.py                   # 数据模型定义
├── tools.py                    # 系统工具脚本
├── README.md                   # 系统文档
├── hr_admin_module/            # HR管理模块
│   ├── __init__.py
│   ├── routes.py
│   ├── dashboard.py            # 高管仪表板
│   ├── employees.py            # 员工管理
│   ├── departments.py          # 部门管理
│   ├── career_tracking.py      # 职业发展跟踪
│   ├── feedback_system.py      # 反馈系统
│   ├── org_health.py           # 组织健康度
│   ├── pdf_report.py           # PDF报告生成
│   ├── salary_analysis.py      # 薪酬分析
│   ├── turnover_alert.py       # 离职预警
│   └── executive_auth.py       # 高管认证
└── employee_manager_module/    # 员工管理模块
    ├── __init__.py
    ├── employee_auth.py        # 员工认证
    ├── profile.py              # 个人资料管理
    ├── performance.py          # 绩效管理
    ├── projects.py             # 项目管理
    ├── learning_recommendation.py  # 学习推荐
    ├── smart_goals.py          # 智能目标
    ├── compensation.py         # 薪酬管理
    ├── feedback.py             # 反馈管理
    ├── status_check.py         # 状态检查工具
    └── debug_tools.py          # 调试工具
```

## 功能模块

### 1. HR管理模块 (hr_admin_module)

#### 高管仪表板
- 组织概览和关键指标
- 员工分布统计
- 绩效趋势分析
- 离职率监控

#### 员工管理
- 员工信息管理
- 组织架构管理
- 职位管理
- 员工状态跟踪

#### 职业发展跟踪
- 职业路径规划
- 技能评估
- 发展计划制定
- 晋升管理

#### 反馈系统
- 360度反馈
- 绩效评估
- 员工满意度调查
- 反馈分析报告

#### 组织健康度
- 组织氛围评估
- 团队效能分析
- 文化契合度
- 健康度报告

#### 薪酬分析
- 薪酬结构分析
- 市场对标
- 薪酬建议
- 预算规划

#### 离职预警
- 离职风险预测
- 预警指标监控
- 干预措施建议
- 保留策略制定

### 2. 员工管理模块 (employee_manager_module)

#### 个人资料管理
- 基本信息维护
- 技能档案管理
- 教育背景记录
- 工作经验管理

#### 绩效管理
- 绩效目标设定
- 绩效评估记录
- 绩效反馈
- 绩效报告

#### 项目管理
- 项目参与记录
- 项目贡献评估
- 项目经验总结
- 项目技能展示

#### 学习推荐
- 个性化学习路径
- 技能差距分析
- 课程推荐
- 学习进度跟踪

#### 智能目标
- 目标设定
- 进度跟踪
- 目标调整
- 完成度评估

#### 薪酬管理
- 薪酬信息查看
- 薪酬历史记录
- 薪酬调整申请
- 薪酬报告

#### 反馈管理
- 反馈接收
- 反馈回应
- 反馈历史
- 改进计划

## 数据模型

### 核心模型

1. **Employee** - 员工信息
2. **Performance** - 绩效记录
3. **Project** - 项目信息
4. **EmployeeProject** - 员工项目关联
5. **LearningPath** - 学习路径
6. **Course** - 课程信息
7. **EmployeeCourse** - 员工课程关联
8. **Feedback** - 反馈记录
9. **Goal** - 目标管理
10. **Compensation** - 薪酬记录

## 使用方法

### 1. 启动系统工具

```bash
cd talent_management_system
python tools.py
```

### 2. 运行特定功能

```python
# 员工界面状态检查
from employee_manager_module.status_check import employee_interface_status
employee_interface_status()

# 员工错误调试
from employee_manager_module.debug_tools import debug_employee_errors
debug_employee_errors()

# 员工路由调试
from employee_manager_module.debug_tools import debug_employee_routes
debug_employee_routes()

# 员工认证调试
from employee_manager_module.debug_tools import debug_employee_auth
debug_employee_auth()
```

### 3. 访问系统页面

#### HR管理员页面
- 高管仪表板: `/talent/hr_admin/dashboard`
- 员工管理: `/talent/hr_admin/employees`
- 部门管理: `/talent/hr_admin/departments`
- 职业跟踪: `/talent/hr_admin/career_tracking`
- 反馈系统: `/talent/hr_admin/feedback_system`
- 组织健康: `/talent/hr_admin/org_health`
- 薪酬分析: `/talent/hr_admin/salary_analysis`
- 离职预警: `/talent/hr_admin/turnover_alert`

#### 员工页面
- 员工仪表板: `/talent/employee_management/employee_dashboard`
- 个人资料: `/talent/employee_manager/profile`
- 绩效管理: `/talent/employee_manager/performance`
- 项目管理: `/talent/employee_manager/projects`
- 学习推荐: `/talent/employee_manager/learning_recommendation`
- 智能目标: `/talent/employee_manager/smart_goals`
- 薪酬管理: `/talent/employee_manager/compensation`
- 反馈管理: `/talent/employee_manager/feedback`

## 技术特性

### 1. 模块化设计
- 清晰的模块分离
- 独立的功能单元
- 易于维护和扩展

### 2. 数据完整性
- 完整的数据模型
- 关系约束
- 数据验证

### 3. 用户体验
- iOS风格界面
- 响应式设计
- 流畅动画效果

### 4. 调试支持
- 完整的调试工具
- 状态检查功能
- 错误诊断

## 开发指南

### 1. 添加新功能
1. 在对应模块中创建新文件
2. 定义路由和视图函数
3. 更新模块的__init__.py
4. 在主routes.py中注册蓝图

### 2. 数据模型扩展
1. 在models.py中添加新模型
2. 定义字段和关系
3. 运行数据库迁移
4. 更新相关视图

### 3. 调试和测试
1. 使用tools.py进行系统检查
2. 运行特定调试功能
3. 检查路由和认证
4. 验证数据完整性

## 注意事项

1. **权限控制**: 确保用户只能访问其权限范围内的功能
2. **数据安全**: 敏感信息需要加密存储
3. **性能优化**: 大量数据查询需要分页处理
4. **用户体验**: 保持界面的一致性和易用性
5. **错误处理**: 提供友好的错误提示和恢复机制

## 更新日志

### v1.0.0 (当前版本)
- ✅ 完成基础架构搭建
- ✅ 实现员工管理模块
- ✅ 实现HR管理模块
- ✅ 添加调试和状态检查工具
- ✅ 完善数据模型定义
- ✅ 优化代码组织结构
