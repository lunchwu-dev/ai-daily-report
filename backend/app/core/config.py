# Environment configuration
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # 数据库
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/ai_daily_report")
    
    # API配置
    API_V2_PREFIX: str = "/api/v2"
    PROJECT_NAME: str = "AI日报 API"
    VERSION: str = "2.0.0"
    
    # CORS
    CORS_ORIGINS: list = ["*"]  # 生产环境应限制具体域名
    
    # 缓存（可选）
    REDIS_URL: str = os.getenv("REDIS_URL", "")
    
    # 环境
    ENV: str = os.getenv("ENV", "development")
    DEBUG: bool = ENV == "development"

settings = Settings()
