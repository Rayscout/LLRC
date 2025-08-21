# HR现代管理系统

一个基于Next.js + React + TailwindCSS的现代化HR招聘管理系统，采用iOS风格设计，提供完整的招聘流程管理功能。

## ✨ 功能特性

### 🎯 核心功能
- **仪表板**: 关键指标展示、招聘漏斗分析、最近活动
- **候选人管理**: 候选人信息管理、技能匹配分析、状态跟踪
- **面试安排**: 可视化日历、拖拽安排、面试历史记录
- **报告分析**: KPI图表、招聘效率分析、成本分析
- **员工洞察**: AI驱动的流失风险预测、组织健康度分析

### 🎨 设计特色
- **iOS风格**: 现代化、简洁的界面设计
- **响应式布局**: 完美适配桌面和移动设备
- **玻璃拟态效果**: 现代化的视觉体验
- **流畅动画**: 优雅的交互动画和过渡效果

## 🚀 技术栈

- **前端框架**: Next.js 14 (App Router)
- **UI组件**: React + TypeScript
- **样式框架**: TailwindCSS
- **组件库**: shadcn/ui + Radix UI
- **图标库**: Lucide React
- **图表库**: Recharts
- **状态管理**: React Hooks

## 📦 安装和运行

### 环境要求
- Node.js 18+
- npm 或 yarn

### 安装步骤

1. **克隆项目**
```bash
git clone <repository-url>
cd hr-modern-system
```

2. **安装依赖**
```bash
npm install
# 或
yarn install
```

3. **启动开发服务器**
```bash
npm run dev
# 或
yarn dev
```

4. **访问应用**
打开浏览器访问: `http://localhost:3000`

## 🏗️ 项目结构

```
hr-modern-system/
├── app/                    # Next.js App Router
│   ├── dashboard/         # 仪表板页面
│   ├── candidates/        # 候选人管理页面
│   ├── interviews/        # 面试安排页面
│   ├── reports/           # 报告分析页面
│   ├── insights/          # 员工洞察页面
│   ├── globals.css        # 全局样式
│   ├── layout.tsx         # 根布局
│   └── page.tsx           # 主页面
├── components/            # React组件
│   ├── ui/               # 基础UI组件
│   └── layout/           # 布局组件
├── lib/                  # 工具函数
└── public/               # 静态资源
```

## 🎨 组件说明

### 基础UI组件
- `Button`: 按钮组件，支持多种变体和尺寸
- `Card`: 卡片组件，用于内容展示
- `Avatar`: 头像组件
- `Badge`: 标签组件
- `DropdownMenu`: 下拉菜单组件

### 布局组件
- `MainLayout`: 主布局组件，包含侧边栏和顶部导航
- `Sidebar`: 侧边栏导航组件
- `Header`: 顶部导航栏组件

## 📱 页面功能

### 1. 仪表板 (/dashboard)
- 关键指标卡片展示
- 招聘漏斗图表
- 最近活动时间线
- 快速操作按钮

### 2. 候选人管理 (/candidates)
- 候选人列表表格
- 搜索和筛选功能
- 技能匹配度分析
- 招聘进度概览

### 3. 面试安排 (/interviews)
- 周视图日历
- 面试时间槽管理
- 面试类型区分（在线/现场）
- 面试统计信息

### 4. 报告分析 (/reports)
- KPI指标展示
- 招聘时间趋势图
- 招聘漏斗分析
- 招聘官绩效对比
- AI优化建议

### 5. 员工洞察 (/insights)
- 流失风险分析
- 薪资竞争力分析
- 组织健康度雷达图
- 员工满意度趋势
- AI智能建议

## 🎯 使用说明

### 导航
- 左侧边栏提供主要功能导航
- 顶部导航栏包含搜索、通知和用户信息
- 响应式设计，移动端自动折叠侧边栏

### 数据管理
- 所有数据均为模拟数据，可根据实际需求连接后端API
- 支持数据导出（PDF/CSV）
- 实时数据更新和图表刷新

### 自定义配置
- 可在 `tailwind.config.js` 中调整主题色彩
- 组件样式可在 `components/ui/` 目录下修改
- 图表配置可在各页面组件中调整

## 🔧 开发指南

### 添加新页面
1. 在 `app/` 目录下创建新的页面文件夹
2. 创建 `page.tsx` 文件
3. 使用 `MainLayout` 组件包装页面内容
4. 在侧边栏导航中添加对应链接

### 添加新组件
1. 在 `components/` 目录下创建组件文件
2. 遵循现有的组件命名和结构规范
3. 使用 TypeScript 类型定义
4. 添加必要的样式和交互逻辑

### 样式定制
- 使用 TailwindCSS 类名进行样式设计
- 可在 `globals.css` 中添加自定义CSS变量
- 支持深色模式切换（需要额外配置）

## 📊 性能优化

- 使用 Next.js 的自动代码分割
- 组件懒加载和动态导入
- 图表组件的响应式渲染
- 图片优化和CDN支持

## 🌐 部署

### Vercel部署（推荐）
```bash
npm run build
vercel --prod
```

### 其他平台
```bash
npm run build
npm run start
```

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 📄 许可证

MIT License

## 📞 联系方式

如有问题或建议，请通过以下方式联系：
- 提交 Issue
- 发送邮件
- 参与讨论

---

**注意**: 这是一个演示项目，生产环境使用前请确保：
- 完善错误处理
- 添加用户认证
- 连接真实数据库
- 配置环境变量
- 添加单元测试
- 优化性能指标
