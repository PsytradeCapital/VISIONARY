from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.security import HTTPAuthorizationCredentials
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from auth import verify_token, security
from progress_service import progress_service
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/progress", tags=["progress"])

@router.get("/")
async def get_progress_root(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
):
    """Get progress - root endpoint"""
    return await get_progress_overview(credentials=credentials, db=db)

@router.get("/overview")
async def get_progress_overview(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
):
    """Get overall progress overview for the user"""
    try:
        user = await verify_token(credentials.credentials)
        user_id = user["id"]
        
        overview = await progress_service.get_user_progress_overview(user_id, db)
        
        return {
            "success": True,
            "data": overview
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_progress_overview: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/vision/{vision_id}")
async def get_vision_progress(
    vision_id: str,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
):
    """Get progress for a specific vision"""
    try:
        user = await verify_token(credentials.credentials)
        user_id = user["id"]
        
        progress = await progress_service.calculate_vision_progress(user_id, vision_id, db)
        
        if "error" in progress:
            raise HTTPException(status_code=404, detail=progress["error"])
        
        return {
            "success": True,
            "data": progress
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_vision_progress: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.put("/vision/{vision_id}/metric")
async def update_vision_metric(
    vision_id: str,
    metric_name: str = Query(...),
    new_value: float = Query(...),
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
):
    """Update a vision metric value"""
    try:
        user = await verify_token(credentials.credentials)
        user_id = user["id"]
        
        success = await progress_service.update_vision_metric(
            user_id, vision_id, metric_name, new_value, db
        )
        
        if not success:
            raise HTTPException(status_code=404, detail="Metric not found")
        
        return {
            "success": True,
            "message": "Metric updated successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in update_vision_metric: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/report")
async def generate_progress_report(
    period: str = Query("weekly", regex="^(weekly|monthly)$"),
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
):
    """Generate a comprehensive progress report"""
    try:
        user = await verify_token(credentials.credentials)
        user_id = user["id"]
        
        report = await progress_service.generate_progress_report(user_id, period, db)
        
        if "error" in report:
            raise HTTPException(status_code=500, detail=report["error"])
        
        return {
            "success": True,
            "data": report
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in generate_progress_report: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/achievements")
async def get_recent_achievements(
    days: int = Query(7, ge=1, le=30),
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
):
    """Get recent achievements for the user"""
    try:
        user = await verify_token(credentials.credentials)
        user_id = user["id"]
        
        # This would call a method to get achievements
        # For now, return sample data
        achievements = [
            {
                "title": "Completed 7-day workout streak",
                "category": "health",
                "date": "2024-12-19T10:00:00Z",
                "icon": "🎉"
            },
            {
                "title": "Exceeded savings goal for 2 consecutive weeks",
                "category": "financial", 
                "date": "2024-12-17T15:30:00Z",
                "icon": "💰"
            }
        ]
        
        return {
            "success": True,
            "data": achievements
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_recent_achievements: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")