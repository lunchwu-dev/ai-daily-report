# API路由入口
from fastapi import APIRouter
from app.api import reports, stocks, companies

api_router = APIRouter()

api_router.include_router(reports.router, prefix="/reports", tags=["reports"])
api_router.include_router(stocks.router, prefix="/stocks", tags=["stocks"])
api_router.include_router(companies.router, prefix="/companies", tags=["companies"])
