# API路由 - 报告相关接口
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import date

from app.core.database import get_db
from app import models, schemas

router = APIRouter()

@router.get("/", response_model=List[schemas.Report])
def get_reports(skip: int = 0, limit: int = 30, db: Session = Depends(get_db)):
    """获取报告列表"""
    reports = db.query(models.Report).order_by(models.Report.date.desc()).offset(skip).limit(limit).all()
    return reports

@router.get("/latest", response_model=schemas.Report)
def get_latest_report(db: Session = Depends(get_db)):
    """获取最新报告"""
    report = db.query(models.Report).order_by(models.Report.date.desc()).first()
    if not report:
        raise HTTPException(status_code=404, detail="暂无报告")
    return report

@router.get("/{report_date}", response_model=schemas.Report)
def get_report_by_date(report_date: date, db: Session = Depends(get_db)):
    """获取指定日期报告"""
    report = db.query(models.Report).filter(models.Report.date == report_date).first()
    if not report:
        raise HTTPException(status_code=404, detail=f"未找到 {report_date} 的报告")
    return report

@router.post("/", response_model=schemas.Report)
def create_report(report: schemas.ReportCreate, db: Session = Depends(get_db)):
    """创建新报告（管理接口）"""
    db_report = models.Report(**report.dict())
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    return db_report
