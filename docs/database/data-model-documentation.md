# Witsale 数据模型文档

## 1. 模型概览

Witsale 系统包含以下核心模块的数据模型：

- **用户与权限**：用户、角色、权限管理
- **商品管理**：商品分类、商品、SKU、价格、属性
- **订单管理**：订单、订单明细、支付记录、状态历史、退款
- **客户管理**：客户、客户分类、客户等级、联系人、地址、标签
- **库存管理**：仓库、库存、库存变动、调拨、盘点
- **财务管理**：账户、交易、发票、财务报表

## 2. 用户与权限模型

### 2.1 User (用户)

| 字段名 | 类型 | 描述 | 约束 |
|-------|------|------|------|
| id | Integer | 用户ID | 主键，索引 |
| username | String(50) | 用户名 | 唯一，索引，非空 |
| email | String(100) | 邮箱 | 唯一，索引，非空 |
| password_hash | String(255) | 密码哈希 | 非空 |
| phone | String(20) | 电话 | 可空 |
| role_id | Integer | 角色ID | 外键，非空 |
| is_active | Boolean | 是否激活 | 默认True |
| created_at | DateTime | 创建时间 | 默认当前时间 |
| updated_at | DateTime | 更新时间 | 默认当前时间，自动更新 |

**关系**：
- 与 Role 是多对一关系

### 2.2 Role (角色)

| 字段名 | 类型 | 描述 | 约束 |
|-------|------|------|------|
| id | Integer | 角色ID | 主键，索引 |
| name | String(50) | 角色名称 | 唯一，非空 |
| description | String(255) | 角色描述 | 可空 |
| created_at | DateTime | 创建时间 | 默认当前时间 |
| updated_at | DateTime | 更新时间 | 默认当前时间，自动更新 |

**关系**：
- 与 User 是一对多关系
- 与 Permission 是多对多关系（通过 role_permissions 表）

### 2.3 Permission (权限)

| 字段名 | 类型 | 描述 | 约束 |
|-------|------|------|------|
| id | Integer | 权限ID | 主键，索引 |
| name | String(50) | 权限名称 | 唯一，非空 |
| code | String(50) | 权限代码 | 唯一，非空 |
| description | String(255) | 权限描述 | 可空 |
| created_at | DateTime | 创建时间 | 默认当前时间 |
| updated_at | DateTime | 更新时间 | 默认当前时间，自动更新 |

**关系**：
- 与 Role 是多对多关系（通过 role_permissions 表）

### 2.4 RolePermission (角色权限关联)

| 字段名 | 类型 | 描述 | 约束 |
|-------|------|------|------|
| id | Integer | 关联ID | 主键，索引 |
| role_id | Integer | 角色ID | 外键，非空 |
| permission_id | Integer | 权限ID | 外键，非空 |

## 3. 商品管理模型

### 3.1 Category (商品分类)

| 字段名 | 类型 | 描述 | 约束 |
|-------|------|------|------|
| id | Integer | 分类ID | 主键，索引 |
| name | String(100) | 分类名称 | 非空 |
| parent_id | Integer | 父分类ID | 外键，可空 |
| level | Integer | 分类级别 | 非空，默认1 |
| sort | Integer | 排序 | 非空，默认0 |
| is_active | Boolean | 是否激活 | 默认True |
| created_at | DateTime | 创建时间 | 默认当前时间 |
| updated_at | DateTime | 更新时间 | 默认当前时间，自动更新 |

**关系**：
- 自关联（父子关系）
- 与 Product 是一对多关系

### 3.2 Product (商品)

| 字段名 | 类型 | 描述 | 约束 |
|-------|------|------|------|
| id | Integer | 商品ID | 主键，索引 |
| name | String(200) | 商品名称 | 非空，索引 |
| description | Text | 商品描述 | 可空 |
| category_id | Integer | 分类ID | 外键，非空 |
| brand | String(100) | 品牌 | 可空 |
| model | String(100) | 型号 | 可空 |
| is_active | Boolean | 是否激活 | 默认True |
| created_at | DateTime | 创建时间 | 默认当前时间 |
| updated_at | DateTime | 更新时间 | 默认当前时间，自动更新 |

**关系**：
- 与 Category 是多对一关系
- 与 ProductSKU 是一对多关系
- 与 ProductAttribute 是一对多关系

### 3.3 ProductSKU (商品SKU)

| 字段名 | 类型 | 描述 | 约束 |
|-------|------|------|------|
| id | Integer | SKU ID | 主键，索引 |
| product_id | Integer | 商品ID | 外键，非空 |
| sku_code | String(50) | SKU代码 | 非空，唯一，索引 |
| name | String(200) | SKU名称 | 非空 |
| stock | Integer | 库存 | 非空，默认0 |
| cost_price | Float | 成本价 | 非空，默认0.0 |
| weight | Float | 重量 | 可空 |
| volume | Float | 体积 | 可空 |
| attributes | JSON | SKU属性 | 可空 |
| is_active | Boolean | 是否激活 | 默认True |
| created_at | DateTime | 创建时间 | 默认当前时间 |
| updated_at | DateTime | 更新时间 | 默认当前时间，自动更新 |

**关系**：
- 与 Product 是多对一关系
- 与 ProductPrice 是一对多关系

### 3.4 ProductPrice (商品价格)

| 字段名 | 类型 | 描述 | 约束 |
|-------|------|------|------|
| id | Integer | 价格ID | 主键，索引 |
| sku_id | Integer | SKU ID | 外键，非空 |
| price_type | String(20) | 价格类型 | 非空 |
| price | Float | 价格 | 非空 |
| min_quantity | Integer | 最小数量 | 非空，默认1 |
| max_quantity | Integer | 最大数量 | 可空 |
| is_active | Boolean | 是否激活 | 默认True |
| created_at | DateTime | 创建时间 | 默认当前时间 |
| updated_at | DateTime | 更新时间 | 默认当前时间，自动更新 |

**关系**：
- 与 ProductSKU 是多对一关系

### 3.5 ProductAttribute (商品属性)

| 字段名 | 类型 | 描述 | 约束 |
|-------|------|------|------|
| id | Integer | 属性ID | 主键，索引 |
| product_id | Integer | 商品ID | 外键，非空 |
| name | String(100) | 属性名称 | 非空 |
| value | JSON | 属性值 | 非空 |
| is_active | Boolean | 是否激活 | 默认True |
| created_at | DateTime | 创建时间 | 默认当前时间 |
| updated_at | DateTime | 更新时间 | 默认当前时间，自动更新 |

**关系**：
- 与 Product 是多对一关系

## 4. 订单管理模型

### 4.1 Order (订单主表)

| 字段名 | 类型 | 描述 | 约束 |
|-------|------|------|------|
| id | Integer | 订单ID | 主键，索引 |
| order_no | String(50) | 订单号 | 非空，唯一，索引 |
| customer_id | Integer | 客户ID | 非空，索引 |
| customer_name | String(200) | 客户名称 | 非空 |
| order_type | String(20) | 订单类型 | 非空，默认"sales" |
| order_level | String(20) | 订单级别 | 非空，默认"enterprise" |
| parent_order_id | Integer | 父订单ID | 外键，可空 |
| total_amount | Float | 总金额 | 非空，默认0.0 |
| actual_amount | Float | 实际金额 | 非空，默认0.0 |
| discount_amount | Float | 折扣金额 | 非空，默认0.0 |
| payment_method | String(50) | 支付方式 | 可空 |
| payment_status | String(20) | 支付状态 | 非空，默认"unpaid" |
| order_status | String(20) | 订单状态 | 非空，默认"pending" |
| shipping_address | JSON | 收货地址 | 可空 |
| logistics_company | String(100) | 物流公司 | 可空 |
| tracking_number | String(100) | 物流单号 | 可空 |
| notes | Text | 备注 | 可空 |
| created_by | Integer | 创建人ID | 可空 |
| updated_by | Integer | 更新人ID | 可空 |
| created_at | DateTime | 创建时间 | 默认当前时间 |
| updated_at | DateTime | 更新时间 | 默认当前时间，自动更新 |

**关系**：
- 自关联（父子关系）
- 与 OrderItem 是一对多关系
- 与 OrderPayment 是一对多关系
- 与 OrderStatusHistory 是一对多关系
- 与 OrderRefund 是一对多关系

### 4.2 OrderItem (订单商品明细)

| 字段名 | 类型 | 描述 | 约束 |
|-------|------|------|------|
| id | Integer | 明细ID | 主键，索引 |
| order_id | Integer | 订单ID | 外键，非空 |
| product_id | Integer | 商品ID | 非空 |
| product_name | String(200) | 商品名称 | 非空 |
| sku_id | Integer | SKU ID | 可空 |
| sku_code | String(50) | SKU代码 | 可空 |
| quantity | Integer | 数量 | 非空，默认1 |
| unit_price | Float | 单价 | 非空 |
| total_price | Float | 总价 | 非空 |
| discount_price | Float | 折扣价 | 非空，默认0.0 |
| attributes | JSON | 属性 | 可空 |
| created_at | DateTime | 创建时间 | 默认当前时间 |
| updated_at | DateTime | 更新时间 | 默认当前时间，自动更新 |

**关系**：
- 与 Order 是多对一关系

### 4.3 OrderPayment (订单支付记录)

| 字段名 | 类型 | 描述 | 约束 |
|-------|------|------|------|
| id | Integer | 支付记录ID | 主键，索引 |
| order_id | Integer | 订单ID | 外键，非空 |
| payment_no | String(50) | 支付单号 | 非空，唯一，索引 |
| payment_method | String(50) | 支付方式 | 非空 |
| amount | Float | 支付金额 | 非空 |
| transaction_id | String(100) | 交易ID | 可空 |
| payment_status | String(20) | 支付状态 | 非空，默认"pending" |
| paid_at | DateTime | 支付时间 | 可空 |
| notes | Text | 备注 | 可空 |
| created_at | DateTime | 创建时间 | 默认当前时间 |
| updated_at | DateTime | 更新时间 | 默认当前时间，自动更新 |

**关系**：
- 与 Order 是多对一关系

### 4.4 OrderStatusHistory (订单状态历史)

| 字段名 | 类型 | 描述 | 约束 |
|-------|------|------|------|
| id | Integer | 历史记录ID | 主键，索引 |
| order_id | Integer | 订单ID | 外键，非空 |
| status | String(20) | 状态 | 非空 |
| previous_status | String(20) | 之前状态 | 可空 |
| description | Text | 描述 | 可空 |
| operator_id | Integer | 操作人ID | 可空 |
| operator_name | String(100) | 操作人名称 | 可空 |
| created_at | DateTime | 创建时间 | 默认当前时间 |

**关系**：
- 与 Order 是多对一关系

### 4.5 OrderRefund (订单退款记录)

| 字段名 | 类型 | 描述 | 约束 |
|-------|------|------|------|
| id | Integer | 退款记录ID | 主键，索引 |
| order_id | Integer | 订单ID | 外键，非空 |
| refund_no | String(50) | 退款单号 | 非空，唯一，索引 |
| refund_type | String(20) | 退款类型 | 非空 |
| refund_amount | Float | 退款金额 | 非空 |
| reason | Text | 退款原因 | 可空 |
| refund_status | String(20) | 退款状态 | 非空，默认"pending" |
| processed_at | DateTime | 处理时间 | 可空 |
| processed_by | Integer | 处理人ID | 可空 |
| notes | Text | 备注 | 可空 |
| created_at | DateTime | 创建时间 | 默认当前时间 |
| updated_at | DateTime | 更新时间 | 默认当前时间，自动更新 |

**关系**：
- 与 Order 是多对一关系

## 5. 客户管理模型

### 5.1 Customer (客户)

| 字段名 | 类型 | 描述 | 约束 |
|-------|------|------|------|
| id | Integer | 客户ID | 主键，索引 |
| name | String(200) | 客户名称 | 非空 |
| code | String(50) | 客户编码 | 非空，唯一，索引 |
| short_name | String(100) | 简称 | 可空 |
| type | String(20) | 客户类型 | 非空，默认"enterprise" |
| category_id | Integer | 分类ID | 外键，可空 |
| level_id | Integer | 等级ID | 外键，可空 |
| contact_name | String(100) | 联系人 | 可空 |
| contact_phone | String(50) | 联系电话 | 可空 |
| email | String(100) | 邮箱 | 可空 |
| website | String(200) | 网站 | 可空 |
| tax_no | String(50) | 税号 | 可空 |
| registered_capital | Float | 注册资本 | 可空 |
| business_scope | Text | 经营范围 | 可空 |
| founding_date | DateTime | 成立日期 | 可空 |
| status | String(20) | 状态 | 非空，默认"active" |
| total_spend | Float | 总消费 | 非空，默认0.0 |
| total_orders | Integer | 总订单数 | 非空，默认0 |
| credit_limit | Float | 信用额度 | 可空 |
| credit_balance | Float | 信用余额 | 非空，默认0.0 |
| remark | Text | 备注 | 可空 |
| is_active | Boolean | 是否激活 | 默认True |
| created_at | DateTime | 创建时间 | 默认当前时间 |
| updated_at | DateTime | 更新时间 | 默认当前时间，自动更新 |

**关系**：
- 与 CustomerCategory 是多对一关系
- 与 CustomerLevel 是多对一关系
- 与 CustomerContact 是一对多关系
- 与 CustomerAddress 是一对多关系
- 与 CustomerTag 是多对多关系（通过 customer_tag_relations 表）

### 5.2 CustomerCategory (客户分类)

| 字段名 | 类型 | 描述 | 约束 |
|-------|------|------|------|
| id | Integer | 分类ID | 主键，索引 |
| name | String(100) | 分类名称 | 非空，唯一 |
| code | String(50) | 分类编码 | 非空，唯一，索引 |
| description | Text | 描述 | 可空 |
| parent_category_id | Integer | 父分类ID | 外键，可空 |
| level | Integer | 级别 | 非空，默认1 |
| is_active | Boolean | 是否激活 | 默认True |
| created_at | DateTime | 创建时间 | 默认当前时间 |
| updated_at | DateTime | 更新时间 | 默认当前时间，自动更新 |

**关系**：
- 自关联（父子关系）
- 与 Customer 是一对多关系

### 5.3 CustomerLevel (客户等级)

| 字段名 | 类型 | 描述 | 约束 |
|-------|------|------|------|
| id | Integer | 等级ID | 主键，索引 |
| name | String(100) | 等级名称 | 非空，唯一 |
| code | String(50) | 等级编码 | 非空，唯一，索引 |
| description | Text | 描述 | 可空 |
| min_spend | Float | 最低消费 | 非空，默认0.0 |
| max_spend | Float | 最高消费 | 可空 |
| discount_rate | Float | 折扣率 | 非空，默认1.0 |
| priority | Integer | 优先级 | 非空，默认0 |
| is_active | Boolean | 是否激活 | 默认True |
| created_at | DateTime | 创建时间 | 默认当前时间 |
| updated_at | DateTime | 更新时间 | 默认当前时间，自动更新 |

**关系**：
- 与 Customer 是一对多关系

### 5.4 CustomerContact (客户联系人)

| 字段名 | 类型 | 描述 | 约束 |
|-------|------|------|------|
| id | Integer | 联系人ID | 主键，索引 |
| customer_id | Integer | 客户ID | 外键，非空 |
| name | String(100) | 姓名 | 非空 |
| position | String(100) | 职位 | 可空 |
| phone | String(50) | 电话 | 非空 |
| email | String(100) | 邮箱 | 可空 |
| is_primary | Boolean | 是否主联系人 | 默认False |
| remark | Text | 备注 | 可空 |
| created_at | DateTime | 创建时间 | 默认当前时间 |
| updated_at | DateTime | 更新时间 | 默认当前时间，自动更新 |

**关系**：
- 与 Customer 是多对一关系

### 5.5 CustomerAddress (客户地址)

| 字段名 | 类型 | 描述 | 约束 |
|-------|------|------|------|
| id | Integer | 地址ID | 主键，索引 |
| customer_id | Integer | 客户ID | 外键，非空 |
| type | String(20) | 地址类型 | 非空，默认"billing" |
| province | String(100) | 省份 | 非空 |
| city | String(100) | 城市 | 非空 |
| district | String(100) | 区县 | 非空 |
| address | String(500) | 详细地址 | 非空 |
| zip_code | String(20) | 邮编 | 可空 |
| is_default | Boolean | 是否默认 | 默认False |
| is_active | Boolean | 是否激活 | 默认True |
| created_at | DateTime | 创建时间 | 默认当前时间 |
| updated_at | DateTime | 更新时间 | 默认当前时间，自动更新 |

**关系**：
- 与 Customer 是多对一关系

### 5.6 CustomerTag (客户标签)

| 字段名 | 类型 | 描述 | 约束 |
|-------|------|------|------|
| id | Integer | 标签ID | 主键，索引 |
| name | String(100) | 标签名称 | 非空，唯一 |
| code | String(50) | 标签编码 | 非空，唯一，索引 |
| color | String(20) | 颜色 | 可空 |
| description | Text | 描述 | 可空 |
| is_active | Boolean | 是否激活 | 默认True |
| created_at | DateTime | 创建时间 | 默认当前时间 |
| updated_at | DateTime | 更新时间 | 默认当前时间，自动更新 |

**关系**：
- 与 Customer 是多对多关系（通过 customer_tag_relations 表）

### 5.7 CustomerTagRelation (客户标签关联)

| 字段名 | 类型 | 描述 | 约束 |
|-------|------|------|------|
| customer_id | Integer | 客户ID | 外键，主键 |
| tag_id | Integer | 标签ID | 外键，主键 |
| created_at | DateTime | 创建时间 | 默认当前时间 |

## 6. 库存管理模型

### 6.1 Warehouse (仓库)

| 字段名 | 类型 | 描述 | 约束 |
|-------|------|------|------|
| id | Integer | 仓库ID | 主键，索引 |
| name | String(200) | 仓库名称 | 非空 |
| code | String(50) | 仓库编码 | 非空，唯一，索引 |
| address | String(500) | 地址 | 可空 |
| contact_person | String(100) | 联系人 | 可空 |
| contact_phone | String(50) | 联系电话 | 可空 |
| warehouse_type | String(20) | 仓库类型 | 非空，默认"central" |
| level | Integer | 级别 | 非空，默认1 |
| parent_warehouse_id | Integer | 父仓库ID | 外键，可空 |
| is_active | Boolean | 是否激活 | 默认True |
| created_at | DateTime | 创建时间 | 默认当前时间 |
| updated_at | DateTime | 更新时间 | 默认当前时间，自动更新 |

**关系**：
- 自关联（父子关系）
- 与 Stock 是一对多关系
- 与 StockTransfer 是一对多关系（作为调出仓库）
- 与 StockTransfer 是一对多关系（作为调入仓库）

### 6.2 Stock (库存)

| 字段名 | 类型 | 描述 | 约束 |
|-------|------|------|------|
| id | Integer | 库存ID | 主键，索引 |
| warehouse_id | Integer | 仓库ID | 外键，非空 |
| product_id | Integer | 商品ID | 非空 |
| product_name | String(200) | 商品名称 | 非空 |
| sku_id | Integer | SKU ID | 可空 |
| sku_code | String(50) | SKU代码 | 可空 |
| quantity | Integer | 总数量 | 非空，默认0 |
| available_quantity | Integer | 可用数量 | 非空，默认0 |
| locked_quantity | Integer | 锁定数量 | 非空，默认0 |
| cost_price | Float | 成本价 | 非空，默认0.0 |
| min_stock | Integer | 最小库存 | 非空，默认0 |
| max_stock | Integer | 最大库存 | 可空 |
| batch_no | String(100) | 批次号 | 可空 |
| expiry_date | DateTime | 过期日期 | 可空 |
| attributes | JSON | 属性 | 可空 |
| is_active | Boolean | 是否激活 | 默认True |
| created_at | DateTime | 创建时间 | 默认当前时间 |
| updated_at | DateTime | 更新时间 | 默认当前时间，自动更新 |

**关系**：
- 与 Warehouse 是多对一关系
- 与 StockMovement 是一对多关系

### 6.3 StockMovement (库存变动记录)

| 字段名 | 类型 | 描述 | 约束 |
|-------|------|------|------|
| id | Integer | 变动记录ID | 主键，索引 |
| stock_id | Integer | 库存ID | 外键，非空 |
| movement_type | String(20) | 变动类型 | 非空 |
| quantity | Integer | 变动数量 | 非空 |
| before_quantity | Integer | 变动前数量 | 非空 |
| after_quantity | Integer | 变动后数量 | 非空 |
| reference_type | String(50) | 参考类型 | 可空 |
| reference_id | Integer | 参考ID | 可空 |
| reference_no | String(100) | 参考编号 | 可空 |
| remark | Text | 备注 | 可空 |
| operator_id | Integer | 操作人ID | 可空 |
| operator_name | String(100) | 操作人名称 | 可空 |
| created_at | DateTime | 创建时间 | 默认当前时间 |

**关系**：
- 与 Stock 是多对一关系

### 6.4 StockTransfer (库存调拨)

| 字段名 | 类型 | 描述 | 约束 |
|-------|------|------|------|
| id | Integer | 调拨ID | 主键，索引 |
| transfer_no | String(50) | 调拨单号 | 非空，唯一，索引 |
| from_warehouse_id | Integer | 调出仓库ID | 外键，非空 |
| to_warehouse_id | Integer | 调入仓库ID | 外键，非空 |
| transfer_type | String(20) | 调拨类型 | 非空，默认"normal" |
| transfer_status | String(20) | 调拨状态 | 非空，默认"pending" |
| total_quantity | Integer | 总数量 | 非空，默认0 |
| remark | Text | 备注 | 可空 |
| operator_id | Integer | 操作人ID | 可空 |
| operator_name | String(100) | 操作人名称 | 可空 |
| approved_by | Integer | 审批人ID | 可空 |
| approved_at | DateTime | 审批时间 | 可空 |
| shipped_at | DateTime | 发货时间 | 可空 |
| received_at | DateTime | 收货时间 | 可空 |
| created_at | DateTime | 创建时间 | 默认当前时间 |
| updated_at | DateTime | 更新时间 | 默认当前时间，自动更新 |

**关系**：
- 与 Warehouse 是多对一关系（作为调出仓库）
- 与 Warehouse 是多对一关系（作为调入仓库）
- 与 StockTransferItem 是一对多关系

### 6.5 StockTransferItem (库存调拨明细)

| 字段名 | 类型 | 描述 | 约束 |
|-------|------|------|------|
| id | Integer | 调拨明细ID | 主键，索引 |
| transfer_id | Integer | 调拨ID | 外键，非空 |
| product_id | Integer | 商品ID | 非空 |
| product_name | String(200) | 商品名称 | 非空 |
| sku_id | Integer | SKU ID | 可空 |
| sku_code | String(50) | SKU代码 | 可空 |
| quantity | Integer | 数量 | 非空 |
| shipped_quantity | Integer | 已发货数量 | 非空，默认0 |
| received_quantity | Integer | 已收货数量 | 非空，默认0 |
| remark | Text | 备注 | 可空 |
| created_at | DateTime | 创建时间 | 默认当前时间 |

**关系**：
- 与 StockTransfer 是多对一关系

### 6.6 StockCheck (库存盘点)

| 字段名 | 类型 | 描述 | 约束 |
|-------|------|------|------|
| id | Integer | 盘点ID | 主键，索引 |
| check_no | String(50) | 盘点单号 | 非空，唯一，索引 |
| warehouse_id | Integer | 仓库ID | 外键，非空 |
| check_type | String(20) | 盘点类型 | 非空，默认"full" |
| check_status | String(20) | 盘点状态 | 非空，默认"pending" |
| remark | Text | 备注 | 可空 |
| operator_id | Integer | 操作人ID | 可空 |
| operator_name | String(100) | 操作人名称 | 可空 |
| started_at | DateTime | 开始时间 | 可空 |
| completed_at | DateTime | 完成时间 | 可空 |
| created_at | DateTime | 创建时间 | 默认当前时间 |
| updated_at | DateTime | 更新时间 | 默认当前时间，自动更新 |

**关系**：
- 与 Warehouse 是多对一关系
- 与 StockCheckItem 是一对多关系

### 6.7 StockCheckItem (库存盘点明细)

| 字段名 | 类型 | 描述 | 约束 |
|-------|------|------|------|
| id | Integer | 盘点明细ID | 主键，索引 |
| check_id | Integer | 盘点ID | 外键，非空 |
| stock_id | Integer | 库存ID | 外键，非空 |
| product_id | Integer | 商品ID | 非空 |
| product_name | String(200) | 商品名称 | 非空 |
| sku_id | Integer | SKU ID | 可空 |
| sku_code | String(50) | SKU代码 | 可空 |
| system_quantity | Integer | 系统数量 | 非空 |
| actual_quantity | Integer | 实际数量 | 非空 |
| diff_quantity | Integer | 差异数量 | 非空 |
| remark | Text | 备注 | 可空 |
| created_at | DateTime | 创建时间 | 默认当前时间 |

**关系**：
- 与 StockCheck 是多对一关系

## 7. 财务管理模型

### 7.1 Account (账户)

| 字段名 | 类型 | 描述 | 约束 |
|-------|------|------|------|
| id | Integer | 账户ID | 主键，索引 |
| name | String(100) | 账户名称 | 非空，索引 |
| code | String(50) | 账户编码 | 非空，唯一，索引 |
| type | String(50) | 账户类型 | 非空，索引 |
| balance | Float | 余额 | 默认0.0 |
| currency | String(10) | 货币 | 默认"CNY" |
| status | String(20) | 状态 | 默认"active"，索引 |
| description | Text | 描述 | 可空 |
| created_at | DateTime | 创建时间 | 默认当前时间 |
| updated_at | DateTime | 更新时间 | 默认当前时间，自动更新 |

**关系**：
- 与 Transaction 是一对多关系
- 与 Invoice 是一对多关系

### 7.2 Transaction (交易)

| 字段名 | 类型 | 描述 | 约束 |
|-------|------|------|------|
| id | Integer | 交易ID | 主键，索引 |
| transaction_no | String(50) | 交易单号 | 非空，唯一，索引 |
| account_id | Integer | 账户ID | 外键，非空 |
| type | String(20) | 交易类型 | 非空，索引 |
| amount | Float | 金额 | 非空 |
| currency | String(10) | 货币 | 默认"CNY" |
| status | String(20) | 状态 | 默认"pending"，索引 |
| payment_method | String(50) | 支付方式 | 非空 |
| reference_type | String(50) | 参考类型 | 可空 |
| reference_id | Integer | 参考ID | 可空 |
| notes | Text | 备注 | 可空 |
| created_at | DateTime | 创建时间 | 默认当前时间 |
| updated_at | DateTime | 更新时间 | 默认当前时间，自动更新 |

**关系**：
- 与 Account 是多对一关系
- 与 Invoice 是一对多关系

### 7.3 Invoice (发票)

| 字段名 | 类型 | 描述 | 约束 |
|-------|------|------|------|
| id | Integer | 发票ID | 主键，索引 |
| invoice_no | String(50) | 发票号 | 非空，唯一，索引 |
| account_id | Integer | 账户ID | 外键，非空 |
| transaction_id | Integer | 交易ID | 外键，可空 |
| amount | Float | 金额 | 非空 |
| currency | String(10) | 货币 | 默认"CNY" |
| status | String(20) | 状态 | 默认"draft"，索引 |
| issue_date | DateTime | 开票日期 | 默认当前时间 |
| due_date | DateTime | 到期日期 | 可空 |
| tax_amount | Float | 税额 | 默认0.0 |
| total_amount | Float | 总金额 | 非空 |
| notes | Text | 备注 | 可空 |
| created_at | DateTime | 创建时间 | 默认当前时间 |
| updated_at | DateTime | 更新时间 | 默认当前时间，自动更新 |

**关系**：
- 与 Account 是多对一关系
- 与 Transaction 是多对一关系

### 7.4 FinancialReport (财务报表)

| 字段名 | 类型 | 描述 | 约束 |
|-------|------|------|------|
| id | Integer | 报表ID | 主键，索引 |
| report_name | String(100) | 报表名称 | 非空 |
| report_type | String(50) | 报表类型 | 非空，索引 |
| period_start | DateTime | 开始日期 | 非空 |
| period_end | DateTime | 结束日期 | 非空 |
| status | String(20) | 状态 | 默认"generated"，索引 |
| data | Text | 报表数据 | 可空 |
| created_at | DateTime | 创建时间 | 默认当前时间 |
| updated_at | DateTime | 更新时间 | 默认当前时间，自动更新 |

## 8. 关系图

### 8.1 核心实体关系

- **用户** → 角色 → 权限
- **商品** → 分类
- **商品** → SKU → 库存
- **商品** → SKU → 价格
- **订单** → 订单明细 → 商品
- **订单** → 支付记录
- **订单** → 状态历史
- **订单** → 退款记录
- **客户** → 客户分类
- **客户** → 客户等级
- **客户** → 联系人
- **客户** → 地址
- **客户** → 标签
- **仓库** → 库存
- **仓库** → 调拨单
- **账户** → 交易
- **交易** → 发票

## 9. 数据模型设计特点

1. **多级结构**：支持多级分类、多级仓库、多级订单等
2. **灵活的属性系统**：使用 JSON 类型存储灵活的属性数据
3. **完整的状态管理**：订单、库存、财务等都有完整的状态流转
4. **详细的审计记录**：状态变更都有历史记录
5. **多维度关联**：支持多对多关系，如客户与标签
6. **数据完整性**：通过外键约束确保数据一致性
7. **性能优化**：关键字段都有索引

## 10. 总结

Witsale 数据模型设计完整覆盖了企业销售管理系统的核心业务需求，包括用户权限、商品管理、订单管理、客户管理、库存管理和财务管理等模块。模型设计考虑了业务的复杂性和扩展性，支持多级结构、灵活属性和完整的状态管理，为系统的稳定运行和后续扩展提供了坚实的基础。