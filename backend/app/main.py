# FastAPI backend main application
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="AI日报 API",
    description="AI日报 v2.0 前后端分离架构 API",
    version="2.0.0"
)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应限制域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "AI日报 API v2.0", "status": "running"}

@app.get("/api/v2/health")
async def health_check():
    return {"status": "healthy", "version": "2.0.0"}

# 后续将导入路由
# from app.api import reports, stocks, companies
# app.include_router(reports.router, prefix="/api/v2/reports", tags=["reports"])
# app.include_router(stocks.router, prefix="/api/v2/stocks", tags=["stocks"])
# app.include_router(companies.router, prefix="/api/v2/companies", tags=["companies"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
