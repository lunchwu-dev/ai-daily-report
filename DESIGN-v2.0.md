# AI日报 v2.0 架构设计方案（完整版）

## 版本信息
- **版本**: v2.0
- **目标**: 前后端分离架构
- **分支**: `v2.0-dev`
- **基线**: v1.6.3
- **更新日期**: 2026-03-07

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

### 2.1 数据库表清单（共7张表）

| 表名 | 用途 | 每日数据量 | 说明 |
|------|------|-----------|------|
| **reports** | 报告主表 | 1条 | 今日头条、报告基础信息 |
| **news** | 新闻表 | 9条 | 国内3+国际3+零售3 |
| **stock_prices** | 股票价格表 | 15条 | 15家AI股票实时价格 |
| **stock_analysis** | 股票分析表 | 15条 | 深度分析（定位/动态/事件/风险/展望） |
| **ai_companies** | AI公司基础表 | 15条（固定） | 公司基础信息 |
| **investment_advice** | 投资建议表 | 1条 | 短/中/长期策略+风险提示 |
| **retail_cases** | 零售AI案例表 | 3条 | 零售AI应用案例 |

**每日总数据量**: 44条新记录

---

### 2.2 表结构详细设计

#### 2.2.1 报告主表 (reports)

```sql
CREATE TABLE reports (
    id SERIAL PRIMARY KEY,
    date DATE UNIQUE NOT NULL,
    version VARCHAR(10) DEFAULT '2.0',
    
    -- 今日头条
    headline_title VARCHAR(500),
    headline_content TEXT,
    headline_sources JSONB,  -- [{"source": "新华社", "viewpoint": "..."}, ...]
    
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- 索引
CREATE INDEX idx_reports_date ON reports(date);
```

---

#### 2.2.2 新闻表 (news)

```sql
CREATE TABLE news (
    id SERIAL PRIMARY KEY,
    report_id INTEGER REFERENCES reports(id) ON DELETE CASCADE,
    category VARCHAR(50) NOT NULL,  -- 'domestic', 'international', 'retail'
    title VARCHAR(500) NOT NULL,
    summary TEXT,
    source VARCHAR(100),
    sort_order INTEGER DEFAULT 0,
    
    created_at TIMESTAMP DEFAULT NOW()
);

-- 索引
CREATE INDEX idx_news_report_id ON news(report_id);
CREATE INDEX idx_news_category ON news(category);
```

---

#### 2.2.3 股票价格表 (stock_prices)

存储每日15家AI股票的实时价格数据

```sql
CREATE TABLE stock_prices (
    id SERIAL PRIMARY KEY,
    report_id INTEGER REFERENCES reports(id) ON DELETE CASCADE,
    company_id INTEGER REFERENCES ai_companies(id),
    
    -- 价格数据
    price DECIMAL(10, 2) NOT NULL,        -- 收盘价，如 177.82
    change DECIMAL(5, 2),                 -- 涨跌额，如 -4.16
    change_percent DECIMAL(5, 2),         -- 涨跌幅%，如 -4.16
    currency VARCHAR(10) NOT NULL,        -- USD / CNY
    
    -- 可选字段（后续扩展）
    volume BIGINT,                        -- 成交量
    market_cap BIGINT,                    -- 市值
    
    recorded_at TIMESTAMP DEFAULT NOW()
);

-- 索引
CREATE INDEX idx_stock_prices_report_id ON stock_prices(report_id);
CREATE INDEX idx_stock_prices_company_id ON stock_prices(company_id);
```

**设计理由**: 价格单独成表，便于历史价格查询、趋势图表生成

---

#### 2.2.4 股票分析表 (stock_analysis)

存储15家AI股票的深度分析

```sql
CREATE TABLE stock_analysis (
    id SERIAL PRIMARY KEY,
    report_id INTEGER REFERENCES reports(id) ON DELETE CASCADE,
    company_id INTEGER REFERENCES ai_companies(id),
    
    -- 分析内容
    position VARCHAR(500),                -- 市场定位
    dynamics JSONB,                       -- 产业动态，["动态1", "动态2", "动态3"]
    event VARCHAR(200),                   -- 最新事件标题
    event_desc TEXT,                      -- 事件详细分析
    risk TEXT,                            -- 风险因素
    outlook TEXT,                         -- 投资展望
    
    -- 版本管理
    analysis_version INTEGER DEFAULT 1,   -- 分析版本，便于追踪变化
    
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- 索引
CREATE INDEX idx_stock_analysis_report_id ON stock_analysis(report_id);
CREATE INDEX idx_stock_analysis_company_id ON stock_analysis(company_id);
```

**设计理由**: 与 prices 分离，分析内容可能多日不变，或微调后版本+1

---

#### 2.2.5 AI产业链公司基础表 (ai_companies)

存储15家核心公司的基础信息（相对稳定，初始化后很少变动）

```sql
CREATE TABLE ai_companies (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,           -- 公司名称，如NVIDIA
    code VARCHAR(20) NOT NULL,            -- 股票代码，如NVDA
    layer VARCHAR(50) NOT NULL,           -- infrastructure / model / application
    
    -- 公司信息
    position VARCHAR(500),                -- 一句话定位
    description TEXT,                     -- 公司简介
    logo_url VARCHAR(500),                -- Logo链接
    website VARCHAR(500),                 -- 官网链接
    
    -- 状态
    is_active BOOLEAN DEFAULT TRUE,       -- 是否活跃
    
    created_at TIMESTAMP DEFAULT NOW()
);

-- 索引
CREATE INDEX idx_ai_companies_layer ON ai_companies(layer);
CREATE INDEX idx_ai_companies_code ON ai_companies(code);
```

**初始化数据（15家）**:

| layer | name | code |
|-------|------|------|
| infrastructure | NVIDIA | NVDA |
| infrastructure | AMD | AMD |
| infrastructure | Intel | INTC |
| infrastructure | 寒武纪 | 688256.SH |
| infrastructure | 海光信息 | 688041.SH |
| model | OpenAI | - |
| model | Alphabet | GOOGL |
| model | Meta | META |
| model | 阿里巴巴 | BABA |
| model | 科大讯飞 | 002230.SZ |
| application | Microsoft | MSFT |
| application | Adobe | ADBE |
| application | Salesforce | CRM |
| application | Palantir | PLTR |
| application | Tesla | TSLA |

---

#### 2.2.6 投资建议表 (investment_advice)

存储每日的投资配置建议

```sql
CREATE TABLE investment_advice (
    id SERIAL PRIMARY KEY,
    report_id INTEGER REFERENCES reports(id) ON DELETE CASCADE,
    
    -- 短期策略
    short_term_title VARCHAR(200) DEFAULT '短期策略（1-3个月）',
    short_term_content TEXT,              -- 超配/关注/谨慎建议
    
    -- 中长期布局
    long_term_title VARCHAR(200) DEFAULT '中长期布局（6-12个月）',
    long_term_content TEXT,               -- 美股/A股/全球配置建议
    
    -- 风险提示
    risk_title VARCHAR(200) DEFAULT '风险提示',
    risk_content TEXT,                    -- 地缘政治/估值/技术迭代风险
    
    created_at TIMESTAMP DEFAULT NOW()
);

-- 索引
CREATE INDEX idx_investment_advice_report_id ON investment_advice(report_id);
```

---

#### 2.2.7 零售AI案例表 (retail_cases)

```sql
CREATE TABLE retail_cases (
    id SERIAL PRIMARY KEY,
    report_id INTEGER REFERENCES reports(id) ON DELETE CASCADE,
    company VARCHAR(100) NOT NULL,        -- 公司名称，如阿里巴巴
    country VARCHAR(50),                  -- 国家，如中国🇨🇳
    title VARCHAR(500) NOT NULL,          -- 案例标题
    summary TEXT,                         -- 案例摘要
    sort_order INTEGER DEFAULT 0,         -- 排序
    
    created_at TIMESTAMP DEFAULT NOW()
);

-- 索引
CREATE INDEX idx_retail_cases_report_id ON retail_cases(report_id);
```

---

### 2.3 表关系图

```
┌─────────────────────────────────────────────────────────────────┐
│                         reports (1)                              │
│                    报告主表 - 每日1条                              │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  headline_title, headline_content, headline_sources     │   │
│  └─────────────────────────────────────────────────────────┘   │
└───────────────────────────┬─────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
┌───────────────┐  ┌────────────────┐  ┌──────────────────┐
│    news (N)    │  │ stock_prices   │  │ stock_analysis   │
│   新闻表        │  │   (N) 价格表    │  │   (N) 分析表      │
│  每日9条       │  │  每日15条       │  │  每日15条         │
└───────────────┘  └───────┬────────┘  └───────┬──────────┘
                           │                   │
                           └─────────┬─────────┘
                                     │
                                     ▼
                          ┌────────────────────┐
                          │  ai_companies (15) │
                          │   AI公司基础表      │
                          │   固定15家公司      │
                          └────────────────────┘

┌───────────────────────┐  ┌───────────────────────┐
│ investment_advice (1) │  │   retail_cases (N)    │
│     投资建议表         │  │     零售AI案例表       │
│     每日1条            │  │     每日3条            │
└───────────────────────┘  └───────────────────────┘
```

---

### 2.4 每日数据量汇总

| 表名 | 每日新增 | 月度新增 | 年度新增 |
|------|---------|---------|---------|
| reports | 1条 | ~30条 | ~365条 |
| news | 9条 | ~270条 | ~3,285条 |
| stock_prices | 15条 | ~450条 | ~5,475条 |
| stock_analysis | 15条 | ~450条 | ~5,475条 |
| investment_advice | 1条 | ~30条 | ~365条 |
| retail_cases | 3条 | ~90条 | ~1,095条 |
| **合计** | **44条** | **~1,320条** | **~16,060条** |

**存储估算**:
- 单条记录平均 2KB
- 年度数据量：~32MB
- **结论**：PostgreSQL免费额度充足

---

### 2.5 核心查询示例

#### 查询某日完整报告
```sql
-- 1. 报告基础信息
SELECT * FROM reports WHERE date = '2026-03-07';

-- 2. 新闻（按分类排序）
SELECT * FROM news 
WHERE report_id = 123 
ORDER BY category, sort_order;

-- 3. 股票（价格+分析 JOIN，按层级排序）
SELECT 
    c.name,
    c.code,
    c.layer,
    sp.price,
    sp.change,
    sp.change_percent,
    sa.position,
    sa.dynamics,
    sa.event,
    sa.risk,
    sa.outlook
FROM stock_prices sp
JOIN ai_companies c ON sp.company_id = c.id
LEFT JOIN stock_analysis sa 
    ON sp.company_id = sa.company_id 
    AND sp.report_id = sa.report_id
WHERE sp.report_id = 123
ORDER BY 
    CASE c.layer 
        WHEN 'infrastructure' THEN 1 
        WHEN 'model' THEN 2 
        WHEN 'application' THEN 3 
    END;

-- 4. 投资建议
SELECT * FROM investment_advice WHERE report_id = 123;

-- 5. 零售AI案例
SELECT * FROM retail_cases 
WHERE report_id = 123 
ORDER BY sort_order;
```

#### 查询某股票历史价格（用于图表）
```sql
SELECT 
    r.date,
    sp.price,
    sp.change_percent
FROM stock_prices sp
JOIN reports r ON sp.report_id = r.id
JOIN ai_companies c ON sp.company_id = c.id
WHERE c.code = 'NVDA'
  AND r.date BETWEEN '2026-01-01' AND '2026-03-07'
ORDER BY r.date;
```

---

## 三、API 接口设计

### 3.1 RESTful API 列表

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/v2/reports/{date}` | 获取指定日期完整报告 |
| GET | `/api/v2/reports/latest` | 获取最新报告 |
| GET | `/api/v2/reports?limit=30&offset=0` | 获取报告列表 |
| GET | `/api/v2/stocks/{code}/history` | 获取股票历史价格 |
| GET | `/api/v2/companies` | 获取AI产业链公司列表 |

### 3.2 响应格式示例

```json
// GET /api/v2/reports/2026-03-07
{
  "date": "2026-03-07",
  "headline": {
    "title": "两会聚焦AI...",
    "content": "...",
    "sources": [{"source": "新华社", "viewpoint": "..."}]
  },
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
  "investment": {
    "short_term": "...",
    "long_term": "...",
    "risk": "..."
  }
}
```

---

## 四、开发计划

### Phase 1: 基础架构 (Week 1-2)
- [ ] 搭建后端 FastAPI 框架
- [ ] 创建数据库表结构
- [ ] 实现基础 API 接口
- [ ] 初始化 ai_companies 数据

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

---

## 五、服务选型

| 服务 | 选型 | 说明 |
|------|------|------|
| 前端托管 | Cloudflare Pages | 免费，全球CDN |
| 后端API | Cloudflare Workers / FastAPI | Serverless |
| 数据库 | Supabase PostgreSQL | 免费500MB |
| 缓存 | Upstash Redis | 免费10MB |
| 定时任务 | GitHub Actions | 免费 |

---

**文档版本**: v2.0-final
**更新日期**: 2026-03-07
