import json
import re
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from models import KnowledgeEntry, UserFeedback, ScheduleBlock
from database import Vision
import logging
from collections import defaultdict, Counter
import asyncio

logger = logging.getLogger(__name__)

class AIProcessingService:
    """Core AI service for learning user preferences and generating insights"""
    
    def __init__(self):
        self.category_weights = {
            'financial': 1.2,
            'health': 1.1, 
            'nutrition': 1.0,
            'psychological': 1.0,
            'task': 0.8
        }
        
        self.time_patterns = {
            'morning': ['morning', 'am', 'early', 'dawn', 'sunrise'],
            'afternoon': ['afternoon', 'pm', 'lunch', 'midday'],
            'evening': ['evening', 'night', 'dinner', 'sunset'],
            'weekend': ['weekend', 'saturday', 'sunday'],
            'weekday': ['weekday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday']
        }
    
    async def analyze_user_patterns(self, user_id: str, db: AsyncSession) -> Dict[str, Any]:
        """Analyze user behavior patterns from historical data"""
        try:
            # Get user's knowledge entries
            knowledge_query = select(KnowledgeEntry).where(KnowledgeEntry.user_id == user_id)
            knowledge_result = await db.execute(knowledge_query)
            knowledge_entries = knowledge_result.scalars().all()
            
            # Get user's schedule history
            schedule_query = select(ScheduleBlock).join(
                # TODO: Add proper join with Schedule table
            ).where(ScheduleBlock.status.in_(['completed', 'in-progress']))
            
            patterns = {
                'preferred_times': self._analyze_time_preferences(knowledge_entries),
                'goal_priorities': self._analyze_goal_priorities(knowledge_entries),
                'activity_frequency': self._analyze_activity_frequency(knowledge_entries),
                'success_factors': self._analyze_success_factors(knowledge_entries)
            }
            
            return patterns
            
        except Exception as e:
            logger.error(f"Error analyzing user patterns: {str(e)}")
            return self._get_default_patterns()
    
    async def generate_suggestions(self, user_id: str, context: Dict[str, Any], db: AsyncSession) -> List[Dict[str, Any]]:
        """Generate personalized suggestions based on user patterns and context"""
        try:
            patterns = await self.analyze_user_patterns(user_id, db)
            
            suggestions = []
            
            # Generate time-based suggestions
            time_suggestions = self._generate_time_suggestions(patterns, context)
            suggestions.extend(time_suggestions)
            
            # Generate goal-based suggestions
            goal_suggestions = self._generate_goal_suggestions(patterns, context)
            suggestions.extend(goal_suggestions)
            
            # Generate habit suggestions
            habit_suggestions = self._generate_habit_suggestions(patterns, context)
            suggestions.extend(habit_suggestions)
            
            # Rank suggestions by relevance
            ranked_suggestions = self._rank_suggestions(suggestions, patterns)
            
            return ranked_suggestions[:10]  # Return top 10 suggestions
            
        except Exception as e:
            logger.error(f"Error generating suggestions: {str(e)}")
            return []
    
    async def update_personalization_model(self, user_id: str, feedback: Dict[str, Any], db: AsyncSession) -> None:
        """Update personalization model based on user feedback"""
        try:
            # Store feedback in database
            feedback_entry = UserFeedback(
                user_id=user_id,
                feedback_type=feedback.get('type', 'general'),
                context=feedback.get('context', {}),
                rating=feedback.get('rating'),
                comments=feedback.get('comments')
            )
            
            db.add(feedback_entry)
            await db.commit()
            
            # TODO: Implement model retraining logic
            logger.info(f"Updated personalization model for user {user_id}")
            
        except Exception as e:
            logger.error(f"Error updating personalization model: {str(e)}")
            await db.rollback()
    
    def categorize_content(self, content: str) -> Dict[str, Any]:
        """Categorize content using NLP-based classification"""
        content_lower = content.lower()
        
        # Enhanced keyword matching with context
        category_scores = defaultdict(float)
        
        # Financial keywords with context
        financial_patterns = [
            r'\b(save|saving|savings)\b.*\b(money|dollar|budget)\b',
            r'\b(invest|investment|portfolio)\b',
            r'\b(budget|budgeting|expense|income)\b',
            r'\b(debt|credit|loan|mortgage)\b'
        ]
        
        health_patterns = [
            r'\b(exercise|workout|gym|fitness)\b',
            r'\b(run|running|jog|jogging)\b.*\b(daily|weekly)\b',
            r'\b(weight|lose|gain)\b.*\b(pounds|kg|lbs)\b',
            r'\b(doctor|medical|health)\b'
        ]
        
        nutrition_patterns = [
            r'\b(eat|eating|meal|food)\b.*\b(healthy|nutrition)\b',
            r'\b(diet|dieting|calories|protein)\b',
            r'\b(cook|cooking|recipe)\b',
            r'\b(breakfast|lunch|dinner)\b.*\b(plan|planning)\b'
        ]
        
        psychological_patterns = [
            r'\b(meditat|meditation|mindful)\b',
            r'\b(stress|anxiety|mental|mood)\b',
            r'\b(therapy|counseling|wellbeing)\b',
            r'\b(relax|relaxation|calm)\b'
        ]
        
        pattern_categories = {
            'financial': financial_patterns,
            'health': health_patterns,
            'nutrition': nutrition_patterns,
            'psychological': psychological_patterns
        }
        
        # Score based on pattern matching
        for category, patterns in pattern_categories.items():
            for pattern in patterns:
                matches = len(re.findall(pattern, content_lower))
                category_scores[category] += matches * 2  # Pattern matches get higher weight
        
        # Add simple keyword scoring
        from upload_service import UploadProcessingService
        upload_service = UploadProcessingService()
        simple_category = upload_service._categorize_content(content)
        category_scores[simple_category] += 1
        
        # Determine final category
        if not category_scores:
            final_category = 'task'
            confidence = 0.3
        else:
            final_category = max(category_scores, key=category_scores.get)
            max_score = category_scores[final_category]
            total_score = sum(category_scores.values())
            confidence = min(0.95, max_score / max(total_score, 1) + 0.2)
        
        return {
            'category': final_category,
            'confidence': confidence,
            'scores': dict(category_scores)
        }
    
    def _analyze_time_preferences(self, knowledge_entries: List[KnowledgeEntry]) -> List[Dict[str, Any]]:
        """Analyze preferred times from knowledge entries"""
        time_preferences = []
        
        for entry in knowledge_entries:
            content = entry.content.lower()
            
            for time_period, keywords in self.time_patterns.items():
                for keyword in keywords:
                    if keyword in content:
                        time_preferences.append({
                            'period': time_period,
                            'activity_type': entry.category,
                            'confidence': 0.7
                        })
        
        # Aggregate and rank preferences
        preference_counts = Counter((pref['period'], pref['activity_type']) for pref in time_preferences)
        
        ranked_preferences = []
        for (period, activity_type), count in preference_counts.most_common():
            ranked_preferences.append({
                'period': period,
                'activity_type': activity_type,
                'frequency': count,
                'confidence': min(0.9, count * 0.2 + 0.3)
            })
        
        return ranked_preferences[:10]
    
    def _analyze_goal_priorities(self, knowledge_entries: List[KnowledgeEntry]) -> List[Dict[str, Any]]:
        """Analyze goal priorities from user data"""
        category_counts = Counter(entry.category for entry in knowledge_entries)
        total_entries = len(knowledge_entries)
        
        priorities = []
        for category, count in category_counts.items():
            priority_score = (count / max(total_entries, 1)) * self.category_weights.get(category, 1.0)
            priorities.append({
                'category': category,
                'priority_score': priority_score,
                'entry_count': count,
                'weight': self.category_weights.get(category, 1.0)
            })
        
        return sorted(priorities, key=lambda x: x['priority_score'], reverse=True)
    
    def _analyze_activity_frequency(self, knowledge_entries: List[KnowledgeEntry]) -> List[Dict[str, Any]]:
        """Analyze activity frequency patterns"""
        frequency_keywords = {
            'daily': ['daily', 'every day', 'each day'],
            'weekly': ['weekly', 'every week', 'once a week'],
            'monthly': ['monthly', 'every month', 'once a month'],
            'occasional': ['sometimes', 'occasionally', 'when possible']
        }
        
        frequencies = []
        
        for entry in knowledge_entries:
            content = entry.content.lower()
            
            for freq_type, keywords in frequency_keywords.items():
                for keyword in keywords:
                    if keyword in content:
                        frequencies.append({
                            'frequency': freq_type,
                            'category': entry.category,
                            'content_snippet': content[:100] + '...' if len(content) > 100 else content
                        })
        
        return frequencies
    
    def _analyze_success_factors(self, knowledge_entries: List[KnowledgeEntry]) -> List[Dict[str, Any]]:
        """Analyze factors that contribute to success"""
        success_keywords = [
            'successful', 'achieved', 'completed', 'accomplished', 'reached goal',
            'worked well', 'effective', 'helpful', 'motivated', 'consistent'
        ]
        
        failure_keywords = [
            'failed', 'missed', 'skipped', 'difficult', 'challenging', 
            'gave up', 'inconsistent', 'struggled'
        ]
        
        success_factors = []
        
        for entry in knowledge_entries:
            content = entry.content.lower()
            
            success_score = sum(1 for keyword in success_keywords if keyword in content)
            failure_score = sum(1 for keyword in failure_keywords if keyword in content)
            
            if success_score > 0 or failure_score > 0:
                net_score = success_score - failure_score
                success_factors.append({
                    'category': entry.category,
                    'success_score': success_score,
                    'failure_score': failure_score,
                    'net_score': net_score,
                    'content_snippet': content[:150] + '...' if len(content) > 150 else content
                })
        
        return sorted(success_factors, key=lambda x: x['net_score'], reverse=True)
    
    def _generate_time_suggestions(self, patterns: Dict[str, Any], context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate time-based suggestions"""
        suggestions = []
        
        preferred_times = patterns.get('preferred_times', [])
        
        for pref in preferred_times[:5]:  # Top 5 time preferences
            suggestions.append({
                'type': 'time_optimization',
                'title': f"Schedule {pref['activity_type']} activities in the {pref['period']}",
                'description': f"Based on your patterns, you're most successful with {pref['activity_type']} activities during {pref['period']}",
                'confidence': pref['confidence'],
                'category': pref['activity_type'],
                'priority': 'medium'
            })
        
        return suggestions
    
    def _generate_goal_suggestions(self, patterns: Dict[str, Any], context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate goal-based suggestions"""
        suggestions = []
        
        goal_priorities = patterns.get('goal_priorities', [])
        
        for priority in goal_priorities[:3]:  # Top 3 priorities
            if priority['priority_score'] > 0.3:
                suggestions.append({
                    'type': 'goal_focus',
                    'title': f"Increase focus on {priority['category']} goals",
                    'description': f"Your {priority['category']} goals show high engagement. Consider adding more activities in this area.",
                    'confidence': min(0.9, priority['priority_score']),
                    'category': priority['category'],
                    'priority': 'high' if priority['priority_score'] > 0.6 else 'medium'
                })
        
        return suggestions
    
    def _generate_habit_suggestions(self, patterns: Dict[str, Any], context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate habit-building suggestions"""
        suggestions = []
        
        activity_frequencies = patterns.get('activity_frequency', [])
        
        # Suggest daily habits for activities marked as occasional
        occasional_activities = [af for af in activity_frequencies if af['frequency'] == 'occasional']
        
        for activity in occasional_activities[:3]:
            suggestions.append({
                'type': 'habit_building',
                'title': f"Build a consistent {activity['category']} routine",
                'description': f"Consider scheduling regular {activity['category']} activities to build consistency",
                'confidence': 0.6,
                'category': activity['category'],
                'priority': 'medium'
            })
        
        return suggestions
    
    def _rank_suggestions(self, suggestions: List[Dict[str, Any]], patterns: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Rank suggestions by relevance and confidence"""
        goal_priorities = {gp['category']: gp['priority_score'] for gp in patterns.get('goal_priorities', [])}
        
        for suggestion in suggestions:
            category = suggestion.get('category', 'task')
            priority_boost = goal_priorities.get(category, 0.5)
            
            # Calculate final score
            base_confidence = suggestion.get('confidence', 0.5)
            priority_weight = {'high': 1.2, 'medium': 1.0, 'low': 0.8}.get(suggestion.get('priority', 'medium'), 1.0)
            
            suggestion['final_score'] = base_confidence * priority_boost * priority_weight
        
        return sorted(suggestions, key=lambda x: x.get('final_score', 0), reverse=True)
    
    def _get_default_patterns(self) -> Dict[str, Any]:
        """Return default patterns when analysis fails"""
        return {
            'preferred_times': [
                {'period': 'morning', 'activity_type': 'health', 'confidence': 0.5},
                {'period': 'evening', 'activity_type': 'psychological', 'confidence': 0.5}
            ],
            'goal_priorities': [
                {'category': 'health', 'priority_score': 0.8},
                {'category': 'financial', 'priority_score': 0.7}
            ],
            'activity_frequency': [],
            'success_factors': []
        }

# Global AI service instance
ai_service = AIProcessingService()