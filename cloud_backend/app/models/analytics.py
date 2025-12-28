"""
Analytics models for progress tracking and premium visual analytics
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, JSON, Float
from sqlalchemy.sql import func
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field
from datetime import datetime
import uuid

from ..core.database import Base

class ProgressTracking(Base):
    """Progress tracking with real-time calculation and cloud synchronization"""
    __tablename__ = "progress_tracking"
    
    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String, unique=True, index=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(Integer, nullable=False, index=True)
    
    # Progress metrics
    metric_name = Column(String, nullable=False)  # task_completion, goal_progress, focus_time, etc.
    metric_category = Column(String, nullable=False)  # health, career, finance, personal
    current_value = Column(Float, nullable=False)
    target_value = Column(Float, nullable=False)
    unit = Column(String)  # percentage, hours, count, etc.
    
    # Real-time calculation and cloud sync
    real_time_updates = Column(Boolean, default=True)
    last_calculation = Column(DateTime(timezone=True), server_default=func.now())
    cloud_sync_enabled = Column(Boolean, default=True)
    sync_status = Column(String, default="synced")  # synced, pending, failed
    
    # Progress analysis
    progress_percentage = Column(Float, default=0.0)
    trend_direction = Column(String)  # improving, declining, stable
    velocity = Column(Float)  # Rate of progress change
    predicted_completion_date = Column(DateTime(timezone=True))
    
    # Milestone tracking
    milestones = Column(JSON)  # List of milestone definitions and status
    milestones_achieved = Column(Integer, default=0)
    next_milestone = Column(JSON)  # Next milestone details
    milestone_celebration_due = Column(Boolean, default=False)
    
    # Visual analytics integration
    visual_representation_type = Column(String, default="photorealistic")
    chart_data = Column(JSON)  # Data for chart generation
    ai_generated_insights = Column(JSON)  # AI-generated insights about progress
    
    # Recovery and adjustment tracking (Reclaim AI inspired)
    recovery_actions_suggested = Column(JSON)  # Suggested recovery actions
    recovery_actions_taken = Column(JSON)  # Actions actually taken
    adjustment_recommendations = Column(JSON)  # System recommendations
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_milestone_achieved = Column(DateTime(timezone=True))

class VisualAnalytics(Base):
    """Premium visual analytics with AI-generated HD visuals"""
    __tablename__ = "visual_analytics"
    
    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String, unique=True, index=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(Integer, nullable=False, index=True)
    progress_tracking_id = Column(Integer, index=True)
    
    # Visual content details
    visual_type = Column(String, nullable=False)  # progress_chart, milestone_celebration, recovery_motivation
    title = Column(String, nullable=False)
    description = Column(Text)
    
    # AI-generated visual content (DALL-E, Midjourney, Stable Diffusion)
    ai_generated = Column(Boolean, default=True)
    generation_prompt = Column(Text)  # Prompt used for AI generation
    ai_model_used = Column(String)  # dall-e-3, midjourney, stable-diffusion
    generation_parameters = Column(JSON)  # Model-specific parameters
    
    # Photorealistic quality validation
    photorealistic_quality = Column(Boolean, default=True)
    quality_score = Column(Float)  # Quality assessment score
    realism_score = Column(Float)  # How realistic the image appears
    professional_grade = Column(Boolean, default=False)  # Professional photography quality
    
    # Visual content categories
    content_category = Column(String, nullable=False)  # health_progress, financial_success, productivity, wellness
    visual_theme = Column(String)  # real_people_exercising, healthy_meals, success_environments, etc.
    emotional_tone = Column(String)  # motivational, celebratory, encouraging, inspiring
    
    # Premium features for paid appeal
    hd_quality = Column(Boolean, default=True)
    ultra_hd_available = Column(Boolean, default=False)
    interactive_elements = Column(JSON)  # Interactive chart elements
    animation_enabled = Column(Boolean, default=False)
    
    # File storage and delivery
    image_url = Column(String)  # URL to generated image
    thumbnail_url = Column(String)  # Thumbnail version
    mobile_optimized_url = Column(String)  # Mobile-optimized version
    file_size_bytes = Column(Integer)
    
    # Usage and engagement metrics
    view_count = Column(Integer, default=0)
    user_rating = Column(Float)  # User rating of the visual
    engagement_score = Column(Float)  # How engaging the visual is
    shared_count = Column(Integer, default=0)
    
    # Export and sharing capabilities
    exportable = Column(Boolean, default=True)
    export_formats = Column(JSON)  # Available export formats
    sharing_enabled = Column(Boolean, default=True)
    social_media_optimized = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_viewed = Column(DateTime(timezone=True))

class GoalMetrics(Base):
    """Goal metrics with AI-driven insights and celebration systems"""
    __tablename__ = "goal_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String, unique=True, index=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(Integer, nullable=False, index=True)
    
    # Goal definition
    goal_name = Column(String, nullable=False)
    goal_category = Column(String, nullable=False)  # health, career, finance, relationships, personal
    goal_description = Column(Text)
    target_date = Column(DateTime(timezone=True))
    
    # Metrics and measurement
    measurement_type = Column(String, nullable=False)  # quantitative, qualitative, milestone_based
    current_value = Column(Float)
    target_value = Column(Float)
    unit_of_measurement = Column(String)
    measurement_frequency = Column(String, default="daily")  # daily, weekly, monthly
    
    # AI-driven insights and analysis
    ai_insights_enabled = Column(Boolean, default=True)
    pattern_analysis = Column(JSON)  # AI-detected patterns in progress
    success_predictors = Column(JSON)  # Factors that predict success
    risk_factors = Column(JSON)  # Factors that might hinder progress
    ai_recommendations = Column(JSON)  # AI-generated recommendations
    
    # Progress and achievement tracking
    progress_percentage = Column(Float, default=0.0)
    streak_count = Column(Integer, default=0)
    longest_streak = Column(Integer, default=0)
    setbacks_count = Column(Integer, default=0)
    recovery_time_average = Column(Float)  # Average time to recover from setbacks
    
    # Celebration and motivation system
    celebration_milestones = Column(JSON)  # Milestone definitions for celebrations
    celebrations_triggered = Column(Integer, default=0)
    last_celebration_date = Column(DateTime(timezone=True))
    celebration_visual_style = Column(String, default="achievement_scenes")
    
    # Photorealistic celebratory content
    celebration_images_enabled = Column(Boolean, default=True)
    success_visualization_type = Column(String, default="real_people_achieving")
    motivational_scenes = Column(JSON)  # Types of motivational scenes to generate
    
    # Social and sharing features
    sharing_enabled = Column(Boolean, default=False)
    public_progress = Column(Boolean, default=False)
    accountability_partners = Column(JSON)  # List of accountability partner IDs
    
    # Performance analytics
    consistency_score = Column(Float, default=0.0)
    momentum_score = Column(Float, default=0.0)
    difficulty_rating = Column(Float)  # User-assessed difficulty
    satisfaction_rating = Column(Float)  # User satisfaction with progress
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_progress_update = Column(DateTime(timezone=True))
    goal_achieved_date = Column(DateTime(timezone=True))

# Pydantic models for API requests/responses
class ProgressTrackingCreate(BaseModel):
    metric_name: str = Field(..., description="Name of the metric to track")
    metric_category: str = Field(..., description="Category of the metric")
    current_value: float = Field(..., description="Current value")
    target_value: float = Field(..., description="Target value")
    unit: Optional[str] = None
    real_time_updates: bool = Field(True, description="Enable real-time updates")

class ProgressTrackingResponse(BaseModel):
    id: int
    uuid: str
    user_id: int
    metric_name: str
    metric_category: str
    current_value: float
    target_value: float
    progress_percentage: float
    trend_direction: Optional[str]
    milestones_achieved: int
    milestone_celebration_due: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class VisualAnalyticsCreate(BaseModel):
    visual_type: str = Field(..., description="Type of visual content")
    title: str = Field(..., description="Title of the visual")
    description: Optional[str] = None
    content_category: str = Field(..., description="Content category")
    visual_theme: Optional[str] = None
    ai_generated: bool = Field(True, description="Use AI generation")
    photorealistic_quality: bool = Field(True, description="Ensure photorealistic quality")

class VisualAnalyticsResponse(BaseModel):
    id: int
    uuid: str
    user_id: int
    visual_type: str
    title: str
    content_category: str
    ai_generated: bool
    photorealistic_quality: bool
    quality_score: Optional[float]
    image_url: Optional[str]
    hd_quality: bool
    view_count: int
    user_rating: Optional[float]
    created_at: datetime
    
    class Config:
        from_attributes = True

class GoalMetricsCreate(BaseModel):
    goal_name: str = Field(..., description="Name of the goal")
    goal_category: str = Field(..., description="Category of the goal")
    goal_description: Optional[str] = None
    target_date: Optional[datetime] = None
    measurement_type: str = Field(..., description="Type of measurement")
    target_value: Optional[float] = None
    unit_of_measurement: Optional[str] = None
    ai_insights_enabled: bool = Field(True, description="Enable AI insights")

class GoalMetricsResponse(BaseModel):
    id: int
    uuid: str
    user_id: int
    goal_name: str
    goal_category: str
    measurement_type: str
    current_value: Optional[float]
    target_value: Optional[float]
    progress_percentage: float
    streak_count: int
    celebrations_triggered: int
    consistency_score: float
    momentum_score: float
    created_at: datetime
    
    class Config:
        from_attributes = True