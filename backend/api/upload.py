from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from fastapi.security import HTTPAuthorizationCredentials
from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from auth import verify_token, security
from upload_service import upload_service
from models import KnowledgeEntryCreate, KnowledgeEntryResponse
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/upload", tags=["upload"])

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
        
        # Process the document
        result = await upload_service.process_document(file, user_id)
        
        return {
            "success": True,
            "message": "Document processed successfully",
            "data": result
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in upload_document: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

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
        
        # Process the text
        result = await upload_service.process_text_input(text, user_id)
        
        return {
            "success": True,
            "message": "Text processed successfully",
            "data": result
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in upload_text: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/voice")
async def upload_voice(
    audio_file: UploadFile = File(...),
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
):
    """Upload and process voice input"""
    try:
        # Verify user authentication
        user = await verify_token(credentials.credentials)
        user_id = user["id"]
        
        # Read audio data
        audio_data = await audio_file.read()
        
        # Process the voice input
        result = await upload_service.process_voice_input(audio_data, user_id)
        
        return {
            "success": True,
            "message": "Voice input processed successfully",
            "data": result
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in upload_voice: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

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