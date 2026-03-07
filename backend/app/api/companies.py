# API路由 - AI产业链公司接口
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app import models, schemas

router = APIRouter()

@router.get("/", response_model=List[schemas.AICompany])
def get_companies(layer: str = None, db: Session = Depends(get_db)):
    """获取AI产业链公司列表"""
    query = db.query(models.AICompany)
    if layer:
        query = query.filter(models.AICompany.layer == layer)
    return query.all()

@router.get("/layers")
def get_layers(db: Session = Depends(get_db)):
    """获取层级分布"""
    companies = db.query(models.AICompany).filter(models.AICompany.is_active == True).all()
    
    result = {
        "infrastructure": [],
        "model": [],
        "application": []
    }
    
    for c in companies:
        result[c.layer].append({
            "name": c.name,
            "code": c.code,
            "position": c.position
        })
    
    return result
