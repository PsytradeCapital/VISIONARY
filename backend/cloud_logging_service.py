"""
Cloud-based Logging Service for Visionary AI Personal Scheduler
Comprehensive error handling and cloud-based logging system
"""

import json
import logging
import asyncio
from typing import Dict, List, Any, Optional, Union
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum
import uuid
import traceback
import sys
from contextlib import asynccontextmanager

import aiohttp
import aiofiles
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_
from models import ErrorLog, PerformanceMetric, AuditLog
from database import get_db
from redis_client import redis_client

class LogLevel(Enum):
    """Log level enumeration"""
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

class ErrorCategory(Enum):
    """Error category enumeration"""
    SYSTEM = "system"
    USER_INPUT = "user_input"
    EXTERNAL_API = "external_api"
    DATABASE = "database"
    NETWORK = "network"
    SECURITY = "security"
    PERFORMANCE = "performance"
    INTEGRATION = "integration"

class LogDestination(Enum):
    """Log destination enumeration"""
    LOCAL_FILE = "local_file"
    CLOUD_STORAGE = "cloud_storage"
    DATABASE = "database"
    EXTERNAL_SERVICE = "external_service"
    REAL_TIME_STREAM = "real_time_stream"

@dataclass
class LogEntry:
    """Structured log entry"""
    id: str
    timestamp: datetime
    level: LogLevel
    service: str
    operation: str
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    message: str = ""
    details: Dict[str, Any] = None
    error_category: Optional[ErrorCategory] = None
    stack_trace: Optional[str] = None
    request_id: Optional[str] = None
    execution_time_ms: Optional[float] = None
    metadata: Dict[str, Any] = None

@dataclass
class ErrorContext:
    """Error context information"""
    service_name: str
    operation_name: str
    user_id: Optional[str] = None
    request_data: Optional[Dict[str, Any]] = None
    system_state: Optional[Dict[str, Any]] = None
    performance_metrics: Optional[Dict[str, Any]] = None

class CloudLoggingService:
    """
    Comprehensive cloud-based logging service with error handling,
    performance monitoring, and audit trails.
    """
    
    def __init__(self, 
                 cloud_provider: str = "aws",
                 log_level: LogLevel = LogLevel.INFO,
                 enable_cloud_sync: bool = True):
        self.cloud_provider = cloud_provider
        self.log_level = log_level
        self.enable_cloud_sync = enable_cloud_sync
        
        # Configure logging destinations
        self.log_destinations = [
            LogDestination.LOCAL_FILE,
            LogDestination.DATABASE,
            LogDestination.CLOUD_STORAGE
        ]
        
        # Error handling configuration
        self.error_handlers = {}
        self.circuit_breakers = {}
        self.retry_policies = {}
        
        # Performance monitoring
        self.performance_thresholds = {
            'response_time_ms': 5000,
            'memory_usage_mb': 1000,
            'cpu_usage_percentage': 80,
            'error_rate_percentage': 5
        }
        
        # Log aggregation and batching
        self.log_buffer = []
        self.buffer_size = 100
        self.flush_interval_seconds = 30
        
        # Initialize logging
        self._setup_logging()
        
        # Start background tasks
        asyncio.create_task(self._start_log_flushing())
        asyncio.create_task(self._start_performance_monitoring())
    
    def _setup_logging(self):
        """Setup logging configuration"""
        # Configure Python logging
        logging.basicConfig(
            level=getattr(logging, self.log_level.value.upper()),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/visionary.log'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        
        self.logger = logging.getLogger(__name__)
    
    async def log(self, 
                  level: LogLevel,
                  service: str,
                  operation: str,
                  message: str,
                  user_id: Optional[str] = None,
                  details: Optional[Dict[str, Any]] = None,
                  error_category: Optional[ErrorCategory] = None,
                  execution_time_ms: Optional[float] = None,
                  request_id: Optional[str] = None) -> str:
        """
        Log an entry with comprehensive context
        
        Returns:
            Log entry ID for tracking
        """
        log_id = str(uuid.uuid4())
        
        log_entry = LogEntry(
            id=log_id,
            timestamp=datetime.utcnow(),
            level=level,
            service=service,
            operation=operation,
            user_id=user_id,
            message=message,
            details=details or {},
            error_category=error_category,
            execution_time_ms=execution_time_ms,
            request_id=request_id,
            metadata={
                'cloud_provider': self.cloud_provider,
                'log_destinations': [dest.value for dest in self.log_destinations]
            }
        )
        
        # Add to buffer for batch processing
        self.log_buffer.append(log_entry)
        
        # Immediate processing for critical errors
        if level in [LogLevel.ERROR, LogLevel.CRITICAL]:
            await self._process_critical_log(log_entry)
        
        # Flush buffer if it's full
        if len(self.log_buffer) >= self.buffer_size:
            await self._flush_logs()
        
        return log_id
    
    async def log_error(self,
                       service: str,
                       operation: str,
                       error: Exception,
                       context: ErrorContext,
                       user_id: Optional[str] = None) -> str:
        """
        Log an error with full context and stack trace
        
        Returns:
            Error log ID for tracking
        """
        error_id = str(uuid.uuid4())
        
        # Extract stack trace
        stack_trace = traceback.format_exc()
        
        # Determine error category
        error_category = self._categorize_error(error, context)
        
        # Create detailed error information
        error_details = {
            'error_type': type(error).__name__,
            'error_message': str(error),
            'service_name': context.service_name,
            'operation_name': context.operation_name,
            'request_data': context.request_data,
            'system_state': context.system_state,
            'performance_metrics': context.performance_metrics
        }
        
        log_entry = LogEntry(
            id=error_id,
            timestamp=datetime.utcnow(),
            level=LogLevel.ERROR,
            service=service,
            operation=operation,
            user_id=user_id,
            message=f"Error in {service}.{operation}: {str(error)}",
            details=error_details,
            error_category=error_category,
            stack_trace=stack_trace,
            metadata={
                'error_id': error_id,
                'requires_immediate_attention': error_category in [ErrorCategory.SECURITY, ErrorCategory.SYSTEM]
            }
        )
        
        # Immediate processing for errors
        await self._process_critical_log(log_entry)
        
        # Store in database
        await self._store_error_in_database(log_entry, error)
        
        # Trigger error handling workflow
        await self._trigger_error_handling(error, context, error_id)
        
        return error_id
    
    async def log_performance_metric(self,
                                   service: str,
                                   operation: str,
                                   metric_name: str,
                                   metric_value: float,
                                   threshold: Optional[float] = None,
                                   user_id: Optional[str] = None) -> str:
        """
        Log a performance metric with threshold checking
        
        Returns:
            Metric log ID
        """
        metric_id = str(uuid.uuid4())
        
        # Check if metric exceeds threshold
        threshold_exceeded = False
        if threshold and metric_value > threshold:
            threshold_exceeded = True
        
        # Check against default thresholds
        default_threshold = self.performance_thresholds.get(metric_name)
        if default_threshold and metric_value > default_threshold:
            threshold_exceeded = True
        
        log_level = LogLevel.WARNING if threshold_exceeded else LogLevel.INFO
        
        metric_details = {
            'metric_name': metric_name,
            'metric_value': metric_value,
            'threshold': threshold or default_threshold,
            'threshold_exceeded': threshold_exceeded,
            'measurement_time': datetime.utcnow().isoformat()
        }
        
        await self.log(
            level=log_level,
            service=service,
            operation=operation,
            message=f"Performance metric {metric_name}: {metric_value}",
            user_id=user_id,
            details=metric_details,
            request_id=metric_id
        )
        
        # Store performance metric in database
        await self._store_performance_metric(service, operation, metric_name, metric_value, user_id)
        
        return metric_id
    
    async def log_audit_event(self,
                             service: str,
                             operation: str,
                             user_id: str,
                             action: str,
                             resource: str,
                             result: str,
                             details: Optional[Dict[str, Any]] = None) -> str:
        """
        Log an audit event for security and compliance
        
        Returns:
            Audit log ID
        """
        audit_id = str(uuid.uuid4())
        
        audit_details = {
            'action': action,
            'resource': resource,
            'result': result,
            'ip_address': details.get('ip_address') if details else None,
            'user_agent': details.get('user_agent') if details else None,
            'additional_details': details or {}
        }
        
        await self.log(
            level=LogLevel.INFO,
            service=service,
            operation=operation,
            message=f"Audit: {action} on {resource} by user {user_id} - {result}",
            user_id=user_id,
            details=audit_details,
            request_id=audit_id
        )
        
        # Store audit log in database
        await self._store_audit_log(service, operation, user_id, action, resource, result, details)
        
        return audit_id
    
    @asynccontextmanager
    async def operation_context(self,
                               service: str,
                               operation: str,
                               user_id: Optional[str] = None,
                               request_data: Optional[Dict[str, Any]] = None):
        """
        Context manager for operation logging with automatic error handling
        """
        operation_id = str(uuid.uuid4())
        start_time = datetime.utcnow()
        
        # Log operation start
        await self.log(
            level=LogLevel.INFO,
            service=service,
            operation=operation,
            message=f"Starting operation: {operation}",
            user_id=user_id,
            details={'operation_id': operation_id, 'request_data': request_data},
            request_id=operation_id
        )
        
        try:
            yield operation_id
            
            # Log successful completion
            execution_time = (datetime.utcnow() - start_time).total_seconds() * 1000
            
            await self.log(
                level=LogLevel.INFO,
                service=service,
                operation=operation,
                message=f"Operation completed successfully: {operation}",
                user_id=user_id,
                details={'operation_id': operation_id, 'success': True},
                execution_time_ms=execution_time,
                request_id=operation_id
            )
            
            # Log performance metric
            await self.log_performance_metric(
                service=service,
                operation=operation,
                metric_name='execution_time_ms',
                metric_value=execution_time,
                user_id=user_id
            )
            
        except Exception as e:
            # Log error with full context
            execution_time = (datetime.utcnow() - start_time).total_seconds() * 1000
            
            context = ErrorContext(
                service_name=service,
                operation_name=operation,
                user_id=user_id,
                request_data=request_data,
                system_state={'operation_id': operation_id},
                performance_metrics={'execution_time_ms': execution_time}
            )
            
            await self.log_error(service, operation, e, context, user_id)
            
            # Re-raise the exception
            raise
    
    def _categorize_error(self, error: Exception, context: ErrorContext) -> ErrorCategory:
        """Categorize error based on type and context"""
        error_type = type(error).__name__
        
        # Database errors
        if 'database' in error_type.lower() or 'sql' in error_type.lower():
            return ErrorCategory.DATABASE
        
        # Network errors
        if 'connection' in error_type.lower() or 'timeout' in error_type.lower():
            return ErrorCategory.NETWORK
        
        # Security errors
        if 'auth' in error_type.lower() or 'permission' in error_type.lower():
            return ErrorCategory.SECURITY
        
        # External API errors
        if 'api' in context.service_name.lower() or 'external' in context.service_name.lower():
            return ErrorCategory.EXTERNAL_API
        
        # User input errors
        if 'validation' in error_type.lower() or 'value' in error_type.lower():
            return ErrorCategory.USER_INPUT
        
        # Default to system error
        return ErrorCategory.SYSTEM
    
    async def _process_critical_log(self, log_entry: LogEntry):
        """Process critical logs immediately"""
        try:
            # Send to all destinations immediately
            await asyncio.gather(
                self._write_to_local_file(log_entry),
                self._send_to_cloud_storage(log_entry),
                self._store_in_database(log_entry),
                return_exceptions=True
            )
            
            # Send real-time alerts for critical errors
            if log_entry.level == LogLevel.CRITICAL:
                await self._send_critical_alert(log_entry)
                
        except Exception as e:
            # Fallback logging to prevent logging failures from breaking the system
            self.logger.error(f"Failed to process critical log: {str(e)}")
    
    async def _flush_logs(self):
        """Flush log buffer to all destinations"""
        if not self.log_buffer:
            return
        
        try:
            # Process all logs in buffer
            tasks = []
            for log_entry in self.log_buffer:
                tasks.extend([
                    self._write_to_local_file(log_entry),
                    self._store_in_database(log_entry)
                ])
                
                if self.enable_cloud_sync:
                    tasks.append(self._send_to_cloud_storage(log_entry))
            
            # Execute all tasks
            await asyncio.gather(*tasks, return_exceptions=True)
            
            # Clear buffer
            self.log_buffer.clear()
            
        except Exception as e:
            self.logger.error(f"Failed to flush logs: {str(e)}")
    
    async def _write_to_local_file(self, log_entry: LogEntry):
        """Write log entry to local file"""
        try:
            log_line = json.dumps(asdict(log_entry), default=str) + "\n"
            
            async with aiofiles.open('logs/visionary_structured.log', 'a') as f:
                await f.write(log_line)
                
        except Exception as e:
            self.logger.error(f"Failed to write to local file: {str(e)}")
    
    async def _send_to_cloud_storage(self, log_entry: LogEntry):
        """Send log entry to cloud storage"""
        if not self.enable_cloud_sync:
            return
        
        try:
            # This would integrate with actual cloud storage services
            # For now, we'll simulate the process
            await asyncio.sleep(0.01)  # Simulate network delay
            
        except Exception as e:
            self.logger.error(f"Failed to send to cloud storage: {str(e)}")
    
    async def _store_in_database(self, log_entry: LogEntry):
        """Store log entry in database"""
        try:
            async with get_db() as db:
                # Create database record (simplified)
                # In a real implementation, this would use proper ORM models
                pass
                
        except Exception as e:
            self.logger.error(f"Failed to store in database: {str(e)}")
    
    async def _store_error_in_database(self, log_entry: LogEntry, error: Exception):
        """Store error details in database"""
        try:
            async with get_db() as db:
                error_log = ErrorLog(
                    id=log_entry.id,
                    user_id=log_entry.user_id,
                    service_name=log_entry.service,
                    operation_name=log_entry.operation,
                    error_type=type(error).__name__,
                    error_message=str(error),
                    stack_trace=log_entry.stack_trace,
                    error_category=log_entry.error_category.value if log_entry.error_category else None,
                    context_data=log_entry.details,
                    occurred_at=log_entry.timestamp,
                    resolved=False
                )
                
                db.add(error_log)
                await db.commit()
                
        except Exception as e:
            self.logger.error(f"Failed to store error in database: {str(e)}")
    
    async def _store_performance_metric(self, service: str, operation: str, 
                                      metric_name: str, metric_value: float, 
                                      user_id: Optional[str]):
        """Store performance metric in database"""
        try:
            async with get_db() as db:
                performance_metric = PerformanceMetric(
                    id=str(uuid.uuid4()),
                    user_id=user_id,
                    service_name=service,
                    operation_name=operation,
                    metric_name=metric_name,
                    metric_value=metric_value,
                    recorded_at=datetime.utcnow()
                )
                
                db.add(performance_metric)
                await db.commit()
                
        except Exception as e:
            self.logger.error(f"Failed to store performance metric: {str(e)}")
    
    async def _store_audit_log(self, service: str, operation: str, user_id: str,
                             action: str, resource: str, result: str,
                             details: Optional[Dict[str, Any]]):
        """Store audit log in database"""
        try:
            async with get_db() as db:
                audit_log = AuditLog(
                    id=str(uuid.uuid4()),
                    user_id=user_id,
                    service_name=service,
                    operation_name=operation,
                    action=action,
                    resource=resource,
                    result=result,
                    details=details or {},
                    occurred_at=datetime.utcnow()
                )
                
                db.add(audit_log)
                await db.commit()
                
        except Exception as e:
            self.logger.error(f"Failed to store audit log: {str(e)}")
    
    async def _send_critical_alert(self, log_entry: LogEntry):
        """Send critical alert notifications"""
        try:
            # This would integrate with alerting services like PagerDuty, Slack, etc.
            alert_message = f"CRITICAL ERROR in {log_entry.service}: {log_entry.message}"
            self.logger.critical(alert_message)
            
        except Exception as e:
            self.logger.error(f"Failed to send critical alert: {str(e)}")
    
    async def _trigger_error_handling(self, error: Exception, context: ErrorContext, error_id: str):
        """Trigger error handling workflows"""
        try:
            # Implement error handling strategies based on error type and context
            error_category = self._categorize_error(error, context)
            
            if error_category == ErrorCategory.SECURITY:
                await self._handle_security_error(error, context, error_id)
            elif error_category == ErrorCategory.DATABASE:
                await self._handle_database_error(error, context, error_id)
            elif error_category == ErrorCategory.EXTERNAL_API:
                await self._handle_external_api_error(error, context, error_id)
            
        except Exception as e:
            self.logger.error(f"Failed to trigger error handling: {str(e)}")
    
    async def _handle_security_error(self, error: Exception, context: ErrorContext, error_id: str):
        """Handle security-related errors"""
        # Implement security incident response
        pass
    
    async def _handle_database_error(self, error: Exception, context: ErrorContext, error_id: str):
        """Handle database-related errors"""
        # Implement database error recovery
        pass
    
    async def _handle_external_api_error(self, error: Exception, context: ErrorContext, error_id: str):
        """Handle external API errors"""
        # Implement API error handling and retry logic
        pass
    
    async def _start_log_flushing(self):
        """Background task for periodic log flushing"""
        while True:
            try:
                await asyncio.sleep(self.flush_interval_seconds)
                await self._flush_logs()
            except Exception as e:
                self.logger.error(f"Error in log flushing task: {str(e)}")
    
    async def _start_performance_monitoring(self):
        """Background task for performance monitoring"""
        while True:
            try:
                await asyncio.sleep(60)  # Monitor every minute
                await self._collect_system_metrics()
            except Exception as e:
                self.logger.error(f"Error in performance monitoring task: {str(e)}")
    
    async def _collect_system_metrics(self):
        """Collect system performance metrics"""
        try:
            # Collect system metrics (CPU, memory, etc.)
            # This would integrate with system monitoring tools
            
            # Log system health metrics
            await self.log_performance_metric(
                service="system",
                operation="health_check",
                metric_name="cpu_usage_percentage",
                metric_value=45.0  # Placeholder
            )
            
        except Exception as e:
            self.logger.error(f"Failed to collect system metrics: {str(e)}")
    
    async def log_integration_event(self,
                                  service: str,
                                  operation: str,
                                  event_type: str,
                                  event_data: Dict[str, Any],
                                  user_id: Optional[str] = None) -> str:
        """
        Log integration events for service coordination
        
        Returns:
            Integration event log ID
        """
        event_id = str(uuid.uuid4())
        
        await self.log(
            level=LogLevel.INFO,
            service=service,
            operation=operation,
            message=f"Integration event: {event_type}",
            user_id=user_id,
            details={
                'event_type': event_type,
                'event_data': event_data,
                'integration_timestamp': datetime.utcnow().isoformat()
            },
            request_id=event_id
        )
        
        return event_id
    
    async def log_validation_result(self,
                                  service: str,
                                  validation_type: str,
                                  validation_result: Dict[str, Any],
                                  user_id: Optional[str] = None) -> str:
        """
        Log validation results for quality assurance
        
        Returns:
            Validation log ID
        """
        validation_id = str(uuid.uuid4())
        
        log_level = LogLevel.INFO
        if not validation_result.get('success', True):
            log_level = LogLevel.WARNING
        
        await self.log(
            level=log_level,
            service=service,
            operation="validation",
            message=f"Validation completed: {validation_type}",
            user_id=user_id,
            details={
                'validation_type': validation_type,
                'validation_result': validation_result,
                'validation_timestamp': datetime.utcnow().isoformat()
            },
            request_id=validation_id
        )
        
        return validation_id
    
    async def get_system_metrics(self) -> Dict[str, Any]:
        """
        Get current system metrics and health status
        
        Returns:
            System metrics dictionary
        """
        try:
            # Collect current system metrics
            metrics = {
                'timestamp': datetime.utcnow().isoformat(),
                'log_buffer_size': len(self.log_buffer),
                'log_destinations': [dest.value for dest in self.log_destinations],
                'performance_thresholds': self.performance_thresholds,
                'cloud_sync_enabled': self.enable_cloud_sync,
                'log_level': self.log_level.value,
                'system_health': {
                    'logging_service_status': 'healthy',
                    'buffer_utilization': len(self.log_buffer) / self.buffer_size,
                    'error_handlers_count': len(self.error_handlers),
                    'circuit_breakers_count': len(self.circuit_breakers)
                }
            }
            
            # Log metrics collection
            await self.log(
                level=LogLevel.DEBUG,
                service="cloud_logging",
                operation="get_system_metrics",
                message="System metrics collected",
                details=metrics
            )
            
            return metrics
            
        except Exception as e:
            self.logger.error(f"Failed to get system metrics: {str(e)}")
            return {
                'error': str(e),
                'timestamp': datetime.utcnow().isoformat(),
                'status': 'error'
            }

# Global cloud logging service instance
cloud_logging = CloudLoggingService()