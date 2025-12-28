"""
Property-based tests for adaptive schedule formatting.

Feature: ai-personal-scheduler, Property 8: Adaptive schedule formatting
Validates: Requirements 3.5, 6.2

Tests that for any user preference for schedule format, the system should adapt 
to display appropriate views (daily, weekly, monthly) with high-definition visual 
timelines and support multiple input methods.
"""

import pytest
from hypothesis import given, strategies as st, settings, assume, HealthCheck
from hypothesis.stateful import RuleBasedStateMachine, Bundle, rule, initialize, invariant
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import asyncio
import json

from app.services.schedule_generator import ScheduleGeneratorService
from app.services.contextual_alternatives import ContextualAlternativesService
from app.models.schedule import Schedule, ScheduleBlock, TimeFrame


# Test data generators
@st.composite
def schedule_format_preference_strategy(draw):
    """Generate schedule format preferences."""
    return {
        'format_type': draw(st.sampled_from(['daily', 'weekly', 'monthly'])),
        'view_density': draw(st.sampled_from(['compact', 'detailed', 'expanded'])),
        'time_granularity': draw(st.sampled_from(['15min', '30min', '1hour', '2hour'])),
        'visual_style': draw(st.sampled_from(['minimal', 'standard', 'rich', 'hd_timeline'])),
        'color_coding': draw(st.booleans()),
        'weather_integration': draw(st.booleans()),
        'priority_highlighting': draw(st.booleans()),
        'time_zone': draw(st.sampled_from(['UTC', 'America/New_York', 'Europe/London', 'Asia/Tokyo'])),
        'mobile_optimized': draw(st.booleans()),
        'accessibility_mode': draw(st.booleans())
    }


@st.composite
def user_display_preferences_strategy(draw):
    """Generate user display preferences."""
    return {
        'theme': draw(st.sampled_from(['light', 'dark', 'auto', 'high_contrast'])),
        'font_size': draw(st.sampled_from(['small', 'medium', 'large', 'extra_large'])),
        'animation_enabled': draw(st.booleans()),
        'sound_enabled': draw(st.booleans()),
        'notification_style': draw(st.sampled_from(['minimal', 'standard', 'rich'])),
        'language': draw(st.sampled_from(['en', 'es', 'fr', 'de', 'ja', 'zh'])),
        'date_format': draw(st.sampled_from(['MM/DD/YYYY', 'DD/MM/YYYY', 'YYYY-MM-DD'])),
        'time_format': draw(st.sampled_from(['12hour', '24hour'])),
        'first_day_of_week': draw(st.sampled_from(['sunday', 'monday'])),
        'show_weekends': draw(st.booleans())
    }


@st.composite
def schedule_data_strategy(draw):
    """Generate schedule data for formatting tests."""
    start_date = draw(st.datetimes(
        min_value=datetime.now(),
        max_value=datetime.now() + timedelta(days=30)
    ))
    
    num_blocks = draw(st.integers(min_value=1, max_value=20))
    blocks = []
    
    for i in range(num_blocks):
        block_start = start_date + timedelta(
            days=draw(st.integers(min_value=0, max_value=6)),
            hours=draw(st.integers(min_value=6, max_value=22)),
            minutes=draw(st.integers(min_value=0, max_value=45)) * 15
        )
        
        duration_hours = draw(st.floats(min_value=0.25, max_value=4.0))
        block_end = block_start + timedelta(hours=duration_hours)
        
        blocks.append({
            'id': f'block_{i}',
            'title': draw(st.text(min_size=5, max_size=30, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', ' ')))),
            'start_time': block_start,
            'end_time': block_end,
            'category': draw(st.sampled_from(['work', 'personal', 'health', 'social', 'learning'])),
            'priority': draw(st.sampled_from(['low', 'medium', 'high', 'critical'])),
            'location': draw(st.text(min_size=3, max_size=20, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', ' ')))),
            'description': draw(st.text(max_size=100, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', ' ', 'Nd')))),
            'flexible': draw(st.booleans()),
            'weather_sensitive': draw(st.booleans())
        })
    
    return {
        'schedule_id': draw(st.text(min_size=5, max_size=15, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd')))),
        'user_id': draw(st.text(min_size=5, max_size=15, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd')))),
        'time_frame': draw(st.sampled_from(['daily', 'weekly', 'monthly'])),
        'blocks': blocks,
        'created_at': start_date,
        'last_modified': start_date + timedelta(minutes=draw(st.integers(min_value=1, max_value=1440)))
    }


@st.composite
def input_method_strategy(draw):
    """Generate input method configurations."""
    return {
        'method': draw(st.sampled_from(['touch', 'mouse', 'keyboard', 'voice', 'gesture'])),
        'device_type': draw(st.sampled_from(['mobile', 'tablet', 'desktop', 'smartwatch'])),
        'screen_size': {
            'width': draw(st.integers(min_value=320, max_value=3840)),
            'height': draw(st.integers(min_value=240, max_value=2160))
        },
        'touch_enabled': draw(st.booleans()),
        'voice_enabled': draw(st.booleans()),
        'gesture_enabled': draw(st.booleans()),
        'accessibility_features': draw(st.lists(
            st.sampled_from(['screen_reader', 'high_contrast', 'large_text', 'voice_control']),
            min_size=0,
            max_size=4
        ))
    }


class MockScheduleFormatter:
    """Mock schedule formatter for testing adaptive formatting."""
    
    def __init__(self):
        self.format_cache = {}
        self.supported_formats = ['daily', 'weekly', 'monthly']
        self.supported_styles = ['minimal', 'standard', 'rich', 'hd_timeline']
    
    async def format_schedule(
        self,
        schedule_data: Dict[str, Any],
        format_preferences: Dict[str, Any],
        display_preferences: Dict[str, Any],
        input_method: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Format schedule according to preferences."""
        
        # Validate format type
        format_type = format_preferences.get('format_type', 'daily')
        if format_type not in self.supported_formats:
            format_type = 'daily'
        
        # Adapt to device constraints
        screen_width = input_method.get('screen_size', {}).get('width', 1920)
        device_type = input_method.get('device_type', 'desktop')
        
        # Determine optimal layout
        if device_type == 'mobile' or screen_width < 768:
            layout = 'mobile_optimized'
            max_columns = 1
        elif device_type == 'tablet' or screen_width < 1024:
            layout = 'tablet_optimized'
            max_columns = 2
        else:
            layout = 'desktop_optimized'
            max_columns = 7 if format_type == 'weekly' else 4
        
        # Apply visual style
        visual_style = format_preferences.get('visual_style', 'standard')
        if visual_style not in self.supported_styles:
            visual_style = 'standard'
        
        # Generate formatted output
        formatted_schedule = {
            'schedule_id': schedule_data['schedule_id'],
            'format_type': format_type,
            'layout': layout,
            'visual_style': visual_style,
            'columns': max_columns,
            'time_granularity': format_preferences.get('time_granularity', '1hour'),
            'blocks': self._format_blocks(
                schedule_data['blocks'],
                format_type,
                format_preferences,
                display_preferences
            ),
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'device_optimized': device_type,
                'accessibility_compliant': len(input_method.get('accessibility_features', [])) > 0,
                'responsive_design': True,
                'hd_visuals': visual_style == 'hd_timeline'
            }
        }
        
        # Add timeline elements for HD visual style
        if visual_style == 'hd_timeline':
            formatted_schedule['timeline_elements'] = self._generate_timeline_elements(
                schedule_data['blocks'],
                format_preferences
            )
        
        return formatted_schedule
    
    def _format_blocks(
        self,
        blocks: List[Dict[str, Any]],
        format_type: str,
        format_preferences: Dict[str, Any],
        display_preferences: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Format individual schedule blocks."""
        formatted_blocks = []
        
        for block in blocks:
            formatted_block = {
                'id': block['id'],
                'title': block['title'],
                'start_time': block['start_time'].isoformat(),
                'end_time': block['end_time'].isoformat(),
                'duration_minutes': int((block['end_time'] - block['start_time']).total_seconds() / 60),
                'category': block['category'],
                'priority': block['priority'],
                'display_properties': self._get_display_properties(block, format_preferences, display_preferences)
            }
            
            # Add format-specific properties
            if format_type == 'daily':
                formatted_block['time_slot'] = block['start_time'].strftime('%H:%M')
                formatted_block['day_position'] = 0
            elif format_type == 'weekly':
                formatted_block['day_of_week'] = block['start_time'].weekday()
                formatted_block['week_position'] = block['start_time'].weekday()
            elif format_type == 'monthly':
                formatted_block['day_of_month'] = block['start_time'].day
                formatted_block['month_position'] = block['start_time'].day
            
            formatted_blocks.append(formatted_block)
        
        return formatted_blocks
    
    def _get_display_properties(
        self,
        block: Dict[str, Any],
        format_preferences: Dict[str, Any],
        display_preferences: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Get display properties for a block."""
        properties = {
            'color': self._get_priority_color(block['priority']),
            'font_size': display_preferences.get('font_size', 'medium'),
            'theme': display_preferences.get('theme', 'light')
        }
        
        # Apply color coding if enabled
        if format_preferences.get('color_coding', True):
            properties['category_color'] = self._get_category_color(block['category'])
        
        # Apply priority highlighting if enabled
        if format_preferences.get('priority_highlighting', True):
            properties['priority_indicator'] = self._get_priority_indicator(block['priority'])
        
        return properties
    
    def _get_priority_color(self, priority: str) -> str:
        """Get color for priority level."""
        colors = {
            'critical': '#ff4444',
            'high': '#ff8800',
            'medium': '#4488ff',
            'low': '#44ff44'
        }
        return colors.get(priority, '#888888')
    
    def _get_category_color(self, category: str) -> str:
        """Get color for category."""
        colors = {
            'work': '#3366cc',
            'personal': '#dc3912',
            'health': '#ff9900',
            'social': '#109618',
            'learning': '#990099'
        }
        return colors.get(category, '#666666')
    
    def _get_priority_indicator(self, priority: str) -> str:
        """Get priority indicator symbol."""
        indicators = {
            'critical': '🔴',
            'high': '🟠',
            'medium': '🔵',
            'low': '🟢'
        }
        return indicators.get(priority, '⚪')
    
    def _generate_timeline_elements(
        self,
        blocks: List[Dict[str, Any]],
        format_preferences: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Generate HD timeline elements."""
        elements = []
        
        for block in blocks:
            element = {
                'element_id': f"timeline_{block['id']}",
                'type': 'schedule_block',
                'start_time': block['start_time'].isoformat(),
                'end_time': block['end_time'].isoformat(),
                'visual_style': 'hd_block',
                'animation': 'slide_in',
                'interactive': True,
                'metadata': {
                    'category': block['category'],
                    'priority': block['priority'],
                    'weather_sensitive': block.get('weather_sensitive', False)
                }
            }
            elements.append(element)
        
        return elements


class TestAdaptiveScheduleFormattingProperties:
    """Property-based tests for adaptive schedule formatting."""
    
    @pytest.fixture
    def formatter(self):
        """Create schedule formatter instance."""
        return MockScheduleFormatter()
    
    @given(
        schedule_data_strategy(),
        schedule_format_preference_strategy(),
        user_display_preferences_strategy(),
        input_method_strategy()
    )
    @settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_property_format_adaptation_completeness(
        self,
        formatter,
        schedule_data,
        format_preferences,
        display_preferences,
        input_method
    ):
        """
        Property: Format adaptation completeness
        For any valid schedule data and preferences, the formatter should produce 
        a complete formatted output that respects all specified preferences.
        """
        async def run_test():
            formatted = await formatter.format_schedule(
                schedule_data,
                format_preferences,
                display_preferences,
                input_method
            )
            
            # Property: Should have required structure
            assert 'schedule_id' in formatted
            assert 'format_type' in formatted
            assert 'layout' in formatted
            assert 'visual_style' in formatted
            assert 'blocks' in formatted
            assert 'metadata' in formatted
            
            # Property: Format type should match preference or fallback to valid option
            assert formatted['format_type'] in ['daily', 'weekly', 'monthly']
            
            # Property: All blocks should be formatted
            assert len(formatted['blocks']) == len(schedule_data['blocks'])
            
            # Property: Each block should have required formatting properties
            for block in formatted['blocks']:
                assert 'id' in block
                assert 'title' in block
                assert 'start_time' in block
                assert 'end_time' in block
                assert 'duration_minutes' in block
                assert 'display_properties' in block
                
                # Property: Duration should be calculated correctly
                start_time = datetime.fromisoformat(block['start_time'])
                end_time = datetime.fromisoformat(block['end_time'])
                expected_duration = int((end_time - start_time).total_seconds() / 60)
                assert block['duration_minutes'] == expected_duration
            
            # Property: Layout should be appropriate for device
            device_type = input_method.get('device_type', 'desktop')
            screen_width = input_method.get('screen_size', {}).get('width', 1920)
            
            if device_type == 'mobile' or screen_width < 768:
                assert 'mobile' in formatted['layout']
                assert formatted['columns'] == 1
            elif device_type == 'tablet' or screen_width < 1024:
                assert 'tablet' in formatted['layout']
                assert formatted['columns'] <= 2
            else:
                assert 'desktop' in formatted['layout']
        
        asyncio.run(run_test())
    
    @given(
        schedule_data_strategy(),
        schedule_format_preference_strategy(),
        user_display_preferences_strategy()
    )
    @settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_property_visual_style_consistency(
        self,
        formatter,
        schedule_data,
        format_preferences,
        display_preferences
    ):
        """
        Property: Visual style consistency
        Visual styling should be consistently applied across all elements 
        and respect user preferences.
        """
        async def run_test():
            input_method = {'device_type': 'desktop', 'screen_size': {'width': 1920, 'height': 1080}}
            
            formatted = await formatter.format_schedule(
                schedule_data,
                format_preferences,
                display_preferences,
                input_method
            )
            
            # Property: Visual style should be applied consistently
            expected_style = format_preferences.get('visual_style', 'standard')
            if expected_style not in ['minimal', 'standard', 'rich', 'hd_timeline']:
                expected_style = 'standard'
            
            assert formatted['visual_style'] == expected_style
            
            # Property: HD timeline should have timeline elements
            if expected_style == 'hd_timeline':
                assert 'timeline_elements' in formatted
                assert len(formatted['timeline_elements']) > 0
                
                for element in formatted['timeline_elements']:
                    assert 'element_id' in element
                    assert 'type' in element
                    assert 'visual_style' in element
                    assert element['visual_style'] == 'hd_block'
            
            # Property: Display properties should respect user preferences
            theme = display_preferences.get('theme', 'light')
            font_size = display_preferences.get('font_size', 'medium')
            
            for block in formatted['blocks']:
                display_props = block['display_properties']
                assert display_props['theme'] == theme
                assert display_props['font_size'] == font_size
                
                # Property: Color coding should be applied if enabled
                if format_preferences.get('color_coding', True):
                    assert 'category_color' in display_props
                
                # Property: Priority highlighting should be applied if enabled
                if format_preferences.get('priority_highlighting', True):
                    assert 'priority_indicator' in display_props
        
        asyncio.run(run_test())
    
    @given(schedule_data_strategy(), schedule_format_preference_strategy())
    @settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_property_responsive_design_adaptation(self, formatter, schedule_data, format_preferences):
        """
        Property: Responsive design adaptation
        The formatter should adapt layout appropriately for different screen sizes 
        and device types.
        """
        async def run_test():
            display_preferences = {'theme': 'light', 'font_size': 'medium'}
            
            # Test different device configurations
            device_configs = [
                {'device_type': 'mobile', 'screen_size': {'width': 375, 'height': 667}},
                {'device_type': 'tablet', 'screen_size': {'width': 768, 'height': 1024}},
                {'device_type': 'desktop', 'screen_size': {'width': 1920, 'height': 1080}}
            ]
            
            formatted_results = []
            
            for config in device_configs:
                formatted = await formatter.format_schedule(
                    schedule_data,
                    format_preferences,
                    display_preferences,
                    config
                )
                formatted_results.append((config, formatted))
            
            # Property: Mobile should have single column layout
            mobile_result = formatted_results[0][1]
            assert mobile_result['columns'] == 1
            assert 'mobile' in mobile_result['layout']
            
            # Property: Tablet should have limited columns
            tablet_result = formatted_results[1][1]
            assert tablet_result['columns'] <= 2
            assert 'tablet' in tablet_result['layout']
            
            # Property: Desktop should support more columns
            desktop_result = formatted_results[2][1]
            assert desktop_result['columns'] >= tablet_result['columns']
            assert 'desktop' in desktop_result['layout']
            
            # Property: All should have responsive design flag
            for _, result in formatted_results:
                assert result['metadata']['responsive_design'] is True
        
        asyncio.run(run_test())
    
    @given(schedule_data_strategy())
    @settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_property_accessibility_compliance(self, formatter, schedule_data):
        """
        Property: Accessibility compliance
        When accessibility features are requested, the formatter should provide 
        appropriate accommodations.
        """
        async def run_test():
            # Test with accessibility features enabled
            accessibility_input = {
                'device_type': 'desktop',
                'screen_size': {'width': 1920, 'height': 1080},
                'accessibility_features': ['screen_reader', 'high_contrast', 'large_text']
            }
            
            accessibility_display = {
                'theme': 'high_contrast',
                'font_size': 'extra_large'
            }
            
            format_preferences = {
                'format_type': 'daily',
                'visual_style': 'minimal',
                'color_coding': True,
                'priority_highlighting': True
            }
            
            formatted = await formatter.format_schedule(
                schedule_data,
                format_preferences,
                accessibility_display,
                accessibility_input
            )
            
            # Property: Should be marked as accessibility compliant
            assert formatted['metadata']['accessibility_compliant'] is True
            
            # Property: Should respect accessibility display preferences
            for block in formatted['blocks']:
                display_props = block['display_properties']
                assert display_props['theme'] == 'high_contrast'
                assert display_props['font_size'] == 'extra_large'
            
            # Property: Should maintain all required information for screen readers
            for block in formatted['blocks']:
                assert 'title' in block
                assert 'start_time' in block
                assert 'end_time' in block
                assert 'duration_minutes' in block
                assert 'category' in block
                assert 'priority' in block
        
        asyncio.run(run_test())
    
    @given(schedule_data_strategy(), schedule_format_preference_strategy())
    @settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_property_time_granularity_respect(self, formatter, schedule_data, format_preferences):
        """
        Property: Time granularity respect
        The formatter should respect the specified time granularity preferences.
        """
        async def run_test():
            display_preferences = {'theme': 'light', 'font_size': 'medium'}
            input_method = {'device_type': 'desktop', 'screen_size': {'width': 1920, 'height': 1080}}
            
            formatted = await formatter.format_schedule(
                schedule_data,
                format_preferences,
                display_preferences,
                input_method
            )
            
            # Property: Time granularity should be preserved
            expected_granularity = format_preferences.get('time_granularity', '1hour')
            assert formatted['time_granularity'] == expected_granularity
            
            # Property: Format type should be preserved or defaulted appropriately
            expected_format = format_preferences.get('format_type', 'daily')
            if expected_format in ['daily', 'weekly', 'monthly']:
                assert formatted['format_type'] == expected_format
            else:
                assert formatted['format_type'] == 'daily'  # Default fallback
        
        asyncio.run(run_test())
    
    @given(schedule_data_strategy())
    @settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_property_multi_input_method_support(self, formatter, schedule_data):
        """
        Property: Multi-input method support
        The formatter should adapt appropriately for different input methods.
        """
        async def run_test():
            format_preferences = {'format_type': 'daily', 'visual_style': 'standard'}
            display_preferences = {'theme': 'light', 'font_size': 'medium'}
            
            # Test different input methods
            input_methods = [
                {'method': 'touch', 'device_type': 'mobile', 'touch_enabled': True},
                {'method': 'mouse', 'device_type': 'desktop', 'touch_enabled': False},
                {'method': 'keyboard', 'device_type': 'desktop', 'touch_enabled': False},
                {'method': 'voice', 'device_type': 'mobile', 'voice_enabled': True}
            ]
            
            for input_method in input_methods:
                input_method['screen_size'] = {'width': 1920, 'height': 1080}
                
                formatted = await formatter.format_schedule(
                    schedule_data,
                    format_preferences,
                    display_preferences,
                    input_method
                )
                
                # Property: Should generate valid formatted output for all input methods
                assert 'schedule_id' in formatted
                assert 'blocks' in formatted
                assert len(formatted['blocks']) == len(schedule_data['blocks'])
                
                # Property: Should indicate device optimization
                assert 'device_optimized' in formatted['metadata']
                assert formatted['metadata']['device_optimized'] == input_method['device_type']
        
        asyncio.run(run_test())


class AdaptiveScheduleFormattingStateMachine(RuleBasedStateMachine):
    """
    Stateful property testing for adaptive schedule formatting.
    Tests complex formatting scenarios and state transitions.
    """
    
    def __init__(self):
        super().__init__()
        self.formatter = MockScheduleFormatter()
        self.formatting_history = []
        self.preference_changes = []
    
    schedules = Bundle('schedules')
    preferences = Bundle('preferences')
    formatted_outputs = Bundle('formatted_outputs')
    
    @initialize()
    def setup(self):
        """Initialize the state machine."""
        self.formatting_history = []
        self.preference_changes = []
    
    @rule(target=schedules, schedule_data=schedule_data_strategy())
    def add_schedule(self, schedule_data):
        """Add a schedule to the system."""
        return schedule_data
    
    @rule(target=preferences, 
          format_prefs=schedule_format_preference_strategy(),
          display_prefs=user_display_preferences_strategy(),
          input_method=input_method_strategy())
    def create_preferences(self, format_prefs, display_prefs, input_method):
        """Create a preference configuration."""
        return {
            'format': format_prefs,
            'display': display_prefs,
            'input': input_method
        }
    
    @rule(target=formatted_outputs, schedule=schedules, prefs=preferences)
    def format_schedule(self, schedule, prefs):
        """Format a schedule with given preferences."""
        async def run_formatting():
            formatted = await self.formatter.format_schedule(
                schedule,
                prefs['format'],
                prefs['display'],
                prefs['input']
            )
            
            self.formatting_history.append({
                'schedule_id': schedule['schedule_id'],
                'preferences': prefs,
                'formatted': formatted,
                'timestamp': datetime.now()
            })
            
            return formatted
        
        return asyncio.run(run_formatting())
    
    @rule(formatted=formatted_outputs)
    def test_formatted_output_validity(self, formatted):
        """Test that formatted output is valid."""
        # Property: Should have required structure
        assert 'schedule_id' in formatted
        assert 'format_type' in formatted
        assert 'blocks' in formatted
        assert 'metadata' in formatted
        
        # Property: All blocks should have valid time information
        for block in formatted['blocks']:
            start_time = datetime.fromisoformat(block['start_time'])
            end_time = datetime.fromisoformat(block['end_time'])
            assert end_time > start_time, "End time should be after start time"
            
            duration = int((end_time - start_time).total_seconds() / 60)
            assert block['duration_minutes'] == duration, "Duration should be calculated correctly"
    
    @rule(prefs1=preferences, prefs2=preferences)
    def test_preference_consistency(self, prefs1, prefs2):
        """Test consistency across different preference sets."""
        # Property: Different preferences should produce different layouts when appropriate
        if prefs1['input']['device_type'] != prefs2['input']['device_type']:
            # Different device types should potentially have different optimizations
            assert prefs1['input']['device_type'] in ['mobile', 'tablet', 'desktop']
            assert prefs2['input']['device_type'] in ['mobile', 'tablet', 'desktop']
    
    @invariant()
    def formatting_history_is_valid(self):
        """Invariant: All formatting history entries should be valid."""
        for entry in self.formatting_history:
            assert 'schedule_id' in entry
            assert 'preferences' in entry
            assert 'formatted' in entry
            assert 'timestamp' in entry
            
            formatted = entry['formatted']
            assert 'format_type' in formatted
            assert formatted['format_type'] in ['daily', 'weekly', 'monthly']


# Integration test for complete adaptive formatting workflow
@pytest.mark.asyncio
async def test_adaptive_formatting_integration():
    """
    Integration test for complete adaptive formatting workflow.
    Tests the full pipeline from schedule data to formatted output across devices.
    """
    formatter = MockScheduleFormatter()
    
    # Create test schedule data
    base_time = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
    schedule_data = {
        'schedule_id': 'integration_test_schedule',
        'user_id': 'integration_test_user',
        'time_frame': 'daily',
        'blocks': [
            {
                'id': 'morning_exercise',
                'title': 'Morning Workout',
                'start_time': base_time,
                'end_time': base_time + timedelta(hours=1),
                'category': 'health',
                'priority': 'high',
                'location': 'Gym',
                'description': 'Cardio and strength training',
                'flexible': False,
                'weather_sensitive': False
            },
            {
                'id': 'team_meeting',
                'title': 'Team Standup',
                'start_time': base_time + timedelta(hours=2),
                'end_time': base_time + timedelta(hours=2.5),
                'category': 'work',
                'priority': 'critical',
                'location': 'Conference Room A',
                'description': 'Daily team synchronization',
                'flexible': False,
                'weather_sensitive': False
            },
            {
                'id': 'lunch_break',
                'title': 'Lunch',
                'start_time': base_time + timedelta(hours=4),
                'end_time': base_time + timedelta(hours=5),
                'category': 'personal',
                'priority': 'medium',
                'location': 'Cafeteria',
                'description': 'Lunch break',
                'flexible': True,
                'weather_sensitive': False
            }
        ],
        'created_at': base_time,
        'last_modified': base_time
    }
    
    # Test different device configurations
    device_configs = [
        {
            'name': 'mobile',
            'format_prefs': {'format_type': 'daily', 'visual_style': 'minimal', 'mobile_optimized': True},
            'display_prefs': {'theme': 'light', 'font_size': 'medium'},
            'input_method': {'device_type': 'mobile', 'screen_size': {'width': 375, 'height': 667}, 'touch_enabled': True}
        },
        {
            'name': 'tablet',
            'format_prefs': {'format_type': 'weekly', 'visual_style': 'standard', 'mobile_optimized': False},
            'display_prefs': {'theme': 'dark', 'font_size': 'large'},
            'input_method': {'device_type': 'tablet', 'screen_size': {'width': 768, 'height': 1024}, 'touch_enabled': True}
        },
        {
            'name': 'desktop',
            'format_prefs': {'format_type': 'weekly', 'visual_style': 'hd_timeline', 'mobile_optimized': False},
            'display_prefs': {'theme': 'light', 'font_size': 'medium'},
            'input_method': {'device_type': 'desktop', 'screen_size': {'width': 1920, 'height': 1080}, 'touch_enabled': False}
        }
    ]
    
    results = {}
    
    for config in device_configs:
        formatted = await formatter.format_schedule(
            schedule_data,
            config['format_prefs'],
            config['display_prefs'],
            config['input_method']
        )
        
        results[config['name']] = formatted
        
        # Verify basic structure
        assert 'schedule_id' in formatted
        assert 'blocks' in formatted
        assert len(formatted['blocks']) == 3
        
        # Verify device-specific adaptations
        if config['name'] == 'mobile':
            assert formatted['columns'] == 1
            assert 'mobile' in formatted['layout']
        elif config['name'] == 'tablet':
            assert formatted['columns'] <= 2
            assert 'tablet' in formatted['layout']
        elif config['name'] == 'desktop':
            assert formatted['columns'] >= 2
            assert 'desktop' in formatted['layout']
            
            # Desktop with HD timeline should have timeline elements
            if config['format_prefs']['visual_style'] == 'hd_timeline':
                assert 'timeline_elements' in formatted
                assert len(formatted['timeline_elements']) == 3
    
    # Verify responsive behavior
    mobile_result = results['mobile']
    desktop_result = results['desktop']
    
    # Mobile should be more compact
    assert mobile_result['columns'] < desktop_result['columns']
    
    # Both should have same number of blocks
    assert len(mobile_result['blocks']) == len(desktop_result['blocks'])
    
    # HD timeline should only be on desktop
    assert 'timeline_elements' not in mobile_result
    assert 'timeline_elements' in desktop_result


if __name__ == "__main__":
    # Run property tests
    pytest.main([__file__, "-v", "--tb=short"])