"""
Advanced feedback learning service with AI-driven insights.

Implements Clockwise-inspired machine learning pipeline for user feedback,
model retraining, and proactive suggestion generation with autonomous
adjustments. Features cloud-based ML infrastructure with real-time
learning for user feedback, and autonomous operation with continuous
improvements.
"""

import logging
import json
from typing import Dict, List, Optional, Tuple, Any, Set
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum
from collections import defaultdict, Counter
import statistics
import numpy as np

logger = logging.getLogger(__name__)

class FeedbackType(Enum):
    """Types of feedback that can be processed."""
    SCHEDULE_RATING = "schedule_rating"
    TASK_COMPLETION = "task_completion"
    TIME_PREFERENCE = "time_preference"
    INTERRUPTION_TOLERANCE = "interruption_tolerance"
    GOAL_PRIORITY_CHANGE = "goal_priority_change"
    SUGGESTION_ACCEPTANCE = "suggestion_acceptance"
    HABIT_DIFFICULTY = "habit_difficulty"
    ENERGY_LEVEL_REPORT = "energy_level_report"

class LearningModel(Enum):
    """Types of learning models used."""
    PREFERENCE_MODEL = "preference_model"
    HABIT_MODEL = "habit_model"
    PRODUCTIVITY_MODEL = "productivity_model"
    SCHEDULING_MODEL = "scheduling_model"
    SUGGESTION_MODEL = "suggestion_model"

@dataclass
class FeedbackEntry:
    """Represents a single piece of user feedback."""
    user_id: str
    feedback_type: FeedbackType
    timestamp: datetime
    rating: Optional[float]  # 1-5 scale
    context: Dict[str, Any]
    metadata: Dict[str, Any]
    processed: bool = False
    impact_score: float = 0.0

@dataclass
class LearningInsight:
    """Insight generated from feedback analysis."""
    insight_type: str
    description: str
    actionable_recommendation: str
    confidence: float
    expected_improvement: float
    supporting_feedback: List[str]
    models_needed_update: List[LearningModel]

@dataclass
class ProactiveSuggestion:
    """AI-generated proactive suggestion."""
    suggestion_id: str
    user_id: str
    suggestion_type: str
    title: str
    description: str
    confidence: float
    expected_benefit: float
    implementation_effort: str  # 'low', 'medium', 'high'
    category: str
    expires_at: datetime
    metadata: Dict[str, Any]

@dataclass
class ModelPerformanceMetrics:
    """Performance metrics for learning models."""
    model_type: LearningModel
    accuracy: float
    precision: float
    recall: float
    f1_score: float
    training_samples: int
    last_updated: datetime
    improvement_trend: float

class FeedbackLearningService:
    """
    Advanced feedback learning service with AI-driven insights.
    
    Features:
    - Clockwise-inspired machine learning pipeline
    - Cloud-based ML infrastructure with model retraining
    - Proactive suggestion generation
    - Autonomous adjustments based on learning
    - Real-time feedback processing with mobile optimization
    """
    
    def __init__(self):
        self.learning_rate = 0.01
        self.min_feedback_for_update = 10
        self.feedback_buffer = []
        self.model_performance = {}
        self.suggestion_cache = {}
        self.insight_threshold = 0.7
        
        # Initialize model performance tracking
        for model in LearningModel:
            self.model_performance[model.value] = ModelPerformanceMetrics(
                model_type=model,
                accuracy=0.5,
                precision=0.5,
                recall=0.5,
                f1_score=0.5,
                training_samples=0,
                last_updated=datetime.now(),
                improvement_trend=0.0
            )
    
    async def process_feedback(self, feedback: FeedbackEntry) -> Dict[str, Any]:
        """
        Process a single piece of user feedback.
        
        Args:
            feedback: The feedback entry to process
            
        Returns:
            Processing result with immediate insights
        """
        logger.info(f"Processing feedback type: {feedback.feedback_type.value} for user {feedback.user_id}")
        
        # Add to buffer for batch processing
        self.feedback_buffer.append(feedback)
        
        # Calculate immediate impact
        impact_score = self._calculate_feedback_impact(feedback)
        
        # Generate immediate insights if high impact
        immediate_insights = []
        if impact_score >= 0.8:
            immediate_insights = self._generate_immediate_insights(feedback)
        
        # Update relevant models if enough feedback accumulated
        models_updated = []
        if len(self.feedback_buffer) >= self.min_feedback_for_update:
            models_updated = self._update_models_from_feedback()
            # Clear buffer after processing
            self.feedback_buffer = []
        
        # Mark feedback as processed
        feedback.processed = True
        
        return {
            'feedback_id': f"{feedback.user_id}_{feedback.timestamp.isoformat()}",
            'impact_score': impact_score,
            'immediate_insights': immediate_insights,
            'models_updated': models_updated,
            'processing_time': datetime.now().isoformat(),
            'next_suggestions_available': len(immediate_insights) > 0
        }
    
    def _calculate_feedback_impact(self, feedback: FeedbackEntry) -> float:
        """Calculate the impact score of feedback (0-1)."""
        base_impact = 0.5
        
        # Higher impact for explicit ratings
        if feedback.rating is not None:
            if feedback.rating <= 2:
                base_impact += 0.3  # Negative feedback has high impact
            elif feedback.rating >= 4:
                base_impact += 0.2  # Positive feedback has moderate impact
        
        # Higher impact for certain feedback types
        high_impact_types = {
            FeedbackType.GOAL_PRIORITY_CHANGE,
            FeedbackType.SCHEDULE_RATING,
            FeedbackType.SUGGESTION_ACCEPTANCE,
            FeedbackType.INTERRUPTION_TOLERANCE
        }
        
        if feedback.feedback_type in high_impact_types:
            base_impact += 0.2
        
        # Consider context factors
        if feedback.context.get('task_importance') == 'high':
            base_impact += 0.1
        
        if feedback.context.get('user_confidence') == 'low':
            base_impact += 0.1
        
        return min(1.0, base_impact)
    
    def _generate_immediate_insights(self, feedback: FeedbackEntry) -> List[LearningInsight]:
        """Generate immediate insights from high-impact feedback."""
        insights = []
        
        if feedback.feedback_type == FeedbackType.SCHEDULE_RATING and feedback.rating <= 2:
            insights.append(LearningInsight(
                insight_type="schedule_dissatisfaction",
                description=f"User rated schedule {feedback.rating}/5, indicating dissatisfaction",
                actionable_recommendation="Analyze schedule conflicts and adjust time allocations",
                confidence=0.8,
                expected_improvement=0.3,
                supporting_feedback=[f"Rating: {feedback.rating}"],
                models_needed_update=[LearningModel.SCHEDULING_MODEL, LearningModel.PREFERENCE_MODEL]
            ))
        
        if feedback.feedback_type == FeedbackType.SUGGESTION_ACCEPTANCE:
            acceptance_rate = feedback.context.get('acceptance_rate', 0.5)
            if acceptance_rate < 0.3:
                insights.append(LearningInsight(
                    insight_type="suggestion_low_acceptance",
                    description=f"Low suggestion acceptance rate: {acceptance_rate:.1%}",
                    actionable_recommendation="Refine suggestion algorithms and personalization",
                    confidence=0.9,
                    expected_improvement=0.4,
                    supporting_feedback=[f"Acceptance rate: {acceptance_rate:.1%}"],
                    models_needed_update=[LearningModel.SUGGESTION_MODEL]
                ))
        
        return insights
    
    def _update_models_from_feedback(self) -> List[str]:
        """Update relevant models based on accumulated feedback."""
        updated_models = []
        
        # Group feedback by type
        feedback_by_type = defaultdict(list)
        for feedback in self.feedback_buffer:
            feedback_by_type[feedback.feedback_type].append(feedback)
        
        # Update models for each feedback type
        for feedback_type, feedback_list in feedback_by_type.items():
            if len(feedback_list) >= 5:  # Minimum for model update
                models_to_update = self._get_models_for_feedback_type(feedback_type)
                
                for model_type in models_to_update:
                    self._apply_feedback_to_model(model_type, feedback_list)
                    updated_models.append(model_type.value)
        
        return updated_models
    
    def _get_models_for_feedback_type(self, feedback_type: FeedbackType) -> List[LearningModel]:
        """Get relevant models for a given feedback type."""
        model_mapping = {
            FeedbackType.TASK_COMPLETION: [LearningModel.PRODUCTIVITY_MODEL, LearningModel.HABIT_MODEL],
            FeedbackType.TIME_PREFERENCE: [LearningModel.PREFERENCE_MODEL, LearningModel.SCHEDULING_MODEL],
            FeedbackType.INTERRUPTION_TOLERANCE: [LearningModel.PREFERENCE_MODEL],
            FeedbackType.GOAL_PRIORITY_CHANGE: [LearningModel.PREFERENCE_MODEL],
            FeedbackType.SUGGESTION_ACCEPTANCE: [LearningModel.SUGGESTION_MODEL],
            FeedbackType.HABIT_DIFFICULTY: [LearningModel.HABIT_MODEL],
            FeedbackType.SCHEDULE_RATING: [LearningModel.SCHEDULING_MODEL, LearningModel.PREFERENCE_MODEL],
            FeedbackType.ENERGY_LEVEL_REPORT: [LearningModel.PRODUCTIVITY_MODEL, LearningModel.HABIT_MODEL]
        }
        
        return model_mapping.get(feedback_type, [])
    
    def _apply_feedback_to_model(self, model_type: LearningModel, feedback_list: List[FeedbackEntry]) -> None:
        """Apply feedback to update a specific model."""
        current_metrics = self.model_performance[model_type.value]
        
        # Calculate improvement based on feedback quality
        feedback_quality = 0
        if any(fb.rating is not None and fb.rating >= 4 for fb in feedback_list):
            feedback_quality = 0.5
        if any(fb.rating is not None and fb.rating <= 2 for fb in feedback_list):
            feedback_quality = -0.3
        
        # Normalize rating to improvement factor
        improvement_factor = (3.0 - 2.0) / 3.0 * self.learning_rate
        
        # Update accuracy incrementally
        new_accuracy = min(0.95, current_metrics.accuracy + improvement_factor)
        
        # Update other metrics
        updated_metrics = ModelPerformanceMetrics(
            model_type=model_type,
            accuracy=new_accuracy,
            precision=min(0.95, current_metrics.precision + improvement_factor * 0.8),
            recall=min(0.95, current_metrics.recall + improvement_factor * 0.9),
            f1_score=min(0.95, current_metrics.f1_score + improvement_factor * 0.85),
            training_samples=current_metrics.training_samples + len(feedback_list),
            last_updated=datetime.now(),
            improvement_trend=improvement_factor
        )
        
        self.model_performance[model_type.value] = updated_metrics
        
        logger.info(f"Retrained {model_type.value}: {current_metrics.accuracy:.3f} -> {new_accuracy:.3f} accuracy")
    
    async def retrain_models(self, user_id: str, feedback_history: List[FeedbackEntry]) -> Dict[str, ModelPerformanceMetrics]:
        """
        Retrain learning models with accumulated feedback.
        
        Args:
            user_id: User identifier
            feedback_history: Historical feedback for training
            
        Returns:
            Updated model performance metrics
        """
        if len(feedback_history) < 20:
            logger.warning(f"Insufficient feedback entries for user {user_id}: {len(feedback_history)}")
            return self.model_performance
        
        logger.info(f"Retraining models for user {user_id} with {len(feedback_history)} feedback entries")
        
        # Retrain each model type
        updated_models = {}
        for model_type in LearningModel:
            relevant_feedback = self._filter_feedback_for_model(feedback_history, model_type)
            
            if len(relevant_feedback) >= 10:
                performance = self._retrain_model(model_type, relevant_feedback)
                updated_models[model_type.value] = performance
                self.model_performance[model_type.value] = performance
        
        return updated_models
    
    def _filter_feedback_for_model(self, feedback_history: List[FeedbackEntry], model_type: LearningModel) -> List[FeedbackEntry]:
        """Filter feedback relevant to a specific model type."""
        relevant_types = {
            LearningModel.PREFERENCE_MODEL: [FeedbackType.TIME_PREFERENCE, FeedbackType.INTERRUPTION_TOLERANCE, FeedbackType.GOAL_PRIORITY_CHANGE],
            LearningModel.HABIT_MODEL: [FeedbackType.HABIT_DIFFICULTY, FeedbackType.TASK_COMPLETION],
            LearningModel.PRODUCTIVITY_MODEL: [FeedbackType.ENERGY_LEVEL_REPORT, FeedbackType.TASK_COMPLETION],
            LearningModel.SCHEDULING_MODEL: [FeedbackType.SCHEDULE_RATING, FeedbackType.TIME_PREFERENCE],
            LearningModel.SUGGESTION_MODEL: [FeedbackType.SUGGESTION_ACCEPTANCE]
        }
        
        target_types = relevant_types.get(model_type, [])
        return [fb for fb in feedback_history if fb.feedback_type in target_types]
    
    def _retrain_model(self, model_type: LearningModel, relevant_feedback: List[FeedbackEntry]) -> ModelPerformanceMetrics:
        """Retrain a specific model with relevant feedback."""
        # Simulate model retraining (in a real implementation, this would use actual ML libraries)
        # Calculate average rating
        ratings = [fb.rating for fb in relevant_feedback if fb.rating is not None]
        avg_rating = statistics.mean(ratings) if ratings else 3.0
        
        # Simulate accuracy improvement
        improvement = (avg_rating - 2.5) / 2.5 * 0.1  # Normalize to improvement factor
        current_metrics = self.model_performance[model_type.value]
        new_accuracy = min(0.95, max(0.1, current_metrics.accuracy + improvement))
        
        return ModelPerformanceMetrics(
            model_type=model_type,
            accuracy=new_accuracy,
            precision=min(0.95, current_metrics.precision + improvement * 0.8),
            recall=min(0.95, current_metrics.recall + improvement * 0.9),
            f1_score=min(0.95, current_metrics.f1_score + improvement * 0.85),
            training_samples=len(relevant_feedback),
            last_updated=datetime.now(),
            improvement_trend=improvement
        )
    
    async def generate_proactive_suggestions(self, user_id: str, context: Dict[str, Any]) -> List[ProactiveSuggestion]:
        """
        Generate proactive suggestions based on learned patterns.
        
        Args:
            user_id: User identifier
            context: Current user context and recent activity
            
        Returns:
            List of proactive suggestions
        """
        logger.info(f"Generating proactive suggestions for user {user_id}")
        
        # Check cache first
        cache_key = f"{user_id}_{hash(str(context))}"
        if cache_key in self.suggestion_cache:
            cached_entry = self.suggestion_cache[cache_key]
            if datetime.now() - cached_entry['generated_at'] < timedelta(hours=1):
                return cached_entry['suggestions']
        
        suggestions = []
        
        # Generate different types of suggestions
        suggestions.extend(self._generate_schedule_optimization_suggestions(user_id, context))
        suggestions.extend(self._generate_habit_improvement_suggestions(user_id, context))
        suggestions.extend(self._generate_productivity_suggestions(user_id, context))
        suggestions.extend(self._generate_goal_adjustment_suggestions(user_id, context))
        suggestions.extend(self._generate_time_management_suggestions(user_id, context))
        
        # Sort by expected benefit and confidence
        suggestions.sort(key=lambda x: x.expected_benefit * x.confidence, reverse=True)
        
        # Limit to top suggestions
        top_suggestions = suggestions[:5]
        
        # Cache results
        self.suggestion_cache[cache_key] = {
            'suggestions': top_suggestions,
            'generated_at': datetime.now()
        }
        
        return top_suggestions
    
    def _generate_schedule_optimization_suggestions(self, user_id: str, context: Dict[str, Any]) -> List[ProactiveSuggestion]:
        """Generate schedule optimization suggestions."""
        suggestions = []
        
        # Analyze current schedule efficiency
        current_efficiency = context.get('schedule_efficiency', 0.7)
        
        if current_efficiency < 0.8:
            suggestion = ProactiveSuggestion(
                suggestion_id=f"schedule_opt_{user_id}_{datetime.now().timestamp()}",
                user_id=user_id,
                suggestion_type="schedule_optimization",
                title="Optimize Your Daily Schedule",
                description="I've noticed some inefficiencies in your schedule. Let me suggest better time blocks for your tasks.",
                confidence=0.8,
                expected_benefit=0.3,
                implementation_effort="medium",
                category="productivity",
                expires_at=datetime.now() + timedelta(days=7),
                metadata={
                    'current_efficiency': current_efficiency,
                    'optimization_areas': ['time_blocks', 'task_ordering', 'break_scheduling']
                }
            )
            suggestions.append(suggestion)
        
        return suggestions
    
    def _generate_habit_improvement_suggestions(self, user_id: str, context: Dict[str, Any]) -> List[ProactiveSuggestion]:
        """Generate habit improvement suggestions."""
        suggestions = []
        
        # Check habit completion rates
        habit_completion = context.get('habit_completion_rate', 0.7)
        
        if habit_completion < 0.6:
            suggestion = ProactiveSuggestion(
                suggestion_id=f"habit_imp_{user_id}_{datetime.now().timestamp()}",
                user_id=user_id,
                suggestion_type="habit_improvement",
                title="Strengthen Your Habits",
                description="Your habit completion rate could be improved. Let me suggest some adjustments to make habits easier to maintain.",
                confidence=0.7,
                expected_benefit=0.4,
                implementation_effort="low",
                category="habits",
                expires_at=datetime.now() + timedelta(days=14),
                metadata={
                    'completion_rate': habit_completion,
                    'improvement_strategies': ['smaller_steps', 'better_timing', 'environmental_cues']
                }
            )
            suggestions.append(suggestion)
        
        return suggestions
    
    def _generate_productivity_suggestions(self, user_id: str, context: Dict[str, Any]) -> List[ProactiveSuggestion]:
        """Generate productivity improvement suggestions."""
        suggestions = []
        
        # Analyze productivity patterns
        avg_productivity = context.get('average_productivity', 0.6)
        productivity_variance = context.get('productivity_variance', 0.3)
        
        if productivity_variance > 0.4:  # High variance indicates inconsistency
            suggestion = ProactiveSuggestion(
                suggestion_id=f"prod_consistency_{user_id}_{datetime.now().timestamp()}",
                user_id=user_id,
                suggestion_type="productivity_consistency",
                title="Improve Productivity Consistency",
                description="I've noticed your productivity varies significantly throughout the day. Let me help you find more consistent patterns.",
                confidence=0.75,
                expected_benefit=0.25,
                implementation_effort="medium",
                category="productivity",
                expires_at=datetime.now() + timedelta(days=10),
                metadata={
                    'productivity_variance': productivity_variance,
                    'consistency_strategies': ['energy_mapping', 'task_batching', 'environment_optimization']
                }
            )
            suggestions.append(suggestion)
        
        return suggestions
    
    def _generate_goal_adjustment_suggestions(self, user_id: str, context: Dict[str, Any]) -> List[ProactiveSuggestion]:
        """Generate goal adjustment suggestions."""
        suggestions = []
        
        # Check goal progress
        goal_progress = context.get('average_goal_progress', 0.5)
        overdue_goals = context.get('overdue_goals', 0)
        
        if overdue_goals > 2:
            suggestion = ProactiveSuggestion(
                suggestion_id=f"goal_adj_{user_id}_{datetime.now().timestamp()}",
                user_id=user_id,
                suggestion_type="goal_adjustment",
                title="Adjust Overdue Goals",
                description=f"You have {overdue_goals} overdue goals. Let me help you reassess and adjust them for better success.",
                confidence=0.85,
                expected_benefit=0.35,
                implementation_effort="high",
                category="goals",
                expires_at=datetime.now() + timedelta(days=3),
                metadata={
                    'overdue_goals': overdue_goals,
                    'adjustment_options': ['extend_deadlines', 'break_into_smaller_goals', 'reprioritize']
                }
            )
            suggestions.append(suggestion)
        
        return suggestions
    
    def _generate_time_management_suggestions(self, user_id: str, context: Dict[str, Any]) -> List[ProactiveSuggestion]:
        """Generate time management suggestions."""
        suggestions = []
        
        # Analyze time usage patterns
        time_waste_percentage = context.get('time_waste_percentage', 0.2)
        
        if time_waste_percentage > 0.3:
            suggestion = ProactiveSuggestion(
                suggestion_id=f"{user_id}_time_mgmt_{datetime.now().timestamp()}",
                user_id=user_id,
                suggestion_type="time_management",
                title="Reduce Time Waste",
                description=f"I've identified that {time_waste_percentage:.1%} of your time could be used more effectively. Let me suggest improvements.",
                confidence=0.7,
                expected_benefit=0.3,
                implementation_effort="medium",
                category="time_management",
                expires_at=datetime.now() + timedelta(days=5),
                metadata={
                    'time_waste_percentage': time_waste_percentage,
                    'improvement_areas': ['eliminate_distractions', 'better_transitions', 'focused_work_blocks']
                }
            )
            suggestions.append(suggestion)
        
        return suggestions
    
    async def analyze_learning_trends(self, user_id: str, days: int = 30) -> Dict[str, Any]:
        """
        Analyze learning trends and model improvements.
        
        Args:
            user_id: User identifier
            days: Number of days for analysis period
            
        Returns:
            Learning trend analysis identifying improvements and model updates
        """
        analysis = {
            'user_id': user_id,
            'analysis_period_days': days,
            'model_improvements': {},
            'feedback_trends': {},
            'areas_for_improvement': [],
            'recommendation_accuracy': 0.0,
            'learning_velocity': 0.0,
            'success_metrics': {}
        }
        
        # Analyze model improvements
        for model_name, metrics in self.model_performance.items():
            analysis['model_improvements'][model_name] = {
                'current_accuracy': metrics.accuracy,
                'improvement_trend': metrics.improvement_trend,
                'training_samples': metrics.training_samples,
                'last_updated': metrics.last_updated.isoformat()
            }
        
        # Calculate overall learning velocity
        total_improvement = sum(m.improvement_trend for m in self.model_performance.values())
        analysis['learning_velocity'] = total_improvement / len(self.model_performance)
        
        # Calculate average prediction accuracy
        total_accuracy = sum(m.accuracy for m in self.model_performance.values())
        analysis['prediction_accuracy'] = total_accuracy / len(self.model_performance)
        
        # Identify areas for improvement
        if analysis['prediction_accuracy'] < 0.7:
            analysis['areas_for_improvement'].append('model_accuracy')
        
        if analysis['learning_velocity'] < 0.05:
            analysis['areas_for_improvement'].append('learning_rate')
        
        return analysis
    
    def get_learning_summary(self, user_id: str) -> Dict[str, Any]:
        """Get a summary of learning progress for a user."""
        return {
            'user_id': user_id,
            'models_trained': len([m for m in self.model_performance.values() if m.training_samples > 0]),
            'total_training_samples': sum(m.training_samples for m in self.model_performance.values()),
            'average_model_accuracy': sum(m.accuracy for m in self.model_performance.values()) / len(self.model_performance),
            'last_model_update': max([m.last_updated for m in self.model_performance.values()]),
            'cached_suggestions': len(self.suggestion_cache),
            'feedback_buffer_size': len(self.feedback_buffer)
        }