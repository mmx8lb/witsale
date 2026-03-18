# 知识图谱/Ontology模块规格说明

## 1. 需求背景

知识图谱/Ontology是Witsale系统的核心特色之一。系统需要利用知识图谱技术实现智能推荐、语义搜索、客户画像等功能，以提升销售效率和客户体验。知识图谱将整合企业的商品、客户、订单等数据，构建语义化的知识网络。

## 2. 技术方案

### 2.1 核心技术
- **知识图谱构建**：使用owlready2和rdflib构建和管理知识图谱
- **语义搜索**：基于知识图谱实现语义化的搜索功能
- **智能推荐**：利用知识图谱进行商品推荐、客户推荐等
- **客户画像**：基于知识图谱构建客户画像，提供个性化服务
- **知识推理**：利用本体推理能力，从现有知识中推导出新的知识

### 2.2 关键特性
- **知识图谱构建**：支持从结构化和非结构化数据中构建知识图谱
- **语义搜索**：支持基于语义的模糊搜索和精确搜索
- **智能推荐**：基于客户历史行为和知识图谱关系进行推荐
- **客户画像**：构建多维度的客户画像，支持精准营销
- **知识推理**：支持基于本体的推理，发现隐藏的知识关联
- **可视化**：支持知识图谱的可视化展示

## 3. 架构设计

### 3.1 模块结构
```
app/
├── api/
│   └── ontology.py          # 知识图谱相关API
├── core/
│   └── ontology.py          # 知识图谱核心逻辑
├── models/
│   ├── ontology.py           # 知识图谱模型
│   ├── concept.py            # 概念模型
│   └── relationship.py       # 关系模型
├── schemas/
│   └── ontology.py          # 知识图谱相关数据结构
└── services/
    └── ontology_service.py  # 知识图谱服务
```

### 3.2 数据流
1. 数据采集：从企业的商品、客户、订单等系统中采集数据
2. 知识抽取：从采集的数据中抽取实体、属性和关系
3. 知识图谱构建：将抽取的知识构建成知识图谱
4. 知识存储：将知识图谱存储到数据库或图数据库中
5. 知识推理：利用本体推理能力，从现有知识中推导出新的知识
6. 应用服务：为其他模块提供知识图谱相关的服务，如智能推荐、语义搜索等

## 4. 数据模型

### 4.1 概念模型 (Concept)
| 字段名 | 类型 | 描述 |
|-------|------|------|
| id | Integer | 概念ID |
| name | String | 概念名称 |
| type | String | 概念类型（商品、客户、订单等） |
| description | Text | 概念描述 |
| properties | JSONB | 概念属性 |
| created_at | DateTime | 创建时间 |
| updated_at | DateTime | 更新时间 |

### 4.2 关系模型 (Relationship)
| 字段名 | 类型 | 描述 |
|-------|------|------|
| id | Integer | 关系ID |
| source_id | Integer | 源概念ID |
| target_id | Integer | 目标概念ID |
| type | String | 关系类型（购买、关联、属于等） |
| properties | JSONB | 关系属性 |
| created_at | DateTime | 创建时间 |
| updated_at | DateTime | 更新时间 |

### 4.3 知识图谱模型 (Ontology)
| 字段名 | 类型 | 描述 |
|-------|------|------|
| id | Integer | 知识图谱ID |
| name | String | 知识图谱名称 |
| description | Text | 知识图谱描述 |
| version | String | 知识图谱版本 |
| created_at | DateTime | 创建时间 |
| updated_at | DateTime | 更新时间 |

## 5. API设计

### 5.1 知识图谱管理API

#### 5.1.1 创建知识图谱
- **路径**：`/api/ontologies`
- **方法**：`POST`
- **请求体**：
  ```json
  {
    "name": "销售知识图谱",
    "description": "企业销售相关的知识图谱",
    "version": "1.0"
  }
  ```
- **响应**：
  ```json
  {
    "id": 1,
    "name": "销售知识图谱",
    "description": "企业销售相关的知识图谱",
    "version": "1.0",
    "created_at": "2026-03-18T00:00:00"
  }
  ```

#### 5.1.2 获取知识图谱列表
- **路径**：`/api/ontologies`
- **方法**：`GET`
- **响应**：
  ```json
  [
    {
      "id": 1,
      "name": "销售知识图谱",
      "description": "企业销售相关的知识图谱",
      "version": "1.0",
      "created_at": "2026-03-18T00:00:00"
    }
  ]
  ```

### 5.2 概念管理API

#### 5.2.1 创建概念
- **路径**：`/api/concepts`
- **方法**：`POST`
- **请求体**：
  ```json
  {
    "name": "商品",
    "type": "product",
    "description": "销售的商品",
    "properties": {
      "category": "电子产品",
      "brand": "Apple"
    }
  }
  ```
- **响应**：
  ```json
  {
    "id": 1,
    "name": "商品",
    "type": "product",
    "description": "销售的商品",
    "properties": {
      "category": "电子产品",
      "brand": "Apple"
    },
    "created_at": "2026-03-18T00:00:00"
  }
  ```

#### 5.2.2 获取概念列表
- **路径**：`/api/concepts`
- **方法**：`GET`
- **查询参数**：
  - `type`：概念类型
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
        "name": "商品",
        "type": "product",
        "description": "销售的商品",
        "properties": {
          "category": "电子产品",
          "brand": "Apple"
        },
        "created_at": "2026-03-18T00:00:00"
      }
    ]
  }
  ```

### 5.3 关系管理API

#### 5.3.1 创建关系
- **路径**：`/api/relationships`
- **方法**：`POST`
- **请求体**：
  ```json
  {
    "source_id": 1,
    "target_id": 2,
    "type": "purchased",
    "properties": {
      "quantity": 2,
      "price": 1000.00,
      "date": "2026-03-18"
    }
  }
  ```
- **响应**：
  ```json
  {
    "id": 1,
    "source_id": 1,
    "target_id": 2,
    "type": "purchased",
    "properties": {
      "quantity": 2,
      "price": 1000.00,
      "date": "2026-03-18"
    },
    "created_at": "2026-03-18T00:00:00"
  }
  ```

#### 5.3.2 获取关系列表
- **路径**：`/api/relationships`
- **方法**：`GET`
- **查询参数**：
  - `source_id`：源概念ID
  - `target_id`：目标概念ID
  - `type`：关系类型
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
        "source_id": 1,
        "target_id": 2,
        "type": "purchased",
        "properties": {
          "quantity": 2,
          "price": 1000.00,
          "date": "2026-03-18"
        },
        "created_at": "2026-03-18T00:00:00"
      }
    ]
  }
  ```

### 5.4 语义搜索API

#### 5.4.1 语义搜索
- **路径**：`/api/ontology/search`
- **方法**：`GET`
- **查询参数**：
  - `query`：搜索关键词
  - `limit`：返回结果数量
- **响应**：
  ```json
  {
    "query": "智能手机",
    "results": [
      {
        "id": 1,
        "name": "iPhone 15",
        "type": "product",
        "score": 0.95,
        "properties": {
          "category": "智能手机",
          "brand": "Apple"
        }
      },
      {
        "id": 2,
        "name": "Galaxy S24",
        "type": "product",
        "score": 0.90,
        "properties": {
          "category": "智能手机",
          "brand": "Samsung"
        }
      }
    ]
  }
  ```

### 5.5 智能推荐API

#### 5.5.1 商品推荐
- **路径**：`/api/ontology/recommend/products`
- **方法**：`GET`
- **查询参数**：
  - `customer_id`：客户ID
  - `limit`：推荐数量
- **响应**：
  ```json
  {
    "customer_id": 1,
    "recommendations": [
      {
        "id": 1,
        "name": "iPhone 15",
        "type": "product",
        "score": 0.95,
        "reason": "基于您之前购买的Apple产品"
      },
      {
        "id": 3,
        "name": "AirPods Pro",
        "type": "product",
        "score": 0.85,
        "reason": "与您的iPhone 15配套使用"
      }
    ]
  }
  ```

#### 5.5.2 客户推荐
- **路径**：`/api/ontology/recommend/customers`
- **方法**：`GET`
- **查询参数**：
  - `product_id`：商品ID
  - `limit`：推荐数量
- **响应**：
  ```json
  {
    "product_id": 1,
    "recommendations": [
      {
        "id": 1,
        "name": "张三",
        "type": "customer",
        "score": 0.95,
        "reason": "经常购买Apple产品"
      },
      {
        "id": 2,
        "name": "李四",
        "type": "customer",
        "score": 0.80,
        "reason": "对智能手机有兴趣"
      }
    ]
  }
  ```

### 5.6 客户画像API

#### 5.6.1 获取客户画像
- **路径**：`/api/ontology/customer-profile/{customer_id}`
- **方法**：`GET`
- **响应**：
  ```json
  {
    "customer_id": 1,
    "name": "张三",
    "profile": {
      "demographics": {
        "age": 30,
        "gender": "male",
        "location": "北京市"
      },
      "preferences": {
        "brands": ["Apple", "Samsung"],
        "categories": ["智能手机", "笔记本电脑"]
      },
      "behavior": {
        "purchase_frequency": "monthly",
        "average_order_value": 5000.00
      }
    }
  }
  ```

## 6. 测试计划

### 6.1 单元测试
- **测试概念管理**：验证概念的创建、查询、更新等功能
- **测试关系管理**：验证关系的创建、查询、更新等功能
- **测试语义搜索**：验证语义搜索的准确性和性能
- **测试智能推荐**：验证推荐结果的相关性和准确性
- **测试客户画像**：验证客户画像的完整性和准确性

### 6.2 集成测试
- **测试API端点**：验证所有知识图谱相关的API端点
- **测试数据集成**：验证知识图谱与其他模块的数据集成
- **测试推理功能**：验证知识推理的正确性

### 6.3 性能测试
- **测试知识图谱构建**：验证大规模数据下的知识图谱构建性能
- **测试语义搜索**：验证复杂查询下的搜索性能
- **测试推荐系统**：验证推荐算法的性能

## 7. 实现注意事项

1. **数据质量**：确保输入数据的质量和一致性，避免知识图谱中的错误和冲突
2. **性能优化**：对知识图谱的查询和推理进行性能优化，确保系统响应速度
3. **可扩展性**：设计可扩展的知识图谱结构，支持未来新增的概念和关系
4. **错误处理**：统一处理知识图谱相关的错误，返回友好的错误信息
5. **日志记录**：记录知识图谱相关的操作日志，便于审计和排查问题
6. **安全防护**：保护知识图谱数据的安全，防止未授权访问
7. **可视化**：提供知识图谱的可视化工具，便于用户理解和使用

## 8. 依赖项

- **owlready2**：用于本体构建和管理
- **rdflib**：用于RDF数据处理
- **sqlalchemy**：用于数据库操作
- **pydantic**：用于数据验证
- **python-dotenv**：用于环境变量管理
