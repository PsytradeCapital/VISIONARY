"""
Property-based tests for contextual alternatives and weather integration.

Feature: ai-personal-scheduler, Property 7: Contextual alternative suggestions
Validates: Requirements 3.3, 4.5

Tests that for any disruption, weather condition, or external factor affecting 
planned activities, the system should suggest appropriate alternatives that 
align with user goals and current context.
"""

import pytest
from hypothesis import given, strategies as st, settings, assume, HealthCheck
from hypothesis.stateful import RuleBasedStateMachine, Bundle, rule, initialize, invariant
from datetime import datetime, timedelta
from typing import Dict, List, Any
import asyncio
import json

from app.services.contextual_alternatives import (
    ContextualAlternativesService,
    ContextualSuggestionRequest,
    WeatherCondition,
    ActivityType,
    WeatherData,
    ContextualAlternative
)


# Test data generators
@st.composite
def weather_data_strategy(draw):
    """Generate realistic weather data."""
    timestamp = draw(st.datetimes(
        min_value=datetime.now(),
        max_value=datetime.now() + timedelta(days=7)
    ))
    
    condition = draw(st.sampled_from(list(WeatherCondition)))
    
    # Temperature ranges based on condition
    temp_ranges = {
        WeatherCondition.SNOWY: (-20, 5),
        WeatherCondition.STORMY: (5, 25),
        WeatherCondition.RAINY: (5, 20),
        WeatherCondition.CLOUDY: (0, 30),
        WeatherCondition.SUNNY: (15, 40),
        WeatherCondition.FOGGY: (5, 20),
        WeatherCondition.WINDY: (0, 30)
    }
    
    temp_range = temp_ranges.get(condition, (0, 30))
    temperature = draw(st.floats(min_value=temp_range[0], max_value=temp_range[1]))
    
    return WeatherData(
        timestamp=timestamp,
        location=draw(st.text(min_size=3, max_size=20, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', ' ')))),
        condition=condition,
        temperature=temperature,
        humidity=draw(st.floats(min_value=0, max_value=100)),
        wind_speed=draw(st.floats(min_value=0, max_value=100)),
        precipitation_chance=draw(st.floats(min_value=0, max_value=100)),
        uv_index=draw(st.integers(min_value=0, max_value=11)),
        visibility=draw(st.floats(min_value=0.1, max_value=50)),
        air_quality_index=draw(st.one_of(st.none(), st.integers(min_value=0, max_value=500)))
    )


@st.composite
def contextual_request_strategy(draw):
    """Generate contextual suggestion requests."""
    current_time = draw(st.datetimes(
        min_value=datetime.now(),
        max_value=datetime.now() + timedelta(days=1)
    ))
    
    return ContextualSuggestionRequest(
        user_id=draw(st.text(min_size=5, max_size=20, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd')))),
        activity_id=draw(st.text(min_size=3, max_size=15, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd')))),
        current_time=current_time,
        location=draw(st.text(min_size=3, max_size=20, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', ' ')))),
        weather_sensitivity=draw(st.floats(min_value=0.0, max_value=1.0)),
        flexibility_minutes=draw(st.integers(min_value=15, max_value=480)),  # 15 minutes to 8 hours
        user_preferences=draw(st.dictionaries(
            st.text(min_size=1, max_size=10, alphabet=st.characters(whitelist_categories=('Lu', 'Ll'))),
            st.one_of(st.text(max_size=20), st.booleans(), st.integers(min_value=0, max_value=100)),
            min_size=0,
            max_size=5
        )),
        context_factors=draw(st.dictionaries(
            st.text(min_size=1, max_size=15, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', '_'))),
            st.one_of(st.text(max_size=15), st.integers(min_value=0, max_value=10)),
            min_size=0,
            max_size=5
        ))
    )


@st.composite
def scheduled_activity_strategy(draw):
    """Generate scheduled activities."""
    start_time = draw(st.datetimes(
        min_value=datetime.now(),
        max_value=datetime.now() + timedelta(days=2)
    ))
    
    activity_types = ['exercise', 'meeting', 'work', 'social', 'commute', 'creative']
    
    return {
        'id': draw(st.text(min_size=5, max_size=15, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd')))),
        'title': draw(st.text(min_size=5, max_size=30, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', ' ')))),
        'type': draw(st.sampled_from(activity_types)),
        'start_time': start_time.isoformat(),
        'end_time': (start_time + timedelta(hours=draw(st.integers(min_value=1, max_value=4)))).isoformat(),
        'priority': draw(st.sampled_from(['low', 'medium', 'high', 'critical'])),
        'location': draw(st.text(min_size=3, max_size=20, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', ' '))))
    }


class TestContextualAlternativesProperties:
    """Property-based tests for contextual alternatives service."""
    
    @pytest.fixture
    def service(self):
        """Create contextual alternatives service instance."""
        return ContextualAlternativesService(weather_api_key="test_key")
    
    @given(contextual_request_strategy())
    @settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_property_alternative_generation_completeness(self, service, request_data):
        """
        Property: Alternative generation completeness
        For any valid contextual request, the service should generate at least one 
        alternative when weather or context factors suggest it's needed.
        """
        async def run_test():
            # Mock weather data that requires alternatives
            severe_weather = WeatherData(
                timestamp=request_data.current_time,
                location=request_data.location,
                condition=WeatherCondition.STORMY,
                temperature=35.0,  # Extreme heat
                humidity=90.0,
                wind_speed=60.0,  # High wind
                precipitation_chance=80.0,  # High rain chance
                uv_index=10,
                visibility=2.0
            )
            
            # Mock the weather API call
            original_fetch = service._fetch_weather_from_api
            service._fetch_weather_from_api = lambda loc, time: severe_weather
            
            try:
                alternatives = await service.generate_contextual_alternatives(request_data)
                
                # Property: Should generate alternatives for severe weather
                assert len(alternatives) > 0, "Should generate alternatives for severe weather conditions"
                
                # Property: All alternatives should be valid
                for alt in alternatives:
                    assert isinstance(alt, ContextualAlternative)
                    assert alt.alternative_id is not None and alt.alternative_id != ""
                    assert alt.confidence >= 0.0 and alt.confidence <= 1.0
                    assert alt.reason is not None and alt.reason != ""
                    assert isinstance(alt.implementation, dict)
                
                # Property: At least one alternative should address weather
                weather_alternatives = [alt for alt in alternatives if alt.weather_factor]
                assert len(weather_alternatives) > 0, "Should have weather-based alternatives for severe conditions"
                
            finally:
                service._fetch_weather_from_api = original_fetch
        
        asyncio.run(run_test())
    
    @given(contextual_request_strategy(), weather_data_strategy())
    @settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_property_weather_sensitivity_scaling(self, service, request_data, weather_data):
        """
        Property: Weather sensitivity scaling
        Alternatives should scale appropriately with user weather sensitivity settings.
        """
        async def run_test():
            # Test with low sensitivity
            low_sensitivity_request = ContextualSuggestionRequest(
                user_id=request_data.user_id,
                activity_id=request_data.activity_id,
                current_time=request_data.current_time,
                location=request_data.location,
                weather_sensitivity=0.1,  # Low sensitivity
                flexibility_minutes=request_data.flexibility_minutes,
                user_preferences=request_data.user_preferences,
                context_factors=request_data.context_factors
            )
            
            # Test with high sensitivity
            high_sensitivity_request = ContextualSuggestionRequest(
                user_id=request_data.user_id,
                activity_id=request_data.activity_id,
                current_time=request_data.current_time,
                location=request_data.location,
                weather_sensitivity=0.9,  # High sensitivity
                flexibility_minutes=request_data.flexibility_minutes,
                user_preferences=request_data.user_preferences,
                context_factors=request_data.context_factors
            )
            
            # Mock weather API
            service._fetch_weather_from_api = lambda loc, time: weather_data
            
            low_alternatives = await service.generate_contextual_alternatives(low_sensitivity_request)
            high_alternatives = await service.generate_contextual_alternatives(high_sensitivity_request)
            
            # Property: High sensitivity should generate more or equal weather alternatives
            low_weather_alts = len([alt for alt in low_alternatives if alt.weather_factor])
            high_weather_alts = len([alt for alt in high_alternatives if alt.weather_factor])
            
            if weather_data.condition in [WeatherCondition.STORMY, WeatherCondition.RAINY] or \
               weather_data.precipitation_chance > 70 or \
               weather_data.temperature < 0 or weather_data.temperature > 35:
                assert high_weather_alts >= low_weather_alts, \
                    "High weather sensitivity should generate more weather alternatives for severe conditions"
        
        asyncio.run(run_test())
    
    @given(contextual_request_strategy())
    @settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_property_flexibility_constraint_respect(self, service, request_data):
        """
        Property: Flexibility constraint respect
        All time-based alternatives should respect user flexibility constraints.
        """
        async def run_test():
            # Mock weather API
            service._fetch_weather_from_api = lambda loc, time: WeatherData(
                timestamp=request_data.current_time,
                location=request_data.location,
                condition=WeatherCondition.CLOUDY,
                temperature=20.0,
                humidity=50.0,
                wind_speed=10.0,
                precipitation_chance=30.0,
                uv_index=5,
                visibility=10.0
            )
            
            alternatives = await service.generate_contextual_alternatives(request_data)
            
            # Property: Time-based alternatives should respect flexibility
            for alt in alternatives:
                if alt.time_factor and 'time_change' in alt.implementation:
                    new_time = datetime.fromisoformat(alt.implementation['time_change'])
                    time_diff_minutes = abs((new_time - request_data.current_time).total_seconds() / 60)
                    
                    assert time_diff_minutes <= request_data.flexibility_minutes, \
                        f"Time alternative exceeds flexibility: {time_diff_minutes} > {request_data.flexibility_minutes}"
        
        asyncio.run(run_test())
    
    @given(st.lists(scheduled_activity_strategy(), min_size=1, max_size=5))
    @settings(max_examples=50, suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_property_proactive_weather_monitoring(self, service, activities):
        """
        Property: Proactive weather monitoring
        Weather monitoring should generate appropriate alerts for weather-sensitive activities.
        """
        async def run_test():
            user_id = "test_user"
            location = "Test City"
            
            # Mock severe weather for all activity times
            service._fetch_weather_from_api = lambda loc, time: WeatherData(
                timestamp=time,
                location=location,
                condition=WeatherCondition.STORMY,
                temperature=40.0,  # Extreme heat
                humidity=95.0,
                wind_speed=70.0,  # Very high wind
                precipitation_chance=90.0,  # Very high rain chance
                uv_index=11,
                visibility=1.0
            )
            
            suggestions = await service.monitor_weather_changes(user_id, activities, location)
            
            # Property: Should generate alerts for weather-sensitive activities
            outdoor_activities = [a for a in activities if a.get('type') in ['exercise', 'commute', 'social']]
            
            if outdoor_activities:
                # Should have at least some weather alerts for outdoor activities
                weather_alerts = [s for s in suggestions if s['alert_type'] == 'weather_impact']
                assert len(weather_alerts) > 0, "Should generate weather alerts for outdoor activities in severe weather"
                
                # Property: All alerts should have required fields
                for alert in weather_alerts:
                    assert 'suggestion_id' in alert
                    assert 'activity_id' in alert
                    assert 'severity' in alert
                    assert 'message' in alert
                    assert 'suggested_actions' in alert
                    assert alert['severity'] >= 0.0 and alert['severity'] <= 1.0
                    assert isinstance(alert['suggested_actions'], list)
        
        asyncio.run(run_test())
    
    @given(contextual_request_strategy())
    @settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_property_alternative_confidence_ordering(self, service, request_data):
        """
        Property: Alternative confidence ordering
        Alternatives should be ordered by confidence score in descending order.
        """
        async def run_test():
            # Mock weather API
            service._fetch_weather_from_api = lambda loc, time: WeatherData(
                timestamp=request_data.current_time,
                location=request_data.location,
                condition=WeatherCondition.RAINY,
                temperature=15.0,
                humidity=80.0,
                wind_speed=25.0,
                precipitation_chance=75.0,
                uv_index=3,
                visibility=5.0
            )
            
            alternatives = await service.generate_contextual_alternatives(request_data)
            
            # Property: Alternatives should be ordered by confidence (descending)
            if len(alternatives) > 1:
                for i in range(len(alternatives) - 1):
                    assert alternatives[i].confidence >= alternatives[i + 1].confidence, \
                        f"Alternatives not ordered by confidence: {alternatives[i].confidence} < {alternatives[i + 1].confidence}"
        
        asyncio.run(run_test())
    
    @given(contextual_request_strategy())
    @settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_property_visual_timeline_completeness(self, service, request_data):
        """
        Property: Visual timeline completeness
        Visual timeline should include all relevant elements and be properly structured.
        """
        async def run_test():
            # Mock schedule data
            schedule_data = {
                'time_blocks': [
                    {
                        'id': 'block1',
                        'type': 'exercise',
                        'start_time': request_data.current_time.isoformat(),
                        'end_time': (request_data.current_time + timedelta(hours=1)).isoformat(),
                        'priority': 'high'
                    },
                    {
                        'id': 'block2',
                        'type': 'meeting',
                        'start_time': (request_data.current_time + timedelta(hours=2)).isoformat(),
                        'end_time': (request_data.current_time + timedelta(hours=3)).isoformat(),
                        'priority': 'medium'
                    }
                ]
            }
            
            # Mock weather data
            weather_data = [
                WeatherData(
                    timestamp=request_data.current_time,
                    location=request_data.location,
                    condition=WeatherCondition.SUNNY,
                    temperature=25.0,
                    humidity=60.0,
                    wind_speed=15.0,
                    precipitation_chance=10.0,
                    uv_index=6,
                    visibility=15.0
                )
            ]
            
            # Mock alternatives
            service._fetch_weather_from_api = lambda loc, time: weather_data[0]
            alternatives = await service.generate_contextual_alternatives(request_data)
            
            timeline = await service.generate_visual_timeline(
                request_data.user_id,
                schedule_data,
                weather_data,
                alternatives
            )
            
            # Property: Timeline should have required structure
            assert 'timeline_id' in timeline
            assert 'user_id' in timeline
            assert 'elements' in timeline
            assert 'visual_style' in timeline
            assert 'generated_at' in timeline
            
            # Property: Should have elements for schedule blocks
            schedule_elements = [e for e in timeline['elements'] if e['element_type'] == 'task']
            assert len(schedule_elements) == len(schedule_data['time_blocks']), \
                "Should have timeline elements for all schedule blocks"
            
            # Property: Should have weather elements
            weather_elements = [e for e in timeline['elements'] if e['element_type'] == 'weather']
            assert len(weather_elements) > 0, "Should have weather timeline elements"
            
            # Property: All elements should have required fields
            for element in timeline['elements']:
                assert 'element_id' in element
                assert 'element_type' in element
                assert 'start_time' in element
                assert 'visual_style' in element
                assert 'color_scheme' in element
        
        asyncio.run(run_test())


class ContextualAlternativesStateMachine(RuleBasedStateMachine):
    """
    Stateful property testing for contextual alternatives service.
    Tests complex interactions and state transitions.
    """
    
    def __init__(self):
        super().__init__()
        self.service = ContextualAlternativesService(weather_api_key="test_key")
        self.generated_alternatives = []
        self.weather_cache_states = []
        self.timeline_generations = []
    
    requests = Bundle('requests')
    weather_data = Bundle('weather_data')
    alternatives = Bundle('alternatives')
    
    @initialize()
    def setup(self):
        """Initialize the state machine."""
        self.generated_alternatives = []
        self.weather_cache_states = []
        self.timeline_generations = []
    
    @rule(target=requests, request_data=contextual_request_strategy())
    def generate_request(self, request_data):
        """Generate a contextual suggestion request."""
        return request_data
    
    @rule(target=weather_data, weather=weather_data_strategy())
    def add_weather_data(self, weather):
        """Add weather data to the system."""
        return weather
    
    @rule(target=alternatives, request=requests, weather=weather_data)
    def generate_alternatives(self, request, weather):
        """Generate alternatives for a request with specific weather."""
        async def run_generation():
            # Mock weather API
            self.service._fetch_weather_from_api = lambda loc, time: weather
            
            alternatives = await self.service.generate_contextual_alternatives(request)
            self.generated_alternatives.extend(alternatives)
            return alternatives
        
        return asyncio.run(run_generation())
    
    @rule(alternatives_list=alternatives)
    def test_alternatives_consistency(self, alternatives_list):
        """Test that generated alternatives maintain consistency."""
        if alternatives_list:
            # Property: All alternatives should have valid confidence scores
            for alt in alternatives_list:
                assert 0.0 <= alt.confidence <= 1.0, f"Invalid confidence: {alt.confidence}"
                assert alt.alternative_id is not None and alt.alternative_id != ""
                assert alt.reason is not None and alt.reason != ""
    
    @rule(request=requests, weather=weather_data)
    def test_weather_caching_behavior(self, request, weather):
        """Test weather caching behavior."""
        async def run_cache_test():
            # Mock weather API
            call_count = 0
            
            def mock_fetch(loc, time):
                nonlocal call_count
                call_count += 1
                return weather
            
            self.service._fetch_weather_from_api = mock_fetch
            
            # First call should fetch from API
            weather1 = await self.service.get_weather_data(request.location, request.current_time)
            first_call_count = call_count
            
            # Second call within cache duration should use cache
            weather2 = await self.service.get_weather_data(request.location, request.current_time)
            second_call_count = call_count
            
            # Property: Second call should not increase API call count (cache hit)
            assert second_call_count == first_call_count, "Weather data should be cached"
            assert weather1.condition == weather2.condition, "Cached weather should match original"
        
        asyncio.run(run_cache_test())
    
    @invariant()
    def alternatives_are_valid(self):
        """Invariant: All generated alternatives should be valid."""
        for alt in self.generated_alternatives:
            assert isinstance(alt, ContextualAlternative)
            assert 0.0 <= alt.confidence <= 1.0
            assert alt.alternative_id is not None and alt.alternative_id != ""


# Integration test for the complete contextual alternatives workflow
@pytest.mark.asyncio
async def test_contextual_alternatives_integration():
    """
    Integration test for complete contextual alternatives workflow.
    Tests the full pipeline from request to alternatives generation.
    """
    service = ContextualAlternativesService(weather_api_key="test_key")
    
    # Mock severe weather conditions
    severe_weather = WeatherData(
        timestamp=datetime.now() + timedelta(hours=2),
        location="Test City",
        condition=WeatherCondition.STORMY,
        temperature=38.0,
        humidity=90.0,
        wind_speed=65.0,
        precipitation_chance=85.0,
        uv_index=10,
        visibility=2.0
    )
    
    service._fetch_weather_from_api = lambda loc, time: severe_weather
    
    # Create request for outdoor activity
    request = ContextualSuggestionRequest(
        user_id="integration_test_user",
        activity_id="outdoor_exercise",
        current_time=datetime.now() + timedelta(hours=2),
        location="Test City",
        weather_sensitivity=0.8,
        flexibility_minutes=120,
        user_preferences={'activity_type': 'exercise', 'indoor_preference': False},
        context_factors={'energy_level': 'high', 'category': 'exercise'}
    )
    
    # Generate alternatives
    alternatives = await service.generate_contextual_alternatives(request)
    
    # Verify integration results
    assert len(alternatives) > 0, "Should generate alternatives for severe weather"
    
    # Should have weather-based alternatives
    weather_alternatives = [alt for alt in alternatives if alt.weather_factor]
    assert len(weather_alternatives) > 0, "Should have weather-based alternatives"
    
    # Should suggest indoor alternatives
    indoor_alternatives = [alt for alt in alternatives 
                          if 'indoor' in alt.suggested_activity.lower() or 
                             alt.implementation.get('location_change') == 'indoor']
    assert len(indoor_alternatives) > 0, "Should suggest indoor alternatives for severe weather"
    
    # Test visual timeline generation
    schedule_data = {
        'time_blocks': [{
            'id': 'exercise_block',
            'type': 'exercise',
            'start_time': request.current_time.isoformat(),
            'end_time': (request.current_time + timedelta(hours=1)).isoformat(),
            'priority': 'high'
        }]
    }
    
    timeline = await service.generate_visual_timeline(
        request.user_id,
        schedule_data,
        [severe_weather],
        alternatives
    )
    
    # Verify timeline structure
    assert 'timeline_id' in timeline
    assert 'elements' in timeline
    assert len(timeline['elements']) > 0
    
    # Should have task, weather, and alternative elements
    element_types = {e['element_type'] for e in timeline['elements']}
    assert 'task' in element_types, "Timeline should include task elements"
    assert 'weather' in element_types, "Timeline should include weather elements"


if __name__ == "__main__":
    # Run property tests
    pytest.main([__file__, "-v", "--tb=short"])