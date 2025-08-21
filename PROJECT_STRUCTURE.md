# 项目结构说明

## 目录结构

```
Code/SmartRecruit_LLM/
├── smartrecruit_system/                  # 智能招聘系统
│   ├── hr_module/                        # HR功能模块（团队A负责）
│   │   ├── __init__.py                   # HR模块初始化
│   │   ├── routes.py                     # HR模块路由整合
│   │   ├── dashboard.py                  # HR仪表盘功能
│   │   ├── recruitment.py                # HR招聘功能
│   │   └── candidates.py                 # HR候选人管理功能
│   ├── candidate_module/                 # 求职者功能模块（团队B负责）
│   │   ├── __init__.py                   # 求职者模块初始化
│   │   ├── routes.py                     # 求职者模块路由整合
│   │   ├── profile.py                    # 个人信息管理功能
│   │   ├── jobs.py                       # 职位浏览和搜索功能
│   │   └── applications.py               # 申请和面试功能
│   ├── __init__.py                       # 招聘系统主蓝图
│   ├── routes.py                         # 招聘系统路由整合
│   └── models.py                         # 招聘系统数据模型
├── talent_management_system/             # 人才管理系统
│   ├── hr_admin_module/                  # HR管理功能（团队C负责）
│   │   ├── __init__.py                   # HR管理模块初始化
│   │   ├── routes.py                     # HR管理模块路由整合
│   │   ├── dashboard.py                  # HR管理仪表盘功能
│   │   ├── employees.py                  # 员工管理功能
│   │   └── departments.py                # 部门管理功能
│   ├── employee_manager_module/          # 员工/经理功能（团队D负责）
│   │   ├── __init__.py                   # 员工/经理模块初始化
│   │   ├── routes.py                     # 员工/经理模块路由整合
│   │   ├── profile.py                    # 个人信息管理功能
│   │   ├── performance.py                # 绩效管理功能
│   │   └── projects.py                   # 项目管理功能
│   ├── __init__.py                       # 人才系统主蓝图
│   ├── routes.py                         # 人才系统路由整合
│   └── models.py                         # 人才系统数据模型
├── app/                                   # 主应用
│   ├── __init__.py                       # 主应用初始化
│   ├── common/                           # 通用功能（共享）
│   │   ├── __init__.py                   # 通用模块初始化
│   │   ├── routes.py                     # 通用模块路由整合
│   │   ├── auth.py                       # 统一认证功能
│   │   ├── files.py                      # 文件处理功能
│   │   └── utils.py                      # 共享工具函数
│   ├── models.py                         # 统一数据模型
│   ├── config.py                         # 统一配置
│   ├── templates/                        # 模板文件
│   └── static/                           # 静态文件
├── .github/                               # GitHub配置
│   └── workflows/                        # GitHub Actions工作流
│       ├── team-merge.yml                # 团队自动合并
│       ├── system-merge.yml              # 系统自动合并
│       └── main-merge.yml                # 总项目自动合并
├── requirements.txt                       # 统一依赖
├── run.py                                # 主启动文件
├── TEAM_COLLABORATION_GUIDE.md           # 团队协作开发指南
├── PROJECT_STRUCTURE.md                  # 项目结构说明（本文件）
└── README.md                             # 项目说明
```

## 模块说明

### 智能招聘系统 (SmartRecruit System)

#### HR功能模块 (团队A负责)
- **dashboard.py**: HR仪表盘，显示招聘统计、候选人信息等
- **recruitment.py**: 招聘管理，包括职位发布、编辑、删除等
- **candidates.py**: 候选人管理，包括查看申请、安排面试等

#### 求职者功能模块 (团队B负责)
- **profile.py**: 个人信息管理，包括基本信息、简历上传等
- **jobs.py**: 职位浏览和搜索，包括职位列表、详情、智能推荐等
- **applications.py**: 申请和面试，包括职位申请、AI面试、结果查看等

### 人才管理系统 (Talent Management System)

#### HR管理功能 (团队C负责)
- **dashboard.py**: HR管理仪表盘，显示员工统计、部门信息等
- **employees.py**: 员工管理，包括员工信息、入职离职、档案管理等
- **departments.py**: 部门管理，包括部门结构、人员配置等

#### 员工/经理功能 (团队D负责)
- **profile.py**: 个人信息管理，包括基本信息、技能证书等
- **performance.py**: 绩效管理，包括绩效评估、目标设定、反馈等
- **projects.py**: 项目管理，包括项目分配、进度跟踪、成果展示等

## 蓝图注册结构

### 主应用蓝图注册
```python
# app/__init__.py
from .common.routes import common_bp
from ..smartrecruit_system.routes import smartrecruit_bp
from ..talent_management_system.routes import talent_management_bp

app.register_blueprint(common_bp)
app.register_blueprint(smartrecruit_bp)
app.register_blueprint(talent_management_bp)
```

### 系统级蓝图注册
```python
# smartrecruit_system/routes.py
from .hr_module import hr_bp
from .candidate_module import candidate_bp

smartrecruit_bp.register_blueprint(hr_bp)
smartrecruit_bp.register_blueprint(candidate_bp)
```

### 模块级蓝图注册
```python
# smartrecruit_system/hr_module/routes.py
from .dashboard import dashboard_bp
from .recruitment import recruitment_bp
from .candidates import candidates_bp

hr_bp.register_blueprint(dashboard_bp)
hr_bp.register_blueprint(recruitment_bp)
hr_bp.register_blueprint(candidates_bp)
```

## URL路径结构

### 智能招聘系统
```
/smartrecruit/hr/dashboard/                # HR仪表盘
/smartrecruit/hr/recruitment/              # HR招聘管理
/smartrecruit/hr/candidates/               # HR候选人管理
/smartrecruit/candidate/profile/           # 求职者个人信息
/smartrecruit/candidate/jobs/              # 求职者职位浏览
/smartrecruit/candidate/applications/      # 求职者申请管理
```

### 人才管理系统
```
/talent/hr_admin/dashboard/                # HR管理仪表盘
/talent/hr_admin/employees/                # HR员工管理
/talent/hr_admin/departments/              # HR部门管理
/talent/employee_manager/profile/          # 员工/经理个人信息
/talent/employee_manager/performance/      # 员工/经理绩效管理
/talent/employee_manager/projects/         # 员工/经理项目管理
```

### 通用功能
```
/                                           # 主页
/sign                                       # 登录注册
/download                                   # 文件下载
/video                                      # 视频预览
/photo                                      # 头像显示
```

## 数据模型结构

### 统一数据模型 (app/models.py)
- **User**: 用户模型，包含所有用户的基本信息
- **Job**: 职位模型，包含招聘职位的所有信息
- **Application**: 申请模型，包含求职申请的所有信息

### 系统特定模型
- **smartrecruit_system/models.py**: 招聘系统特定的数据模型
- **talent_management_system/models.py**: 人才系统特定的数据模型

## 模板文件结构

### 模板目录组织
```
templates/
├── common/                                # 通用模板
│   ├── base.html                         # 基础模板
│   └── sign.html                         # 登录注册模板
├── smartrecruit/                         # 招聘系统模板
│   ├── hr/                               # HR功能模板
│   │   ├── dashboard.html                # HR仪表盘
│   │   ├── recruitment.html              # 招聘管理
│   │   └── candidates.html               # 候选人管理
│   └── candidate/                        # 求职者功能模板
│       ├── profile.html                  # 个人信息
│       ├── jobs.html                     # 职位浏览
│       └── applications.html             # 申请管理
└── talent_management/                    # 人才系统模板
    ├── hr_admin/                         # HR管理模板
    │   ├── dashboard.html                # HR管理仪表盘
    │   ├── employees.html                # 员工管理
    │   └── departments.html              # 部门管理
    └── employee_manager/                 # 员工/经理模板
        ├── profile.html                  # 个人信息
        ├── performance.html              # 绩效管理
        └── projects.html                 # 项目管理
```

## 静态文件结构

### 静态资源组织
```
static/
├── common/                                # 通用静态资源
│   ├── css/                              # 通用样式
│   ├── js/                               # 通用脚本
│   └── images/                           # 通用图片
├── smartrecruit/                         # 招聘系统静态资源
│   ├── hr/                               # HR功能静态资源
│   └── candidate/                        # 求职者功能静态资源
└── talent_management/                    # 人才系统静态资源
    ├── hr_admin/                         # HR管理静态资源
    └── employee_manager/                 # 员工/经理静态资源
```

## 开发注意事项

### 1. 模块边界
- 每个团队只在自己负责的模块下开发
- 不要修改其他团队的代码
- 共享功能放在 `app/common/` 目录

### 2. 导入路径
- 使用相对导入：`from ...models import User, Job, Application, db`
- 避免循环导入问题
- 保持导入路径的一致性

### 3. 蓝图命名
- 每个蓝图都有唯一的名称
- 避免蓝图名称冲突
- 使用描述性的蓝图名称

### 4. 路由设计
- 路由路径要清晰明确
- 避免路径冲突
- 使用RESTful风格的API设计

## 部署说明

### 开发环境
```bash
# 安装依赖
pip install -r requirements.txt

# 运行应用
python run.py
```

### 生产环境
```bash
# 使用生产级WSGI服务器
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

## 更新日志

- 2024-08-21: 创建项目结构说明文档
- 2024-08-21: 完成项目架构重构
- 2024-08-21: 建立模块化开发结构
