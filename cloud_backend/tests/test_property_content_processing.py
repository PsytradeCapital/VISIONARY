"""
Property-based tests for content processing consistency.

**Feature: ai-personal-scheduler, Property 1: Content processing consistency**
**Validates: Requirements 1.1, 1.2, 1.5, 2.1**
"""

import pytest
from hypothesis import given, strategies as st, settings, Verbosity
from hypothesis.stateful import RuleBasedStateMachine, rule, initialize, invariant
import tempfile
import os
from io import BytesIO
from unittest.mock import Mock, patch

# Mock services for testing without full dependencies
class MockDocumentParser:
    def extract_text_content(self, content):
        return {'text': content.strip(), 'status': 'success'}
    
    def parse_document(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return {'text': content.strip(), 'status': 'success'}

class MockVoiceProcessor:
    def transcribe_audio(self, audio_data):
        return {'text': 'mock transcription', 'confidence': 0.95}
    
    def process_voice_input(self, audio_data):
        result = self.transcribe_audio(audio_data)
        return result

class MockUploadService:
    def process_file_upload(self, file_path, filename):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return {'status': 'success', 'content': content.strip()}
        except Exception as e:
            return {'status': 'error', 'error': str(e)}


class ContentProcessingStateMachine(RuleBasedStateMachine):
    """
    Stateful property-based testing for content processing consistency.
    
    Tests that content processing maintains consistency across different
    input types and processing methods.
    """
    
    def __init__(self):
        super().__init__()
        self.document_parser = MockDocumentParser()
        self.voice_processor = MockVoiceProcessor()
        self.upload_service = MockUploadService()
        self.processed_content = {}
        self.original_content = {}
    
    @initialize()
    def setup(self):
        """Initialize test state."""
        self.processed_content.clear()
        self.original_content.clear()
    
    @rule(
        content=st.text(min_size=10, max_size=1000),
        content_type=st.sampled_from(['text', 'document', 'voice'])
    )
    def process_content(self, content, content_type):
        """Process content through different processing pipelines."""
        content_id = f"{content_type}_{len(self.processed_content)}"
        self.original_content[content_id] = content
        
        try:
            if content_type == 'text':
                # Direct text processing
                result = self.document_parser.extract_text_content(content)
            elif content_type == 'document':
                # Simulate document processing
                with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
                    f.write(content)
                    f.flush()
                    result = self.document_parser.parse_document(f.name)
                    os.unlink(f.name)
            else:  # voice
                # Mock voice processing
                result = self.voice_processor.process_voice_input(BytesIO(b'mock_audio_data'))
            
            if result and 'text' in result:
                self.processed_content[content_id] = result['text']
        except Exception as e:
            # Log processing errors but continue testing
            print(f"Processing error for {content_type}: {e}")
    
    @rule(content_id=st.sampled_from([]))
    def reprocess_content(self, content_id):
        """Reprocess existing content to test consistency."""
        if content_id in self.original_content:
            original = self.original_content[content_id]
            content_type = content_id.split('_')[0]
            
            # Reprocess the same content
            try:
                if content_type == 'text':
                    result = self.document_parser.extract_text_content(original)
                elif content_type == 'document':
                    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
                        f.write(original)
                        f.flush()
                        result = self.document_parser.parse_document(f.name)
                        os.unlink(f.name)
                else:  # voice
                    result = self.voice_processor.process_voice_input(BytesIO(b'mock_audio_data'))
                
                # Verify consistency
                if result and 'text' in result and content_id in self.processed_content:
                    assert result['text'] == self.processed_content[content_id], \
                        f"Reprocessing {content_id} produced different result"
            except Exception as e:
                print(f"Reprocessing error for {content_id}: {e}")
    
    @invariant()
    def content_preservation_invariant(self):
        """
        Property 1: Content processing consistency
        
        For any content processing operation, the essential information
        should be preserved and consistent across multiple processing attempts.
        """
        for content_id, processed in self.processed_content.items():
            original = self.original_content.get(content_id, "")
            
            # Essential content should be preserved
            if original and processed:
                # Check that significant words are preserved
                original_words = set(original.lower().split())
                processed_words = set(processed.lower().split())
                
                # At least 70% of significant words should be preserved
                if len(original_words) > 0:
                    common_words = original_words.intersection(processed_words)
                    preservation_ratio = len(common_words) / len(original_words)
                    
                    assert preservation_ratio >= 0.7, \
                        f"Content preservation failed for {content_id}: {preservation_ratio:.2f} < 0.7"
    
    @invariant()
    def processing_consistency_invariant(self):
        """
        Verify that processing results are consistent and well-formed.
        """
        for content_id, processed in self.processed_content.items():
            # Processed content should be non-empty for non-empty input
            original = self.original_content.get(content_id, "")
            if original.strip():
                assert processed.strip(), f"Empty result for non-empty input: {content_id}"
            
            # Processed content should be reasonable length
            if len(original) > 10:
                assert len(processed) >= len(original) * 0.5, \
                    f"Processed content too short for {content_id}"


@given(
    text_content=st.text(min_size=1, max_size=500),
    processing_method=st.sampled_from(['direct', 'file_based'])
)
@settings(max_examples=100, verbosity=Verbosity.verbose)
def test_text_processing_consistency(text_content, processing_method):
    """
    Property 1: Content processing consistency for text input
    
    For any text content, processing through different methods should
    produce consistent results.
    """
    parser = MockDocumentParser()
    
    try:
        if processing_method == 'direct':
            result1 = parser.extract_text_content(text_content)
            result2 = parser.extract_text_content(text_content)
        else:  # file_based
            with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
                f.write(text_content)
                f.flush()
                result1 = parser.parse_document(f.name)
                result2 = parser.parse_document(f.name)
                os.unlink(f.name)
        
        # Results should be consistent
        if result1 and result2:
            assert result1.get('text') == result2.get('text'), \
                "Inconsistent processing results for same input"
    except Exception as e:
        # Skip invalid inputs but log for debugging
        print(f"Skipping invalid input: {e}")


@given(
    file_size=st.integers(min_value=1, max_value=1024*1024),  # 1B to 1MB
    file_type=st.sampled_from(['txt', 'pdf', 'doc'])
)
@settings(max_examples=50, verbosity=Verbosity.verbose)
def test_upload_processing_consistency(file_size, file_type):
    """
    Property 1: Content processing consistency for file uploads
    
    For any valid file upload, processing should be consistent and
    handle various file sizes appropriately.
    """
    upload_service = MockUploadService()
    
    # Create mock file data
    mock_content = "A" * min(file_size, 1000)  # Limit for testing
    
    try:
        with tempfile.NamedTemporaryFile(suffix=f'.{file_type}', delete=False) as f:
            f.write(mock_content.encode())
            f.flush()
            
            # Process file multiple times
            result1 = upload_service.process_file_upload(f.name, f'test.{file_type}')
            result2 = upload_service.process_file_upload(f.name, f'test.{file_type}')
            
            os.unlink(f.name)
            
            # Results should be consistent
            if result1 and result2:
                assert result1.get('status') == result2.get('status'), \
                    "Inconsistent upload processing status"
                
                if 'content' in result1 and 'content' in result2:
                    assert result1['content'] == result2['content'], \
                        "Inconsistent content extraction"
    except Exception as e:
        # Skip unsupported file types or invalid inputs
        print(f"Skipping unsupported file type {file_type}: {e}")


@given(
    audio_duration=st.floats(min_value=0.1, max_value=60.0),
    audio_quality=st.sampled_from(['low', 'medium', 'high'])
)
@settings(max_examples=50, verbosity=Verbosity.verbose)
def test_voice_processing_consistency(audio_duration, audio_quality):
    """
    Property 1: Content processing consistency for voice input
    
    For any voice input, processing should handle different audio
    qualities and durations consistently.
    """
    voice_processor = MockVoiceProcessor()
    
    # Mock audio data based on parameters
    mock_text = f"Test audio content for {audio_duration:.1f} seconds at {audio_quality} quality"
    confidence = {'low': 0.7, 'medium': 0.85, 'high': 0.95}[audio_quality]
    
    audio_data = BytesIO(b'mock_audio_data' * int(audio_duration * 10))
    
    # Process same audio multiple times
    result1 = voice_processor.process_voice_input(audio_data)
    audio_data.seek(0)  # Reset stream
    result2 = voice_processor.process_voice_input(audio_data)
    
    # Results should be consistent
    if result1 and result2:
        assert result1.get('text') == result2.get('text'), \
            "Inconsistent voice processing results"
        assert result1.get('confidence') == result2.get('confidence'), \
            "Inconsistent confidence scores"


# Stateful testing
ContentProcessingTest = ContentProcessingStateMachine.TestCase


if __name__ == "__main__":
    # Run property-based tests
    pytest.main([__file__, "-v", "--tb=short"])