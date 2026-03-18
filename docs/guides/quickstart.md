# Witsale 快速开始指南

## 5 分钟启动项目

### 前提条件

确保你已经安装：
- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- Redis 7+
- Git

---

### 步骤 1: 克隆项目

```bash
git clone https://github.com/mmx8lb/witsale.git
cd witsale
```

---

### 步骤 2: 配置后端

#### 2.1 进入后端目录

```bash
cd backend
```

#### 2.2 配置环境变量

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件，填入你的数据库和 Redis 配置
# 主要配置项：
# - DATABASE_URL
# - REDIS_URL
# - SECRET_KEY
```

#### 2.3 安装依赖

```bash
# 推荐使用虚拟环境
python -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

#### 2.4 启动后端服务

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

后端服务将运行在: http://localhost:8000

访问 API 文档:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

### 步骤 3: 配置前端

#### 3.1 进入前端管理端目录

```bash
cd frontend/apps/web/admin
```

#### 3.2 安装依赖

```bash
npm install
```

#### 3.3 启动前端开发服务器

```bash
npm run dev
```

前端服务将运行在: http://localhost:5173

---

### 步骤 4: 访问应用

| 服务 | 地址 | 说明 |
|------|------|------|
| 前端管理端 | http://localhost:5173 | 内部管理端 |
| 后端 API | http://localhost:8000 | API 服务 |
| API 文档 | http://localhost:8000/docs | Swagger UI |

---

## 常用命令

### 后端

```bash
# 进入后端目录
cd backend

# 激活虚拟环境
source venv/bin/activate

# 启动开发服务器（带热重载）
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# 运行测试
pytest

# 代码格式化
black .
isort .
```

### 前端

```bash
# 进入前端管理端目录
cd frontend/apps/web/admin

# 安装依赖
npm install

# 启动开发服务器
npm run dev

# 构建生产版本
npm run build

# 代码检查
npm run lint
```

---

## 项目结构

```
witsale/
├── backend/              # 后端代码
│   ├── app/             # 应用代码
│   ├── domain/          # 领域模型
│   ├── infra/           # 基础设施
│   ├── tests/           # 测试
│   └── requirements.txt # 依赖
├── frontend/            # 前端代码
│   ├── apps/
│   │   └── web/admin/  # 内部管理端
│   └── packages/        # 共享包
├── docs/               # 文档
└── README.md
```

---

## 故障排查

### 问题 1: 后端无法连接数据库

**解决方案**:
1. 确认 PostgreSQL 服务正在运行
2. 检查 `.env` 中的 `DATABASE_URL` 配置
3. 确认数据库已创建

```bash
# 检查 PostgreSQL 状态
sudo systemctl status postgresql

# 连接测试
psql -U your_user -d your_db
```

### 问题 2: 前端依赖安装失败

**解决方案**:
```bash
# 清理 npm 缓存
npm cache clean --force

# 删除 node_modules 重新安装
rm -rf node_modules
rm package-lock.json
npm install
```

### 问题 3: 端口被占用

**解决方案**:
```bash
# 查看端口占用
lsof -i :8000  # 后端
lsof -i :5173  # 前端

# 杀掉占用端口的进程
kill -9 <PID>
```

---

## 下一步

1. 阅读 `docs/README.md` 了解项目概况
2. 查看 `docs/development-process.md` 了解开发流程
3. 开始核心功能开发！

---

## 获取帮助

- 项目文档: `docs/` 目录
- 问题反馈: GitHub Issues
- 技术讨论: 当前聊天窗口

---

*最后更新: 2026-03-19*
