from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.security import HTTPAuthorizationCredentials
from typing import List, Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from auth import verify_token, security
from schedule_service import schedule_service, TimeFrame
from pydantic import BaseModel
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/schedule", tags=["schedule"])

class ScheduleRequest(BaseModel):
    timeframe: str  # 'daily', 'weekly', 'monthly'
    preferences: Dict[str, Any] = {}
    start_date: Optional[datetime] = None

class ScheduleModification(BaseModel):
    type: str  # 'update_block', 'add_block', 'delete_block'
    block_id: Optional[str] = None
    block_data: Optional[Dict[str, Any]] = None
    updates: Optional[Dict[str, Any]] = None

class DisruptionRequest(BaseModel):
    type: str  # 'time_conflict', 'activity_unavailable', 'weather'
    details: Dict[str, Any]

@router.post("/generate")
async def generate_schedule(
    request: ScheduleRequest,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
):
    """Generate a new personalized schedule"""
    try:
        # Verify user authentication
        user = await verify_token(credentials.credentials)
        user_id = user["id"]
        
        # Validate timeframe
        try:
            timeframe = TimeFrame(request.timeframe.lower())
        except ValueError:
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid timeframe. Must be one of: {[tf.value for tf in TimeFrame]}"
            )
        
        # Add start_date to preferences if provided
        preferences = request.preferences.copy()
        if request.start_date:
            preferences['start_date'] = request.start_date
        
        # Generate schedule
        schedule = await schedule_service.generate_schedule(
            user_id=user_id,
            timeframe=timeframe,
            preferences=preferences,
            db=db
        )
        
        return {
            "success": True,
            "message": "Schedule generated successfully",
            "data": schedule
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating schedule: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.put("/{schedule_id}")
async def update_schedule(
    schedule_id: str,
    modifications: List[ScheduleModification],
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
):
    """Update an existing schedule with modifications"""
    try:
        # Verify user authentication
        user = await verify_token(credentials.credentials)
        
        # Convert modifications to dict format
        mod_dicts = []
        for mod in modifications:
            mod_dict = {
                'type': mod.type,
                'block_id': mod.block_id,
                'block_data': mod.block_data,
                'updates': mod.updates
            }
            mod_dicts.append(mod_dict)
        
        # Update schedule
        updated_schedule = await schedule_service.update_schedule(
            schedule_id=schedule_id,
            modifications=mod_dicts,
            db=db
        )
        
        return {
            "success": True,
            "message": "Schedule updated successfully",
            "data": updated_schedule
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating schedule: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/{schedule_id}/alternatives")
async def get_alternatives(
    schedule_id: str,
    disruption: DisruptionRequest,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
):
    """Get alternative suggestions for schedule disruptions"""
    try:
        # Verify user authentication
        user = await verify_token(credentials.credentials)
        
        # Get alternatives
        alternatives = await schedule_service.suggest_alternatives(
            schedule_id=schedule_id,
            disruption={
                'type': disruption.type,
                **disruption.details
            },
            db=db
        )
        
        return {
            "success": True,
            "message": "Alternatives generated successfully",
            "data": alternatives
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting alternatives: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/{schedule_id}/optimize")
async def optimize_schedule(
    schedule_id: str,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
):
    """Optimize an existing schedule for better efficiency"""
    try:
        # Verify user authentication
        user = await verify_token(credentials.credentials)
        
        # Optimize schedule
        optimization_result = await schedule_service.optimize_schedule(
            schedule_id=schedule_id,
            db=db
        )
        
        return {
            "success": True,
            "message": "Schedule optimization completed",
            "data": optimization_result
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error optimizing schedule: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

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