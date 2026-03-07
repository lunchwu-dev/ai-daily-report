# AI日报 v2.0 架构设计方案

## 版本信息
- **版本**: v2.0
- **目标**: 前后端分离架构
- **分支**: `v2.0-dev`
- **基线**: v1.6.3

---

## 一、架构概述

### 1.1 当前架构（v1.6.3）问题
```
数据获取 → Python生成HTML → 静态部署
                    ↑
            数据+模板耦合在一起
                    ↓
        每日更新需重新生成整个HTML
```

**痛点**:
- 数据更新需重新生成整个HTML文件
- 前端样式/结构调整影响历史报告
- 无法灵活查询历史数据
- 数据复用困难

### 1.2 目标架构（v2.0）
```
┌─────────────────────────────────────────────────────────────┐
│                        前端层 (Frontend)                     │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │  报告展示页  │  │  首页/索引   │  │  管理后台（可选）    │  │
│  │  React/Vue  │  │   React     │  │      React          │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
│                      ↑ 调用API获取数据                        │
└──────────────────────┼──────────────────────────────────────┘
                       │
┌──────────────────────┼──────────────────────────────────────┐
│                      │         后端层 (Backend)              │
│                      │                                       │
│  ┌───────────────────┴───────────────────────────────────┐   │
│  │                  API Gateway                           │   │
│  │              (FastAPI / Flask)                         │   │
│  └────────────────────────────────────────────────────────┘   │
│                      ↑ 读取数据                               │
│  ┌───────────────────┴───────────────────────────────────┐   │
│  │                  数据服务层                            │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────────────┐    │   │
│  │  │ 新闻数据  │  │ 股票数据  │  │   报告元数据      │    │   │
│  │  │  Service │  │  Service │  │    Service       │    │   │
│  │  └──────────┘  └──────────┘  └──────────────────┘    │   │
│  └────────────────────────────────────────────────────────┘   │
│                      ↑ 写入/读取                              │
│  ┌───────────────────┴───────────────────────────────────┐   │
│  │                  数据存储层 (Database)                 │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────────────┐    │   │
│  │  │ PostgreSQL│  │  Redis   │  │   对象存储        │    │   │
│  │  │ (主数据库)│  │  (缓存)  │  │  (Cloudflare R2) │    │   │
│  │  └──────────┘  └──────────┘  └──────────────────┘    │   │
│  └────────────────────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────────────┘
                       ↑ 定时任务写入
┌──────────────────────┴──────────────────────────────────────┐
│                    数据采集层 (Data Collector)               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐   │
│  │  AI新闻采集   │  │  股票数据采集 │  │   数据清洗/处理   │   │
│  │  Kimi Search │  │  Yahoo/Alpha │  │   Python脚本     │   │
│  └──────────────┘  └──────────────┘  └──────────────────┘   │
│                         每日 6:30 执行                        │
└───────────────────────────────────────────────────────────────┘
```

---

## 二、数据模型设计

### 2.1 数据库 Schema (PostgreSQL)

```sql
-- 报告表
CREATE TABLE reports (
    id SERIAL PRIMARY KEY,
    date DATE UNIQUE NOT NULL,
    version VARCHAR(10) DEFAULT '2.0',
    headline_title VARCHAR(500),
    headline_content TEXT,
    headline_sources JSONB,
    investment_short TEXT,
    investment_long TEXT,
    investment_risk TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- 新闻表
CREATE TABLE news (
    id SERIAL PRIMARY KEY,
    report_id INTEGER REFERENCES reports(id),
    category VARCHAR(50), -- 'domestic', 'international', 'retail'
    title VARCHAR(500),
    summary TEXT,
    source VARCHAR(100),
    sort_order INTEGER DEFAULT 0
);

-- 股票表
CREATE TABLE stocks (
    id SERIAL PRIMARY KEY,
    report_id INTEGER REFERENCES reports(id),
    layer VARCHAR(50), -- 'infrastructure', 'model', 'application'
    name VARCHAR(100),
    code VARCHAR(20),
    price DECIMAL(10, 2),
    change DECIMAL(5, 2),
    currency VARCHAR(10),
    position VARCHAR(500),
    dynamics JSONB,
    event VARCHAR(200),
    event_desc TEXT,
    risk TEXT,
    outlook TEXT,
    sort_order INTEGER DEFAULT 0
);

-- AI产业链公司表（基础数据）
CREATE TABLE ai_companies (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    code VARCHAR(20),
    layer VARCHAR(50),
    position VARCHAR(500),
    description TEXT,
    logo_url VARCHAR(500),
    website VARCHAR(500)
);

-- 零售AI案例表
CREATE TABLE retail_cases (
    id SERIAL PRIMARY KEY,
    report_id INTEGER REFERENCES reports(id),
    company VARCHAR(100),
    country VARCHAR(50),
    title VARCHAR(500),
    summary TEXT,
    sort_order INTEGER DEFAULT 0
);
```

### 2.2 API 接口设计

```yaml
# RESTful API

# 获取指定日期报告
GET /api/v2/reports/{date}
Response:
  {
    "date": "2026-03-07",
    "headline": { ... },
    "news": {
      "domestic": [...],
      "international": [...],
      "retail": [...]
    },
    "stocks": {
      "infrastructure": [...],
      "model": [...],
      "application": [...]
    },
    "investment": { ... }
  }

# 获取报告列表
GET /api/v2/reports?limit=30&offset=0

# 获取最新报告
GET /api/v2/reports/latest

# 获取股票历史数据
GET /api/v2/stocks/{code}/history?start=2026-01-01&end=2026-03-07

# 获取AI产业链公司列表
GET /api/v2/companies

# 管理接口（可选）
POST /api/v2/admin/reports  # 创建报告
PUT /api/v2/admin/reports/{date}  # 更新报告
DELETE /api/v2/admin/reports/{date}  # 删除报告
```

---

## 三、前端架构

### 3.1 技术栈
- **框架**: React 18 + TypeScript
- **构建**: Vite
- **样式**: Tailwind CSS
- **状态管理**: Zustand / React Query
- **图表**: ECharts / Recharts
- **部署**: Cloudflare Pages

### 3.2 页面结构
```
src/
├── components/           # 公共组件
│   ├── Layout.tsx       # 布局框架
│   ├── Header.tsx       # 头部
│   ├── Footer.tsx       # 底部
│   ├── StockCard.tsx    # 股票卡片
│   ├── NewsCard.tsx     # 新闻卡片
│   └── Chart/           # 图表组件
│
├── pages/               # 页面
│   ├── Report/          # 报告展示页
│   │   ├── index.tsx
│   │   ├── Headline.tsx
│   │   ├── NewsSection.tsx
│   │   ├── StockSection.tsx
│   │   └── InvestmentSection.tsx
│   │
│   ├── Index/           # 首页/历史索引
│   │   └── index.tsx
│   │
│   └── Admin/           # 管理后台（可选）
│       └── index.tsx
│
├── hooks/               # 自定义Hooks
│   ├── useReport.ts     # 获取报告数据
│   ├── useReports.ts    # 获取报告列表
│   └── useStocks.ts     # 获取股票数据
│
├── services/            # API服务
│   └── api.ts
│
├── types/               # TypeScript类型
│   └── index.ts
│
└── utils/               # 工具函数
    └── format.ts
```

### 3.3 前端部署
- **托管**: Cloudflare Pages
- **域名**: `ai-daily-report-32b.pages.dev`
- **构建命令**: `npm run build`
- **输出目录**: `dist/`

---

## 四、后端架构

### 4.1 技术栈
- **框架**: FastAPI (Python)
- **数据库**: PostgreSQL + SQLAlchemy
- **缓存**: Redis
- **部署**: Cloudflare Workers / Docker
- **API文档**: 自动生成 Swagger UI

### 4.2 项目结构
```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI入口
│   ├── config.py            # 配置
│   │
│   ├── api/                 # API路由
│   │   ├── __init__.py
│   │   ├── reports.py       # 报告接口
│   │   ├── stocks.py        # 股票接口
│   │   └── admin.py         # 管理接口
│   │
│   ├── models/              # 数据模型
│   │   ├── __init__.py
│   │   ├── report.py
│   │   ├── news.py
│   │   ├── stock.py
│   │   └── company.py
│   │
│   ├── schemas/             # Pydantic模型
│   │   ├── __init__.py
│   │   ├── report.py
│   │   └── stock.py
│   │
│   ├── services/            # 业务逻辑
│   │   ├── __init__.py
│   │   ├── report_service.py
│   │   └── stock_service.py
│   │
│   └── core/                # 核心功能
│       ├── database.py      # 数据库连接
│       └── cache.py         # 缓存配置
│
├── migrations/              # 数据库迁移
│   └── versions/
│
├── tests/                   # 测试
│
├── Dockerfile
├── requirements.txt
└── alembic.ini
```

### 4.3 后端部署
- **方案A**: Cloudflare Workers (Serverless)
- **方案B**: Docker + Fly.io / Railway
- **数据库**: Supabase PostgreSQL / Neon

---

## 五、数据采集层

### 5.1 数据获取脚本
```
collectors/
├── __init__.py
├── config.py
├── main.py                  # 每日执行入口
│
├── news/                    # 新闻采集
│   ├── kimi_search.py       # Kimi Search API
│   └── processor.py         # 数据清洗
│
├── stocks/                  # 股票采集
│   ├── yahoo_finance.py     # Yahoo Finance API
│   └── alpha_vantage.py     # Alpha Vantage API
│
└── database/                # 数据写入
    └── writer.py            # 写入PostgreSQL
```

### 5.2 执行流程
```python
# 每日 6:30 执行
async def daily_update():
    # 1. 获取AI新闻
    news_data = await collect_news()
    
    # 2. 获取股票数据
    stock_data = await collect_stocks()
    
    # 3. 数据清洗处理
    processed = process_data(news_data, stock_data)
    
    # 4. 写入数据库
    await write_to_database(processed)
    
    # 5. 清除缓存
    await clear_cache()
    
    # 6. 触发前端重新部署（可选）
    # 或前端自动获取最新数据
```

---

## 六、部署架构

### 6.1 完整部署图
```
┌─────────────────────────────────────────────────────────────┐
│                         用户访问                             │
└──────────────────────────┬──────────────────────────────────┘
                           │
           ┌───────────────┼───────────────┐
           │               │               │
           ▼               ▼               ▼
┌─────────────────┐ ┌──────────────┐ ┌──────────────┐
│  Cloudflare     │ │  Cloudflare  │ │  Cloudflare  │
│  Pages          │ │  Workers     │ │  R2 Storage  │
│  (前端)          │ │  (后端API)   │ │  (静态资源)  │
└─────────────────┘ └──────┬───────┘ └──────────────┘
                           │
           ┌───────────────┼───────────────┐
           │               │               │
           ▼               ▼               ▼
┌─────────────────┐ ┌──────────────┐ ┌──────────────┐
│  Supabase       │ │  Upstash     │ │  GitHub      │
│  PostgreSQL     │ │  Redis       │ │  Actions     │
│  (主数据库)      │ │  (缓存)      │ │  (定时任务)  │
└─────────────────┘ └──────────────┘ └──────────────┘
```

### 6.2 服务选型
| 服务 | 选型 | 说明 |
|------|------|------|
| 前端托管 | Cloudflare Pages | 免费，全球CDN |
| 后端API | Cloudflare Workers | Serverless，免费额度充足 |
| 数据库 | Supabase PostgreSQL | 免费500MB，足够初期使用 |
| 缓存 | Upstash Redis | 免费10MB，API响应缓存 |
| 定时任务 | GitHub Actions | 免费，每日触发 |
| 对象存储 | Cloudflare R2 | 免费10GB，存储静态资源 |

---

## 七、开发计划

### Phase 1: 基础架构 (Week 1-2)
- [ ] 创建 v2.0-dev 分支
- [ ] 搭建后端 FastAPI 框架
- [ ] 设计数据库 Schema
- [ ] 实现基础 API 接口

### Phase 2: 前端开发 (Week 2-3)
- [ ] 搭建 React + Vite 项目
- [ ] 实现报告展示页面
- [ ] 实现首页/历史索引
- [ ] 对接后端 API

### Phase 3: 数据采集 (Week 3-4)
- [ ] 重构新闻采集脚本
- [ ] 重构股票采集脚本
- [ ] 实现数据写入数据库
- [ ] 配置定时任务

### Phase 4: 部署测试 (Week 4)
- [ ] 部署后端 API
- [ ] 部署前端页面
- [ ] 配置数据库
- [ ] 端到端测试

### Phase 5: 优化迭代 (Week 5+)
- [ ] 性能优化
- [ ] 缓存策略
- [ ] 错误处理
- [ ] 监控告警

---

## 八、优势对比

| 特性 | v1.6.3 (静态) | v2.0 (前后端分离) |
|------|---------------|-------------------|
| 数据更新 | 重新生成HTML | 仅更新数据库 |
| 前端迭代 | 影响历史报告 | 不影响历史数据 |
| 历史查询 | 需解析HTML | 直接SQL查询 |
| 数据复用 | 困难 | 容易 |
| 扩展性 | 有限 | 强 |
| 开发效率 | 低 | 高 |
| 部署复杂度 | 简单 | 中等 |

---

**文档版本**: v2.0-design
**设计日期**: 2026-03-07
**作者**: AI Assistant
