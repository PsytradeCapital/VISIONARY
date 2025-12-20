from sqlalchemy import Column, String, DateTime, Integer, Text, Boolean, ForeignKey, Float, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from database import Base
import uuid
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

# Extended data models for task 2.1 and 2.3

class KnowledgeEntry(Base):
    __tablename__ = "knowledge_entries"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    source_type = Column(String(20), nullable=False)  # document, voice, text, feedback
    content = Column(Text, nullable=False)
    extracted_data = Column(JSON)  # Store routines, goals, preferences, constraints
    category = Column(String(50), nullable=False)
    confidence = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_used = Column(DateTime, default=datetime.utcnow)

class VisionMetric(Base):
    __tablename__ = "vision_metrics"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    vision_id = Column(UUID(as_uuid=True), ForeignKey("visions.id"), nullable=False)
    metric_name = Column(String(100), nullable=False)
    target_value = Column(Float)
    current_value = Column(Float, default=0.0)
    unit = Column(String(20))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Schedule(Base):
    __tablename__ = "schedules"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    title = Column(String(255), nullable=False)
    timeframe = Column(String(20), nullable=False)  # daily, weekly, monthly
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    status = Column(String(20), default="active")  # active, completed, archived
    flexibility_options = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class ScheduleBlock(Base):
    __tablename__ = "schedule_blocks"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    schedule_id = Column(UUID(as_uuid=True), ForeignKey("schedules.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    category = Column(String(50), nullable=False)
    priority = Column(Integer, default=1)
    flexibility = Column(JSON)  # time_flexible, duration_flexible, location_flexible
    related_vision_id = Column(UUID(as_uuid=True), ForeignKey("visions.id"))
    status = Column(String(20), default="scheduled")  # scheduled, in-progress, completed, skipped
    alternatives = Column(JSON)  # Store alternative options
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Reminder(Base):
    __tablename__ = "reminders"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    schedule_block_id = Column(UUID(as_uuid=True), ForeignKey("schedule_blocks.id"))
    title = Column(String(255), nullable=False)
    message = Column(Text)
    reminder_time = Column(DateTime, nullable=False)
    channels = Column(JSON)  # push, email, sms
    status = Column(String(20), default="pending")  # pending, sent, failed
    created_at = Column(DateTime, default=datetime.utcnow)

class UserFeedback(Base):
    __tablename__ = "user_feedback"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    feedback_type = Column(String(50), nullable=False)  # schedule_rating, suggestion_feedback, etc.
    context = Column(JSON)  # Related schedule, suggestion, etc.
    rating = Column(Integer)  # 1-5 rating
    comments = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

# Pydantic models for API requests/responses

class VisionCreate(BaseModel):
    category: str
    title: str
    description: Optional[str] = None
    target_date: Optional[datetime] = None
    priority: int = 1

class VisionResponse(BaseModel):
    id: str
    category: str
    title: str
    description: Optional[str]
    target_date: Optional[datetime]
    priority: int
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class KnowledgeEntryCreate(BaseModel):
    source_type: str
    content: str
    category: str
    extracted_data: Optional[dict] = None
    confidence: float = 0.0

class KnowledgeEntryResponse(BaseModel):
    id: str
    source_type: str
    content: str
    category: str
    confidence: float
    created_at: datetime
    
    class Config:
        from_attributes = True

class ScheduleBlockCreate(BaseModel):
    title: str
    description: Optional[str] = None
    start_time: datetime
    end_time: datetime
    category: str
    priority: int = 1
    flexibility: Optional[dict] = None
    related_vision_id: Optional[str] = None

class ScheduleBlockResponse(BaseModel):
    id: str
    title: str
    description: Optional[str]
    start_time: datetime
    end_time: datetime
    category: str
    priority: int
    status: str
    
    class Config:
        from_attributes = True