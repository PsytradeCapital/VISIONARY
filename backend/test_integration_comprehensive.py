"""
Comprehensive Integration Test for Visionary AI Personal Scheduler
Tests the complete integration of all cloud services and mobile components
"""

import pytest
import asyncio
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any
from unittest.mock import Mock, AsyncMock, patch
import uuid

from integration_service import ComprehensiveIntegrationService, IntegrationMode, ServiceStatus
from cloud_logging_service import CloudLoggingService, LogLevel, ErrorCategory
from models import *
from database import get_db

class TestComprehensiveIntegration:
    """Test suite for comprehensive service integration"""
    
    @pytest.fixture
    async def integration_service(self):
        """Create integration service for testing"""
        service = ComprehensiveIntegrationService(IntegrationMode.DEVELOPMENT)
        return service
    
    @pytest.fixture
    async def mock_db_session(self):
        """Mock database session"""
        mock_session = AsyncMock()
        return mock_session
    
    @pytest.fixture
    def sample_user_data(self):
        """Sample user data for testing"""
        return {
            'user_id': str(uuid.uuid4()),
            'email': 'test@example.com',
            'preferences': {
                'schedule_format': 'weekly',
                'reminder_channels': ['push', 'email'],
                'theme': 'light'
            }
        }
    
    @pytest.fixture
    def sample_upload_data(self):
        """Sample upload data for testing"""
        return {
            'content': 'I want to exercise daily at 7 AM and save $500 per month for my vacation fund.',
            'category': 'mixed',
            'source': 'text_input'
        }
    
    @pytest.fixture
    def sample_vision_data(self):
        """Sample vision data for testing"""
        return {
            'title': 'Get Fit and Save Money',
            'category': 'health',
            'description': 'Improve fitness and build savings',
            'target_date': (datetime.now() + timedelta(days=90)).isoformat(),
            'metrics': [
                {'name': 'workout_days_per_week', 'target': 5, 'current': 0},
                {'name': 'monthly_savings', 'target': 500, 'current': 0}
            ]
        }
    
    @pytest.mark.asyncio
    async def test_system_initialization(self, integration_service):
        """Test complete system initialization"""
        # Test system initialization
        result = await integration_service.initialize_system()
        
        # Verify initialization success
        assert result.success == True
        assert result.operation == "system_initialization"
        assert 'database' in result.service_results
        assert 'redis' in result.service_results
        assert 'security' in result.service_results
        
        # Verify execution time is reasonable
        assert result.execution_time_ms > 0
        assert result.execution_time_ms < 30000  # Should complete within 30 seconds
        
        # Verify no critical errors
        critical_errors = [error for error in (result.errors or []) 
                          if 'critical' in error.lower()]
        assert len(critical_errors) == 0
    
    @pytest.mark.asyncio
    async def test_comprehensive_health_check(self, integration_service):
        """Test comprehensive health check of all services"""
        # Perform health check
        health_results = await integration_service.perform_comprehensive_health_check()
        
        # Verify all services are checked
        expected_services = [
            'ai_processing', 'upload_processing', 'schedule_generation',
            'reminder_system', 'progress_tracking', 'external_integrations',
            'security_service', 'websocket_service'
        ]
        
        for service in expected_services:
            assert service in health_results
            assert health_results[service].service_name == service
            assert health_results[service].last_check is not None
            assert health_results[service].response_time_ms >= 0
    
    @pytest.mark.asyncio
    async def test_upload_to_schedule_journey(self, integration_service, mock_db_session, 
                                            sample_user_data, sample_upload_data):
        """Test complete upload to schedule generation journey"""
        user_id = sample_user_data['user_id']
        
        journey_data = {
            'upload_data': sample_upload_data,
            'timeframe': 'weekly',
            'preferences': sample_user_data['preferences'],
            'context': {'mobile_optimized': True}
        }
        
        # Process the journey
        result = await integration_service.process_user_journey(
            user_id=user_id,
            journey_type="upload_to_schedule",
            journey_data=journey_data,
            db=mock_db_session
        )
        
        # Verify journey success
        assert result.success == True
        assert result.operation == "user_journey_upload_to_schedule"
        
        # Verify all steps completed
        journey_results = result.service_results
        expected_steps = ['upload', 'ai_analysis', 'suggestions', 'schedule', 'reminders', 'progress']
        
        for step in expected_steps:
            assert step in journey_results['steps']
        
        # Verify schedule was generated
        assert 'schedule' in journey_results['steps']
        schedule_result = journey_results['steps']['schedule']
        assert 'schedule_id' in schedule_result or 'blocks' in schedule_result
        
        # Verify reminders were set up
        assert 'reminders' in journey_results['steps']
        reminders_result = journey_results['steps']['reminders']
        assert 'scheduled_reminders' in reminders_result
    
    @pytest.mark.asyncio
    async def test_goal_to_progress_journey(self, integration_service, mock_db_session,
                                          sample_user_data, sample_vision_data):
        """Test goal setting to progress tracking journey"""
        user_id = sample_user_data['user_id']
        
        journey_data = {
            'vision_data': sample_vision_data,
            'timeframe': 'monthly',
            'preferences': sample_user_data['preferences']
        }
        
        # Process the journey
        result = await integration_service.process_user_journey(
            user_id=user_id,
            journey_type="goal_to_progress",
            journey_data=journey_data,
            db=mock_db_session
        )
        
        # Verify journey success
        assert result.success == True
        assert result.operation == "user_journey_goal_to_progress"
        
        # Verify vision creation
        journey_results = result.service_results
        assert 'vision_creation' in journey_results['steps']
        assert 'vision_id' in journey_results['steps']['vision_creation']
        
        # Verify schedule generation
        assert 'schedule' in journey_results['steps']
        
        # Verify progress tracking setup
        assert 'progress_setup' in journey_results['steps']
        
        # Verify motivational content
        assert 'motivation' in journey_results['steps']
        assert journey_results['steps']['motivation']['message_sent'] == True
    
    @pytest.mark.asyncio
    async def test_disruption_to_recovery_journey(self, integration_service, mock_db_session,
                                                sample_user_data):
        """Test disruption handling and autonomous recovery"""
        user_id = sample_user_data['user_id']
        
        journey_data = {
            'disruption': {
                'type': 'missed_goal',
                'category': 'health',
                'details': 'Missed morning workout due to oversleeping'
            },
            'schedule_id': str(uuid.uuid4())
        }
        
        # Process the journey
        result = await integration_service.process_user_journey(
            user_id=user_id,
            journey_type="disruption_to_recovery",
            journey_data=journey_data,
            db=mock_db_session
        )
        
        # Verify journey success
        assert result.success == True
        assert result.operation == "user_journey_disruption_to_recovery"
        
        # Verify disruption analysis
        journey_results = result.service_results
        assert 'disruption_analysis' in journey_results['steps']
        
        # Verify recovery suggestions
        assert 'recovery_suggestions' in journey_results['steps']
        
        # Verify autonomous rescheduling (if premium feature enabled)
        if integration_service.premium_features.get('autonomous_rescheduling'):
            assert 'autonomous_rescheduling' in journey_results['steps']
            rescheduling_result = journey_results['steps']['autonomous_rescheduling']
            assert 'optimization_score' in rescheduling_result
        
        # Verify notifications sent
        assert 'notifications' in journey_results['steps']
        assert journey_results['steps']['notifications']['recovery_message_sent'] == True
    
    @pytest.mark.asyncio
    async def test_mobile_sync_journey(self, integration_service, mock_db_session,
                                     sample_user_data):
        """Test mobile upload to cross-platform sync journey"""
        user_id = sample_user_data['user_id']
        
        journey_data = {
            'mobile_data': {
                'type': 'voice_input',
                'content': 'Schedule gym session for tomorrow at 6 PM',
                'device_type': 'mobile',
                'platform': 'ios'
            }
        }
        
        # Process the journey
        result = await integration_service.process_user_journey(
            user_id=user_id,
            journey_type="mobile_sync",
            journey_data=journey_data,
            db=mock_db_session
        )
        
        # Verify journey success
        assert result.success == True
        assert result.operation == "user_journey_mobile_sync"
        
        # Verify mobile upload processing
        journey_results = result.service_results
        assert 'mobile_upload' in journey_results['steps']
        mobile_result = journey_results['steps']['mobile_upload']
        assert mobile_result['mobile_optimized'] == True
        assert mobile_result['cloud_synced'] == True
        
        # Verify cloud sync
        assert 'cloud_sync' in journey_results['steps']
        sync_result = journey_results['steps']['cloud_sync']
        assert sync_result['cross_platform_available'] == True
        
        # Verify real-time updates
        assert 'real_time_updates' in journey_results['steps']
        assert journey_results['steps']['real_time_updates']['updates_sent'] == True
    
    @pytest.mark.asyncio
    async def test_system_status_monitoring(self, integration_service):
        """Test comprehensive system status monitoring"""
        # Get system status
        status = await integration_service.get_system_status()
        
        # Verify status structure
        assert 'system_health' in status
        assert 'service_health' in status
        assert 'performance_metrics' in status
        assert 'premium_features' in status
        assert 'integration_mode' in status
        
        # Verify system health metrics
        system_health = status['system_health']
        assert 'overall_percentage' in system_health
        assert 'healthy_services' in system_health
        assert 'total_services' in system_health
        assert 'status' in system_health
        
        # Verify performance metrics
        performance = status['performance_metrics']
        expected_metrics = [
            'request_count', 'error_count', 'average_response_time_ms',
            'memory_usage_mb', 'active_connections', 'uptime_hours'
        ]
        
        for metric in expected_metrics:
            assert metric in performance
            assert isinstance(performance[metric], (int, float))
        
        # Verify premium features
        premium_features = status['premium_features']
        expected_features = [
            'ai_visual_generation', 'advanced_analytics', 'multi_calendar_sync',
            'autonomous_rescheduling', 'focus_time_protection', 'photorealistic_imagery'
        ]
        
        for feature in expected_features:
            assert feature in premium_features
            assert isinstance(premium_features[feature], bool)
    
    @pytest.mark.asyncio
    async def test_error_handling_and_recovery(self, integration_service, mock_db_session):
        """Test error handling and recovery mechanisms"""
        user_id = str(uuid.uuid4())
        
        # Test with invalid journey data to trigger errors
        invalid_journey_data = {
            'invalid_field': 'invalid_value'
        }
        
        # Process journey that should fail gracefully
        result = await integration_service.process_user_journey(
            user_id=user_id,
            journey_type="invalid_journey_type",
            journey_data=invalid_journey_data,
            db=mock_db_session
        )
        
        # Verify graceful failure
        assert result.success == False
        assert result.operation == "user_journey_invalid_journey_type"
        assert len(result.errors) > 0
        
        # Verify error contains useful information
        error_message = result.errors[0]
        assert 'journey' in error_message.lower() or 'error' in error_message.lower()
    
    @pytest.mark.asyncio
    async def test_performance_monitoring(self, integration_service):
        """Test performance monitoring and metrics collection"""
        # Simulate some operations to generate metrics
        user_id = str(uuid.uuid4())
        
        # Perform multiple operations
        for i in range(5):
            journey_data = {
                'upload_data': {'content': f'Test content {i}'},
                'timeframe': 'daily'
            }
            
            result = await integration_service.process_user_journey(
                user_id=user_id,
                journey_type="upload_to_schedule",
                journey_data=journey_data,
                db=AsyncMock()
            )
            
            # Verify execution time is tracked
            assert result.execution_time_ms > 0
        
        # Get system status to check performance metrics
        status = await integration_service.get_system_status()
        performance_metrics = status['performance_metrics']
        
        # Verify metrics are being collected
        assert performance_metrics['request_count'] >= 0
        assert performance_metrics['average_response_time_ms'] >= 0
    
    @pytest.mark.asyncio
    async def test_premium_feature_validation(self, integration_service):
        """Test premium feature availability and validation"""
        # Verify premium features are properly configured
        premium_features = integration_service.premium_features
        
        # Test AI visual generation feature
        assert premium_features['ai_visual_generation'] == True
        assert premium_features['photorealistic_imagery'] == True
        
        # Test advanced scheduling features
        assert premium_features['autonomous_rescheduling'] == True
        assert premium_features['focus_time_protection'] == True
        assert premium_features['habit_defense'] == True
        
        # Test analytics features
        assert premium_features['advanced_analytics'] == True
        assert premium_features['premium_visual_analytics'] == True
        
        # Test integration features
        assert premium_features['multi_calendar_sync'] == True
    
    @pytest.mark.asyncio
    async def test_cloud_logging_integration(self, integration_service):
        """Test integration with cloud logging service"""
        from cloud_logging_service import cloud_logging
        
        # Test logging during operation
        user_id = str(uuid.uuid4())
        
        # Use logging context manager
        async with cloud_logging.operation_context(
            service="integration_test",
            operation="test_operation",
            user_id=user_id
        ) as operation_id:
            
            # Perform some operation
            await asyncio.sleep(0.1)
            
            # Log a performance metric
            await cloud_logging.log_performance_metric(
                service="integration_test",
                operation="test_operation",
                metric_name="test_metric",
                metric_value=100.0,
                user_id=user_id
            )
        
        # Verify operation completed without errors
        assert operation_id is not None
    
    @pytest.mark.asyncio
    async def test_concurrent_user_journeys(self, integration_service, mock_db_session):
        """Test handling multiple concurrent user journeys"""
        # Create multiple users
        user_ids = [str(uuid.uuid4()) for _ in range(3)]
        
        # Create concurrent journey tasks
        tasks = []
        for user_id in user_ids:
            journey_data = {
                'upload_data': {'content': f'User {user_id} goals and preferences'},
                'timeframe': 'weekly'
            }
            
            task = integration_service.process_user_journey(
                user_id=user_id,
                journey_type="upload_to_schedule",
                journey_data=journey_data,
                db=mock_db_session
            )
            tasks.append(task)
        
        # Execute all journeys concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Verify all journeys completed
        assert len(results) == 3
        
        # Verify no exceptions occurred
        for result in results:
            assert not isinstance(result, Exception)
            assert result.success == True
    
    @pytest.mark.asyncio
    async def test_service_circuit_breaker(self, integration_service):
        """Test circuit breaker functionality for service failures"""
        # This would test circuit breaker patterns for handling service failures
        # For now, we'll test that the system handles service unavailability gracefully
        
        # Simulate service failure by checking health
        health_results = await integration_service.perform_comprehensive_health_check()
        
        # Verify system continues to operate even if some services are unhealthy
        healthy_services = sum(1 for h in health_results.values() 
                             if h.status == ServiceStatus.HEALTHY)
        total_services = len(health_results)
        
        # System should be resilient to individual service failures
        assert total_services > 0
        
        # At least core services should be healthy in test environment
        core_services = ['ai_processing', 'upload_processing', 'schedule_generation']
        for service_name in core_services:
            if service_name in health_results:
                # In test environment, we expect these to be healthy or at least not critical failures
                assert health_results[service_name].status in [ServiceStatus.HEALTHY, ServiceStatus.DEGRADED]

if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v", "--asyncio-mode=auto"])