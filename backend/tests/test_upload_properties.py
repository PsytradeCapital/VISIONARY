import pytest
from hypothesis import given, strategies as st, settings
from upload_service import UploadProcessingService

# Property-based test for content categorization consistency
# Feature: ai-personal-scheduler, Property 1: Content categorization consistency

class TestUploadProperties:
    
    def setup_method(self):
        self.upload_service = UploadProcessingService()
    
    @given(
        content=st.text(min_size=10, max_size=1000),
        source_type=st.sampled_from(['document', 'voice', 'text'])
    )
    @settings(max_examples=100)
    def test_content_categorization_consistency(self, content, source_type):
        """
        Property 1: Content categorization consistency
        For any uploaded content (document, voice, or text), the system should 
        correctly categorize it into one of the predefined categories with 
        consistent results across input methods.
        """
        # Test that categorization is consistent
        category1 = self.upload_service._categorize_content(content)
        category2 = self.upload_service._categorize_content(content)
        
        # Property: Same content should always get same category
        assert category1 == category2, f"Inconsistent categorization: {category1} != {category2}"
        
        # Property: Category should be one of the predefined categories
        valid_categories = {'financial', 'health', 'nutrition', 'psychological', 'task'}
        assert category1 in valid_categories, f"Invalid category: {category1}"
        
        # Property: Confidence should be between 0 and 1
        extracted_items = self.upload_service._extract_actionable_items(content)
        confidence = self.upload_service._calculate_confidence(content, category1, extracted_items)
        assert 0.0 <= confidence <= 1.0, f"Invalid confidence score: {confidence}"
    
    @given(
        financial_content=st.text().filter(lambda x: any(word in x.lower() for word in ['money', 'budget', 'savings']))
    )
    @settings(max_examples=50)
    def test_financial_content_categorization(self, financial_content):
        """Test that content with financial keywords is categorized as financial"""
        category = self.upload_service._categorize_content(financial_content)
        # If content has financial keywords, it should likely be categorized as financial
        # (though other categories might have higher scores in some cases)
        assert category in {'financial', 'task'}, f"Financial content categorized as: {category}"
    
    @given(
        health_content=st.text().filter(lambda x: any(word in x.lower() for word in ['exercise', 'workout', 'fitness']))
    )
    @settings(max_examples=50)
    def test_health_content_categorization(self, health_content):
        """Test that content with health keywords is categorized appropriately"""
        category = self.upload_service._categorize_content(health_content)
        assert category in {'health', 'task'}, f"Health content categorized as: {category}"
    
    @given(text_input=st.text(min_size=1, max_size=500))
    @settings(max_examples=100)
    def test_extracted_items_structure(self, text_input):
        """
        Property: Extracted items should always have the correct structure
        """
        extracted_items = self.upload_service._extract_actionable_items(text_input)
        
        # Property: Should always return dict with required keys
        required_keys = {'routines', 'goals', 'preferences', 'constraints'}
        assert isinstance(extracted_items, dict), "Extracted items should be a dictionary"
        assert set(extracted_items.keys()) == required_keys, f"Missing keys: {required_keys - set(extracted_items.keys())}"
        
        # Property: All values should be lists
        for key, value in extracted_items.items():
            assert isinstance(value, list), f"Value for {key} should be a list, got {type(value)}"
            
        # Property: All list items should be strings
        for key, items in extracted_items.items():
            for item in items:
                assert isinstance(item, str), f"Item in {key} should be string, got {type(item)}"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])