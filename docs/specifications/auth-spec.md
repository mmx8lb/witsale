# 用户认证与授权模块规格说明

## 1. 需求背景

在企业销售管理系统中，用户认证与授权是核心功能之一。系统需要支持多种用户角色，包括企业员工、渠道客户、终端客户和最终客户，并且需要基于RBAC（基于角色的访问控制）模型实现精细化的权限管理。

## 2. 技术方案

### 2.1 认证方式
- **JWT认证**：使用JSON Web Token作为认证令牌
- **密码加密**：使用bcrypt进行密码哈希
- **会话管理**：使用Redis存储会话信息

### 2.2 授权模型
- **RBAC（基于角色的访问控制）**：
  - 角色：系统预定义多种角色，如管理员、销售经理、渠道商、终端客户等
  - 权限：细粒度的操作权限，如查看、创建、编辑、删除等
  - 资源：系统中的各种资源，如用户、商品、订单等

## 3. 架构设计

### 3.1 模块结构
```
app/
├── api/
│   └── auth.py          # 认证相关API
├── core/
│   ├── auth.py          # 认证核心逻辑
│   ├── security.py      # 安全相关功能
│   └── jwt.py           # JWT令牌管理
├── models/
│   ├── user.py          # 用户模型
│   ├── role.py          # 角色模型
│   └── permission.py    # 权限模型
├── schemas/
│   └── auth.py          # 认证相关数据结构
└── services/
    └── auth_service.py  # 认证服务
```

### 3.2 数据流
1. 用户登录：提交用户名和密码
2. 系统验证：验证用户身份，生成JWT令牌
3. 令牌存储：将令牌返回给客户端，客户端存储
4. 请求授权：客户端每次请求携带JWT令牌
5. 权限验证：系统验证令牌有效性，检查用户权限

## 4. 数据模型

### 4.1 用户模型 (User)
| 字段名 | 类型 | 描述 |
|-------|------|------|
| id | Integer | 用户ID |
| username | String | 用户名 |
| password_hash | String | 密码哈希 |
| email | String | 邮箱 |
| phone | String | 电话 |
| role_id | Integer | 角色ID |
| is_active | Boolean | 是否激活 |
| created_at | DateTime | 创建时间 |
| updated_at | DateTime | 更新时间 |

### 4.2 角色模型 (Role)
| 字段名 | 类型 | 描述 |
|-------|------|------|
| id | Integer | 角色ID |
| name | String | 角色名称 |
| description | String | 角色描述 |
| created_at | DateTime | 创建时间 |
| updated_at | DateTime | 更新时间 |

### 4.3 权限模型 (Permission)
| 字段名 | 类型 | 描述 |
|-------|------|------|
| id | Integer | 权限ID |
| name | String | 权限名称 |
| code | String | 权限代码 |
| description | String | 权限描述 |
| created_at | DateTime | 创建时间 |
| updated_at | DateTime | 更新时间 |

### 4.4 角色权限关联模型 (RolePermission)
| 字段名 | 类型 | 描述 |
|-------|------|------|
| id | Integer | 关联ID |
| role_id | Integer | 角色ID |
| permission_id | Integer | 权限ID |

## 5. API设计

### 5.1 认证相关API

#### 5.1.1 登录
- **路径**：`/api/auth/login`
- **方法**：`POST`
- **请求体**：
  ```json
  {
    "username": "admin",
    "password": "password123"
  }
  ```
- **响应**：
  ```json
  {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer",
    "expires_in": 3600,
    "user": {
      "id": 1,
      "username": "admin",
      "email": "admin@example.com",
      "role": "admin"
    }
  }
  ```

#### 5.1.2 注册
- **路径**：`/api/auth/register`
- **方法**：`POST`
- **请求体**：
  ```json
  {
    "username": "newuser",
    "password": "password123",
    "email": "newuser@example.com",
    "phone": "13800138000",
    "role_id": 2
  }
  ```
- **响应**：
  ```json
  {
    "id": 2,
    "username": "newuser",
    "email": "newuser@example.com",
    "phone": "13800138000",
    "role_id": 2
  }
  ```

#### 5.1.3 刷新令牌
- **路径**：`/api/auth/refresh`
- **方法**：`POST`
- **请求头**：`Authorization: Bearer <refresh_token>`
- **响应**：
  ```json
  {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer",
    "expires_in": 3600
  }
  ```

#### 5.1.4 登出
- **路径**：`/api/auth/logout`
- **方法**：`POST`
- **请求头**：`Authorization: Bearer <access_token>`
- **响应**：
  ```json
  {
    "message": "Logged out successfully"
  }
  ```

### 5.2 权限管理API

#### 5.2.1 获取角色列表
- **路径**：`/api/auth/roles`
- **方法**：`GET`
- **请求头**：`Authorization: Bearer <access_token>`
- **响应**：
  ```json
  [
    {
      "id": 1,
      "name": "admin",
      "description": "系统管理员"
    },
    {
      "id": 2,
      "name": "sales_manager",
      "description": "销售经理"
    }
  ]
  ```

#### 5.2.2 获取权限列表
- **路径**：`/api/auth/permissions`
- **方法**：`GET`
- **请求头**：`Authorization: Bearer <access_token>`
- **响应**：
  ```json
  [
    {
      "id": 1,
      "name": "user:read",
      "code": "USER_READ",
      "description": "查看用户"
    },
    {
      "id": 2,
      "name": "user:create",
      "code": "USER_CREATE",
      "description": "创建用户"
    }
  ]
  ```

## 6. 测试计划

### 6.1 单元测试
- **测试用户模型**：验证用户创建、密码哈希等功能
- **测试认证服务**：验证登录、注册、令牌生成等功能
- **测试权限管理**：验证角色和权限的关联与验证

### 6.2 集成测试
- **测试API端点**：验证所有认证和授权相关的API端点
- **测试权限控制**：验证不同角色的用户是否能正确访问相应资源

### 6.3 安全性测试
- **测试密码强度**：验证密码哈希和验证功能
- **测试JWT令牌**：验证令牌的生成、验证和过期处理
- **测试权限绕过**：验证是否存在权限绕过的安全漏洞

## 7. 实现注意事项

1. **密码安全**：使用bcrypt进行密码哈希，确保密码存储安全
2. **令牌管理**：设置合理的令牌过期时间，实现令牌刷新机制
3. **权限粒度**：设计细粒度的权限控制，确保最小权限原则
4. **日志记录**：记录认证和授权相关的操作日志，便于审计和排查问题
5. **错误处理**：统一处理认证和授权相关的错误，返回友好的错误信息
6. **性能优化**：缓存角色和权限信息，减少数据库查询

## 8. 依赖项

- **python-jose[cryptography]**：用于JWT令牌生成和验证
- **passlib[bcrypt]**：用于密码哈希
- **aioredis**：用于Redis会话管理
- **pydantic**：用于数据验证
