"""
Enhanced knowledge base and schedule models with AI processing metadata and cloud processing flags
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, JSON, Float, LargeBinary
from sqlalchemy.sql import func
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field
from datetime import datetime
import uuid

from ..core.database import Base

class KnowledgeBase(Base):
    """Enhanced knowledge base with AI processing metadata and cloud processing flags"""
    __tablename__ = "knowledge_base"
    
    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String, unique=True, index=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(Integer, nullable=False, index=True)
    
    # Content information
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    content_type = Column(String, nullable=False)  # document, voice, text, image
    source_file_name = Column(String)
    source_file_size = Column(Integer)
    
    # AI processing metadata
    processing_status = Column(String, default="pending")  # pending, processing, completed, failed
    ai_processing_enabled = Column(Boolean, default=True)
    cloud_processing_flag = Column(Boolean, default=True)
    processing_priority = Column(String, default="normal")  # low, normal, high, urgent
    
    # Content analysis results
    categories = Column(JSON)  # AI-generated categories
    tags = Column(JSON)  # Extracted tags and keywords
    sentiment_score = Column(Float)  # Sentiment analysis result
    confidence_score = Column(Float)  # AI confidence in categorization
    
    # Pattern recognition and insights
    patterns_detected = Column(JSON)  # Recurring themes, habits, preferences
    actionable_items = Column(JSON)  # Tasks, goals, reminders extracted
    related_content_ids = Column(JSON)  # IDs of related knowledge base items
    
    # Mobile optimization flags
    mobile_optimized = Column(Boolean, default=False)
    offline_available = Column(Boolean, default=False)
    sync_priority = Column(String, default="normal")  # low, normal, high
    
    # Visual elements support
    visual_elements = Column(JSON)  # Associated images, charts, diagrams
    ai_generated_visuals = Column(JSON)  # AI-generated visual content metadata
    visual_summary_available = Column(Boolean, default=False)
    
    # Autonomous adjustment tracking
    auto_adjustments_made = Column(Integer, default=0)
    last_adjustment_timestamp = Column(DateTime(timezone=True))
    adjustment_success_rate = Column(Float, default=0.0)
    
    # Focus time protection integration
    focus_time_relevant = Column(Boolean, default=False)
    focus_time_category = Column(String)  # deep_work, creative, analytical, etc.
    estimated_focus_duration = Column(Integer)  # minutes
    
    # Timestamps and versioning
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_accessed = Column(DateTime(timezone=True))
    version = Column(Integer, default=1)

class Document(Base):
    """Document storage with cloud processing and mobile optimization"""
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String, unique=True, index=True, default=lambda: str(uuid.uuid4()))
    knowledge_base_id = Column(Integer, nullable=False, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    
    # File information
    original_filename = Column(String, nullable=False)
    file_type = Column(String, nullable=False)  # pdf, docx, txt, mp3, mp4, etc.
    file_size = Column(Integer, nullable=False)
    mime_type = Column(String)
    
    # Storage information
    storage_path = Column(String, nullable=False)  # S3 path or local path
    encrypted = Column(Boolean, default=True)
    encryption_key_id = Column(String)
    
    # Processing status
    upload_status = Column(String, default="uploaded")  # uploaded, processing, processed, failed
    processing_progress = Column(Float, default=0.0)  # 0.0 to 1.0
    processing_errors = Column(JSON)  # Error messages if processing failed
    
    # Mobile optimization
    mobile_preview_available = Column(Boolean, default=False)
    mobile_preview_path = Column(String)
    thumbnail_path = Column(String)
    compressed_version_path = Column(String)
    
    # Cloud processing flags
    cloud_backup_enabled = Column(Boolean, default=True)
    cloud_backup_path = Column(String)
    sync_status = Column(String, default="synced")  # synced, pending, failed
    
    # Timestamps
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())
    processed_at = Column(DateTime(timezone=True))
    last_accessed = Column(DateTime(timezone=True))

class ProcessingMetadata(Base):
    """Metadata for AI processing operations and cloud ML infrastructure"""
    __tablename__ = "processing_metadata"
    
    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String, unique=True, index=True, default=lambda: str(uuid.uuid4()))
    knowledge_base_id = Column(Integer, nullable=False, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    
    # Processing operation details
    operation_type = Column(String, nullable=False)  # categorization, extraction, analysis, etc.
    processing_engine = Column(String, nullable=False)  # openai, google, custom, etc.
    model_version = Column(String, nullable=False)
    
    # Cloud ML infrastructure details
    cloud_provider = Column(String)  # aws, gcp, azure
    compute_instance_type = Column(String)
    processing_region = Column(String)
    estimated_cost = Column(Float)
    actual_cost = Column(Float)
    
    # Performance metrics
    processing_duration = Column(Float)  # seconds
    tokens_processed = Column(Integer)
    api_calls_made = Column(Integer)
    success_rate = Column(Float)
    
    # Quality metrics
    accuracy_score = Column(Float)
    relevance_score = Column(Float)
    user_feedback_score = Column(Float)
    manual_corrections_needed = Column(Integer)
    
    # Resource usage
    memory_usage_mb = Column(Float)
    cpu_usage_percent = Column(Float)
    network_bandwidth_mb = Column(Float)
    storage_used_mb = Column(Float)
    
    # Error handling and debugging
    error_count = Column(Integer, default=0)
    warning_count = Column(Integer, default=0)
    debug_logs = Column(JSON)
    retry_count = Column(Integer, default=0)
    
    # Timestamps
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True))
    last_retry_at = Column(DateTime(timezone=True))

# Pydantic models for API requests/responses
class KnowledgeBaseCreate(BaseModel):
    title: str = Field(..., description="Title of the knowledge base item")
    content: str = Field(..., description="Content text")
    content_type: str = Field(..., description="Type of content")
    ai_processing_enabled: bool = Field(True, description="Enable AI processing")
    cloud_processing_flag: bool = Field(True, description="Enable cloud processing")
    processing_priority: str = Field("normal", description="Processing priority")

class KnowledgeBaseResponse(BaseModel):
    id: int
    uuid: str
    user_id: int
    title: str
    content_type: str
    processing_status: str
    categories: Optional[List[str]]
    tags: Optional[List[str]]
    confidence_score: Optional[float]
    patterns_detected: Optional[Dict[str, Any]]
    actionable_items: Optional[List[Dict[str, Any]]]
    mobile_optimized: bool
    visual_summary_available: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class DocumentUpload(BaseModel):
    original_filename: str = Field(..., description="Original filename")
    file_type: str = Field(..., description="File type/extension")
    file_size: int = Field(..., description="File size in bytes")
    encrypted: bool = Field(True, description="Whether file should be encrypted")
    mobile_preview_required: bool = Field(True, description="Generate mobile preview")

class DocumentResponse(BaseModel):
    id: int
    uuid: str
    knowledge_base_id: int
    original_filename: str
    file_type: str
    file_size: int
    upload_status: str
    processing_progress: float
    mobile_preview_available: bool
    cloud_backup_enabled: bool
    sync_status: str
    uploaded_at: datetime
    
    class Config:
        from_attributes = True

class ProcessingMetadataResponse(BaseModel):
    id: int
    uuid: str
    operation_type: str
    processing_engine: str
    model_version: str
    processing_duration: Optional[float]
    accuracy_score: Optional[float]
    success_rate: Optional[float]
    error_count: int
    started_at: datetime
    completed_at: Optional[datetime]
    
    class Config:
        from_attributes = True