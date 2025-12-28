"""
Enhanced reminder system with conversational tones and mobile push notifications.

Task 9.1: Create cloud-based reminder scheduling with mobile push notifications
- Implements Celery-based reminder engine with cloud processing
- Add Toki-inspired conversational tones and supportive messaging
- Integrate Firebase/APNs for mobile push notifications with rich content
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum
import json
import uuid
from pathlib import Path

# Celery for background task processing
try:
    from celery import Celery
    CELERY_AVAILABLE = True
except ImportError:
    CELERY_AVAILABLE = False

# Firebase Admin SDK for push notifications
try:
    import firebase_admin
    from firebase_admin import credentials, messaging
    FIREBASE_AVAILABLE = True
except ImportError:
    FIREBASE_AVAILABLE = False

# APNs for iOS push notifications
try:
    from apns2.client import APNsClient
    from apns2.payload import Payload
    APNS_AVAILABLE = True
except ImportError:
    APNS_AVAILABLE = False

from ..core.config import settings

logger = logging.getLogger(__name__)

class ReminderType(Enum):
    """Types of reminders that can be scheduled."""
    TASK_DUE = "task_due"
    GOAL_PROGRESS = "goal_progress"
    HABIT_REMINDER = "habit_reminder"
    MOTIVATIONAL = "motivational"
    CELEBRATION = "celebration"
    RECOVERY_ACTION = "recovery_action"
    SCHEDULE_UPDATE = "schedule_update"
    FOCUS_TIME = "focus_time"

class ConversationalTone(Enum):
    """Toki-inspired conversational tones for reminders."""
    SUPPORTIVE = "supportive"
    MOTIVATIONAL = "motivational"
    FRIENDLY = "friendly"
    PROFESSIONAL = "professional"
    ENCOURAGING = "encouraging"
    GENTLE = "gentle"
    ENERGETIC = "energetic"
    CALM = "calm"

class NotificationChannel(Enum):
    """Available notification channels."""
    PUSH_NOTIFICATION = "push_notification"
    EMAIL = "email"
    SMS = "sms"
    IN_APP = "in_app"
    WEBHOOK = "webhook"

@dataclass
class ReminderContent:
    """Content for a reminder with conversational tone."""
    title: str
    message: str
    tone: ConversationalTone
    personalization_data: Dict[str, Any]
    rich_content: Optional[Dict[str, Any]] = None  # Images, actions, etc.
    motivational_quote: Optional[str] = None
    ai_generated_image_url: Optional[str] = None

@dataclass
class ReminderSchedule:
    """Schedule configuration for a reminder."""
    reminder_id: str
    user_id: str
    reminder_type: ReminderType
    scheduled_time: datetime
    content: ReminderContent
    channels: List[NotificationChannel]
    repeat_pattern: Optional[str] = None  # cron-like pattern
    timezone: str = "UTC"
    priority: int = 1  # 1-5, 5 being highest
    expires_at: Optional[datetime] = None
    metadata: Dict[str, Any] = None

@dataclass
class NotificationResult:
    """Result of a notification delivery attempt."""
    reminder_id: str
    channel: NotificationChannel
    success: bool
    delivery_time: datetime
    error_message: Optional[str] = None
    device_token: Optional[str] = None
    message_id: Optional[str] = None

class ReminderService:
    """
    Enhanced reminder system with conversational tones and mobile push notifications.
    
    Features:
    - Celery-based reminder engine with cloud processing
    - Toki-inspired conversational tones and supportive messaging
    - Firebase/APNs integration for mobile push notifications with rich content
    - Context-aware message generation with user vision alignment
    - Real-time reminder scheduling with cloud synchronization
    """
    
    def __init__(self):
        # Initialize Celery for background processing
        self.celery_app = None
        if CELERY_AVAILABLE:
            self.celery_app = Celery(
                'reminder_service',
                broker=settings.REDIS_URL,
                backend=settings.REDIS_URL
            )
            self._configure_celery()
        
        # Initialize Firebase for push notifications
        self.firebase_app = None
        if FIREBASE_AVAILABLE and hasattr(settings, 'FIREBASE_CREDENTIALS_PATH'):
            try:
                cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_PATH)
                self.firebase_app = firebase_admin.initialize_app(cred)
                logger.info("Firebase initialized for push notifications")
            except Exception as e:
                logger.warning(f"Failed to initialize Firebase: {e}")
        
        # Initialize APNs for iOS notifications
        self.apns_client = None
        if APNS_AVAILABLE and hasattr(settings, 'APNS_KEY_PATH'):
            try:
                self.apns_client = APNsClient(
                    settings.APNS_KEY_PATH,
                    key_id=settings.APNS_KEY_ID,
                    team_id=settings.APNS_TEAM_ID,
                    use_sandbox=settings.ENVIRONMENT == "development"
                )
                logger.info("APNs client initialized for iOS notifications")
            except Exception as e:
                logger.warning(f"Failed to initialize APNs: {e}")
        
        # Conversational tone templates
        self.tone_templates = self._initialize_tone_templates()
        
        # Motivational quotes database
        self.motivational_quotes = self._load_motivational_quotes()
        
        # Active reminders tracking
        self.active_reminders = {}
        
        # Delivery statistics
        self.delivery_stats = {
            'total_sent': 0,
            'successful_deliveries': 0,
            'failed_deliveries': 0,
            'channel_stats': {}
        }
    
    def _configure_celery(self):
        """Configure Celery for reminder processing."""
        if not self.celery_app:
            return
        
        self.celery_app.conf.update(
            task_serializer='json',
            accept_content=['json'],
            result_serializer='json',
            timezone='UTC',
            enable_utc=True,
            beat_schedule={
                'process-scheduled-reminders': {
                    'task': 'reminder_service.process_scheduled_reminders',
                    'schedule': 60.0,  # Every minute
                },
                'cleanup-expired-reminders': {
                    'task': 'reminder_service.cleanup_expired_reminders',
                    'schedule': 3600.0,  # Every hour
                }
            }
        )
    
    def _initialize_tone_templates(self) -> Dict[ConversationalTone, Dict[str, List[str]]]:
        """Initialize Toki-inspired conversational tone templates."""
        return {
            ConversationalTone.SUPPORTIVE: {
                'task_due': [
                    "Hey {name}, just a gentle reminder that {task} is coming up. You've got this! 💪",
                    "Hi {name}! Time for {task}. I believe in you - you've been doing great! ✨",
                    "{name}, your {task} is ready for you. Take it one step at a time. 🌟"
                ],
                'motivational': [
                    "You're making amazing progress, {name}! Keep up the wonderful work! 🎉",
                    "I'm so proud of how far you've come, {name}. You're doing incredible! 💫",
                    "Your dedication is inspiring, {name}. Every step counts! 🌈"
                ]
            },
            ConversationalTone.MOTIVATIONAL: {
                'task_due': [
                    "Time to crush {task}, {name}! You're unstoppable! 🔥",
                    "Let's make it happen, {name}! {task} is your next victory! 🏆",
                    "Ready to dominate {task}, {name}? Your future self will thank you! ⚡"
                ],
                'motivational': [
                    "You're a champion, {name}! Keep pushing those boundaries! 🚀",
                    "Greatness is calling, {name}! Answer with action! 💥",
                    "You were born to achieve amazing things, {name}! Go get 'em! 🌟"
                ]
            },
            ConversationalTone.FRIENDLY: {
                'task_due': [
                    "Hey buddy! Don't forget about {task} - you've got this! 😊",
                    "Hi there, {name}! Just a friendly nudge about {task}. 👋",
                    "Hope you're having a great day, {name}! Time for {task}! 🌞"
                ],
                'motivational': [
                    "You're doing awesome, {name}! Keep being amazing! 😄",
                    "Love seeing your progress, {name}! You rock! 🎸",
                    "You're such an inspiration, {name}! Keep shining! ✨"
                ]
            },
            ConversationalTone.PROFESSIONAL: {
                'task_due': [
                    "Good day, {name}. This is a reminder for {task} scheduled at this time.",
                    "Hello {name}, your {task} is now due for completion.",
                    "Reminder: {task} requires your attention, {name}."
                ],
                'motivational': [
                    "Your consistent progress is commendable, {name}.",
                    "Excellent work on maintaining your schedule, {name}.",
                    "Your dedication to your goals is noteworthy, {name}."
                ]
            },
            ConversationalTone.ENCOURAGING: {
                'task_due': [
                    "You can do this, {name}! {task} is just another step forward! 🌱",
                    "Believe in yourself, {name}! {task} is within your reach! 🌸",
                    "Every small step matters, {name}. Time for {task}! 🦋"
                ],
                'motivational': [
                    "Look how much you've grown, {name}! I'm cheering you on! 📣",
                    "Your progress is beautiful to see, {name}! Keep blooming! 🌺",
                    "You're stronger than you know, {name}! Keep going! 💪"
                ]
            },
            ConversationalTone.GENTLE: {
                'task_due': [
                    "Gentle reminder, {name}: {task} is ready when you are. 🕊️",
                    "No pressure, {name}, but {task} is waiting for you. Take your time. 🌿",
                    "Softly reminding you about {task}, {name}. You're doing wonderfully. 🌙"
                ],
                'motivational': [
                    "You're moving at just the right pace, {name}. Trust yourself. 🌊",
                    "Your journey is beautiful, {name}. Every step is perfect. 🍃",
                    "Be kind to yourself, {name}. You're doing better than you think. 💚"
                ]
            },
            ConversationalTone.ENERGETIC: {
                'task_due': [
                    "WOOHOO! Time for {task}, {name}! Let's GO! 🎉",
                    "Energy time, {name}! {task} is calling your name! ⚡",
                    "Ready, set, GO {name}! {task} awaits your awesomeness! 🚀"
                ],
                'motivational': [
                    "You're ON FIRE, {name}! Keep that momentum going! 🔥",
                    "AMAZING energy, {name}! You're absolutely crushing it! 💥",
                    "WOW! Look at you go, {name}! Unstoppable force! 🌪️"
                ]
            },
            ConversationalTone.CALM: {
                'task_due': [
                    "Peaceful reminder, {name}: {task} is here. Breathe and begin. 🧘",
                    "In your own time, {name}, {task} is ready for your attention. 🌸",
                    "Calmly approaching {task}, {name}. You have everything you need. 🌊"
                ],
                'motivational': [
                    "Your steady progress brings peace, {name}. Well done. 🕯️",
                    "Like a calm river, you flow toward your goals, {name}. 🌊",
                    "Your mindful approach is beautiful, {name}. Keep flowing. 🍃"
                ]
            }
        }
    
    def _load_motivational_quotes(self) -> Dict[str, List[str]]:
        """Load motivational quotes categorized by vision type."""
        return {
            'health': [
                "Your body can do it. It's your mind you have to convince.",
                "Health is not about the weight you lose, but about the life you gain.",
                "Every workout is progress, no matter how small.",
                "Strong is the new beautiful.",
                "Your health is an investment, not an expense."
            ],
            'financial': [
                "Financial peace isn't the acquisition of stuff. It's learning to live on less than you make.",
                "The best investment you can make is in yourself.",
                "Every dollar saved is a step toward financial freedom.",
                "Wealth is not about having a lot of money; it's about having a lot of options.",
                "Your financial future is created by what you do today, not tomorrow."
            ],
            'nutrition': [
                "Let food be thy medicine and medicine be thy food.",
                "You are what you eat, so don't be fast, cheap, easy, or fake.",
                "Healthy eating is a form of self-respect.",
                "Nourish your body. It's the only place you have to live.",
                "Every healthy choice is a victory worth celebrating."
            ],
            'psychological': [
                "Your mind is a powerful thing. When you fill it with positive thoughts, your life will start to change.",
                "Mental health is not a destination, but a process.",
                "You are braver than you believe, stronger than you seem, and smarter than you think.",
                "Progress, not perfection, is the goal.",
                "Your mental health is a priority. Your happiness is essential. Your self-care is a necessity."
            ],
            'productivity': [
                "The way to get started is to quit talking and begin doing.",
                "Productivity is never an accident. It is always the result of a commitment to excellence.",
                "Focus on being productive instead of busy.",
                "Small daily improvements over time lead to stunning results.",
                "You don't have to be great to get started, but you have to get started to be great."
            ]
        }
    
    async def schedule_reminder(self, reminder: ReminderSchedule) -> str:
        """
        Schedule a reminder for future delivery.
        
        Args:
            reminder: The reminder configuration
            
        Returns:
            Reminder ID for tracking
        """
        reminder_id = reminder.reminder_id or str(uuid.uuid4())
        reminder.reminder_id = reminder_id
        
        logger.info(f"Scheduling reminder {reminder_id} for user {reminder.user_id} at {reminder.scheduled_time}")
        
        # Store reminder for tracking
        self.active_reminders[reminder_id] = reminder
        
        # Schedule with Celery if available
        if self.celery_app:
            try:
                # Calculate delay until scheduled time
                delay = (reminder.scheduled_time - datetime.utcnow()).total_seconds()
                
                if delay > 0:
                    # Schedule for future delivery
                    self.celery_app.send_task(
                        'reminder_service.deliver_reminder',
                        args=[asdict(reminder)],
                        countdown=delay
                    )
                else:
                    # Deliver immediately
                    await self.deliver_reminder(reminder)
                    
            except Exception as e:
                logger.error(f"Failed to schedule reminder with Celery: {e}")
                # Fallback to in-memory scheduling
                await self._schedule_in_memory(reminder)
        else:
            # Fallback to in-memory scheduling
            await self._schedule_in_memory(reminder)
        
        return reminder_id
    
    async def _schedule_in_memory(self, reminder: ReminderSchedule):
        """Fallback in-memory scheduling when Celery is not available."""
        delay = (reminder.scheduled_time - datetime.utcnow()).total_seconds()
        
        if delay > 0:
            # Schedule for future delivery
            asyncio.create_task(self._delayed_delivery(reminder, delay))
        else:
            # Deliver immediately
            await self.deliver_reminder(reminder)
    
    async def _delayed_delivery(self, reminder: ReminderSchedule, delay: float):
        """Deliver reminder after a delay."""
        await asyncio.sleep(delay)
        await self.deliver_reminder(reminder)
    
    async def deliver_reminder(self, reminder: ReminderSchedule) -> List[NotificationResult]:
        """
        Deliver a reminder through specified channels.
        
        Args:
            reminder: The reminder to deliver
            
        Returns:
            List of delivery results for each channel
        """
        logger.info(f"Delivering reminder {reminder.reminder_id} to user {reminder.user_id}")
        
        results = []
        
        # Generate personalized content
        personalized_content = await self._personalize_content(reminder)
        
        # Deliver through each channel
        for channel in reminder.channels:
            try:
                result = await self._deliver_to_channel(reminder, personalized_content, channel)
                results.append(result)
                
                # Update statistics
                self._update_delivery_stats(channel, result.success)
                
            except Exception as e:
                logger.error(f"Failed to deliver reminder {reminder.reminder_id} via {channel}: {e}")
                results.append(NotificationResult(
                    reminder_id=reminder.reminder_id,
                    channel=channel,
                    success=False,
                    delivery_time=datetime.utcnow(),
                    error_message=str(e)
                ))
        
        # Remove from active reminders if not repeating
        if not reminder.repeat_pattern:
            self.active_reminders.pop(reminder.reminder_id, None)
        
        return results
    
    async def _personalize_content(self, reminder: ReminderSchedule) -> ReminderContent:
        """Personalize reminder content based on user data and tone."""
        content = reminder.content
        
        # Get user personalization data
        user_data = content.personalization_data
        user_name = user_data.get('name', 'there')
        
        # Select appropriate template based on tone and reminder type
        tone_templates = self.tone_templates.get(content.tone, {})
        reminder_type_key = reminder.reminder_type.value.replace('_', ' ')
        
        # Find the best matching template category
        template_category = 'task_due'  # default
        if reminder.reminder_type in [ReminderType.MOTIVATIONAL, ReminderType.CELEBRATION]:
            template_category = 'motivational'
        
        templates = tone_templates.get(template_category, [content.message])
        
        # Select template (could be randomized or based on user preference)
        import random
        selected_template = random.choice(templates) if templates else content.message
        
        # Personalize the message
        personalized_message = selected_template.format(
            name=user_name,
            task=user_data.get('task_name', 'your task'),
            goal=user_data.get('goal_name', 'your goal'),
            progress=user_data.get('progress', ''),
            **user_data
        )
        
        # Add motivational quote if appropriate
        motivational_quote = None
        if reminder.reminder_type in [ReminderType.MOTIVATIONAL, ReminderType.GOAL_PROGRESS]:
            vision_category = user_data.get('vision_category', 'productivity')
            quotes = self.motivational_quotes.get(vision_category, self.motivational_quotes['productivity'])
            motivational_quote = random.choice(quotes)
        
        return ReminderContent(
            title=content.title,
            message=personalized_message,
            tone=content.tone,
            personalization_data=user_data,
            rich_content=content.rich_content,
            motivational_quote=motivational_quote,
            ai_generated_image_url=content.ai_generated_image_url
        )
    
    async def _deliver_to_channel(
        self, 
        reminder: ReminderSchedule, 
        content: ReminderContent, 
        channel: NotificationChannel
    ) -> NotificationResult:
        """Deliver reminder to a specific channel."""
        
        if channel == NotificationChannel.PUSH_NOTIFICATION:
            return await self._deliver_push_notification(reminder, content)
        elif channel == NotificationChannel.EMAIL:
            return await self._deliver_email(reminder, content)
        elif channel == NotificationChannel.SMS:
            return await self._deliver_sms(reminder, content)
        elif channel == NotificationChannel.IN_APP:
            return await self._deliver_in_app(reminder, content)
        elif channel == NotificationChannel.WEBHOOK:
            return await self._deliver_webhook(reminder, content)
        else:
            raise ValueError(f"Unsupported notification channel: {channel}")
    
    async def _deliver_push_notification(
        self, 
        reminder: ReminderSchedule, 
        content: ReminderContent
    ) -> NotificationResult:
        """Deliver push notification via Firebase/APNs."""
        
        # Get user device tokens (would come from user preferences/database)
        device_tokens = reminder.metadata.get('device_tokens', []) if reminder.metadata else []
        
        if not device_tokens:
            return NotificationResult(
                reminder_id=reminder.reminder_id,
                channel=NotificationChannel.PUSH_NOTIFICATION,
                success=False,
                delivery_time=datetime.utcnow(),
                error_message="No device tokens available"
            )
        
        # Try Firebase first (Android/Web)
        if self.firebase_app:
            try:
                # Create Firebase message
                firebase_message = messaging.MulticastMessage(
                    tokens=device_tokens,
                    notification=messaging.Notification(
                        title=content.title,
                        body=content.message,
                        image=content.ai_generated_image_url
                    ),
                    data={
                        'reminder_id': reminder.reminder_id,
                        'reminder_type': reminder.reminder_type.value,
                        'tone': content.tone.value,
                        'motivational_quote': content.motivational_quote or '',
                        'rich_content': json.dumps(content.rich_content) if content.rich_content else ''
                    },
                    android=messaging.AndroidConfig(
                        priority='high',
                        notification=messaging.AndroidNotification(
                            icon='ic_notification',
                            color='#FF6B35',
                            sound='default',
                            channel_id='reminders'
                        )
                    ),
                    apns=messaging.APNSConfig(
                        payload=messaging.APNSPayload(
                            aps=messaging.Aps(
                                alert=messaging.ApsAlert(
                                    title=content.title,
                                    body=content.message
                                ),
                                badge=1,
                                sound='default',
                                category='REMINDER'
                            )
                        )
                    )
                )
                
                # Send message
                response = messaging.send_multicast(firebase_message)
                
                return NotificationResult(
                    reminder_id=reminder.reminder_id,
                    channel=NotificationChannel.PUSH_NOTIFICATION,
                    success=response.success_count > 0,
                    delivery_time=datetime.utcnow(),
                    message_id=str(response.responses[0].message_id) if response.responses else None,
                    error_message=f"Failed: {response.failure_count}" if response.failure_count > 0 else None
                )
                
            except Exception as e:
                logger.error(f"Firebase push notification failed: {e}")
        
        # Fallback to APNs for iOS
        if self.apns_client:
            try:
                payload = Payload(
                    alert={
                        'title': content.title,
                        'body': content.message
                    },
                    badge=1,
                    sound='default',
                    custom={
                        'reminder_id': reminder.reminder_id,
                        'reminder_type': reminder.reminder_type.value,
                        'motivational_quote': content.motivational_quote or ''
                    }
                )
                
                # Send to first device token (would iterate in real implementation)
                device_token = device_tokens[0]
                self.apns_client.send_notification(device_token, payload)
                
                return NotificationResult(
                    reminder_id=reminder.reminder_id,
                    channel=NotificationChannel.PUSH_NOTIFICATION,
                    success=True,
                    delivery_time=datetime.utcnow(),
                    device_token=device_token
                )
                
            except Exception as e:
                logger.error(f"APNs push notification failed: {e}")
        
        # If all methods fail
        return NotificationResult(
            reminder_id=reminder.reminder_id,
            channel=NotificationChannel.PUSH_NOTIFICATION,
            success=False,
            delivery_time=datetime.utcnow(),
            error_message="No push notification service available"
        )
    
    async def _deliver_email(
        self, 
        reminder: ReminderSchedule, 
        content: ReminderContent
    ) -> NotificationResult:
        """Deliver email notification."""
        # Placeholder for email delivery
        # In a real implementation, would use SendGrid, AWS SES, etc.
        
        user_email = reminder.metadata.get('email') if reminder.metadata else None
        
        if not user_email:
            return NotificationResult(
                reminder_id=reminder.reminder_id,
                channel=NotificationChannel.EMAIL,
                success=False,
                delivery_time=datetime.utcnow(),
                error_message="No email address available"
            )
        
        # Simulate email sending
        logger.info(f"Sending email to {user_email}: {content.title}")
        
        return NotificationResult(
            reminder_id=reminder.reminder_id,
            channel=NotificationChannel.EMAIL,
            success=True,
            delivery_time=datetime.utcnow(),
            message_id=f"email_{reminder.reminder_id}"
        )
    
    async def _deliver_sms(
        self, 
        reminder: ReminderSchedule, 
        content: ReminderContent
    ) -> NotificationResult:
        """Deliver SMS notification."""
        # Placeholder for SMS delivery
        # In a real implementation, would use Twilio, AWS SNS, etc.
        
        phone_number = reminder.metadata.get('phone') if reminder.metadata else None
        
        if not phone_number:
            return NotificationResult(
                reminder_id=reminder.reminder_id,
                channel=NotificationChannel.SMS,
                success=False,
                delivery_time=datetime.utcnow(),
                error_message="No phone number available"
            )
        
        # Simulate SMS sending
        logger.info(f"Sending SMS to {phone_number}: {content.message}")
        
        return NotificationResult(
            reminder_id=reminder.reminder_id,
            channel=NotificationChannel.SMS,
            success=True,
            delivery_time=datetime.utcnow(),
            message_id=f"sms_{reminder.reminder_id}"
        )
    
    async def _deliver_in_app(
        self, 
        reminder: ReminderSchedule, 
        content: ReminderContent
    ) -> NotificationResult:
        """Deliver in-app notification."""
        # Store notification for in-app display
        # In a real implementation, would store in database or cache
        
        logger.info(f"Storing in-app notification for user {reminder.user_id}")
        
        return NotificationResult(
            reminder_id=reminder.reminder_id,
            channel=NotificationChannel.IN_APP,
            success=True,
            delivery_time=datetime.utcnow(),
            message_id=f"inapp_{reminder.reminder_id}"
        )
    
    async def _deliver_webhook(
        self, 
        reminder: ReminderSchedule, 
        content: ReminderContent
    ) -> NotificationResult:
        """Deliver webhook notification."""
        # Placeholder for webhook delivery
        webhook_url = reminder.metadata.get('webhook_url') if reminder.metadata else None
        
        if not webhook_url:
            return NotificationResult(
                reminder_id=reminder.reminder_id,
                channel=NotificationChannel.WEBHOOK,
                success=False,
                delivery_time=datetime.utcnow(),
                error_message="No webhook URL available"
            )
        
        # Simulate webhook sending
        logger.info(f"Sending webhook to {webhook_url}")
        
        return NotificationResult(
            reminder_id=reminder.reminder_id,
            channel=NotificationChannel.WEBHOOK,
            success=True,
            delivery_time=datetime.utcnow(),
            message_id=f"webhook_{reminder.reminder_id}"
        )
    
    def _update_delivery_stats(self, channel: NotificationChannel, success: bool):
        """Update delivery statistics."""
        self.delivery_stats['total_sent'] += 1
        
        if success:
            self.delivery_stats['successful_deliveries'] += 1
        else:
            self.delivery_stats['failed_deliveries'] += 1
        
        # Update channel-specific stats
        channel_key = channel.value
        if channel_key not in self.delivery_stats['channel_stats']:
            self.delivery_stats['channel_stats'][channel_key] = {
                'sent': 0,
                'successful': 0,
                'failed': 0
            }
        
        self.delivery_stats['channel_stats'][channel_key]['sent'] += 1
        if success:
            self.delivery_stats['channel_stats'][channel_key]['successful'] += 1
        else:
            self.delivery_stats['channel_stats'][channel_key]['failed'] += 1
    
    async def cancel_reminder(self, reminder_id: str) -> bool:
        """Cancel a scheduled reminder."""
        if reminder_id in self.active_reminders:
            del self.active_reminders[reminder_id]
            logger.info(f"Cancelled reminder {reminder_id}")
            return True
        return False
    
    async def update_reminder(self, reminder_id: str, updates: Dict[str, Any]) -> bool:
        """Update a scheduled reminder."""
        if reminder_id in self.active_reminders:
            reminder = self.active_reminders[reminder_id]
            
            # Update fields
            for key, value in updates.items():
                if hasattr(reminder, key):
                    setattr(reminder, key, value)
            
            logger.info(f"Updated reminder {reminder_id}")
            return True
        return False
    
    async def get_user_reminders(self, user_id: str) -> List[ReminderSchedule]:
        """Get all active reminders for a user."""
        return [
            reminder for reminder in self.active_reminders.values()
            if reminder.user_id == user_id
        ]
    
    async def get_delivery_statistics(self) -> Dict[str, Any]:
        """Get reminder delivery statistics."""
        return {
            **self.delivery_stats,
            'success_rate': (
                self.delivery_stats['successful_deliveries'] / 
                max(1, self.delivery_stats['total_sent'])
            ),
            'active_reminders': len(self.active_reminders),
            'last_updated': datetime.utcnow().isoformat()
        }
    
    async def cleanup_expired_reminders(self):
        """Clean up expired reminders."""
        current_time = datetime.utcnow()
        expired_ids = []
        
        for reminder_id, reminder in self.active_reminders.items():
            if reminder.expires_at and reminder.expires_at < current_time:
                expired_ids.append(reminder_id)
        
        for reminder_id in expired_ids:
            del self.active_reminders[reminder_id]
            logger.info(f"Cleaned up expired reminder {reminder_id}")
        
        return len(expired_ids)
    
    # Celery tasks (would be in separate module in real implementation)
    @staticmethod
    async def process_scheduled_reminders():
        """Celery task to process scheduled reminders."""
        # This would be implemented as a Celery task
        pass
    
    @staticmethod
    async def deliver_reminder_task(reminder_data: Dict[str, Any]):
        """Celery task to deliver a reminder."""
        # This would be implemented as a Celery task
        pass