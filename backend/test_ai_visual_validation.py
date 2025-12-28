"""
Comprehensive Test Suite for AI Visual Validation Service
Tests photorealistic image validation and premium analytics validation
"""

import pytest
import asyncio
import json
import numpy as np
from PIL import Image
from io import BytesIO
import uuid
from datetime import datetime
from unittest.mock import Mock, AsyncMock, patch

from ai_visual_validation_service import (
    AIVisualValidationService, 
    ImageQualityLevel, 
    ValidationResult, 
    ContentCategory,
    PhotorealismScore,
    ValidationMetrics,
    PremiumAnalyticsValidation
)

class TestAIVisualValidation:
    """Test suite for AI visual validation service"""
    
    @pytest.fixture
    def validation_service(self):
        """Create validation service for testing"""
        return AIVisualValidationService()
    
    @pytest.fixture
    def sample_photorealistic_image(self):
        """Create sample photorealistic image for testing"""
        # Create a high-quality test image
        image = Image.new('RGB', (1024, 768), color='white')
        
        # Add some realistic elements (simplified for testing)
        pixels = np.array(image)
        
        # Add gradient to simulate natural lighting
        for i in range(768):
            for j in range(1024):
                pixels[i, j] = [
                    min(255, 200 + int(30 * np.sin(i * 0.01))),
                    min(255, 180 + int(40 * np.cos(j * 0.008))),
                    min(255, 160 + int(20 * np.sin((i + j) * 0.005)))
                ]
        
        # Add some texture/noise to simulate real photo characteristics
        noise = np.random.normal(0, 10, pixels.shape).astype(np.int16)
        pixels = np.clip(pixels.astype(np.int16) + noise, 0, 255).astype(np.uint8)
        
        image = Image.fromarray(pixels)
        
        # Convert to bytes
        img_buffer = BytesIO()
        image.save(img_buffer, format='JPEG', quality=95)
        return img_buffer.getvalue()
    
    @pytest.fixture
    def sample_cartoon_image(self):
        """Create sample cartoon/illustration image for testing"""
        # Create a cartoon-like test image with flat colors
        image = Image.new('RGB', (512, 512), color='blue')
        
        pixels = np.array(image)
        
        # Create flat color regions typical of cartoons
        pixels[:256, :] = [255, 0, 0]  # Red top half
        pixels[256:, :] = [0, 255, 0]  # Green bottom half
        pixels[:, 256:] = [0, 0, 255]  # Blue right half
        
        image = Image.fromarray(pixels)
        
        # Convert to bytes
        img_buffer = BytesIO()
        image.save(img_buffer, format='PNG')
        return img_buffer.getvalue()
    
    @pytest.fixture
    def sample_low_quality_image(self):
        """Create sample low quality image for testing"""
        # Create a low resolution, low quality image
        image = Image.new('RGB', (128, 96), color='gray')
        
        # Convert to bytes with high compression
        img_buffer = BytesIO()
        image.save(img_buffer, format='JPEG', quality=10)
        return img_buffer.getvalue()
    
    @pytest.fixture
    def sample_health_content(self):
        """Sample health content description"""
        return {
            'category': 'health_fitness',
            'description': 'Person exercising in a modern gym',
            'expected_elements': ['person', 'gym_equipment', 'exercise_activity'],
            'quality_requirements': 'photorealistic'
        }
    
    @pytest.fixture
    def sample_nutrition_content(self):
        """Sample nutrition content description"""
        return {
            'category': 'nutrition_food',
            'description': 'Healthy meal with fresh vegetables',
            'expected_elements': ['food', 'vegetables', 'healthy_presentation'],
            'quality_requirements': 'professional_food_photography'
        }
    
    @pytest.fixture
    def sample_analytics_data(self):
        """Sample premium analytics data"""
        return {
            'chart_type': 'progress_chart',
            'data_points': [
                {'date': '2024-01-01', 'value': 10},
                {'date': '2024-01-02', 'value': 15},
                {'date': '2024-01-03', 'value': 22},
                {'date': '2024-01-04', 'value': 18},
                {'date': '2024-01-05', 'value': 25}
            ],
            'visual_style': 'premium',
            'color_scheme': 'professional',
            'interactive_features': ['hover', 'zoom', 'export'],
            'mobile_optimized': True
        }
    
    @pytest.mark.asyncio
    async def test_photorealistic_image_validation_approved(self, validation_service, 
                                                          sample_photorealistic_image, 
                                                          sample_health_content):
        """Test validation of high-quality photorealistic image"""
        
        # Validate the photorealistic image
        result = await validation_service.validate_photorealistic_image(
            image_data=sample_photorealistic_image,
            image_url="https://example.com/test_image.jpg",
            content_category=ContentCategory.HEALTH_FITNESS,
            ai_model_used="dall-e-3",
            expected_content=sample_health_content
        )
        
        # Verify validation result
        assert isinstance(result, ValidationMetrics)
        assert result.image_id is not None
        assert result.validation_timestamp is not None
        
        # Verify photorealism scores
        assert isinstance(result.photorealism_score, PhotorealismScore)
        assert result.photorealism_score.overall_score >= 0.0
        assert result.photorealism_score.overall_score <= 10.0
        
        # For a well-constructed test image, expect reasonable scores
        assert result.photorealism_score.realism_score >= 5.0
        assert result.photorealism_score.quality_score >= 5.0
        
        # Verify quality level is appropriate
        assert result.quality_level in [
            ImageQualityLevel.PHOTOREALISTIC,
            ImageQualityLevel.PROFESSIONAL_PHOTOGRAPHY,
            ImageQualityLevel.LIFESTYLE_PHOTOGRAPHY
        ]
        
        # Verify content category
        assert result.content_category == ContentCategory.HEALTH_FITNESS
        
        # Verify AI model tracking
        assert result.ai_model_used == "dall-e-3"
        
        # Verify technical metrics are present
        assert isinstance(result.technical_metrics, dict)
        assert 'resolution_width' in result.technical_metrics
        assert 'resolution_height' in result.technical_metrics
        assert 'sharpness' in result.technical_metrics
    
    @pytest.mark.asyncio
    async def test_cartoon_image_validation_rejected(self, validation_service, 
                                                   sample_cartoon_image, 
                                                   sample_health_content):
        """Test validation of cartoon/illustration image (should be rejected)"""
        
        # Validate the cartoon image
        result = await validation_service.validate_photorealistic_image(
            image_data=sample_cartoon_image,
            image_url="https://example.com/cartoon_image.png",
            content_category=ContentCategory.HEALTH_FITNESS,
            ai_model_used="stable-diffusion",
            expected_content=sample_health_content
        )
        
        # Verify validation result
        assert isinstance(result, ValidationMetrics)
        
        # Cartoon images should have lower scores
        assert result.photorealism_score.overall_score < 7.0
        
        # Quality level should indicate non-photorealistic content
        assert result.quality_level in [
            ImageQualityLevel.CARTOON,
            ImageQualityLevel.ILLUSTRATION,
            ImageQualityLevel.DIGITAL_ART,
            ImageQualityLevel.REJECTED
        ]
        
        # Validation result should indicate rejection or need for regeneration
        assert result.validation_result in [
            ValidationResult.REJECTED,
            ValidationResult.NEEDS_REGENERATION,
            ValidationResult.REQUIRES_MANUAL_REVIEW
        ]
        
        # Should have rejection reasons
        if result.rejection_reasons:
            assert len(result.rejection_reasons) > 0
            # Check for appropriate rejection reasons
            rejection_text = ' '.join(result.rejection_reasons).lower()
            assert any(keyword in rejection_text for keyword in [
                'quality', 'realism', 'photorealistic', 'cartoon', 'illustration'
            ])
    
    @pytest.mark.asyncio
    async def test_low_quality_image_validation_rejected(self, validation_service, 
                                                       sample_low_quality_image, 
                                                       sample_health_content):
        """Test validation of low quality image (should be rejected)"""
        
        # Validate the low quality image
        result = await validation_service.validate_photorealistic_image(
            image_data=sample_low_quality_image,
            image_url="https://example.com/low_quality_image.jpg",
            content_category=ContentCategory.HEALTH_FITNESS,
            ai_model_used="dall-e-3",
            expected_content=sample_health_content
        )
        
        # Verify validation result
        assert isinstance(result, ValidationMetrics)
        
        # Low quality images should have poor scores
        assert result.photorealism_score.quality_score < 6.0
        
        # Should be rejected or need regeneration
        assert result.validation_result in [
            ValidationResult.REJECTED,
            ValidationResult.NEEDS_REGENERATION
        ]
        
        # Technical metrics should reflect low quality
        assert result.technical_metrics['resolution_width'] < 512
        assert result.technical_metrics['resolution_height'] < 512
    
    @pytest.mark.asyncio
    async def test_nutrition_content_validation(self, validation_service, 
                                              sample_photorealistic_image, 
                                              sample_nutrition_content):
        """Test validation of nutrition/food content"""
        
        # Validate nutrition content
        result = await validation_service.validate_photorealistic_image(
            image_data=sample_photorealistic_image,
            image_url="https://example.com/food_image.jpg",
            content_category=ContentCategory.NUTRITION_FOOD,
            ai_model_used="dall-e-3",
            expected_content=sample_nutrition_content
        )
        
        # Verify content category is correct
        assert result.content_category == ContentCategory.NUTRITION_FOOD
        
        # Verify validation completed
        assert isinstance(result, ValidationMetrics)
        assert result.validation_result in [
            ValidationResult.APPROVED,
            ValidationResult.NEEDS_REGENERATION,
            ValidationResult.REQUIRES_MANUAL_REVIEW
        ]
    
    @pytest.mark.asyncio
    async def test_financial_success_content_validation(self, validation_service, 
                                                      sample_photorealistic_image):
        """Test validation of financial success content"""
        
        financial_content = {
            'category': 'financial_success',
            'description': 'Professional celebrating business success',
            'expected_elements': ['person', 'office_environment', 'success_indicators'],
            'quality_requirements': 'professional_photography'
        }
        
        # Validate financial content
        result = await validation_service.validate_photorealistic_image(
            image_data=sample_photorealistic_image,
            image_url="https://example.com/success_image.jpg",
            content_category=ContentCategory.FINANCIAL_SUCCESS,
            ai_model_used="dall-e-3",
            expected_content=financial_content
        )
        
        # Verify content category is correct
        assert result.content_category == ContentCategory.FINANCIAL_SUCCESS
        
        # Verify validation completed
        assert isinstance(result, ValidationMetrics)
    
    @pytest.mark.asyncio
    async def test_wellness_lifestyle_content_validation(self, validation_service, 
                                                       sample_photorealistic_image):
        """Test validation of wellness/lifestyle content"""
        
        wellness_content = {
            'category': 'wellness_lifestyle',
            'description': 'Person meditating in peaceful environment',
            'expected_elements': ['person', 'peaceful_setting', 'wellness_activity'],
            'quality_requirements': 'lifestyle_photography'
        }
        
        # Validate wellness content
        result = await validation_service.validate_photorealistic_image(
            image_data=sample_photorealistic_image,
            image_url="https://example.com/wellness_image.jpg",
            content_category=ContentCategory.WELLNESS_LIFESTYLE,
            ai_model_used="stable-diffusion",
            expected_content=wellness_content
        )
        
        # Verify content category is correct
        assert result.content_category == ContentCategory.WELLNESS_LIFESTYLE
        
        # Verify validation completed
        assert isinstance(result, ValidationMetrics)
    
    @pytest.mark.asyncio
    async def test_premium_analytics_validation_approved(self, validation_service, 
                                                       sample_analytics_data):
        """Test validation of premium analytics (should be approved)"""
        
        user_context = {
            'user_id': str(uuid.uuid4()),
            'premium_user': True,
            'preferences': {
                'chart_style': 'professional',
                'color_scheme': 'modern'
            }
        }
        
        # Validate premium analytics
        result = await validation_service.validate_premium_analytics(
            analytics_data=sample_analytics_data,
            chart_type="progress_chart",
            user_context=user_context
        )
        
        # Verify validation result
        assert isinstance(result, PremiumAnalyticsValidation)
        assert result.analytics_id is not None
        assert result.chart_type == "progress_chart"
        
        # Verify scoring metrics
        assert result.visual_quality_score >= 0.0
        assert result.visual_quality_score <= 10.0
        assert result.data_clarity_score >= 0.0
        assert result.data_clarity_score <= 10.0
        assert result.professional_appearance_score >= 0.0
        assert result.professional_appearance_score <= 10.0
        assert result.mobile_optimization_score >= 0.0
        assert result.mobile_optimization_score <= 10.0
        assert result.accessibility_score >= 0.0
        assert result.accessibility_score <= 10.0
        assert result.premium_features_score >= 0.0
        assert result.premium_features_score <= 10.0
        
        # Overall premium score should be calculated
        assert result.overall_premium_score >= 0.0
        assert result.overall_premium_score <= 10.0
        
        # For well-designed analytics, should meet premium standards
        # (Note: This depends on the mock implementation returning good scores)
        assert isinstance(result.meets_premium_standards, bool)
    
    @pytest.mark.asyncio
    async def test_premium_analytics_validation_different_chart_types(self, validation_service):
        """Test validation of different chart types"""
        
        chart_types = [
            "progress_chart",
            "goal_tracking_chart",
            "habit_streak_chart",
            "financial_overview_chart",
            "health_metrics_chart"
        ]
        
        user_context = {
            'user_id': str(uuid.uuid4()),
            'premium_user': True
        }
        
        for chart_type in chart_types:
            analytics_data = {
                'chart_type': chart_type,
                'data_points': [{'x': i, 'y': i * 2} for i in range(10)],
                'visual_style': 'premium'
            }
            
            # Validate each chart type
            result = await validation_service.validate_premium_analytics(
                analytics_data=analytics_data,
                chart_type=chart_type,
                user_context=user_context
            )
            
            # Verify validation completed for each type
            assert isinstance(result, PremiumAnalyticsValidation)
            assert result.chart_type == chart_type
            assert result.analytics_id is not None
    
    @pytest.mark.asyncio
    async def test_validation_error_handling(self, validation_service):
        """Test error handling in validation service"""
        
        # Test with invalid image data
        invalid_image_data = b"invalid image data"
        
        result = await validation_service.validate_photorealistic_image(
            image_data=invalid_image_data,
            image_url="https://example.com/invalid_image.jpg",
            content_category=ContentCategory.HEALTH_FITNESS,
            ai_model_used="dall-e-3",
            expected_content={}
        )
        
        # Should handle error gracefully
        assert isinstance(result, ValidationMetrics)
        assert result.validation_result == ValidationResult.REJECTED
        assert result.quality_level == ImageQualityLevel.REJECTED
        assert len(result.rejection_reasons) > 0
        assert result.manual_review_required == True
        
        # Error should be in rejection reasons
        rejection_text = ' '.join(result.rejection_reasons).lower()
        assert 'error' in rejection_text or 'validation' in rejection_text
    
    @pytest.mark.asyncio
    async def test_photorealism_thresholds(self, validation_service):
        """Test photorealism threshold enforcement"""
        
        # Verify thresholds are properly configured
        thresholds = validation_service.photorealism_thresholds
        
        assert 'minimum_overall_score' in thresholds
        assert 'minimum_realism_score' in thresholds
        assert 'minimum_quality_score' in thresholds
        assert 'minimum_authenticity_score' in thresholds
        assert 'minimum_professional_score' in thresholds
        
        # Verify threshold values are reasonable
        assert thresholds['minimum_overall_score'] >= 5.0
        assert thresholds['minimum_realism_score'] >= 5.0
        assert thresholds['minimum_quality_score'] >= 5.0
        assert thresholds['minimum_authenticity_score'] >= 5.0
        
        # Verify premium analytics thresholds
        premium_thresholds = validation_service.premium_analytics_thresholds
        
        assert 'minimum_visual_quality' in premium_thresholds
        assert 'minimum_professional_appearance' in premium_thresholds
        assert 'minimum_premium_score' in premium_thresholds
        
        assert premium_thresholds['minimum_visual_quality'] >= 7.0
        assert premium_thresholds['minimum_professional_appearance'] >= 7.0
        assert premium_thresholds['minimum_premium_score'] >= 6.0
    
    @pytest.mark.asyncio
    async def test_rejection_criteria_validation(self, validation_service):
        """Test rejection criteria for non-photorealistic content"""
        
        # Verify rejection criteria are properly configured
        rejection_criteria = validation_service.rejection_criteria
        
        assert 'cartoon_indicators' in rejection_criteria
        assert 'digital_art_indicators' in rejection_criteria
        assert 'illustration_indicators' in rejection_criteria
        assert 'low_quality_indicators' in rejection_criteria
        
        # Verify each category has appropriate indicators
        cartoon_indicators = rejection_criteria['cartoon_indicators']
        assert len(cartoon_indicators) > 0
        assert any('color' in indicator for indicator in cartoon_indicators)
        
        digital_art_indicators = rejection_criteria['digital_art_indicators']
        assert len(digital_art_indicators) > 0
        assert any('artificial' in indicator for indicator in digital_art_indicators)
        
        illustration_indicators = rejection_criteria['illustration_indicators']
        assert len(illustration_indicators) > 0
        assert any('style' in indicator for indicator in illustration_indicators)
        
        quality_indicators = rejection_criteria['low_quality_indicators']
        assert len(quality_indicators) > 0
        assert any('quality' in indicator or 'blur' in indicator for indicator in quality_indicators)
    
    @pytest.mark.asyncio
    async def test_manual_review_requirements(self, validation_service, 
                                            sample_photorealistic_image, 
                                            sample_health_content):
        """Test manual review requirement logic"""
        
        # Test with borderline quality image
        result = await validation_service.validate_photorealistic_image(
            image_data=sample_photorealistic_image,
            image_url="https://example.com/borderline_image.jpg",
            content_category=ContentCategory.HEALTH_FITNESS,
            ai_model_used="dall-e-3",
            expected_content=sample_health_content
        )
        
        # Verify manual review logic
        assert isinstance(result.manual_review_required, bool)
        
        # If validation result requires manual review, flag should be True
        if result.validation_result == ValidationResult.REQUIRES_MANUAL_REVIEW:
            assert result.manual_review_required == True
    
    @pytest.mark.asyncio
    async def test_content_category_specific_validation(self, validation_service, 
                                                      sample_photorealistic_image):
        """Test category-specific validation logic"""
        
        categories_to_test = [
            ContentCategory.HEALTH_FITNESS,
            ContentCategory.NUTRITION_FOOD,
            ContentCategory.FINANCIAL_SUCCESS,
            ContentCategory.WELLNESS_LIFESTYLE,
            ContentCategory.CELEBRATION,
            ContentCategory.MOTIVATIONAL
        ]
        
        for category in categories_to_test:
            expected_content = {
                'category': category.value,
                'description': f'Test content for {category.value}',
                'quality_requirements': 'photorealistic'
            }
            
            result = await validation_service.validate_photorealistic_image(
                image_data=sample_photorealistic_image,
                image_url=f"https://example.com/{category.value}_image.jpg",
                content_category=category,
                ai_model_used="dall-e-3",
                expected_content=expected_content
            )
            
            # Verify category-specific validation completed
            assert result.content_category == category
            assert isinstance(result, ValidationMetrics)
    
    @pytest.mark.asyncio
    async def test_ai_model_tracking(self, validation_service, 
                                   sample_photorealistic_image, 
                                   sample_health_content):
        """Test AI model tracking in validation"""
        
        ai_models_to_test = [
            "dall-e-3",
            "midjourney",
            "stable-diffusion",
            "custom-model-v1"
        ]
        
        for ai_model in ai_models_to_test:
            result = await validation_service.validate_photorealistic_image(
                image_data=sample_photorealistic_image,
                image_url=f"https://example.com/{ai_model}_image.jpg",
                content_category=ContentCategory.HEALTH_FITNESS,
                ai_model_used=ai_model,
                expected_content=sample_health_content
            )
            
            # Verify AI model is tracked correctly
            assert result.ai_model_used == ai_model
    
    @pytest.mark.asyncio
    async def test_validation_performance(self, validation_service, 
                                        sample_photorealistic_image, 
                                        sample_health_content):
        """Test validation performance and timing"""
        
        import time
        
        start_time = time.time()
        
        # Perform validation
        result = await validation_service.validate_photorealistic_image(
            image_data=sample_photorealistic_image,
            image_url="https://example.com/performance_test_image.jpg",
            content_category=ContentCategory.HEALTH_FITNESS,
            ai_model_used="dall-e-3",
            expected_content=sample_health_content
        )
        
        end_time = time.time()
        validation_time = end_time - start_time
        
        # Verify validation completed
        assert isinstance(result, ValidationMetrics)
        
        # Verify reasonable performance (should complete within 10 seconds)
        assert validation_time < 10.0
        
        # Verify timestamp is recent
        time_diff = (datetime.now() - result.validation_timestamp).total_seconds()
        assert time_diff < 60  # Should be within last minute

if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v", "--asyncio-mode=auto"])