"""
Enhanced upload processing service with cloud processing and mobile optimization
Task 3.1: Implement enhanced document parsing with cloud processing
"""

import asyncio
import uuid
from datetime import datetime
from typing import Optional, Dict, Any, List, BinaryIO
from pathlib import Path
import mimetypes
import hashlib
from io import BytesIO

from fastapi import UploadFile, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import aiofiles
import aiofiles.os
from PIL import Image
import PyPDF2
import docx
from pydantic import BaseModel

from ..models.knowledge import KnowledgeBase, Document, ProcessingMetadata
from ..models.user import User
from ..core.config import settings
from ..core.database import get_postgres_session
from .document_parser import DocumentParser
from .voice_processor import VoiceProcessor
from .file_storage import FileStorageService

class UploadResult(BaseModel):
    """Result of upload processing"""
    success: bool
    document_id: Optional[str] = None
    knowledge_base_id: Optional[str] = None
    processing_status: str
    message: str
    file_info: Optional[Dict[str, Any]] = None
    mobile_preview_url: Optional[str] = None
    thumbnail_url: Optional[str] = None

class UploadService:
    """Enhanced upload processing service with cloud processing and mobile optimization"""
    
    def __init__(self):
        self.document_parser = DocumentParser()
        self.voice_processor = VoiceProcessor()
        self.file_storage = FileStorageService()
        
        # Mobile optimization settings
        self.mobile_image_max_width = 800
        self.mobile_image_max_height = 600
        self.mobile_image_quality = 85
        
        # Cloud processing settings
        self.max_file_size = 100 * 1024 * 1024  # 100MB
        self.allowed_extensions = {
            'documents': ['.pdf', '.docx', '.doc', '.txt', '.rtf', '.odt'],
            'images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'],
            'audio': ['.mp3', '.wav', '.m4a', '.aac', '.ogg'],
            'video': ['.mp4', '.avi', '.mov', '.wmv', '.flv']
        }
        
    async def process_upload(
        self,
        file: UploadFile,
        user_id: int,
        mobile_optimized: bool = True,
        cloud_processing: bool = True,
        processing_priority: str = "normal"
    ) -> UploadResult:
        """
        Process uploaded file with cloud-based NLP processing and mobile optimization
        
        Args:
            file: Uploaded file
            user_id: User ID
            mobile_optimized: Enable mobile optimization
            cloud_processing: Enable cloud-based processing
            processing_priority: Processing priority (low, normal, high, urgent)
        """
        try:
            # Validate file
            validation_result = await self._validate_file(file)
            if not validation_result["valid"]:
                return UploadResult(
                    success=False,
                    processing_status="failed",
                    message=validation_result["error"]
                )
            
            # Generate unique identifiers
            document_uuid = str(uuid.uuid4())
            knowledge_base_uuid = str(uuid.uuid4())
            
            # Read file content
            file_content = await file.read()
            file_hash = hashlib.sha256(file_content).hexdigest()
            
            # Store file securely
            storage_result = await self.file_storage.store_file(
                file_content=file_content,
                filename=file.filename,
                user_id=user_id,
                document_uuid=document_uuid,
                encrypted=True
            )
            
            if not storage_result["success"]:
                return UploadResult(
                    success=False,
                    processing_status="failed",
                    message=f"File storage failed: {storage_result['error']}"
                )
            
            # Create database records
            async with get_postgres_session() as session:
                # Create document record
                document = Document(
                    uuid=document_uuid,
                    user_id=user_id,
                    original_filename=file.filename,
                    file_type=Path(file.filename).suffix.lower(),
                    file_size=len(file_content),
                    mime_type=file.content_type,
                    storage_path=storage_result["storage_path"],
                    encrypted=True,
                    encryption_key_id=storage_result["encryption_key_id"],
                    upload_status="processing",
                    mobile_preview_available=False,
                    cloud_backup_enabled=True
                )
                
                session.add(document)
                await session.flush()
                
                # Create knowledge base entry
                knowledge_base = KnowledgeBase(
                    uuid=knowledge_base_uuid,
                    user_id=user_id,
                    title=file.filename,
                    content="",  # Will be populated by processing
                    content_type=self._determine_content_type(file.filename, file.content_type),
                    source_file_name=file.filename,
                    source_file_size=len(file_content),
                    processing_status="pending",
                    ai_processing_enabled=cloud_processing,
                    cloud_processing_flag=cloud_processing,
                    processing_priority=processing_priority,
                    mobile_optimized=mobile_optimized
                )
                
                session.add(knowledge_base)
                await session.commit()
            
            # Start background processing
            asyncio.create_task(self._process_file_content(
                document_uuid=document_uuid,
                knowledge_base_uuid=knowledge_base_uuid,
                file_content=file_content,
                filename=file.filename,
                content_type=file.content_type,
                user_id=user_id,
                mobile_optimized=mobile_optimized,
                cloud_processing=cloud_processing
            ))
            
            # Generate mobile preview if needed
            mobile_preview_url = None
            thumbnail_url = None
            
            if mobile_optimized and self._is_image_file(file.filename):
                preview_result = await self._create_mobile_preview(
                    file_content, document_uuid, user_id
                )
                mobile_preview_url = preview_result.get("preview_url")
                thumbnail_url = preview_result.get("thumbnail_url")
            
            return UploadResult(
                success=True,
                document_id=document_uuid,
                knowledge_base_id=knowledge_base_uuid,
                processing_status="processing",
                message="File uploaded successfully and processing started",
                file_info={
                    "filename": file.filename,
                    "size": len(file_content),
                    "type": file.content_type,
                    "hash": file_hash
                },
                mobile_preview_url=mobile_preview_url,
                thumbnail_url=thumbnail_url
            )
            
        except Exception as e:
            return UploadResult(
                success=False,
                processing_status="failed",
                message=f"Upload processing failed: {str(e)}"
            )
    
    async def _validate_file(self, file: UploadFile) -> Dict[str, Any]:
        """Validate uploaded file"""
        if not file.filename:
            return {"valid": False, "error": "No filename provided"}
        
        # Check file extension
        file_ext = Path(file.filename).suffix.lower()
        all_allowed = []
        for exts in self.allowed_extensions.values():
            all_allowed.extend(exts)
        
        if file_ext not in all_allowed:
            return {"valid": False, "error": f"File type {file_ext} not allowed"}
        
        # Check file size (read first to get size)
        file.file.seek(0, 2)  # Seek to end
        file_size = file.file.tell()
        file.file.seek(0)  # Reset to beginning
        
        if file_size > self.max_file_size:
            return {"valid": False, "error": f"File size {file_size} exceeds maximum {self.max_file_size}"}
        
        if file_size == 0:
            return {"valid": False, "error": "Empty file not allowed"}
        
        return {"valid": True}
    
    def _determine_content_type(self, filename: str, mime_type: str) -> str:
        """Determine content type for processing"""
        file_ext = Path(filename).suffix.lower()
        
        if file_ext in self.allowed_extensions['documents']:
            return "document"
        elif file_ext in self.allowed_extensions['images']:
            return "image"
        elif file_ext in self.allowed_extensions['audio']:
            return "voice"
        elif file_ext in self.allowed_extensions['video']:
            return "video"
        else:
            return "unknown"
    
    def _is_image_file(self, filename: str) -> bool:
        """Check if file is an image"""
        file_ext = Path(filename).suffix.lower()
        return file_ext in self.allowed_extensions['images']
    
    async def _create_mobile_preview(
        self, 
        file_content: bytes, 
        document_uuid: str, 
        user_id: int
    ) -> Dict[str, Any]:
        """Create mobile-optimized preview and thumbnail"""
        try:
            # Open image
            image = Image.open(BytesIO(file_content))
            
            # Create mobile preview
            preview_image = image.copy()
            preview_image.thumbnail(
                (self.mobile_image_max_width, self.mobile_image_max_height),
                Image.Resampling.LANCZOS
            )
            
            # Create thumbnail
            thumbnail_image = image.copy()
            thumbnail_image.thumbnail((200, 200), Image.Resampling.LANCZOS)
            
            # Save preview and thumbnail
            preview_buffer = BytesIO()
            thumbnail_buffer = BytesIO()
            
            # Use JPEG for better compression
            format_type = "JPEG" if image.mode == "RGB" else "PNG"
            
            preview_image.save(
                preview_buffer, 
                format=format_type, 
                quality=self.mobile_image_quality,
                optimize=True
            )
            
            thumbnail_image.save(
                thumbnail_buffer,
                format=format_type,
                quality=70,
                optimize=True
            )
            
            # Store preview and thumbnail
            preview_result = await self.file_storage.store_file(
                file_content=preview_buffer.getvalue(),
                filename=f"{document_uuid}_preview.jpg",
                user_id=user_id,
                document_uuid=f"{document_uuid}_preview",
                encrypted=False  # Previews don't need encryption
            )
            
            thumbnail_result = await self.file_storage.store_file(
                file_content=thumbnail_buffer.getvalue(),
                filename=f"{document_uuid}_thumbnail.jpg",
                user_id=user_id,
                document_uuid=f"{document_uuid}_thumbnail",
                encrypted=False
            )
            
            return {
                "preview_url": preview_result.get("public_url"),
                "thumbnail_url": thumbnail_result.get("public_url")
            }
            
        except Exception as e:
            print(f"Error creating mobile preview: {e}")
            return {}
    
    async def _process_file_content(
        self,
        document_uuid: str,
        knowledge_base_uuid: str,
        file_content: bytes,
        filename: str,
        content_type: str,
        user_id: int,
        mobile_optimized: bool,
        cloud_processing: bool
    ):
        """Background processing of file content with cloud-based NLP"""
        processing_start_time = datetime.utcnow()
        
        try:
            # Create processing metadata
            async with get_postgres_session() as session:
                processing_metadata = ProcessingMetadata(
                    uuid=str(uuid.uuid4()),
                    knowledge_base_id=knowledge_base_uuid,
                    user_id=user_id,
                    operation_type="content_extraction",
                    processing_engine="cloud_nlp",
                    model_version="v1.0",
                    cloud_provider="aws",  # or gcp, azure
                    processing_region=settings.AWS_REGION,
                    started_at=processing_start_time
                )
                
                session.add(processing_metadata)
                await session.commit()
            
            # Extract content based on file type
            extracted_content = ""
            content_metadata = {}
            
            file_ext = Path(filename).suffix.lower()
            
            if file_ext == '.pdf':
                extracted_content, content_metadata = await self.document_parser.parse_pdf(file_content)
            elif file_ext in ['.docx', '.doc']:
                extracted_content, content_metadata = await self.document_parser.parse_docx(file_content)
            elif file_ext == '.txt':
                extracted_content = file_content.decode('utf-8', errors='ignore')
            elif file_ext in self.allowed_extensions['audio']:
                if cloud_processing:
                    extracted_content, content_metadata = await self.voice_processor.transcribe_audio(
                        file_content, filename
                    )
            elif file_ext in self.allowed_extensions['images']:
                if cloud_processing:
                    extracted_content, content_metadata = await self.document_parser.extract_text_from_image(
                        file_content
                    )
            
            # Process with cloud-based NLP if enabled
            ai_results = {}
            if cloud_processing and extracted_content:
                ai_results = await self._process_with_cloud_nlp(
                    extracted_content, user_id, processing_metadata.uuid
                )
            
            # Update knowledge base with results
            async with get_postgres_session() as session:
                # Update knowledge base
                kb_result = await session.get(KnowledgeBase, knowledge_base_uuid)
                if kb_result:
                    kb_result.content = extracted_content
                    kb_result.processing_status = "completed"
                    kb_result.categories = ai_results.get("categories", [])
                    kb_result.tags = ai_results.get("tags", [])
                    kb_result.sentiment_score = ai_results.get("sentiment_score")
                    kb_result.confidence_score = ai_results.get("confidence_score")
                    kb_result.patterns_detected = ai_results.get("patterns", {})
                    kb_result.actionable_items = ai_results.get("actionable_items", [])
                    kb_result.mobile_optimized = mobile_optimized
                    kb_result.visual_summary_available = bool(content_metadata.get("has_images"))
                
                # Update document status
                doc_result = await session.get(Document, document_uuid)
                if doc_result:
                    doc_result.upload_status = "processed"
                    doc_result.processing_progress = 1.0
                    doc_result.processed_at = datetime.utcnow()
                
                # Update processing metadata
                proc_result = await session.get(ProcessingMetadata, processing_metadata.uuid)
                if proc_result:
                    processing_duration = (datetime.utcnow() - processing_start_time).total_seconds()
                    proc_result.processing_duration = processing_duration
                    proc_result.completed_at = datetime.utcnow()
                    proc_result.success_rate = 1.0 if extracted_content else 0.5
                    proc_result.accuracy_score = ai_results.get("confidence_score", 0.8)
                
                await session.commit()
                
        except Exception as e:
            # Handle processing errors
            async with get_postgres_session() as session:
                # Update knowledge base with error
                kb_result = await session.get(KnowledgeBase, knowledge_base_uuid)
                if kb_result:
                    kb_result.processing_status = "failed"
                
                # Update document with error
                doc_result = await session.get(Document, document_uuid)
                if doc_result:
                    doc_result.upload_status = "failed"
                    doc_result.processing_errors = [{"error": str(e), "timestamp": datetime.utcnow().isoformat()}]
                
                await session.commit()
            
            print(f"Error processing file content: {e}")
    
    async def _process_with_cloud_nlp(
        self, 
        content: str, 
        user_id: int, 
        processing_id: str
    ) -> Dict[str, Any]:
        """Process content with cloud-based NLP (placeholder for actual implementation)"""
        # This would integrate with actual cloud NLP services like:
        # - OpenAI GPT for content analysis
        # - Google Cloud Natural Language API
        # - AWS Comprehend
        # - Azure Cognitive Services
        
        # Placeholder implementation
        await asyncio.sleep(0.1)  # Simulate processing time
        
        # Mock AI results
        words = content.split()
        
        return {
            "categories": ["general", "document"],
            "tags": words[:10] if len(words) > 10 else words,
            "sentiment_score": 0.7,
            "confidence_score": 0.85,
            "patterns": {
                "word_count": len(words),
                "has_dates": "date" in content.lower() or "time" in content.lower(),
                "has_numbers": any(char.isdigit() for char in content)
            },
            "actionable_items": [
                {
                    "type": "task",
                    "text": "Review document content",
                    "priority": "medium",
                    "confidence": 0.8
                }
            ]
        }
    
    async def get_upload_status(self, document_uuid: str, user_id: int) -> Dict[str, Any]:
        """Get upload processing status"""
        async with get_postgres_session() as session:
            # Get document
            document = await session.get(Document, document_uuid)
            if not document or document.user_id != user_id:
                raise HTTPException(status_code=404, detail="Document not found")
            
            # Get knowledge base
            knowledge_base = await session.get(KnowledgeBase, document.knowledge_base_id)
            
            return {
                "document_uuid": document_uuid,
                "upload_status": document.upload_status,
                "processing_progress": document.processing_progress,
                "processing_status": knowledge_base.processing_status if knowledge_base else "unknown",
                "mobile_preview_available": document.mobile_preview_available,
                "mobile_preview_path": document.mobile_preview_path,
                "thumbnail_path": document.thumbnail_path,
                "processed_at": document.processed_at,
                "errors": document.processing_errors or []
            }
    
    async def delete_upload(self, document_uuid: str, user_id: int) -> Dict[str, Any]:
        """Securely delete uploaded file and associated data"""
        async with get_postgres_session() as session:
            # Get document
            document = await session.get(Document, document_uuid)
            if not document or document.user_id != user_id:
                raise HTTPException(status_code=404, detail="Document not found")
            
            # Delete from storage
            storage_result = await self.file_storage.delete_file(
                document.storage_path, document.encryption_key_id
            )
            
            # Delete preview and thumbnail if they exist
            if document.mobile_preview_path:
                await self.file_storage.delete_file(document.mobile_preview_path)
            if document.thumbnail_path:
                await self.file_storage.delete_file(document.thumbnail_path)
            
            # Delete database records
            if document.knowledge_base_id:
                knowledge_base = await session.get(KnowledgeBase, document.knowledge_base_id)
                if knowledge_base:
                    await session.delete(knowledge_base)
            
            await session.delete(document)
            await session.commit()
            
            return {
                "success": True,
                "message": "Document and associated data deleted successfully",
                "storage_deleted": storage_result.get("success", False)
            }