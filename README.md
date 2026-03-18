# WitSale 项目规则

## 📖 概述

本项目建立了科学规范、高效严谨的代码开发全流程管理体系，确保项目严格遵循 **需求 → 计划 → 审核 → 编码 → 文档更新** 的完整开发流程。

---

## 🚫 禁止事项

⚠️ **严禁以下行为：**

1. 未完成前置流程就直接生成代码
2. 需求不明就开始开发
3. 计划缺失就盲目编码
4. 未经审核就进入下一阶段
5. 跳过完整开发流程

---

## 📂 文档结构

```
witsale/
├── README.md                      # 本文件
├── checklists/                    # 检查清单
│   └── DEVELOPMENT_FLOW_CHECKLIST.md
├── templates/                     # 模板文件
│   ├── SRS_TEMPLATE.md
│   └── PROJECT_PLAN_TEMPLATE.md
├── guides/                        # 执行指南
│   ├── REQUIREMENTS_PHASE_GUIDE.md
│   ├── PLANNING_PHASE_GUIDE.md
│   ├── REVIEW_PHASE_GUIDE.md
│   ├── CODING_PHASE_GUIDE.md
│   └── DOCUMENTATION_PHASE_GUIDE.md
└── docs/                          # 项目文档（实际项目使用）
    ├── rules/                     # 项目规则
    │   ├── README.md              # 规则目录索引
    │   └── PROJECT_RULES.md       # 项目规则总纲
    ├── requirements/              # 需求文档
    ├── plans/                     # 计划文档
    ├── architecture/              # 架构文档
    ├── api/                       # 接口文档
    ├── database/                  # 数据库文档
    └── deployment/                # 部署文档
```

---

## 📋 快速开始

### 第一步：了解规则
阅读 [PROJECT_RULES.md](./PROJECT_RULES.md) 了解完整的项目规则。

### 第二步：熟悉检查清单
查看 [checklists/DEVELOPMENT_FLOW_CHECKLIST.md](./checklists/DEVELOPMENT_FLOW_CHECKLIST.md) 了解每个阶段的检查项。

### 第三步：项目启动指南

#### 后端启动

1. **进入后端目录**
   ```bash
   cd backend
   ```

2. **激活虚拟环境（如果使用）**
   ```bash
   # Linux/Mac
   source venv/bin/activate
   
   # Windows
   venv\Scripts\activate
   ```

3. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

4. **启动后端服务**
   ```bash
   # 开发模式（带热重载）
   uvicorn app.main:app --reload
   
   # 或者指定主机和端口
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

5. **访问API文档**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

#### 前端启动

1. **进入前端管理端目录**
   ```bash
   cd frontend/apps/web/admin
   ```

2. **安装依赖**
   ```bash
   npm install
   ```

3. **启动前端开发服务器**
   ```bash
   npm run dev
   ```

4. **访问前端页面**
   - 本地访问: http://localhost:5173/（或根据终端显示的其他端口）

#### 开发说明

- 后端默认运行在 8000 端口，前端默认运行在 5173 端口
- 开发模式下，前端和后端都支持热重载功能
- 确保先启动后端服务，再启动前端服务

### 第四步：开始新项目

1. **需求阶段**
   - 使用 [templates/SRS_TEMPLATE.md](./templates/SRS_TEMPLATE.md) 编写需求规格说明书
   - 参考 [guides/REQUIREMENTS_PHASE_GUIDE.md](./guides/REQUIREMENTS_PHASE_GUIDE.md)
   - 将文档放置在 `docs/requirements/` 目录

2. **计划阶段**
   - 使用 [templates/PROJECT_PLAN_TEMPLATE.md](./templates/PROJECT_PLAN_TEMPLATE.md) 编写项目计划
   - 参考 [guides/PLANNING_PHASE_GUIDE.md](./guides/PLANNING_PHASE_GUIDE.md)
   - 将文档放置在 `docs/plans/` 目录

3. **审核阶段**
   - 参考 [guides/REVIEW_PHASE_GUIDE.md](./guides/REVIEW_PHASE_GUIDE.md)
   - 需求和计划审核通过后方可进入编码阶段

4. **编码阶段**
   - 参考 [guides/CODING_PHASE_GUIDE.md](./guides/CODING_PHASE_GUIDE.md)
   - 遵循编码规范，进行代码审查

5. **文档更新阶段**
   - 参考 [guides/DOCUMENTATION_PHASE_GUIDE.md](./guides/DOCUMENTATION_PHASE_GUIDE.md)
   - 更新相关技术文档

---

## 🔄 开发流程图

```
┌─────────────────┐
│   需求编写阶段   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   计划制定阶段   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    审核阶段      │◄─────────┐
└────────┬────────┘          │
         │ 审核通过           │ 审核不通过
         ▼                    │
┌─────────────────┐           │
│   代码编写阶段   │           │
└────────┬────────┘           │
         │                    │
         ▼                    │
┌─────────────────┐           │
│   文档更新阶段   │───────────┘
└─────────────────┘
```

---

## 📞 沟通与汇报

- 保持专业、及时的沟通
- 定期汇报项目进展
- 问题及时上报，不隐瞒
- 里程碑节点必须汇报

---

## 📝 版本历史

| 版本 | 日期 | 说明 |
|------|------|------|
| V1.0 | 2026-03-18 | 初始版本 |

---

## ⚠️ 重要提醒

**在开始任何编码工作前，请务必确认：**

- [ ] 已阅读并理解 PROJECT_RULES.md
- [ ] 需求规格说明书已审核通过
- [ ] 项目计划已审核通过
- [ ] 已查看 DEVELOPMENT_FLOW_CHECKLIST.md

---

**让我们一起科学规范地开发！** 🎯
