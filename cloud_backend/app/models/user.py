"""
Enhanced user profile and vision data models with cloud sync and AI personalization
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, JSON, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field
from datetime import datetime
import uuid

from ..core.database import Base

class User(Base):
    """Enhanced user model with cloud sync settings and AI personalization"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String, unique=True, index=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    
    # Cloud sync and mobile-first settings
    cloud_sync_enabled = Column(Boolean, default=True)
    mobile_primary_device = Column(Boolean, default=True)
    last_sync_timestamp = Column(DateTime(timezone=True), server_default=func.now())
    sync_conflicts_count = Column(Integer, default=0)
    
    # AI personalization settings
    ai_personalization_enabled = Column(Boolean, default=True)
    ai_learning_consent = Column(Boolean, default=False)
    personalization_score = Column(Float, default=0.0)
    ai_model_version = Column(String, default="v1.0")
    
    # Premium features and visual analytics
    premium_subscription = Column(Boolean, default=False)
    visual_analytics_enabled = Column(Boolean, default=True)
    premium_visual_quality = Column(String, default="standard")  # standard, hd, ultra_hd
    
    # Account status and timestamps
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class UserProfile(Base):
    """Enhanced user profile with mobile-first preferences and focus time protection"""
    __tablename__ = "user_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    
    # Personal vision and goals
    personal_vision = Column(Text)
    life_goals = Column(JSON)  # List of structured goals
    priority_areas = Column(JSON)  # Health, Career, Finance, Relationships, etc.
    success_metrics = Column(JSON)  # Custom success indicators
    
    # Focus time protection (Motion/Reclaim AI inspired)
    focus_time_enabled = Column(Boolean, default=True)
    focus_blocks_per_day = Column(Integer, default=2)
    min_focus_duration = Column(Integer, default=60)  # minutes
    focus_time_preferences = Column(JSON)  # Time slots, break preferences
    habit_defense_enabled = Column(Boolean, default=True)
    
    # Mobile-first preferences
    mobile_notifications_enabled = Column(Boolean, default=True)
    push_notification_times = Column(JSON)  # Preferred notification windows
    mobile_theme_preference = Column(String, default="auto")  # light, dark, auto
    touch_friendly_ui = Column(Boolean, default=True)
    offline_mode_enabled = Column(Boolean, default=True)
    
    # Conversational tone settings (Toki inspired)
    conversational_tone = Column(String, default="supportive")  # supportive, professional, casual, motivational
    reminder_personality = Column(String, default="encouraging")
    celebration_style = Column(String, default="enthusiastic")
    recovery_messaging = Column(String, default="gentle")
    
    # AI-generated visual preferences
    visual_style_preference = Column(String, default="photorealistic")
    preferred_image_themes = Column(JSON)  # Nature, urban, minimalist, etc.
    avatar_style = Column(String, default="realistic")
    progress_visualization_type = Column(String, default="photorealistic_scenes")
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class UserPreferences(Base):
    """User preferences for cloud processing and autonomous adjustments"""
    __tablename__ = "user_preferences"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    
    # Cloud processing preferences
    cloud_processing_enabled = Column(Boolean, default=True)
    auto_categorization = Column(Boolean, default=True)
    ai_schedule_generation = Column(Boolean, default=True)
    autonomous_adjustments = Column(Boolean, default=False)  # Requires explicit consent
    
    # Schedule and time management
    work_hours_start = Column(String, default="09:00")
    work_hours_end = Column(String, default="17:00")
    timezone = Column(String, default="UTC")
    calendar_integration = Column(JSON)  # Google, Outlook, Apple Calendar
    
    # AI processing settings
    content_analysis_depth = Column(String, default="standard")  # basic, standard, deep
    pattern_recognition_enabled = Column(Boolean, default=True)
    predictive_scheduling = Column(Boolean, default=True)
    learning_from_feedback = Column(Boolean, default=True)
    
    # Visual and notification preferences
    notification_frequency = Column(String, default="balanced")  # minimal, balanced, frequent
    visual_reminder_style = Column(String, default="photorealistic")
    progress_image_frequency = Column(String, default="weekly")
    celebration_visual_style = Column(String, default="achievement_scenes")
    
    # Privacy and data settings
    data_retention_period = Column(Integer, default=365)  # days
    analytics_sharing = Column(Boolean, default=False)
    usage_data_collection = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

# Pydantic models for API requests/responses
class UserCreate(BaseModel):
    email: str = Field(..., description="User email address")
    password: str = Field(..., min_length=8, description="User password")
    full_name: str = Field(..., description="User full name")
    mobile_primary_device: bool = Field(True, description="Is mobile the primary device")

class UserResponse(BaseModel):
    id: int
    uuid: str
    email: str
    full_name: str
    cloud_sync_enabled: bool
    mobile_primary_device: bool
    ai_personalization_enabled: bool
    premium_subscription: bool
    visual_analytics_enabled: bool
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class UserProfileCreate(BaseModel):
    personal_vision: Optional[str] = None
    life_goals: Optional[List[Dict[str, Any]]] = None
    priority_areas: Optional[List[str]] = None
    focus_time_enabled: bool = True
    conversational_tone: str = "supportive"
    visual_style_preference: str = "photorealistic"

class UserProfileResponse(BaseModel):
    id: int
    user_id: int
    personal_vision: Optional[str]
    life_goals: Optional[List[Dict[str, Any]]]
    focus_time_enabled: bool
    conversational_tone: str
    visual_style_preference: str
    mobile_theme_preference: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class UserPreferencesUpdate(BaseModel):
    cloud_processing_enabled: Optional[bool] = None
    autonomous_adjustments: Optional[bool] = None
    work_hours_start: Optional[str] = None
    work_hours_end: Optional[str] = None
    timezone: Optional[str] = None
    notification_frequency: Optional[str] = None
    visual_reminder_style: Optional[str] = None