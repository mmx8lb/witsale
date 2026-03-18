# Witsale 项目目录结构审查报告

## 一、当前结构概览

```
witsale/
├── .git/
├── backend/                    # 后端服务
├── frontend-admin/             # 管理端Web
├── frontend-company/           # 公司页面
├── frontend-mall/              # 商城Web
├── mobile-field/               # 外勤App
├── mobile-key-customer/        # 核心客户App
├── mobile-customer/            # 普通客户App
├── shared/                     # 共享代码
└── docs/
    ├── requirements/
    ├── architecture/
    ├── api/
    └── database/
```

---

## 二、审查评估

### ✅ 优点

1. **Monorepo结构清晰** - 所有子项目在同一仓库，便于统一管理
2. **按应用类型拆分** - backend/frontend/mobile 分类明确
3. **文档独立目录** - docs/ 目录分层合理

---

### ⚠️ 问题与改进建议

#### 问题 1: 目录命名不统一，缺少前缀

**当前问题：**
- `frontend-admin/` vs `mobile-field/` - 命名风格不一致
- `frontend-company/` - "company" 语义不够明确
- `mobile-key-customer/` - 名称过长

**建议方案：**
```
apps/
├── backend/                    # 后端服务
├── web-admin/                  # 管理端（原frontend-admin）
├── web-portal/                 # 企业门户（原frontend-company，语义更清晰）
├── web-mall/                   # 商城（原frontend-mall）
├── app-field/                  # 外勤App（原mobile-field）
├── app-key-account/            # 核心客户App（原mobile-key-customer，更简洁）
└── app-customer/               # 普通客户App（原mobile-customer）
```

**调整理由：**
- 统一使用 `web-` 和 `app-` 前缀，类型一目了然
- `portal` 比 `company` 更准确（企业门户）
- `account` 比 `customer` 在App场景更通用

---

#### 问题 2: 缺少根级别配置文件

**当前问题：**
- 没有 `README.md` - 项目入口文档缺失
- 没有 `CONTRIBUTING.md` - 贡献指南缺失
- 没有 `docker-compose.yml` - 本地开发环境缺失
- 没有 `.gitignore` - Git忽略规则缺失

**建议添加：**
```
witsale/
├── README.md                   # 项目说明
├── CONTRIBUTING.md             # 贡献指南
├── docker-compose.yml          # 本地开发环境
├── .gitignore                  # Git忽略规则
├── .editorconfig               # 编辑器配置
├── Makefile                    # 常用命令封装
└── scripts/                    # 辅助脚本
    ├── setup.sh
    └── deploy.sh
```

---

#### 问题 3: shared/ 目录缺少细分，缺少品牌关联

**当前问题：**
- `shared/` 太笼统，没有明确用途
- 没有体现项目品牌 "witsale"

**建议方案（品牌化）：**
```
packages/                       # 共享包（替代shared）
├── witsale-types/              # 共享类型定义（品牌化）
├── witsale-utils/              # 共享工具函数（品牌化）
├── witsale-ui/                 # 共享UI组件（品牌化）
├── witsale-constants/          # 共享常量（品牌化）
└── witsale-validators/         # 共享验证器（品牌化）
```

或者更简单的：
```
shared/
├── types/                      # 类型定义
├── utils/                      # 工具函数
├── constants/                  # 常量
└── schemas/                    # 数据Schema
```

---

#### 问题 4: docs/ 可以更完善

**当前结构：**
```
docs/
├── requirements/
├── architecture/
├── api/
└── database/
```

**建议补充：**
```
docs/
├── requirements/               # 需求文档
├── architecture/               # 架构设计
├── api/                        # API文档
├── database/                   # 数据库设计
├── guides/                     # 开发指南
│   ├── backend.md
│   ├── frontend.md
│   └── mobile.md
├── deployments/                # 部署文档
│   ├── dev.md
│   ├── staging.md
│   └── prod.md
└── adr/                        # 架构决策记录 (ADR)
    ├── 001-tech-stack.md
    └── 002-monorepo.md
```

---

#### 问题 5: 缺少基础设施配置目录

**建议添加：**
```
infra/                          # 基础设施即代码
├── docker/                     # Docker相关
│   ├── backend.Dockerfile
│   └── frontend.Dockerfile
├── k8s/                        # Kubernetes配置（如需要）
└── terraform/                  # Terraform配置（如需要）
```

---

#### 问题 6: 移动端命名优化

**当前：**
- `mobile-field/`
- `mobile-key-customer/`
- `mobile-customer/`

**建议：**
```
apps/
├── app-field/                  # 外勤App
├── app-vip/                    # VIP客户App（更简洁）
└── app-customer/               # 普通客户App
```

---

## 三、推荐的完整目录结构

### 最终推荐方案（平衡实用性与规范性）

```
witsale/
├── .git/
├── .gitignore
├── .editorconfig
├── README.md
├── CONTRIBUTING.md
├── Makefile
├── docker-compose.yml
│
├── apps/                       # 所有应用
│   ├── backend/                # FastAPI后端服务
│   ├── web-admin/              # 管理端Web
│   ├── web-portal/             # 企业门户
│   ├── web-mall/               # 商城Web
│   ├── app-field/              # 外勤App
│   ├── app-vip/                # VIP客户App
│   └── app-customer/           # 普通客户App
│
├── packages/                   # 共享包
│   ├── shared-types/           # 共享类型定义
│   ├── shared-utils/           # 共享工具函数
│   ├── shared-constants/       # 共享常量
│   └── shared-validators/      # 共享验证器
│
├── docs/
│   ├── README.md
│   ├── requirements/
│   ├── architecture/
│   ├── api/
│   ├── database/
│   ├── guides/
│   ├── deployments/
│   └── adr/
│
├── infra/
│   └── docker/
│
├── scripts/
│   ├── setup.sh
│   ├── lint.sh
│   └── test.sh
│
└── tools/                      # 内部工具（可选）
    └── codegen/
```

---

## 四、迁移建议（分阶段）

### 阶段 1: 添加必要文件（立即执行）
- [ ] 创建 `README.md`
- [ ] 创建 `.gitignore`
- [ ] 创建 `.editorconfig`

### 阶段 2: 目录结构调整（谨慎执行）
- [ ] 重命名 `frontend-*` → `web-*`
- [ ] 重命名 `mobile-*` → `app-*`
- [ ] 移动到 `apps/` 目录下
- [ ] 调整 `shared/` 结构

### 阶段 3: 完善文档（持续进行）
- [ ] 补充开发指南
- [ ] 补充部署文档

---

## 五、命名规范总结

### 目录命名原则
1. **小写+连字符** (kebab-case)：`web-admin`, `app-field`
2. **前缀明确类型**：`web-*` (Web应用), `app-*` (移动应用), `shared-*` (共享)
3. **语义简洁**：避免过长名称，如 `vip` 优于 `key-customer`
4. **单数/复数统一**：目录名用单数（除了特殊情况）

### 文件命名原则
- 配置文件：`kebab-case` (`.gitignore`, `docker-compose.yml`)
- 代码文件：遵循对应语言规范
- 文档：`kebab-case` (`backend-implementation-plan.md`)

---

## 六、预期改进效果

| 方面 | 当前 | 调整后 | 提升 |
|------|------|--------|------|
| 可导航性 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 目录结构更直观 |
| 一致性 | ⭐⭐ | ⭐⭐⭐⭐⭐ | 命名统一规范 |
| 可维护性 | ⭐⭐⭐ | ⭐⭐⭐⭐ | 职责更清晰 |
| 新人友好度 | ⭐⭐ | ⭐⭐⭐⭐ | 有README和指南 |
| 专业度 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 符合行业最佳实践 |
