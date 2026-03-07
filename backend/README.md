# Backend README

## AI日报 v2.0 后端

### 技术栈
- FastAPI
- SQLAlchemy
- PostgreSQL
- Pydantic

### 本地开发

1. 安装依赖
```bash
cd backend
pip install -r requirements.txt
```

2. 配置环境变量
```bash
export DATABASE_URL="postgresql://user:password@localhost:5432/ai_daily_report"
```

3. 初始化数据库
```bash
python scripts/init_db.py
```

4. 启动服务
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

5. 访问 API 文档
```
http://localhost:8000/docs
```

### 部署

#### 方案A: Fly.io (推荐)
```bash
fly deploy
```

#### 方案B: Cloudflare Workers
```bash
wrangler deploy
```

### API 接口

| 接口 | 说明 |
|------|------|
| GET /api/v2/reports | 报告列表 |
| GET /api/v2/reports/latest | 最新报告 |
| GET /api/v2/reports/{date} | 指定日期报告 |
| GET /api/v2/stocks/{code}/history | 股票历史价格 |
| GET /api/v2/companies | 公司列表 |

### 数据库

- 主数据库: PostgreSQL (Supabase)
- 缓存: Redis (可选)
- 连接池: SQLAlchemy

### 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| DATABASE_URL | PostgreSQL连接URL | localhost |
| REDIS_URL | Redis连接URL | 空 |
| ENV | 环境 | development |
