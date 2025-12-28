"""
Photorealistic progress visualization system.

Generates images of real people achieving health milestones, real financial success scenes,
real wellness environments, and context-aware image selection based on user's specific goals.
"""

import json
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum
import statistics
from .ai_visual_generator import (
    AIVisualGeneratorService, PhotorealisticImage, HealthContext, 
    NutritionContext, FinancialContext, WellnessContext, VisionCategory,
    ImageStyle, ImageResolution
)

logger = logging.getLogger(__name__)


class ProgressStage(Enum):
    """Stages of progress for visualization."""
    STARTING = "starting"
    EARLY_PROGRESS = "early_progress"
    SIGNIFICANT_PROGRESS = "significant_progress"
    MAJOR_MILESTONE = "major_milestone"
    GOAL_ACHIEVED = "goal_achieved"


class VisualizationType(Enum):
    """Types of progress visualizations."""
    BEFORE_AFTER = "before_after"
    MILESTONE_CELEBRATION = "milestone_celebration"
    JOURNEY_PROGRESSION = "journey_progression"
    SUCCESS_SCENARIO = "success_scenario"
    MOTIVATIONAL_FUTURE = "motivational_future"


@dataclass
class ProgressVisualization:
    """Represents a progress visualization with photorealistic images."""
    id: str
    user_id: str
    goal_id: str
    visualization_type: VisualizationType
    progress_stage: ProgressStage
    primary_image: PhotorealisticImage
    supporting_images: List[PhotorealisticImage]
    progress_metrics: Dict[str, float]
    contextual_message: str
    generated_at: datetime
    expires_at: datetime
    metadata: Dict[str, Any]


@dataclass
class HealthMilestone:
    """Health milestone for visualization."""
    milestone_type: str  # 'weight_loss', 'strength_gain', 'endurance_improvement'
    current_value: float
    target_value: float
    progress_percentage: float
    achievement_date: Optional[datetime]
    celebration_worthy: bool


@dataclass
class FinancialMilestone:
    """Financial milestone for visualization."""
    milestone_type: str  # 'savings_goal', 'debt_reduction', 'income_increase'
    current_amount: float
    target_amount: float
    progress_percentage: float
    achievement_date: Optional[datetime]
    celebration_worthy: bool


@dataclass
class WellnessMilestone:
    """Wellness milestone for visualization."""
    milestone_type: str  # 'stress_reduction', 'sleep_improvement', 'mindfulness'
    current_score: float
    target_score: float
    progress_percentage: float
    achievement_date: Optional[datetime]
    celebration_worthy: bool


class ProgressVisualizationService:
    """
    Photorealistic progress visualization system.
    
    Features:
    - Real people achieving health milestones (fit people exercising, healthy meals)
    - Real financial success scenes (people in nice offices, celebrating achievements)
    - Real wellness environments (peaceful nature scenes, happy people meditating)
    - Context-aware image selection based on user's specific goals and progress
    - Premium photorealistic quality validation
    """
    
    def __init__(self, visual_generator: AIVisualGeneratorService):
        self.visual_generator = visual_generator
        self.visualization_cache = {}
        self.cache_duration = timedelta(hours=12)
        
        # Progress stage thresholds
        self.progress_thresholds = {
            ProgressStage.STARTING: (0.0, 0.1),
            ProgressStage.EARLY_PROGRESS: (0.1, 0.3),
            ProgressStage.SIGNIFICANT_PROGRESS: (0.3, 0.7),
            ProgressStage.MAJOR_MILESTONE: (0.7, 0.9),
            ProgressStage.GOAL_ACHIEVED: (0.9, 1.0)
        }
    
    async def generate_health_milestone_visualization(
        self, 
        user_id: str, 
        milestone: HealthMilestone,
        user_preferences: Dict[str, Any] = None
    ) -> ProgressVisualization:
        """
        Generate photorealistic health milestone visualizations.
        
        Args:
            user_id: User identifier
            milestone: Health milestone data
            user_preferences: User preferences for personalization
            
        Returns:
            ProgressVisualization with real people achieving health goals
        """
        logger.info(f"Generating health milestone visualization for {milestone.milestone_type}")
        
        # Determine progress stage
        progress_stage = self._determine_progress_stage(milestone.progress_percentage)
        
        # Build health context
        health_context = self._build_health_context(milestone, user_preferences)
        
        # Generate primary image based on milestone type and progress
        primary_image = await self._generate_health_progress_image(
            milestone, health_context, progress_stage
        )
        
        # Generate supporting images
        supporting_images = await self._generate_health_supporting_images(
            milestone, health_context, progress_stage
        )
        
        # Create contextual message
        contextual_message = self._create_health_progress_message(milestone, progress_stage)
        
        # Create visualization
        visualization = ProgressVisualization(
            id=f"health_{user_id}_{datetime.now().timestamp()}",
            user_id=user_id,
            goal_id=milestone.milestone_type,
            visualization_type=VisualizationType.MILESTONE_CELEBRATION if milestone.celebration_worthy else VisualizationType.JOURNEY_PROGRESSION,
            progress_stage=progress_stage,
            primary_image=primary_image,
            supporting_images=supporting_images,
            progress_metrics={
                'current_value': milestone.current_value,
                'target_value': milestone.target_value,
                'progress_percentage': milestone.progress_percentage
            },
            contextual_message=contextual_message,
            generated_at=datetime.now(),
            expires_at=datetime.now() + self.cache_duration,
            metadata={
                'milestone_type': milestone.milestone_type,
                'category': 'health',
                'celebration_worthy': milestone.celebration_worthy
            }
        )
        
        return visualization
    
    async def generate_financial_success_visualization(
        self,
        user_id: str,
        milestone: FinancialMilestone,
        user_context: Dict[str, Any] = None
    ) -> ProgressVisualization:
        """
        Generate photorealistic financial success visualizations.
        
        Args:
            user_id: User identifier
            milestone: Financial milestone data
            user_context: User context for personalization
            
        Returns:
            ProgressVisualization with real people in success scenarios
        """
        logger.info(f"Generating financial success visualization for {milestone.milestone_type}")
        
        # Determine progress stage
        progress_stage = self._determine_progress_stage(milestone.progress_percentage)
        
        # Build financial context
        financial_context = self._build_financial_context(milestone, user_context)
        
        # Generate primary success image
        primary_image = await self._generate_financial_success_image(
            milestone, financial_context, progress_stage
        )
        
        # Generate supporting images
        supporting_images = await self._generate_financial_supporting_images(
            milestone, financial_context, progress_stage
        )
        
        # Create contextual message
        contextual_message = self._create_financial_progress_message(milestone, progress_stage)
        
        # Create visualization
        visualization = ProgressVisualization(
            id=f"financial_{user_id}_{datetime.now().timestamp()}",
            user_id=user_id,
            goal_id=milestone.milestone_type,
            visualization_type=VisualizationType.SUCCESS_SCENARIO if milestone.celebration_worthy else VisualizationType.JOURNEY_PROGRESSION,
            progress_stage=progress_stage,
            primary_image=primary_image,
            supporting_images=supporting_images,
            progress_metrics={
                'current_amount': milestone.current_amount,
                'target_amount': milestone.target_amount,
                'progress_percentage': milestone.progress_percentage
            },
            contextual_message=contextual_message,
            generated_at=datetime.now(),
            expires_at=datetime.now() + self.cache_duration,
            metadata={
                'milestone_type': milestone.milestone_type,
                'category': 'financial',
                'celebration_worthy': milestone.celebration_worthy
            }
        )
        
        return visualization
    
    async def generate_wellness_environment_visualization(
        self,
        user_id: str,
        milestone: WellnessMilestone,
        user_preferences: Dict[str, Any] = None
    ) -> ProgressVisualization:
        """
        Generate photorealistic wellness environment visualizations.
        
        Args:
            user_id: User identifier
            milestone: Wellness milestone data
            user_preferences: User preferences for personalization
            
        Returns:
            ProgressVisualization with real wellness environments
        """
        logger.info(f"Generating wellness visualization for {milestone.milestone_type}")
        
        # Determine progress stage
        progress_stage = self._determine_progress_stage(milestone.progress_percentage)
        
        # Build wellness context
        wellness_context = self._build_wellness_context(milestone, user_preferences)
        
        # Generate primary wellness image
        primary_image = await self._generate_wellness_environment_image(
            milestone, wellness_context, progress_stage
        )
        
        # Generate supporting images
        supporting_images = await self._generate_wellness_supporting_images(
            milestone, wellness_context, progress_stage
        )
        
        # Create contextual message
        contextual_message = self._create_wellness_progress_message(milestone, progress_stage)
        
        # Create visualization
        visualization = ProgressVisualization(
            id=f"wellness_{user_id}_{datetime.now().timestamp()}",
            user_id=user_id,
            goal_id=milestone.milestone_type,
            visualization_type=VisualizationType.MOTIVATIONAL_FUTURE if progress_stage in [ProgressStage.STARTING, ProgressStage.EARLY_PROGRESS] else VisualizationType.MILESTONE_CELEBRATION,
            progress_stage=progress_stage,
            primary_image=primary_image,
            supporting_images=supporting_images,
            progress_metrics={
                'current_score': milestone.current_score,
                'target_score': milestone.target_score,
                'progress_percentage': milestone.progress_percentage
            },
            contextual_message=contextual_message,
            generated_at=datetime.now(),
            expires_at=datetime.now() + self.cache_duration,
            metadata={
                'milestone_type': milestone.milestone_type,
                'category': 'wellness',
                'celebration_worthy': milestone.celebration_worthy
            }
        )
        
        return visualization
    
    async def generate_context_aware_visualization(
        self,
        user_id: str,
        goal_data: Dict[str, Any],
        progress_data: Dict[str, Any],
        user_context: Dict[str, Any]
    ) -> ProgressVisualization:
        """
        Generate context-aware visualization based on user's specific goals and progress.
        
        Args:
            user_id: User identifier
            goal_data: User's goal information
            progress_data: Current progress data
            user_context: User context and preferences
            
        Returns:
            ProgressVisualization tailored to user's specific situation
        """
        logger.info(f"Generating context-aware visualization for user {user_id}")
        
        goal_category = goal_data.get('category', 'general')
        progress_percentage = progress_data.get('progress_percentage', 0.0)
        
        # Route to appropriate visualization based on category
        if goal_category == 'health' or goal_category == 'fitness':
            milestone = HealthMilestone(
                milestone_type=goal_data.get('type', 'general_health'),
                current_value=progress_data.get('current_value', 0.0),
                target_value=goal_data.get('target_value', 100.0),
                progress_percentage=progress_percentage,
                achievement_date=None,
                celebration_worthy=progress_percentage >= 0.7
            )
            return await self.generate_health_milestone_visualization(
                user_id, milestone, user_context
            )
        
        elif goal_category == 'financial':
            milestone = FinancialMilestone(
                milestone_type=goal_data.get('type', 'savings_goal'),
                current_amount=progress_data.get('current_amount', 0.0),
                target_amount=goal_data.get('target_amount', 10000.0),
                progress_percentage=progress_percentage,
                achievement_date=None,
                celebration_worthy=progress_percentage >= 0.7
            )
            return await self.generate_financial_success_visualization(
                user_id, milestone, user_context
            )
        
        elif goal_category in ['wellness', 'psychological', 'mindfulness']:
            milestone = WellnessMilestone(
                milestone_type=goal_data.get('type', 'stress_reduction'),
                current_score=progress_data.get('current_score', 0.0),
                target_score=goal_data.get('target_score', 10.0),
                progress_percentage=progress_percentage,
                achievement_date=None,
                celebration_worthy=progress_percentage >= 0.7
            )
            return await self.generate_wellness_environment_visualization(
                user_id, milestone, user_context
            )
        
        else:
            # Default to motivational visualization
            return await self._generate_general_motivational_visualization(
                user_id, goal_data, progress_data, user_context
            )
    
    def _determine_progress_stage(self, progress_percentage: float) -> ProgressStage:
        """Determine progress stage based on percentage."""
        for stage, (min_val, max_val) in self.progress_thresholds.items():
            if min_val <= progress_percentage <= max_val:
                return stage
        return ProgressStage.STARTING
    
    def _build_health_context(self, milestone: HealthMilestone, 
                            user_preferences: Dict[str, Any] = None) -> HealthContext:
        """Build health context for image generation."""
        if user_preferences is None:
            user_preferences = {}
        
        # Map milestone types to activities
        activity_mapping = {
            'weight_loss': 'running',
            'muscle_gain': 'gym',
            'strength_gain': 'gym',
            'endurance_improvement': 'running',
            'flexibility': 'yoga',
            'cardiovascular': 'running'
        }
        
        # Map milestone types to goals
        goal_mapping = {
            'weight_loss': 'weight_loss',
            'muscle_gain': 'muscle_gain',
            'strength_gain': 'muscle_gain',
            'endurance_improvement': 'endurance',
            'flexibility': 'flexibility',
            'cardiovascular': 'endurance'
        }
        
        activity_type = activity_mapping.get(milestone.milestone_type, 'gym')
        goal_type = goal_mapping.get(milestone.milestone_type, 'weight_loss')
        
        return HealthContext(
            goal_type=goal_type,
            current_progress=milestone.progress_percentage,
            activity_type=activity_type,
            gender_preference=user_preferences.get('gender_preference', 'diverse'),
            age_range=user_preferences.get('age_range', 'young_adult'),
            environment=user_preferences.get('preferred_environment', 'gym')
        )
    
    def _build_financial_context(self, milestone: FinancialMilestone,
                               user_context: Dict[str, Any] = None) -> FinancialContext:
        """Build financial context for image generation."""
        if user_context is None:
            user_context = {}
        
        # Map milestone types to achievement types
        achievement_mapping = {
            'savings_goal': 'investment_growth',
            'debt_reduction': 'debt_freedom',
            'income_increase': 'promotion',
            'investment_growth': 'investment_growth',
            'business_goal': 'business_success'
        }
        
        achievement_type = achievement_mapping.get(milestone.milestone_type, 'investment_growth')
        
        return FinancialContext(
            achievement_type=achievement_type,
            setting=user_context.get('preferred_setting', 'office'),
            professional_level=user_context.get('professional_level', 'mid_career'),
            success_indicators=['charts', 'handshake', 'nice_office']
        )
    
    def _build_wellness_context(self, milestone: WellnessMilestone,
                              user_preferences: Dict[str, Any] = None) -> WellnessContext:
        """Build wellness context for image generation."""
        if user_preferences is None:
            user_preferences = {}
        
        # Map milestone types to moods and activities
        mood_mapping = {
            'stress_reduction': 'calm',
            'sleep_improvement': 'peaceful',
            'mindfulness': 'focused',
            'anxiety_reduction': 'calm',
            'mood_improvement': 'energized'
        }
        
        activity_mapping = {
            'stress_reduction': 'meditation',
            'sleep_improvement': 'reading',
            'mindfulness': 'meditation',
            'anxiety_reduction': 'nature_walk',
            'mood_improvement': 'nature_walk'
        }
        
        mood_state = mood_mapping.get(milestone.milestone_type, 'calm')
        activity = activity_mapping.get(milestone.milestone_type, 'meditation')
        
        return WellnessContext(
            mood_state=mood_state,
            activity=activity,
            environment=user_preferences.get('preferred_environment', 'nature'),
            time_of_day=user_preferences.get('preferred_time', 'golden_hour')
        )
    
    async def _generate_health_progress_image(self, milestone: HealthMilestone,
                                            context: HealthContext,
                                            stage: ProgressStage) -> PhotorealisticImage:
        """Generate primary health progress image."""
        # Adjust context based on progress stage
        if stage == ProgressStage.GOAL_ACHIEVED:
            context.current_progress = 1.0
        
        return await self.visual_generator.generate_health_progress_image(context)
    
    async def _generate_health_supporting_images(self, milestone: HealthMilestone,
                                               context: HealthContext,
                                               stage: ProgressStage) -> List[PhotorealisticImage]:
        """Generate supporting health images."""
        supporting_images = []
        
        # Generate nutrition image if relevant
        if milestone.milestone_type in ['weight_loss', 'muscle_gain']:
            nutrition_context = NutritionContext(
                meal_type='lunch',
                dietary_preferences=['healthy', 'balanced'],
                cuisine_style='mediterranean',
                presentation_style='home_cooked',
                portion_size='single'
            )
            nutrition_image = await self.visual_generator.generate_nutrition_image(
                'healthy_meal', nutrition_context
            )
            supporting_images.append(nutrition_image)
        
        # Generate celebration image if milestone achieved
        if stage == ProgressStage.GOAL_ACHIEVED:
            celebration_image = await self.visual_generator.generate_celebration_image(
                {'type': 'health', 'title': f'{milestone.milestone_type} achieved'},
                {'celebration_preference': 'personal'}
            )
            supporting_images.append(celebration_image)
        
        return supporting_images
    
    async def _generate_financial_success_image(self, milestone: FinancialMilestone,
                                              context: FinancialContext,
                                              stage: ProgressStage) -> PhotorealisticImage:
        """Generate primary financial success image."""
        achievement_data = {
            'type': milestone.milestone_type,
            'amount': milestone.current_amount,
            'progress': milestone.progress_percentage
        }
        
        return await self.visual_generator.generate_financial_success_image(
            achievement_data, context
        )
    
    async def _generate_financial_supporting_images(self, milestone: FinancialMilestone,
                                                  context: FinancialContext,
                                                  stage: ProgressStage) -> List[PhotorealisticImage]:
        """Generate supporting financial images."""
        supporting_images = []
        
        # Generate celebration image if major milestone
        if stage in [ProgressStage.MAJOR_MILESTONE, ProgressStage.GOAL_ACHIEVED]:
            celebration_image = await self.visual_generator.generate_celebration_image(
                {'type': 'financial', 'title': f'{milestone.milestone_type} milestone'},
                {'celebration_preference': 'professional'}
            )
            supporting_images.append(celebration_image)
        
        return supporting_images
    
    async def _generate_wellness_environment_image(self, milestone: WellnessMilestone,
                                                 context: WellnessContext,
                                                 stage: ProgressStage) -> PhotorealisticImage:
        """Generate primary wellness environment image."""
        return await self.visual_generator.generate_wellness_image(
            context.mood_state, context.activity, context
        )
    
    async def _generate_wellness_supporting_images(self, milestone: WellnessMilestone,
                                                 context: WellnessContext,
                                                 stage: ProgressStage) -> List[PhotorealisticImage]:
        """Generate supporting wellness images."""
        supporting_images = []
        
        # Generate motivational scene
        motivational_image = await self.visual_generator.generate_motivational_scene(
            VisionCategory.WELLNESS, {'preferred_motivation_style': 'peaceful'}
        )
        supporting_images.append(motivational_image)
        
        return supporting_images
    
    def _create_health_progress_message(self, milestone: HealthMilestone,
                                      stage: ProgressStage) -> str:
        """Create contextual message for health progress."""
        messages = {
            ProgressStage.STARTING: f"Starting your {milestone.milestone_type} journey! Every step counts.",
            ProgressStage.EARLY_PROGRESS: f"Great start on your {milestone.milestone_type} goal! You're {milestone.progress_percentage:.0%} there.",
            ProgressStage.SIGNIFICANT_PROGRESS: f"Amazing progress on {milestone.milestone_type}! You're {milestone.progress_percentage:.0%} complete.",
            ProgressStage.MAJOR_MILESTONE: f"Incredible! You're almost there with your {milestone.milestone_type} goal - {milestone.progress_percentage:.0%} complete!",
            ProgressStage.GOAL_ACHIEVED: f"🎉 Congratulations! You've achieved your {milestone.milestone_type} goal!"
        }
        
        return messages.get(stage, f"Keep going with your {milestone.milestone_type} journey!")
    
    def _create_financial_progress_message(self, milestone: FinancialMilestone,
                                         stage: ProgressStage) -> str:
        """Create contextual message for financial progress."""
        messages = {
            ProgressStage.STARTING: f"Starting your {milestone.milestone_type} journey! Building wealth takes time.",
            ProgressStage.EARLY_PROGRESS: f"Good progress on your {milestone.milestone_type}! You're {milestone.progress_percentage:.0%} there.",
            ProgressStage.SIGNIFICANT_PROGRESS: f"Excellent financial progress! Your {milestone.milestone_type} is {milestone.progress_percentage:.0%} complete.",
            ProgressStage.MAJOR_MILESTONE: f"Outstanding! You're nearly there with your {milestone.milestone_type} - {milestone.progress_percentage:.0%} complete!",
            ProgressStage.GOAL_ACHIEVED: f"🎉 Financial goal achieved! You've completed your {milestone.milestone_type}!"
        }
        
        return messages.get(stage, f"Keep building towards your {milestone.milestone_type} goal!")
    
    def _create_wellness_progress_message(self, milestone: WellnessMilestone,
                                        stage: ProgressStage) -> str:
        """Create contextual message for wellness progress."""
        messages = {
            ProgressStage.STARTING: f"Beginning your {milestone.milestone_type} journey. Small steps lead to big changes.",
            ProgressStage.EARLY_PROGRESS: f"Positive changes in {milestone.milestone_type}! You're {milestone.progress_percentage:.0%} there.",
            ProgressStage.SIGNIFICANT_PROGRESS: f"Wonderful progress in {milestone.milestone_type}! You're {milestone.progress_percentage:.0%} complete.",
            ProgressStage.MAJOR_MILESTONE: f"Remarkable growth! Your {milestone.milestone_type} goal is {milestone.progress_percentage:.0%} complete!",
            ProgressStage.GOAL_ACHIEVED: f"🌟 Wellness goal achieved! You've mastered {milestone.milestone_type}!"
        }
        
        return messages.get(stage, f"Continue nurturing your {milestone.milestone_type} progress!")
    
    async def _generate_general_motivational_visualization(
        self,
        user_id: str,
        goal_data: Dict[str, Any],
        progress_data: Dict[str, Any],
        user_context: Dict[str, Any]
    ) -> ProgressVisualization:
        """Generate general motivational visualization for uncategorized goals."""
        progress_percentage = progress_data.get('progress_percentage', 0.0)
        progress_stage = self._determine_progress_stage(progress_percentage)
        
        # Generate motivational scene
        primary_image = await self.visual_generator.generate_motivational_scene(
            VisionCategory.PRODUCTIVITY, user_context
        )
        
        # Create visualization
        visualization = ProgressVisualization(
            id=f"general_{user_id}_{datetime.now().timestamp()}",
            user_id=user_id,
            goal_id=goal_data.get('id', 'general_goal'),
            visualization_type=VisualizationType.MOTIVATIONAL_FUTURE,
            progress_stage=progress_stage,
            primary_image=primary_image,
            supporting_images=[],
            progress_metrics=progress_data,
            contextual_message=f"Keep pushing towards your {goal_data.get('title', 'goal')}! You're {progress_percentage:.0%} there.",
            generated_at=datetime.now(),
            expires_at=datetime.now() + self.cache_duration,
            metadata={
                'category': 'general',
                'goal_type': goal_data.get('type', 'general')
            }
        )
        
        return visualization
    
    def get_visualization_stats(self) -> Dict[str, Any]:
        """Get visualization generation statistics."""
        return {
            'cached_visualizations': len(self.visualization_cache),
            'cache_duration_hours': self.cache_duration.total_seconds() / 3600,
            'progress_stages_supported': len(self.progress_thresholds),
            'visualization_types_supported': len(VisualizationType),
            'categories_supported': ['health', 'financial', 'wellness', 'general']
        }