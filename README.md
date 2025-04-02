# KET考试备考系统

这是一个专门为准备剑桥KET考试（Key English Test）设计的在线学习系统。系统提供全面的词汇学习、句子练习和阅读理解训练，帮助考生高效备考。

## 主要功能

- 词汇学习模块
  - 高频词汇训练
  - 情境化词汇学习
  - 词汇测试和复习
  - 个性化词汇本
  
- 句子练习模块
  - 语法结构训练
  - 常见句型练习
  - 口语表达练习
  
- 阅读理解模块
  - KET考试真题练习
  - 分级阅读材料
  - 阅读策略指导
  
## 技术栈

### 后端
- Python 3.9+
- FastAPI
- MongoDB
- JWT认证
- Pytest (测试框架)

### 前端
- Vue.js 3
- Vite
- Element Plus
- Axios
- Pinia (状态管理)

## 开发环境配置

1. 后端配置
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\activate
pip install -r requirements.txt
```

2. 前端配置
```bash
cd frontend
npm install
npm run dev
```

3. 数据库配置
- 确保MongoDB服务已启动
- 默认连接地址: mongodb://localhost:27017/ket_system

## 项目结构
```
KET/
├── backend/           # 后端代码
│   ├── app/
│   ├── tests/
│   └── requirements.txt
├── frontend/          # 前端代码
│   ├── src/
│   └── package.json
├── DOC/              # 项目文档
└── README.md
```

## 开发团队

- 后端开发
- 前端开发
- 教育内容设计
- UI/UX设计

## 版本控制

项目使用Git进行版本控制，请遵循以下分支命名规范：
- main: 主分支
- develop: 开发分支
- feature/*: 功能分支
- bugfix/*: 修复分支 