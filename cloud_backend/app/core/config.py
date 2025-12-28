"""
Configuration settings for cloud-native deployment
"""

from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # Database Configuration
    POSTGRES_URL: str = os.getenv("POSTGRES_URL", "postgresql+asyncpg://user:password@localhost/visionary")
    MONGODB_URL: str = os.getenv("MONGODB_URL", "mongodb://localhost:27017/visionary_knowledge")
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    
    # AWS/Cloud Configuration
    AWS_ACCESS_KEY_ID: Optional[str] = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY: Optional[str] = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_REGION: str = os.getenv("AWS_REGION", "us-east-1")
    S3_BUCKET_NAME: str = os.getenv("S3_BUCKET_NAME", "visionary-files")
    
    # Security Configuration
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ENCRYPTION_KEY: str = os.getenv("ENCRYPTION_KEY", "your-encryption-key-32-chars-long")
    
    # External API Configuration
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    GOOGLE_CLOUD_CREDENTIALS: Optional[str] = os.getenv("GOOGLE_CLOUD_CREDENTIALS")
    
    # Application Configuration
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    API_V1_STR: str = "/api/v1"
    
    # Mobile and Web Configuration
    MOBILE_APP_SCHEME: str = "visionary"
    WEB_APP_URL: str = os.getenv("WEB_APP_URL", "https://app.visionary.ai")
    
    class Config:
        case_sensitive = True

settings = Settings()