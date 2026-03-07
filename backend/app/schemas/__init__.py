# Pydantic schemas for API
from pydantic import BaseModel
from typing import List, Optional
from datetime import date, datetime

# News schemas
class NewsBase(BaseModel):
    category: str
    title: str
    summary: Optional[str] = None
    source: Optional[str] = None

class News(NewsBase):
    id: int
    sort_order: int
    
    class Config:
        from_attributes = True

# Stock schemas
class StockPriceBase(BaseModel):
    price: float
    change: Optional[float] = None
    change_percent: Optional[float] = None
    currency: str

class StockPrice(StockPriceBase):
    id: int
    company_name: str
    company_code: str
    company_layer: str
    
    class Config:
        from_attributes = True

class StockAnalysisBase(BaseModel):
    position: Optional[str] = None
    dynamics: List[str] = []
    event: Optional[str] = None
    event_desc: Optional[str] = None
    risk: Optional[str] = None
    outlook: Optional[str] = None

class StockAnalysis(StockAnalysisBase):
    id: int
    analysis_version: int
    
    class Config:
        from_attributes = True

# Investment advice schema
class InvestmentAdvice(BaseModel):
    short_term_title: str
    short_term_content: Optional[str] = None
    long_term_title: str
    long_term_content: Optional[str] = None
    risk_title: str
    risk_content: Optional[str] = None
    
    class Config:
        from_attributes = True

# Retail case schema
class RetailCase(BaseModel):
    company: str
    country: Optional[str] = None
    title: str
    summary: Optional[str] = None
    
    class Config:
        from_attributes = True

# Report schemas
class ReportBase(BaseModel):
    date: date
    version: str = "2.0"
    headline_title: Optional[str] = None
    headline_content: Optional[str] = None

class ReportCreate(ReportBase):
    pass

class Report(ReportBase):
    id: int
    headline_sources: List[dict] = []
    news: List[News] = []
    stock_prices: List[StockPrice] = []
    investment_advice: Optional[InvestmentAdvice] = None
    retail_cases: List[RetailCase] = []
    created_at: datetime
    
    class Config:
        from_attributes = True

# Company schema
class AICompany(BaseModel):
    id: int
    name: str
    code: str
    layer: str
    position: Optional[str] = None
    
    class Config:
        from_attributes = True
