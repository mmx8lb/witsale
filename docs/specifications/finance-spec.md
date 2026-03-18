# 财务管理模块规格说明

## 1. 需求背景

财务管理是企业销售管理系统的重要功能之一。系统需要支持多种结算方式，包括在线支付、线下支付、信用结算等。此外，还需要支持财务报表、账户管理、收支管理等功能。

## 2. 技术方案

### 2.1 核心技术
- **多结算方式**：支持在线支付、线下支付、信用结算等多种结算方式
- **财务报表**：生成各种财务报表，如收支报表、利润报表、现金流报表等
- **账户管理**：管理企业和客户的账户信息
- **收支管理**：记录和管理企业的收入和支出
- **发票管理**：支持发票的开具、管理和查询

### 2.2 关键特性
- **多结算方式**：支持在线支付、线下支付、信用结算等多种结算方式
- **财务报表**：生成各种财务报表，如收支报表、利润报表、现金流报表等
- **账户管理**：管理企业和客户的账户信息
- **收支管理**：记录和管理企业的收入和支出
- **发票管理**：支持发票的开具、管理和查询
- **财务分析**：提供财务数据的分析和预测

## 3. 架构设计

### 3.1 模块结构
```
app/
├── api/
│   └── finance.py          # 财务相关API
├── core/
│   └── finance.py          # 财务核心逻辑
├── models/
│   ├── account.py           # 账户模型
│   ├── transaction.py       # 交易模型
│   ├── invoice.py           # 发票模型
│   └── financial_report.py  # 财务报表模型
├── schemas/
│   └── finance.py          # 财务相关数据结构
└── services/
    └── finance_service.py  # 财务服务
```

### 3.2 数据流
1. 交易记录：记录企业的收入和支出
2. 账户管理：管理企业和客户的账户信息
3. 结算处理：处理各种结算方式的交易
4. 发票开具：为交易开具发票
5. 报表生成：生成各种财务报表
6. 财务分析：分析财务数据，提供决策支持

## 4. 数据模型

### 4.1 账户模型 (Account)
| 字段名 | 类型 | 描述 |
|-------|------|------|
| id | Integer | 账户ID |
| name | String | 账户名称 |
| type | String | 账户类型（企业账户、客户账户、银行账户等） |
| balance | Decimal | 账户余额 |
| currency | String | 货币类型 |
| status | String | 账户状态 |
| created_at | DateTime | 创建时间 |
| updated_at | DateTime | 更新时间 |

### 4.2 交易模型 (Transaction)
| 字段名 | 类型 | 描述 |
|-------|------|------|
| id | Integer | 交易ID |
| transaction_no | String | 交易编号 |
| account_id | Integer | 账户ID |
| type | String | 交易类型（收入、支出） |
| amount | Decimal | 交易金额 |
| currency | String | 货币类型 |
| status | String | 交易状态 |
| payment_method | String | 支付方式 |
| reference_type | String | 参考类型（订单、采购单等） |
| reference_id | Integer | 参考ID |
| notes | Text | 交易备注 |
| created_at | DateTime | 创建时间 |
| updated_at | DateTime | 更新时间 |

### 4.3 发票模型 (Invoice)
| 字段名 | 类型 | 描述 |
|-------|------|------|
| id | Integer | 发票ID |
| invoice_no | String | 发票编号 |
| transaction_id | Integer | 交易ID |
| customer_id | Integer | 客户ID |
| customer_name | String | 客户名称 |
| amount | Decimal | 发票金额 |
| tax_amount | Decimal | 税额 |
| total_amount | Decimal | 总金额 |
| status | String | 发票状态 |
| issued_date | DateTime | 开具日期 |
| due_date | DateTime | 到期日期 |
| notes | Text | 发票备注 |
| created_at | DateTime | 创建时间 |
| updated_at | DateTime | 更新时间 |

### 4.4 财务报表模型 (FinancialReport)
| 字段名 | 类型 | 描述 |
|-------|------|------|
| id | Integer | 报表ID |
| report_type | String | 报表类型（收支报表、利润报表、现金流报表等） |
| period | String | 报表期间 |
| start_date | Date | 开始日期 |
| end_date | Date | 结束日期 |
| data | JSONB | 报表数据 |
| created_at | DateTime | 创建时间 |
| created_by | Integer | 创建人ID |

## 5. API设计

### 5.1 账户管理API

#### 5.1.1 创建账户
- **路径**：`/api/accounts`
- **方法**：`POST`
- **请求体**：
  ```json
  {
    "name": "企业账户",
    "type": "enterprise",
    "balance": 10000.00,
    "currency": "CNY"
  }
  ```
- **响应**：
  ```json
  {
    "id": 1,
    "name": "企业账户",
    "type": "enterprise",
    "balance": 10000.00,
    "currency": "CNY",
    "status": "active"
  }
  ```

#### 5.1.2 获取账户列表
- **路径**：`/api/accounts`
- **方法**：`GET`
- **响应**：
  ```json
  [
    {
      "id": 1,
      "name": "企业账户",
      "type": "enterprise",
      "balance": 10000.00,
      "currency": "CNY",
      "status": "active"
    }
  ]
  ```

### 5.2 交易管理API

#### 5.2.1 创建交易
- **路径**：`/api/transactions`
- **方法**：`POST`
- **请求体**：
  ```json
  {
    "account_id": 1,
    "type": "income",
    "amount": 1000.00,
    "currency": "CNY",
    "payment_method": "online",
    "reference_type": "order",
    "reference_id": 1,
    "notes": "订单支付"
  }
  ```
- **响应**：
  ```json
  {
    "id": 1,
    "transaction_no": "TRA202603180001",
    "account_id": 1,
    "type": "income",
    "amount": 1000.00,
    "currency": "CNY",
    "status": "completed",
    "payment_method": "online",
    "reference_type": "order",
    "reference_id": 1,
    "notes": "订单支付"
  }
  ```

#### 5.2.2 获取交易列表
- **路径**：`/api/transactions`
- **方法**：`GET`
- **查询参数**：
  - `account_id`：账户ID
  - `type`：交易类型
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
        "transaction_no": "TRA202603180001",
        "account_id": 1,
        "type": "income",
        "amount": 1000.00,
        "currency": "CNY",
        "status": "completed",
        "payment_method": "online",
        "reference_type": "order",
        "reference_id": 1,
        "created_at": "2026-03-18T00:00:00"
      }
    ]
  }
  ```

### 5.3 发票管理API

#### 5.3.1 创建发票
- **路径**：`/api/invoices`
- **方法**：`POST`
- **请求体**：
  ```json
  {
    "transaction_id": 1,
    "customer_id": 1,
    "customer_name": "客户名称",
    "amount": 1000.00,
    "tax_amount": 100.00,
    "total_amount": 1100.00,
    "due_date": "2026-04-18T00:00:00",
    "notes": "发票备注"
  }
  ```
- **响应**：
  ```json
  {
    "id": 1,
    "invoice_no": "INV202603180001",
    "transaction_id": 1,
    "customer_id": 1,
    "customer_name": "客户名称",
    "amount": 1000.00,
    "tax_amount": 100.00,
    "total_amount": 1100.00,
    "status": "issued",
    "issued_date": "2026-03-18T00:00:00",
    "due_date": "2026-04-18T00:00:00",
    "notes": "发票备注"
  }
  ```

#### 5.3.2 获取发票列表
- **路径**：`/api/invoices`
- **方法**：`GET`
- **查询参数**：
  - `customer_id`：客户ID
  - `status`：发票状态
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
        "invoice_no": "INV202603180001",
        "customer_name": "客户名称",
        "total_amount": 1100.00,
        "status": "issued",
        "issued_date": "2026-03-18T00:00:00",
        "due_date": "2026-04-18T00:00:00"
      }
    ]
  }
  ```

### 5.4 财务报表API

#### 5.4.1 生成财务报表
- **路径**：`/api/financial-reports`
- **方法**：`POST`
- **请求体**：
  ```json
  {
    "report_type": "income_expense",
    "period": "monthly",
    "start_date": "2026-03-01",
    "end_date": "2026-03-31"
  }
  ```
- **响应**：
  ```json
  {
    "id": 1,
    "report_type": "income_expense",
    "period": "monthly",
    "start_date": "2026-03-01",
    "end_date": "2026-03-31",
    "data": {
      "income": 10000.00,
      "expense": 5000.00,
      "profit": 5000.00
    }
  }
  ```

#### 5.4.2 获取财务报表列表
- **路径**：`/api/financial-reports`
- **方法**：`GET`
- **查询参数**：
  - `report_type`：报表类型
  - `period`：报表期间
  - `start_date`：开始日期
  - `end_date`：结束日期
- **响应**：
  ```json
  [
    {
      "id": 1,
      "report_type": "income_expense",
      "period": "monthly",
      "start_date": "2026-03-01",
      "end_date": "2026-03-31",
      "created_at": "2026-03-31T23:59:59"
    }
  ]
  ```

## 6. 测试计划

### 6.1 单元测试
- **测试账户模型**：验证账户创建、更新、余额变动等功能
- **测试交易服务**：验证交易创建、状态更新、金额计算等功能
- **测试发票服务**：验证发票开具、状态管理等功能
- **测试报表生成**：验证财务报表的准确性

### 6.2 集成测试
- **测试API端点**：验证所有财务管理相关的API端点
- **测试订单集成**：验证订单与财务模块的集成
- **测试支付集成**：验证支付与财务模块的集成
- **测试报表集成**：验证报表与其他模块的集成

### 6.3 性能测试
- **测试交易处理**：验证高并发下的交易处理性能
- **测试报表生成**：验证大量数据下的报表生成性能
- **测试账户余额更新**：验证账户余额更新的性能

## 7. 实现注意事项

1. **数据一致性**：确保财务数据与订单、支付等模块的数据一致性
2. **事务处理**：使用数据库事务确保财务相关操作的原子性
3. **并发控制**：处理并发财务操作，避免数据冲突
4. **错误处理**：统一处理财务管理相关的错误，返回友好的错误信息
5. **日志记录**：记录财务相关的操作日志，便于审计和排查问题
6. **安全防护**：保护财务数据的安全，防止未授权访问
7. **可扩展性**：支持未来新增的财务功能和结算方式

## 8. 依赖项

- **sqlalchemy**：用于数据库操作
- **pydantic**：用于数据验证
- **python-dotenv**：用于环境变量管理
- **python-jose**：用于JWT认证
