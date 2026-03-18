# Witsale 后端服务

## 项目概览

Witsale 后端服务是一个基于 FastAPI 构建的企业销售管理系统后端，采用 DDD (领域驱动设计) 架构，支持 PostgreSQL 数据库和 Redis 缓存。

## 技术栈

- **Web框架**: FastAPI (Python)
- **数据库**: PostgreSQL 15+
- **缓存**: Redis 7+
- **ORM**: SQLAlchemy 2.0 (异步)
- **数据迁移**: Alembic
- **认证**: JWT + OAuth2
- **API文档**: OpenAPI/Swagger

## 项目结构

```
backend/
├── app/
│   ├── core/              # 核心配置和工具
│   ├── domain/            # 领域层 (DDD核心)
│   ├── application/       # 应用层
│   ├── infrastructure/    # 基础设施层
│   ├── interfaces/        # 接口层 (API)
│   └── main.py            # FastAPI入口
├── alembic/               # 数据库迁移
├── venv/                  # 虚拟环境
├── .env                   # 环境变量
├── requirements.txt       # 依赖
├── pyproject.toml         # 项目配置
└── README.md              # 项目说明
```

## 快速启动

### 1. 安装依赖

```bash
# 使用pip安装依赖
pip install -r requirements.txt

# 或者使用poetry安装依赖
poetry install
```

### 2. 配置环境变量

复制 `.env.example` 文件并修改为 `.env`，然后根据实际情况配置环境变量：

```env
# Database Configuration
DATABASE_URL="postgresql://postgres:postgres@localhost:5432/witsale"

# Redis Configuration
REDIS_URL="redis://localhost:6379/0"

# JWT Configuration
SECRET_KEY="your-secret-key-here"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application Configuration
APP_NAME="Witsale API"
DEBUG=True
```

### 3. 运行数据库迁移

```bash
# 初始化数据库
python -m alembic upgrade head
```

### 4. 启动应用

```bash
# 开发模式
uvicorn app.main:app --reload

# 生产模式
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 5. 访问API文档

启动应用后，可以通过以下地址访问自动生成的 API 文档：

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 开发规范

- **代码风格**: 遵循 PEP8 规范
- **提交规范**: 使用约定式提交 (Conventional Commits)
- **测试覆盖率**: 单元测试覆盖率 > 80%
- **安全**: 双人审查安全代码

## 核心功能模块

1. **用户与认证** (RBAC权限)
2. **商品管理** (多级定价 + 特殊策略)
3. **订单管理** (多级订单)
4. **库存管理** (分布式多级库存)
5. **财务管理** (多种结算方式)
6. **外勤管理** (打卡 + 轨迹)
7. **知识图谱/Ontology** (智能推荐 + 语义搜索)

## 注意事项

- 本项目使用 Python 3.11+，建议使用 Python 3.11 或更高版本
- 开发环境需要 PostgreSQL 15+ 和 Redis 7+ 服务
- 生产环境建议使用 HTTPS 协议
