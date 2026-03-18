# 库存管理模块规格说明

## 1. 需求背景

库存管理是企业销售管理系统的核心功能之一。系统需要支持分布式多级库存管理，包括总仓、区域仓、前置仓等多级库存结构。此外，还需要支持库存的实时更新、库存预警、库存调拨等功能。

## 2. 技术方案

### 2.1 核心技术
- **分布式库存**：支持多级库存结构，如总仓、区域仓、前置仓等
- **实时库存**：实现库存的实时更新和同步
- **库存预警**：设置库存预警阈值，当库存低于阈值时发出预警
- **库存调拨**：支持不同仓库之间的库存调拨
- **库存盘点**：支持库存的定期盘点和调整

### 2.2 关键特性
- **多级库存**：支持总仓、区域仓、前置仓等多级库存结构
- **实时更新**：订单处理、采购入库等操作实时更新库存
- **库存预警**：设置库存预警阈值，当库存低于阈值时发出预警
- **库存调拨**：支持不同仓库之间的库存调拨
- **库存盘点**：支持库存的定期盘点和调整
- **库存报表**：支持库存数据的统计和分析

## 3. 架构设计

### 3.1 模块结构
```
app/
├── api/
│   └── inventory.py        # 库存相关API
├── core/
│   └── inventory.py        # 库存核心逻辑
├── models/
│   ├── warehouse.py        # 仓库模型
│   ├── inventory.py        # 库存模型
│   └── inventory_movement.py # 库存变动记录模型
├── schemas/
│   └── inventory.py        # 库存相关数据结构
└── services/
    └── inventory_service.py # 库存服务
```

### 3.2 数据流
1. 采购入库：采购商品入库，增加库存数量
2. 销售出库：销售商品出库，减少库存数量
3. 库存调拨：从一个仓库调拨到另一个仓库，减少源仓库库存，增加目标仓库库存
4. 库存盘点：定期盘点库存，调整库存数量
5. 库存预警：当库存低于预警阈值时，发出预警通知

## 4. 数据模型

### 4.1 仓库模型 (Warehouse)
| 字段名 | 类型 | 描述 |
|-------|------|------|
| id | Integer | 仓库ID |
| name | String | 仓库名称 |
| type | String | 仓库类型（总仓、区域仓、前置仓等） |
| location | String | 仓库位置 |
| contact | String | 联系人 |
| phone | String | 联系电话 |
| is_active | Boolean | 是否激活 |
| created_at | DateTime | 创建时间 |
| updated_at | DateTime | 更新时间 |

### 4.2 库存模型 (Inventory)
| 字段名 | 类型 | 描述 |
|-------|------|------|
| id | Integer | 库存ID |
| warehouse_id | Integer | 仓库ID |
| product_id | Integer | 商品ID |
| product_name | String | 商品名称 |
| sku | String | 商品SKU |
| quantity | Integer | 库存数量 |
| min_stock | Integer | 最小库存预警 |
| max_stock | Integer | 最大库存限制 |
| unit | String | 单位 |
| last_updated | DateTime | 最后更新时间 |
| created_at | DateTime | 创建时间 |
| updated_at | DateTime | 更新时间 |

### 4.3 库存变动记录模型 (InventoryMovement)
| 字段名 | 类型 | 描述 |
|-------|------|------|
| id | Integer | 变动ID |
| warehouse_id | Integer | 仓库ID |
| product_id | Integer | 商品ID |
| movement_type | String | 变动类型（入库、出库、调拨） |
| quantity | Integer | 变动数量 |
| before_quantity | Integer | 变动前数量 |
| after_quantity | Integer | 变动后数量 |
| reference_type | String | 参考类型（订单、采购单、调拨单等） |
| reference_id | Integer | 参考ID |
| notes | Text | 备注 |
| created_at | DateTime | 创建时间 |
| created_by | Integer | 创建人ID |

## 5. API设计

### 5.1 仓库管理API

#### 5.1.1 创建仓库
- **路径**：`/api/warehouses`
- **方法**：`POST`
- **请求体**：
  ```json
  {
    "name": "总仓库",
    "type": "main",
    "location": "北京市朝阳区",
    "contact": "张三",
    "phone": "13800138000"
  }
  ```
- **响应**：
  ```json
  {
    "id": 1,
    "name": "总仓库",
    "type": "main",
    "location": "北京市朝阳区",
    "contact": "张三",
    "phone": "13800138000",
    "is_active": true
  }
  ```

#### 5.1.2 获取仓库列表
- **路径**：`/api/warehouses`
- **方法**：`GET`
- **响应**：
  ```json
  [
    {
      "id": 1,
      "name": "总仓库",
      "type": "main",
      "location": "北京市朝阳区",
      "contact": "张三",
      "phone": "13800138000",
      "is_active": true
    }
  ]
  ```

### 5.2 库存管理API

#### 5.2.1 获取库存列表
- **路径**：`/api/inventories`
- **方法**：`GET`
- **查询参数**：
  - `warehouse_id`：仓库ID
  - `product_id`：商品ID
  - `sku`：商品SKU
  - `min_quantity`：最小库存
  - `max_quantity`：最大库存
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
        "warehouse_id": 1,
        "warehouse_name": "总仓库",
        "product_id": 1,
        "product_name": "商品名称",
        "sku": "SKU001",
        "quantity": 100,
        "min_stock": 10,
        "max_stock": 500,
        "unit": "件",
        "last_updated": "2026-03-18T00:00:00"
      }
    ]
  }
  ```

#### 5.2.2 获取库存详情
- **路径**：`/api/inventories/{id}`
- **方法**：`GET`
- **响应**：
  ```json
  {
    "id": 1,
    "warehouse_id": 1,
    "warehouse_name": "总仓库",
    "product_id": 1,
    "product_name": "商品名称",
    "sku": "SKU001",
    "quantity": 100,
    "min_stock": 10,
    "max_stock": 500,
    "unit": "件",
    "last_updated": "2026-03-18T00:00:00",
    "movements": [
      {
        "movement_type": "in",
        "quantity": 50,
        "before_quantity": 50,
        "after_quantity": 100,
        "reference_type": "purchase",
        "reference_id": 1,
        "created_at": "2026-03-18T00:00:00"
      }
    ]
  }
  ```

#### 5.2.3 调整库存
- **路径**：`/api/inventories/{id}/adjust`
- **方法**：`POST`
- **请求体**：
  ```json
  {
    "quantity": 120,
    "reason": "库存盘点调整"
  }
  ```
- **响应**：
  ```json
  {
    "message": "库存调整成功"
  }
  ```

#### 5.2.4 库存预警
- **路径**：`/api/inventories/alert`
- **方法**：`GET`
- **响应**：
  ```json
  [
    {
      "id": 1,
      "warehouse_id": 1,
      "warehouse_name": "总仓库",
      "product_id": 1,
      "product_name": "商品名称",
      "sku": "SKU001",
      "quantity": 5,
      "min_stock": 10,
      "unit": "件"
    }
  ]
  ```

### 5.3 库存调拨API

#### 5.3.1 创建调拨单
- **路径**：`/api/inventory-transfers`
- **方法**：`POST`
- **请求体**：
  ```json
  {
    "from_warehouse_id": 1,
    "to_warehouse_id": 2,
    "items": [
      {
        "product_id": 1,
        "quantity": 10
      }
    ],
    "notes": "调拨备注"
  }
  ```
- **响应**：
  ```json
  {
    "id": 1,
    "from_warehouse_id": 1,
    "from_warehouse_name": "总仓库",
    "to_warehouse_id": 2,
    "to_warehouse_name": "区域仓",
    "status": "pending",
    "items": [
      {
        "product_id": 1,
        "product_name": "商品名称",
        "quantity": 10
      }
    ],
    "notes": "调拨备注"
  }
  ```

#### 5.3.2 确认调拨
- **路径**：`/api/inventory-transfers/{id}/confirm`
- **方法**：`POST`
- **响应**：
  ```json
  {
    "message": "调拨确认成功"
  }
  ```

### 5.4 库存统计API

#### 5.4.1 获取库存统计数据
- **路径**：`/api/inventories/stats`
- **方法**：`GET`
- **查询参数**：
  - `warehouse_id`：仓库ID
- **响应**：
  ```json
  {
    "total_products": 100,
    "total_quantity": 10000,
    "total_value": 1000000.00,
    "low_stock_products": 5,
    "out_of_stock_products": 2
  }
  ```

## 6. 测试计划

### 6.1 单元测试
- **测试库存模型**：验证库存创建、更新、调整等功能
- **测试库存服务**：验证库存入库、出库、调拨等核心业务逻辑
- **测试库存预警**：验证库存预警功能的准确性
- **测试库存统计**：验证库存统计数据的准确性

### 6.2 集成测试
- **测试API端点**：验证所有库存管理相关的API端点
- **测试订单集成**：验证订单与库存模块的集成
- **测试采购集成**：验证采购与库存模块的集成
- **测试调拨集成**：验证调拨功能的完整性

### 6.3 性能测试
- **测试库存更新**：验证高并发下的库存更新性能
- **测试库存查询**：验证大量库存数据下的查询性能
- **测试库存调拨**：验证库存调拨的性能

## 7. 实现注意事项

1. **数据一致性**：确保库存数据与订单、采购等模块的数据一致性
2. **事务处理**：使用数据库事务确保库存相关操作的原子性
3. **并发控制**：处理并发库存操作，避免数据冲突
4. **错误处理**：统一处理库存管理相关的错误，返回友好的错误信息
5. **日志记录**：记录库存相关的操作日志，便于审计和排查问题
6. **安全防护**：保护库存数据的安全，防止未授权访问
7. **可扩展性**：支持未来新增的仓库类型和库存管理需求

## 8. 依赖项

- **sqlalchemy**：用于数据库操作
- **pydantic**：用于数据验证
- **python-dotenv**：用于环境变量管理
