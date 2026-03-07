# SQLAlchemy models
from sqlalchemy import Column, Integer, String, Text, Date, DateTime, Numeric, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base

class Report(Base):
    __tablename__ = "reports"
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, unique=True, index=True, nullable=False)
    version = Column(String(10), default="2.0")
    headline_title = Column(String(500))
    headline_content = Column(Text)
    headline_sources = Column(JSON, default=[])
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    
    # 关系
    news = relationship("News", back_populates="report", cascade="all, delete-orphan")
    stock_prices = relationship("StockPrice", back_populates="report", cascade="all, delete-orphan")
    stock_analysis = relationship("StockAnalysis", back_populates="report", cascade="all, delete-orphan")
    investment_advice = relationship("InvestmentAdvice", back_populates="report", cascade="all, delete-orphan")
    retail_cases = relationship("RetailCase", back_populates="report", cascade="all, delete-orphan")

class News(Base):
    __tablename__ = "news"
    
    id = Column(Integer, primary_key=True, index=True)
    report_id = Column(Integer, ForeignKey("reports.id"), nullable=False)
    category = Column(String(50), nullable=False)  # domestic, international, retail
    title = Column(String(500), nullable=False)
    summary = Column(Text)
    source = Column(String(100))
    sort_order = Column(Integer, default=0)
    created_at = Column(DateTime)
    
    report = relationship("Report", back_populates="news")

class AICompany(Base):
    __tablename__ = "ai_companies"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    layer = Column(String(50), nullable=False)  # infrastructure, model, application
    position = Column(String(500))
    description = Column(Text)
    logo_url = Column(String(500))
    website = Column(String(500))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime)
    
    # 关系
    stock_prices = relationship("StockPrice", back_populates="company")
    stock_analysis = relationship("StockAnalysis", back_populates="company")

class StockPrice(Base):
    __tablename__ = "stock_prices"
    
    id = Column(Integer, primary_key=True, index=True)
    report_id = Column(Integer, ForeignKey("reports.id"), nullable=False)
    company_id = Column(Integer, ForeignKey("ai_companies.id"))
    price = Column(Numeric(10, 2), nullable=False)
    change = Column(Numeric(5, 2))
    change_percent = Column(Numeric(5, 2))
    currency = Column(String(10), nullable=False)
    volume = Column(Integer)
    market_cap = Column(Integer)
    recorded_at = Column(DateTime)
    
    report = relationship("Report", back_populates="stock_prices")
    company = relationship("AICompany", back_populates="stock_prices")

class StockAnalysis(Base):
    __tablename__ = "stock_analysis"
    
    id = Column(Integer, primary_key=True, index=True)
    report_id = Column(Integer, ForeignKey("reports.id"), nullable=False)
    company_id = Column(Integer, ForeignKey("ai_companies.id"))
    position = Column(String(500))
    dynamics = Column(JSON, default=[])
    event = Column(String(200))
    event_desc = Column(Text)
    risk = Column(Text)
    outlook = Column(Text)
    analysis_version = Column(Integer, default=1)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    
    report = relationship("Report", back_populates="stock_analysis")
    company = relationship("AICompany", back_populates="stock_analysis")

class InvestmentAdvice(Base):
    __tablename__ = "investment_advice"
    
    id = Column(Integer, primary_key=True, index=True)
    report_id = Column(Integer, ForeignKey("reports.id"), nullable=False, unique=True)
    short_term_title = Column(String(200), default="短期策略（1-3个月）")
    short_term_content = Column(Text)
    long_term_title = Column(String(200), default="中长期布局（6-12个月）")
    long_term_content = Column(Text)
    risk_title = Column(String(200), default="风险提示")
    risk_content = Column(Text)
    created_at = Column(DateTime)
    
    report = relationship("Report", back_populates="investment_advice")

class RetailCase(Base):
    __tablename__ = "retail_cases"
    
    id = Column(Integer, primary_key=True, index=True)
    report_id = Column(Integer, ForeignKey("reports.id"), nullable=False)
    company = Column(String(100), nullable=False)
    country = Column(String(50))
    title = Column(String(500), nullable=False)
    summary = Column(Text)
    sort_order = Column(Integer, default=0)
    created_at = Column(DateTime)
    
    report = relationship("Report", back_populates="retail_cases")
