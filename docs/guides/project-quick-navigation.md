# Witsale 慧售 - 项目快速导航与状态报告

## 📋 项目概览

- **项目名称**: Witsale (慧售)
- **类型**: 多端企业销售管理系统 (B2B+B2C)
- **技术栈**: FastAPI + PostgreSQL + Redis + React + React Native + 知识图谱
- **当前日期**: 2026-03-18

---

## 🚀 任务快速索引 (T1-T15)

| 任务ID | 任务名称 | 优先级 | 状态 | 定义文档 | 相关代码 |
|--------|----------|--------|------|----------|----------|
| **T1** | 后端项目初始化 | 高 | ✅ 已完成 | [开发计划](../guides/development-plan.md) | `app/main.py` |
| **T2** | 用户认证与授权系统 | 高 | ✅ 已完成 | [开发计划](../guides/development-plan.md) | `app/models/user.py`, `app/interfaces/api/v1/auth.py` |
| **T3** | 商品管理模块 | 高 | ✅ 已完成 | [开发计划](../guides/development-plan.md) | `app/models/product.py`, `app/application/services/product_service.py` |
| **T4** | 订单管理模块 | 高 | ✅ 已完成 | [开发计划](../guides/development-plan.md#34-t4-订单管理模块) | `app/models/order.py`, `app/application/services/order_service.py` |
| **T5** | 库存管理模块 | 高 | ✅ 已完成 | [开发计划](../guides/development-plan.md#35-t5-库存管理模块) | `app/models/inventory.py`, `app/application/services/inventory_service.py` |
| **T6** | 客户管理模块 | 中 | ✅ 已完成 | [开发计划](../guides/development-plan.md#36-t6-客户管理模块) | `app/models/customer.py`, `app/application/services/customer_service.py` |
| **T7** | 财务管理模块 | 中 | ⏳ 待开始 | [开发计划](../guides/development-plan.md#37-t7-财务管理模块) | 待创建 |
| **T8** | 外勤管理模块 | 中 | ⏳ 待开始 | [开发计划](../guides/development-plan.md#38-t8-外勤管理模块) | 待创建 |
| **T9** | 知识图谱集成 | 中 | ⏳ 待开始 | [开发计划](../guides/development-plan.md#39-t9-知识图谱集成) | 待创建 |
| **T10** | 内部管理端前端 | 中 | ⏳ 待开始 | [开发计划](../guides/development-plan.md#310-t10-内部管理端前端) | 待创建 |
| **T11** | 外部管理端前端 | 低 | ⏳ 待开始 | [开发计划](../guides/development-plan.md) | 待创建 |
| **T12** | 企业门户前端 | 低 | ⏳ 待开始 | [开发计划](../guides/development-plan.md) | 待创建 |
| **T13** | 商城前端 | 低 | ⏳ 待开始 | [开发计划](../guides/development-plan.md) | 待创建 |
| **T14** | 移动应用开发 | 低 | ⏳ 待开始 | [开发计划](../guides/development-plan.md) | 待创建 |
| **T15** | 系统集成与测试 | 低 | ⏳ 待开始 | [开发计划](../guides/development-plan.md) | 待创建 |

---

## 📊 当前进度看板

### ✅ 已完成 (6/15)

- **T1**: 后端项目初始化
- **T2**: 用户认证与授权系统
- **T3**: 商品管理模块
- **T4**: 订单管理模块
- **T5**: 库存管理模块
- **T6**: 客户管理模块

### 🚀 进行中 (0/15)

### ⏳ 待开始 (9/15)

- T7-T15

---

## 🔍 文档快速索引

### 核心文档
| 文档类型 | 位置 | 说明 |
|---------|------|------|
| 项目信息中心 | [README.md](../README.md) | 项目整体信息 |
| 需求文档 | [witsale-requirements.md](../requirements/witsale-requirements.md) | 业务需求梳理 |
| 开发计划 | [development-plan.md](../guides/development-plan.md) | **T1-T15详细定义** ⭐ |
| 开发流程 | [development-process.md](../guides/development-process.md) | 开发规范与流程 |
| 会议记录 | [2026-03-18-项目启动与需求梳理.md](../meetings/2026-03-18-项目启动与需求梳理.md) | 项目启动会议 |

### 技术架构
| 文档类型 | 位置 |
|---------|------|
| 后端架构 | [backend-implementation-plan.md](../architecture/backend-implementation-plan.md) |
| 前端架构 | [frontend-implementation-plan.md](../architecture/frontend-implementation-plan.md) |
| 数据库设计 | [schema.md](../database/schema.md) |
| API设计 | [api-design.md](../api/api-design.md) |

### 规格说明
| 模块 | 位置 |
|------|------|
| 主规格 | [main-specification.md](../specifications/main-specification.md) |
| 认证 | [auth-spec.md](../specifications/auth-spec.md) |
| 商品 | [product-spec.md](../specifications/product-spec.md) |
| 订单 | [order-spec.md](../specifications/order-spec.md) |
| 库存 | [inventory-spec.md](../specifications/inventory-spec.md) |
| 财务 | [finance-spec.md](../specifications/finance-spec.md) |

---

## 🎯 T5 库存管理模块 - 快速开始

### 📝 T5 任务定义

**任务ID**: T5  
**任务名称**: 库存管理模块  
**优先级**: 高  
**计划时间**: 14天 (2026-05-13 ~ 2026-05-26)

### 🔗 快速链接
- **详细定义**: [开发计划 - T5](../guides/development-plan.md#35-t5-库存管理模块)
- **规格说明**: [inventory-spec.md](../specifications/inventory-spec.md)

### 📋 T5 核心功能

1. **仓库管理** - 多级仓库体系、仓库信息维护
2. **库存管理** - 库存查询、库存变动、库存预警
3. **库存调拨** - 仓库间库存调拨流程
4. **库存盘点** - 库存盘点、差异处理
5. **与订单集成** - 订单扣库存、退款退库存

### 📂 代码结构快速导航

### 后端目录结构
```
backend/
├── app/
│   ├── models/              # 数据模型
│   │   ├── user.py         # T2: 用户模型
│   │   ├── product.py      # T3: 商品模型
│   │   ├── order.py        # T4: 订单模型
│   │   └── inventory.py    # T5: 库存模型
│   ├── schemas/             # Pydantic Schema
│   │   ├── auth.py         # T2: 认证Schema
│   │   ├── product.py      # T3: 商品Schema
│   │   ├── order.py        # T4: 订单Schema
│   │   └── inventory.py    # T5: 库存Schema
│   ├── application/         # 应用层
│   │   └── services/       # 服务层
│   │       ├── auth_service.py   # T2: 认证服务
│   │       ├── product_service.py # T3: 商品服务
│   │       ├── order_service.py   # T4: 订单服务
│   │       └── inventory_service.py # T5: 库存服务
│   ├── infrastructure/      # 基础设施层
│   │   └── persistence/    # 数据持久化
│   │       ├── product_repository.py # T3: 商品仓储
│   │       ├── order_repository.py   # T4: 订单仓储
│   │       └── inventory_repository.py # T5: 库存仓储
│   └── interfaces/api/     # 接口层
│       ├── routes.py       # 路由配置
│       └── v1/
│           ├── auth.py     # T2: 认证API
│           └── endpoints/
│               ├── product.py # T3: 商品API
│               ├── order.py   # T4: 订单API
│               └── inventory.py # T5: 库存API
├── alembic/versions/       # 数据库迁移
│   ├── b24043fb4d63_create_product_tables.py # T3: 商品迁移
│   ├── 9470a73312c3_create_order_tables.py   # T4: 订单迁移
│   └── xxx_create_inventory_tables.py         # T5: 库存迁移
└── tests/
    └── test_product.py     # T3: 商品测试
```

---

## 🔧 开发服务器

**当前状态**: ✅ 运行中  
**端口**: 8000  
**地址**: http://127.0.0.1:8000  
**API文档**: http://127.0.0.1:8000/docs

---

## 📞 快速帮助

### 常用命令
- `/spec` - 进入规格说明模式
- `/plan` - 进入实施计划模式
- `/help` - 显示帮助信息

### 下一个任务
当前T5进行中，完成后将开始**T6客户管理模块**！

---

*最后更新: 2026-03-18*
*本文档用于快速定位项目信息和状态*
