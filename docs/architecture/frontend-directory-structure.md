# 前端目录结构设计

## 1. 目录结构调整建议

基于之前的技术栈讨论和项目需求，对前端目录结构进行如下调整：

```
frontend/
 ├── apps/                    # 应用集合
 │   ├── web/                # Web端应用
 │   │   ├── admin/          # 内部管理端（Ant Design）
 │   │   ├── portal/         # 企业门户（轻量级UI框架）
 │   │   └── mall/           # 商城（轻量级UI框架）
 │   └── mobile/             # 移动端应用
 │       ├── field/          # 外勤App（Expo）
 │       ├── vip/            # 核心客户App（Expo）
 │       └── customer/       # 普通客户App（Expo）
 ├── packages/               # 共享包
 │   ├── ui/                 # 共享UI组件
 │   │   ├── web/            # Web端共享组件
 │   │   └── mobile/         # 移动端共享组件
 │   ├── utils/              # 共享工具函数
 │   ├── types/              # 共享类型定义
 │   ├── api/                # API客户端
 │   └── config/             # 共享配置
 ├── scripts/                # 脚本工具
 ├── turbo.json              # Turborepo配置
 ├── package.json            # 根package.json
 └── README.md               # 前端项目说明
```

## 2. 调整理由

### 2.1 按平台分类

- **web/**：包含所有Web端应用，使用React 18+ + Vite
- **mobile/**：包含所有移动端应用，使用Expo + React Native

这样分类更清晰，便于管理不同平台的应用。

### 2.2 共享包优化

- **ui/**：按平台分为web和mobile子目录，确保组件在对应平台上的兼容性
- **api/**：新增API客户端包，统一管理所有API调用
- **scripts/**：新增脚本目录，存放构建、部署等脚本

### 2.3 技术栈适配

- **Web端**：
  - admin：使用Ant Design of React
  - portal/mall：使用轻量级UI框架（Tailwind CSS或Chakra UI）

- **移动端**：
  - 全部使用Expo + React Native
  - 共享移动端组件

## 3. 目录结构说明

### 3.1 apps/web/

- **admin/**：内部管理端
  - 使用Ant Design of React
  - 复杂的企业级管理界面
  - 完整的RBAC权限控制

- **portal/**：企业门户
  - 使用轻量级UI框架
  - 企业形象展示
  - 产品介绍和新闻资讯

- **mall/**：商城
  - 使用轻量级UI框架
  - 商品展示和购买
  - 订单管理

### 3.2 apps/mobile/

- **field/**：外勤App
  - 打卡和轨迹记录
  - 客户拜访管理
  - 离线操作支持

- **vip/**：核心客户App
  - 专属服务和优惠
  - 订单和库存查询
  - 个性化推荐

- **customer/**：普通客户App
  - 商品购买
  - 订单跟踪
  - 基本服务

### 3.3 packages/

- **ui/web/**：Web端共享组件
  - 表单组件
  - 数据展示组件
  - 布局组件

- **ui/mobile/**：移动端共享组件
  - 移动端专用组件
  - 触摸友好的交互元素

- **utils/**：共享工具函数
  - 日期处理
  - 数据转换
  - 验证函数

- **types/**：共享类型定义
  - API响应类型
  - 业务模型类型
  - 配置类型

- **api/**：API客户端
  - 统一的API调用封装
  - 错误处理
  - 认证管理

- **config/**：共享配置
  - 环境变量
  - 应用配置
  - 主题配置

### 3.4 scripts/

- 构建脚本
- 部署脚本
- 代码质量检查脚本

## 4. 技术实现要点

### 4.1 包管理

- 使用pnpm作为包管理器，支持workspace
- 使用Turborepo进行高效的monorepo管理

### 4.2 构建配置

- Web端：Vite + TypeScript
- 移动端：Expo + TypeScript

### 4.3 代码规范

- ESLint + Prettier
- 统一的代码风格
- 类型检查

### 4.4 测试策略

- 单元测试：Jest
- 集成测试：React Testing Library
- E2E测试：Cypress（Web）、Detox（移动端）

## 5. 优势

1. **清晰的平台分离**：Web和移动端分开管理，便于针对不同平台优化
2. **共享代码最大化**：通过packages目录，减少重复代码
3. **技术栈适配**：针对不同应用场景选择合适的UI框架
4. **可扩展性**：模块化设计，便于添加新的应用或功能
5. **维护性**：结构清晰，便于团队协作和代码维护

## 6. 实施建议

1. 先搭建基础目录结构
2. 配置Turborepo和pnpm workspace
3. 创建共享包的基础结构
4. 分别初始化Web和移动端应用
5. 逐步实现各个应用的功能

通过以上目录结构设计，可以有效管理Witsale项目的前端代码，确保不同端的应用都能高效开发和维护。