#!/usr/bin/env python3
"""
Fixed database initialization script for SQLite
This script creates all the required database tables with SQLite-compatible types
"""

import asyncio
import sys
import os

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, String, DateTime, Integer, Text, Boolean, ForeignKey, Float
import uuid
from datetime import datetime
from sqlalchemy import text

# Database configuration
DATABASE_URL = "sqlite+aiosqlite:///./backend/visionary.db"

# Create async engine
engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

# SQLite-compatible models
class User(Base):
    __tablename__ = "users"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

class UserProfile(Base):
    __tablename__ = "user_profiles"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    schedule_format = Column(String(20), default="daily")
    reminder_channels = Column(Text)  # JSON array as text
    theme = Column(String(20), default="light")
    timezone = Column(String(50), default="UTC")
    language = Column(String(10), default="en")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

class Vision(Base):
    __tablename__ = "visions"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    category = Column(String(50), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    target_date = Column(DateTime)
    priority = Column(Integer, default=1)
    status = Column(String(20), default="active")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

class KnowledgeEntry(Base):
    __tablename__ = "knowledge_entries"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    source_type = Column(String(20), nullable=False)
    content = Column(Text, nullable=False)
    extracted_data = Column(Text)  # JSON as text for SQLite
    category = Column(String(50), nullable=False)
    confidence = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_used = Column(DateTime, default=datetime.utcnow)

class VisionMetric(Base):
    __tablename__ = "vision_metrics"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    vision_id = Column(String(36), ForeignKey("visions.id"), nullable=False)
    metric_name = Column(String(100), nullable=False)
    target_value = Column(Float)
    current_value = Column(Float, default=0.0)
    unit = Column(String(20))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

class Schedule(Base):
    __tablename__ = "schedules"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    title = Column(String(255), nullable=False)
    timeframe = Column(String(20), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    status = Column(String(20), default="active")
    flexibility_options = Column(Text)  # JSON as text
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

class ScheduleBlock(Base):
    __tablename__ = "schedule_blocks"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    schedule_id = Column(String(36), ForeignKey("schedules.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    category = Column(String(50), nullable=False)
    priority = Column(Integer, default=1)
    flexibility = Column(Text)  # JSON as text
    related_vision_id = Column(String(36), ForeignKey("visions.id"))
    status = Column(String(20), default="scheduled")
    alternatives = Column(Text)  # JSON as text
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

class Reminder(Base):
    __tablename__ = "reminders"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    schedule_block_id = Column(String(36), ForeignKey("schedule_blocks.id"))
    title = Column(String(255), nullable=False)
    message = Column(Text)
    reminder_time = Column(DateTime, nullable=False)
    channels = Column(Text)  # JSON as text
    status = Column(String(20), default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)

class UserFeedback(Base):
    __tablename__ = "user_feedback"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    feedback_type = Column(String(50), nullable=False)
    context = Column(Text)  # JSON as text
    rating = Column(Integer)
    comments = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

async def init_db():
    """Initialize database tables"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def main():
    """Initialize the database with all required tables"""
    print("🚀 Initializing Visionary AI Database (SQLite)...")
    
    try:
        # Test database connection
        print("📡 Testing database connection...")
        async with engine.begin() as conn:
            result = await conn.execute(text("SELECT 1"))
            print("✅ Database connection successful!")
        
        # Initialize all tables
        print("🏗️  Creating database tables...")
        await init_db()
        print("✅ All database tables created successfully!")
        
        # Verify tables were created
        print("🔍 Verifying tables...")
        async with engine.begin() as conn:
            # List all tables
            result = await conn.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))
            tables = [row[0] for row in result.fetchall()]
            print(f"📋 Created tables: {', '.join(tables)}")
            
            # Check users table specifically
            if 'users' in tables:
                print("✅ Users table created successfully!")
            else:
                print("❌ Users table not found")
        
        print("\n🎉 Database initialization completed successfully!")
        print("🚀 You can now start your backend server and use the app!")
        
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        await engine.dispose()
    
    return True

if __name__ == "__main__":
    success = asyncio.run(main())
    if not success:
        sys.exit(1)