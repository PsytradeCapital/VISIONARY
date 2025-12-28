"""
Progress tracking with celebration and recovery system.

Task 9.4: Implement progress tracking with celebration and recovery
- Create real-time progress calculation with cloud synchronization
- Build Reclaim AI-inspired recovery action recommendation system
- Add milestone celebration with AI-generated celebratory visuals
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta, date
from dataclasses import dataclass, asdict
from enum import Enum
import json
import uuid
import statistics
from pathlib import Path

from ..core.config import settings

logger = logging.getLogger(__name__)

class ProgressMetric(Enum):
    """Types of progress metrics that can be tracked."""
    TASK_COMPLETION = "task_completion"
    GOAL_ACHIEVEMENT = "goal_achievement"
    HABIT_CONSISTENCY = "habit_consistency"
    TIME_MANAGEMENT = "time_management"
    HEALTH_METRICS = "health_metrics"
    FITNESS_PROGRESS = "fitness_progress"
    NUTRITION_TRACKING = "nutrition_tracking"
    FINANCIAL_GOALS = "financial_goals"
    PRODUCTIVITY_SCORE = "productivity_score"
    LEARNING_PROGRESS = "learning_progress"

class MilestoneType(Enum):
    """Types of milestones for celebration."""
    DAILY_STREAK = "daily_streak"
    WEEKLY_GOAL = "weekly_goal"
    MONTHLY_TARGET = "monthly_target"
    MAJOR_ACHIEVEMENT = "major_achievement"
    HABIT_FORMATION = "habit_formation"
    PERSONAL_BEST = "personal_best"
    CONSISTENCY_MILESTONE = "consistency_milestone"
    RECOVERY_SUCCESS = "recovery_success"

class RecoveryActionType(Enum):
    """Types of recovery actions for getting back on track."""
    SCHEDULE_ADJUSTMENT = "schedule_adjustment"
    GOAL_MODIFICATION = "goal_modification"
    HABIT_RESET = "habit_reset"
    MOTIVATION_BOOST = "motivation_boost"
    SUPPORT_SYSTEM = "support_system"
    BREAK_RECOMMENDATION = "break_recommendation"
    ALTERNATIVE_APPROACH = "alternative_approach"
    PROFESSIONAL_HELP = "professional_help"

@dataclass
class ProgressData:
    """Progress data for a specific metric."""
    metric_type: ProgressMetric
    user_id: str
    current_value: float
    target_value: float
    unit: str
    period_start: datetime
    period_end: datetime
    last_updated: datetime
    trend_direction: str  # "up", "down", "stable"
    completion_percentage: float
    historical_data: List[Dict[str, Any]] = None
    metadata: Dict[str, Any] = None

@dataclass
class Milestone:
    """Milestone achievement data."""
    milestone_id: str
    user_id: str
    milestone_type: MilestoneType
    title: str
    description: str
    achieved_at: datetime
    metric_type: ProgressMetric
    achievement_value: float
    celebration_content: Optional[Dict[str, Any]] = None
    ai_generated_image_url: Optional[str] = None
    shared: bool = False
    metadata: Dict[str, Any] = None

@dataclass
class RecoveryAction:
    """Recovery action recommendation."""
    action_id: str
    user_id: str
    action_type: RecoveryActionType
    title: str
    description: str
    priority: int  # 1-5, 5 being highest
    estimated_impact: float  # 0.0-1.0
    time_investment: str  # "5 minutes", "1 hour", etc.
    difficulty_level: str  # "easy", "medium", "hard"
    suggested_timing: datetime
    expires_at: datetime
    implemented: bool = False
    effectiveness_score: Optional[float] = None
    metadata: Dict[str, Any] = None

@dataclass
class ProgressSummary:
    """Comprehensive progress summary for a user."""
    user_id: str
    summary_date: datetime
    overall_score: float  # 0.0-100.0
    metrics: Dict[ProgressMetric, ProgressData]
    recent_milestones: List[Milestone]
    active_recovery_actions: List[RecoveryAction]
    trends: Dict[str, Any]
    recommendations: List[str]
    celebration_pending: bool = False

class ProgressTrackingService:
    """
    Progress tracking with celebration and recovery system.
    
    Features:
    - Real-time progress calculation with cloud synchronization
    - Reclaim AI-inspired recovery action recommendation system
    - Milestone celebration with AI-generated celebratory visuals
    - Comprehensive analytics and trend analysis
    - Personalized recovery suggestions based on user patterns
    """
    
    def __init__(self):
        # Progress data storage (in production, would use database)
        self.progress_data = {}  # user_id -> {metric_type -> ProgressData}
        self.milestones = {}     # user_id -> List[Milestone]
        self.recovery_actions = {}  # user_id -> List[RecoveryAction]
        
        # Recovery action templates
        self.recovery_templates = self._initialize_recovery_templates()
        
        # Milestone thresholds
        self.milestone_thresholds = self._initialize_milestone_thresholds()
        
        # Celebration content templates
        self.celebration_templates = self._initialize_celebration_templates()
        
        # Analytics cache
        self.analytics_cache = {}
        
        logger.info("ProgressTrackingService initialized")
    
    def _initialize_recovery_templates(self) -> Dict[RecoveryActionType, List[Dict[str, Any]]]:
        """Initialize recovery action templates."""
        return {
            RecoveryActionType.SCHEDULE_ADJUSTMENT: [
                {
                    'title': 'Adjust Your Schedule',
                    'description': 'Let\'s modify your schedule to be more realistic and achievable.',
                    'time_investment': '10 minutes',
                    'difficulty': 'easy',
                    'impact': 0.7
                },
                {
                    'title': 'Redistribute Tasks',
                    'description': 'Move some tasks to less busy days to balance your workload.',
                    'time_investment': '15 minutes',
                    'difficulty': 'medium',
                    'impact': 0.8
                }
            ],
            RecoveryActionType.GOAL_MODIFICATION: [
                {
                    'title': 'Adjust Goal Targets',
                    'description': 'Let\'s set more achievable targets that match your current capacity.',
                    'time_investment': '5 minutes',
                    'difficulty': 'easy',
                    'impact': 0.6
                },
                {
                    'title': 'Break Down Large Goals',
                    'description': 'Split your big goal into smaller, manageable milestones.',
                    'time_investment': '20 minutes',
                    'difficulty': 'medium',
                    'impact': 0.9
                }
            ],
            RecoveryActionType.HABIT_RESET: [
                {
                    'title': 'Start Small Again',
                    'description': 'Reset to a smaller, easier version of your habit to rebuild momentum.',
                    'time_investment': '2 minutes daily',
                    'difficulty': 'easy',
                    'impact': 0.8
                },
                {
                    'title': 'Change Your Environment',
                    'description': 'Modify your environment to make the habit easier to maintain.',
                    'time_investment': '30 minutes',
                    'difficulty': 'medium',
                    'impact': 0.7
                }
            ],
            RecoveryActionType.MOTIVATION_BOOST: [
                {
                    'title': 'Review Your Why',
                    'description': 'Reconnect with the reasons why this goal matters to you.',
                    'time_investment': '10 minutes',
                    'difficulty': 'easy',
                    'impact': 0.6
                },
                {
                    'title': 'Visualize Success',
                    'description': 'Spend time imagining how achieving this goal will feel.',
                    'time_investment': '15 minutes',
                    'difficulty': 'easy',
                    'impact': 0.7
                }
            ],
            RecoveryActionType.BREAK_RECOMMENDATION: [
                {
                    'title': 'Take a Strategic Break',
                    'description': 'Sometimes stepping back helps you come back stronger.',
                    'time_investment': '1-3 days',
                    'difficulty': 'easy',
                    'impact': 0.5
                },
                {
                    'title': 'Practice Self-Care',
                    'description': 'Focus on rest and recovery to restore your energy.',
                    'time_investment': '1 hour daily',
                    'difficulty': 'easy',
                    'impact': 0.6
                }
            ]
        }
    
    def _initialize_milestone_thresholds(self) -> Dict[MilestoneType, Dict[str, Any]]:
        """Initialize milestone achievement thresholds."""
        return {
            MilestoneType.DAILY_STREAK: {
                'thresholds': [3, 7, 14, 30, 60, 100],
                'titles': ['3-Day Streak!', '1-Week Strong!', '2-Week Champion!', 
                          '30-Day Warrior!', '60-Day Legend!', '100-Day Master!']
            },
            MilestoneType.WEEKLY_GOAL: {
                'completion_threshold': 0.8,  # 80% completion
                'title': 'Weekly Goal Achieved!'
            },
            MilestoneType.MONTHLY_TARGET: {
                'completion_threshold': 0.75,  # 75% completion
                'title': 'Monthly Target Reached!'
            },
            MilestoneType.HABIT_FORMATION: {
                'consistency_threshold': 0.85,  # 85% consistency over 21 days
                'duration_days': 21,
                'title': 'Habit Formed!'
            },
            MilestoneType.PERSONAL_BEST: {
                'improvement_threshold': 0.1,  # 10% improvement
                'title': 'New Personal Best!'
            }
        }
    
    def _initialize_celebration_templates(self) -> Dict[MilestoneType, List[str]]:
        """Initialize celebration content templates."""
        return {
            MilestoneType.DAILY_STREAK: [
                "🔥 You're on fire! {streak_days} days of consistency!",
                "💪 Unstoppable! {streak_days} days and counting!",
                "⭐ Streak master! {streak_days} days of dedication!"
            ],
            MilestoneType.WEEKLY_GOAL: [
                "🎉 Week conquered! You achieved {completion}% of your goal!",
                "🏆 Weekly champion! Outstanding progress this week!",
                "✨ Goal crushed! Another successful week in the books!"
            ],
            MilestoneType.MONTHLY_TARGET: [
                "🎊 Monthly milestone achieved! You're {completion}% there!",
                "🌟 Incredible month! Your consistency is paying off!",
                "🚀 Monthly target reached! You're building something amazing!"
            ],
            MilestoneType.HABIT_FORMATION: [
                "🎯 Habit formed! This is now part of who you are!",
                "🌱 Growth achieved! Your new habit is taking root!",
                "💎 Transformation complete! You've built a lasting habit!"
            ],
            MilestoneType.PERSONAL_BEST: [
                "🏅 New record! You've outdone yourself!",
                "⚡ Personal best achieved! You're getting stronger!",
                "🎖️ Peak performance! You've reached a new level!"
            ]
        }
    
    async def update_progress(
        self,
        user_id: str,
        metric_type: ProgressMetric,
        current_value: float,
        target_value: float,
        unit: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> ProgressData:
        """
        Update progress data for a user and metric.
        
        Args:
            user_id: User identifier
            metric_type: Type of progress metric
            current_value: Current progress value
            target_value: Target value to achieve
            unit: Unit of measurement
            metadata: Additional metadata
            
        Returns:
            Updated progress data
        """
        logger.info(f"Updating progress for user {user_id}, metric {metric_type.value}")
        
        # Initialize user progress if not exists
        if user_id not in self.progress_data:
            self.progress_data[user_id] = {}
        
        # Get existing progress or create new
        existing_progress = self.progress_data[user_id].get(metric_type)
        
        # Calculate completion percentage
        completion_percentage = min((current_value / max(target_value, 0.001)) * 100, 100)
        
        # Determine trend direction
        trend_direction = "stable"
        if existing_progress:
            if current_value > existing_progress.current_value:
                trend_direction = "up"
            elif current_value < existing_progress.current_value:
                trend_direction = "down"
        
        # Create updated progress data
        progress_data = ProgressData(
            metric_type=metric_type,
            user_id=user_id,
            current_value=current_value,
            target_value=target_value,
            unit=unit,
            period_start=existing_progress.period_start if existing_progress else datetime.utcnow(),
            period_end=datetime.utcnow() + timedelta(days=30),  # Default 30-day period
            last_updated=datetime.utcnow(),
            trend_direction=trend_direction,
            completion_percentage=completion_percentage,
            historical_data=self._update_historical_data(existing_progress, current_value),
            metadata=metadata or {}
        )
        
        # Store updated progress
        self.progress_data[user_id][metric_type] = progress_data
        
        # Check for milestones
        await self._check_milestones(user_id, metric_type, progress_data)
        
        # Check if recovery actions are needed
        await self._check_recovery_needs(user_id, metric_type, progress_data)
        
        return progress_data
    
    def _update_historical_data(
        self, 
        existing_progress: Optional[ProgressData], 
        new_value: float
    ) -> List[Dict[str, Any]]:
        """Update historical data with new value."""
        historical_data = []
        
        if existing_progress and existing_progress.historical_data:
            historical_data = existing_progress.historical_data.copy()
        
        # Add new data point
        historical_data.append({
            'timestamp': datetime.utcnow().isoformat(),
            'value': new_value
        })
        
        # Keep only last 100 data points
        return historical_data[-100:]
    
    async def _check_milestones(
        self,
        user_id: str,
        metric_type: ProgressMetric,
        progress_data: ProgressData
    ):
        """Check if any milestones have been achieved."""
        
        # Initialize user milestones if not exists
        if user_id not in self.milestones:
            self.milestones[user_id] = []
        
        # Check different milestone types
        await self._check_completion_milestones(user_id, metric_type, progress_data)
        await self._check_streak_milestones(user_id, metric_type, progress_data)
        await self._check_personal_best_milestones(user_id, metric_type, progress_data)
        await self._check_consistency_milestones(user_id, metric_type, progress_data)
    
    async def _check_completion_milestones(
        self,
        user_id: str,
        metric_type: ProgressMetric,
        progress_data: ProgressData
    ):
        """Check for goal completion milestones."""
        
        completion = progress_data.completion_percentage
        
        # Weekly goal milestone (80% completion)
        if completion >= 80 and not self._milestone_exists(user_id, MilestoneType.WEEKLY_GOAL, metric_type):
            milestone = await self._create_milestone(
                user_id=user_id,
                milestone_type=MilestoneType.WEEKLY_GOAL,
                metric_type=metric_type,
                achievement_value=completion,
                title="Weekly Goal Achieved!",
                description=f"You've reached {completion:.1f}% of your {metric_type.value} goal!"
            )
            self.milestones[user_id].append(milestone)
        
        # Monthly target milestone (75% completion)
        if completion >= 75 and not self._milestone_exists(user_id, MilestoneType.MONTHLY_TARGET, metric_type):
            milestone = await self._create_milestone(
                user_id=user_id,
                milestone_type=MilestoneType.MONTHLY_TARGET,
                metric_type=metric_type,
                achievement_value=completion,
                title="Monthly Target Reached!",
                description=f"Outstanding! You've achieved {completion:.1f}% of your monthly target!"
            )
            self.milestones[user_id].append(milestone)
    
    async def _check_streak_milestones(
        self,
        user_id: str,
        metric_type: ProgressMetric,
        progress_data: ProgressData
    ):
        """Check for streak-based milestones."""
        
        # Calculate current streak from historical data
        streak_days = self._calculate_streak(progress_data.historical_data)
        
        # Check streak thresholds
        thresholds = self.milestone_thresholds[MilestoneType.DAILY_STREAK]['thresholds']
        titles = self.milestone_thresholds[MilestoneType.DAILY_STREAK]['titles']
        
        for i, threshold in enumerate(thresholds):
            if streak_days >= threshold and not self._milestone_exists(
                user_id, MilestoneType.DAILY_STREAK, metric_type, threshold
            ):
                milestone = await self._create_milestone(
                    user_id=user_id,
                    milestone_type=MilestoneType.DAILY_STREAK,
                    metric_type=metric_type,
                    achievement_value=streak_days,
                    title=titles[i],
                    description=f"Incredible! You've maintained consistency for {streak_days} days!"
                )
                self.milestones[user_id].append(milestone)
    
    async def _check_personal_best_milestones(
        self,
        user_id: str,
        metric_type: ProgressMetric,
        progress_data: ProgressData
    ):
        """Check for personal best achievements."""
        
        if not progress_data.historical_data or len(progress_data.historical_data) < 2:
            return
        
        # Get historical values
        historical_values = [point['value'] for point in progress_data.historical_data[:-1]]
        current_value = progress_data.current_value
        
        # Check if current value is a personal best
        if historical_values and current_value > max(historical_values):
            improvement = (current_value - max(historical_values)) / max(historical_values)
            
            # Only create milestone for significant improvements (>10%)
            if improvement >= 0.1:
                milestone = await self._create_milestone(
                    user_id=user_id,
                    milestone_type=MilestoneType.PERSONAL_BEST,
                    metric_type=metric_type,
                    achievement_value=current_value,
                    title="New Personal Best!",
                    description=f"Amazing! You've improved by {improvement*100:.1f}% - that's a new record!"
                )
                self.milestones[user_id].append(milestone)
    
    async def _check_consistency_milestones(
        self,
        user_id: str,
        metric_type: ProgressMetric,
        progress_data: ProgressData
    ):
        """Check for consistency-based milestones (habit formation)."""
        
        if not progress_data.historical_data or len(progress_data.historical_data) < 21:
            return
        
        # Calculate consistency over last 21 days
        recent_data = progress_data.historical_data[-21:]
        consistency = self._calculate_consistency(recent_data)
        
        # Check habit formation threshold (85% consistency over 21 days)
        if consistency >= 0.85 and not self._milestone_exists(
            user_id, MilestoneType.HABIT_FORMATION, metric_type
        ):
            milestone = await self._create_milestone(
                user_id=user_id,
                milestone_type=MilestoneType.HABIT_FORMATION,
                metric_type=metric_type,
                achievement_value=consistency,
                title="Habit Formed!",
                description=f"Congratulations! You've maintained {consistency*100:.1f}% consistency for 21 days!"
            )
            self.milestones[user_id].append(milestone)
    
    def _calculate_streak(self, historical_data: Optional[List[Dict[str, Any]]]) -> int:
        """Calculate current streak from historical data."""
        if not historical_data:
            return 0
        
        # Simple streak calculation - count consecutive days with progress
        # In a real implementation, this would be more sophisticated
        streak = 0
        for point in reversed(historical_data):
            if point['value'] > 0:
                streak += 1
            else:
                break
        
        return streak
    
    def _calculate_consistency(self, data_points: List[Dict[str, Any]]) -> float:
        """Calculate consistency percentage from data points."""
        if not data_points:
            return 0.0
        
        # Count days with positive progress
        positive_days = sum(1 for point in data_points if point['value'] > 0)
        return positive_days / len(data_points)
    
    def _milestone_exists(
        self,
        user_id: str,
        milestone_type: MilestoneType,
        metric_type: ProgressMetric,
        threshold: Optional[int] = None
    ) -> bool:
        """Check if a milestone already exists."""
        if user_id not in self.milestones:
            return False
        
        for milestone in self.milestones[user_id]:
            if (milestone.milestone_type == milestone_type and 
                milestone.metric_type == metric_type):
                if threshold is None or milestone.achievement_value >= threshold:
                    return True
        
        return False
    
    async def _create_milestone(
        self,
        user_id: str,
        milestone_type: MilestoneType,
        metric_type: ProgressMetric,
        achievement_value: float,
        title: str,
        description: str
    ) -> Milestone:
        """Create a new milestone achievement."""
        
        milestone_id = str(uuid.uuid4())
        
        # Generate celebration content
        celebration_content = await self._generate_celebration_content(
            milestone_type, achievement_value, metric_type
        )
        
        milestone = Milestone(
            milestone_id=milestone_id,
            user_id=user_id,
            milestone_type=milestone_type,
            title=title,
            description=description,
            achieved_at=datetime.utcnow(),
            metric_type=metric_type,
            achievement_value=achievement_value,
            celebration_content=celebration_content,
            metadata={
                'auto_generated': True,
                'celebration_shown': False
            }
        )
        
        logger.info(f"Created milestone {milestone_id} for user {user_id}: {title}")
        
        return milestone
    
    async def _generate_celebration_content(
        self,
        milestone_type: MilestoneType,
        achievement_value: float,
        metric_type: ProgressMetric
    ) -> Dict[str, Any]:
        """Generate celebration content for milestone."""
        
        templates = self.celebration_templates.get(milestone_type, [
            "🎉 Milestone achieved! Great work!"
        ])
        
        # Select template (could be randomized or personalized)
        import random
        template = random.choice(templates)
        
        # Format template with achievement data
        celebration_message = template.format(
            streak_days=int(achievement_value) if milestone_type == MilestoneType.DAILY_STREAK else '',
            completion=f"{achievement_value:.1f}" if 'completion' in template else '',
            metric=metric_type.value.replace('_', ' ').title()
        )
        
        return {
            'message': celebration_message,
            'emoji': self._get_celebration_emoji(milestone_type),
            'color_scheme': self._get_celebration_colors(milestone_type),
            'animation': 'confetti',
            'sound': 'celebration_chime'
        }
    
    def _get_celebration_emoji(self, milestone_type: MilestoneType) -> str:
        """Get appropriate emoji for milestone type."""
        emoji_map = {
            MilestoneType.DAILY_STREAK: "🔥",
            MilestoneType.WEEKLY_GOAL: "🎉",
            MilestoneType.MONTHLY_TARGET: "🎊",
            MilestoneType.HABIT_FORMATION: "🎯",
            MilestoneType.PERSONAL_BEST: "🏅",
            MilestoneType.CONSISTENCY_MILESTONE: "⭐",
            MilestoneType.RECOVERY_SUCCESS: "💪"
        }
        return emoji_map.get(milestone_type, "🎉")
    
    def _get_celebration_colors(self, milestone_type: MilestoneType) -> Dict[str, str]:
        """Get color scheme for milestone celebration."""
        color_schemes = {
            MilestoneType.DAILY_STREAK: {"primary": "#FF6B35", "secondary": "#F7931E"},
            MilestoneType.WEEKLY_GOAL: {"primary": "#4CAF50", "secondary": "#8BC34A"},
            MilestoneType.MONTHLY_TARGET: {"primary": "#9C27B0", "secondary": "#E91E63"},
            MilestoneType.HABIT_FORMATION: {"primary": "#2196F3", "secondary": "#03DAC6"},
            MilestoneType.PERSONAL_BEST: {"primary": "#FFD700", "secondary": "#FFA000"},
        }
        return color_schemes.get(milestone_type, {"primary": "#4CAF50", "secondary": "#8BC34A"})
    
    async def _check_recovery_needs(
        self,
        user_id: str,
        metric_type: ProgressMetric,
        progress_data: ProgressData
    ):
        """Check if user needs recovery actions."""
        
        # Initialize user recovery actions if not exists
        if user_id not in self.recovery_actions:
            self.recovery_actions[user_id] = []
        
        # Analyze progress patterns to determine recovery needs
        needs_recovery = await self._analyze_recovery_needs(progress_data)
        
        if needs_recovery:
            recovery_actions = await self._generate_recovery_actions(
                user_id, metric_type, progress_data
            )
            
            # Add new recovery actions
            for action in recovery_actions:
                self.recovery_actions[user_id].append(action)
    
    async def _analyze_recovery_needs(self, progress_data: ProgressData) -> bool:
        """Analyze if user needs recovery actions based on progress patterns."""
        
        # Check for declining trend
        if progress_data.trend_direction == "down":
            return True
        
        # Check for low completion percentage
        if progress_data.completion_percentage < 30:
            return True
        
        # Check for stagnation (no progress in recent history)
        if progress_data.historical_data and len(progress_data.historical_data) >= 7:
            recent_values = [point['value'] for point in progress_data.historical_data[-7:]]
            if len(set(recent_values)) == 1:  # All values are the same
                return True
        
        # Check for inconsistency
        if progress_data.historical_data and len(progress_data.historical_data) >= 14:
            consistency = self._calculate_consistency(progress_data.historical_data[-14:])
            if consistency < 0.5:  # Less than 50% consistency
                return True
        
        return False
    
    async def _generate_recovery_actions(
        self,
        user_id: str,
        metric_type: ProgressMetric,
        progress_data: ProgressData
    ) -> List[RecoveryAction]:
        """Generate personalized recovery actions."""
        
        recovery_actions = []
        
        # Determine appropriate recovery action types based on the situation
        action_types = self._select_recovery_action_types(progress_data)
        
        for action_type in action_types:
            templates = self.recovery_templates.get(action_type, [])
            
            for template in templates[:2]:  # Max 2 actions per type
                action = RecoveryAction(
                    action_id=str(uuid.uuid4()),
                    user_id=user_id,
                    action_type=action_type,
                    title=template['title'],
                    description=template['description'],
                    priority=self._calculate_action_priority(action_type, progress_data),
                    estimated_impact=template['impact'],
                    time_investment=template['time_investment'],
                    difficulty_level=template['difficulty'],
                    suggested_timing=datetime.utcnow() + timedelta(hours=1),
                    expires_at=datetime.utcnow() + timedelta(days=7),
                    metadata={
                        'metric_type': metric_type.value,
                        'generated_at': datetime.utcnow().isoformat(),
                        'auto_generated': True
                    }
                )
                
                recovery_actions.append(action)
        
        logger.info(f"Generated {len(recovery_actions)} recovery actions for user {user_id}")
        
        return recovery_actions
    
    def _select_recovery_action_types(self, progress_data: ProgressData) -> List[RecoveryActionType]:
        """Select appropriate recovery action types based on progress analysis."""
        
        action_types = []
        
        # Low completion - suggest goal modification or schedule adjustment
        if progress_data.completion_percentage < 30:
            action_types.extend([
                RecoveryActionType.GOAL_MODIFICATION,
                RecoveryActionType.SCHEDULE_ADJUSTMENT
            ])
        
        # Declining trend - suggest motivation boost or habit reset
        if progress_data.trend_direction == "down":
            action_types.extend([
                RecoveryActionType.MOTIVATION_BOOST,
                RecoveryActionType.HABIT_RESET
            ])
        
        # Stagnation - suggest break or alternative approach
        if progress_data.historical_data:
            recent_values = [point['value'] for point in progress_data.historical_data[-7:]]
            if len(set(recent_values)) <= 2:  # Very little variation
                action_types.extend([
                    RecoveryActionType.BREAK_RECOMMENDATION,
                    RecoveryActionType.ALTERNATIVE_APPROACH
                ])
        
        return list(set(action_types))  # Remove duplicates
    
    def _calculate_action_priority(
        self, 
        action_type: RecoveryActionType, 
        progress_data: ProgressData
    ) -> int:
        """Calculate priority for recovery action (1-5, 5 being highest)."""
        
        base_priority = {
            RecoveryActionType.SCHEDULE_ADJUSTMENT: 4,
            RecoveryActionType.GOAL_MODIFICATION: 3,
            RecoveryActionType.HABIT_RESET: 4,
            RecoveryActionType.MOTIVATION_BOOST: 2,
            RecoveryActionType.BREAK_RECOMMENDATION: 1,
            RecoveryActionType.ALTERNATIVE_APPROACH: 3
        }.get(action_type, 2)
        
        # Adjust based on progress severity
        if progress_data.completion_percentage < 20:
            base_priority += 1
        elif progress_data.completion_percentage > 60:
            base_priority -= 1
        
        return max(1, min(5, base_priority))
    
    async def get_progress_summary(self, user_id: str) -> ProgressSummary:
        """Get comprehensive progress summary for a user."""
        
        user_progress = self.progress_data.get(user_id, {})
        user_milestones = self.milestones.get(user_id, [])
        user_recovery_actions = self.recovery_actions.get(user_id, [])
        
        # Calculate overall score
        overall_score = self._calculate_overall_score(user_progress)
        
        # Get recent milestones (last 30 days)
        recent_milestones = [
            milestone for milestone in user_milestones
            if milestone.achieved_at > datetime.utcnow() - timedelta(days=30)
        ]
        
        # Get active recovery actions
        active_recovery_actions = [
            action for action in user_recovery_actions
            if not action.implemented and action.expires_at > datetime.utcnow()
        ]
        
        # Generate trends analysis
        trends = await self._analyze_trends(user_progress)
        
        # Generate recommendations
        recommendations = await self._generate_recommendations(user_progress, trends)
        
        # Check if celebration is pending
        celebration_pending = any(
            not milestone.metadata.get('celebration_shown', False)
            for milestone in recent_milestones
        )
        
        return ProgressSummary(
            user_id=user_id,
            summary_date=datetime.utcnow(),
            overall_score=overall_score,
            metrics=user_progress,
            recent_milestones=recent_milestones,
            active_recovery_actions=active_recovery_actions,
            trends=trends,
            recommendations=recommendations,
            celebration_pending=celebration_pending
        )
    
    def _calculate_overall_score(self, user_progress: Dict[ProgressMetric, ProgressData]) -> float:
        """Calculate overall progress score (0-100)."""
        
        if not user_progress:
            return 0.0
        
        # Calculate weighted average of completion percentages
        total_weight = 0
        weighted_sum = 0
        
        # Define weights for different metrics
        metric_weights = {
            ProgressMetric.TASK_COMPLETION: 1.0,
            ProgressMetric.GOAL_ACHIEVEMENT: 1.2,
            ProgressMetric.HABIT_CONSISTENCY: 1.1,
            ProgressMetric.TIME_MANAGEMENT: 0.9,
            ProgressMetric.HEALTH_METRICS: 1.0,
            ProgressMetric.FITNESS_PROGRESS: 1.0,
            ProgressMetric.NUTRITION_TRACKING: 0.8,
            ProgressMetric.FINANCIAL_GOALS: 1.1,
            ProgressMetric.PRODUCTIVITY_SCORE: 0.9,
            ProgressMetric.LEARNING_PROGRESS: 0.8
        }
        
        for metric_type, progress_data in user_progress.items():
            weight = metric_weights.get(metric_type, 1.0)
            weighted_sum += progress_data.completion_percentage * weight
            total_weight += weight
        
        return weighted_sum / total_weight if total_weight > 0 else 0.0
    
    async def _analyze_trends(self, user_progress: Dict[ProgressMetric, ProgressData]) -> Dict[str, Any]:
        """Analyze progress trends."""
        
        trends = {
            'improving_metrics': [],
            'declining_metrics': [],
            'stable_metrics': [],
            'overall_trend': 'stable',
            'momentum_score': 0.0
        }
        
        for metric_type, progress_data in user_progress.items():
            if progress_data.trend_direction == "up":
                trends['improving_metrics'].append(metric_type.value)
            elif progress_data.trend_direction == "down":
                trends['declining_metrics'].append(metric_type.value)
            else:
                trends['stable_metrics'].append(metric_type.value)
        
        # Determine overall trend
        improving_count = len(trends['improving_metrics'])
        declining_count = len(trends['declining_metrics'])
        
        if improving_count > declining_count:
            trends['overall_trend'] = 'improving'
        elif declining_count > improving_count:
            trends['overall_trend'] = 'declining'
        
        # Calculate momentum score
        trends['momentum_score'] = (improving_count - declining_count) / max(len(user_progress), 1)
        
        return trends
    
    async def _generate_recommendations(
        self, 
        user_progress: Dict[ProgressMetric, ProgressData],
        trends: Dict[str, Any]
    ) -> List[str]:
        """Generate personalized recommendations."""
        
        recommendations = []
        
        # Recommendations based on overall trend
        if trends['overall_trend'] == 'improving':
            recommendations.append("You're on a great trajectory! Keep up the momentum.")
        elif trends['overall_trend'] == 'declining':
            recommendations.append("Consider reviewing your goals and adjusting your approach.")
        
        # Recommendations based on specific metrics
        for metric_type, progress_data in user_progress.items():
            if progress_data.completion_percentage < 30:
                recommendations.append(
                    f"Focus on improving your {metric_type.value.replace('_', ' ')} - "
                    f"consider breaking it into smaller steps."
                )
            elif progress_data.completion_percentage > 80:
                recommendations.append(
                    f"Excellent progress on {metric_type.value.replace('_', ' ')}! "
                    f"You're almost there!"
                )
        
        # Limit to top 5 recommendations
        return recommendations[:5]
    
    async def mark_recovery_action_implemented(
        self, 
        user_id: str, 
        action_id: str,
        effectiveness_score: Optional[float] = None
    ) -> bool:
        """Mark a recovery action as implemented."""
        
        if user_id not in self.recovery_actions:
            return False
        
        for action in self.recovery_actions[user_id]:
            if action.action_id == action_id:
                action.implemented = True
                action.effectiveness_score = effectiveness_score
                logger.info(f"Marked recovery action {action_id} as implemented")
                return True
        
        return False
    
    async def get_milestone_celebrations(self, user_id: str) -> List[Milestone]:
        """Get pending milestone celebrations for a user."""
        
        if user_id not in self.milestones:
            return []
        
        pending_celebrations = [
            milestone for milestone in self.milestones[user_id]
            if not milestone.metadata.get('celebration_shown', False)
        ]
        
        return pending_celebrations
    
    async def mark_celebration_shown(self, user_id: str, milestone_id: str) -> bool:
        """Mark a milestone celebration as shown."""
        
        if user_id not in self.milestones:
            return False
        
        for milestone in self.milestones[user_id]:
            if milestone.milestone_id == milestone_id:
                milestone.metadata['celebration_shown'] = True
                logger.info(f"Marked celebration {milestone_id} as shown")
                return True
        
        return False
    
    async def cleanup_expired_data(self) -> Dict[str, int]:
        """Clean up expired recovery actions and old data."""
        
        current_time = datetime.utcnow()
        cleanup_stats = {
            'expired_recovery_actions': 0,
            'old_milestones': 0
        }
        
        # Clean up expired recovery actions
        for user_id, actions in self.recovery_actions.items():
            expired_actions = [
                action for action in actions
                if action.expires_at < current_time
            ]
            
            for action in expired_actions:
                actions.remove(action)
                cleanup_stats['expired_recovery_actions'] += 1
        
        # Clean up old milestones (older than 1 year)
        one_year_ago = current_time - timedelta(days=365)
        
        for user_id, milestones in self.milestones.items():
            old_milestones = [
                milestone for milestone in milestones
                if milestone.achieved_at < one_year_ago
            ]
            
            for milestone in old_milestones:
                milestones.remove(milestone)
                cleanup_stats['old_milestones'] += 1
        
        logger.info(f"Cleanup completed: {cleanup_stats}")
        
        return cleanup_stats