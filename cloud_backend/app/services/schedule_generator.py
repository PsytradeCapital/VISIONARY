"""
Intelligent schedule generation service with autonomous features.

Implements SkedPal-inspired constraint satisfaction solver, Akiflow-style multi-calendar
integration, and dynamic time blocking with habit defense mechanisms like Motion.
"""

import json
import logging
from typing import Dict, List, Optional, Any, Tuple, Set
from datetime import datetime, timedelta, time
from dataclasses import dataclass, asdict
from enum import Enum
import heapq
from collections import defaultdict
from .pattern_recognition import (
    PatternRecognitionService, FocusTimeBlock, HabitDefenseRule, 
    PatternType, FocusTimeQuality
)

logger = logging.getLogger(__name__)


class ScheduleType(Enum):
    """Types of schedules that can be generated."""
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"


class TaskPriority(Enum):
    """Task priority levels."""
    CRITICAL = 5
    HIGH = 4
    MEDIUM = 3
    LOW = 2
    OPTIONAL = 1


class ConflictResolutionStrategy(Enum):
    """Strategies for resolving scheduling conflicts."""
    RESCHEDULE_LOWER_PRIORITY = "reschedule_lower_priority"
    SPLIT_TASK = "split_task"
    SUGGEST_ALTERNATIVE_TIME = "suggest_alternative_time"
    DEFER_TO_NEXT_DAY = "defer_to_next_day"
    COMPRESS_TASKS = "compress_tasks"


@dataclass
class TimeBlock:
    """Represents a time block in the schedule."""
    id: str
    title: str
    start_time: datetime
    end_time: datetime
    duration_minutes: int
    priority: TaskPriority
    task_type: str
    vision_category: Optional[str] = None
    flexibility_minutes: int = 0
    is_focus_time: bool = False
    is_habit: bool = False
    buffer_time_minutes: int = 0
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


@dataclass
class ScheduleConstraint:
    """Represents a scheduling constraint."""
    constraint_type: str  # 'time_window', 'duration', 'frequency', 'dependency'
    parameters: Dict[str, Any]
    priority: int  # 1-10, higher = more important
    flexibility: float  # 0.0-1.0, higher = more flexible


@dataclass
class ExternalCalendar:
    """Represents an external calendar integration."""
    calendar_id: str
    calendar_type: str  # 'google', 'apple', 'outlook'
    events: List[Dict[str, Any]]
    sync_enabled: bool
    conflict_resolution: str


@dataclass
class ScheduleConflict:
    """Represents a scheduling conflict."""
    conflict_id: str
    conflicting_blocks: List[TimeBlock]
    conflict_type: str  # 'overlap', 'constraint_violation', 'resource_conflict'
    severity: int  # 1-10
    suggested_resolutions: List[Dict[str, Any]]


@dataclass
class GeneratedSchedule:
    """Represents a generated schedule."""
    schedule_id: str
    user_id: str
    schedule_type: ScheduleType
    start_date: datetime
    end_date: datetime
    time_blocks: List[TimeBlock]
    conflicts: List[ScheduleConflict]
    optimization_score: float
    focus_time_protected: bool
    habits_preserved: bool
    metadata: Dict[str, Any]


class ScheduleGeneratorService:
    """
    Intelligent schedule generation service with autonomous features.
    
    Features:
    - SkedPal-inspired constraint satisfaction solver with autonomous adjustments
    - Akiflow-style multi-calendar integration with conflict prevention
    - Dynamic time blocking with habit defense mechanisms like Motion
    - Focus time protection and autonomous rescheduling
    - Real-time conflict resolution and optimization
    """
    
    def __init__(self, pattern_service: PatternRecognitionService):
        self.pattern_service = pattern_service
        self.schedule_cache = {}
        
        # Optimization parameters
        self.max_optimization_iterations = 100
        self.min_optimization_score = 0.7
        self.focus_time_buffer_minutes = 15
        self.habit_protection_strength = 0.8
        
        # Constraint weights for optimization
        self.constraint_weights = {
            'priority_alignment': 0.3,
            'time_preference': 0.2,
            'focus_time_protection': 0.2,
            'habit_preservation': 0.15,
            'energy_alignment': 0.1,
            'conflict_minimization': 0.05
        }
    
    async def generate_schedule(
        self,
        user_id: str,
        schedule_type: ScheduleType,
        tasks: List[Dict[str, Any]],
        constraints: List[ScheduleConstraint],
        external_calendars: List[ExternalCalendar] = None,
        user_preferences: Dict[str, Any] = None
    ) -> GeneratedSchedule:
        """
        Generate intelligent schedule with autonomous time blocking.
        
        Args:
            user_id: User identifier
            schedule_type: Type of schedule to generate
            tasks: List of tasks to schedule
            constraints: Scheduling constraints
            external_calendars: External calendar integrations
            user_preferences: User preferences and patterns
            
        Returns:
            GeneratedSchedule with optimized time blocks
        """
        logger.info(f"Generating {schedule_type.value} schedule for user {user_id}")
        
        if external_calendars is None:
            external_calendars = []
        if user_preferences is None:
            user_preferences = {}
        
        # Get user patterns for intelligent scheduling
        user_patterns = await self._get_user_patterns(user_id)
        
        # Generate focus time blocks
        focus_blocks = await self._generate_focus_time_blocks(user_id, user_patterns)
        
        # Generate habit defense rules
        habit_rules = await self._generate_habit_defense_rules(user_id, user_patterns)
        
        # Create time blocks from tasks
        time_blocks = self._create_time_blocks_from_tasks(tasks, user_preferences)
        
        # Integrate external calendar events
        external_blocks = self._integrate_external_calendars(external_calendars)
        
        # Perform constraint satisfaction and optimization
        optimized_schedule = await self._optimize_schedule(
            user_id=user_id,
            schedule_type=schedule_type,
            time_blocks=time_blocks,
            external_blocks=external_blocks,
            focus_blocks=focus_blocks,
            habit_rules=habit_rules,
            constraints=constraints,
            user_patterns=user_patterns
        )
        
        return optimized_schedule
    
    async def resolve_conflicts(
        self,
        schedule: GeneratedSchedule,
        new_task: Dict[str, Any],
        resolution_strategy: ConflictResolutionStrategy = ConflictResolutionStrategy.RESCHEDULE_LOWER_PRIORITY
    ) -> GeneratedSchedule:
        """
        Resolve scheduling conflicts using autonomous adjustments.
        
        Args:
            schedule: Current schedule
            new_task: New task to add
            resolution_strategy: Strategy for conflict resolution
            
        Returns:
            Updated schedule with conflicts resolved
        """
        logger.info(f"Resolving conflicts for new task: {new_task.get('title', 'Untitled')}")
        
        # Create time block for new task
        new_block = self._create_time_block_from_task(new_task)
        
        # Detect conflicts
        conflicts = self._detect_conflicts(schedule.time_blocks, new_block)
        
        if not conflicts:
            # No conflicts, add task directly
            schedule.time_blocks.append(new_block)
            return schedule
        
        # Resolve conflicts based on strategy
        resolved_schedule = await self._apply_conflict_resolution(
            schedule, new_block, conflicts, resolution_strategy
        )
        
        # Re-optimize after conflict resolution
        return await self._reoptimize_schedule(resolved_schedule)
    
    async def autonomous_reschedule(
        self,
        schedule: GeneratedSchedule,
        disruption: Dict[str, Any]
    ) -> GeneratedSchedule:
        """
        Perform autonomous rescheduling based on disruptions.
        
        Args:
            schedule: Current schedule
            disruption: Information about the disruption
            
        Returns:
            Autonomously adjusted schedule
        """
        logger.info(f"Performing autonomous reschedule due to: {disruption.get('type', 'unknown')}")
        
        disruption_type = disruption.get('type')
        affected_time = disruption.get('time_range', {})
        
        # Identify affected blocks
        affected_blocks = self._identify_affected_blocks(schedule.time_blocks, affected_time)
        
        # Apply autonomous adjustments based on disruption type
        if disruption_type == 'meeting_overrun':
            adjusted_schedule = await self._handle_meeting_overrun(schedule, affected_blocks, disruption)
        elif disruption_type == 'urgent_task':
            adjusted_schedule = await self._handle_urgent_task(schedule, affected_blocks, disruption)
        elif disruption_type == 'energy_level_change':
            adjusted_schedule = await self._handle_energy_change(schedule, affected_blocks, disruption)
        elif disruption_type == 'external_event':
            adjusted_schedule = await self._handle_external_event(schedule, affected_blocks, disruption)
        else:
            # Generic rescheduling
            adjusted_schedule = await self._generic_reschedule(schedule, affected_blocks, disruption)
        
        return adjusted_schedule
    
    async def integrate_multiple_calendars(
        self,
        user_id: str,
        calendars: List[ExternalCalendar],
        schedule_preferences: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Integrate multiple external calendars with conflict prevention.
        
        Args:
            user_id: User identifier
            calendars: List of external calendars
            schedule_preferences: User scheduling preferences
            
        Returns:
            Integration result with conflict analysis
        """
        logger.info(f"Integrating {len(calendars)} calendars for user {user_id}")
        
        # Collect all external events
        all_events = []
        calendar_conflicts = []
        
        for calendar in calendars:
            events = self._normalize_calendar_events(calendar)
            all_events.extend(events)
            
            # Check for conflicts between calendars
            conflicts = self._detect_cross_calendar_conflicts(all_events, events)
            if conflicts:
                calendar_conflicts.extend(conflicts)
        
        # Create integrated timeline
        integrated_timeline = self._create_integrated_timeline(all_events)
        
        # Identify scheduling opportunities
        available_slots = self._identify_available_slots(integrated_timeline, schedule_preferences)
        
        return {
            'integrated_timeline': integrated_timeline,
            'available_slots': available_slots,
            'calendar_conflicts': calendar_conflicts,
            'total_events': len(all_events),
            'integration_quality': self._calculate_integration_quality(all_events, calendar_conflicts)
        }
    
    async def _get_user_patterns(self, user_id: str) -> Dict[str, Any]:
        """Get user patterns for intelligent scheduling."""
        # This would typically fetch from the pattern recognition service
        # For now, return default patterns
        return {
            'productivity_hours': [9, 10, 11, 14, 15],
            'focus_time_preferences': [
                {'start_hour': 9, 'duration': 120, 'quality': 'high'},
                {'start_hour': 14, 'duration': 90, 'quality': 'medium'}
            ],
            'energy_patterns': {
                'high_energy': [8, 9, 10, 14, 15],
                'medium_energy': [11, 12, 16, 17],
                'low_energy': [13, 18, 19]
            },
            'habit_times': {
                'exercise': {'preferred_hour': 7, 'flexibility': 60},
                'planning': {'preferred_hour': 8, 'flexibility': 30}
            }
        }
    
    async def _generate_focus_time_blocks(self, user_id: str, patterns: Dict[str, Any]) -> List[FocusTimeBlock]:
        """Generate focus time blocks based on user patterns."""
        focus_blocks = []
        
        focus_preferences = patterns.get('focus_time_preferences', [])
        
        for pref in focus_preferences:
            start_hour = pref['start_hour']
            duration = pref['duration']
            quality = pref['quality']
            
            # Map quality to enum
            quality_map = {
                'high': FocusTimeQuality.DEEP,
                'medium': FocusTimeQuality.MODERATE,
                'low': FocusTimeQuality.SHALLOW
            }
            
            focus_block = FocusTimeBlock(
                start_time=time(start_hour, 0),
                end_time=time(start_hour + duration // 60, duration % 60),
                duration_minutes=duration,
                quality=quality_map.get(quality, FocusTimeQuality.MODERATE),
                protection_level=4 if quality == 'high' else 3,
                buffer_minutes=self.focus_time_buffer_minutes,
                interruption_cost=10.0 if quality == 'high' else 5.0,
                recovery_time_minutes=20 if quality == 'high' else 10
            )
            
            focus_blocks.append(focus_block)
        
        return focus_blocks
    
    async def _generate_habit_defense_rules(self, user_id: str, patterns: Dict[str, Any]) -> List[HabitDefenseRule]:
        """Generate habit defense rules based on user patterns."""
        habit_rules = []
        
        habit_times = patterns.get('habit_times', {})
        
        for habit_name, habit_data in habit_times.items():
            preferred_hour = habit_data['preferred_hour']
            flexibility = habit_data['flexibility']
            
            # Generate alternative times
            alternative_times = [
                time(max(0, preferred_hour - 1), 0),
                time(min(23, preferred_hour + 1), 0)
            ]
            
            habit_rule = HabitDefenseRule(
                habit_name=habit_name,
                priority=4,  # High priority for habits
                time_flexibility_minutes=flexibility,
                minimum_frequency_per_week=5,  # Assume daily habits
                protection_strength=self.habit_protection_strength,
                alternative_times=alternative_times,
                conflict_resolution_strategy='reschedule_conflicting_task'
            )
            
            habit_rules.append(habit_rule)
        
        return habit_rules
    
    def _create_time_blocks_from_tasks(self, tasks: List[Dict[str, Any]], 
                                     user_preferences: Dict[str, Any]) -> List[TimeBlock]:
        """Create time blocks from task list."""
        time_blocks = []
        
        for task in tasks:
            block = self._create_time_block_from_task(task, user_preferences)
            time_blocks.append(block)
        
        return time_blocks
    
    def _create_time_block_from_task(self, task: Dict[str, Any], 
                                   user_preferences: Dict[str, Any] = None) -> TimeBlock:
        """Create a time block from a single task."""
        if user_preferences is None:
            user_preferences = {}
        
        # Extract task information
        task_id = task.get('id', f"task_{datetime.now().timestamp()}")
        title = task.get('title', 'Untitled Task')
        duration = task.get('duration_minutes', 60)
        priority_str = task.get('priority', 'medium')
        task_type = task.get('type', 'general')
        
        # Map priority string to enum
        priority_map = {
            'critical': TaskPriority.CRITICAL,
            'high': TaskPriority.HIGH,
            'medium': TaskPriority.MEDIUM,
            'low': TaskPriority.LOW,
            'optional': TaskPriority.OPTIONAL
        }
        
        priority = priority_map.get(priority_str.lower(), TaskPriority.MEDIUM)
        
        # Determine if this is focus time or habit
        is_focus_time = task.get('requires_focus', False) or task_type in ['deep_work', 'creative', 'analysis']
        is_habit = task.get('is_habit', False) or task.get('recurring', False)
        
        # Calculate flexibility and buffer time
        flexibility_minutes = task.get('flexibility_minutes', 30 if priority.value <= 3 else 15)
        buffer_time = 10 if is_focus_time else 5
        
        # Create placeholder start/end times (will be optimized later)
        now = datetime.now()
        start_time = task.get('preferred_start_time', now)
        if isinstance(start_time, str):
            start_time = datetime.fromisoformat(start_time)
        
        end_time = start_time + timedelta(minutes=duration)
        
        return TimeBlock(
            id=task_id,
            title=title,
            start_time=start_time,
            end_time=end_time,
            duration_minutes=duration,
            priority=priority,
            task_type=task_type,
            vision_category=task.get('vision_category'),
            flexibility_minutes=flexibility_minutes,
            is_focus_time=is_focus_time,
            is_habit=is_habit,
            buffer_time_minutes=buffer_time,
            metadata=task.get('metadata', {})
        )
    
    def _integrate_external_calendars(self, calendars: List[ExternalCalendar]) -> List[TimeBlock]:
        """Integrate external calendar events as time blocks."""
        external_blocks = []
        
        for calendar in calendars:
            if not calendar.sync_enabled:
                continue
            
            for event in calendar.events:
                # Convert calendar event to time block
                block = self._convert_event_to_time_block(event, calendar)
                external_blocks.append(block)
        
        return external_blocks
    
    def _convert_event_to_time_block(self, event: Dict[str, Any], 
                                   calendar: ExternalCalendar) -> TimeBlock:
        """Convert calendar event to time block."""
        event_id = event.get('id', f"ext_{datetime.now().timestamp()}")
        title = event.get('title', 'External Event')
        
        # Parse start and end times
        start_time = datetime.fromisoformat(event['start_time'])
        end_time = datetime.fromisoformat(event['end_time'])
        duration = int((end_time - start_time).total_seconds() / 60)
        
        return TimeBlock(
            id=event_id,
            title=f"[{calendar.calendar_type.upper()}] {title}",
            start_time=start_time,
            end_time=end_time,
            duration_minutes=duration,
            priority=TaskPriority.HIGH,  # External events are typically high priority
            task_type='external_event',
            flexibility_minutes=0,  # External events are usually fixed
            is_focus_time=False,
            is_habit=False,
            buffer_time_minutes=5,
            metadata={
                'calendar_id': calendar.calendar_id,
                'calendar_type': calendar.calendar_type,
                'external_event': True
            }
        )
    
    async def _optimize_schedule(
        self,
        user_id: str,
        schedule_type: ScheduleType,
        time_blocks: List[TimeBlock],
        external_blocks: List[TimeBlock],
        focus_blocks: List[FocusTimeBlock],
        habit_rules: List[HabitDefenseRule],
        constraints: List[ScheduleConstraint],
        user_patterns: Dict[str, Any]
    ) -> GeneratedSchedule:
        """Optimize schedule using constraint satisfaction and autonomous adjustments."""
        
        # Combine all blocks
        all_blocks = time_blocks + external_blocks
        
        # Sort by priority and constraints
        all_blocks.sort(key=lambda x: (x.priority.value, x.start_time), reverse=True)
        
        # Apply constraint satisfaction algorithm
        optimized_blocks = await self._constraint_satisfaction_solver(
            all_blocks, focus_blocks, habit_rules, constraints, user_patterns
        )
        
        # Detect remaining conflicts
        conflicts = self._detect_all_conflicts(optimized_blocks)
        
        # Calculate optimization score
        optimization_score = self._calculate_optimization_score(
            optimized_blocks, focus_blocks, habit_rules, user_patterns
        )
        
        # Determine schedule date range
        if optimized_blocks:
            start_date = min(block.start_time for block in optimized_blocks)
            end_date = max(block.end_time for block in optimized_blocks)
        else:
            start_date = datetime.now()
            end_date = start_date + timedelta(days=1)
        
        return GeneratedSchedule(
            schedule_id=f"schedule_{user_id}_{datetime.now().timestamp()}",
            user_id=user_id,
            schedule_type=schedule_type,
            start_date=start_date,
            end_date=end_date,
            time_blocks=optimized_blocks,
            conflicts=conflicts,
            optimization_score=optimization_score,
            focus_time_protected=self._check_focus_time_protection(optimized_blocks, focus_blocks),
            habits_preserved=self._check_habits_preserved(optimized_blocks, habit_rules),
            metadata={
                'generation_time': datetime.now().isoformat(),
                'total_blocks': len(optimized_blocks),
                'external_blocks': len(external_blocks),
                'optimization_iterations': 1  # Placeholder
            }
        )
    
    async def _constraint_satisfaction_solver(
        self,
        blocks: List[TimeBlock],
        focus_blocks: List[FocusTimeBlock],
        habit_rules: List[HabitDefenseRule],
        constraints: List[ScheduleConstraint],
        user_patterns: Dict[str, Any]
    ) -> List[TimeBlock]:
        """Solve scheduling constraints using CSP algorithm."""
        
        # Initialize solution
        solution = []
        unscheduled = blocks.copy()
        
        # Schedule fixed blocks first (external events, habits)
        fixed_blocks = [b for b in blocks if b.flexibility_minutes == 0 or b.is_habit]
        flexible_blocks = [b for b in blocks if b not in fixed_blocks]
        
        # Add fixed blocks to solution
        solution.extend(fixed_blocks)
        
        # Schedule flexible blocks using constraint satisfaction
        for block in flexible_blocks:
            best_time = self._find_best_time_slot(
                block, solution, focus_blocks, habit_rules, user_patterns
            )
            
            if best_time:
                # Update block timing
                block.start_time = best_time
                block.end_time = best_time + timedelta(minutes=block.duration_minutes)
                solution.append(block)
            else:
                # Could not schedule - add to conflicts
                logger.warning(f"Could not schedule block: {block.title}")
        
        return solution
    
    def _find_best_time_slot(
        self,
        block: TimeBlock,
        existing_blocks: List[TimeBlock],
        focus_blocks: List[FocusTimeBlock],
        habit_rules: List[HabitDefenseRule],
        user_patterns: Dict[str, Any]
    ) -> Optional[datetime]:
        """Find the best time slot for a block."""
        
        # Generate candidate time slots
        candidates = self._generate_candidate_slots(block, existing_blocks, user_patterns)
        
        # Score each candidate
        best_slot = None
        best_score = -1
        
        for candidate_time in candidates:
            score = self._score_time_slot(
                block, candidate_time, existing_blocks, focus_blocks, habit_rules, user_patterns
            )
            
            if score > best_score:
                best_score = score
                best_slot = candidate_time
        
        return best_slot if best_score > 0.5 else None
    
    def _generate_candidate_slots(
        self,
        block: TimeBlock,
        existing_blocks: List[TimeBlock],
        user_patterns: Dict[str, Any]
    ) -> List[datetime]:
        """Generate candidate time slots for a block."""
        candidates = []
        
        # Get working hours
        work_start = user_patterns.get('work_start_hour', 9)
        work_end = user_patterns.get('work_end_hour', 17)
        
        # Generate slots for next 7 days
        base_date = datetime.now().replace(hour=work_start, minute=0, second=0, microsecond=0)
        
        for day_offset in range(7):
            current_date = base_date + timedelta(days=day_offset)
            
            # Generate hourly slots within working hours
            for hour_offset in range(work_end - work_start):
                slot_time = current_date + timedelta(hours=hour_offset)
                
                # Check if slot has enough time for the block
                if self._has_sufficient_time(slot_time, block, existing_blocks):
                    candidates.append(slot_time)
        
        return candidates
    
    def _score_time_slot(
        self,
        block: TimeBlock,
        candidate_time: datetime,
        existing_blocks: List[TimeBlock],
        focus_blocks: List[FocusTimeBlock],
        habit_rules: List[HabitDefenseRule],
        user_patterns: Dict[str, Any]
    ) -> float:
        """Score a candidate time slot for a block."""
        score = 0.0
        
        # Check for conflicts
        if self._has_conflicts(block, candidate_time, existing_blocks):
            return 0.0  # Invalid slot
        
        # Priority alignment (higher priority tasks get better times)
        priority_score = block.priority.value / 5.0
        score += priority_score * self.constraint_weights['priority_alignment']
        
        # Time preference alignment
        hour = candidate_time.hour
        productivity_hours = user_patterns.get('productivity_hours', [9, 10, 11, 14, 15])
        
        if hour in productivity_hours:
            time_pref_score = 1.0
        else:
            time_pref_score = 0.5
        
        score += time_pref_score * self.constraint_weights['time_preference']
        
        # Focus time alignment
        if block.is_focus_time:
            focus_score = self._calculate_focus_time_score(candidate_time, focus_blocks)
            score += focus_score * self.constraint_weights['focus_time_protection']
        
        # Energy alignment
        energy_patterns = user_patterns.get('energy_patterns', {})
        energy_score = self._calculate_energy_alignment_score(candidate_time, energy_patterns, block)
        score += energy_score * self.constraint_weights['energy_alignment']
        
        return min(1.0, score)
    
    def _has_sufficient_time(self, slot_time: datetime, block: TimeBlock, 
                           existing_blocks: List[TimeBlock]) -> bool:
        """Check if a time slot has sufficient time for the block."""
        end_time = slot_time + timedelta(minutes=block.duration_minutes + block.buffer_time_minutes)
        
        for existing_block in existing_blocks:
            if (slot_time < existing_block.end_time and 
                end_time > existing_block.start_time):
                return False
        
        return True
    
    def _has_conflicts(self, block: TimeBlock, candidate_time: datetime,
                     existing_blocks: List[TimeBlock]) -> bool:
        """Check if placing a block at candidate time creates conflicts."""
        block_end = candidate_time + timedelta(minutes=block.duration_minutes)
        
        for existing_block in existing_blocks:
            if (candidate_time < existing_block.end_time and 
                block_end > existing_block.start_time):
                return True
        
        return False
    
    def _calculate_focus_time_score(self, candidate_time: datetime,
                                  focus_blocks: List[FocusTimeBlock]) -> float:
        """Calculate score for focus time alignment."""
        hour = candidate_time.hour
        
        for focus_block in focus_blocks:
            if focus_block.start_time.hour <= hour <= focus_block.end_time.hour:
                # Higher score for better quality focus times
                quality_scores = {
                    FocusTimeQuality.DEEP: 1.0,
                    FocusTimeQuality.MODERATE: 0.7,
                    FocusTimeQuality.SHALLOW: 0.4,
                    FocusTimeQuality.INTERRUPTED: 0.2
                }
                return quality_scores.get(focus_block.quality, 0.5)
        
        return 0.3  # Default score for non-focus times
    
    def _calculate_energy_alignment_score(self, candidate_time: datetime,
                                        energy_patterns: Dict[str, List[int]],
                                        block: TimeBlock) -> float:
        """Calculate score for energy level alignment."""
        hour = candidate_time.hour
        
        # Match task type to energy requirements
        high_energy_tasks = ['creative', 'analysis', 'deep_work', 'problem_solving']
        medium_energy_tasks = ['meeting', 'communication', 'planning']
        low_energy_tasks = ['administrative', 'email', 'routine']
        
        high_energy_hours = energy_patterns.get('high_energy', [])
        medium_energy_hours = energy_patterns.get('medium_energy', [])
        low_energy_hours = energy_patterns.get('low_energy', [])
        
        if block.task_type in high_energy_tasks:
            return 1.0 if hour in high_energy_hours else 0.5
        elif block.task_type in medium_energy_tasks:
            return 1.0 if hour in medium_energy_hours else 0.7
        elif block.task_type in low_energy_tasks:
            return 1.0 if hour in low_energy_hours else 0.8
        else:
            return 0.7  # Default score
    
    def _detect_conflicts(self, existing_blocks: List[TimeBlock], 
                        new_block: TimeBlock) -> List[ScheduleConflict]:
        """Detect conflicts between existing blocks and a new block."""
        conflicts = []
        
        for existing_block in existing_blocks:
            if self._blocks_overlap(existing_block, new_block):
                conflict = ScheduleConflict(
                    conflict_id=f"conflict_{datetime.now().timestamp()}",
                    conflicting_blocks=[existing_block, new_block],
                    conflict_type='overlap',
                    severity=self._calculate_conflict_severity(existing_block, new_block),
                    suggested_resolutions=self._generate_conflict_resolutions(existing_block, new_block)
                )
                conflicts.append(conflict)
        
        return conflicts
    
    def _blocks_overlap(self, block1: TimeBlock, block2: TimeBlock) -> bool:
        """Check if two time blocks overlap."""
        return (block1.start_time < block2.end_time and 
                block1.end_time > block2.start_time)
    
    def _calculate_conflict_severity(self, block1: TimeBlock, block2: TimeBlock) -> int:
        """Calculate severity of conflict between two blocks."""
        # Higher priority conflicts are more severe
        priority_factor = (block1.priority.value + block2.priority.value) / 2
        
        # Focus time conflicts are more severe
        focus_factor = 2 if (block1.is_focus_time or block2.is_focus_time) else 1
        
        # Habit conflicts are more severe
        habit_factor = 2 if (block1.is_habit or block2.is_habit) else 1
        
        severity = int(priority_factor * focus_factor * habit_factor)
        return min(10, max(1, severity))
    
    def _generate_conflict_resolutions(self, block1: TimeBlock, 
                                     block2: TimeBlock) -> List[Dict[str, Any]]:
        """Generate suggested resolutions for a conflict."""
        resolutions = []
        
        # Reschedule lower priority block
        lower_priority_block = block1 if block1.priority.value < block2.priority.value else block2
        resolutions.append({
            'strategy': 'reschedule_lower_priority',
            'description': f'Reschedule "{lower_priority_block.title}" to a different time',
            'affected_block': lower_priority_block.id
        })
        
        # Split longer task
        longer_block = block1 if block1.duration_minutes > block2.duration_minutes else block2
        if longer_block.duration_minutes > 60:
            resolutions.append({
                'strategy': 'split_task',
                'description': f'Split "{longer_block.title}" into smaller chunks',
                'affected_block': longer_block.id
            })
        
        # Suggest alternative times
        resolutions.append({
            'strategy': 'suggest_alternative_time',
            'description': 'Find alternative time slots for one of the tasks',
            'affected_blocks': [block1.id, block2.id]
        })
        
        return resolutions
    
    def _detect_all_conflicts(self, blocks: List[TimeBlock]) -> List[ScheduleConflict]:
        """Detect all conflicts in a list of time blocks."""
        conflicts = []
        
        for i, block1 in enumerate(blocks):
            for j, block2 in enumerate(blocks[i+1:], i+1):
                if self._blocks_overlap(block1, block2):
                    conflict = ScheduleConflict(
                        conflict_id=f"conflict_{i}_{j}",
                        conflicting_blocks=[block1, block2],
                        conflict_type='overlap',
                        severity=self._calculate_conflict_severity(block1, block2),
                        suggested_resolutions=self._generate_conflict_resolutions(block1, block2)
                    )
                    conflicts.append(conflict)
        
        return conflicts
    
    def _calculate_optimization_score(
        self,
        blocks: List[TimeBlock],
        focus_blocks: List[FocusTimeBlock],
        habit_rules: List[HabitDefenseRule],
        user_patterns: Dict[str, Any]
    ) -> float:
        """Calculate overall optimization score for the schedule."""
        if not blocks:
            return 0.0
        
        total_score = 0.0
        
        # Priority alignment score
        priority_score = sum(block.priority.value for block in blocks) / (len(blocks) * 5)
        total_score += priority_score * self.constraint_weights['priority_alignment']
        
        # Focus time protection score
        focus_score = 1.0 if self._check_focus_time_protection(blocks, focus_blocks) else 0.5
        total_score += focus_score * self.constraint_weights['focus_time_protection']
        
        # Habit preservation score
        habit_score = 1.0 if self._check_habits_preserved(blocks, habit_rules) else 0.5
        total_score += habit_score * self.constraint_weights['habit_preservation']
        
        # Conflict minimization score
        conflicts = self._detect_all_conflicts(blocks)
        conflict_score = 1.0 - (len(conflicts) / max(len(blocks), 1))
        total_score += conflict_score * self.constraint_weights['conflict_minimization']
        
        return min(1.0, total_score)
    
    def _check_focus_time_protection(self, blocks: List[TimeBlock],
                                   focus_blocks: List[FocusTimeBlock]) -> bool:
        """Check if focus time is properly protected."""
        for focus_block in focus_blocks:
            focus_start = focus_block.start_time
            focus_end = focus_block.end_time
            
            # Check if any non-focus blocks overlap with focus time
            for block in blocks:
                if not block.is_focus_time:
                    block_start = block.start_time.time()
                    block_end = block.end_time.time()
                    
                    if (block_start < focus_end and block_end > focus_start):
                        return False
        
        return True
    
    def _check_habits_preserved(self, blocks: List[TimeBlock],
                              habit_rules: List[HabitDefenseRule]) -> bool:
        """Check if important habits are preserved."""
        for habit_rule in habit_rules:
            habit_blocks = [b for b in blocks if b.is_habit and habit_rule.habit_name in b.title.lower()]
            
            if not habit_blocks:
                return False  # Habit not scheduled
        
        return True
    
    async def _apply_conflict_resolution(
        self,
        schedule: GeneratedSchedule,
        new_block: TimeBlock,
        conflicts: List[ScheduleConflict],
        strategy: ConflictResolutionStrategy
    ) -> GeneratedSchedule:
        """Apply conflict resolution strategy."""
        
        if strategy == ConflictResolutionStrategy.RESCHEDULE_LOWER_PRIORITY:
            return await self._reschedule_lower_priority(schedule, new_block, conflicts)
        elif strategy == ConflictResolutionStrategy.SPLIT_TASK:
            return await self._split_conflicting_task(schedule, new_block, conflicts)
        elif strategy == ConflictResolutionStrategy.SUGGEST_ALTERNATIVE_TIME:
            return await self._suggest_alternative_times(schedule, new_block, conflicts)
        elif strategy == ConflictResolutionStrategy.DEFER_TO_NEXT_DAY:
            return await self._defer_to_next_day(schedule, new_block, conflicts)
        else:
            # Default: reschedule lower priority
            return await self._reschedule_lower_priority(schedule, new_block, conflicts)
    
    async def _reschedule_lower_priority(
        self,
        schedule: GeneratedSchedule,
        new_block: TimeBlock,
        conflicts: List[ScheduleConflict]
    ) -> GeneratedSchedule:
        """Reschedule lower priority conflicting blocks."""
        
        for conflict in conflicts:
            conflicting_blocks = conflict.conflicting_blocks
            
            # Find lower priority block
            lower_priority_block = min(conflicting_blocks, key=lambda x: x.priority.value)
            
            if lower_priority_block != new_block:
                # Remove from current position
                schedule.time_blocks.remove(lower_priority_block)
                
                # Find new time slot
                new_time = self._find_alternative_time_slot(lower_priority_block, schedule.time_blocks)
                
                if new_time:
                    lower_priority_block.start_time = new_time
                    lower_priority_block.end_time = new_time + timedelta(minutes=lower_priority_block.duration_minutes)
                    schedule.time_blocks.append(lower_priority_block)
        
        # Add new block
        schedule.time_blocks.append(new_block)
        
        return schedule
    
    def _find_alternative_time_slot(self, block: TimeBlock, 
                                  existing_blocks: List[TimeBlock]) -> Optional[datetime]:
        """Find alternative time slot for a block."""
        # Simple implementation - find next available slot
        current_time = datetime.now().replace(minute=0, second=0, microsecond=0)
        
        for hour_offset in range(24 * 7):  # Search for a week
            candidate_time = current_time + timedelta(hours=hour_offset)
            
            # Check if this time works
            if self._has_sufficient_time(candidate_time, block, existing_blocks):
                return candidate_time
        
        return None
    
    async def _reoptimize_schedule(self, schedule: GeneratedSchedule) -> GeneratedSchedule:
        """Re-optimize schedule after changes."""
        # Simple re-optimization - recalculate scores and conflicts
        schedule.conflicts = self._detect_all_conflicts(schedule.time_blocks)
        schedule.optimization_score = self._calculate_optimization_score(
            schedule.time_blocks, [], [], {}
        )
        
        return schedule
    
    def get_schedule_stats(self) -> Dict[str, Any]:
        """Get schedule generation statistics."""
        return {
            'cached_schedules': len(self.schedule_cache),
            'max_optimization_iterations': self.max_optimization_iterations,
            'min_optimization_score': self.min_optimization_score,
            'constraint_weights': self.constraint_weights,
            'supported_schedule_types': [t.value for t in ScheduleType],
            'supported_priorities': [p.value for p in TaskPriority],
            'conflict_resolution_strategies': [s.value for s in ConflictResolutionStrategy]
        }