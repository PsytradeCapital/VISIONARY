from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from typing import List, Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from auth import verify_token, security
from reminder_service import reminder_service
from pydantic import BaseModel
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/reminders", tags=["reminders"])

@router.get("/")
async def get_reminders_root(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
):
    """Get reminders - root endpoint"""
    return await get_user_reminders(credentials=credentials, db=db)

class ReminderRequest(BaseModel):
    title: str
    message: Optional[str] = None
    reminder_time: datetime
    channels: List[str] = ['push']
    schedule_block_id: Optional[str] = None

class MotivationRequest(BaseModel):
    category: str
    activity_name: Optional[str] = None
    context: Dict[str, Any] = {}

class AchievementRequest(BaseModel):
    type: str  # 'streak', 'goal_completion', 'milestone'
    details: str
    days: Optional[int] = None
    goal_name: Optional[str] = None
    milestone: Optional[str] = None

class MissedGoalRequest(BaseModel):
    type: str
    category: str
    goal_name: str
    details: Dict[str, Any] = {}

@router.post("/schedule")
async def schedule_reminder(
    request: ReminderRequest,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
):
    """Schedule a new reminder"""
    try:
        # Verify user authentication
        user = await verify_token(credentials.credentials)
        user_id = user["id"]
        
        # Prepare reminder data
        reminder_data = {
            'user_id': user_id,
            'title': request.title,
            'message': request.message,
            'reminder_time': request.reminder_time,
            'channels': request.channels,
            'schedule_block_id': request.schedule_block_id
        }
        
        # Schedule the reminder
        reminder_id = await reminder_service.schedule_reminder(reminder_data, db)
        
        return {
            "success": True,
            "message": "Reminder scheduled successfully",
            "data": {
                "reminder_id": reminder_id,
                "scheduled_time": request.reminder_time.isoformat()
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error scheduling reminder: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/motivational")
async def send_motivational_message(
    request: MotivationRequest,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
):
    """Send a motivational message"""
    try:
        # Verify user authentication
        user = await verify_token(credentials.credentials)
        user_id = user["id"]
        
        # Prepare context
        context = request.context.copy()
        context['category'] = request.category
        if request.activity_name:
            context['activity_name'] = request.activity_name
        
        # Send motivational message
        await reminder_service.send_motivational_message(user_id, context, db)
        
        return {
            "success": True,
            "message": "Motivational message sent successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error sending motivational message: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/celebrate")
async def celebrate_achievement(
    request: AchievementRequest,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
):
    """Celebrate user achievement"""
    try:
        # Verify user authentication
        user = await verify_token(credentials.credentials)
        user_id = user["id"]
        
        # Prepare achievement data
        achievement = {
            'type': request.type,
            'details': request.details
        }
        
        if request.days:
            achievement['days'] = request.days
        if request.goal_name:
            achievement['goal_name'] = request.goal_name
        if request.milestone:
            achievement['milestone'] = request.milestone
        
        # Celebrate the achievement
        await reminder_service.celebrate_progress(user_id, achievement, db)
        
        return {
            "success": True,
            "message": "Achievement celebrated successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error celebrating achievement: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/recovery")
async def get_recovery_suggestions(
    request: MissedGoalRequest,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
):
    """Get recovery suggestions for missed goals"""
    try:
        # Verify user authentication
        user = await verify_token(credentials.credentials)
        user_id = user["id"]
        
        # Prepare missed goal data
        missed_goal = {
            'type': request.type,
            'category': request.category,
            'goal_name': request.goal_name,
            **request.details
        }
        
        # Get recovery suggestions
        suggestions = await reminder_service.suggest_recovery(user_id, missed_goal, db)
        
        return {
            "success": True,
            "message": "Recovery suggestions generated",
            "data": {
                "suggestions": suggestions,
                "total": len(suggestions)
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting recovery suggestions: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/user")
async def get_user_reminders(
    status: Optional[str] = None,
    limit: int = 50,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
):
    """Get user's reminders"""
    try:
        # Verify user authentication
        user = await verify_token(credentials.credentials)
        user_id = user["id"]
        
        # TODO: Implement database query to get user reminders
        # For now, return placeholder data
        
        return {
            "success": True,
            "data": {
                "reminders": [],
                "total": 0
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting user reminders: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.delete("/{reminder_id}")
async def cancel_reminder(
    reminder_id: str,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
):
    """Cancel a scheduled reminder"""
    try:
        # Verify user authentication
        user = await verify_token(credentials.credentials)
        
        # TODO: Implement reminder cancellation
        # For now, return success
        
        return {
            "success": True,
            "message": "Reminder cancelled successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error cancelling reminder: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")