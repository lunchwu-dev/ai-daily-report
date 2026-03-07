# Database configuration with Supabase support
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 数据库URL优先级：环境变量 > 默认本地
# Supabase PostgreSQL URL格式：postgresql://user:password@host:port/database
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://postgres:postgres@localhost:5432/ai_daily_report"
)

# 创建引擎
# pool_pre_ping=True 确保连接有效性
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# 会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 模型基类
Base = declarative_base()

# 依赖注入函数
async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 数据库初始化函数
def init_db():
    """初始化数据库，创建所有表"""
    from app import models
    Base.metadata.create_all(bind=engine)
    print("✅ 数据库表创建完成")

# 测试连接
def test_connection():
    """测试数据库连接"""
    try:
        with engine.connect() as conn:
            result = conn.execute("SELECT 1")
            print("✅ 数据库连接成功")
            return True
    except Exception as e:
        print(f"❌ 数据库连接失败: {e}")
        return False
