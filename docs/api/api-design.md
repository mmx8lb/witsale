# Witsale API接口设计

## 一、API设计原则

### 1.1 RESTful规范
- **资源命名**：使用复数形式（如 `/api/v1/products`）
- **HTTP方法**：正确使用GET/POST/PUT/PATCH/DELETE
- **状态码**：遵循HTTP状态码规范
- **幂等性**：PUT和DELETE操作应该是幂等的
- **无状态**：API应该是无状态的，依赖JWT进行认证

### 1.2 版本管理
- **URL版本**：使用 `/api/v1/` 格式
- **向后兼容**：确保API版本变更不破坏现有客户端
- **版本控制**：通过URL路径进行版本控制

### 1.3 响应格式
- **统一响应结构**：所有API返回统一的响应格式
- **JSON格式**：使用JSON作为数据交换格式
- **字段命名**：使用snake_case命名规范

---

## 二、认证与授权

### 2.1 认证机制
- **JWT (JSON Web Token)**：使用JWT进行认证
- **Token类型**：Access Token + Refresh Token
- **Token存储**：客户端存储在localStorage或安全的存储中
- **Token过期**：Access Token短期有效，Refresh Token长期有效

### 2.2 授权机制
- **RBAC (Role-Based Access Control)**：基于角色的权限控制
- **权限检查**：每个API端点都需要进行权限检查
- **资源级权限**：支持资源级别的权限控制

### 2.3 认证流程
1. **登录**：POST `/api/v1/auth/login` 获取Access Token和Refresh Token
2. **请求API**：在请求头中携带 `Authorization: Bearer {token}`
3. **Token刷新**：当Access Token过期时，使用Refresh Token获取新的Access Token
4. **登出**：POST `/api/v1/auth/logout` 使Token失效

---

## 三、核心API接口

### 3.1 认证相关接口

#### 登录
- **URL**：`POST /api/v1/auth/login`
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
    "access_token": "...",
    "refresh_token": "...",
    "token_type": "bearer",
    "expires_in": 3600
  }
  ```

#### 刷新Token
- **URL**：`POST /api/v1/auth/refresh`
- **请求体**：
  ```json
  {
    "refresh_token": "..."
  }
  ```
- **响应**：
  ```json
  {
    "access_token": "...",
    "expires_in": 3600
  }
  ```

#### 登出
- **URL**：`POST /api/v1/auth/logout`
- **请求头**：`Authorization: Bearer {token}`
- **响应**：
  ```json
  {
    "message": "Successfully logged out"
  }
  ```

### 3.2 用户相关接口

#### 获取用户列表
- **URL**：`GET /api/v1/users`
- **请求参数**：
  - `page`：页码（默认1）
  - `page_size`：每页数量（默认20）
  - `role_id`：角色ID（可选）
- **响应**：
  ```json
  {
    "total": 100,
    "page": 1,
    "page_size": 20,
    "data": [
      {
        "id": "...",
        "username": "admin",
        "email": "admin@example.com",
        "full_name": "Admin User",
        "role_id": "...",
        "is_active": true
      }
    ]
  }
  ```

#### 创建用户
- **URL**：`POST /api/v1/users`
- **请求体**：
  ```json
  {
    "username": "newuser",
    "email": "newuser@example.com",
    "password": "password123",
    "full_name": "New User",
    "role_id": "...",
    "client_id": "..." (可选)
  }
  ```
- **响应**：
  ```json
  {
    "id": "...",
    "username": "newuser",
    "email": "newuser@example.com",
    "full_name": "New User",
    "role_id": "...",
    "is_active": true
  }
  ```

#### 获取用户详情
- **URL**：`GET /api/v1/users/{id}`
- **响应**：
  ```json
  {
    "id": "...",
    "username": "admin",
    "email": "admin@example.com",
    "full_name": "Admin User",
    "role_id": "...",
    "client_id": "...",
    "is_active": true,
    "created_at": "...",
    "updated_at": "..."
  }
  ```

#### 更新用户
- **URL**：`PUT /api/v1/users/{id}`
- **请求体**：
  ```json
  {
    "email": "updated@example.com",
    "full_name": "Updated Name",
    "role_id": "...",
    "is_active": true
  }
  ```
- **响应**：
  ```json
  {
    "id": "...",
    "username": "admin",
    "email": "updated@example.com",
    "full_name": "Updated Name",
    "role_id": "...",
    "is_active": true
  }
  ```

#### 删除用户
- **URL**：`DELETE /api/v1/users/{id}`
- **响应**：
  ```json
  {
    "message": "User deleted successfully"
  }
  ```

### 3.3 角色与权限接口

#### 获取角色列表
- **URL**：`GET /api/v1/roles`
- **响应**：
  ```json
  {
    "total": 5,
    "data": [
      {
        "id": "...",
        "name": "admin",
        "description": "Administrator"
      }
    ]
  }
  ```

#### 获取权限列表
- **URL**：`GET /api/v1/permissions`
- **响应**：
  ```json
  {
    "total": 20,
    "data": [
      {
        "id": "...",
        "name": "user:create",
        "description": "Create user"
      }
    ]
  }
  ```

#### 分配权限给角色
- **URL**：`POST /api/v1/roles/{role_id}/permissions`
- **请求体**：
  ```json
  {
    "permission_ids": ["...", "..."]
  }
  ```
- **响应**：
  ```json
  {
    "message": "Permissions assigned successfully"
  }
  ```

### 3.4 客户相关接口

#### 获取客户列表
- **URL**：`GET /api/v1/clients`
- **请求参数**：
  - `page`：页码
  - `page_size`：每页数量
  - `client_type`：客户类型（渠道/终端/个人）
  - `status`：状态
- **响应**：
  ```json
  {
    "total": 50,
    "page": 1,
    "page_size": 20,
    "data": [
      {
        "id": "...",
        "name": "ABC Company",
        "client_type": "渠道",
        "contact_name": "John Doe",
        "contact_phone": "13800138000",
        "status": "active"
      }
    ]
  }
  ```

#### 创建客户
- **URL**：`POST /api/v1/clients`
- **请求体**：
  ```json
  {
    "name": "New Company",
    "client_type": "渠道",
    "contact_name": "Jane Smith",
    "contact_phone": "13900139000",
    "contact_email": "contact@example.com",
    "address": "北京市朝阳区"
  }
  ```
- **响应**：
  ```json
  {
    "id": "...",
    "name": "New Company",
    "client_type": "渠道",
    "contact_name": "Jane Smith",
    "contact_phone": "13900139000",
    "status": "active"
  }
  ```

### 3.5 商品相关接口

#### 获取商品列表
- **URL**：`GET /api/v1/products`
- **请求参数**：
  - `page`：页码
  - `page_size`：每页数量
  - `category_id`：分类ID
  - `status`：状态
  - `search`：搜索关键词
- **响应**：
  ```json
  {
    "total": 100,
    "page": 1,
    "page_size": 20,
    "data": [
      {
        "id": "...",
        "name": "Product Name",
        "category_id": "...",
        "description": "Product description",
        "status": "active"
      }
    ]
  }
  ```

#### 创建商品
- **URL**：`POST /api/v1/products`
- **请求体**：
  ```json
  {
    "name": "New Product",
    "category_id": "...",
    "description": "Product description",
    "specs": {"key": "value"},
    "attributes": {"color": "red"}
  }
  ```
- **响应**：
  ```json
  {
    "id": "...",
    "name": "New Product",
    "category_id": "...",
    "description": "Product description",
    "status": "active"
  }
  ```

#### 获取商品详情
- **URL**：`GET /api/v1/products/{id}`
- **响应**：
  ```json
  {
    "id": "...",
    "name": "Product Name",
    "category_id": "...",
    "description": "Product description",
    "specs": {"key": "value"},
    "attributes": {"color": "red"},
    "status": "active",
    "skus": [
      {
        "id": "...",
        "sku_code": "SKU001",
        "name": "SKU Name"
      }
    ]
  }
  ```

### 3.6 SKU相关接口

#### 获取SKU列表
- **URL**：`GET /api/v1/skus`
- **请求参数**：
  - `product_id`：商品ID
  - `status`：状态
- **响应**：
  ```json
  {
    "total": 50,
    "data": [
      {
        "id": "...",
        "product_id": "...",
        "sku_code": "SKU001",
        "name": "SKU Name",
        "barcode": "1234567890",
        "status": "active"
      }
    ]
  }
  ```

#### 创建SKU
- **URL**：`POST /api/v1/skus`
- **请求体**：
  ```json
  {
    "product_id": "...",
    "sku_code": "SKU001",
    "name": "SKU Name",
    "attributes": {"color": "red", "size": "M"},
    "barcode": "1234567890"
  }
  ```
- **响应**：
  ```json
  {
    "id": "...",
    "product_id": "...",
    "sku_code": "SKU001",
    "name": "SKU Name",
    "status": "active"
  }
  ```

### 3.7 价格相关接口

#### 获取价格列表
- **URL**：`GET /api/v1/prices`
- **请求参数**：
  - `sku_id`：SKU ID
  - `price_type`：价格类型
- **响应**：
  ```json
  {
    "total": 10,
    "data": [
      {
        "id": "...",
        "sku_id": "...",
        "price_type": "渠道",
        "price": 100.00,
        "effective_date": "2026-01-01",
        "expiry_date": "2026-12-31"
      }
    ]
  }
  ```

#### 创建价格
- **URL**：`POST /api/v1/prices`
- **请求体**：
  ```json
  {
    "sku_id": "...",
    "price_type": "渠道",
    "price": 100.00,
    "effective_date": "2026-01-01",
    "expiry_date": "2026-12-31"
  }
  ```
- **响应**：
  ```json
  {
    "id": "...",
    "sku_id": "...",
    "price_type": "渠道",
    "price": 100.00,
    "effective_date": "2026-01-01",
    "expiry_date": "2026-12-31"
  }
  ```

### 3.8 库存相关接口

#### 获取库存列表
- **URL**：`GET /api/v1/inventory`
- **请求参数**：
  - `warehouse_id`：仓库ID
  - `sku_id`：SKU ID
  - `min_quantity`：最小库存
- **响应**：
  ```json
  {
    "total": 100,
    "data": [
      {
        "id": "...",
        "sku_id": "...",
        "warehouse_id": "...",
        "quantity": 100,
        "reserved_quantity": 10,
        "updated_at": "..."
      }
    ]
  }
  ```

#### 库存调整
- **URL**：`POST /api/v1/inventory/adjust`
- **请求体**：
  ```json
  {
    "sku_id": "...",
    "warehouse_id": "...",
    "quantity": 50,
    "type": "入库",
    "reference_id": "..."
  }
  ```
- **响应**：
  ```json
  {
    "id": "...",
    "sku_id": "...",
    "warehouse_id": "...",
    "quantity": 150,
    "reserved_quantity": 10
  }
  ```

### 3.9 订单相关接口

#### 获取订单列表
- **URL**：`GET /api/v1/orders`
- **请求参数**：
  - `page`：页码
  - `page_size`：每页数量
  - `client_id`：客户ID
  - `status`：订单状态
  - `start_date`：开始日期
  - `end_date`：结束日期
- **响应**：
  ```json
  {
    "total": 200,
    "page": 1,
    "page_size": 20,
    "data": [
      {
        "id": "...",
        "order_number": "ORD20260318001",
        "client_id": "...",
        "user_id": "...",
        "total_amount": 1000.00,
        "status": "completed",
        "payment_status": "paid",
        "created_at": "..."
      }
    ]
  }
  ```

#### 创建订单
- **URL**：`POST /api/v1/orders`
- **请求体**：
  ```json
  {
    "client_id": "...",
    "delivery_address": "北京市朝阳区",
    "notes": "加急",
    "items": [
      {
        "sku_id": "...",
        "quantity": 2,
        "unit_price": 100.00
      }
    ]
  }
  ```
- **响应**：
  ```json
  {
    "id": "...",
    "order_number": "ORD20260318001",
    "client_id": "...",
    "total_amount": 200.00,
    "status": "pending",
    "payment_status": "unpaid",
    "created_at": "..."
  }
  ```

#### 获取订单详情
- **URL**：`GET /api/v1/orders/{id}`
- **响应**：
  ```json
  {
    "id": "...",
    "order_number": "ORD20260318001",
    "client_id": "...",
    "user_id": "...",
    "total_amount": 200.00,
    "status": "pending",
    "payment_status": "unpaid",
    "delivery_address": "北京市朝阳区",
    "notes": "加急",
    "created_at": "...",
    "updated_at": "...",
    "items": [
      {
        "id": "...",
        "sku_id": "...",
        "quantity": 2,
        "unit_price": 100.00,
        "subtotal": 200.00
      }
    ]
  }
  ```

#### 更新订单状态
- **URL**：`PATCH /api/v1/orders/{id}/status`
- **请求体**：
  ```json
  {
    "status": "completed"
  }
  ```
- **响应**：
  ```json
  {
    "id": "...",
    "order_number": "ORD20260318001",
    "status": "completed"
  }
  ```

### 3.10 支付相关接口

#### 创建支付
- **URL**：`POST /api/v1/payments`
- **请求体**：
  ```json
  {
    "order_id": "...",
    "amount": 200.00,
    "payment_method": "微信支付",
    "transaction_id": "wx1234567890"
  }
  ```
- **响应**：
  ```json
  {
    "id": "...",
    "order_id": "...",
    "amount": 200.00,
    "payment_method": "微信支付",
    "transaction_id": "wx1234567890",
    "status": "completed"
  }
  ```

### 3.11 外勤相关接口

#### 获取拜访列表
- **URL**：`GET /api/v1/field/visits`
- **请求参数**：
  - `user_id`：外勤人员ID
  - `client_id`：客户ID
  - `start_date`：开始日期
  - `end_date`：结束日期
- **响应**：
  ```json
  {
    "total": 50,
    "data": [
      {
        "id": "...",
        "user_id": "...",
        "client_id": "...",
        "visit_date": "2026-03-18",
        "start_time": "...",
        "end_time": "...",
        "location": "POINT(116.404 39.915)",
        "status": "completed"
      }
    ]
  }
  ```

#### 创建拜访记录
- **URL**：`POST /api/v1/field/visits`
- **请求体**：
  ```json
  {
    "client_id": "...",
    "visit_date": "2026-03-18",
    "start_time": "2026-03-18T10:00:00",
    "end_time": "2026-03-18T11:00:00",
    "location": "POINT(116.404 39.915)",
    "notes": "拜访记录"
  }
  ```
- **响应**：
  ```json
  {
    "id": "...",
    "user_id": "...",
    "client_id": "...",
    "visit_date": "2026-03-18",
    "status": "completed"
  }
  ```

### 3.12 知识图谱相关接口

#### 获取实体列表
- **URL**：`GET /api/v1/knowledge/entities`
- **请求参数**：
  - `type`：实体类型
  - `search`：搜索关键词
- **响应**：
  ```json
  {
    "total": 100,
    "data": [
      {
        "id": "...",
        "type": "product",
        "name": "Product Name",
        "properties": {"key": "value"}
      }
    ]
  }
  ```

#### 创建实体
- **URL**：`POST /api/v1/knowledge/entities`
- **请求体**：
  ```json
  {
    "type": "product",
    "name": "New Product",
    "properties": {"category": "electronics"}
  }
  ```
- **响应**：
  ```json
  {
    "id": "...",
    "type": "product",
    "name": "New Product",
    "properties": {"category": "electronics"}
  }
  ```

#### 创建关系
- **URL**：`POST /api/v1/knowledge/relations`
- **请求体**：
  ```json
  {
    "source_id": "...",
    "target_id": "...",
    "relation_type": "related_to",
    "properties": {"strength": "strong"}
  }
  ```
- **响应**：
  ```json
  {
    "id": "...",
    "source_id": "...",
    "target_id": "...",
    "relation_type": "related_to",
    "properties": {"strength": "strong"}
  }
  ```

---

## 四、错误处理

### 4.1 错误响应格式
```json
{
  "error_code": "VALIDATION_ERROR",
  "message": "请求参数验证失败",
  "details": [
    {
      "field": "username",
      "message": "用户名不能为空"
    }
  ],
  "request_id": "..."
}
```

### 4.2 常见错误码

| 错误码 | 描述 | HTTP状态码 |
|--------|------|------------|
| `VALIDATION_ERROR` | 请求参数验证失败 | 400 |
| `AUTHENTICATION_ERROR` | 认证失败 | 401 |
| `AUTHORIZATION_ERROR` | 权限不足 | 403 |
| `NOT_FOUND` | 资源不存在 | 404 |
| `CONFLICT` | 资源冲突 | 409 |
| `INTERNAL_ERROR` | 内部服务器错误 | 500 |
| `SERVICE_UNAVAILABLE` | 服务不可用 | 503 |

---

## 五、分页与排序

### 5.1 分页参数
- `page`：页码，从1开始
- `page_size`：每页数量，默认20，最大100

### 5.2 排序参数
- `order_by`：排序字段
- `order_dir`：排序方向，`asc`或`desc`

### 5.3 分页响应格式
```json
{
  "total": 100,
  "page": 1,
  "page_size": 20,
  "data": [...]
}
```

---

## 六、限流与安全

### 6.1 限流策略
- **IP限流**：每IP每分钟最多60个请求
- **用户限流**：每用户每分钟最多100个请求
- **API限流**：关键API单独限流

### 6.2 安全措施
- **HTTPS**：强制使用HTTPS
- **CORS**：配置合适的CORS策略
- **CSRF**：防范CSRF攻击
- **输入验证**：严格的输入验证
- **敏感信息**：避免返回敏感信息

---

## 七、API文档

### 7.1 OpenAPI/Swagger
- 使用FastAPI自动生成OpenAPI文档
- 访问地址：`/docs`
- 包含所有API接口的详细说明

### 7.2 接口测试
- 支持在Swagger UI中直接测试API
- 提供API密钥管理

---

*Last updated: 2026-03-18*
