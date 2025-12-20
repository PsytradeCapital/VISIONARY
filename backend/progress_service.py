from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from models import Vision, VisionMetric, ScheduleBlock, UserFeedback
import uuid
import logging

logger = logging.getLogger(__name__)

class ProgressTrackingService:
    """Service for tracking and calculating progress toward user visions"""
    
    def __init__(self):
        pass
    
    async def calculate_vision_progress(self, user_id: str, vision_id: str, db: AsyncSession) -> Dict[str, Any]:
        """Calculate progress for a specific vision"""
        try:
            # Get vision and its metrics
            vision_query = select(Vision).where(Vision.id == uuid.UUID(vision_id), Vision.user_id == uuid.UUID(user_id))
            vision_result = await db.execute(vision_query)
            vision = vision_result.scalar_one_or_none()
            
            if not vision:
                return {"error": "Vision not found"}
            
            # Get vision metrics
            metrics_query = select(VisionMetric).where(VisionMetric.vision_id == uuid.UUID(vision_id))
            metrics_result = await db.execute(metrics_query)
            metrics = metrics_result.scalars().all()
            
            # Calculate completion percentage
            total_progress = 0.0
            metric_count = len(metrics)
            
            if metric_count > 0:
                for metric in metrics:
                    if metric.target_value and metric.target_value > 0:
                        progress = min(100, (metric.current_value / metric.target_value) * 100)
                        total_progress += progress
                
                total_progress = total_progress / metric_count
            
            # Get related completed schedule blocks
            completed_blocks_query = select(func.count(ScheduleBlock.id)).where(
                ScheduleBlock.related_vision_id == uuid.UUID(vision_id),
                ScheduleBlock.status == 'completed'
            )
            completed_blocks_result = await db.execute(completed_blocks_query)
            completed_blocks = completed_blocks_result.scalar() or 0
            
            return {
                "vision_id": vision_id,
                "title": vision.title,
                "category": vision.category,
                "progress_percentage": round(total_progress, 1),
                "completed_tasks": completed_blocks,
                "metrics": [
                    {
                        "name": metric.metric_name,
                        "current": metric.current_value,
                        "target": metric.target_value,
                        "unit": metric.unit,
                        "progress": round((metric.current_value / metric.target_value) * 100, 1) if metric.target_value else 0
                    }
                    for metric in metrics
                ],
                "status": vision.status
            }
            
        except Exception as e:
            logger.error(f"Error calculating vision progress: {str(e)}")
            return {"error": str(e)}
    
    async def get_user_progress_overview(self, user_id: str, db: AsyncSession) -> Dict[str, Any]:
        """Get overall progress overview for user"""
        try:
            # Get all user visions
            visions_query = select(Vision).where(Vision.user_id == uuid.UUID(user_id), Vision.status == 'active')
            visions_result = await db.execute(visions_query)
            visions = visions_result.scalars().all()
            
            progress_by_category = {}
            overall_progress = []
            
            for vision in visions:
                vision_progress = await self.calculate_vision_progress(user_id, str(vision.id), db)
                
                if "error" not in vision_progress:
                    overall_progress.append(vision_progress)
                    
                    # Group by category
                    category = vision.category
                    if category not in progress_by_category:
                        progress_by_category[category] = {
                            "total_visions": 0,
                            "average_progress": 0,
                            "completed_tasks": 0
                        }
                    
                    progress_by_category[category]["total_visions"] += 1
                    progress_by_category[category]["average_progress"] += vision_progress["progress_percentage"]
                    progress_by_category[category]["completed_tasks"] += vision_progress["completed_tasks"]
            
            # Calculate averages
            for category_data in progress_by_category.values():
                if category_data["total_visions"] > 0:
                    category_data["average_progress"] = round(
                        category_data["average_progress"] / category_data["total_visions"], 1
                    )
            
            # Get recent achievements
            recent_achievements = await self._get_recent_achievements(user_id, db)
            
            return {
                "overall_progress": overall_progress,
                "progress_by_category": progress_by_category,
                "recent_achievements": recent_achievements,
                "total_active_visions": len(visions)
            }
            
        except Exception as e:
            logger.error(f"Error getting user progress overview: {str(e)}")
            return {"error": str(e)}
    
    async def update_vision_metric(self, user_id: str, vision_id: str, metric_name: str, new_value: float, db: AsyncSession) -> bool:
        """Update a vision metric value"""
        try:
            # Find the metric
            metric_query = select(VisionMetric).where(
                VisionMetric.vision_id == uuid.UUID(vision_id),
                VisionMetric.metric_name == metric_name
            )
            metric_result = await db.execute(metric_query)
            metric = metric_result.scalar_one_or_none()
            
            if metric:
                old_value = metric.current_value
                metric.current_value = new_value
                metric.updated_at = datetime.utcnow()
                
                await db.commit()
                
                # Check if this is a milestone achievement
                if metric.target_value and new_value >= metric.target_value and old_value < metric.target_value:
                    await self._record_achievement(user_id, vision_id, f"Reached target for {metric_name}", db)
                
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error updating vision metric: {str(e)}")
            return False
    
    async def _get_recent_achievements(self, user_id: str, db: AsyncSession, days: int = 7) -> List[Dict[str, Any]]:
        """Get recent achievements for the user"""
        try:
            # Get completed schedule blocks from last week
            since_date = datetime.utcnow() - timedelta(days=days)
            
            completed_query = select(ScheduleBlock).where(
                ScheduleBlock.status == 'completed',
                ScheduleBlock.updated_at >= since_date
            ).join(
                # Join with schedules to get user_id
                # This is a simplified version - in real implementation, we'd need proper joins
            ).limit(10)
            
            # For now, return sample achievements
            achievements = [
                {
                    "title": "Completed 7-day workout streak",
                    "category": "health",
                    "date": datetime.utcnow() - timedelta(days=1),
                    "icon": "🎉"
                },
                {
                    "title": "Exceeded savings goal for 2 consecutive weeks",
                    "category": "financial",
                    "date": datetime.utcnow() - timedelta(days=3),
                    "icon": "💰"
                },
                {
                    "title": "Maintained daily meditation practice for 14 days",
                    "category": "psychological",
                    "date": datetime.utcnow() - timedelta(days=5),
                    "icon": "🧘"
                }
            ]
            
            return achievements
            
        except Exception as e:
            logger.error(f"Error getting recent achievements: {str(e)}")
            return []
    
    async def _record_achievement(self, user_id: str, vision_id: str, description: str, db: AsyncSession):
        """Record a new achievement"""
        try:
            # In a real implementation, we'd have an achievements table
            # For now, we'll log it
            logger.info(f"Achievement recorded for user {user_id}: {description}")
            
        except Exception as e:
            logger.error(f"Error recording achievement: {str(e)}")
    
    async def generate_progress_report(self, user_id: str, period: str, db: AsyncSession) -> Dict[str, Any]:
        """Generate a comprehensive progress report"""
        try:
            # Get progress overview
            overview = await self.get_user_progress_overview(user_id, db)
            
            # Calculate period-specific metrics
            if period == "weekly":
                period_days = 7
            elif period == "monthly":
                period_days = 30
            else:
                period_days = 7
            
            # Get achievements for the period
            achievements = await self._get_recent_achievements(user_id, db, period_days)
            
            # Generate insights and recommendations
            insights = self._generate_insights(overview)
            recommendations = self._generate_recommendations(overview)
            
            return {
                "period": period,
                "generated_at": datetime.utcnow(),
                "overview": overview,
                "achievements": achievements,
                "insights": insights,
                "recommendations": recommendations
            }
            
        except Exception as e:
            logger.error(f"Error generating progress report: {str(e)}")
            return {"error": str(e)}
    
    def _generate_insights(self, overview: Dict[str, Any]) -> List[str]:
        """Generate insights based on progress data"""
        insights = []
        
        progress_by_category = overview.get("progress_by_category", {})
        
        # Find best performing category
        best_category = None
        best_progress = 0
        
        for category, data in progress_by_category.items():
            if data["average_progress"] > best_progress:
                best_progress = data["average_progress"]
                best_category = category
        
        if best_category:
            insights.append(f"Your {best_category} goals are performing best with {best_progress}% average progress")
        
        # Find areas needing attention
        for category, data in progress_by_category.items():
            if data["average_progress"] < 50:
                insights.append(f"Your {category} goals may need more attention - currently at {data['average_progress']}%")
        
        return insights
    
    def _generate_recommendations(self, overview: Dict[str, Any]) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        progress_by_category = overview.get("progress_by_category", {})
        
        for category, data in progress_by_category.items():
            if data["average_progress"] < 30:
                recommendations.append(f"Consider breaking down your {category} goals into smaller, more manageable tasks")
            elif data["average_progress"] > 80:
                recommendations.append(f"Great progress on {category}! Consider setting more ambitious targets")
        
        if len(progress_by_category) < 3:
            recommendations.append("Consider adding goals in different life areas for a more balanced approach")
        
        return recommendations

# Global service instance
progress_service = ProgressTrackingService()