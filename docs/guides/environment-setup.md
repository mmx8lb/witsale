# 开发环境配置指南

## 1. 环境信息

- **操作系统**: Debian Linux
- **PostgreSQL数据库**:
  - 用户名: lb
  - 密码: 00000
  - 数据库名: witsale
  - 端口: 5432

## 2. 数据库配置

### 2.1 数据库状态

- PostgreSQL服务: ✅ 运行中
- witsale数据库: ✅ 已存在
- 数据库表: ✅ 已清空

### 2.2 数据库连接验证

```bash
# 连接到postgres数据库
psql -U lb -h localhost -d postgres -c "\l"

# 连接到witsale数据库
psql -U lb -h localhost -d witsale -c "\dt"
```

### 2.3 数据库表结构

当前witsale数据库包含以下表:
- customers
- order_items
- orders
- products
- users

所有表已被清空，确保环境初始状态一致。

## 3. 后端配置

### 3.1 配置文件

后端配置文件: `backend/.env`

```env
# 数据库连接配置
DATABASE_URL=postgresql://lb:00000@localhost:5432/witsale

# Redis配置
REDIS_URL=redis://localhost:6379/0

# 应用配置
APP_NAME=Witsale
APP_VERSION=1.0.0
APP_ENV=development

# 安全配置
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# 日志配置
LOG_LEVEL=INFO
```

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
