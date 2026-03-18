# 订单管理模块规格说明

## 1. 需求背景

订单管理是企业销售管理系统的核心功能之一。系统需要支持订单的全生命周期管理，包括订单创建、处理、状态管理、物流跟踪等。此外，还需要支持多级订单（如企业订单、渠道订单、终端订单等）和多种订单类型（如销售订单、退货订单、换货订单等）。

## 2. 技术方案

### 2.1 核心技术
- **订单状态管理**：实现订单的完整状态流转，如待支付、已支付、待发货、已发货、已完成、已取消等
- **多级订单**：支持企业订单、渠道订单、终端订单等多级订单结构
- **订单类型**：支持销售订单、退货订单、换货订单等多种订单类型
- **物流跟踪**：集成物流信息，实现订单物流状态的实时跟踪
- **支付集成**：集成多种支付方式，如在线支付、线下支付等

### 2.2 关键特性
- **订单创建**：支持手动创建订单和从购物车创建订单
- **订单处理**：支持订单审核、确认、发货、退货等操作
- **订单查询**：支持多种条件的订单查询和筛选
- **订单统计**：支持订单数据的统计和分析
- **订单通知**：支持订单状态变更的通知机制

## 3. 架构设计

### 3.1 模块结构
```
app/
├── api/
│   └── order.py          # 订单相关API
├── core/
│   └── order.py          # 订单核心逻辑
├── models/
│   ├── order.py          # 订单模型
│   ├── order_item.py     # 订单商品模型
│   └── order_status.py   # 订单状态模型
├── schemas/
│   └── order.py          # 订单相关数据结构
└── services/
    └── order_service.py  # 订单服务
```

### 3.2 数据流
1. 订单创建：用户创建订单，系统生成订单号，计算总价
2. 订单支付：用户支付订单，系统更新订单状态
3. 订单处理：管理员审核订单，安排发货
4. 订单发货：系统更新订单状态，生成物流信息
5. 订单完成：用户确认收货，系统更新订单状态
6. 订单退货/换货：用户申请退货/换货，系统处理相关流程

## 4. 数据模型

### 4.1 订单模型 (Order)
| 字段名 | 类型 | 描述 |
|-------|------|------|
| id | Integer | 订单ID |
| order_no | String | 订单号 |
| customer_id | Integer | 客户ID |
| customer_name | String | 客户名称 |
| order_type | String | 订单类型（销售、退货、换货） |
| order_level | String | 订单级别（企业、渠道、终端） |
| total_amount | Decimal | 订单总金额 |
| actual_amount | Decimal | 实际支付金额 |
| payment_method | String | 支付方式 |
| payment_status | String | 支付状态 |
| order_status | String | 订单状态 |
| shipping_address | JSONB | 收货地址 |
| logistics_company | String | 物流公司 |
| tracking_number | String | 物流单号 |
| notes | Text | 订单备注 |
| created_at | DateTime | 创建时间 |
| updated_at | DateTime | 更新时间 |
| created_by | Integer | 创建人ID |
| updated_by | Integer | 更新人ID |

### 4.2 订单商品模型 (OrderItem)
| 字段名 | 类型 | 描述 |
|-------|------|------|
| id | Integer | 订单商品ID |
| order_id | Integer | 订单ID |
| product_id | Integer | 商品ID |
| product_name | String | 商品名称 |
| sku | String | 商品SKU |
| quantity | Integer | 数量 |
| unit_price | Decimal | 单价 |
| total_price | Decimal | 总价 |
| attributes | JSONB | 商品属性 |
| created_at | DateTime | 创建时间 |
| updated_at | DateTime | 更新时间 |

### 4.3 订单状态模型 (OrderStatus)
| 字段名 | 类型 | 描述 |
|-------|------|------|
| id | Integer | 状态ID |
| order_id | Integer | 订单ID |
| status | String | 状态名称 |
| description | Text | 状态描述 |
| created_at | DateTime | 创建时间 |
| created_by | Integer | 创建人ID |

## 5. API设计

### 5.1 订单管理API

#### 5.1.1 创建订单
- **路径**：`/api/orders`
- **方法**：`POST`
- **请求体**：
  ```json
  {
    "customer_id": 1,
    "customer_name": "客户名称",
    "order_type": "sales",
    "order_level": "enterprise",
    "items": [
      {
        "product_id": 1,
        "product_name": "商品名称",
        "sku": "SKU001",
        "quantity": 2,
        "unit_price": 100.00,
        "attributes": {"color": "红色", "size": "M"}
      }
    ],
    "shipping_address": {
      "name": "收件人",
      "phone": "13800138000",
      "address": "北京市朝阳区"
    },
    "payment_method": "online",
    "notes": "订单备注"
  }
  ```
- **响应**：
  ```json
  {
    "id": 1,
    "order_no": "ORD202603180001",
    "customer_id": 1,
    "customer_name": "客户名称",
    "order_type": "sales",
    "order_level": "enterprise",
    "total_amount": 200.00,
    "actual_amount": 200.00,
    "payment_method": "online",
    "payment_status": "unpaid",
    "order_status": "pending",
    "shipping_address": {
      "name": "收件人",
      "phone": "13800138000",
      "address": "北京市朝阳区"
    },
    "notes": "订单备注",
    "items": [
      {
        "product_id": 1,
        "product_name": "商品名称",
        "sku": "SKU001",
        "quantity": 2,
        "unit_price": 100.00,
        "total_price": 200.00,
        "attributes": {"color": "红色", "size": "M"}
      }
    ]
  }
  ```

#### 5.1.2 获取订单列表
- **路径**：`/api/orders`
- **方法**：`GET`
- **查询参数**：
  - `order_no`：订单号
  - `customer_id`：客户ID
  - `order_status`：订单状态
  - `start_date`：开始日期
  - `end_date`：结束日期
  - `page`：页码
  - `limit`：每页数量
- **响应**：
  ```json
  {
    "total": 100,
    "page": 1,
    "limit": 10,
    "items": [
      {
        "id": 1,
        "order_no": "ORD202603180001",
        "customer_name": "客户名称",
        "order_type": "sales",
        "order_level": "enterprise",
        "total_amount": 200.00,
        "payment_status": "paid",
        "order_status": "shipped",
        "created_at": "2026-03-18T00:00:00"
      }
    ]
  }
  ```

#### 5.1.3 获取订单详情
- **路径**：`/api/orders/{id}`
- **方法**：`GET`
- **响应**：
  ```json
  {
    "id": 1,
    "order_no": "ORD202603180001",
    "customer_id": 1,
    "customer_name": "客户名称",
    "order_type": "sales",
    "order_level": "enterprise",
    "total_amount": 200.00,
    "actual_amount": 200.00,
    "payment_method": "online",
    "payment_status": "paid",
    "order_status": "shipped",
    "shipping_address": {
      "name": "收件人",
      "phone": "13800138000",
      "address": "北京市朝阳区"
    },
    "logistics_company": "顺丰速运",
    "tracking_number": "SF1234567890",
    "notes": "订单备注",
    "items": [
      {
        "product_id": 1,
        "product_name": "商品名称",
        "sku": "SKU001",
        "quantity": 2,
        "unit_price": 100.00,
        "total_price": 200.00,
        "attributes": {"color": "红色", "size": "M"}
      }
    ],
    "status_history": [
      {
        "status": "pending",
        "description": "订单创建",
        "created_at": "2026-03-18T00:00:00"
      },
      {
        "status": "paid",
        "description": "订单支付",
        "created_at": "2026-03-18T01:00:00"
      },
      {
        "status": "shipped",
        "description": "订单发货",
        "created_at": "2026-03-18T02:00:00"
      }
    ]
  }
  ```

#### 5.1.4 更新订单
- **路径**：`/api/orders/{id}`
- **方法**：`PUT`
- **请求体**：
  ```json
  {
    "shipping_address": {
      "name": "更新后的收件人",
      "phone": "13800138001",
      "address": "北京市海淀区"
    },
    "notes": "更新后的订单备注"
  }
  ```
- **响应**：
  ```json
  {
    "id": 1,
    "order_no": "ORD202603180001",
    "customer_id": 1,
    "customer_name": "客户名称",
    "order_type": "sales",
    "order_level": "enterprise",
    "total_amount": 200.00,
    "actual_amount": 200.00,
    "payment_method": "online",
    "payment_status": "paid",
    "order_status": "shipped",
    "shipping_address": {
      "name": "更新后的收件人",
      "phone": "13800138001",
      "address": "北京市海淀区"
    },
    "logistics_company": "顺丰速运",
    "tracking_number": "SF1234567890",
    "notes": "更新后的订单备注"
  }
  ```

#### 5.1.5 取消订单
- **路径**：`/api/orders/{id}/cancel`
- **方法**：`POST`
- **请求体**：
  ```json
  {
    "reason": "取消原因"
  }
  ```
- **响应**：
  ```json
  {
    "message": "订单取消成功"
  }
  ```

#### 5.1.6 支付订单
- **路径**：`/api/orders/{id}/pay`
- **方法**：`POST`
- **请求体**：
  ```json
  {
    "payment_method": "online",
    "transaction_id": "TRA1234567890"
  }
  ```
- **响应**：
  ```json
  {
    "message": "订单支付成功"
  }
  ```

#### 5.1.7 发货订单
- **路径**：`/api/orders/{id}/ship`
- **方法**：`POST`
- **请求体**：
  ```json
  {
    "logistics_company": "顺丰速运",
    "tracking_number": "SF1234567890"
  }
  ```
- **响应**：
  ```json
  {
    "message": "订单发货成功"
  }
  ```

#### 5.1.8 确认收货
- **路径**：`/api/orders/{id}/confirm`
- **方法**：`POST`
- **响应**：
  ```json
  {
    "message": "订单确认收货成功"
  }
  ```

### 5.2 订单统计API

#### 5.2.1 获取订单统计数据
- **路径**：`/api/orders/stats`
- **方法**：`GET`
- **查询参数**：
  - `start_date`：开始日期
  - `end_date`：结束日期
- **响应**：
  ```json
  {
    "total_orders": 100,
    "total_amount": 10000.00,
    "paid_orders": 80,
    "shipped_orders": 60,
    "completed_orders": 50,
    "cancelled_orders": 5
  }
  ```

## 6. 测试计划

### 6.1 单元测试
- **测试订单模型**：验证订单创建、更新、状态变更等功能
- **测试订单服务**：验证订单处理、支付、发货等核心业务逻辑
- **测试订单状态流转**：验证订单状态的正确流转
- **测试订单统计**：验证订单统计数据的准确性

### 6.2 集成测试
- **测试API端点**：验证所有订单管理相关的API端点
- **测试商品集成**：验证订单与商品模块的集成
- **测试库存集成**：验证订单与库存模块的集成
- **测试支付集成**：验证订单与支付模块的集成

### 6.3 性能测试
- **测试订单创建**：验证高并发下的订单创建性能
- **测试订单查询**：验证大量订单数据下的查询性能
- **测试订单状态更新**：验证订单状态更新的性能

## 7. 实现注意事项

1. **数据一致性**：确保订单数据与商品、库存、支付等模块的数据一致性
2. **事务处理**：使用数据库事务确保订单相关操作的原子性
3. **并发控制**：处理并发订单操作，避免数据冲突
4. **错误处理**：统一处理订单管理相关的错误，返回友好的错误信息
5. **日志记录**：记录订单相关的操作日志，便于审计和排查问题
6. **安全防护**：保护订单数据的安全，防止未授权访问
7. **可扩展性**：支持未来新增的订单类型和业务流程

## 8. 依赖项

- **sqlalchemy**：用于数据库操作
- **pydantic**：用于数据验证
- **python-dotenv**：用于环境变量管理
- **python-jose**：用于JWT认证
