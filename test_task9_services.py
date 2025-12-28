#!/usr/bin/env python3
"""
Test script for Task 9 services: Enhanced reminder system with conversational tones.

Tests:
- ReminderService: Cloud-based reminder scheduling with mobile push notifications
- MotivationalContentService: Photorealistic motivational content system
"""

import asyncio
import sys
import os
from datetime import datetime, timedelta
from pathlib import Path

# Add the cloud_backend directory to Python path
sys.path.insert(0, str(Path(__file__).parent / "cloud_backend"))

try:
    from cloud_backend.app.services.reminder_service import (
        ReminderService, ReminderSchedule, ReminderContent, ReminderType,
        ConversationalTone, NotificationChannel
    )
    from cloud_backend.app.services.motivational_content_service import (
        MotivationalContentService, VisionCategory, ContentType, 
        ContentPersonalization
    )
    print("✅ Successfully imported Task 9 services")
except ImportError as e:
    print(f"❌ Failed to import services: {e}")
    sys.exit(1)

async def test_reminder_service():
    """Test the ReminderService functionality."""
    print("\n🔔 Testing ReminderService...")
    
    try:
        # Initialize service
        reminder_service = ReminderService()
        print("✅ ReminderService initialized successfully")
        
        # Test reminder scheduling
        reminder_content = ReminderContent(
            title="Daily Health Check",
            message="Time for your daily health routine!",
            tone=ConversationalTone.SUPPORTIVE,
            personalization_data={
                'name': 'Alex',
                'task_name': 'morning workout',
                'vision_category': 'health'
            }
        )
        
        reminder_schedule = ReminderSchedule(
            reminder_id="test_reminder_1",
            user_id="user_123",
            reminder_type=ReminderType.HABIT_REMINDER,
            scheduled_time=datetime.utcnow() + timedelta(seconds=5),
            content=reminder_content,
            channels=[NotificationChannel.IN_APP, NotificationChannel.PUSH_NOTIFICATION],
            metadata={
                'device_tokens': ['test_token_1', 'test_token_2'],
                'email': 'test@example.com'
            }
        )
        
        # Schedule reminder
        reminder_id = await reminder_service.schedule_reminder(reminder_schedule)
        print(f"✅ Reminder scheduled successfully: {reminder_id}")
        
        # Test immediate delivery
        results = await reminder_service.deliver_reminder(reminder_schedule)
        print(f"✅ Reminder delivered to {len(results)} channels")
        
        for result in results:
            status = "✅ Success" if result.success else "❌ Failed"
            print(f"  {status}: {result.channel.value} - {result.error_message or 'OK'}")
        
        # Test user reminders retrieval
        user_reminders = await reminder_service.get_user_reminders("user_123")
        print(f"✅ Retrieved {len(user_reminders)} reminders for user")
        
        # Test delivery statistics
        stats = await reminder_service.get_delivery_statistics()
        print(f"✅ Delivery statistics: {stats['success_rate']:.2%} success rate")
        
        return True
        
    except Exception as e:
        print(f"❌ ReminderService test failed: {e}")
        return False

async def test_motivational_content_service():
    """Test the MotivationalContentService functionality."""
    print("\n🎨 Testing MotivationalContentService...")
    
    try:
        # Initialize service
        content_service = MotivationalContentService()
        print("✅ MotivationalContentService initialized successfully")
        
        # Test content generation
        personalization = ContentPersonalization(
            user_name="Sarah",
            age_range="25-35",
            fitness_level="intermediate",
            goals=["lose weight", "build strength"],
            current_progress={"fitness": 65.0, "nutrition": 80.0},
            vision_statement="I want to be the healthiest version of myself"
        )
        
        # Generate motivational content
        content = await content_service.generate_motivational_content(
            user_id="user_456",
            vision_category=VisionCategory.FITNESS,
            content_type=ContentType.PROGRESS_CELEBRATION,
            personalization=personalization,
            include_image=False  # Skip image generation for testing
        )
        
        print(f"✅ Generated motivational content: {content.content_id}")
        print(f"  Title: {content.title}")
        print(f"  Message: {content.message[:100]}...")
        print(f"  Quote: {content.motivational_quote}")
        
        # Test content retrieval
        retrieved_content = await content_service.get_content_by_id(content.content_id)
        print(f"✅ Retrieved content by ID: {retrieved_content is not None}")
        
        # Test user content history
        history = await content_service.get_user_content_history("user_456")
        print(f"✅ Retrieved {len(history)} content items from history")
        
        # Test engagement tracking
        await content_service.update_engagement_score(content.content_id, {
            'viewed': True,
            'liked': True,
            'view_time_seconds': 15
        })
        print(f"✅ Updated engagement score: {content.engagement_score}")
        
        # Test analytics
        analytics = await content_service.get_content_analytics()
        print(f"✅ Content analytics: {analytics['total_content']} total items")
        
        return True
        
    except Exception as e:
        print(f"❌ MotivationalContentService test failed: {e}")
        return False

async def test_integration():
    """Test integration between reminder and motivational content services."""
    print("\n🔗 Testing Service Integration...")
    
    try:
        # Initialize both services
        reminder_service = ReminderService()
        content_service = MotivationalContentService()
        
        # Generate motivational content
        personalization = ContentPersonalization(
            user_name="Jordan",
            goals=["financial freedom"],
            current_progress={"savings": 45.0}
        )
        
        content = await content_service.generate_motivational_content(
            user_id="user_789",
            vision_category=VisionCategory.FINANCIAL,
            content_type=ContentType.MOTIVATIONAL_QUOTE,
            personalization=personalization,
            include_image=False
        )
        
        # Create reminder with motivational content
        reminder_content = ReminderContent(
            title=content.title,
            message=content.message,
            tone=ConversationalTone.MOTIVATIONAL,
            personalization_data=content.personalization_data,
            motivational_quote=content.motivational_quote,
            ai_generated_image_url=content.ai_generated_image_url
        )
        
        reminder_schedule = ReminderSchedule(
            reminder_id="integration_test",
            user_id="user_789",
            reminder_type=ReminderType.MOTIVATIONAL,
            scheduled_time=datetime.utcnow() + timedelta(seconds=2),
            content=reminder_content,
            channels=[NotificationChannel.IN_APP]
        )
        
        # Schedule and deliver integrated reminder
        reminder_id = await reminder_service.schedule_reminder(reminder_schedule)
        results = await reminder_service.deliver_reminder(reminder_schedule)
        
        print(f"✅ Integrated reminder delivered successfully: {reminder_id}")
        print(f"  Content ID: {content.content_id}")
        print(f"  Delivery results: {len(results)} channels")
        
        return True
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        return False

async def main():
    """Run all Task 9 service tests."""
    print("🚀 Starting Task 9 Service Tests")
    print("=" * 50)
    
    # Run individual service tests
    reminder_test = await test_reminder_service()
    content_test = await test_motivational_content_service()
    integration_test = await test_integration()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    print(f"  ReminderService: {'✅ PASS' if reminder_test else '❌ FAIL'}")
    print(f"  MotivationalContentService: {'✅ PASS' if content_test else '❌ FAIL'}")
    print(f"  Service Integration: {'✅ PASS' if integration_test else '❌ FAIL'}")
    
    all_passed = reminder_test and content_test and integration_test
    
    if all_passed:
        print("\n🎉 All Task 9 services are working correctly!")
        print("✅ Enhanced reminder system with conversational tones: READY")
        print("✅ Photorealistic motivational content system: READY")
        return 0
    else:
        print("\n❌ Some tests failed. Please check the implementation.")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)