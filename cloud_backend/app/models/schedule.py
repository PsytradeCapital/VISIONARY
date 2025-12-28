"""
Schedule models with autonomous adjustment tracking and focus time protection
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, JSON, Float
from sqlalchemy.sql import func
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field
from datetime import datetime, time
import uuid

from ..core.database import Base

class Schedule(Base):
    """Enhanced schedule model with autonomous adjustments and focus time protection"""
    __tablename__ = "schedules"
    
    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String, unique=True, index=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(Integer, nullable=False, index=True)
    
    # Schedule information
    title = Column(String, nullable=False)
    description = Column(Text)
    schedule_date = Column(DateTime(timezone=True), nullable=False)
    schedule_type = Column(String, default="daily")  # daily, weekly, monthly, custom
    
    # Autonomous adjustment tracking
    autonomous_adjustments_enabled = Column(Boolean, default=False)
    auto_adjustments_count = Column(Integer, default=0)
    last_auto_adjustment = Column(DateTime(timezone=True))
    adjustment_success_rate = Column(Float, default=0.0)
    user_approval_required = Column(Boolean, default=True)
    
    # Focus time protection (Motion/Reclaim AI inspired)
    focus_time_protected = Column(Boolean, default=False)
    focus_blocks = Column(JSON)  # List of protected focus time blocks
    habit_defense_active = Column(Boolean, default=False)
    interruption_buffer_minutes = Column(Integer, default=15)
    
    # AI-generated schedule metadata
    ai_generated = Column(Boolean, default=False)
    ai_confidence_score = Column(Float)
    ai_model_version = Column(String)
    generation_parameters = Column(JSON)  # Parameters used for AI generation
    
    # Mobile optimization flags
    mobile_optimized = Column(Boolean, default=True)
    offline_sync_enabled = Column(Boolean, default=True)
    push_notifications_enabled = Column(Boolean, default=True)
    
    # Visual elements and AI-generated content
    visual_timeline_available = Column(Boolean, default=False)
    ai_generated_visuals = Column(JSON)  # Metadata for associated visuals
    progress_visualization_type = Column(String, default="photorealistic")
    
    # Status and completion tracking
    status = Column(String, default="active")  # active, completed, cancelled, archived
    completion_percentage = Column(Float, default=0.0)
    actual_vs_planned_variance = Column(Float, default=0.0)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_accessed = Column(DateTime(timezone=True))

class Task(Base):
    """Enhanced task model with AI processing and mobile optimization"""
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String, unique=True, index=True, default=lambda: str(uuid.uuid4()))
    schedule_id = Column(Integer, nullable=False, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    
    # Task information
    title = Column(String, nullable=False)
    description = Column(Text)
    priority = Column(String, default="medium")  # low, medium, high, urgent
    category = Column(String)  # work, personal, health, finance, etc.
    
    # Time management
    estimated_duration = Column(Integer)  # minutes
    actual_duration = Column(Integer)  # minutes
    start_time = Column(DateTime(timezone=True))
    end_time = Column(DateTime(timezone=True))
    deadline = Column(DateTime(timezone=True))
    
    # AI processing and categorization
    ai_categorized = Column(Boolean, default=False)
    ai_category_confidence = Column(Float)
    ai_priority_suggestion = Column(String)
    ai_duration_estimate = Column(Integer)  # AI-estimated duration in minutes
    
    # Focus time integration
    requires_focus_time = Column(Boolean, default=False)
    focus_time_type = Column(String)  # deep_work, creative, analytical, administrative
    interruption_sensitivity = Column(String, default="medium")  # low, medium, high
    
    # Mobile and cloud features
    mobile_reminder_enabled = Column(Boolean, default=True)
    cloud_sync_priority = Column(String, default="normal")  # low, normal, high
    offline_completion_allowed = Column(Boolean, default=True)
    
    # Progress and completion
    status = Column(String, default="pending")  # pending, in_progress, completed, cancelled
    completion_percentage = Column(Float, default=0.0)
    completion_notes = Column(Text)
    
    # Visual and motivational elements
    progress_visual_type = Column(String, default="photorealistic")
    celebration_visual_enabled = Column(Boolean, default=True)
    motivational_image_url = Column(String)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    completed_at = Column(DateTime(timezone=True))

class TimeBlock(Base):
    """Time block model for autonomous time blocking and conflict resolution"""
    __tablename__ = "time_blocks"
    
    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String, unique=True, index=True, default=lambda: str(uuid.uuid4()))
    schedule_id = Column(Integer, nullable=False, index=True)
    task_id = Column(Integer, index=True)  # Optional - can be unassigned time block
    user_id = Column(Integer, nullable=False, index=True)
    
    # Time block details
    title = Column(String, nullable=False)
    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=False)
    duration_minutes = Column(Integer, nullable=False)
    
    # Autonomous time blocking (SkedPal inspired)
    auto_scheduled = Column(Boolean, default=False)
    scheduling_algorithm = Column(String)  # constraint_satisfaction, ml_optimization, etc.
    scheduling_confidence = Column(Float)
    alternative_slots = Column(JSON)  # Alternative time slots if conflicts arise
    
    # Conflict resolution (Akiflow style)
    conflict_detected = Column(Boolean, default=False)
    conflicting_blocks = Column(JSON)  # IDs of conflicting time blocks
    conflict_resolution_strategy = Column(String)  # reschedule, split, prioritize, etc.
    conflict_resolved = Column(Boolean, default=True)
    
    # Focus time and habit defense (Motion inspired)
    is_focus_block = Column(Boolean, default=False)
    focus_type = Column(String)  # deep_work, creative, meetings, admin
    habit_defense_enabled = Column(Boolean, default=False)
    buffer_before_minutes = Column(Integer, default=0)
    buffer_after_minutes = Column(Integer, default=0)
    
    # Dynamic adjustments and flexibility
    flexible_timing = Column(Boolean, default=False)
    min_duration = Column(Integer)  # Minimum duration if flexible
    max_duration = Column(Integer)  # Maximum duration if flexible
    can_be_split = Column(Boolean, default=False)
    can_be_moved = Column(Boolean, default=True)
    
    # Mobile and real-time features
    mobile_notification_enabled = Column(Boolean, default=True)
    real_time_updates_enabled = Column(Boolean, default=True)
    location_based_reminder = Column(JSON)  # Location-based reminder settings
    
    # Status and tracking
    status = Column(String, default="scheduled")  # scheduled, in_progress, completed, cancelled
    actual_start_time = Column(DateTime(timezone=True))
    actual_end_time = Column(DateTime(timezone=True))
    effectiveness_rating = Column(Float)  # User-provided rating
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Reminder(Base):
    """Enhanced reminder model with conversational tones and photorealistic content"""
    __tablename__ = "reminders"
    
    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String, unique=True, index=True, default=lambda: str(uuid.uuid4()))
    task_id = Column(Integer, index=True)
    time_block_id = Column(Integer, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    
    # Reminder content
    title = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    reminder_type = Column(String, nullable=False)  # task, break, focus, celebration, recovery
    
    # Conversational tones (Toki inspired)
    conversational_tone = Column(String, default="supportive")  # supportive, professional, casual, motivational
    personality_style = Column(String, default="encouraging")
    message_template = Column(String)
    personalized_message = Column(Text)
    
    # Photorealistic motivational content
    motivational_image_enabled = Column(Boolean, default=True)
    image_generation_prompt = Column(Text)
    generated_image_url = Column(String)
    image_style = Column(String, default="photorealistic")  # photorealistic, artistic, minimal
    
    # Context-aware messaging
    context_aware = Column(Boolean, default=True)
    user_current_state = Column(String)  # focused, distracted, productive, struggling
    adaptive_messaging = Column(Boolean, default=True)
    success_context = Column(JSON)  # Recent achievements, progress made
    
    # Scheduling and delivery
    scheduled_time = Column(DateTime(timezone=True), nullable=False)
    delivery_method = Column(JSON)  # push, email, sms, in_app
    delivered = Column(Boolean, default=False)
    delivered_at = Column(DateTime(timezone=True))
    
    # User interaction and feedback
    acknowledged = Column(Boolean, default=False)
    acknowledged_at = Column(DateTime(timezone=True))
    user_response = Column(String)  # positive, negative, neutral, no_response
    effectiveness_score = Column(Float)
    
    # Mobile and cloud features
    mobile_push_enabled = Column(Boolean, default=True)
    rich_notification_content = Column(JSON)  # Images, actions, etc.
    offline_delivery_fallback = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

# Pydantic models for API requests/responses
class ScheduleCreate(BaseModel):
    title: str = Field(..., description="Schedule title")
    description: Optional[str] = None
    schedule_date: datetime = Field(..., description="Schedule date")
    schedule_type: str = Field("daily", description="Schedule type")
    autonomous_adjustments_enabled: bool = Field(False, description="Enable autonomous adjustments")
    focus_time_protected: bool = Field(False, description="Enable focus time protection")

class ScheduleResponse(BaseModel):
    id: int
    uuid: str
    user_id: int
    title: str
    description: Optional[str]
    schedule_date: datetime
    schedule_type: str
    autonomous_adjustments_enabled: bool
    auto_adjustments_count: int
    focus_time_protected: bool
    ai_generated: bool
    status: str
    completion_percentage: float
    created_at: datetime
    
    class Config:
        from_attributes = True

class TaskCreate(BaseModel):
    title: str = Field(..., description="Task title")
    description: Optional[str] = None
    priority: str = Field("medium", description="Task priority")
    category: Optional[str] = None
    estimated_duration: Optional[int] = None
    deadline: Optional[datetime] = None
    requires_focus_time: bool = Field(False, description="Requires focus time")

class TaskResponse(BaseModel):
    id: int
    uuid: str
    schedule_id: int
    title: str
    priority: str
    category: Optional[str]
    estimated_duration: Optional[int]
    actual_duration: Optional[int]
    status: str
    completion_percentage: float
    requires_focus_time: bool
    ai_categorized: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class TimeBlockCreate(BaseModel):
    title: str = Field(..., description="Time block title")
    start_time: datetime = Field(..., description="Start time")
    end_time: datetime = Field(..., description="End time")
    task_id: Optional[int] = None
    is_focus_block: bool = Field(False, description="Is this a focus block")
    flexible_timing: bool = Field(False, description="Allow flexible timing")

class TimeBlockResponse(BaseModel):
    id: int
    uuid: str
    title: str
    start_time: datetime
    end_time: datetime
    duration_minutes: int
    auto_scheduled: bool
    conflict_detected: bool
    is_focus_block: bool
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class ReminderCreate(BaseModel):
    title: str = Field(..., description="Reminder title")
    message: str = Field(..., description="Reminder message")
    reminder_type: str = Field(..., description="Type of reminder")
    scheduled_time: datetime = Field(..., description="When to send reminder")
    conversational_tone: str = Field("supportive", description="Conversational tone")
    motivational_image_enabled: bool = Field(True, description="Include motivational image")

class ReminderResponse(BaseModel):
    id: int
    uuid: str
    title: str
    message: str
    reminder_type: str
    scheduled_time: datetime
    conversational_tone: str
    delivered: bool
    acknowledged: bool
    user_response: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True