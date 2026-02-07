from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.security import HTTPAuthorizationCredentials
from typing import List, Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from auth import verify_token, security
from gemini_ai_service import gemini_service
from pydantic import BaseModel
from datetime import datetime
import logging
import uuid

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/schedule", tags=["schedule"])

class ScheduleRequest(BaseModel):
    timeframe: str  # 'daily', 'weekly', 'monthly'
    preferences: Dict[str, Any] = {}
    start_date: Optional[datetime] = None
    goals: List[str] = []

class ScheduleModification(BaseModel):
    type: str  # 'update_block', 'add_block', 'delete_block'
    block_id: Optional[str] = None
    block_data: Optional[Dict[str, Any]] = None
    updates: Optional[Dict[str, Any]] = None

@router.post("/generate")
async def generate_schedule(
    request: ScheduleRequest,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
):
    """Generate a new personalized schedule using Gemini AI"""
    try:
        user = await verify_token(credentials.credentials)
        user_id = user["id"]
        
        # Prepare user data for AI
        user_data = {
            "user_id": user_id,
            "goals": request.goals or ["productivity", "health"],
            "preferences": request.preferences,
            "timeframe": request.timeframe,
            "available_hours": request.preferences.get("available_hours", 8)
        }
        
        # Generate schedule using Gemini AI
        schedule = await gemini_service.generate_schedule(user_data)
        
        # Add metadata
        schedule["user_id"] = user_id
        schedule["timeframe"] = request.timeframe
        
        return {
            "success": True,
            "message": "Schedule generated successfully",
            "schedule_id": schedule.get("schedule_id"),
            "blocks": schedule.get("blocks", []),
            "generated_at": schedule.get("generated_at")
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating schedule: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{schedule_id}")
async def update_schedule(
    schedule_id: str,
    modifications: List[ScheduleModification],
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
):
    """Update an existing schedule"""
    try:
        user = await verify_token(credentials.credentials)
        
        return {
            "success": True,
            "message": "Schedule updated successfully",
            "schedule_id": schedule_id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating schedule: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/")
async def get_schedules_root(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
):
    """Get user's schedules - root endpoint"""
    return await get_user_schedules(credentials=credentials, db=db)

@router.get("/tasks")
async def get_user_tasks(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
):
    """Get user's tasks"""
    try:
        # Verify user authentication
        user = await verify_token(credentials.credentials)
        user_id = user["id"]
        
        # TODO: Implement database query to get user tasks
        # For now, return placeholder data
        
        return {
            "success": True,
            "data": {
                "tasks": [],
                "total": 0
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting user tasks: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/user")
async def get_user_schedules(
    timeframe: Optional[str] = Query(None, description="Filter by timeframe"),
    status: Optional[str] = Query("active", description="Filter by status"),
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
):
    """Get user's schedules"""
    try:
        # Verify user authentication
        user = await verify_token(credentials.credentials)
        user_id = user["id"]
        
        # TODO: Implement database query to get user schedules
        # For now, return placeholder data
        
        return {
            "success": True,
            "data": {
                "schedules": [],
                "total": 0
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting user schedules: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/{schedule_id}")
async def get_schedule(
    schedule_id: str,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
):
    """Get a specific schedule by ID"""
    try:
        # Verify user authentication
        user = await verify_token(credentials.credentials)
        
        # TODO: Implement database query to get specific schedule
        # For now, return placeholder data
        
        return {
            "success": True,
            "data": {
                "schedule_id": schedule_id,
                "title": "Sample Schedule",
                "blocks": []
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting schedule: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")