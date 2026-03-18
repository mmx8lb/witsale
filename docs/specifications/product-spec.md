# 商品管理模块规格说明

## 1. 需求背景

商品管理是企业销售管理系统的核心功能之一。系统需要支持商品的全生命周期管理，包括商品信息维护、分类管理、多级定价策略、特殊促销策略等。此外，还需要支持商品的库存管理、销售分析等功能。

## 2. 技术方案

### 2.1 核心技术
- **数据库设计**：使用PostgreSQL的JSONB、Array等高级特性存储商品属性和规格
- **定价策略**：实现基于客户级别、数量、时间等多维度的定价策略
- **特殊策略**：实现达赠、礼品、运补等特殊促销策略
- **搜索功能**：支持商品名称、描述、属性等多维度搜索

### 2.2 关键特性
- **多级分类**：支持商品的多级分类管理
- **商品属性**：支持自定义商品属性和规格
- **多级定价**：支持不同客户级别、不同数量的价格策略
- **特殊策略**：支持达赠、礼品、运补等特殊促销策略
- **库存管理**：与库存模块集成，实时显示库存状态

## 3. 架构设计

### 3.1 模块结构
```
app/
├── api/
│   └── product.py        # 商品相关API
├── core/
│   └── product.py        # 商品核心逻辑
├── models/
│   ├── product.py        # 商品模型
│   ├── category.py       # 分类模型
│   └── price.py          # 价格模型
├── schemas/
│   └── product.py        # 商品相关数据结构
└── services/
    └── product_service.py # 商品服务
```

### 3.2 数据流
1. 商品创建：管理员创建商品信息，包括基本信息、分类、属性、价格等
2. 商品查询：用户通过API查询商品信息，支持多种筛选条件
3. 价格计算：系统根据客户级别、购买数量等因素计算商品价格
4. 库存更新：商品销售或入库时，更新库存信息
5. 特殊策略应用：根据促销规则应用特殊策略

## 4. 数据模型

### 4.1 商品模型 (Product)
| 字段名 | 类型 | 描述 |
|-------|------|------|
| id | Integer | 商品ID |
| name | String | 商品名称 |
| description | Text | 商品描述 |
| category_id | Integer | 分类ID |
| brand | String | 品牌 |
| sku | String | 商品SKU |
| bar_code | String | 条形码 |
| attributes | JSONB | 商品属性（如颜色、尺寸等） |
| specifications | JSONB | 商品规格（如重量、体积等） |
| min_stock | Integer | 最小库存预警 |
| is_active | Boolean | 是否激活 |
| created_at | DateTime | 创建时间 |
| updated_at | DateTime | 更新时间 |

### 4.2 分类模型 (Category)
| 字段名 | 类型 | 描述 |
|-------|------|------|
| id | Integer | 分类ID |
| name | String | 分类名称 |
| parent_id | Integer | 父分类ID |
| level | Integer | 分类级别 |
| path | String | 分类路径 |
| created_at | DateTime | 创建时间 |
| updated_at | DateTime | 更新时间 |

### 4.3 价格模型 (Price)
| 字段名 | 类型 | 描述 |
|-------|------|------|
| id | Integer | 价格ID |
| product_id | Integer | 商品ID |
| customer_level_id | Integer | 客户级别ID |
| min_quantity | Integer | 最小数量 |
| max_quantity | Integer | 最大数量 |
| price | Decimal | 价格 |
| effective_from | DateTime | 生效时间 |
| effective_to | DateTime | 失效时间 |
| created_at | DateTime | 创建时间 |
| updated_at | DateTime | 更新时间 |

### 4.4 特殊策略模型 (SpecialStrategy)
| 字段名 | 类型 | 描述 |
|-------|------|------|
| id | Integer | 策略ID |
| name | String | 策略名称 |
| type | String | 策略类型（达赠、礼品、运补等） |
| product_id | Integer | 商品ID |
| condition | JSONB | 触发条件 |
| reward | JSONB | 奖励内容 |
| effective_from | DateTime | 生效时间 |
| effective_to | DateTime | 失效时间 |
| created_at | DateTime | 创建时间 |
| updated_at | DateTime | 更新时间 |

## 5. API设计

### 5.1 商品管理API

#### 5.1.1 创建商品
- **路径**：`/api/products`
- **方法**：`POST`
- **请求体**：
  ```json
  {
    "name": "商品名称",
    "description": "商品描述",
    "category_id": 1,
    "brand": "品牌名称",
    "sku": "SKU001",
    "bar_code": "1234567890",
    "attributes": {"color": "红色", "size": "M"},
    "specifications": {"weight": "1kg", "volume": "1000ml"},
    "min_stock": 10
  }
  ```
- **响应**：
  ```json
  {
    "id": 1,
    "name": "商品名称",
    "description": "商品描述",
    "category_id": 1,
    "brand": "品牌名称",
    "sku": "SKU001",
    "bar_code": "1234567890",
    "attributes": {"color": "红色", "size": "M"},
    "specifications": {"weight": "1kg", "volume": "1000ml"},
    "min_stock": 10,
    "is_active": true
  }
  ```

#### 5.1.2 获取商品列表
- **路径**：`/api/products`
- **方法**：`GET`
- **查询参数**：
  - `category_id`：分类ID
  - `brand`：品牌
  - `search`：搜索关键词
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
        "name": "商品名称",
        "description": "商品描述",
        "category_id": 1,
        "brand": "品牌名称",
        "sku": "SKU001",
        "bar_code": "1234567890",
        "attributes": {"color": "红色", "size": "M"},
        "specifications": {"weight": "1kg", "volume": "1000ml"},
        "min_stock": 10,
        "is_active": true
      }
    ]
  }
  ```

#### 5.1.3 获取商品详情
- **路径**：`/api/products/{id}`
- **方法**：`GET`
- **响应**：
  ```json
  {
    "id": 1,
    "name": "商品名称",
    "description": "商品描述",
    "category_id": 1,
    "brand": "品牌名称",
    "sku": "SKU001",
    "bar_code": "1234567890",
    "attributes": {"color": "红色", "size": "M"},
    "specifications": {"weight": "1kg", "volume": "1000ml"},
    "min_stock": 10,
    "is_active": true,
    "prices": [
      {
        "customer_level_id": 1,
        "min_quantity": 1,
        "max_quantity": 9,
        "price": 100.00
      },
      {
        "customer_level_id": 1,
        "min_quantity": 10,
        "max_quantity": 99,
        "price": 90.00
      }
    ]
  }
  ```

#### 5.1.4 更新商品
- **路径**：`/api/products/{id}`
- **方法**：`PUT`
- **请求体**：
  ```json
  {
    "name": "更新后的商品名称",
    "description": "更新后的商品描述",
    "category_id": 2,
    "brand": "更新后的品牌名称",
    "attributes": {"color": "蓝色", "size": "L"}
  }
  ```
- **响应**：
  ```json
  {
    "id": 1,
    "name": "更新后的商品名称",
    "description": "更新后的商品描述",
    "category_id": 2,
    "brand": "更新后的品牌名称",
    "sku": "SKU001",
    "bar_code": "1234567890",
    "attributes": {"color": "蓝色", "size": "L"},
    "specifications": {"weight": "1kg", "volume": "1000ml"},
    "min_stock": 10,
    "is_active": true
  }
  ```

#### 5.1.5 删除商品
- **路径**：`/api/products/{id}`
- **方法**：`DELETE`
- **响应**：
  ```json
  {
    "message": "商品删除成功"
  }
  ```

### 5.2 分类管理API

#### 5.2.1 创建分类
- **路径**：`/api/categories`
- **方法**：`POST`
- **请求体**：
  ```json
  {
    "name": "分类名称",
    "parent_id": null,
    "level": 1
  }
  ```
- **响应**：
  ```json
  {
    "id": 1,
    "name": "分类名称",
    "parent_id": null,
    "level": 1,
    "path": "1"
  }
  ```

#### 5.2.2 获取分类列表
- **路径**：`/api/categories`
- **方法**：`GET`
- **响应**：
  ```json
  [
    {
      "id": 1,
      "name": "分类名称",
      "parent_id": null,
      "level": 1,
      "path": "1",
      "children": [
        {
          "id": 2,
          "name": "子分类名称",
          "parent_id": 1,
          "level": 2,
          "path": "1/2"
        }
      ]
    }
  ]
  ```

### 5.3 价格管理API

#### 5.3.1 设置商品价格
- **路径**：`/api/products/{id}/prices`
- **方法**：`POST`
- **请求体**：
  ```json
  [
    {
      "customer_level_id": 1,
      "min_quantity": 1,
      "max_quantity": 9,
      "price": 100.00,
      "effective_from": "2026-01-01T00:00:00",
      "effective_to": "2026-12-31T23:59:59"
    },
    {
      "customer_level_id": 1,
      "min_quantity": 10,
      "max_quantity": 99,
      "price": 90.00,
      "effective_from": "2026-01-01T00:00:00",
      "effective_to": "2026-12-31T23:59:59"
    }
  ]
  ```
- **响应**：
  ```json
  {
    "message": "价格设置成功"
  }
  ```

### 5.4 特殊策略API

#### 5.4.1 创建特殊策略
- **路径**：`/api/special-strategies`
- **方法**：`POST`
- **请求体**：
  ```json
  {
    "name": "达赠活动",
    "type": "gift",
    "product_id": 1,
    "condition": {"min_quantity": 10},
    "reward": {"product_id": 2, "quantity": 1},
    "effective_from": "2026-01-01T00:00:00",
    "effective_to": "2026-12-31T23:59:59"
  }
  ```
- **响应**：
  ```json
  {
    "id": 1,
    "name": "达赠活动",
    "type": "gift",
    "product_id": 1,
    "condition": {"min_quantity": 10},
    "reward": {"product_id": 2, "quantity": 1},
    "effective_from": "2026-01-01T00:00:00",
    "effective_to": "2026-12-31T23:59:59"
  }
  ```

## 6. 测试计划

### 6.1 单元测试
- **测试商品模型**：验证商品创建、更新、删除等功能
- **测试价格计算**：验证不同客户级别、不同数量的价格计算
- **测试特殊策略**：验证达赠、礼品、运补等特殊策略的应用
- **测试分类管理**：验证分类的创建、查询、层级关系等

### 6.2 集成测试
- **测试API端点**：验证所有商品管理相关的API端点
- **测试库存集成**：验证商品与库存模块的集成
- **测试订单集成**：验证商品与订单模块的集成

### 6.3 性能测试
- **测试商品搜索**：验证大量商品数据下的搜索性能
- **测试价格计算**：验证复杂价格策略下的计算性能
- **测试库存更新**：验证高并发下的库存更新性能

## 7. 实现注意事项

1. **数据一致性**：确保商品信息、价格、库存等数据的一致性
2. **性能优化**：对商品搜索、价格计算等高频操作进行性能优化
3. **灵活性**：设计灵活的商品属性和规格管理机制
4. **可扩展性**：支持未来新增的商品类型和属性
5. **错误处理**：统一处理商品管理相关的错误，返回友好的错误信息
6. **日志记录**：记录商品管理相关的操作日志，便于审计和排查问题

## 8. 依赖项

- **sqlalchemy**：用于数据库操作
- **pydantic**：用于数据验证
- **python-dotenv**：用于环境变量管理
