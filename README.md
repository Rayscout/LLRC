# LLRC - 智能人才管理系统

## 项目概述

LLRC (Learning & Leadership Resource Center) 是一个基于Flask的智能人才管理系统，集成了人才招聘、培训管理、绩效评估、职业发展追踪等核心功能。系统采用现代化的Web技术栈，提供直观的用户界面和强大的后台管理功能。

## 核心功能

### 🎯 人才招聘管理
- **智能简历解析**：自动解析简历信息，提取关键数据
- **AI面试评估**：基于AI技术的面试评分系统
- **招聘流程管理**：完整的招聘流程跟踪和管理
- **人才库管理**：集中管理候选人信息

### 📊 人才分析仪表板
- **实时数据展示**：关键指标实时监控
- **可视化图表**：多种图表类型展示数据趋势
- **预测分析**：基于历史数据的趋势预测
- **自定义报表**：灵活的报表生成功能

### 🎓 学习中心
- **课程管理**：在线课程发布和管理
- **学习追踪**：员工学习进度监控
- **技能评估**：技能水平评估和认证
- **学习路径**：个性化学习路径规划

### 📈 绩效管理
- **目标设定**：SMART目标管理
- **绩效评估**：多维度绩效评估体系
- **反馈系统**：实时反馈和沟通
- **改进计划**：绩效改进计划制定

### 🏢 组织健康监控
- **员工满意度**：满意度调查和分析
- **流失预警**：员工流失风险预警
- **组织氛围**：组织文化氛围评估
- **健康指数**：组织健康度综合评估

### 💼 职业发展
- **职业路径规划**：个性化职业发展路径
- **技能图谱**：技能需求和发展图谱
- **晋升管理**：晋升流程和标准管理
- **导师制度**：导师匹配和管理

## 技术架构

### 后端技术栈
- **Flask**: Web框架
- **SQLAlchemy**: ORM数据库操作
- **MongoDB**: 文档数据库
- **Redis**: 缓存和会话管理
- **Celery**: 异步任务处理

### 前端技术栈
- **HTML5/CSS3**: 现代化UI设计
- **JavaScript**: 交互功能实现
- **Chart.js**: 数据可视化
- **Bootstrap**: 响应式布局

### 部署架构
- **Nginx**: Web服务器和负载均衡
- **Gunicorn**: WSGI应用服务器
- **Docker**: 容器化部署
- **Linux**: 服务器操作系统

## 项目结构

```
LLRC/
├── app/                          # 主应用目录
│   ├── __init__.py              # Flask应用初始化
│   ├── models.py                # 数据模型定义
│   ├── talent_dashboard.py      # 人才仪表板路由
│   ├── talent_analysis_service.py # 人才分析服务
│   ├── pdf_generator.py         # PDF生成器
│   ├── utils.py                 # 工具函数
│   ├── templates/               # HTML模板
│   │   ├── talent_management/   # 人才管理模板
│   │   ├── smartrecruit/        # 招聘系统模板
│   │   └── common/              # 公共模板
│   ├── static/                  # 静态资源
│   └── tools/                   # 工具模块
├── config/                      # 配置文件
│   ├── config.py               # 应用配置
│   ├── nginx.conf              # Nginx配置
│   └── gunicorn.conf.py        # Gunicorn配置
├── database/                    # 数据库相关
│   ├── create_tables.py         # 表创建脚本
│   ├── init_database.py         # 数据库初始化
│   └── migrations/              # 数据库迁移
├── scripts/                     # 脚本文件
│   ├── deploy.sh               # 部署脚本
│   ├── start.bat               # Windows启动脚本
│   └── setup_venv.ps1          # 环境设置脚本
├── docs/                        # 文档
├── tests/                       # 测试文件
├── requirements.txt             # Python依赖
├── run.py                       # 应用入口
└── wsgi.py                      # WSGI入口
```

## 安装部署

### 环境要求
- Python 3.8+
- MySQL 8.0+ 或 PostgreSQL 12+
- MongoDB 4.4+
- Redis 6.0+
- Node.js 14+ (可选，用于前端构建)

### 快速安装

1. **克隆项目**
```bash
git clone <repository-url>
cd LLRC
```

2. **创建虚拟环境**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows
```

3. **安装依赖**
```bash
pip install -r requirements.txt
```

4. **配置数据库**
```bash
# 编辑 config/config.py 配置数据库连接
python database/init_database.py
```

5. **启动应用**
```bash
python run.py
```

### Docker部署

1. **构建镜像**
```bash
docker build -t llrc .
```

2. **运行容器**
```bash
docker run -d -p 5000:5000 --name llrc-app llrc
```

### 生产环境部署

1. **使用Gunicorn**
```bash
gunicorn -c config/gunicorn.conf.py wsgi:app
```

2. **配置Nginx**
```bash
# 复制 config/nginx.conf 到 /etc/nginx/sites-available/
sudo ln -s /etc/nginx/sites-available/llrc /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

## 使用指南

### 管理员功能
- **用户管理**：创建和管理用户账户
- **权限控制**：设置用户权限和角色
- **系统配置**：配置系统参数和选项
- **数据备份**：数据库备份和恢复

### HR功能
- **招聘管理**：发布职位、筛选简历、安排面试
- **员工管理**：员工信息管理、合同管理
- **绩效管理**：绩效评估、目标设定
- **培训管理**：培训计划、课程管理

### 员工功能
- **个人信息**：查看和更新个人信息
- **学习中心**：参与培训、查看学习进度
- **绩效查看**：查看个人绩效评估
- **职业发展**：查看职业发展路径

## 配置说明

### 环境变量
```bash
# 数据库配置
DATABASE_URL=mysql://user:password@localhost/llrc
MONGODB_URL=mongodb://localhost:27017/llrc
REDIS_URL=redis://localhost:6379/0

# 应用配置
SECRET_KEY=your-secret-key
DEBUG=False
FLASK_ENV=production

# 邮件配置
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-password
```

### 数据库配置
系统支持多种数据库：
- **MySQL**: 主要业务数据
- **MongoDB**: 文档存储和日志
- **Redis**: 缓存和会话

## API文档

### 认证接口
- `POST /api/login` - 用户登录
- `POST /api/logout` - 用户登出
- `GET /api/profile` - 获取用户信息

### 人才管理接口
- `GET /api/talent/dashboard` - 获取人才仪表板数据
- `POST /api/talent/analysis` - 人才分析
- `GET /api/talent/export` - 导出人才数据

### 招聘接口
- `GET /api/recruitment/jobs` - 获取职位列表
- `POST /api/recruitment/jobs` - 创建职位
- `GET /api/recruitment/candidates` - 获取候选人列表

## 开发指南

### 代码规范
- 遵循PEP 8 Python代码规范
- 使用类型注解
- 编写单元测试
- 添加详细的文档字符串

### 提交规范
```
feat: 新功能
fix: 修复bug
docs: 文档更新
style: 代码格式调整
refactor: 代码重构
test: 测试相关
chore: 构建过程或辅助工具的变动
```

### 测试
```bash
# 运行单元测试
python -m pytest tests/

# 运行覆盖率测试
python -m pytest --cov=app tests/
```

## 故障排除

### 常见问题
1. **数据库连接失败**
   - 检查数据库服务是否启动
   - 验证连接字符串配置
   - 确认网络连接正常

2. **模板文件找不到**
   - 检查模板路径配置
   - 确认文件权限设置
   - 验证Jinja2配置

3. **静态文件无法访问**
   - 检查Nginx配置
   - 确认静态文件路径
   - 验证文件权限

### 日志查看
```bash
# 查看应用日志
tail -f logs/app.log

# 查看Nginx日志
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log
```

## 贡献指南

1. Fork项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开Pull Request

## 许可证

本项目采用MIT许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 联系方式

- 项目维护者: [Your Name]
- 邮箱: [your.email@example.com]
- 项目链接: [https://github.com/your-username/LLRC]

## 更新日志

### v1.0.0 (2024-09-04)
- 初始版本发布
- 基础功能实现
- 用户认证系统
- 人才管理模块

---

**注意**: 这是一个企业级人才管理系统，请确保在生产环境中正确配置安全设置和权限控制。
