"""
Enhanced content categorization service with advanced NLP.

Implements Motion/Lindy-inspired categorization with confidence scoring
and real-time categorization with mobile optimization.
"""

import re
import json
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime
from dataclasses import dataclass
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class ContentCategory(Enum):
    """Content categories inspired by Motion/Lindy AI schedulers."""
    WORK = "work"
    PERSONAL = "personal"
    HEALTH = "health"
    FINANCE = "finance"
    LEARNING = "learning"
    SOCIAL = "social"
    TRAVEL = "travel"
    SHOPPING = "shopping"
    ENTERTAINMENT = "entertainment"
    HOUSEHOLD = "household"
    URGENT = "urgent"
    ROUTINE = "routine"


class Priority(Enum):
    """Task priority levels."""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    URGENT = 4


@dataclass
class CategoryResult:
    """Result of content categorization."""
    category: ContentCategory
    confidence: float
    priority: Priority
    keywords: List[str]
    metadata: Dict[str, Any]
    processing_time_ms: float


class ContentCategorizer:
    """
    Advanced NLP-based content categorization service.
    
    Features:
    - Motion/Lindy-inspired categorization patterns
    - Confidence scoring for reliability
    - Real-time processing optimized for mobile
    - Context-aware classification
    - Multi-language support preparation
    """
    
    def __init__(self):
        self.category_patterns = self._initialize_patterns()
        self.priority_keywords = self._initialize_priority_keywords()
        self.confidence_threshold = 0.7
        
    def _initialize_patterns(self) -> Dict[ContentCategory, List[str]]:
        """Initialize categorization patterns based on Motion/Lindy AI."""
        return {
            ContentCategory.WORK: [
                r'\b(meeting|call|presentation|project|deadline|client|boss|office|work|job|task|report|email|conference)\b',
                r'\b(standup|scrum|sprint|review|planning|development|coding|programming)\b',
                r'\b(proposal|contract|negotiation|budget|revenue|sales|marketing)\b'
            ],
            ContentCategory.PERSONAL: [
                r'\b(family|friend|personal|private|home|house|relationship|birthday|anniversary)\b',
                r'\b(hobby|interest|passion|creative|art|music|reading|writing)\b',
                r'\b(self|myself|reflection|journal|diary|meditation|mindfulness)\b'
            ],
            ContentCategory.HEALTH: [
                r'\b(doctor|appointment|medical|health|fitness|gym|workout|exercise|run|walk)\b',
                r'\b(diet|nutrition|meal|food|cooking|recipe|calories|weight|wellness)\b',
                r'\b(therapy|counseling|mental|stress|anxiety|depression|sleep|rest)\b'
            ],
            ContentCategory.FINANCE: [
                r'\b(money|budget|finance|bank|investment|savings|expense|income|tax|bill)\b',
                r'\b(payment|purchase|buy|sell|cost|price|loan|mortgage|insurance)\b',
                r'\b(retirement|401k|ira|stock|bond|portfolio|financial|advisor)\b'
            ],
            ContentCategory.LEARNING: [
                r'\b(learn|study|course|class|education|training|skill|knowledge|book|read)\b',
                r'\b(tutorial|lesson|practice|homework|assignment|exam|test|certification)\b',
                r'\b(research|investigate|explore|discover|understand|master|improve)\b'
            ],
            ContentCategory.SOCIAL: [
                r'\b(party|event|gathering|celebration|dinner|lunch|coffee|drinks|hangout)\b',
                r'\b(social|community|volunteer|charity|networking|meetup|club|group)\b',
                r'\b(wedding|funeral|graduation|reunion|festival|concert|show)\b'
            ],
            ContentCategory.TRAVEL: [
                r'\b(travel|trip|vacation|holiday|flight|hotel|booking|reservation|passport)\b',
                r'\b(destination|visit|explore|sightseeing|tour|adventure|journey)\b',
                r'\b(airport|train|bus|car|rental|accommodation|itinerary)\b'
            ],
            ContentCategory.SHOPPING: [
                r'\b(shop|buy|purchase|order|delivery|store|mall|online|amazon|grocery)\b',
                r'\b(clothes|clothing|shoes|electronics|gadget|appliance|furniture)\b',
                r'\b(gift|present|birthday|christmas|holiday|special|occasion)\b'
            ],
            ContentCategory.ENTERTAINMENT: [
                r'\b(movie|film|tv|show|series|netflix|streaming|watch|entertainment)\b',
                r'\b(game|gaming|play|fun|leisure|relax|enjoy|hobby|sport|sports)\b',
                r'\b(music|concert|theater|art|museum|gallery|exhibition|performance)\b'
            ],
            ContentCategory.HOUSEHOLD: [
                r'\b(clean|cleaning|chore|maintenance|repair|fix|organize|declutter)\b',
                r'\b(laundry|dishes|vacuum|mop|garden|yard|lawn|pet|pets|dog|cat)\b',
                r'\b(utility|electric|gas|water|internet|phone|service|provider)\b'
            ],
            ContentCategory.URGENT: [
                r'\b(urgent|emergency|asap|immediately|critical|important|deadline|due)\b',
                r'\b(crisis|problem|issue|trouble|help|support|fix|solve|resolve)\b',
                r'\b(now|today|tonight|this morning|this afternoon|right away)\b'
            ],
            ContentCategory.ROUTINE: [
                r'\b(daily|weekly|monthly|routine|regular|habit|schedule|recurring)\b',
                r'\b(morning|evening|night|breakfast|lunch|dinner|commute|drive)\b',
                r'\b(check|review|update|maintain|monitor|track|follow up)\b'
            ]
        }
    
    def _initialize_priority_keywords(self) -> Dict[Priority, List[str]]:
        """Initialize priority detection keywords."""
        return {
            Priority.URGENT: [
                'urgent', 'emergency', 'asap', 'critical', 'immediately', 'crisis',
                'deadline today', 'due today', 'overdue', 'late', 'rush'
            ],
            Priority.HIGH: [
                'important', 'high priority', 'deadline', 'due soon', 'meeting',
                'presentation', 'client', 'boss', 'interview', 'appointment'
            ],
            Priority.MEDIUM: [
                'moderate', 'normal', 'standard', 'regular', 'planned', 'scheduled',
                'routine', 'follow up', 'review', 'check'
            ],
            Priority.LOW: [
                'low priority', 'when possible', 'eventually', 'someday', 'maybe',
                'nice to have', 'optional', 'leisure', 'hobby', 'entertainment'
            ]
        }
    
    def categorize_content(self, content: str, context: Optional[Dict[str, Any]] = None) -> CategoryResult:
        """
        Categorize content using advanced NLP patterns.
        
        Args:
            content: Text content to categorize
            context: Optional context information (time, location, user preferences)
            
        Returns:
            CategoryResult with category, confidence, and metadata
        """
        start_time = datetime.now()
        
        # Normalize content for processing
        normalized_content = self._normalize_content(content)
        
        # Extract keywords and patterns
        keywords = self._extract_keywords(normalized_content)
        
        # Calculate category scores
        category_scores = self._calculate_category_scores(normalized_content, keywords)
        
        # Determine best category and confidence
        best_category, confidence = self._select_best_category(category_scores)
        
        # Determine priority
        priority = self._determine_priority(normalized_content, keywords, context)
        
        # Apply context-based adjustments
        if context:
            best_category, confidence = self._apply_context_adjustments(
                best_category, confidence, context, normalized_content
            )
        
        # Calculate processing time
        processing_time = (datetime.now() - start_time).total_seconds() * 1000
        
        # Prepare metadata
        metadata = {
            'original_content': content,
            'normalized_content': normalized_content,
            'category_scores': {cat.value: score for cat, score in category_scores.items()},
            'context_applied': context is not None,
            'timestamp': datetime.now().isoformat()
        }
        
        return CategoryResult(
            category=best_category,
            confidence=confidence,
            priority=priority,
            keywords=keywords,
            metadata=metadata,
            processing_time_ms=processing_time
        )
    
    def _normalize_content(self, content: str) -> str:
        """Normalize content for consistent processing."""
        # Convert to lowercase
        normalized = content.lower().strip()
        
        # Remove extra whitespace
        normalized = re.sub(r'\s+', ' ', normalized)
        
        # Remove special characters but keep important punctuation
        normalized = re.sub(r'[^\w\s\-\.\,\!\?]', ' ', normalized)
        
        return normalized
    
    def _extract_keywords(self, content: str) -> List[str]:
        """Extract relevant keywords from content."""
        # Simple keyword extraction - can be enhanced with NLP libraries
        words = content.split()
        
        # Filter out common stop words
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have',
            'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should',
            'may', 'might', 'can', 'this', 'that', 'these', 'those', 'i', 'you',
            'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them'
        }
        
        keywords = [word for word in words if len(word) > 2 and word not in stop_words]
        
        # Return unique keywords, limited for mobile optimization
        return list(set(keywords))[:20]
    
    def _calculate_category_scores(self, content: str, keywords: List[str]) -> Dict[ContentCategory, float]:
        """Calculate scores for each category based on pattern matching."""
        scores = {}
        
        for category, patterns in self.category_patterns.items():
            score = 0.0
            matches = 0
            
            for pattern in patterns:
                # Count pattern matches
                pattern_matches = len(re.findall(pattern, content, re.IGNORECASE))
                if pattern_matches > 0:
                    matches += pattern_matches
                    score += pattern_matches * 0.3  # Base score per match
            
            # Boost score based on keyword relevance
            for keyword in keywords:
                for pattern in patterns:
                    if re.search(pattern, keyword, re.IGNORECASE):
                        score += 0.2
            
            # Normalize score (0-1 range)
            if matches > 0:
                score = min(score / len(patterns), 1.0)
            
            scores[category] = score
        
        return scores
    
    def _select_best_category(self, category_scores: Dict[ContentCategory, float]) -> Tuple[ContentCategory, float]:
        """Select the best category and calculate confidence."""
        if not category_scores:
            return ContentCategory.PERSONAL, 0.5
        
        # Sort categories by score
        sorted_categories = sorted(category_scores.items(), key=lambda x: x[1], reverse=True)
        
        best_category, best_score = sorted_categories[0]
        
        # Calculate confidence based on score separation
        if len(sorted_categories) > 1:
            second_score = sorted_categories[1][1]
            confidence = best_score if best_score - second_score > 0.1 else best_score * 0.8
        else:
            confidence = best_score
        
        # Ensure minimum confidence for valid categorization
        if confidence < 0.3:
            return ContentCategory.PERSONAL, 0.5
        
        return best_category, min(confidence, 1.0)
    
    def _determine_priority(self, content: str, keywords: List[str], context: Optional[Dict[str, Any]]) -> Priority:
        """Determine task priority based on content and context."""
        priority_scores = {priority: 0 for priority in Priority}
        
        # Check for priority keywords
        for priority, priority_keywords in self.priority_keywords.items():
            for keyword in priority_keywords:
                if keyword in content:
                    priority_scores[priority] += 1
        
        # Context-based priority adjustments
        if context:
            # Time-based urgency
            if 'due_date' in context:
                # This would need proper date parsing in a real implementation
                priority_scores[Priority.HIGH] += 1
            
            # User preferences
            if context.get('user_priority_preference') == 'high':
                priority_scores[Priority.HIGH] += 0.5
        
        # Select highest scoring priority
        best_priority = max(priority_scores.items(), key=lambda x: x[1])[0]
        
        # Default to medium if no clear priority indicators
        return best_priority if priority_scores[best_priority] > 0 else Priority.MEDIUM
    
    def _apply_context_adjustments(self, category: ContentCategory, confidence: float, 
                                 context: Dict[str, Any], content: str) -> Tuple[ContentCategory, float]:
        """Apply context-based adjustments to categorization."""
        adjusted_confidence = confidence
        
        # Time-based adjustments
        if 'time_of_day' in context:
            time_hour = context['time_of_day']
            
            # Work hours boost work category
            if 9 <= time_hour <= 17 and category == ContentCategory.WORK:
                adjusted_confidence = min(adjusted_confidence * 1.2, 1.0)
            
            # Evening hours boost personal/entertainment
            elif time_hour >= 18 and category in [ContentCategory.PERSONAL, ContentCategory.ENTERTAINMENT]:
                adjusted_confidence = min(adjusted_confidence * 1.1, 1.0)
        
        # Location-based adjustments
        if 'location' in context:
            location = context['location'].lower()
            
            if 'office' in location and category == ContentCategory.WORK:
                adjusted_confidence = min(adjusted_confidence * 1.3, 1.0)
            elif 'gym' in location and category == ContentCategory.HEALTH:
                adjusted_confidence = min(adjusted_confidence * 1.3, 1.0)
            elif 'home' in location and category == ContentCategory.PERSONAL:
                adjusted_confidence = min(adjusted_confidence * 1.1, 1.0)
        
        # User history adjustments (placeholder for ML integration)
        if 'user_patterns' in context:
            # This would integrate with user behavior patterns
            pass
        
        return category, adjusted_confidence
    
    def batch_categorize(self, contents: List[str], context: Optional[Dict[str, Any]] = None) -> List[CategoryResult]:
        """
        Categorize multiple content items efficiently.
        Optimized for mobile batch processing.
        """
        results = []
        
        for content in contents:
            try:
                result = self.categorize_content(content, context)
                results.append(result)
            except Exception as e:
                logger.error(f"Error categorizing content '{content[:50]}...': {e}")
                # Return default categorization on error
                results.append(CategoryResult(
                    category=ContentCategory.PERSONAL,
                    confidence=0.5,
                    priority=Priority.MEDIUM,
                    keywords=[],
                    metadata={'error': str(e)},
                    processing_time_ms=0.0
                ))
        
        return results
    
    def get_category_suggestions(self, partial_content: str, limit: int = 5) -> List[Tuple[ContentCategory, float]]:
        """
        Get category suggestions for partial content (real-time typing).
        Optimized for mobile real-time suggestions.
        """
        if len(partial_content) < 3:
            return []
        
        # Quick categorization for partial content
        normalized = self._normalize_content(partial_content)
        keywords = self._extract_keywords(normalized)
        scores = self._calculate_category_scores(normalized, keywords)
        
        # Return top suggestions
        sorted_suggestions = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return [(cat, score) for cat, score in sorted_suggestions[:limit] if score > 0.1]
    
    def update_patterns(self, new_patterns: Dict[str, List[str]]) -> None:
        """
        Update categorization patterns (for ML model updates).
        Allows dynamic pattern updates without service restart.
        """
        for category_name, patterns in new_patterns.items():
            try:
                category = ContentCategory(category_name)
                self.category_patterns[category] = patterns
                logger.info(f"Updated patterns for category: {category_name}")
            except ValueError:
                logger.warning(f"Unknown category: {category_name}")
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Get performance statistics for monitoring."""
        return {
            'categories_count': len(self.category_patterns),
            'patterns_per_category': {
                cat.value: len(patterns) 
                for cat, patterns in self.category_patterns.items()
            },
            'confidence_threshold': self.confidence_threshold,
            'service_status': 'active'
        }