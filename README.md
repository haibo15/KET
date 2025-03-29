# KET考试备考系统

## 项目简介
KET考试备考系统是一个专门为剑桥英语考试KET（Key English Test）考生设计的在线备考平台。该系统提供词汇学习、测试练习和进度追踪等功能，帮助考生更高效地准备KET考试。

## 技术栈
- 前端：Next.js + TypeScript + Tailwind CSS
- 后端：Node.js + Express + TypeScript
- 数据库：MongoDB
- 开发工具：ESLint, Prettier

## 主要功能
### 1. 词汇学习系统
- 分级词汇学习
- 单词发音功能
- 智能复习提醒
- 学习进度追踪
- 单词搜索功能

### 2. 用户系统
- 用户注册和登录
- 个人学习进度记录
- 错题收集功能
- 学习数据统计

### 3. 测试系统
- 单词测试
- 进度评估
- 错题复习
- 成绩追踪

## 项目结构
```
KET/
├── frontend/          # Next.js前端项目
├── backend/           # Express后端项目
├── DOC/              # 项目文档
│   ├── project_plan.md       # 项目整体规划
│   ├── vocabulary_plan.md    # 词汇系统设计
│   └── development_progress.md # 开发进度
└── README.md
```

## 开发进度
### 已完成
- ✅ 项目整体规划和系统设计
- ✅ 后端基础架构搭建
- ✅ 词汇模块API开发
- ✅ 前端基础架构搭建
- ✅ 基础UI组件开发

### 进行中
- 🔄 页面样式和交互优化
- 🔄 单词发音功能实现
- 🔄 加载状态和错误处理
- 🔄 KET核心词汇收集

### 计划中
- ⏳ 用户认证系统
- ⏳ 学习进度追踪
- ⏳ 测试系统开发
- ⏳ 性能优化

## 本地开发
1. 克隆项目
```bash
git clone [项目地址]
```

2. 安装依赖
```bash
# 前端
cd frontend
npm install

# 后端
cd backend
npm install
```

3. 配置环境变量
```bash
# 后端
cp .env.example .env
# 编辑.env文件配置必要的环境变量
```

4. 启动开发服务器
```bash
# 前端
npm run dev

# 后端
npm run dev
```

## 贡献指南
1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 发起 Pull Request

## 许可证
[待定]

## 联系方式
[待定] 