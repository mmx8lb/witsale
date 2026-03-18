# 外勤管理模块规格说明

## 1. 需求背景

外勤管理是企业销售管理系统的重要功能之一。系统需要支持外勤人员的打卡、轨迹跟踪、任务管理等功能，以便企业能够实时了解外勤人员的工作状态和位置信息。

## 2. 技术方案

### 2.1 核心技术
- **打卡功能**：支持外勤人员的上下班打卡、拜访客户打卡等
- **轨迹跟踪**：使用GPS技术实时跟踪外勤人员的位置轨迹
- **任务管理**：分配和管理外勤人员的工作任务
- **拜访管理**：记录和管理外勤人员的客户拜访情况
- **数据同步**：支持离线操作和数据同步

### 2.2 关键特性
- **打卡功能**：支持上下班打卡、拜访客户打卡等多种打卡类型
- **轨迹跟踪**：实时跟踪外勤人员的位置轨迹，支持历史轨迹查询
- **任务管理**：分配、跟踪和管理外勤人员的工作任务
- **拜访管理**：记录客户拜访的详细信息，包括时间、地点、内容等
- **数据同步**：支持离线操作和数据同步，确保数据的完整性
- **报表统计**：生成外勤人员的工作统计报表

## 3. 架构设计

### 3.1 模块结构
```
app/
├── api/
│   └── field.py          # 外勤相关API
├── core/
│   └── field.py          # 外勤核心逻辑
├── models/
│   ├── attendance.py      # 打卡模型
│   ├── track.py           # 轨迹模型
│   ├── task.py            # 任务模型
│   └── visit.py           # 拜访模型
├── schemas/
│   └── field.py          # 外勤相关数据结构
└── services/
    └── field_service.py  # 外勤服务
```

### 3.2 数据流
1. 打卡记录：外勤人员进行打卡操作，系统记录打卡时间和位置
2. 轨迹跟踪：系统实时记录外勤人员的位置轨迹
3. 任务分配：管理员分配任务给外勤人员
4. 任务执行：外勤人员执行任务，记录执行情况
5. 拜访记录：外勤人员记录客户拜访情况
6. 数据同步：外勤人员的操作数据同步到服务器
7. 报表生成：系统生成外勤人员的工作统计报表

## 4. 数据模型

### 4.1 打卡模型 (Attendance)
| 字段名 | 类型 | 描述 |
|-------|------|------|
| id | Integer | 打卡ID |
| user_id | Integer | 用户ID |
| user_name | String | 用户名 |
| type | String | 打卡类型（上班、下班、拜访等） |
| location | String | 打卡位置 |
| latitude | Decimal | 纬度 |
| longitude | Decimal | 经度 |
| status | String | 打卡状态 |
| notes | Text | 打卡备注 |
| created_at | DateTime | 创建时间 |

### 4.2 轨迹模型 (Track)
| 字段名 | 类型 | 描述 |
|-------|------|------|
| id | Integer | 轨迹ID |
| user_id | Integer | 用户ID |
| user_name | String | 用户名 |
| latitude | Decimal | 纬度 |
| longitude | Decimal | 经度 |
| location | String | 位置描述 |
| timestamp | DateTime | 时间戳 |
| created_at | DateTime | 创建时间 |

### 4.3 任务模型 (Task)
| 字段名 | 类型 | 描述 |
|-------|------|------|
| id | Integer | 任务ID |
| title | String | 任务标题 |
| description | Text | 任务描述 |
| assignee_id | Integer | 负责人ID |
| assignee_name | String | 负责人名称 |
| status | String | 任务状态（待分配、待执行、已完成、已取消） |
| priority | String | 任务优先级 |
| start_time | DateTime | 开始时间 |
| end_time | DateTime | 结束时间 |
| created_at | DateTime | 创建时间 |
| updated_at | DateTime | 更新时间 |

### 4.4 拜访模型 (Visit)
| 字段名 | 类型 | 描述 |
|-------|------|------|
| id | Integer | 拜访ID |
| user_id | Integer | 用户ID |
| user_name | String | 用户名 |
| customer_id | Integer | 客户ID |
| customer_name | String | 客户名称 |
| location | String | 拜访位置 |
| latitude | Decimal | 纬度 |
| longitude | Decimal | 经度 |
| purpose | String | 拜访目的 |
| content | Text | 拜访内容 |
| status | String | 拜访状态 |
| start_time | DateTime | 开始时间 |
| end_time | DateTime | 结束时间 |
| created_at | DateTime | 创建时间 |
| updated_at | DateTime | 更新时间 |

## 5. API设计

### 5.1 打卡管理API

#### 5.1.1 打卡
- **路径**：`/api/attendances`
- **方法**：`POST`
- **请求体**：
  ```json
  {
    "type": "work_in",
    "location": "北京市朝阳区",
    "latitude": 39.9042,
    "longitude": 116.4074,
    "notes": "上班打卡"
  }
  ```
- **响应**：
  ```json
  {
    "id": 1,
    "user_id": 1,
    "user_name": "张三",
    "type": "work_in",
    "location": "北京市朝阳区",
    "latitude": 39.9042,
    "longitude": 116.4074,
    "status": "success",
    "notes": "上班打卡",
    "created_at": "2026-03-18T09:00:00"
  }
  ```

#### 5.1.2 获取打卡记录
- **路径**：`/api/attendances`
- **方法**：`GET`
- **查询参数**：
  - `user_id`：用户ID
  - `type`：打卡类型
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
        "user_id": 1,
        "user_name": "张三",
        "type": "work_in",
        "location": "北京市朝阳区",
        "status": "success",
        "created_at": "2026-03-18T09:00:00"
      }
    ]
  }
  ```

### 5.2 轨迹管理API

#### 5.2.1 上传轨迹
- **路径**：`/api/tracks`
- **方法**：`POST`
- **请求体**：
  ```json
  {
    "tracks": [
      {
        "latitude": 39.9042,
        "longitude": 116.4074,
        "location": "北京市朝阳区",
        "timestamp": "2026-03-18T09:00:00"
      },
      {
        "latitude": 39.9052,
        "longitude": 116.4084,
        "location": "北京市朝阳区",
        "timestamp": "2026-03-18T09:01:00"
      }
    ]
  }
  ```
- **响应**：
  ```json
  {
    "message": "轨迹上传成功"
  }
  ```

#### 5.2.2 获取轨迹
- **路径**：`/api/tracks`
- **方法**：`GET`
- **查询参数**：
  - `user_id`：用户ID
  - `start_date`：开始日期
  - `end_date`：结束日期
- **响应**：
  ```json
  {
    "user_id": 1,
    "user_name": "张三",
    "tracks": [
      {
        "latitude": 39.9042,
        "longitude": 116.4074,
        "location": "北京市朝阳区",
        "timestamp": "2026-03-18T09:00:00"
      },
      {
        "latitude": 39.9052,
        "longitude": 116.4084,
        "location": "北京市朝阳区",
        "timestamp": "2026-03-18T09:01:00"
      }
    ]
  }
  ```

### 5.3 任务管理API

#### 5.3.1 创建任务
- **路径**：`/api/tasks`
- **方法**：`POST`
- **请求体**：
  ```json
  {
    "title": "拜访客户",
    "description": "拜访朝阳区的客户",
    "assignee_id": 1,
    "priority": "high",
    "start_time": "2026-03-18T10:00:00",
    "end_time": "2026-03-18T12:00:00"
  }
  ```
- **响应**：
  ```json
  {
    "id": 1,
    "title": "拜访客户",
    "description": "拜访朝阳区的客户",
    "assignee_id": 1,
    "assignee_name": "张三",
    "status": "pending",
    "priority": "high",
    "start_time": "2026-03-18T10:00:00",
    "end_time": "2026-03-18T12:00:00"
  }
  ```

#### 5.3.2 获取任务列表
- **路径**：`/api/tasks`
- **方法**：`GET`
- **查询参数**：
  - `assignee_id`：负责人ID
  - `status`：任务状态
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
        "title": "拜访客户",
        "description": "拜访朝阳区的客户",
        "assignee_id": 1,
        "assignee_name": "张三",
        "status": "pending",
        "priority": "high",
        "start_time": "2026-03-18T10:00:00",
        "end_time": "2026-03-18T12:00:00"
      }
    ]
  }
  ```

#### 5.3.3 更新任务状态
- **路径**：`/api/tasks/{id}/status`
- **方法**：`PUT`
- **请求体**：
  ```json
  {
    "status": "completed",
    "notes": "任务已完成"
  }
  ```
- **响应**：
  ```json
  {
    "message": "任务状态更新成功"
  }
  ```

### 5.4 拜访管理API

#### 5.4.1 创建拜访记录
- **路径**：`/api/visits`
- **方法**：`POST`
- **请求体**：
  ```json
  {
    "customer_id": 1,
    "customer_name": "客户名称",
    "location": "北京市朝阳区",
    "latitude": 39.9042,
    "longitude": 116.4074,
    "purpose": "业务洽谈",
    "content": "讨论合作事宜",
    "start_time": "2026-03-18T10:00:00",
    "end_time": "2026-03-18T11:00:00"
  }
  ```
- **响应**：
  ```json
  {
    "id": 1,
    "user_id": 1,
    "user_name": "张三",
    "customer_id": 1,
    "customer_name": "客户名称",
    "location": "北京市朝阳区",
    "latitude": 39.9042,
    "longitude": 116.4074,
    "purpose": "业务洽谈",
    "content": "讨论合作事宜",
    "status": "completed",
    "start_time": "2026-03-18T10:00:00",
    "end_time": "2026-03-18T11:00:00"
  }
  ```

#### 5.4.2 获取拜访记录
- **路径**：`/api/visits`
- **方法**：`GET`
- **查询参数**：
  - `user_id`：用户ID
  - `customer_id`：客户ID
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
        "user_id": 1,
        "user_name": "张三",
        "customer_id": 1,
        "customer_name": "客户名称",
        "location": "北京市朝阳区",
        "purpose": "业务洽谈",
        "status": "completed",
        "start_time": "2026-03-18T10:00:00",
        "end_time": "2026-03-18T11:00:00"
      }
    ]
  }
  ```

### 5.5 报表API

#### 5.5.1 获取外勤统计报表
- **路径**：`/api/field/reports`
- **方法**：`GET`
- **查询参数**：
  - `user_id`：用户ID
  - `start_date`：开始日期
  - `end_date`：结束日期
- **响应**：
  ```json
  {
    "user_id": 1,
    "user_name": "张三",
    "period": "2026-03-01 to 2026-03-31",
    "attendance_count": 20,
    "visit_count": 15,
    "task_completed_count": 10,
    "total_distance": 100.5
  }
  ```

## 6. 测试计划

### 6.1 单元测试
- **测试打卡功能**：验证打卡记录的创建、查询等功能
- **测试轨迹跟踪**：验证轨迹上传、查询等功能
- **测试任务管理**：验证任务创建、分配、状态更新等功能
- **测试拜访管理**：验证拜访记录的创建、查询等功能

### 6.2 集成测试
- **测试API端点**：验证所有外勤管理相关的API端点
- **测试数据同步**：验证离线操作和数据同步功能
- **测试报表生成**：验证报表生成的准确性

### 6.3 性能测试
- **测试轨迹上传**：验证高并发下的轨迹上传性能
- **测试打卡操作**：验证打卡操作的响应性能
- **测试数据同步**：验证大量数据下的数据同步性能

## 7. 实现注意事项

1. **数据一致性**：确保外勤数据与其他模块的数据一致性
2. **位置精度**：确保GPS定位的准确性和可靠性
3. **数据安全**：保护外勤人员的位置信息安全
4. **错误处理**：统一处理外勤管理相关的错误，返回友好的错误信息
5. **日志记录**：记录外勤相关的操作日志，便于审计和排查问题
6. **可扩展性**：支持未来新增的外勤管理功能
7. **离线支持**：确保外勤人员在无网络环境下也能正常工作

## 8. 依赖项

- **sqlalchemy**：用于数据库操作
- **pydantic**：用于数据验证
- **python-dotenv**：用于环境变量管理
- **python-jose**：用于JWT认证
