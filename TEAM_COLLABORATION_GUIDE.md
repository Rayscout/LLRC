# 团队协作开发指南

## 项目架构概述

本项目采用模块化架构设计，分为两个主要系统：

### 1. 智能招聘系统 (SmartRecruit System)
- **组A（HR功能）**：负责 `smartrecruit_system/hr_module/` 下的所有功能
- **组B（Candidate功能）**：负责 `smartrecruit_system/candidate_module/` 下的所有功能

### 2. 人才管理系统 (Talent Management System)
- **组C（HR管理功能）**：负责 `talent_management_system/hr_admin_module/` 下的所有功能
- **组D（员工/经理功能）**：负责 `talent_management_system/employee_manager_module/` 下的所有功能

## Git分支策略

### 分支结构
```
main (主分支)
├── develop (开发分支)
│   ├── smartrecruit/                     # 招聘系统分支
│   │   ├── hr/                           # HR功能分支
│   │   └── candidate/                    # 求职者功能分支
│   └── talent_management/                # 人才系统分支
│       ├── hr_admin/                     # HR管理功能分支
│       └── employee_manager/             # 员工/经理功能分支
```

### 团队分工和分支管理

#### 团队A（智能招聘系统 - HR功能）
- **负责模块**：`smartrecruit_system/hr_module/`
- **开发分支**：从 `hr/` 分支创建个人功能分支
- **工作流程**：
  1. 从 `hr/` 分支创建功能分支：`team-a-[功能名]-feature`
  2. 在 `hr_module/` 目录下开发
  3. 提交PR到 `hr/` 分支
  4. 组内代码审查和合并

#### 团队B（智能招聘系统 - Candidate功能）
- **负责模块**：`smartrecruit_system/candidate_module/`
- **开发分支**：从 `candidate/` 分支创建个人功能分支
- **工作流程**：
  1. 从 `candidate/` 分支创建功能分支：`team-b-[功能名]-feature`
  2. 在 `candidate_module/` 目录下开发
  3. 提交PR到 `candidate/` 分支
  4. 组内代码审查和合并

#### 团队C（人才管理系统 - HR管理功能）
- **负责模块**：`talent_management_system/hr_admin_module/`
- **开发分支**：从 `hr_admin/` 分支创建个人功能分支
- **工作流程**：
  1. 从 `hr_admin/` 分支创建功能分支：`team-c-[功能名]-feature`
  2. 在 `hr_admin_module/` 目录下开发
  3. 提交PR到 `hr_admin/` 分支
  4. 组内代码审查和合并

#### 团队D（人才管理系统 - 员工/经理功能）
- **负责模块**：`talent_management_system/employee_manager_module/`
- **开发分支**：从 `employee_manager/` 分支创建个人功能分支
- **工作流程**：
  1. 从 `employee_manager/` 分支创建功能分支：`team-d-[功能名]-feature`
  2. 在 `employee_manager_module/` 目录下开发
  3. 提交PR到 `employee_manager/` 分支
  4. 组内代码审查和合并

## 开发流程

### 第一层：组内协作
1. 每个同学从对应的团队分支创建个人功能分支
2. 在指定模块目录下开发功能
3. 提交代码到个人功能分支
4. 创建PR到团队分支
5. 组内代码审查和合并

### 第二层：系统内协作
1. 组A和组B分别完成HR和Candidate功能后
2. 组A提交PR到 `smartrecruit/` 分支
3. 组B提交PR到 `smartrecruit/` 分支
4. 系统内代码审查和合并

### 第三层：总项目合并
1. 招聘系统完成集成后，提交PR到 `develop` 分支
2. 人才系统完成集成后，提交PR到 `develop` 分支
3. 总项目代码审查和合并
4. 最终合并到 `main` 分支

## 代码提交规范

### 提交信息格式
```
格式：type(scope): 简短描述

示例：
feat(hr): 添加HR仪表盘统计功能
fix(candidate): 修复职位搜索分页问题
docs(talent): 更新人才管理API文档
style(hr_admin): 统一代码格式
refactor(employee_manager): 重构绩效评估模块
test(recruitment): 添加招聘流程测试用例
```

### 类型说明
- `feat`: 新功能
- `fix`: 修复bug
- `docs`: 文档更新
- `style`: 代码格式调整
- `refactor`: 代码重构
- `test`: 测试相关
- `chore`: 构建过程或辅助工具的变动

## 代码审查清单

### 功能完整性
- [ ] 功能是否按需求完整实现
- [ ] 是否有遗漏的边界情况
- [ ] 错误处理是否完善

### 代码质量
- [ ] 代码结构是否清晰
- [ ] 命名是否规范
- [ ] 是否有重复代码
- [ ] 性能是否合理

### 安全性
- [ ] 是否有SQL注入风险
- [ ] 是否有XSS风险
- [ ] 权限控制是否合理
- [ ] 输入验证是否完善

### 测试覆盖
- [ ] 是否有单元测试
- [ ] 测试用例是否覆盖主要功能
- [ ] 异常情况是否有测试

## 注意事项

### 1. 模块边界
- 只在自己负责的模块下开发
- 不要修改其他团队的代码
- 共享功能放在 `app/common/` 目录

### 2. 依赖管理
- 新增依赖需要更新 `requirements.txt`
- 避免引入不必要的依赖包
- 版本兼容性要仔细检查

### 3. 数据库操作
- 新增数据模型需要创建迁移文件
- 数据库操作要有异常处理
- 避免N+1查询问题

### 4. 前端模板
- 模板文件放在对应的 `templates/` 目录
- 静态资源放在对应的 `static/` 目录
- 保持模板结构清晰

## 常见问题解决

### 1. 分支冲突
```bash
# 解决冲突步骤
git checkout develop
git pull origin develop
git checkout your-feature-branch
git merge develop
# 解决冲突后
git add .
git commit -m "resolve: 解决与develop分支的冲突"
git push origin your-feature-branch
```

### 2. 模块导入问题
```python
# 正确的导入方式
from ...models import User, Job, Application, db
from ...utils import helper_function
from ...config import Config
```

### 3. 蓝图注册问题
```python
# 确保蓝图正确注册
from .module_name import module_bp
main_bp.register_blueprint(module_bp)
```

## 联系信息

如有问题，请联系：
- 项目负责人：[姓名]
- 技术负责人：[姓名]
- 各团队负责人：[姓名]

## 更新日志

- 2024-08-21: 创建团队协作开发指南
- 2024-08-21: 完成项目架构重构
- 2024-08-21: 配置GitHub自动合并工作流
