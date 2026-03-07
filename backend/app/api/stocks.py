# API路由 - 股票相关接口
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import date

from app.core.database import get_db
from app import models, schemas

router = APIRouter()

@router.get("/{code}/history")
def get_stock_history(code: str, start: date = None, end: date = None, db: Session = Depends(get_db)):
    """获取股票历史价格"""
    # 查找公司
    company = db.query(models.AICompany).filter(models.AICompany.code == code).first()
    if not company:
        raise HTTPException(status_code=404, detail=f"未找到股票代码 {code}")
    
    # 构建查询
    query = db.query(
        models.Report.date,
        models.StockPrice.price,
        models.StockPrice.change,
        models.StockPrice.change_percent
    ).join(models.Report).filter(models.StockPrice.company_id == company.id)
    
    if start:
        query = query.filter(models.Report.date >= start)
    if end:
        query = query.filter(models.Report.date <= end)
    
    results = query.order_by(models.Report.date).all()
    
    return {
        "code": code,
        "name": company.name,
        "data": [
            {
                "date": r.date,
                "price": float(r.price),
                "change": float(r.change) if r.change else None,
                "change_percent": float(r.change_percent) if r.change_percent else None
            }
            for r in results
        ]
    }

@router.get("/today/losers")
def get_today_losers(db: Session = Depends(get_db)):
    """获取今日跌幅最大的股票"""
    latest_report = db.query(models.Report).order_by(models.Report.date.desc()).first()
    if not latest_report:
        raise HTTPException(status_code=404, detail="暂无数据")
    
    stocks = db.query(models.StockPrice).join(models.AICompany).filter(
        models.StockPrice.report_id == latest_report.id
    ).order_by(models.StockPrice.change_percent).limit(5).all()
    
    return [
        {
            "name": s.company.name,
            "code": s.company.code,
            "price": float(s.price),
            "change_percent": float(s.change_percent) if s.change_percent else 0
        }
        for s in stocks
    ]

@router.get("/today/gainers")
def get_today_gainers(db: Session = Depends(get_db)):
    """获取今日涨幅最大的股票"""
    latest_report = db.query(models.Report).order_by(models.Report.date.desc()).first()
    if not latest_report:
        raise HTTPException(status_code=404, detail="暂无数据")
    
    stocks = db.query(models.StockPrice).join(models.AICompany).filter(
        models.StockPrice.report_id == latest_report.id
    ).order_by(models.StockPrice.change_percent.desc()).limit(5).all()
    
    return [
        {
            "name": s.company.name,
            "code": s.company.code,
            "price": float(s.price),
            "change_percent": float(s.change_percent) if s.change_percent else 0
        }
        for s in stocks
    ]
