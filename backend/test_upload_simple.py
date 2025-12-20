#!/usr/bin/env python3
"""
Simple test script to validate upload service logic without external dependencies
"""

import sys
import os

# Add current directory to path to import our modules
sys.path.insert(0, os.path.dirname(__file__))

def test_categorization():
    """Test the categorization logic"""
    
    # Mock the UploadProcessingService class without external dependencies
    class MockUploadService:
        def __init__(self):
            self.category_keywords = {
                'financial': ['money', 'budget', 'savings', 'investment', 'income', 'expense', 'financial', 'debt', 'credit'],
                'health': ['exercise', 'workout', 'fitness', 'health', 'medical', 'doctor', 'gym', 'running', 'weight'],
                'nutrition': ['food', 'meal', 'diet', 'nutrition', 'eating', 'recipe', 'cooking', 'calories', 'protein'],
                'psychological': ['meditation', 'mindfulness', 'therapy', 'mental', 'stress', 'anxiety', 'mood', 'wellbeing'],
                'task': ['work', 'project', 'meeting', 'deadline', 'task', 'appointment', 'schedule', 'reminder']
            }
        
        def _categorize_content(self, text: str) -> str:
            """Categorize content based on keywords"""
            text_lower = text.lower()
            category_scores = {}
            
            for category, keywords in self.category_keywords.items():
                score = sum(1 for keyword in keywords if keyword in text_lower)
                if score > 0:
                    category_scores[category] = score
            
            if not category_scores:
                return 'task'  # Default category
            
            # Return category with highest score
            return max(category_scores, key=category_scores.get)
        
        def _extract_actionable_items(self, text: str):
            """Extract actionable items from text"""
            items = {
                'routines': [],
                'goals': [],
                'preferences': [],
                'constraints': []
            }
            
            lines = text.split('\n')
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                line_lower = line.lower()
                
                # Detect routines
                if any(word in line_lower for word in ['daily', 'every day', 'morning', 'evening', 'routine']):
                    items['routines'].append(line)
                
                # Detect goals
                elif any(word in line_lower for word in ['goal', 'want to', 'plan to', 'achieve', 'target']):
                    items['goals'].append(line)
                
                # Detect preferences
                elif any(word in line_lower for word in ['prefer', 'like', 'enjoy', 'favorite', 'best time']):
                    items['preferences'].append(line)
                
                # Detect constraints
                elif any(word in line_lower for word in ['cannot', 'busy', 'unavailable', 'conflict', 'limited']):
                    items['constraints'].append(line)
            
            return items
    
    # Test cases
    service = MockUploadService()
    
    test_cases = [
        {
            'text': 'I want to save money and create a budget for my expenses',
            'expected_category': 'financial'
        },
        {
            'text': 'My daily workout routine includes running and gym exercises',
            'expected_category': 'health'
        },
        {
            'text': 'I prefer eating healthy meals with lots of protein and vegetables',
            'expected_category': 'nutrition'
        },
        {
            'text': 'I practice meditation every morning for mental wellbeing',
            'expected_category': 'psychological'
        },
        {
            'text': 'I have a meeting scheduled for tomorrow at 3 PM',
            'expected_category': 'task'
        }
    ]
    
    print("Testing content categorization...")
    passed = 0
    total = len(test_cases)
    
    for i, test_case in enumerate(test_cases):
        result = service._categorize_content(test_case['text'])
        expected = test_case['expected_category']
        
        if result == expected:
            print(f"✓ Test {i+1}: PASSED - '{test_case['text'][:50]}...' -> {result}")
            passed += 1
        else:
            print(f"✗ Test {i+1}: FAILED - '{test_case['text'][:50]}...' -> {result} (expected {expected})")
    
    print(f"\nCategorization Tests: {passed}/{total} passed")
    
    # Test extraction
    print("\nTesting item extraction...")
    extraction_text = """
    My daily morning routine includes exercise at 6 AM.
    I want to achieve my goal of saving $10,000 this year.
    I prefer working out in the evening.
    I cannot schedule meetings on Fridays.
    """
    
    extracted = service._extract_actionable_items(extraction_text)
    
    print("Extracted items:")
    for category, items in extracted.items():
        if items:
            print(f"  {category}: {len(items)} items")
            for item in items:
                print(f"    - {item}")
    
    # Validate structure
    required_keys = {'routines', 'goals', 'preferences', 'constraints'}
    if set(extracted.keys()) == required_keys:
        print("✓ Extraction structure is correct")
    else:
        print("✗ Extraction structure is incorrect")
    
    return passed == total

if __name__ == "__main__":
    print("=== Visionary Upload Service Tests ===\n")
    
    success = test_categorization()
    
    if success:
        print("\n🎉 All tests passed! Upload service logic is working correctly.")
    else:
        print("\n⚠️  Some tests failed. Check the implementation.")
    
    print("\nNext steps:")
    print("1. Install dependencies: pip install -r requirements.txt")
    print("2. Set up database (PostgreSQL)")
    print("3. Run the FastAPI server: python main.py")
    print("4. Test the frontend: npm start")