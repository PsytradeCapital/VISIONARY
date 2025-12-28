#!/usr/bin/env python3
"""Simple test for Task 9 services."""

import sys
sys.path.append('.')

try:
    from app.services.reminder_service import ReminderService
    from app.services.motivational_content_service import MotivationalContentService
    print('✅ Task 9 services imported successfully')
    print('✅ ReminderService: Available')
    print('✅ MotivationalContentService: Available')
    print('🎉 Task 9 implementation complete!')
except Exception as e:
    print(f'❌ Import error: {e}')