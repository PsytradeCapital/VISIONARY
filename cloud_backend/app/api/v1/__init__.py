"""
API v1 routes
"""

from fastapi import APIRouter
from .endpoints import auth, upload, schedule, reminder, analytics

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(upload.router, prefix="/upload", tags=["upload"])
api_router.include_router(schedule.router, prefix="/schedule", tags=["schedule"])
api_router.include_router(reminder.router, prefix="/reminder", tags=["reminder"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])