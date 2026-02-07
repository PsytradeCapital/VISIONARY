from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from fastapi.security import HTTPAuthorizationCredentials
from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from auth import verify_token, security
from gemini_ai_service import gemini_service
from models import KnowledgeEntryCreate, KnowledgeEntryResponse, KnowledgeEntry
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/upload", tags=["upload"])

@router.get("/status")
async def get_upload_status(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
):
    """Get upload service status"""
    try:
        # Verify user authentication
        user = await verify_token(credentials.credentials)
        
        return {
            "success": True,
            "status": "operational",
            "supported_formats": ["pdf", "txt", "docx", "mp3", "wav", "m4a"],
            "max_file_size": "10MB"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting upload status: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/document")
async def upload_document(
    file: UploadFile = File(...),
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
):
    """Upload and process a document (PDF, TXT, DOCX)"""
    try:
        # Verify user authentication
        user = await verify_token(credentials.credentials)
        user_id = user["id"]
        
        # Convert user_id to UUID if it's a string
        import uuid
        if isinstance(user_id, str):
            user_id = uuid.UUID(user_id)
        
        # Read file content
        content = await file.read()
        text = content.decode('utf-8', errors='ignore')
        
        # Process with Gemini AI
        result = await gemini_service.analyze_document(text)
        
        # Save to database
        knowledge_entry = KnowledgeEntry(
            user_id=user_id,
            source_type='document',
            content=text[:1000],  # Store first 1000 chars
            extracted_data=result.get('tasks', []),
            category=result.get('category', 'task'),
            confidence=result.get('confidence', 0.8)
        )
        
        db.add(knowledge_entry)
        await db.commit()
        await db.refresh(knowledge_entry)
        
        return {
            "success": True,
            "message": "Document processed and saved successfully",
            "data": {
                "id": str(knowledge_entry.id),
                "filename": file.filename,
                "category": knowledge_entry.category,
                "tasks": result.get('tasks', []),
                "summary": result.get('summary', ''),
                "confidence": knowledge_entry.confidence
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in upload_document: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.post("/text")
async def upload_text(
    text: str = Form(...),
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
):
    """Process direct text input"""
    try:
        # Verify user authentication
        user = await verify_token(credentials.credentials)
        user_id = user["id"]
        
        # Convert user_id to UUID if it's a string
        import uuid
        if isinstance(user_id, str):
            user_id = uuid.UUID(user_id)
        
        # Process with Gemini AI
        result = await gemini_service.analyze_document(text)
        
        # Save to database
        knowledge_entry = KnowledgeEntry(
            user_id=user_id,
            source_type='text',
            content=text,
            extracted_data=result.get('tasks', []),
            category=result.get('category', 'task'),
            confidence=result.get('confidence', 0.8)
        )
        
        db.add(knowledge_entry)
        await db.commit()
        await db.refresh(knowledge_entry)
        
        return {
            "success": True,
            "message": "Text processed and saved successfully",
            "data": {
                "id": str(knowledge_entry.id),
                "content_length": len(text),
                "category": knowledge_entry.category,
                "tasks": result.get('tasks', []),
                "summary": result.get('summary', ''),
                "confidence": knowledge_entry.confidence
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in upload_text: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.post("/voice")
async def upload_voice(
    file: UploadFile = File(...),
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
):
    """Upload and process voice recording"""
    try:
        # Verify user authentication
        user = await verify_token(credentials.credentials)
        user_id = user["id"]
        
        # Convert user_id to UUID if it's a string
        import uuid
        if isinstance(user_id, str):
            user_id = uuid.UUID(user_id)
        
        # For now, return placeholder for voice
        result = {
            "transcribed_text": "Voice transcription coming soon",
            "category": "task",
            "confidence": 0.5,
            "extracted_items": {}
        }
        
        # Save to database
        knowledge_entry = KnowledgeEntry(
            user_id=user_id,
            source_type='voice',
            content=result.get('transcribed_text', 'Voice transcription coming soon'),
            extracted_data=result.get('tasks', []),
            category=result.get('category', 'task'),
            confidence=result.get('confidence', 0.5)
        )
        
        db.add(knowledge_entry)
        await db.commit()
        await db.refresh(knowledge_entry)
        
        return {
            "success": True,
            "message": "Voice recording processed and saved successfully",
            "data": {
                "id": str(knowledge_entry.id),
                "transcribed_text": result.get('transcribed_text', 'Voice transcription coming soon'),
                "category": knowledge_entry.category,
                "confidence": knowledge_entry.confidence
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in upload_voice: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get("/knowledge")
async def get_knowledge_entries(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
):
    """Get all knowledge entries for the user"""
    try:
        user = await verify_token(credentials.credentials)
        user_id = user["id"]
        
        # Convert user_id to UUID if it's a string
        import uuid
        if isinstance(user_id, str):
            user_id = uuid.UUID(user_id)
        
        from sqlalchemy import select
        result = await db.execute(
            select(KnowledgeEntry).where(KnowledgeEntry.user_id == user_id)
        )
        entries = result.scalars().all()
        
        return {
            "success": True,
            "data": [
                {
                    "id": str(entry.id),
                    "source_type": entry.source_type,
                    "category": entry.category,
                    "content": entry.content[:200] + "..." if len(entry.content) > 200 else entry.content,
                    "extracted_data": entry.extracted_data,
                    "confidence": entry.confidence,
                    "created_at": entry.created_at.isoformat()
                }
                for entry in entries
            ]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting knowledge entries: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get("/history")
async def get_upload_history(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
):
    """Get user's upload history"""
    try:
        # Verify user authentication
        user = await verify_token(credentials.credentials)
        user_id = user["id"]
        
        # TODO: Implement database query to get user's knowledge entries
        # For now, return placeholder data
        
        return {
            "success": True,
            "data": {
                "total_uploads": 0,
                "recent_uploads": []
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_upload_history: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")