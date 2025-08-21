# 代码重构说明

## 重构目标
将原来的单一 `routes.py` 文件按角色和功能模块进行分离，提高代码的可维护性和可读性。

## 新的代码结构

### 1. 按角色分离
```
app/
├── candidate/          # 求职者相关功能
├── hr/                # HR相关功能  
└── common/            # 通用功能
```

### 2. 按功能模块进一步分离

#### 求职者模块 (`candidate/`)
- `profile.py` - 个人信息管理（设置、简历上传、头像上传）
- `jobs.py` - 职位浏览和搜索（职位列表、详情、智能搜索、推荐）
- `applications.py` - 申请和面试（申请职位、AI面试、查看申请）

#### HR模块 (`hr/`)
- `dashboard.py` - HR仪表盘（统计、候选人管理、面试安排、报告、洞察）
- `jobs.py` - 职位管理（发布招聘、编辑职位、查看应聘者、面试详情）

#### 通用模块 (`common/`)
- `auth.py` - 认证功能（登录、注册、退出、主页重定向）
- `files.py` - 文件处理（下载、视频预览、头像显示）

### 3. 蓝图注册结构
```
common_bp (/)           # 根路径，包含认证和文件
├── auth_bp (/sign, /logout, /)
└── files_bp (/download, /video, /photo, /debug)

candidate_bp (/candidate)  # 求职者功能
├── profile_bp (/candidate/profile)
├── jobs_bp (/candidate/jobs)
└── applications_bp (/candidate/applications)

hr_bp (/hr)            # HR功能
├── dashboard_bp (/hr/dashboard)
└── jobs_bp (/hr/jobs)
```

## 主要变化

### 1. URL路径变化
- 原来：`/settings` → 现在：`/candidate/profile/settings`
- 原来：`/job_search` → 现在：`/candidate/jobs/search`
- 原来：`/hr_dashboard` → 现在：`/hr/dashboard/`
- 原来：`/publish_recruitment` → 现在：`/hr/jobs/publish`

### 2. 模板路径变化
需要将模板文件移动到对应的角色文件夹：
```
templates/
├── common/
│   └── sign.html
├── candidate/
│   ├── settings.html
│   ├── job_list.html
│   ├── job_detail.html
│   ├── job_search.html
│   ├── interview_questions.html
│   ├── loading.html
│   ├── interview_results.html
│   └── my_applications.html
└── hr/
    ├── dashboard.html
    ├── candidates.html
    ├── interviews.html
    ├── reports.html
    ├── insights.html
    ├── publish_recruitment.html
    ├── my_jobs.html
    ├── edit_job.html
    ├── job_candidates.html
    └── interview_detail.html
```

### 3. 导入路径变化
- 原来：`from . import db, applications_collection`
- 现在：`from ...models import User, Job, Application, db`

## 重构优势

### 1. 代码组织更清晰
- 按角色分离，职责明确
- 按功能模块分离，便于维护
- 每个文件职责单一，代码量适中

### 2. 权限控制更严格
- HR功能集中在HR模块中
- 求职者功能集中在求职者模块中
- 通用功能可被所有角色使用

### 3. 扩展性更好
- 新增功能时，可以轻松添加到对应模块
- 修改功能时，只需要关注相关模块
- 测试时可以针对特定模块进行

### 4. 团队协作更友好
- 不同开发者可以专注于不同模块
- 减少代码冲突
- 便于代码审查

## 注意事项

### 1. 模板文件需要移动
需要将现有的模板文件按照新的结构重新组织。

### 2. 静态文件路径
静态文件路径保持不变，但模板中的URL需要更新。

### 3. 数据库模型
数据库模型保持不变，所有功能仍然使用相同的数据库结构。

### 4. 向后兼容
为了保持向后兼容，可以考虑添加URL重定向。

## 下一步工作

1. 移动模板文件到对应的角色文件夹
2. 更新模板中的URL引用
3. 测试所有功能是否正常工作
4. 更新文档和注释
5. 考虑添加URL重定向以保持向后兼容

## 运行测试

重构完成后，可以通过以下方式测试：

1. 启动应用：`python run.py`
2. 测试求职者功能：访问 `/candidate/` 相关路径
3. 测试HR功能：访问 `/hr/` 相关路径
4. 测试通用功能：访问 `/` 相关路径

如果遇到问题，请检查：
- 蓝图是否正确注册
- 模板文件是否在正确位置
- URL路径是否正确
- 导入语句是否正确
