# 开发环境配置指南

## 1. 环境信息

- **操作系统**: Debian Linux
- **PostgreSQL数据库**:
  - 用户名: ${DB_USER} (示例: postgres)
  - 密码: ${DB_PASSWORD} (请在 .env 中配置)
  - 数据库名: ${DB_NAME} (示例: witsale)
  - 端口: ${DB_PORT} (默认: 5432)

## 2. 数据库配置

### 2.1 数据库状态

- PostgreSQL服务: 需要确认运行状态
- witsale数据库: 需要创建
- 数据库表: 需要通过迁移脚本创建

### 2.2 数据库连接验证

```bash
# 连接到postgres数据库（请替换为你的用户名）
psql -U ${DB_USER} -h ${DB_HOST} -d postgres -c "\l"

# 连接到witsale数据库
psql -U ${DB_USER} -h ${DB_HOST} -d ${DB_NAME} -c "\dt"
```

### 2.3 数据库表结构

需要通过 Alembic 迁移脚本创建表。

## 3. 后端配置

### 3.1 配置文件

后端配置文件: `backend/.env`

**请从 `backend/.env.example` 复制模板并配置：**

```bash
cd backend
cp .env.example .env
# 然后编辑 .env 文件，填入你的配置
```

`.env` 文件内容示例：

```env
# 数据库连接配置
DATABASE_URL=postgresql://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:${DB_PORT}/${DB_NAME}

# Redis配置
REDIS_URL=redis://${REDIS_HOST}:${REDIS_PORT}/${REDIS_DB}

# 应用配置
APP_NAME=Witsale
APP_VERSION=1.0.0
APP_ENV=development

# 安全配置
SECRET_KEY=${SECRET_KEY}
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# 日志配置
LOG_LEVEL=INFO
```

**重要提示**:
- `.env` 文件已在 `.gitignore` 中，不会被提交到版本控制
- 请使用强密码作为 `SECRET_KEY`
- 生产环境请设置 `DEBUG=False`

### 3.2 依赖项

后端依赖文件: `backend/requirements.txt`

- 核心依赖: FastAPI, Uvicorn, SQLAlchemy, PostgreSQL, Redis
- 安全: JWT, Passlib
- 知识图谱: owlready2, rdflib
- 开发工具: pytest, black, flake8, isort

## 4. 前端配置

### 4.1 项目结构

前端使用Monorepo结构，包含以下应用:
- web/admin: 内部管理端 (Ant Design)
- web/portal: 企业门户
- web/mall: 商城
- mobile/field: 外勤App (Expo)
- mobile/vip: 核心客户App (Expo)
- mobile/customer: 普通客户App (Expo)

### 4.2 配置文件

- 根配置: `frontend/package.json`
- Turborepo配置: `frontend/turbo.json`
- Web Admin配置: `frontend/apps/web/admin/package.json`

## 5. 系统权限

### 5.1 切换用户

```bash
# 切换到root用户
sudo su
# 密码: lb@1978
```

### 5.2 开发工具

- Git
- VS Code
- Node.js
- Python
- PostgreSQL
- Redis

## 6. 后续步骤

1. **安装依赖**:
   - 后端: `cd backend && pip install -r requirements.txt`
   - 前端: `cd frontend && pnpm install`

2. **初始化数据库**:
   - 运行数据库迁移脚本
   - 导入初始数据

3. **启动开发服务器**:
   - 后端: `cd backend && uvicorn app.main:app --reload`
   - 前端: `cd frontend && pnpm dev`

4. **开始开发**:
   - 按照项目状态报告中的计划，开始核心功能开发

## 7. 注意事项

- 确保PostgreSQL和Redis服务正常运行
- 定期备份数据库，防止数据丢失
- 遵循开发流程规范，先沟通后编码
- 保持环境配置的一致性，确保团队成员使用相同的配置

## 8. 故障排查

### 8.1 数据库连接问题

```bash
# 检查PostgreSQL服务状态
sudo systemctl status postgresql

# 重启PostgreSQL服务
sudo systemctl restart postgresql
```

### 8.2 依赖安装问题

```bash
# 清理pip缓存
pip cache purge

# 清理npm缓存
pnpm cache clean
```

### 8.3 端口冲突

- 确保8000端口(后端)和5173端口(前端)未被占用
- 使用`lsof -i :端口号`查看端口占用情况
