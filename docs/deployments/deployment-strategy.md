# Witsale 部署策略参考文档

## 一、部署架构设计

### 1. 环境分离
- **开发环境 (Local)**：本地开发，连接本地或测试数据库
- **测试环境 (Staging)**：云服务器上的测试环境，模拟生产配置
- **生产环境 (Production)**：云服务器上的正式环境

### 2. 技术栈适配
- **后端**：FastAPI + PostgreSQL + Redis
- **前端**：React + Ant Design
- **部署工具**：Docker + Docker Compose（简化环境管理）

## 二、具体部署方案

### 1. 服务器准备
- **操作系统**：推荐 Ubuntu 20.04 LTS 或 CentOS 7+
- **硬件要求**：至少 2GB 内存，50GB 磁盘空间
- **网络配置**：开放必要端口（80, 443, 8000 等）
- **依赖安装**：Docker、Docker Compose、Git

### 2. 部署流程设计

#### 方案 A：手动部署（适合初期开发）
1. **代码同步**：使用 Git 拉取代码到服务器
2. **环境配置**：在服务器上配置环境变量
3. **构建部署**：
   - 后端：安装依赖，启动应用
   - 前端：构建静态文件，部署到 Nginx

#### 方案 B：自动化部署（推荐）
1. **配置 CI/CD**：使用 GitHub Actions 或 Jenkins
2. **触发机制**：代码提交到特定分支时自动部署
3. **部署步骤**：
   - 拉取代码
   - 运行测试
   - 构建应用
   - 部署到服务器
   - 重启服务

### 3. 技术实现细节

#### 后端部署
- 使用 **Uvicorn** 作为 ASGI 服务器
- 配置 **Gunicorn** 作为进程管理器（生产环境）
- 使用 **Alembic** 管理数据库迁移
- 配置 **Nginx** 作为反向代理

#### 前端部署
- 使用 **Vite** 构建静态文件
- 部署到 **Nginx** 静态目录
- 配置 Nginx 反向代理到后端 API

#### 数据库与缓存
- **PostgreSQL**：使用系统服务或 Docker 容器
- **Redis**：使用系统服务或 Docker 容器
- **数据备份**：定期自动备份数据库

## 三、边开发边部署的优势
1. **快速反馈**：实时看到代码变更的效果
2. **持续测试**：在真实环境中验证功能
3. **提前发现问题**：更早发现部署相关的问题
4. **协作便捷**：团队成员可以访问测试环境查看进度

## 四、注意事项
1. **数据安全**：测试环境避免使用真实生产数据
2. **环境隔离**：确保开发、测试、生产环境配置隔离
3. **备份策略**：定期备份数据库和关键配置
4. **监控告警**：设置基本的监控和告警机制
5. **版本控制**：使用 Git 分支管理不同环境的代码

## 五、推荐工具
- **代码管理**：GitHub/GitLab
- **CI/CD**：GitHub Actions、Jenkins
- **容器化**：Docker、Docker Compose
- **监控**：Prometheus + Grafana
- **日志管理**：ELK Stack

## 六、部署配置示例

### Docker Compose 配置示例
```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/witsale
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis

  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend

  db:
    image: postgres:15
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_DB=witsale
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

### Nginx 配置示例
```nginx
server {
    listen 80;
    server_name example.com;

    location / {
        root /usr/share/nginx/html;
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 七、部署流程文档

### 开发环境部署
1. 克隆代码库
2. 安装依赖
3. 配置环境变量
4. 启动开发服务器

### 测试环境部署
1. 推送代码到测试分支
2. CI/CD 自动构建部署
3. 运行测试
4. 验证功能

### 生产环境部署
1. 推送代码到主分支
2. CI/CD 自动构建部署
3. 运行测试
4. 监控部署状态
5. 验证功能

## 八、故障排查指南

### 常见问题
1. **数据库连接失败**：检查数据库配置和网络连接
2. **API 响应慢**：检查服务器资源和数据库性能
3. **前端页面空白**：检查前端构建和 Nginx 配置
4. **权限错误**：检查文件权限和用户权限

### 排查步骤
1. 查看应用日志
2. 检查服务状态
3. 测试网络连接
4. 验证配置文件
5. 检查数据库状态

## 九、监控与维护

### 监控指标
- **服务器**：CPU、内存、磁盘使用率
- **应用**：响应时间、错误率、请求量
- **数据库**：查询性能、连接数、缓存命中率

### 维护计划
- **每日**：检查应用状态和日志
- **每周**：备份数据库和配置
- **每月**：更新依赖和安全补丁
- **每季度**：性能优化和容量规划

## 十、总结

通过本部署策略，Witsale 系统可以实现边开发边部署的持续集成流程，确保开发效率的同时保证系统的稳定性和可靠性。随着项目的发展，可以根据实际需求调整部署策略，以适应不断变化的业务需求。