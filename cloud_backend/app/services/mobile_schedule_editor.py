"""
Mobile-first schedule editing and real-time updates service.

Creates mobile-optimized APIs for schedule editing with touch-friendly interfaces,
implements real-time cloud synchronization for schedule modifications, and adds
alternative suggestion generation with cloud-based AI processing.
"""

import json
import logging
import asyncio
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum
import websockets
from .schedule_generator import (
    ScheduleGeneratorService, GeneratedSchedule, TimeBlock, TaskPriority,
    ConflictResolutionStrategy, ScheduleConflict
)

logger = logging.getLogger(__name__)


class EditAction(Enum):
    """Types of schedule edit actions."""
    MOVE_TASK = "move_task"
    RESIZE_TASK = "resize_task"
    DELETE_TASK = "delete_task"
    ADD_TASK = "add_task"
    SPLIT_TASK = "split_task"
    MERGE_TASKS = "merge_tasks"
    CHANGE_PRIORITY = "change_priority"
    ADD_BREAK = "add_break"


class TouchGesture(Enum):
    """Touch gestures for mobile editing."""
    TAP = "tap"
    LONG_PRESS = "long_press"
    DRAG = "drag"
    PINCH = "pinch"
    SWIPE_LEFT = "swipe_left"
    SWIPE_RIGHT = "swipe_right"
    DOUBLE_TAP = "double_tap"


class SyncStatus(Enum):
    """Real-time synchronization status."""
    SYNCED = "synced"
    SYNCING = "syncing"
    CONFLICT = "conflict"
    OFFLINE = "offline"
    ERROR = "error"


@dataclass
class MobileEditRequest:
    """Request for mobile schedule editing."""
    user_id: str
    schedule_id: str
    action: EditAction
    target_block_id: Optional[str]
    gesture: TouchGesture
    touch_coordinates: Tuple[float, float]  # x, y coordinates
    new_values: Dict[str, Any]
    timestamp: datetime
    device_info: Dict[str, Any]


@dataclass
class RealTimeUpdate:
    """Real-time update for schedule synchronization."""
    update_id: str
    user_id: str
    schedule_id: str
    action: EditAction
    affected_blocks: List[str]
    changes: Dict[str, Any]
    timestamp: datetime
    sync_status: SyncStatus
    conflict_resolution: Optional[Dict[str, Any]] = None


@dataclass
class AlternativeSuggestion:
    """Alternative suggestion for schedule modifications."""
    suggestion_id: str
    suggestion_type: str  # 'time_slot', 'task_split', 'priority_change', 'break_addition'
    description: str
    confidence: float
    impact_score: float
    implementation: Dict[str, Any]
    visual_preview: Optional[str] = None


@dataclass
class TouchFriendlyInterface:
    """Configuration for touch-friendly mobile interface."""
    min_touch_target_size: int = 44  # pixels
    gesture_sensitivity: float = 0.8
    haptic_feedback_enabled: bool = True
    visual_feedback_duration: int = 200  # milliseconds
    auto_scroll_enabled: bool = True
    zoom_levels: List[float] = None
    
    def __post_init__(self):
        if self.zoom_levels is None:
            self.zoom_levels = [0.5, 0.75, 1.0, 1.25, 1.5]


class MobileScheduleEditorService:
    """
    Mobile-first schedule editing and real-time updates service.
    
    Features:
    - Mobile-optimized APIs for schedule editing with touch-friendly interfaces
    - Real-time cloud synchronization for schedule modifications
    - Alternative suggestion generation with cloud-based AI processing
    - Gesture-based editing with haptic feedback
    - Conflict resolution with visual previews
    - Offline editing with sync when online
    """
    
    def __init__(self, schedule_generator: ScheduleGeneratorService):
        self.schedule_generator = schedule_generator
        self.active_connections = {}  # WebSocket connections for real-time updates
        self.pending_edits = {}  # Offline edits waiting for sync
        self.edit_history = {}  # Edit history for undo/redo
        
        # Mobile interface configuration
        self.touch_interface = TouchFriendlyInterface()
        
        # Real-time sync configuration
        self.sync_interval_seconds = 2
        self.max_offline_edits = 50
        self.conflict_resolution_timeout = 30  # seconds
    
    async def handle_mobile_edit(self, edit_request: MobileEditRequest) -> Dict[str, Any]:
        """
        Handle mobile schedule editing request with touch-friendly interface.
        
        Args:
            edit_request: Mobile edit request with gesture and touch data
            
        Returns:
            Edit result with real-time updates and suggestions
        """
        logger.info(f"Handling mobile edit: {edit_request.action.value} for user {edit_request.user_id}")
        
        try:
            # Validate touch gesture and coordinates
            if not self._validate_touch_input(edit_request):
                return {
                    'success': False,
                    'error': 'Invalid touch input',
                    'suggestions': []
                }
            
            # Get current schedule
            schedule = await self._get_schedule(edit_request.schedule_id)
            if not schedule:
                return {
                    'success': False,
                    'error': 'Schedule not found',
                    'suggestions': []
                }
            
            # Apply edit based on action type
            edit_result = await self._apply_mobile_edit(edit_request, schedule)
            
            # Generate alternative suggestions
            suggestions = await self._generate_alternative_suggestions(
                edit_request, schedule, edit_result
            )
            
            # Create real-time update
            real_time_update = RealTimeUpdate(
                update_id=f"update_{datetime.now().timestamp()}",
                user_id=edit_request.user_id,
                schedule_id=edit_request.schedule_id,
                action=edit_request.action,
                affected_blocks=edit_result.get('affected_blocks', []),
                changes=edit_result.get('changes', {}),
                timestamp=datetime.now(),
                sync_status=SyncStatus.SYNCING
            )
            
            # Broadcast real-time update
            await self._broadcast_real_time_update(real_time_update)
            
            # Save edit to history for undo/redo
            self._save_edit_to_history(edit_request, edit_result)
            
            return {
                'success': True,
                'edit_result': edit_result,
                'suggestions': suggestions,
                'real_time_update': asdict(real_time_update),
                'haptic_feedback': self._generate_haptic_feedback(edit_request.action),
                'visual_feedback': self._generate_visual_feedback(edit_request.action)
            }
            
        except Exception as e:
            logger.error(f"Error handling mobile edit: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'suggestions': []
            }
    
    async def setup_real_time_sync(self, user_id: str, websocket) -> None:
        """
        Set up real-time synchronization for mobile client.
        
        Args:
            user_id: User identifier
            websocket: WebSocket connection for real-time updates
        """
        logger.info(f"Setting up real-time sync for user {user_id}")
        
        # Store WebSocket connection
        self.active_connections[user_id] = websocket
        
        try:
            # Send initial sync status
            await websocket.send(json.dumps({
                'type': 'sync_status',
                'status': SyncStatus.SYNCED.value,
                'timestamp': datetime.now().isoformat()
            }))
            
            # Start sync loop
            await self._real_time_sync_loop(user_id, websocket)
            
        except websockets.exceptions.ConnectionClosed:
            logger.info(f"WebSocket connection closed for user {user_id}")
        except Exception as e:
            logger.error(f"Error in real-time sync: {str(e)}")
        finally:
            # Clean up connection
            if user_id in self.active_connections:
                del self.active_connections[user_id]
    
    async def handle_offline_edits(self, user_id: str, offline_edits: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Handle offline edits when device comes back online.
        
        Args:
            user_id: User identifier
            offline_edits: List of edits made while offline
            
        Returns:
            Sync result with conflict resolution
        """
        logger.info(f"Handling {len(offline_edits)} offline edits for user {user_id}")
        
        sync_results = []
        conflicts = []
        
        for edit_data in offline_edits:
            try:
                # Convert to edit request
                edit_request = self._convert_to_edit_request(edit_data)
                
                # Check for conflicts with server state
                conflict = await self._check_for_conflicts(edit_request)
                
                if conflict:
                    conflicts.append(conflict)
                    # Store for manual resolution
                    self.pending_edits[user_id] = self.pending_edits.get(user_id, [])
                    self.pending_edits[user_id].append(edit_request)
                else:
                    # Apply edit
                    result = await self.handle_mobile_edit(edit_request)
                    sync_results.append(result)
            
            except Exception as e:
                logger.error(f"Error processing offline edit: {str(e)}")
                conflicts.append({
                    'type': 'processing_error',
                    'error': str(e),
                    'edit_data': edit_data
                })
        
        return {
            'synced_edits': len(sync_results),
            'conflicts': conflicts,
            'sync_results': sync_results,
            'requires_manual_resolution': len(conflicts) > 0
        }
    
    async def generate_smart_suggestions(
        self,
        user_id: str,
        schedule_id: str,
        context: Dict[str, Any]
    ) -> List[AlternativeSuggestion]:
        """
        Generate smart alternative suggestions with cloud-based AI processing.
        
        Args:
            user_id: User identifier
            schedule_id: Schedule identifier
            context: Context for suggestion generation
            
        Returns:
            List of alternative suggestions
        """
        logger.info(f"Generating smart suggestions for user {user_id}")
        
        # Get current schedule
        schedule = await self._get_schedule(schedule_id)
        if not schedule:
            return []
        
        suggestions = []
        
        # Analyze schedule for optimization opportunities
        optimization_opportunities = await self._analyze_schedule_optimization(schedule, context)
        
        # Generate time slot suggestions
        time_suggestions = await self._generate_time_slot_suggestions(schedule, context)
        suggestions.extend(time_suggestions)
        
        # Generate task split suggestions
        split_suggestions = await self._generate_task_split_suggestions(schedule, context)
        suggestions.extend(split_suggestions)
        
        # Generate priority adjustment suggestions
        priority_suggestions = await self._generate_priority_suggestions(schedule, context)
        suggestions.extend(priority_suggestions)
        
        # Generate break addition suggestions
        break_suggestions = await self._generate_break_suggestions(schedule, context)
        suggestions.extend(break_suggestions)
        
        # Sort by confidence and impact
        suggestions.sort(key=lambda x: x.confidence * x.impact_score, reverse=True)
        
        return suggestions[:10]  # Return top 10 suggestions
    
    async def resolve_schedule_conflicts(
        self,
        user_id: str,
        conflicts: List[ScheduleConflict],
        resolution_preferences: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Resolve schedule conflicts with mobile-friendly interface.
        
        Args:
            user_id: User identifier
            conflicts: List of conflicts to resolve
            resolution_preferences: User preferences for conflict resolution
            
        Returns:
            Conflict resolution result
        """
        logger.info(f"Resolving {len(conflicts)} conflicts for user {user_id}")
        
        resolution_results = []
        
        for conflict in conflicts:
            try:
                # Generate resolution options
                resolution_options = await self._generate_conflict_resolution_options(
                    conflict, resolution_preferences
                )
                
                # Apply automatic resolution if preference is set
                if resolution_preferences.get('auto_resolve', False):
                    best_option = max(resolution_options, key=lambda x: x.get('score', 0))
                    resolution_result = await self._apply_conflict_resolution(conflict, best_option)
                    resolution_results.append(resolution_result)
                else:
                    # Present options to user for manual selection
                    resolution_results.append({
                        'conflict_id': conflict.conflict_id,
                        'options': resolution_options,
                        'requires_user_input': True
                    })
            
            except Exception as e:
                logger.error(f"Error resolving conflict {conflict.conflict_id}: {str(e)}")
                resolution_results.append({
                    'conflict_id': conflict.conflict_id,
                    'error': str(e),
                    'resolved': False
                })
        
        return {
            'total_conflicts': len(conflicts),
            'resolved_conflicts': len([r for r in resolution_results if r.get('resolved', False)]),
            'pending_conflicts': len([r for r in resolution_results if r.get('requires_user_input', False)]),
            'resolution_results': resolution_results
        }
    
    def _validate_touch_input(self, edit_request: MobileEditRequest) -> bool:
        """Validate touch input for mobile editing."""
        # Check if coordinates are within valid range
        x, y = edit_request.touch_coordinates
        if x < 0 or y < 0:
            return False
        
        # Validate gesture for action
        valid_gestures = {
            EditAction.MOVE_TASK: [TouchGesture.DRAG],
            EditAction.RESIZE_TASK: [TouchGesture.PINCH, TouchGesture.DRAG],
            EditAction.DELETE_TASK: [TouchGesture.SWIPE_LEFT, TouchGesture.LONG_PRESS],
            EditAction.ADD_TASK: [TouchGesture.TAP, TouchGesture.DOUBLE_TAP],
            EditAction.CHANGE_PRIORITY: [TouchGesture.LONG_PRESS],
            EditAction.ADD_BREAK: [TouchGesture.DOUBLE_TAP]
        }
        
        allowed_gestures = valid_gestures.get(edit_request.action, [])
        return edit_request.gesture in allowed_gestures
    
    async def _apply_mobile_edit(
        self,
        edit_request: MobileEditRequest,
        schedule: GeneratedSchedule
    ) -> Dict[str, Any]:
        """Apply mobile edit to schedule."""
        
        if edit_request.action == EditAction.MOVE_TASK:
            return await self._move_task(edit_request, schedule)
        elif edit_request.action == EditAction.RESIZE_TASK:
            return await self._resize_task(edit_request, schedule)
        elif edit_request.action == EditAction.DELETE_TASK:
            return await self._delete_task(edit_request, schedule)
        elif edit_request.action == EditAction.ADD_TASK:
            return await self._add_task(edit_request, schedule)
        elif edit_request.action == EditAction.SPLIT_TASK:
            return await self._split_task(edit_request, schedule)
        elif edit_request.action == EditAction.CHANGE_PRIORITY:
            return await self._change_priority(edit_request, schedule)
        elif edit_request.action == EditAction.ADD_BREAK:
            return await self._add_break(edit_request, schedule)
        else:
            raise ValueError(f"Unsupported edit action: {edit_request.action}")
    
    async def _move_task(self, edit_request: MobileEditRequest, schedule: GeneratedSchedule) -> Dict[str, Any]:
        """Move task to new time slot."""
        target_block = self._find_block_by_id(schedule, edit_request.target_block_id)
        if not target_block:
            raise ValueError("Target block not found")
        
        # Calculate new time based on touch coordinates
        new_start_time = self._calculate_time_from_coordinates(
            edit_request.touch_coordinates, schedule
        )
        
        # Update block timing
        duration = target_block.duration_minutes
        target_block.start_time = new_start_time
        target_block.end_time = new_start_time + timedelta(minutes=duration)
        
        # Check for conflicts
        conflicts = self.schedule_generator._detect_conflicts(
            [b for b in schedule.time_blocks if b.id != target_block.id],
            target_block
        )
        
        return {
            'action': 'move_task',
            'affected_blocks': [target_block.id],
            'changes': {
                'new_start_time': new_start_time.isoformat(),
                'new_end_time': target_block.end_time.isoformat()
            },
            'conflicts': [asdict(c) for c in conflicts],
            'success': len(conflicts) == 0
        }
    
    async def _resize_task(self, edit_request: MobileEditRequest, schedule: GeneratedSchedule) -> Dict[str, Any]:
        """Resize task duration."""
        target_block = self._find_block_by_id(schedule, edit_request.target_block_id)
        if not target_block:
            raise ValueError("Target block not found")
        
        # Calculate new duration based on gesture
        new_duration = edit_request.new_values.get('duration_minutes', target_block.duration_minutes)
        
        # Update block
        target_block.duration_minutes = new_duration
        target_block.end_time = target_block.start_time + timedelta(minutes=new_duration)
        
        return {
            'action': 'resize_task',
            'affected_blocks': [target_block.id],
            'changes': {
                'new_duration': new_duration,
                'new_end_time': target_block.end_time.isoformat()
            },
            'success': True
        }
    
    async def _delete_task(self, edit_request: MobileEditRequest, schedule: GeneratedSchedule) -> Dict[str, Any]:
        """Delete task from schedule."""
        target_block = self._find_block_by_id(schedule, edit_request.target_block_id)
        if not target_block:
            raise ValueError("Target block not found")
        
        # Remove block from schedule
        schedule.time_blocks.remove(target_block)
        
        return {
            'action': 'delete_task',
            'affected_blocks': [target_block.id],
            'changes': {
                'deleted_block': asdict(target_block)
            },
            'success': True
        }
    
    async def _add_task(self, edit_request: MobileEditRequest, schedule: GeneratedSchedule) -> Dict[str, Any]:
        """Add new task to schedule."""
        # Calculate time from touch coordinates
        start_time = self._calculate_time_from_coordinates(
            edit_request.touch_coordinates, schedule
        )
        
        # Create new task block
        new_task_data = edit_request.new_values
        new_block = TimeBlock(
            id=f"task_{datetime.now().timestamp()}",
            title=new_task_data.get('title', 'New Task'),
            start_time=start_time,
            end_time=start_time + timedelta(minutes=new_task_data.get('duration_minutes', 60)),
            duration_minutes=new_task_data.get('duration_minutes', 60),
            priority=TaskPriority.MEDIUM,
            task_type=new_task_data.get('task_type', 'general'),
            flexibility_minutes=30
        )
        
        # Add to schedule
        schedule.time_blocks.append(new_block)
        
        return {
            'action': 'add_task',
            'affected_blocks': [new_block.id],
            'changes': {
                'new_block': asdict(new_block)
            },
            'success': True
        }
    
    async def _add_break(self, edit_request: MobileEditRequest, schedule: GeneratedSchedule) -> Dict[str, Any]:
        """Add break to schedule."""
        # Calculate time from touch coordinates
        start_time = self._calculate_time_from_coordinates(
            edit_request.touch_coordinates, schedule
        )
        
        # Create break block
        break_duration = edit_request.new_values.get('duration_minutes', 15)
        break_block = TimeBlock(
            id=f"break_{datetime.now().timestamp()}",
            title="Break",
            start_time=start_time,
            end_time=start_time + timedelta(minutes=break_duration),
            duration_minutes=break_duration,
            priority=TaskPriority.LOW,
            task_type='break',
            flexibility_minutes=10
        )
        
        # Add to schedule
        schedule.time_blocks.append(break_block)
        
        return {
            'action': 'add_break',
            'affected_blocks': [break_block.id],
            'changes': {
                'new_break': asdict(break_block)
            },
            'success': True
        }
    
    def _find_block_by_id(self, schedule: GeneratedSchedule, block_id: str) -> Optional[TimeBlock]:
        """Find time block by ID."""
        for block in schedule.time_blocks:
            if block.id == block_id:
                return block
        return None
    
    def _calculate_time_from_coordinates(
        self,
        coordinates: Tuple[float, float],
        schedule: GeneratedSchedule
    ) -> datetime:
        """Calculate time from touch coordinates."""
        x, y = coordinates
        
        # Simple calculation - in real implementation, this would consider
        # the actual UI layout and time scale
        base_time = schedule.start_date.replace(hour=9, minute=0, second=0, microsecond=0)
        
        # Assume y coordinate represents hours (0-1 = 9-17 hours)
        hour_offset = int(y * 8)  # 8 working hours
        minute_offset = int((y * 8 - hour_offset) * 60)
        
        return base_time + timedelta(hours=hour_offset, minutes=minute_offset)
    
    async def _generate_alternative_suggestions(
        self,
        edit_request: MobileEditRequest,
        schedule: GeneratedSchedule,
        edit_result: Dict[str, Any]
    ) -> List[AlternativeSuggestion]:
        """Generate alternative suggestions for the edit."""
        suggestions = []
        
        # If there are conflicts, suggest alternatives
        if edit_result.get('conflicts'):
            # Suggest alternative time slots
            alt_times = await self._suggest_alternative_times(edit_request, schedule)
            suggestions.extend(alt_times)
            
            # Suggest task splitting if task is long
            if edit_request.action == EditAction.MOVE_TASK:
                target_block = self._find_block_by_id(schedule, edit_request.target_block_id)
                if target_block and target_block.duration_minutes > 90:
                    split_suggestion = AlternativeSuggestion(
                        suggestion_id=f"split_{datetime.now().timestamp()}",
                        suggestion_type='task_split',
                        description=f'Split "{target_block.title}" into smaller chunks',
                        confidence=0.8,
                        impact_score=0.7,
                        implementation={
                            'action': 'split_task',
                            'block_id': target_block.id,
                            'split_count': 2
                        }
                    )
                    suggestions.append(split_suggestion)
        
        return suggestions
    
    async def _suggest_alternative_times(
        self,
        edit_request: MobileEditRequest,
        schedule: GeneratedSchedule
    ) -> List[AlternativeSuggestion]:
        """Suggest alternative time slots."""
        suggestions = []
        
        target_block = self._find_block_by_id(schedule, edit_request.target_block_id)
        if not target_block:
            return suggestions
        
        # Find available time slots
        available_slots = self._find_available_slots(schedule, target_block.duration_minutes)
        
        for i, slot in enumerate(available_slots[:3]):  # Top 3 suggestions
            suggestion = AlternativeSuggestion(
                suggestion_id=f"alt_time_{i}_{datetime.now().timestamp()}",
                suggestion_type='time_slot',
                description=f'Move to {slot.strftime("%I:%M %p")}',
                confidence=0.9 - (i * 0.1),  # Decreasing confidence
                impact_score=0.8,
                implementation={
                    'action': 'move_task',
                    'block_id': target_block.id,
                    'new_start_time': slot.isoformat()
                }
            )
            suggestions.append(suggestion)
        
        return suggestions
    
    def _find_available_slots(self, schedule: GeneratedSchedule, duration_minutes: int) -> List[datetime]:
        """Find available time slots for a given duration."""
        available_slots = []
        
        # Simple implementation - find gaps in schedule
        sorted_blocks = sorted(schedule.time_blocks, key=lambda x: x.start_time)
        
        current_time = schedule.start_date.replace(hour=9, minute=0, second=0, microsecond=0)
        end_time = schedule.start_date.replace(hour=17, minute=0, second=0, microsecond=0)
        
        for block in sorted_blocks:
            # Check gap before this block
            gap_duration = (block.start_time - current_time).total_seconds() / 60
            
            if gap_duration >= duration_minutes:
                available_slots.append(current_time)
            
            current_time = block.end_time
        
        # Check gap after last block
        if current_time < end_time:
            gap_duration = (end_time - current_time).total_seconds() / 60
            if gap_duration >= duration_minutes:
                available_slots.append(current_time)
        
        return available_slots
    
    async def _broadcast_real_time_update(self, update: RealTimeUpdate) -> None:
        """Broadcast real-time update to connected clients."""
        if update.user_id in self.active_connections:
            try:
                websocket = self.active_connections[update.user_id]
                await websocket.send(json.dumps({
                    'type': 'schedule_update',
                    'update': asdict(update)
                }))
            except Exception as e:
                logger.error(f"Error broadcasting update: {str(e)}")
    
    async def _real_time_sync_loop(self, user_id: str, websocket) -> None:
        """Real-time synchronization loop."""
        while True:
            try:
                # Wait for sync interval
                await asyncio.sleep(self.sync_interval_seconds)
                
                # Check for pending updates
                if user_id in self.pending_edits:
                    # Process pending edits
                    pending = self.pending_edits[user_id]
                    if pending:
                        await websocket.send(json.dumps({
                            'type': 'sync_required',
                            'pending_edits': len(pending)
                        }))
                
                # Send heartbeat
                await websocket.send(json.dumps({
                    'type': 'heartbeat',
                    'timestamp': datetime.now().isoformat()
                }))
                
            except websockets.exceptions.ConnectionClosed:
                break
            except Exception as e:
                logger.error(f"Error in sync loop: {str(e)}")
                break
    
    def _generate_haptic_feedback(self, action: EditAction) -> Dict[str, Any]:
        """Generate haptic feedback configuration for mobile action."""
        feedback_patterns = {
            EditAction.MOVE_TASK: {'type': 'light', 'duration': 100},
            EditAction.RESIZE_TASK: {'type': 'medium', 'duration': 150},
            EditAction.DELETE_TASK: {'type': 'heavy', 'duration': 200},
            EditAction.ADD_TASK: {'type': 'success', 'duration': 100},
            EditAction.CHANGE_PRIORITY: {'type': 'warning', 'duration': 150},
            EditAction.ADD_BREAK: {'type': 'light', 'duration': 80}
        }
        
        return feedback_patterns.get(action, {'type': 'light', 'duration': 100})
    
    def _generate_visual_feedback(self, action: EditAction) -> Dict[str, Any]:
        """Generate visual feedback for mobile action."""
        visual_feedback = {
            EditAction.MOVE_TASK: {'animation': 'slide', 'color': '#007AFF', 'duration': 200},
            EditAction.RESIZE_TASK: {'animation': 'scale', 'color': '#34C759', 'duration': 250},
            EditAction.DELETE_TASK: {'animation': 'fade_out', 'color': '#FF3B30', 'duration': 300},
            EditAction.ADD_TASK: {'animation': 'fade_in', 'color': '#007AFF', 'duration': 200},
            EditAction.CHANGE_PRIORITY: {'animation': 'pulse', 'color': '#FF9500', 'duration': 150},
            EditAction.ADD_BREAK: {'animation': 'bounce', 'color': '#5AC8FA', 'duration': 180}
        }
        
        return visual_feedback.get(action, {'animation': 'fade', 'color': '#007AFF', 'duration': 200})
    
    def _save_edit_to_history(self, edit_request: MobileEditRequest, edit_result: Dict[str, Any]) -> None:
        """Save edit to history for undo/redo functionality."""
        user_id = edit_request.user_id
        
        if user_id not in self.edit_history:
            self.edit_history[user_id] = []
        
        history_entry = {
            'timestamp': edit_request.timestamp.isoformat(),
            'action': edit_request.action.value,
            'edit_request': asdict(edit_request),
            'edit_result': edit_result
        }
        
        self.edit_history[user_id].append(history_entry)
        
        # Keep only last 50 edits
        if len(self.edit_history[user_id]) > 50:
            self.edit_history[user_id] = self.edit_history[user_id][-50:]
    
    async def _get_schedule(self, schedule_id: str) -> Optional[GeneratedSchedule]:
        """Get schedule by ID (placeholder implementation)."""
        # In real implementation, this would fetch from database
        # For now, return a mock schedule
        return GeneratedSchedule(
            schedule_id=schedule_id,
            user_id="mock_user",
            schedule_type=self.schedule_generator.ScheduleType.DAILY,
            start_date=datetime.now(),
            end_date=datetime.now() + timedelta(days=1),
            time_blocks=[],
            conflicts=[],
            optimization_score=0.8,
            focus_time_protected=True,
            habits_preserved=True,
            metadata={}
        )
    
    def get_mobile_editor_stats(self) -> Dict[str, Any]:
        """Get mobile editor statistics."""
        return {
            'active_connections': len(self.active_connections),
            'pending_edits': sum(len(edits) for edits in self.pending_edits.values()),
            'edit_history_entries': sum(len(history) for history in self.edit_history.values()),
            'sync_interval_seconds': self.sync_interval_seconds,
            'supported_gestures': [g.value for g in TouchGesture],
            'supported_actions': [a.value for a in EditAction],
            'touch_interface_config': asdict(self.touch_interface)
        }