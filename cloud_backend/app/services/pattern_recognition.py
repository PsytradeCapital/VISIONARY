"""
Pattern recognition service with focus time protection.

Implements Reclaim AI-inspired pattern analysis with cloud ML,
focus time protection algorithms, and autonomous scheduling adjustments.
"""

import json
import logging
from typing import Dict, List, Optional, Tuple, Any, Set
from datetime import datetime, timedelta, time
from dataclasses import dataclass, asdict
from enum import Enum
import statistics
from collections import defaultdict, Counter

logger = logging.getLogger(__name__)


class PatternType(Enum):
    """Types of patterns that can be recognized."""
    PRODUCTIVITY = "productivity"
    FOCUS_TIME = "focus_time"
    BREAK_PATTERN = "break_pattern"
    ENERGY_LEVEL = "energy_level"
    TASK_DURATION = "task_duration"
    CONTEXT_SWITCH = "context_switch"
    HABIT_FORMATION = "habit_formation"
    DISTRACTION = "distraction"


class FocusTimeQuality(Enum):
    """Quality levels for focus time periods."""
    DEEP = "deep"
    MODERATE = "moderate"
    SHALLOW = "shallow"
    INTERRUPTED = "interrupted"


@dataclass
class TimePattern:
    """Represents a recognized time-based pattern."""
    pattern_type: PatternType
    time_range: Tuple[time, time]
    confidence: float
    frequency: int
    duration_minutes: int
    quality_score: float
    metadata: Dict[str, Any]


@dataclass
class FocusTimeBlock:
    """Represents a focus time block with protection rules."""
    start_time: time
    end_time: time
    duration_minutes: int
    quality: FocusTimeQuality
    protection_level: int  # 1-5, higher = more protection
    buffer_minutes: int
    interruption_cost: float
    recovery_time_minutes: int


@dataclass
class HabitDefenseRule:
    """Rule for defending important habits against conflicts."""
    habit_name: str
    priority: int
    time_flexibility_minutes: int
    minimum_frequency_per_week: int
    protection_strength: float
    alternative_times: List[time]
    conflict_resolution_strategy: str


@dataclass
class PatternInsight:
    """Insight derived from pattern analysis."""
    insight_type: str
    description: str
    confidence: float
    actionable_suggestion: str
    impact_score: float
    supporting_data: Dict[str, Any]


class PatternRecognitionService:
    """
    Advanced pattern recognition service with focus time protection.
    
    Features:
    - Reclaim AI-inspired pattern analysis
    - Focus time protection algorithms
    - Habit defense mechanisms
    - Autonomous scheduling adjustments
    - Cloud-based ML processing
    - Mobile optimization
    """
    
    def __init__(self):
        self.min_pattern_occurrences = 3
        self.confidence_threshold = 0.7
        self.focus_time_buffer_minutes = 15
        self.habit_defense_enabled = True
        self.pattern_cache = {}
    
    def analyze_user_patterns(self, user_id: str, historical_data: List[Dict[str, Any]], 
                            days_to_analyze: int = 30) -> Dict[str, List[TimePattern]]:
        """
        Analyze user patterns from historical data.
        
        Args:
            user_id: User identifier
            historical_data: List of user activity records
            days_to_analyze: Number of days to analyze
            
        Returns:
            Dictionary of pattern types to recognized patterns
        """
        logger.info(f"Analyzing patterns for user {user_id} over {days_to_analyze} days")
        
        # Filter recent data
        cutoff_date = datetime.now() - timedelta(days=days_to_analyze)
        recent_data = [
            record for record in historical_data 
            if datetime.fromisoformat(record.get('timestamp', '2024-01-01')) >= cutoff_date
        ]
        
        if len(recent_data) < 10:
            logger.warning(f"Insufficient data for pattern analysis: {len(recent_data)} records")
            return {}
        
        patterns = {}
        
        # Analyze different pattern types
        patterns[PatternType.PRODUCTIVITY.value] = self._analyze_productivity_patterns(recent_data)
        patterns[PatternType.FOCUS_TIME.value] = self._analyze_focus_time_patterns(recent_data)
        patterns[PatternType.BREAK_PATTERN.value] = self._analyze_break_patterns(recent_data)
        patterns[PatternType.ENERGY_LEVEL.value] = self._analyze_energy_patterns(recent_data)
        patterns[PatternType.TASK_DURATION.value] = self._analyze_task_duration_patterns(recent_data)
        patterns[PatternType.CONTEXT_SWITCH.value] = self._analyze_context_switch_patterns(recent_data)
        patterns[PatternType.HABIT_FORMATION.value] = self._analyze_habit_patterns(recent_data)
        patterns[PatternType.DISTRACTION.value] = self._analyze_distraction_patterns(recent_data)
        
        # Cache results for performance
        self.pattern_cache[user_id] = {
            'patterns': patterns,
            'analyzed_at': datetime.now(),
            'data_points': len(recent_data)
        }
        
        return patterns
    
    def _analyze_productivity_patterns(self, data: List[Dict[str, Any]]) -> List[TimePattern]:
        """Analyze productivity patterns throughout the day."""
        productivity_by_hour = defaultdict(list)
        
        for record in data:
            if 'productivity_score' in record and 'timestamp' in record:
                try:
                    timestamp = datetime.fromisoformat(record['timestamp'])
                    hour = timestamp.hour
                    score = float(record['productivity_score'])
                    productivity_by_hour[hour].append(score)
                except (ValueError, TypeError):
                    continue
        
        patterns = []
        
        # Find high productivity periods
        for hour, scores in productivity_by_hour.items():
            if len(scores) >= self.min_pattern_occurrences:
                avg_score = statistics.mean(scores)
                if avg_score >= 0.7:  # High productivity threshold
                    pattern = TimePattern(
                        pattern_type=PatternType.PRODUCTIVITY,
                        time_range=(time(hour, 0), time(hour, 59)),
                        confidence=min(len(scores) / 10.0, 1.0),
                        frequency=len(scores),
                        duration_minutes=60,
                        quality_score=avg_score,
                        metadata={
                            'average_productivity': avg_score,
                            'score_variance': statistics.variance(scores) if len(scores) > 1 else 0,
                            'sample_size': len(scores)
                        }
                    )
                    patterns.append(pattern)
        
        return patterns
    
    def _analyze_focus_time_patterns(self, data: List[Dict[str, Any]]) -> List[TimePattern]:
        """Analyze focus time patterns for protection."""
        focus_sessions = []
        
        for record in data:
            if record.get('activity_type') == 'focus_work' and 'duration_minutes' in record:
                try:
                    timestamp = datetime.fromisoformat(record['timestamp'])
                    duration = int(record['duration_minutes'])
                    quality = record.get('focus_quality', 'moderate')
                    
                    focus_sessions.append({
                        'hour': timestamp.hour,
                        'duration': duration,
                        'quality': quality,
                        'interruptions': record.get('interruptions', 0)
                    })
                except (ValueError, TypeError):
                    continue
        
        # Group by hour and analyze
        focus_by_hour = defaultdict(list)
        for session in focus_sessions:
            focus_by_hour[session['hour']].append(session)
        
        patterns = []
        
        for hour, sessions in focus_by_hour.items():
            if len(sessions) >= self.min_pattern_occurrences:
                avg_duration = statistics.mean([s['duration'] for s in sessions])
                avg_interruptions = statistics.mean([s['interruptions'] for s in sessions])
                
                # Calculate quality score
                quality_scores = {'deep': 1.0, 'moderate': 0.7, 'shallow': 0.4, 'interrupted': 0.2}
                avg_quality = statistics.mean([
                    quality_scores.get(s['quality'], 0.5) for s in sessions
                ])
                
                if avg_duration >= 25:  # Minimum focus session length
                    pattern = TimePattern(
                        pattern_type=PatternType.FOCUS_TIME,
                        time_range=(time(hour, 0), time(hour, 59)),
                        confidence=min(len(sessions) / 7.0, 1.0),  # Weekly frequency
                        frequency=len(sessions),
                        duration_minutes=int(avg_duration),
                        quality_score=avg_quality,
                        metadata={
                            'average_interruptions': avg_interruptions,
                            'protection_recommended': avg_interruptions > 2,
                            'buffer_time_needed': max(15, int(avg_interruptions * 5))
                        }
                    )
                    patterns.append(pattern)
        
        return patterns
    
    def generate_focus_time_blocks(self, user_id: str, patterns: Dict[str, List[TimePattern]]) -> List[FocusTimeBlock]:
        """
        Generate protected focus time blocks based on patterns.
        
        Args:
            user_id: User identifier
            patterns: Recognized patterns from analysis
            
        Returns:
            List of recommended focus time blocks with protection
        """
        focus_blocks = []
        
        # Get focus time and productivity patterns
        focus_patterns = patterns.get(PatternType.FOCUS_TIME.value, [])
        productivity_patterns = patterns.get(PatternType.PRODUCTIVITY.value, [])
        distraction_patterns = patterns.get(PatternType.DISTRACTION.value, [])
        
        # Combine focus and productivity patterns
        all_focus_times = focus_patterns + [
            p for p in productivity_patterns if p.quality_score >= 0.8
        ]
        
        for pattern in all_focus_times:
            start_time, end_time = pattern.time_range
            
            # Calculate protection level based on pattern quality and distractions
            protection_level = self._calculate_protection_level(
                pattern, distraction_patterns
            )
            
            # Determine buffer time
            buffer_minutes = max(
                self.focus_time_buffer_minutes,
                pattern.metadata.get('buffer_time_needed', 15)
            )
            
            # Calculate interruption cost
            interruption_cost = self._calculate_interruption_cost(pattern)
            
            # Determine focus quality
            quality = self._determine_focus_quality(pattern)
            
            focus_block = FocusTimeBlock(
                start_time=start_time,
                end_time=end_time,
                duration_minutes=pattern.duration_minutes,
                quality=quality,
                protection_level=protection_level,
                buffer_minutes=buffer_minutes,
                interruption_cost=interruption_cost,
                recovery_time_minutes=int(interruption_cost * 2)
            )
            
            focus_blocks.append(focus_block)
        
        # Sort by protection level (highest first)
        focus_blocks.sort(key=lambda x: x.protection_level, reverse=True)
        
        return focus_blocks
    
    def generate_habit_defense_rules(self, user_id: str, patterns: Dict[str, List[TimePattern]]) -> List[HabitDefenseRule]:
        """
        Generate habit defense rules to protect important habits.
        
        Args:
            user_id: User identifier
            patterns: Recognized patterns from analysis
            
        Returns:
            List of habit defense rules
        """
        defense_rules = []
        
        habit_patterns = patterns.get(PatternType.HABIT_FORMATION.value, [])
        
        for pattern in habit_patterns:
            habit_name = pattern.metadata.get('habit_name', 'Unknown Habit')
            completion_rate = pattern.metadata.get('completion_rate', 0.5)
            
            # Higher priority for habits with lower completion rates
            priority = 5 if completion_rate < 0.6 else (4 if completion_rate < 0.8 else 3)
            
            # Calculate flexibility based on consistency
            consistency_score = pattern.metadata.get('consistency_score', 0.5)
            time_flexibility = int(60 * (1.0 - consistency_score))  # Less consistent = more flexible
            
            # Generate alternative times
            preferred_hour = pattern.metadata.get('preferred_hour', 9)
            alternative_times = [
                time(max(0, preferred_hour - 1), 0),
                time(min(23, preferred_hour + 1), 0),
                time(max(0, preferred_hour - 2), 0),
                time(min(23, preferred_hour + 2), 0)
            ]
            
            # Determine protection strength
            protection_strength = min(1.0, completion_rate + 0.3)
            
            defense_rule = HabitDefenseRule(
                habit_name=habit_name,
                priority=priority,
                time_flexibility_minutes=time_flexibility,
                minimum_frequency_per_week=max(1, int(pattern.frequency / 4)),  # Weekly minimum
                protection_strength=protection_strength,
                alternative_times=alternative_times,
                conflict_resolution_strategy='reschedule_conflicting_task' if priority >= 4 else 'suggest_alternative'
            )
            
            defense_rules.append(defense_rule)
        
        return defense_rules
    
    def _calculate_protection_level(self, pattern: TimePattern, distraction_patterns: List[TimePattern]) -> int:
        """Calculate protection level (1-5) for a focus time block."""
        base_protection = 3
        
        # Increase protection for high-quality focus times
        if pattern.quality_score >= 0.9:
            base_protection += 2
        elif pattern.quality_score >= 0.7:
            base_protection += 1
        
        # Increase protection if distractions are common during this time
        pattern_hour = pattern.time_range[0].hour
        for distraction in distraction_patterns:
            if distraction.time_range[0].hour == pattern_hour:
                if distraction.metadata.get('total_interruptions', 0) > 5:
                    base_protection += 1
                break
        
        return min(5, max(1, base_protection))
    
    def _calculate_interruption_cost(self, pattern: TimePattern) -> float:
        """Calculate the cost of interrupting this focus period (in minutes)."""
        base_cost = 5.0  # Minimum interruption cost
        
        # Higher cost for higher quality focus times
        quality_multiplier = pattern.quality_score * 2
        
        # Higher cost for longer focus sessions
        duration_multiplier = min(pattern.duration_minutes / 60.0, 2.0)
        
        return base_cost * quality_multiplier * duration_multiplier
    
    def _determine_focus_quality(self, pattern: TimePattern) -> FocusTimeQuality:
        """Determine focus quality based on pattern characteristics."""
        quality_score = pattern.quality_score
        interruptions = pattern.metadata.get('average_interruptions', 0)
        
        if quality_score >= 0.9 and interruptions <= 1:
            return FocusTimeQuality.DEEP
        elif quality_score >= 0.7 and interruptions <= 2:
            return FocusTimeQuality.MODERATE
        elif quality_score >= 0.5:
            return FocusTimeQuality.SHALLOW
        else:
            return FocusTimeQuality.INTERRUPTED
    
    def get_pattern_summary(self, user_id: str) -> Dict[str, Any]:
        """Get a summary of user patterns for dashboard display."""
        if user_id not in self.pattern_cache:
            return {'status': 'no_data', 'message': 'No pattern analysis available'}
        
        cache_entry = self.pattern_cache[user_id]
        patterns = cache_entry['patterns']
        
        summary = {
            'analyzed_at': cache_entry['analyzed_at'].isoformat(),
            'data_points': cache_entry['data_points'],
            'pattern_counts': {
                pattern_type: len(pattern_list)
                for pattern_type, pattern_list in patterns.items()
            },
            'top_insights': [],
            'focus_time_blocks': len(patterns.get(PatternType.FOCUS_TIME.value, [])),
            'habits_tracked': len(patterns.get(PatternType.HABIT_FORMATION.value, [])),
            'optimization_opportunities': 0
        }
        
        # Count optimization opportunities
        for pattern_list in patterns.values():
            for pattern in pattern_list:
                if pattern.metadata.get('optimization_needed') or pattern.metadata.get('protection_recommended'):
                    summary['optimization_opportunities'] += 1
        
        return summary