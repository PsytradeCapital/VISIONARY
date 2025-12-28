"""
Contextual alternatives and weather integration service.

Integrates weather APIs for activity-based alternative suggestions, creates context-aware
suggestion algorithms with cloud processing, and adds Structured-inspired high-definition
visual timeline generation.
"""

import json
import logging
import aiohttp
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum

logger = logging.getLogger(__name__)


class WeatherCondition(Enum):
    """Weather condition types."""
    SUNNY = "sunny"
    CLOUDY = "cloudy"
    RAINY = "rainy"
    SNOWY = "snowy"
    STORMY = "stormy"
    FOGGY = "foggy"
    WINDY = "windy"


class ActivityType(Enum):
    """Types of activities that can be affected by weather."""
    OUTDOOR_EXERCISE = "outdoor_exercise"
    INDOOR_EXERCISE = "indoor_exercise"
    COMMUTING = "commuting"
    OUTDOOR_MEETING = "outdoor_meeting"
    INDOOR_MEETING = "indoor_meeting"
    RECREATIONAL = "recreational"
    WORK_FOCUSED = "work_focused"
    SOCIAL = "social"


@dataclass
class WeatherData:
    """Weather information for a specific time and location."""
    timestamp: datetime
    location: str
    condition: WeatherCondition
    temperature: float  # Celsius
    humidity: float  # Percentage
    wind_speed: float  # km/h
    precipitation_chance: float  # Percentage
    uv_index: int
    visibility: float  # km
    air_quality_index: Optional[int] = None


@dataclass
class ContextualAlternative:
    """Alternative suggestion based on context."""
    alternative_id: str
    original_activity: str
    suggested_activity: str
    reason: str
    confidence: float
    weather_factor: bool
    time_factor: bool
    location_factor: bool
    implementation: Dict[str, Any]
    visual_timeline_data: Optional[Dict[str, Any]] = None

@dataclass
class VisualTimelineElement:
    """Element for high-definition visual timeline."""
    element_id: str
    element_type: str  # 'task', 'weather', 'alternative', 'transition'
    start_time: datetime
    end_time: datetime
    visual_style: str
    color_scheme: str
    icon_url: Optional[str]
    background_image_url: Optional[str]
    animation_type: str
    metadata: Dict[str, Any]


@dataclass
class ContextualSuggestionRequest:
    """Request for contextual alternative suggestions."""
    user_id: str
    activity_id: str
    current_time: datetime
    location: str
    weather_sensitivity: float  # 0.0-1.0
    flexibility_minutes: int
    user_preferences: Dict[str, Any]
    context_factors: Dict[str, Any]


class ContextualAlternativesService:
    """
    Contextual alternatives and weather integration service.
    
    Features:
    - Weather API integration for activity-based alternative suggestions
    - Context-aware suggestion algorithms with cloud processing
    - Structured-inspired high-definition visual timeline generation
    - Real-time weather monitoring and proactive suggestions
    - Location-based activity recommendations
    - Time-sensitive alternative generation
    """
    
    def __init__(self, weather_api_key: str):
        self.weather_api_key = weather_api_key
        self.weather_cache = {}
        self.cache_duration = timedelta(minutes=30)
        
        # Weather impact thresholds
        self.weather_thresholds = {
            'precipitation_cancel': 70,  # % chance
            'temperature_extreme_low': -10,  # Celsius
            'temperature_extreme_high': 35,  # Celsius
            'wind_speed_high': 50,  # km/h
            'uv_index_high': 8,
            'air_quality_poor': 150
        }
        
        # Activity weather sensitivity
        self.activity_weather_sensitivity = {
            ActivityType.OUTDOOR_EXERCISE: 0.9,
            ActivityType.INDOOR_EXERCISE: 0.1,
            ActivityType.COMMUTING: 0.7,
            ActivityType.OUTDOOR_MEETING: 0.8,
            ActivityType.INDOOR_MEETING: 0.2,
            ActivityType.RECREATIONAL: 0.6,
            ActivityType.WORK_FOCUSED: 0.1,
            ActivityType.SOCIAL: 0.4
        }
    
    async def get_weather_data(self, location: str, timestamp: datetime) -> WeatherData:
        """
        Get weather data for specific location and time.
        
        Args:
            location: Location identifier (city, coordinates)
            timestamp: Time for weather forecast
            
        Returns:
            WeatherData with current/forecast information
        """
        logger.info(f"Getting weather data for {location} at {timestamp}")
        
        # Check cache first
        cache_key = f"{location}_{timestamp.strftime('%Y%m%d%H')}"
        if cache_key in self.weather_cache:
            cached_data = self.weather_cache[cache_key]
            if datetime.now() - cached_data['cached_at'] < self.cache_duration:
                return cached_data['weather_data']
        
        # Fetch from weather API
        weather_data = await self._fetch_weather_from_api(location, timestamp)
        
        # Cache the result
        self.weather_cache[cache_key] = {
            'weather_data': weather_data,
            'cached_at': datetime.now()
        }
        
        return weather_data
    
    async def generate_contextual_alternatives(
        self,
        request: ContextualSuggestionRequest
    ) -> List[ContextualAlternative]:
        """
        Generate contextual alternatives based on weather and other factors.
        
        Args:
            request: Contextual suggestion request
            
        Returns:
            List of contextual alternatives
        """
        logger.info(f"Generating contextual alternatives for activity {request.activity_id}")
        
        alternatives = []
        
        # Get weather data
        weather_data = await self.get_weather_data(request.location, request.current_time)
        
        # Analyze weather impact
        weather_impact = self._analyze_weather_impact(weather_data, request)
        
        # Generate weather-based alternatives
        if weather_impact['requires_alternative']:
            weather_alternatives = await self._generate_weather_alternatives(
                request, weather_data, weather_impact
            )
            alternatives.extend(weather_alternatives)
        
        # Generate time-based alternatives
        time_alternatives = await self._generate_time_based_alternatives(request)
        alternatives.extend(time_alternatives)
        
        # Generate location-based alternatives
        location_alternatives = await self._generate_location_alternatives(request, weather_data)
        alternatives.extend(location_alternatives)
        
        # Generate context-aware alternatives
        context_alternatives = await self._generate_context_aware_alternatives(request)
        alternatives.extend(context_alternatives)
        
        # Sort by confidence and relevance
        alternatives.sort(key=lambda x: x.confidence, reverse=True)
        
        return alternatives[:10]  # Return top 10 alternatives
    
    async def generate_visual_timeline(
        self,
        user_id: str,
        schedule_data: Dict[str, Any],
        weather_data: List[WeatherData],
        alternatives: List[ContextualAlternative]
    ) -> Dict[str, Any]:
        """
        Generate Structured-inspired high-definition visual timeline.
        
        Args:
            user_id: User identifier
            schedule_data: Schedule information
            weather_data: Weather forecast data
            alternatives: Available alternatives
            
        Returns:
            Visual timeline configuration
        """
        logger.info(f"Generating visual timeline for user {user_id}")
        
        timeline_elements = []
        
        # Add schedule blocks
        for block in schedule_data.get('time_blocks', []):
            element = await self._create_schedule_timeline_element(block, weather_data)
            timeline_elements.append(element)
        
        # Add weather indicators
        for weather in weather_data:
            element = await self._create_weather_timeline_element(weather)
            timeline_elements.append(element)
        
        # Add alternative suggestions
        for alternative in alternatives:
            element = await self._create_alternative_timeline_element(alternative)
            timeline_elements.append(element)
        
        # Add transition elements
        transition_elements = await self._create_transition_elements(timeline_elements)
        timeline_elements.extend(transition_elements)
        
        # Sort by time
        timeline_elements.sort(key=lambda x: x.start_time)
        
        return {
            'timeline_id': f"timeline_{user_id}_{datetime.now().timestamp()}",
            'user_id': user_id,
            'elements': [asdict(e) for e in timeline_elements],
            'visual_style': 'structured_hd',
            'color_scheme': 'adaptive',
            'animation_enabled': True,
            'interactive_elements': True,
            'weather_integration': True,
            'generated_at': datetime.now().isoformat()
        }
    
    async def monitor_weather_changes(
        self,
        user_id: str,
        scheduled_activities: List[Dict[str, Any]],
        location: str
    ) -> List[Dict[str, Any]]:
        """
        Monitor weather changes and generate proactive suggestions.
        
        Args:
            user_id: User identifier
            scheduled_activities: List of scheduled activities
            location: User location
            
        Returns:
            List of proactive weather-based suggestions
        """
        logger.info(f"Monitoring weather changes for user {user_id}")
        
        proactive_suggestions = []
        
        for activity in scheduled_activities:
            activity_time = datetime.fromisoformat(activity['start_time'])
            
            # Get weather forecast for activity time
            weather_data = await self.get_weather_data(location, activity_time)
            
            # Check if weather affects this activity
            activity_type = ActivityType(activity.get('type', 'work_focused'))
            sensitivity = self.activity_weather_sensitivity.get(activity_type, 0.5)
            
            if sensitivity > 0.5:  # Weather-sensitive activity
                weather_impact = self._analyze_weather_impact_for_activity(
                    weather_data, activity, sensitivity
                )
                
                if weather_impact['severity'] > 0.6:
                    suggestion = {
                        'suggestion_id': f"weather_alert_{datetime.now().timestamp()}",
                        'activity_id': activity['id'],
                        'alert_type': 'weather_impact',
                        'severity': weather_impact['severity'],
                        'message': weather_impact['message'],
                        'suggested_actions': weather_impact['suggested_actions'],
                        'weather_condition': weather_data.condition.value,
                        'advance_notice_hours': (activity_time - datetime.now()).total_seconds() / 3600
                    }
                    proactive_suggestions.append(suggestion)
        
        return proactive_suggestions
    async def _fetch_weather_from_api(self, location: str, timestamp: datetime) -> WeatherData:
        """Fetch weather data from external API."""
        # Example using OpenWeatherMap API
        base_url = "https://api.openweathermap.org/data/2.5"
        
        # Determine if we need current weather or forecast
        now = datetime.now()
        hours_ahead = (timestamp - now).total_seconds() / 3600
        
        if hours_ahead <= 1:
            # Current weather
            url = f"{base_url}/weather"
            params = {
                'q': location,
                'appid': self.weather_api_key,
                'units': 'metric'
            }
        else:
            # Forecast weather
            url = f"{base_url}/forecast"
            params = {
                'q': location,
                'appid': self.weather_api_key,
                'units': 'metric'
            }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return self._parse_weather_response(data, timestamp, location)
                else:
                    logger.error(f"Weather API error: {response.status}")
                    # Return default weather data
                    return self._get_default_weather_data(location, timestamp)
    
    def _parse_weather_response(self, data: Dict[str, Any], timestamp: datetime, location: str) -> WeatherData:
        """Parse weather API response."""
        if 'list' in data:  # Forecast data
            # Find closest forecast to requested time
            forecasts = data['list']
            closest_forecast = min(
                forecasts,
                key=lambda x: abs(datetime.fromtimestamp(x['dt']) - timestamp)
            )
            weather_info = closest_forecast
        else:  # Current weather data
            weather_info = data
        
        # Map weather condition
        condition_map = {
            'clear': WeatherCondition.SUNNY,
            'clouds': WeatherCondition.CLOUDY,
            'rain': WeatherCondition.RAINY,
            'drizzle': WeatherCondition.RAINY,
            'thunderstorm': WeatherCondition.STORMY,
            'snow': WeatherCondition.SNOWY,
            'mist': WeatherCondition.FOGGY,
            'fog': WeatherCondition.FOGGY
        }
        
        weather_main = weather_info['weather'][0]['main'].lower()
        condition = condition_map.get(weather_main, WeatherCondition.CLOUDY)
        
        return WeatherData(
            timestamp=timestamp,
            location=location,
            condition=condition,
            temperature=weather_info['main']['temp'],
            humidity=weather_info['main']['humidity'],
            wind_speed=weather_info.get('wind', {}).get('speed', 0) * 3.6,  # m/s to km/h
            precipitation_chance=weather_info.get('pop', 0) * 100,  # Probability of precipitation
            uv_index=weather_info.get('uvi', 5),  # Default moderate UV
            visibility=weather_info.get('visibility', 10000) / 1000,  # meters to km
            air_quality_index=None  # Would need separate API call
        )
    
    def _get_default_weather_data(self, location: str, timestamp: datetime) -> WeatherData:
        """Get default weather data when API fails."""
        return WeatherData(
            timestamp=timestamp,
            location=location,
            condition=WeatherCondition.CLOUDY,
            temperature=20.0,
            humidity=50.0,
            wind_speed=10.0,
            precipitation_chance=20.0,
            uv_index=5,
            visibility=10.0
        )
    
    def _analyze_weather_impact(self, weather_data: WeatherData, 
                              request: ContextualSuggestionRequest) -> Dict[str, Any]:
        """Analyze weather impact on planned activity."""
        impact = {
            'requires_alternative': False,
            'severity': 0.0,
            'factors': [],
            'recommendations': []
        }
        
        # Check precipitation
        if weather_data.precipitation_chance > self.weather_thresholds['precipitation_cancel']:
            impact['requires_alternative'] = True
            impact['severity'] += 0.4
            impact['factors'].append('high_precipitation_chance')
            impact['recommendations'].append('move_indoors')
        
        # Check temperature extremes
        if weather_data.temperature < self.weather_thresholds['temperature_extreme_low']:
            impact['requires_alternative'] = True
            impact['severity'] += 0.3
            impact['factors'].append('extreme_cold')
            impact['recommendations'].append('indoor_alternative')
        elif weather_data.temperature > self.weather_thresholds['temperature_extreme_high']:
            impact['requires_alternative'] = True
            impact['severity'] += 0.3
            impact['factors'].append('extreme_heat')
            impact['recommendations'].append('cooler_time_or_indoor')
        
        # Check wind conditions
        if weather_data.wind_speed > self.weather_thresholds['wind_speed_high']:
            impact['severity'] += 0.2
            impact['factors'].append('high_wind')
            impact['recommendations'].append('sheltered_location')
        
        # Check UV index
        if weather_data.uv_index > self.weather_thresholds['uv_index_high']:
            impact['severity'] += 0.1
            impact['factors'].append('high_uv')
            impact['recommendations'].append('sun_protection_or_shade')
        
        # Apply user weather sensitivity
        impact['severity'] *= request.weather_sensitivity
        
        if impact['severity'] > 0.5:
            impact['requires_alternative'] = True
        
        return impact
    
    async def _generate_weather_alternatives(
        self,
        request: ContextualSuggestionRequest,
        weather_data: WeatherData,
        weather_impact: Dict[str, Any]
    ) -> List[ContextualAlternative]:
        """Generate weather-based alternatives."""
        alternatives = []
        
        # Indoor alternatives for outdoor activities
        if 'move_indoors' in weather_impact['recommendations']:
            indoor_alt = ContextualAlternative(
                alternative_id=f"indoor_{datetime.now().timestamp()}",
                original_activity=request.activity_id,
                suggested_activity=f"Indoor version of {request.activity_id}",
                reason=f"Weather conditions ({weather_data.condition.value}) suggest indoor alternative",
                confidence=0.9,
                weather_factor=True,
                time_factor=False,
                location_factor=True,
                implementation={
                    'location_change': 'indoor',
                    'activity_modification': 'weather_adapted'
                }
            )
            alternatives.append(indoor_alt)
        
        # Time-shifted alternatives
        if weather_impact['severity'] > 0.3:
            # Suggest earlier or later time
            for time_shift in [-2, -1, 1, 2]:  # Hours
                new_time = request.current_time + timedelta(hours=time_shift)
                
                # Check if new time is within flexibility
                if abs(time_shift * 60) <= request.flexibility_minutes:
                    time_alt = ContextualAlternative(
                        alternative_id=f"time_shift_{time_shift}_{datetime.now().timestamp()}",
                        original_activity=request.activity_id,
                        suggested_activity=f"{request.activity_id} at {new_time.strftime('%I:%M %p')}",
                        reason=f"Better weather conditions expected at {new_time.strftime('%I:%M %p')}",
                        confidence=0.7,
                        weather_factor=True,
                        time_factor=True,
                        location_factor=False,
                        implementation={
                            'time_change': new_time.isoformat(),
                            'reason': 'weather_optimization'
                        }
                    )
                    alternatives.append(time_alt)
        
        return alternatives
    
    async def _generate_time_based_alternatives(self, request: ContextualSuggestionRequest) -> List[ContextualAlternative]:
        """Generate time-based alternatives."""
        alternatives = []
        
        current_hour = request.current_time.hour
        
        # Suggest optimal times based on activity type
        optimal_times = {
            'exercise': [7, 8, 17, 18],
            'work': [9, 10, 14, 15],
            'meeting': [10, 11, 14, 15],
            'creative': [9, 10, 15, 16],
            'administrative': [11, 13, 16, 17]
        }
        
        activity_category = request.context_factors.get('category', 'work')
        preferred_hours = optimal_times.get(activity_category, [10, 14])
        
        for hour in preferred_hours:
            if hour != current_hour and abs(hour - current_hour) <= request.flexibility_minutes // 60:
                new_time = request.current_time.replace(hour=hour, minute=0)
                
                time_alt = ContextualAlternative(
                    alternative_id=f"optimal_time_{hour}_{datetime.now().timestamp()}",
                    original_activity=request.activity_id,
                    suggested_activity=f"{request.activity_id} at {new_time.strftime('%I:%M %p')}",
                    reason=f"Optimal time for {activity_category} activities",
                    confidence=0.6,
                    weather_factor=False,
                    time_factor=True,
                    location_factor=False,
                    implementation={
                        'time_change': new_time.isoformat(),
                        'reason': 'time_optimization'
                    }
                )
                alternatives.append(time_alt)
        
        return alternatives
    
    async def _generate_location_alternatives(
        self,
        request: ContextualSuggestionRequest,
        weather_data: WeatherData
    ) -> List[ContextualAlternative]:
        """Generate location-based alternatives."""
        alternatives = []
        
        # Suggest covered locations for bad weather
        if weather_data.condition in [WeatherCondition.RAINY, WeatherCondition.STORMY]:
            covered_locations = [
                'Indoor gym', 'Shopping mall', 'Community center', 
                'Library', 'Coworking space', 'Cafe'
            ]
            
            for location in covered_locations:
                location_alt = ContextualAlternative(
                    alternative_id=f"location_{location.lower().replace(' ', '_')}_{datetime.now().timestamp()}",
                    original_activity=request.activity_id,
                    suggested_activity=f"{request.activity_id} at {location}",
                    reason=f"Covered location recommended due to {weather_data.condition.value} weather",
                    confidence=0.8,
                    weather_factor=True,
                    time_factor=False,
                    location_factor=True,
                    implementation={
                        'location_change': location,
                        'reason': 'weather_protection'
                    }
                )
                alternatives.append(location_alt)
        
        return alternatives
    
    async def _generate_context_aware_alternatives(self, request: ContextualSuggestionRequest) -> List[ContextualAlternative]:
        """Generate context-aware alternatives based on user preferences and situation."""
        alternatives = []
        
        # Energy level based alternatives
        energy_level = request.context_factors.get('energy_level', 'medium')
        
        if energy_level == 'low':
            low_energy_alt = ContextualAlternative(
                alternative_id=f"low_energy_{datetime.now().timestamp()}",
                original_activity=request.activity_id,
                suggested_activity=f"Light version of {request.activity_id}",
                reason="Adjusted for current energy level",
                confidence=0.7,
                weather_factor=False,
                time_factor=False,
                location_factor=False,
                implementation={
                    'intensity_reduction': 0.5,
                    'duration_reduction': 0.3,
                    'reason': 'energy_optimization'
                }
            )
            alternatives.append(low_energy_alt)
        
        # Social context alternatives
        social_preference = request.user_preferences.get('social_preference', 'neutral')
        
        if social_preference == 'social':
            social_alt = ContextualAlternative(
                alternative_id=f"social_{datetime.now().timestamp()}",
                original_activity=request.activity_id,
                suggested_activity=f"Group {request.activity_id}",
                reason="Enhanced for social interaction",
                confidence=0.6,
                weather_factor=False,
                time_factor=False,
                location_factor=False,
                implementation={
                    'social_enhancement': True,
                    'group_activity': True,
                    'reason': 'social_optimization'
                }
            )
            alternatives.append(social_alt)
        
        return alternatives
    async def _create_schedule_timeline_element(
        self,
        block: Dict[str, Any],
        weather_data: List[WeatherData]
    ) -> VisualTimelineElement:
        """Create timeline element for schedule block."""
        start_time = datetime.fromisoformat(block['start_time'])
        end_time = datetime.fromisoformat(block['end_time'])
        
        # Find relevant weather data
        relevant_weather = None
        for weather in weather_data:
            if start_time <= weather.timestamp <= end_time:
                relevant_weather = weather
                break
        
        # Determine visual style based on activity type and weather
        visual_style = self._determine_visual_style(block, relevant_weather)
        color_scheme = self._determine_color_scheme(block, relevant_weather)
        
        return VisualTimelineElement(
            element_id=f"schedule_{block['id']}",
            element_type='task',
            start_time=start_time,
            end_time=end_time,
            visual_style=visual_style,
            color_scheme=color_scheme,
            icon_url=self._get_activity_icon_url(block['type']),
            background_image_url=None,
            animation_type='slide_in',
            metadata={
                'activity_type': block['type'],
                'priority': block.get('priority', 'medium'),
                'weather_affected': relevant_weather is not None
            }
        )
    
    async def _create_weather_timeline_element(self, weather: WeatherData) -> VisualTimelineElement:
        """Create timeline element for weather indicator."""
        return VisualTimelineElement(
            element_id=f"weather_{weather.timestamp.timestamp()}",
            element_type='weather',
            start_time=weather.timestamp,
            end_time=weather.timestamp + timedelta(hours=1),
            visual_style='weather_indicator',
            color_scheme=self._get_weather_color_scheme(weather.condition),
            icon_url=self._get_weather_icon_url(weather.condition),
            background_image_url=None,
            animation_type='fade_in',
            metadata={
                'condition': weather.condition.value,
                'temperature': weather.temperature,
                'precipitation_chance': weather.precipitation_chance
            }
        )
    
    async def _create_alternative_timeline_element(self, alternative: ContextualAlternative) -> VisualTimelineElement:
        """Create timeline element for alternative suggestion."""
        # Estimate timing based on implementation
        start_time = datetime.now()  # Placeholder
        if 'time_change' in alternative.implementation:
            start_time = datetime.fromisoformat(alternative.implementation['time_change'])
        
        return VisualTimelineElement(
            element_id=f"alt_{alternative.alternative_id}",
            element_type='alternative',
            start_time=start_time,
            end_time=start_time + timedelta(hours=1),
            visual_style='alternative_suggestion',
            color_scheme='suggestion_blue',
            icon_url='/icons/alternative.svg',
            background_image_url=None,
            animation_type='pulse',
            metadata={
                'confidence': alternative.confidence,
                'reason': alternative.reason,
                'weather_factor': alternative.weather_factor
            }
        )
    
    async def _create_transition_elements(self, elements: List[VisualTimelineElement]) -> List[VisualTimelineElement]:
        """Create transition elements between timeline items."""
        transitions = []
        
        sorted_elements = sorted(elements, key=lambda x: x.start_time)
        
        for i in range(len(sorted_elements) - 1):
            current = sorted_elements[i]
            next_element = sorted_elements[i + 1]
            
            # Create transition if there's a gap
            if current.end_time < next_element.start_time:
                gap_duration = next_element.start_time - current.end_time
                
                if gap_duration > timedelta(minutes=15):  # Only for significant gaps
                    transition = VisualTimelineElement(
                        element_id=f"transition_{i}",
                        element_type='transition',
                        start_time=current.end_time,
                        end_time=next_element.start_time,
                        visual_style='transition_gap',
                        color_scheme='neutral_gray',
                        icon_url=None,
                        background_image_url=None,
                        animation_type='none',
                        metadata={
                            'gap_duration_minutes': int(gap_duration.total_seconds() / 60),
                            'transition_type': 'free_time'
                        }
                    )
                    transitions.append(transition)
        
        return transitions
    
    def _determine_visual_style(self, block: Dict[str, Any], weather: Optional[WeatherData]) -> str:
        """Determine visual style for schedule block."""
        base_style = f"activity_{block['type']}"
        
        if weather:
            if weather.condition in [WeatherCondition.RAINY, WeatherCondition.STORMY]:
                return f"{base_style}_weather_affected"
            elif weather.condition == WeatherCondition.SUNNY:
                return f"{base_style}_sunny"
        
        return base_style
    
    def _determine_color_scheme(self, block: Dict[str, Any], weather: Optional[WeatherData]) -> str:
        """Determine color scheme for schedule block."""
        priority_colors = {
            'critical': 'red_urgent',
            'high': 'orange_high',
            'medium': 'blue_medium',
            'low': 'green_low'
        }
        
        base_color = priority_colors.get(block.get('priority', 'medium'), 'blue_medium')
        
        if weather and weather.condition in [WeatherCondition.RAINY, WeatherCondition.STORMY]:
            return f"{base_color}_muted"
        
        return base_color
    
    def _get_weather_color_scheme(self, condition: WeatherCondition) -> str:
        """Get color scheme for weather condition."""
        weather_colors = {
            WeatherCondition.SUNNY: 'yellow_sunny',
            WeatherCondition.CLOUDY: 'gray_cloudy',
            WeatherCondition.RAINY: 'blue_rainy',
            WeatherCondition.SNOWY: 'white_snowy',
            WeatherCondition.STORMY: 'dark_stormy',
            WeatherCondition.FOGGY: 'light_gray_foggy',
            WeatherCondition.WINDY: 'teal_windy'
        }
        
        return weather_colors.get(condition, 'gray_default')
    
    def _get_activity_icon_url(self, activity_type: str) -> str:
        """Get icon URL for activity type."""
        icon_map = {
            'exercise': '/icons/exercise.svg',
            'meeting': '/icons/meeting.svg',
            'work': '/icons/work.svg',
            'break': '/icons/break.svg',
            'commute': '/icons/commute.svg',
            'social': '/icons/social.svg',
            'creative': '/icons/creative.svg'
        }
        
        return icon_map.get(activity_type, '/icons/default.svg')
    
    def _get_weather_icon_url(self, condition: WeatherCondition) -> str:
        """Get icon URL for weather condition."""
        weather_icons = {
            WeatherCondition.SUNNY: '/icons/weather/sunny.svg',
            WeatherCondition.CLOUDY: '/icons/weather/cloudy.svg',
            WeatherCondition.RAINY: '/icons/weather/rainy.svg',
            WeatherCondition.SNOWY: '/icons/weather/snowy.svg',
            WeatherCondition.STORMY: '/icons/weather/stormy.svg',
            WeatherCondition.FOGGY: '/icons/weather/foggy.svg',
            WeatherCondition.WINDY: '/icons/weather/windy.svg'
        }
        
        return weather_icons.get(condition, '/icons/weather/default.svg')
    
    def _analyze_weather_impact_for_activity(
        self,
        weather_data: WeatherData,
        activity: Dict[str, Any],
        sensitivity: float
    ) -> Dict[str, Any]:
        """Analyze weather impact for specific activity."""
        impact = {
            'severity': 0.0,
            'message': '',
            'suggested_actions': []
        }
        
        activity_type = activity.get('type', 'general')
        
        # Check precipitation impact
        if weather_data.precipitation_chance > 50:
            impact['severity'] += 0.4 * sensitivity
            impact['message'] = f"High chance of rain ({weather_data.precipitation_chance:.0f}%) during {activity_type}"
            impact['suggested_actions'].append('Consider indoor alternative')
        
        # Check temperature impact
        if weather_data.temperature < 5 or weather_data.temperature > 30:
            impact['severity'] += 0.3 * sensitivity
            temp_desc = "cold" if weather_data.temperature < 5 else "hot"
            impact['message'] += f" Extreme {temp_desc} weather ({weather_data.temperature:.1f}°C)"
            impact['suggested_actions'].append('Adjust timing or location')
        
        # Check wind impact
        if weather_data.wind_speed > 30:
            impact['severity'] += 0.2 * sensitivity
            impact['message'] += f" High winds ({weather_data.wind_speed:.0f} km/h)"
            impact['suggested_actions'].append('Find sheltered location')
        
        return impact
    
    def get_contextual_service_stats(self) -> Dict[str, Any]:
        """Get contextual alternatives service statistics."""
        return {
            'weather_cache_entries': len(self.weather_cache),
            'cache_duration_minutes': self.cache_duration.total_seconds() / 60,
            'weather_thresholds': self.weather_thresholds,
            'activity_sensitivity_map': {k.value: v for k, v in self.activity_weather_sensitivity.items()},
            'supported_weather_conditions': [c.value for c in WeatherCondition],
            'supported_activity_types': [a.value for a in ActivityType]
        }