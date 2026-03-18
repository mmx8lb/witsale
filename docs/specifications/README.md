# Witsale 慧售 - 规格说明文档

## 文档概述

本目录包含 Witsale 慧售系统的所有规格说明文档，采用统一的组织结构，方便查阅和管理。

## 文档结构

### 核心规格说明

| 文档名称 | 描述 | 状态 |
|---------|------|------|
| [main-specification.md](main-specification.md) | 系统总体规格说明 | ✅ 已完成 |
| [auth-spec.md](auth-spec.md) | 用户认证与授权模块 | ✅ 已完成 |
| [product-spec.md](product-spec.md) | 商品管理模块 | ✅ 已完成 |
| [order-spec.md](order-spec.md) | 订单管理模块 | ✅ 已完成 |
| [inventory-spec.md](inventory-spec.md) | 库存管理模块 | ✅ 已完成 |
| [finance-spec.md](finance-spec.md) | 财务管理模块 | ✅ 已完成 |
| [field-spec.md](field-spec.md) | 外勤管理模块 | ✅ 已完成 |
| [ontology-spec.md](ontology-spec.md) | 知识图谱/Ontology模块 | ✅ 已完成 |

## 文档管理规范

1. **文档命名**：使用 `{module}-spec.md` 的命名格式
2. **文档结构**：每个规格说明文档应包含以下部分：
   - 模块概述
   - 需求分析
   - 技术方案
   - 架构设计
   - 数据模型
   - API设计
   - 测试计划
3. **版本控制**：文档应与代码版本保持同步
4. **更新机制**：任何需求变更或技术决策必须及时更新对应文档

## 查阅指南

1. 首先阅读 `main-specification.md` 了解系统总体架构
2. 然后根据需要查阅具体模块的规格说明
3. 所有文档均采用 Markdown 格式，支持在线阅读和本地查看

*Last updated: 2026-03-18*