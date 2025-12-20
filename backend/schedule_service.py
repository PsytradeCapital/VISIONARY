import uuid
from datetime import datetime, timedelta, time
from typing import Dict, List, Any, Optional, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_
from models import Schedule, ScheduleBlock
from database import Vision, UserProfile
from ai_service import ai_service
import logging
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)

class TimeFrame(Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"

@dataclass
class TimeSlot:
    start_time: datetime
    end_time: datetime
    available: bool = True
    priority: int = 1

@dataclass
class ScheduleConstraint:
    type: str  # 'time_block', 'duration_limit', 'category_limit'
    parameters: Dict[str, Any]

class ScheduleGenerationService:
    """Service for creating and managing flexible schedules based on AI insights"""
    
    def __init__(self):
        self.default_time_blocks = {
            'morning': (6, 12),    # 6 AM - 12 PM
            'afternoon': (12, 18), # 12 PM - 6 PM
            'evening': (18, 22)    # 6 PM - 10 PM
        }
        
        self.category_durations = {
            'health': 60,        # 1 hour default
            'nutrition': 30,     # 30 minutes
            'financial': 45,     # 45 minutes
            'psychological': 20, # 20 minutes
            'task': 60          # 1 hour
        }
        
        self.priority_weights = {
            1: 0.5,  # Low priority
            2: 1.0,  # Medium priority
            3: 1.5,  # High priority
            4: 2.0,  # Critical priority
            5: 3.0   # Urgent priority
        }
    
    async def generate_schedule(
        self, 
        user_id: str, 
        timeframe: TimeFrame, 
        preferences: Dict[str, Any],
        db: AsyncSession
    ) -> Dict[str, Any]:
        """Generate a personalized schedule based on AI insights and user preferences"""
        try:
            # Get user patterns and preferences
            patterns = await ai_service.analyze_user_patterns(user_id, db)
            user_visions = await self._get_user_visions(user_id, db)
            
            # Determine schedule period
            start_date, end_date = self._get_schedule_period(timeframe, preferences)
            
            # Generate time slots
            available_slots = self._generate_time_slots(start_date, end_date, timeframe)
            
            # Get activities from visions and patterns
            activities = await self._generate_activities_from_visions(user_visions, patterns)
            
            # Apply constraints
            constraints = self._build_constraints(preferences, patterns)
            
            # Optimize schedule
            optimized_blocks = self._optimize_schedule(activities, available_slots, constraints, patterns)
            
            # Create schedule record
            schedule = Schedule(
                user_id=uuid.UUID(user_id),
                title=f"{timeframe.value.title()} Schedule - {start_date.strftime('%Y-%m-%d')}",
                timeframe=timeframe.value,
                start_date=start_date,
                end_date=end_date,
                flexibility_options=preferences.get('flexibility', {}),
                status='active'
            )
            
            db.add(schedule)
            await db.flush()  # Get the schedule ID
            
            # Create schedule blocks
            schedule_blocks = []
            for block_data in optimized_blocks:
                block = ScheduleBlock(
                    schedule_id=schedule.id,
                    title=block_data['title'],
                    description=block_data.get('description'),
                    start_time=block_data['start_time'],
                    end_time=block_data['end_time'],
                    category=block_data['category'],
                    priority=block_data['priority'],
                    flexibility=block_data.get('flexibility', {}),
                    related_vision_id=block_data.get('vision_id'),
                    alternatives=block_data.get('alternatives', [])
                )
                schedule_blocks.append(block)
                db.add(block)
            
            await db.commit()
            
            return {
                'schedule_id': str(schedule.id),
                'title': schedule.title,
                'timeframe': schedule.timeframe,
                'start_date': schedule.start_date,
                'end_date': schedule.end_date,
                'blocks': [self._serialize_block(block) for block in schedule_blocks],
                'goal_alignment': self._calculate_goal_alignment(schedule_blocks, user_visions),
                'flexibility_score': self._calculate_flexibility_score(schedule_blocks)
            }
            
        except Exception as e:
            logger.error(f"Error generating schedule: {str(e)}")
            await db.rollback()
            raise
    
    async def update_schedule(
        self, 
        schedule_id: str, 
        modifications: List[Dict[str, Any]], 
        db: AsyncSession
    ) -> Dict[str, Any]:
        """Update an existing schedule with modifications"""
        try:
            # Get existing schedule
            schedule_query = select(Schedule).where(Schedule.id == uuid.UUID(schedule_id))
            schedule_result = await db.execute(schedule_query)
            schedule = schedule_result.scalar_one_or_none()
            
            if not schedule:
                raise ValueError(f"Schedule {schedule_id} not found")
            
            # Get existing blocks
            blocks_query = select(ScheduleBlock).where(ScheduleBlock.schedule_id == schedule.id)
            blocks_result = await db.execute(blocks_query)
            existing_blocks = blocks_result.scalars().all()
            
            # Apply modifications
            updated_blocks = []
            for modification in modifications:
                mod_type = modification.get('type')
                
                if mod_type == 'update_block':
                    block_id = modification.get('block_id')
                    updates = modification.get('updates', {})
                    
                    for block in existing_blocks:
                        if str(block.id) == block_id:
                            for key, value in updates.items():
                                if hasattr(block, key):
                                    setattr(block, key, value)
                            block.updated_at = datetime.utcnow()
                            updated_blocks.append(block)
                
                elif mod_type == 'add_block':
                    new_block_data = modification.get('block_data', {})
                    new_block = ScheduleBlock(
                        schedule_id=schedule.id,
                        **new_block_data
                    )
                    db.add(new_block)
                    updated_blocks.append(new_block)
                
                elif mod_type == 'delete_block':
                    block_id = modification.get('block_id')
                    for block in existing_blocks:
                        if str(block.id) == block_id:
                            await db.delete(block)
            
            schedule.updated_at = datetime.utcnow()
            await db.commit()
            
            # Return updated schedule
            all_blocks_query = select(ScheduleBlock).where(ScheduleBlock.schedule_id == schedule.id)
            all_blocks_result = await db.execute(all_blocks_query)
            all_blocks = all_blocks_result.scalars().all()
            
            return {
                'schedule_id': str(schedule.id),
                'blocks': [self._serialize_block(block) for block in all_blocks],
                'updated_at': schedule.updated_at
            }
            
        except Exception as e:
            logger.error(f"Error updating schedule: {str(e)}")
            await db.rollback()
            raise
    
    async def suggest_alternatives(
        self, 
        schedule_id: str, 
        disruption: Dict[str, Any], 
        db: AsyncSession
    ) -> List[Dict[str, Any]]:
        """Suggest alternatives when plans are disrupted"""
        try:
            # Get affected schedule blocks
            affected_blocks = await self._get_affected_blocks(schedule_id, disruption, db)
            
            alternatives = []
            
            for block in affected_blocks:
                block_alternatives = []
                
                # Time-based alternatives
                if disruption.get('type') == 'time_conflict':
                    time_alternatives = self._generate_time_alternatives(block, disruption)
                    block_alternatives.extend(time_alternatives)
                
                # Activity-based alternatives
                if disruption.get('type') == 'activity_unavailable':
                    activity_alternatives = self._generate_activity_alternatives(block, disruption)
                    block_alternatives.extend(activity_alternatives)
                
                # Weather-based alternatives
                if disruption.get('type') == 'weather':
                    weather_alternatives = self._generate_weather_alternatives(block, disruption)
                    block_alternatives.extend(weather_alternatives)
                
                alternatives.append({
                    'block_id': str(block.id),
                    'original_title': block.title,
                    'alternatives': block_alternatives
                })
            
            return alternatives
            
        except Exception as e:
            logger.error(f"Error suggesting alternatives: {str(e)}")
            return []
    
    async def optimize_schedule(self, schedule_id: str, db: AsyncSession) -> Dict[str, Any]:
        """Optimize an existing schedule for better efficiency"""
        try:
            # Get schedule and blocks
            schedule_query = select(Schedule).where(Schedule.id == uuid.UUID(schedule_id))
            schedule_result = await db.execute(schedule_query)
            schedule = schedule_result.scalar_one_or_none()
            
            if not schedule:
                raise ValueError(f"Schedule {schedule_id} not found")
            
            blocks_query = select(ScheduleBlock).where(ScheduleBlock.schedule_id == schedule.id)
            blocks_result = await db.execute(blocks_query)
            blocks = blocks_result.scalars().all()
            
            # Analyze current schedule efficiency
            efficiency_score = self._calculate_efficiency_score(blocks)
            
            # Generate optimization suggestions
            optimizations = []
            
            # Time gap optimization
            time_gaps = self._find_time_gaps(blocks)
            if time_gaps:
                optimizations.append({
                    'type': 'time_gap_optimization',
                    'description': f"Found {len(time_gaps)} time gaps that could be better utilized",
                    'suggestions': self._suggest_gap_fillers(time_gaps)
                })
            
            # Priority reordering
            priority_issues = self._analyze_priority_ordering(blocks)
            if priority_issues:
                optimizations.append({
                    'type': 'priority_reordering',
                    'description': 'Some high-priority tasks are scheduled at suboptimal times',
                    'suggestions': priority_issues
                })
            
            # Category balancing
            category_balance = self._analyze_category_balance(blocks)
            if category_balance['needs_rebalancing']:
                optimizations.append({
                    'type': 'category_balancing',
                    'description': 'Schedule could benefit from better category distribution',
                    'suggestions': category_balance['suggestions']
                })
            
            return {
                'current_efficiency': efficiency_score,
                'optimizations': optimizations,
                'estimated_improvement': self._estimate_improvement(optimizations)
            }
            
        except Exception as e:
            logger.error(f"Error optimizing schedule: {str(e)}")
            return {'error': str(e)}
    
    def _get_schedule_period(self, timeframe: TimeFrame, preferences: Dict[str, Any]) -> Tuple[datetime, datetime]:
        """Determine start and end dates for the schedule"""
        now = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        
        if timeframe == TimeFrame.DAILY:
            start_date = preferences.get('start_date', now)
            if isinstance(start_date, str):
                start_date = datetime.fromisoformat(start_date)
            end_date = start_date + timedelta(days=1)
        
        elif timeframe == TimeFrame.WEEKLY:
            # Start from Monday of current week
            days_since_monday = now.weekday()
            start_date = now - timedelta(days=days_since_monday)
            end_date = start_date + timedelta(days=7)
        
        elif timeframe == TimeFrame.MONTHLY:
            # Start from first day of current month
            start_date = now.replace(day=1)
            if start_date.month == 12:
                end_date = start_date.replace(year=start_date.year + 1, month=1)
            else:
                end_date = start_date.replace(month=start_date.month + 1)
        
        return start_date, end_date
    
    def _generate_time_slots(self, start_date: datetime, end_date: datetime, timeframe: TimeFrame) -> List[TimeSlot]:
        """Generate available time slots for the schedule period"""
        slots = []
        current_date = start_date
        
        while current_date < end_date:
            # Generate slots for each day
            for period, (start_hour, end_hour) in self.default_time_blocks.items():
                slot_start = current_date.replace(hour=start_hour, minute=0)
                slot_end = current_date.replace(hour=end_hour, minute=0)
                
                slots.append(TimeSlot(
                    start_time=slot_start,
                    end_time=slot_end,
                    available=True,
                    priority=2  # Default medium priority
                ))
            
            current_date += timedelta(days=1)
        
        return slots
    
    async def _get_user_visions(self, user_id: str, db: AsyncSession) -> List[Vision]:
        """Get user's active visions"""
        visions_query = select(Vision).where(
            and_(
                Vision.user_id == uuid.UUID(user_id),
                Vision.status == 'active'
            )
        )
        visions_result = await db.execute(visions_query)
        return visions_result.scalars().all()
    
    async def _generate_activities_from_visions(self, visions: List[Vision], patterns: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate schedule activities based on user visions and patterns"""
        activities = []
        
        for vision in visions:
            # Create activities based on vision category
            if vision.category == 'health':
                activities.extend([
                    {
                        'title': 'Morning Workout',
                        'category': 'health',
                        'duration': 60,
                        'priority': vision.priority,
                        'vision_id': str(vision.id),
                        'preferred_time': 'morning',
                        'flexibility': {'time_flexible': True, 'duration_flexible': True}
                    },
                    {
                        'title': 'Health Check Progress',
                        'category': 'health',
                        'duration': 15,
                        'priority': vision.priority,
                        'vision_id': str(vision.id),
                        'preferred_time': 'evening',
                        'flexibility': {'time_flexible': True, 'duration_flexible': False}
                    }
                ])
            
            elif vision.category == 'financial':
                activities.append({
                    'title': 'Budget Review',
                    'category': 'financial',
                    'duration': 30,
                    'priority': vision.priority,
                    'vision_id': str(vision.id),
                    'preferred_time': 'evening',
                    'flexibility': {'time_flexible': True, 'duration_flexible': True}
                })
            
            elif vision.category == 'nutrition':
                activities.extend([
                    {
                        'title': 'Meal Planning',
                        'category': 'nutrition',
                        'duration': 20,
                        'priority': vision.priority,
                        'vision_id': str(vision.id),
                        'preferred_time': 'morning',
                        'flexibility': {'time_flexible': True, 'duration_flexible': True}
                    },
                    {
                        'title': 'Healthy Meal Prep',
                        'category': 'nutrition',
                        'duration': 45,
                        'priority': vision.priority,
                        'vision_id': str(vision.id),
                        'preferred_time': 'afternoon',
                        'flexibility': {'time_flexible': False, 'duration_flexible': True}
                    }
                ])
            
            elif vision.category == 'psychological':
                activities.append({
                    'title': 'Meditation Session',
                    'category': 'psychological',
                    'duration': 20,
                    'priority': vision.priority,
                    'vision_id': str(vision.id),
                    'preferred_time': 'morning',
                    'flexibility': {'time_flexible': True, 'duration_flexible': False}
                })
        
        return activities
    
    def _build_constraints(self, preferences: Dict[str, Any], patterns: Dict[str, Any]) -> List[ScheduleConstraint]:
        """Build scheduling constraints from preferences and patterns"""
        constraints = []
        
        # Time block constraints
        if 'unavailable_times' in preferences:
            for unavailable in preferences['unavailable_times']:
                constraints.append(ScheduleConstraint(
                    type='time_block',
                    parameters={
                        'start_time': unavailable['start'],
                        'end_time': unavailable['end'],
                        'blocked': True
                    }
                ))
        
        # Duration limits
        if 'max_daily_hours' in preferences:
            constraints.append(ScheduleConstraint(
                type='duration_limit',
                parameters={
                    'max_hours_per_day': preferences['max_daily_hours'],
                    'scope': 'daily'
                }
            ))
        
        # Category limits
        goal_priorities = patterns.get('goal_priorities', [])
        for priority in goal_priorities:
            if priority['priority_score'] > 0.7:  # High priority categories
                constraints.append(ScheduleConstraint(
                    type='category_limit',
                    parameters={
                        'category': priority['category'],
                        'min_weekly_hours': 3,  # Ensure minimum time for high-priority categories
                        'preferred_distribution': 'spread'  # Spread across multiple days
                    }
                ))
        
        return constraints
    
    def _optimize_schedule(
        self, 
        activities: List[Dict[str, Any]], 
        time_slots: List[TimeSlot], 
        constraints: List[ScheduleConstraint],
        patterns: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Optimize schedule using constraint satisfaction and priority weighting"""
        
        # Sort activities by priority and user patterns
        sorted_activities = self._sort_activities_by_priority(activities, patterns)
        
        scheduled_blocks = []
        used_slots = set()
        
        for activity in sorted_activities:
            best_slot = self._find_best_slot(activity, time_slots, used_slots, constraints, patterns)
            
            if best_slot:
                # Create schedule block
                duration_minutes = activity['duration']
                end_time = best_slot.start_time + timedelta(minutes=duration_minutes)
                
                # Ensure we don't exceed the slot boundary
                if end_time > best_slot.end_time:
                    end_time = best_slot.end_time
                
                block = {
                    'title': activity['title'],
                    'description': f"Scheduled {activity['category']} activity",
                    'start_time': best_slot.start_time,
                    'end_time': end_time,
                    'category': activity['category'],
                    'priority': activity['priority'],
                    'flexibility': activity.get('flexibility', {}),
                    'vision_id': activity.get('vision_id'),
                    'alternatives': self._generate_block_alternatives(activity, time_slots, used_slots)
                }
                
                scheduled_blocks.append(block)
                used_slots.add(id(best_slot))
        
        return scheduled_blocks
    
    def _sort_activities_by_priority(self, activities: List[Dict[str, Any]], patterns: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Sort activities by priority, considering user patterns"""
        goal_priorities = {gp['category']: gp['priority_score'] for gp in patterns.get('goal_priorities', [])}
        
        def activity_score(activity):
            base_priority = self.priority_weights.get(activity['priority'], 1.0)
            pattern_boost = goal_priorities.get(activity['category'], 0.5)
            return base_priority * (1 + pattern_boost)
        
        return sorted(activities, key=activity_score, reverse=True)
    
    def _find_best_slot(
        self, 
        activity: Dict[str, Any], 
        time_slots: List[TimeSlot], 
        used_slots: set,
        constraints: List[ScheduleConstraint],
        patterns: Dict[str, Any]
    ) -> Optional[TimeSlot]:
        """Find the best available time slot for an activity"""
        
        preferred_time = activity.get('preferred_time', 'any')
        duration = activity['duration']
        
        # Filter available slots
        available_slots = [
            slot for slot in time_slots 
            if id(slot) not in used_slots and slot.available
        ]
        
        # Apply time preference filtering
        if preferred_time != 'any':
            preferred_slots = []
            for slot in available_slots:
                slot_hour = slot.start_time.hour
                
                if preferred_time == 'morning' and 6 <= slot_hour < 12:
                    preferred_slots.append(slot)
                elif preferred_time == 'afternoon' and 12 <= slot_hour < 18:
                    preferred_slots.append(slot)
                elif preferred_time == 'evening' and 18 <= slot_hour < 22:
                    preferred_slots.append(slot)
            
            if preferred_slots:
                available_slots = preferred_slots
        
        # Check constraints
        valid_slots = []
        for slot in available_slots:
            if self._check_constraints(slot, activity, constraints):
                # Check if activity fits in the slot
                required_duration = timedelta(minutes=duration)
                if slot.end_time - slot.start_time >= required_duration:
                    valid_slots.append(slot)
        
        if not valid_slots:
            return None
        
        # Score slots based on various factors
        scored_slots = []
        for slot in valid_slots:
            score = self._calculate_slot_score(slot, activity, patterns)
            scored_slots.append((slot, score))
        
        # Return the highest-scored slot
        scored_slots.sort(key=lambda x: x[1], reverse=True)
        return scored_slots[0][0] if scored_slots else None
    
    def _check_constraints(self, slot: TimeSlot, activity: Dict[str, Any], constraints: List[ScheduleConstraint]) -> bool:
        """Check if a slot satisfies all constraints for an activity"""
        for constraint in constraints:
            if constraint.type == 'time_block':
                params = constraint.parameters
                if params.get('blocked', False):
                    blocked_start = params['start_time']
                    blocked_end = params['end_time']
                    
                    # Check for overlap
                    if (slot.start_time < blocked_end and slot.end_time > blocked_start):
                        return False
        
        return True
    
    def _calculate_slot_score(self, slot: TimeSlot, activity: Dict[str, Any], patterns: Dict[str, Any]) -> float:
        """Calculate a score for how well a slot fits an activity"""
        score = 1.0
        
        # Time preference bonus
        preferred_time = activity.get('preferred_time', 'any')
        slot_hour = slot.start_time.hour
        
        if preferred_time == 'morning' and 6 <= slot_hour < 12:
            score += 0.5
        elif preferred_time == 'afternoon' and 12 <= slot_hour < 18:
            score += 0.5
        elif preferred_time == 'evening' and 18 <= slot_hour < 22:
            score += 0.5
        
        # Pattern-based bonus
        preferred_times = patterns.get('preferred_times', [])
        for pref in preferred_times:
            if (pref['activity_type'] == activity['category'] and 
                pref['period'] == preferred_time):
                score += pref['confidence'] * 0.3
        
        # Slot priority
        score += slot.priority * 0.2
        
        return score
    
    def _generate_block_alternatives(self, activity: Dict[str, Any], time_slots: List[TimeSlot], used_slots: set) -> List[Dict[str, Any]]:
        """Generate alternative options for a scheduled block"""
        alternatives = []
        
        # Find other suitable time slots
        available_slots = [
            slot for slot in time_slots 
            if id(slot) not in used_slots and slot.available
        ]
        
        for slot in available_slots[:3]:  # Top 3 alternatives
            alternatives.append({
                'type': 'time_change',
                'start_time': slot.start_time.isoformat(),
                'end_time': (slot.start_time + timedelta(minutes=activity['duration'])).isoformat(),
                'description': f"Move to {slot.start_time.strftime('%I:%M %p')}"
            })
        
        # Activity alternatives (if flexible)
        if activity.get('flexibility', {}).get('activity_flexible', False):
            alternatives.append({
                'type': 'activity_change',
                'description': f"Alternative {activity['category']} activity",
                'suggestions': [
                    f"Quick {activity['category']} session (15 min)",
                    f"Extended {activity['category']} session (90 min)"
                ]
            })
        
        return alternatives
    
    def _serialize_block(self, block: ScheduleBlock) -> Dict[str, Any]:
        """Serialize a schedule block for API response"""
        return {
            'id': str(block.id),
            'title': block.title,
            'description': block.description,
            'start_time': block.start_time.isoformat(),
            'end_time': block.end_time.isoformat(),
            'category': block.category,
            'priority': block.priority,
            'status': block.status,
            'flexibility': block.flexibility,
            'related_vision_id': str(block.related_vision_id) if block.related_vision_id else None,
            'alternatives': block.alternatives
        }
    
    def _calculate_goal_alignment(self, blocks: List[ScheduleBlock], visions: List[Vision]) -> Dict[str, Any]:
        """Calculate how well the schedule aligns with user goals"""
        vision_categories = {vision.category: vision.priority for vision in visions}
        block_categories = {}
        
        for block in blocks:
            category = block.category
            duration = (block.end_time - block.start_time).total_seconds() / 3600  # hours
            
            if category in block_categories:
                block_categories[category] += duration
            else:
                block_categories[category] = duration
        
        alignment_scores = {}
        for category, vision_priority in vision_categories.items():
            scheduled_hours = block_categories.get(category, 0)
            # Simple alignment calculation - could be more sophisticated
            alignment_scores[category] = min(1.0, scheduled_hours * vision_priority / 10)
        
        overall_alignment = sum(alignment_scores.values()) / len(alignment_scores) if alignment_scores else 0
        
        return {
            'overall_score': overall_alignment,
            'category_scores': alignment_scores,
            'total_scheduled_hours': sum(block_categories.values())
        }
    
    def _calculate_flexibility_score(self, blocks: List[ScheduleBlock]) -> float:
        """Calculate the flexibility score of the schedule"""
        if not blocks:
            return 0.0
        
        flexible_blocks = 0
        for block in blocks:
            flexibility = block.flexibility or {}
            if (flexibility.get('time_flexible', False) or 
                flexibility.get('duration_flexible', False)):
                flexible_blocks += 1
        
        return flexible_blocks / len(blocks)
    
    # Additional helper methods for optimization and alternatives...
    
    async def _get_affected_blocks(self, schedule_id: str, disruption: Dict[str, Any], db: AsyncSession) -> List[ScheduleBlock]:
        """Get schedule blocks affected by a disruption"""
        # Implementation depends on disruption type
        blocks_query = select(ScheduleBlock).where(ScheduleBlock.schedule_id == uuid.UUID(schedule_id))
        blocks_result = await db.execute(blocks_query)
        return blocks_result.scalars().all()
    
    def _generate_time_alternatives(self, block: ScheduleBlock, disruption: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate time-based alternatives for a disrupted block"""
        alternatives = []
        
        # Suggest moving to different time slots
        original_duration = block.end_time - block.start_time
        
        # Earlier time
        earlier_start = block.start_time - timedelta(hours=2)
        alternatives.append({
            'type': 'time_shift',
            'description': f"Move to {earlier_start.strftime('%I:%M %p')}",
            'start_time': earlier_start.isoformat(),
            'end_time': (earlier_start + original_duration).isoformat()
        })
        
        # Later time
        later_start = block.start_time + timedelta(hours=2)
        alternatives.append({
            'type': 'time_shift',
            'description': f"Move to {later_start.strftime('%I:%M %p')}",
            'start_time': later_start.isoformat(),
            'end_time': (later_start + original_duration).isoformat()
        })
        
        return alternatives
    
    def _generate_activity_alternatives(self, block: ScheduleBlock, disruption: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate activity-based alternatives"""
        alternatives = []
        
        category = block.category
        
        if category == 'health':
            alternatives.extend([
                {'type': 'activity_substitute', 'description': 'Indoor workout instead of outdoor run'},
                {'type': 'activity_substitute', 'description': 'Yoga session instead of gym workout'},
                {'type': 'activity_substitute', 'description': 'Walking meeting instead of stationary exercise'}
            ])
        elif category == 'nutrition':
            alternatives.extend([
                {'type': 'activity_substitute', 'description': 'Quick healthy snack prep instead of full meal'},
                {'type': 'activity_substitute', 'description': 'Meal delivery order with healthy options'}
            ])
        
        return alternatives
    
    def _generate_weather_alternatives(self, block: ScheduleBlock, disruption: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate weather-appropriate alternatives"""
        weather_condition = disruption.get('weather_condition', 'unknown')
        alternatives = []
        
        if weather_condition in ['rain', 'storm']:
            if block.category == 'health':
                alternatives.append({
                    'type': 'weather_alternative',
                    'description': 'Indoor workout due to rain',
                    'location': 'indoor'
                })
        elif weather_condition in ['snow', 'ice']:
            alternatives.append({
                'type': 'weather_alternative', 
                'description': 'Work from home option due to weather',
                'location': 'home'
            })
        
        return alternatives
    
    def _calculate_efficiency_score(self, blocks: List[ScheduleBlock]) -> float:
        """Calculate the efficiency score of a schedule"""
        if not blocks:
            return 0.0
        
        # Simple efficiency calculation based on time utilization and priority distribution
        total_time = sum((block.end_time - block.start_time).total_seconds() for block in blocks)
        high_priority_time = sum(
            (block.end_time - block.start_time).total_seconds() 
            for block in blocks if block.priority >= 3
        )
        
        priority_ratio = high_priority_time / total_time if total_time > 0 else 0
        
        # Check for time gaps (inefficiency indicator)
        sorted_blocks = sorted(blocks, key=lambda b: b.start_time)
        gap_penalty = 0
        
        for i in range(len(sorted_blocks) - 1):
            current_end = sorted_blocks[i].end_time
            next_start = sorted_blocks[i + 1].start_time
            gap_duration = (next_start - current_end).total_seconds() / 3600  # hours
            
            if gap_duration > 0.5:  # Gaps longer than 30 minutes
                gap_penalty += gap_duration * 0.1
        
        efficiency = priority_ratio - gap_penalty
        return max(0.0, min(1.0, efficiency))
    
    def _find_time_gaps(self, blocks: List[ScheduleBlock]) -> List[Dict[str, Any]]:
        """Find time gaps in the schedule"""
        if not blocks:
            return []
        
        sorted_blocks = sorted(blocks, key=lambda b: b.start_time)
        gaps = []
        
        for i in range(len(sorted_blocks) - 1):
            current_end = sorted_blocks[i].end_time
            next_start = sorted_blocks[i + 1].start_time
            gap_duration = next_start - current_end
            
            if gap_duration.total_seconds() > 1800:  # Gaps longer than 30 minutes
                gaps.append({
                    'start_time': current_end,
                    'end_time': next_start,
                    'duration_minutes': gap_duration.total_seconds() / 60
                })
        
        return gaps
    
    def _suggest_gap_fillers(self, gaps: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Suggest activities to fill time gaps"""
        suggestions = []
        
        for gap in gaps:
            duration_minutes = gap['duration_minutes']
            
            if duration_minutes >= 60:
                suggestions.append({
                    'gap_start': gap['start_time'].isoformat(),
                    'suggestion': 'Add a focused work session or skill development activity',
                    'duration': 60
                })
            elif duration_minutes >= 30:
                suggestions.append({
                    'gap_start': gap['start_time'].isoformat(),
                    'suggestion': 'Add a quick exercise or meditation session',
                    'duration': 30
                })
            elif duration_minutes >= 15:
                suggestions.append({
                    'gap_start': gap['start_time'].isoformat(),
                    'suggestion': 'Add a brief planning or reflection activity',
                    'duration': 15
                })
        
        return suggestions
    
    def _analyze_priority_ordering(self, blocks: List[ScheduleBlock]) -> List[Dict[str, Any]]:
        """Analyze if high-priority tasks are optimally scheduled"""
        issues = []
        
        # Check if high-priority tasks are scheduled during low-energy times
        for block in blocks:
            if block.priority >= 4:  # High priority
                hour = block.start_time.hour
                
                # Assuming low-energy times are late evening (after 8 PM) or very early morning (before 6 AM)
                if hour >= 20 or hour < 6:
                    issues.append({
                        'block_id': str(block.id),
                        'issue': 'High-priority task scheduled during low-energy time',
                        'suggestion': 'Consider moving to morning or afternoon slot',
                        'current_time': block.start_time.strftime('%I:%M %p')
                    })
        
        return issues
    
    def _analyze_category_balance(self, blocks: List[ScheduleBlock]) -> Dict[str, Any]:
        """Analyze if schedule has good category balance"""
        category_hours = defaultdict(float)
        
        for block in blocks:
            duration_hours = (block.end_time - block.start_time).total_seconds() / 3600
            category_hours[block.category] += duration_hours
        
        total_hours = sum(category_hours.values())
        
        # Check for imbalances
        needs_rebalancing = False
        suggestions = []
        
        for category, hours in category_hours.items():
            percentage = (hours / total_hours) * 100 if total_hours > 0 else 0
            
            if category in ['health', 'psychological'] and percentage < 10:
                needs_rebalancing = True
                suggestions.append(f"Consider adding more {category} activities (currently {percentage:.1f}%)")
            elif category == 'task' and percentage > 70:
                needs_rebalancing = True
                suggestions.append(f"Too much time on tasks ({percentage:.1f}%), consider adding personal development activities")
        
        return {
            'needs_rebalancing': needs_rebalancing,
            'category_distribution': dict(category_hours),
            'suggestions': suggestions
        }
    
    def _estimate_improvement(self, optimizations: List[Dict[str, Any]]) -> float:
        """Estimate potential improvement from optimizations"""
        improvement_score = 0.0
        
        for optimization in optimizations:
            if optimization['type'] == 'time_gap_optimization':
                improvement_score += 0.15  # 15% improvement from better time utilization
            elif optimization['type'] == 'priority_reordering':
                improvement_score += 0.20  # 20% improvement from better priority scheduling
            elif optimization['type'] == 'category_balancing':
                improvement_score += 0.10  # 10% improvement from better balance
        
        return min(0.50, improvement_score)  # Cap at 50% improvement

# Global schedule service instance
schedule_service = ScheduleGenerationService()