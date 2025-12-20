import asyncio
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from models import Reminder, ScheduleBlock
from database import Vision, UserProfile
from redis_client import redis_client
import logging
from enum import Enum
import random

logger = logging.getLogger(__name__)

class ReminderChannel(Enum):
    PUSH = "push"
    EMAIL = "email"
    SMS = "sms"

class ReminderService:
    """Service for managing reminders and motivational messaging"""
    
    def __init__(self):
        self.motivational_quotes = {
            'health': [
                "Your body can do it. It's your mind you need to convince.",
                "Take care of your body. It's the only place you have to live.",
                "A healthy outside starts from the inside.",
                "Health is not about the weight you lose, but about the life you gain.",
                "Every workout is progress, no matter how small."
            ],
            'financial': [
                "A budget is telling your money where to go instead of wondering where it went.",
                "It's not how much money you make, but how much money you keep.",
                "The best investment you can make is in yourself.",
                "Financial peace isn't the acquisition of stuff. It's learning to live on less than you make.",
                "Every dollar saved is a step toward financial freedom."
            ],
            'nutrition': [
                "Let food be thy medicine and medicine be thy food.",
                "You are what you eat, so don't be fast, cheap, easy, or fake.",
                "Healthy eating is a form of self-respect.",
                "Nourish your body. It's the only one you've got.",
                "Good nutrition is the foundation of a healthy life."
            ],
            'psychological': [
                "Peace comes from within. Do not seek it without.",
                "The mind is everything. What you think you become.",
                "Mindfulness is about being fully awake in our lives.",
                "You have been assigned this mountain to show others it can be moved.",
                "Mental health is not a destination, but a process."
            ],
            'task': [
                "The way to get started is to quit talking and begin doing.",
                "Success is the sum of small efforts repeated day in and day out.",
                "Focus on progress, not perfection.",
                "You don't have to be great to get started, but you have to get started to be great.",
                "Every accomplishment starts with the decision to try."
            ]
        }
        
        self.celebration_messages = [
            "🎉 Amazing work! You're crushing your goals!",
            "🌟 Fantastic progress! Keep up the momentum!",
            "🚀 You're on fire! Another milestone achieved!",
            "💪 Incredible dedication! You're inspiring!",
            "🏆 Outstanding achievement! You should be proud!",
            "✨ Brilliant work! You're making it happen!",
            "🎯 Perfect execution! You're hitting your targets!",
            "🌈 Wonderful progress! You're creating positive change!"
        ]
    
    async def schedule_reminder(self, reminder_data: Dict[str, Any], db: AsyncSession) -> str:
        """Schedule a new reminder"""
        try:
            # Create reminder record
            reminder = Reminder(
                user_id=reminder_data['user_id'],
                schedule_block_id=reminder_data.get('schedule_block_id'),
                title=reminder_data['title'],
                message=reminder_data.get('message', ''),
                reminder_time=reminder_data['reminder_time'],
                channels=reminder_data.get('channels', ['push']),
                status='pending'
            )
            
            db.add(reminder)
            await db.commit()
            
            # Schedule in Redis for processing
            await self._schedule_in_redis(str(reminder.id), reminder_data['reminder_time'])
            
            logger.info(f"Scheduled reminder {reminder.id} for {reminder_data['reminder_time']}")
            return str(reminder.id)
            
        except Exception as e:
            logger.error(f"Error scheduling reminder: {str(e)}")
            await db.rollback()
            raise
    
    async def send_motivational_message(self, user_id: str, context: Dict[str, Any], db: AsyncSession) -> None:
        """Send a motivational message based on context"""
        try:
            # Get user preferences
            user_profile = await self._get_user_profile(user_id, db)
            
            # Select appropriate motivational content
            category = context.get('category', 'task')
            quotes = self.motivational_quotes.get(category, self.motivational_quotes['task'])
            selected_quote = random.choice(quotes)
            
            # Create contextual message
            activity_name = context.get('activity_name', 'your activity')
            message = f"Time for {activity_name}! 💪\n\n{selected_quote}\n\nYou've got this!"
            
            # Send through preferred channels
            channels = user_profile.get('reminder_channels', ['push']) if user_profile else ['push']
            
            for channel in channels:
                await self._send_message(user_id, message, channel, context)
            
            logger.info(f"Sent motivational message to user {user_id}")
            
        except Exception as e:
            logger.error(f"Error sending motivational message: {str(e)}")
    
    async def celebrate_progress(self, user_id: str, achievement: Dict[str, Any], db: AsyncSession) -> None:
        """Celebrate user achievements and progress"""
        try:
            # Select celebration message
            celebration = random.choice(self.celebration_messages)
            
            # Create achievement-specific message
            achievement_type = achievement.get('type', 'general')
            achievement_details = achievement.get('details', '')
            
            if achievement_type == 'streak':
                days = achievement.get('days', 1)
                message = f"{celebration}\n\nYou've maintained a {days}-day streak! {achievement_details}"
            elif achievement_type == 'goal_completion':
                goal_name = achievement.get('goal_name', 'your goal')
                message = f"{celebration}\n\nYou completed '{goal_name}'! Time to celebrate your success!"
            elif achievement_type == 'milestone':
                milestone = achievement.get('milestone', 'milestone')
                message = f"{celebration}\n\nYou reached a major milestone: {milestone}!"
            else:
                message = f"{celebration}\n\n{achievement_details}"
            
            # Get user preferences and send celebration
            user_profile = await self._get_user_profile(user_id, db)
            channels = user_profile.get('reminder_channels', ['push']) if user_profile else ['push']
            
            for channel in channels:
                await self._send_message(user_id, message, channel, achievement)
            
            # Store achievement for progress tracking
            await self._store_achievement(user_id, achievement, db)
            
            logger.info(f"Celebrated achievement for user {user_id}: {achievement_type}")
            
        except Exception as e:
            logger.error(f"Error celebrating progress: {str(e)}")
    
    async def suggest_recovery(self, user_id: str, missed_goal: Dict[str, Any], db: AsyncSession) -> List[Dict[str, Any]]:
        """Suggest recovery actions for missed goals"""
        try:
            goal_type = missed_goal.get('type', 'general')
            category = missed_goal.get('category', 'task')
            
            recovery_suggestions = []
            
            if category == 'health':
                recovery_suggestions = [
                    {
                        'type': 'quick_alternative',
                        'title': '10-Minute Quick Workout',
                        'description': 'A short but effective workout to get back on track',
                        'duration': 10,
                        'difficulty': 'easy'
                    },
                    {
                        'type': 'schedule_adjustment',
                        'title': 'Reschedule for Tomorrow Morning',
                        'description': 'Move your workout to tomorrow morning when you have more energy',
                        'suggested_time': 'morning'
                    },
                    {
                        'type': 'habit_modification',
                        'title': 'Break It Down',
                        'description': 'Split your workout into smaller 15-minute sessions throughout the day',
                        'approach': 'micro_habits'
                    }
                ]
            
            elif category == 'financial':
                recovery_suggestions = [
                    {
                        'type': 'quick_action',
                        'title': '5-Minute Budget Check',
                        'description': 'Quickly review your expenses from today',
                        'duration': 5,
                        'difficulty': 'easy'
                    },
                    {
                        'type': 'goal_adjustment',
                        'title': 'Adjust This Week\'s Target',
                        'description': 'Slightly modify your weekly savings goal to stay on track',
                        'approach': 'flexible_goals'
                    }
                ]
            
            elif category == 'nutrition':
                recovery_suggestions = [
                    {
                        'type': 'immediate_action',
                        'title': 'Healthy Snack Now',
                        'description': 'Choose a nutritious snack to get back on your nutrition plan',
                        'duration': 2,
                        'difficulty': 'easy'
                    },
                    {
                        'type': 'next_meal_planning',
                        'title': 'Plan Your Next Meal',
                        'description': 'Focus on making your next meal extra healthy',
                        'approach': 'forward_focus'
                    }
                ]
            
            elif category == 'psychological':
                recovery_suggestions = [
                    {
                        'type': 'micro_session',
                        'title': '3-Minute Breathing Exercise',
                        'description': 'A quick mindfulness exercise to reset your day',
                        'duration': 3,
                        'difficulty': 'easy'
                    },
                    {
                        'type': 'self_compassion',
                        'title': 'Practice Self-Kindness',
                        'description': 'Remember that missing one session doesn\'t define your progress',
                        'approach': 'mindset_shift'
                    }
                ]
            
            # Add motivational message
            motivational_message = self._get_recovery_motivation(category)
            
            # Send recovery suggestions
            user_profile = await self._get_user_profile(user_id, db)
            channels = user_profile.get('reminder_channels', ['push']) if user_profile else ['push']
            
            message = f"Don't worry about missing your goal! Here's how to get back on track:\n\n{motivational_message}"
            
            for channel in channels:
                await self._send_message(user_id, message, channel, missed_goal)
            
            return recovery_suggestions
            
        except Exception as e:
            logger.error(f"Error suggesting recovery: {str(e)}")
            return []
    
    async def process_pending_reminders(self, db: AsyncSession) -> None:
        """Process all pending reminders that are due"""
        try:
            current_time = datetime.utcnow()
            
            # Get due reminders
            due_reminders_query = select(Reminder).where(
                and_(
                    Reminder.status == 'pending',
                    Reminder.reminder_time <= current_time
                )
            )
            
            result = await db.execute(due_reminders_query)
            due_reminders = result.scalars().all()
            
            for reminder in due_reminders:
                try:
                    await self._send_reminder(reminder, db)
                    reminder.status = 'sent'
                except Exception as e:
                    logger.error(f"Failed to send reminder {reminder.id}: {str(e)}")
                    reminder.status = 'failed'
            
            await db.commit()
            
            if due_reminders:
                logger.info(f"Processed {len(due_reminders)} reminders")
                
        except Exception as e:
            logger.error(f"Error processing pending reminders: {str(e)}")
    
    async def _schedule_in_redis(self, reminder_id: str, reminder_time: datetime) -> None:
        """Schedule reminder in Redis for processing"""
        try:
            # Calculate delay in seconds
            delay = (reminder_time - datetime.utcnow()).total_seconds()
            
            if delay > 0:
                # Store reminder ID with expiration
                await redis_client.set(
                    f"reminder:{reminder_id}",
                    json.dumps({
                        'reminder_id': reminder_id,
                        'scheduled_time': reminder_time.isoformat()
                    }),
                    expire=int(delay + 3600)  # Add 1 hour buffer
                )
                
                logger.debug(f"Scheduled reminder {reminder_id} in Redis with {delay} seconds delay")
            
        except Exception as e:
            logger.error(f"Error scheduling reminder in Redis: {str(e)}")
    
    async def _send_reminder(self, reminder: Reminder, db: AsyncSession) -> None:
        """Send a specific reminder"""
        try:
            # Get related schedule block for context
            context = {}
            if reminder.schedule_block_id:
                block_query = select(ScheduleBlock).where(ScheduleBlock.id == reminder.schedule_block_id)
                block_result = await db.execute(block_query)
                block = block_result.scalar_one_or_none()
                
                if block:
                    context = {
                        'activity_name': block.title,
                        'category': block.category,
                        'start_time': block.start_time,
                        'duration': (block.end_time - block.start_time).total_seconds() / 60
                    }
            
            # Enhance message with motivational content
            enhanced_message = await self._enhance_reminder_message(reminder, context)
            
            # Send through all specified channels
            for channel in reminder.channels:
                await self._send_message(str(reminder.user_id), enhanced_message, channel, context)
            
            logger.info(f"Sent reminder {reminder.id} to user {reminder.user_id}")
            
        except Exception as e:
            logger.error(f"Error sending reminder {reminder.id}: {str(e)}")
            raise
    
    async def _enhance_reminder_message(self, reminder: Reminder, context: Dict[str, Any]) -> str:
        """Enhance reminder message with motivational content"""
        base_message = reminder.message or reminder.title
        
        # Add motivational quote if context available
        if context.get('category'):
            category = context['category']
            quotes = self.motivational_quotes.get(category, [])
            if quotes:
                quote = random.choice(quotes)
                base_message += f"\n\n💡 {quote}"
        
        # Add time-sensitive encouragement
        if context.get('start_time'):
            start_time = context['start_time']
            time_str = start_time.strftime('%I:%M %p')
            base_message += f"\n\n⏰ Scheduled for {time_str}"
        
        # Add duration info
        if context.get('duration'):
            duration = int(context['duration'])
            base_message += f" ({duration} minutes)"
        
        return base_message
    
    async def _send_message(self, user_id: str, message: str, channel: str, context: Dict[str, Any]) -> None:
        """Send message through specified channel"""
        try:
            if channel == ReminderChannel.PUSH.value:
                await self._send_push_notification(user_id, message, context)
            elif channel == ReminderChannel.EMAIL.value:
                await self._send_email(user_id, message, context)
            elif channel == ReminderChannel.SMS.value:
                await self._send_sms(user_id, message, context)
            else:
                logger.warning(f"Unknown reminder channel: {channel}")
                
        except Exception as e:
            logger.error(f"Error sending message via {channel}: {str(e)}")
    
    async def _send_push_notification(self, user_id: str, message: str, context: Dict[str, Any]) -> None:
        """Send push notification (placeholder implementation)"""
        # TODO: Implement actual push notification service integration
        logger.info(f"PUSH notification to {user_id}: {message[:50]}...")
    
    async def _send_email(self, user_id: str, message: str, context: Dict[str, Any]) -> None:
        """Send email notification (placeholder implementation)"""
        # TODO: Implement actual email service integration
        logger.info(f"EMAIL to {user_id}: {message[:50]}...")
    
    async def _send_sms(self, user_id: str, message: str, context: Dict[str, Any]) -> None:
        """Send SMS notification (placeholder implementation)"""
        # TODO: Implement actual SMS service integration
        logger.info(f"SMS to {user_id}: {message[:50]}...")
    
    async def _get_user_profile(self, user_id: str, db: AsyncSession) -> Optional[Dict[str, Any]]:
        """Get user profile for preferences"""
        try:
            profile_query = select(UserProfile).where(UserProfile.user_id == user_id)
            result = await db.execute(profile_query)
            profile = result.scalar_one_or_none()
            
            if profile:
                return {
                    'reminder_channels': json.loads(profile.reminder_channels) if profile.reminder_channels else ['push'],
                    'timezone': profile.timezone,
                    'language': profile.language
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting user profile: {str(e)}")
            return None
    
    async def _store_achievement(self, user_id: str, achievement: Dict[str, Any], db: AsyncSession) -> None:
        """Store achievement for progress tracking"""
        try:
            # TODO: Implement achievement storage in database
            # For now, just log the achievement
            logger.info(f"Achievement stored for user {user_id}: {achievement}")
            
        except Exception as e:
            logger.error(f"Error storing achievement: {str(e)}")
    
    def _get_recovery_motivation(self, category: str) -> str:
        """Get motivational message for recovery"""
        recovery_messages = {
            'health': "Every fitness journey has ups and downs. What matters is getting back up! 💪",
            'financial': "Financial discipline is built one decision at a time. You're still on the right path! 💰",
            'nutrition': "One meal doesn't define your nutrition journey. Focus on your next healthy choice! 🥗",
            'psychological': "Self-care isn't selfish, it's essential. Be kind to yourself and try again! 🧘",
            'task': "Progress isn't always linear. Every step forward counts, no matter how small! 🎯"
        }
        
        return recovery_messages.get(category, "Remember, progress is a journey, not a destination. Keep going! ✨")

# Global reminder service instance
reminder_service = ReminderService()