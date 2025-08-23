# 人才管理系统 - 主管和员工功能

## 概述

本系统在原有的求职者和招聘者（HR）功能基础上，新增了主管和员工角色，实现了完整的人才管理功能。

## 新增功能

### 1. 主管功能
- **团队管理**: 管理下属员工信息、分配任务、监控工作进度
- **绩效监控**: 实时监控团队绩效、KPI达成情况、提供反馈
- **发展规划**: 制定团队发展计划、培训安排、职业规划指导

### 2. 员工功能
- **个人档案**: 管理个人信息、技能证书、工作经历等档案信息
- **绩效跟踪**: 查看个人绩效表现、KPI达成情况、获得反馈
- **培训发展**: 参与培训课程、技能提升、职业发展规划

## 系统架构

### 文件结构
```
LLRC/
├── app/
│   ├── templates/
│   │   └── talent_management/
│   │       ├── hr_admin/
│   │       │   ├── supervisor_auth.html      # 主管登录注册界面
│   │       │   └── supervisor_dashboard.html # 主管仪表盘
│   │       └── employee_management/
│   │           ├── employee_auth.html        # 员工登录注册界面
│   │           └── employee_dashboard.html   # 员工仪表盘
│   ├── models.py                             # 用户模型（已更新）
│   └── common/
│       └── auth.py                           # 认证逻辑（已更新）
├── talent_management_system/
│   ├── hr_admin_module/
│   │   └── supervisor_auth.py                # 主管认证后端
│   ├── employee_manager_module/
│   │   └── employee_auth.py                  # 员工认证后端
│   └── routes.py                             # 路由配置（已更新）
└── test_talent_management.py                 # 测试脚本
```

### 数据库模型更新

在原有的 `User` 模型中新增了以下字段：

```python
class User(db.Model):
    # ... 原有字段 ...
    
    # 新增字段支持主管和员工
    user_type = db.Column(db.String(20), default='candidate')  # candidate, recruiter, supervisor, employee
    department = db.Column(db.String(100))  # 部门
    supervisor_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 主管ID
    hire_date = db.Column(db.Date)  # 入职日期
    employee_id = db.Column(db.String(50))  # 员工编号
    
    # 关系
    supervisor = db.relationship('User', remote_side=[id], backref=db.backref('subordinates', lazy=True))
```

## 使用方法

### 1. 主管注册和登录

#### 注册流程
1. 访问主登录页面
2. 选择"主管"身份
3. 填写基本信息：
   - 姓名、公司名称、部门、职位
   - 邮箱、手机号、生日
   - 密码和确认密码
4. 提交注册

#### 登录流程
1. 选择"主管"身份
2. 输入邮箱和密码
3. 登录成功后进入主管仪表盘

### 2. 员工注册和登录

#### 注册流程
1. 访问主登录页面
2. 选择"员工"身份
3. 填写所有必填信息：
   - 基本信息：姓名、公司名称、部门、职位
   - 员工信息：员工编号、主管邮箱、入职日期
   - 联系信息：邮箱、手机号、生日
   - 密码和确认密码
4. 提交注册（系统会自动验证主管邮箱）

#### 登录流程
1. 选择"员工"身份
2. 输入邮箱和密码
3. 登录成功后进入员工仪表盘

### 3. 访问路径

- **主管认证**: `/talent/supervisor/auth`
- **主管仪表盘**: `/talent/supervisor/dashboard`
- **员工认证**: `/talent/employee/auth`
- **员工仪表盘**: `/talent/employee/dashboard`

## 技术特性

### 1. 动态表单
- 根据选择的角色动态显示/隐藏相关字段
- 自动设置必填字段验证
- 实时表单验证

### 2. 角色权限管理
- 基于用户类型的访问控制
- 自动重定向到对应的仪表盘
- 会话管理增强

### 3. 数据关联
- 员工自动关联到指定主管
- 主管可以查看下属员工列表
- 支持团队层级结构

## 测试

运行测试脚本验证系统配置：

```bash
cd LLRC
python test_talent_management.py
```

测试内容包括：
- 数据库模型验证
- 蓝图注册检查
- 路由配置验证

## 注意事项

1. **主管注册**: 主管必须先注册，员工才能关联到主管
2. **员工编号**: 员工编号必须唯一，不能重复
3. **主管邮箱**: 员工注册时必须提供有效的主管邮箱
4. **数据库迁移**: 如果使用现有数据库，需要运行数据库迁移以添加新字段

## 扩展功能

系统设计支持以下扩展：
- 绩效评估模块
- 培训管理模块
- 任务分配系统
- 团队协作功能
- 报表和分析

## 技术支持

如有问题，请联系：
- 技术支持: support@ll-talent.cn
- 电话: +86 138 0000 0000

---

© 2025 林理人才开发团队（北京林业大学）. 保留所有权利.
