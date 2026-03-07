# FastAPI backend main application
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import api_router

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

# 根路由
@app.get("/")
async def root():
    return {
        "message": "AI日报 API v2.0",
        "status": "running",
        "docs": "/docs"
    }

# 健康检查
@app.get("/api/v2/health")
async def health_check():
    return {"status": "healthy", "version": "2.0.0"}

# API路由
app.include_router(api_router, prefix="/api/v2")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
