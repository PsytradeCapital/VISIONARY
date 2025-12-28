"""
Database configuration for PostgreSQL and MongoDB
"""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from motor.motor_asyncio import AsyncIOMotorClient
from typing import AsyncGenerator
import logging

from .config import settings

logger = logging.getLogger(__name__)

# PostgreSQL Configuration
class Base(DeclarativeBase):
    pass

# Create async engine for PostgreSQL
postgres_engine = create_async_engine(
    settings.POSTGRES_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,
    pool_recycle=300,
)

# Create session factory
AsyncSessionLocal = async_sessionmaker(
    postgres_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# MongoDB Configuration
mongodb_client: AsyncIOMotorClient = None
mongodb_database = None

async def init_db():
    """Initialize database connections"""
    global mongodb_client, mongodb_database
    
    try:
        # Initialize MongoDB
        mongodb_client = AsyncIOMotorClient(settings.MONGODB_URL)
        mongodb_database = mongodb_client.get_database("visionary_knowledge")
        
        # Test MongoDB connection
        await mongodb_client.admin.command('ping')
        logger.info("MongoDB connection established")
        
        # Create PostgreSQL tables
        async with postgres_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("PostgreSQL tables created")
        
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise

async def get_postgres_session() -> AsyncGenerator[AsyncSession, None]:
    """Get PostgreSQL session"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

def get_mongodb_database():
    """Get MongoDB database"""
    return mongodb_database

async def close_db_connections():
    """Close database connections"""
    global mongodb_client
    if mongodb_client:
        mongodb_client.close()
    await postgres_engine.dispose()