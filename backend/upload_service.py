import os
import json
import asyncio
from typing import List, Dict, Any, Optional
from fastapi import UploadFile, HTTPException
import PyPDF2
import docx
import io
import re
from datetime import datetime
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models import KnowledgeEntry, KnowledgeEntryCreate
from database import get_db
import logging

logger = logging.getLogger(__name__)

class UploadProcessingService:
    """Service for processing document uploads, voice inputs, and text processing"""
    
    def __init__(self):
        self.supported_formats = {'.pdf', '.txt', '.docx'}
        self.category_keywords = {
            'financial': ['money', 'budget', 'savings', 'investment', 'income', 'expense', 'financial', 'debt', 'credit'],
            'health': ['exercise', 'workout', 'fitness', 'health', 'medical', 'doctor', 'gym', 'running', 'weight'],
            'nutrition': ['food', 'meal', 'diet', 'nutrition', 'eating', 'recipe', 'cooking', 'calories', 'protein'],
            'psychological': ['meditation', 'mindfulness', 'therapy', 'mental', 'stress', 'anxiety', 'mood', 'wellbeing'],
            'task': ['work', 'project', 'meeting', 'deadline', 'task', 'appointment', 'schedule', 'reminder']
        }
    
    async def process_document(self, file: UploadFile, user_id) -> Dict[str, Any]:
        """Process uploaded document and extract content"""
        try:
            # Validate file format
            file_extension = os.path.splitext(file.filename or '')[1].lower()
            if file_extension not in self.supported_formats:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Unsupported file format. Supported formats: {', '.join(self.supported_formats)}"
                )
            
            # Read file content
            content = await file.read()
            
            # Extract text based on file type
            if file_extension == '.pdf':
                text_content = await self._extract_pdf_text(content)
            elif file_extension == '.txt':
                text_content = content.decode('utf-8')
            elif file_extension == '.docx':
                text_content = await self._extract_docx_text(content)
            else:
                raise HTTPException(status_code=400, detail="Unsupported file format")
            
            # Process the extracted text
            processed_content = await self._process_text_content(text_content, user_id, 'document')
            
            return {
                'id': processed_content['id'],
                'filename': file.filename,
                'content_length': len(text_content),
                'category': processed_content['category'],
                'extracted_items': processed_content['extracted_items'],
                'confidence': processed_content['confidence']
            }
            
        except Exception as e:
            logger.error(f"Error processing document: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error processing document: {str(e)}")
    
    async def process_voice_input(self, file: UploadFile, user_id) -> Dict[str, Any]:
        """Process voice input and convert to text"""
        try:
            # Read audio data
            audio_data = await file.read()
            
            # TODO: Implement Google Speech-to-Text API integration
            # For now, return a placeholder
            text_content = "Voice input processing not yet implemented"
            
            processed_content = await self._process_text_content(text_content, user_id, 'voice')
            
            return {
                'id': processed_content['id'],
                'transcribed_text': text_content,
                'category': processed_content['category'],
                'extracted_items': processed_content['extracted_items'],
                'confidence': processed_content['confidence']
            }
            
        except Exception as e:
            logger.error(f"Error processing voice input: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error processing voice input: {str(e)}")
    
    async def process_text_input(self, text: str, user_id) -> Dict[str, Any]:
        """Process direct text input"""
        try:
            processed_content = await self._process_text_content(text, user_id, 'text')
            
            return {
                'id': processed_content['id'],
                'content_length': len(text),
                'category': processed_content['category'],
                'extracted_items': processed_content['extracted_items'],
                'confidence': processed_content['confidence']
            }
            
        except Exception as e:
            logger.error(f"Error processing text input: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error processing text input: {str(e)}")
    
    async def _extract_pdf_text(self, content: bytes) -> str:
        """Extract text from PDF content"""
        try:
            pdf_file = io.BytesIO(content)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            
            return text.strip()
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error reading PDF: {str(e)}")
    
    async def _extract_docx_text(self, content: bytes) -> str:
        """Extract text from DOCX content"""
        try:
            doc_file = io.BytesIO(content)
            doc = docx.Document(doc_file)
            
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            
            return text.strip()
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error reading DOCX: {str(e)}")
    
    async def _process_text_content(self, text: str, user_id, source_type: str) -> Dict[str, Any]:
        """Process text content and categorize it"""
        try:
            # Categorize content
            category = self._categorize_content(text)
            
            # Extract actionable items
            extracted_items = self._extract_actionable_items(text)
            
            # Calculate confidence score
            confidence = self._calculate_confidence(text, category, extracted_items)
            
            # Ensure user_id is a UUID object
            import uuid
            if isinstance(user_id, str):
                user_id = uuid.UUID(user_id)
            
            # Store in knowledge base
            knowledge_entry = KnowledgeEntry(
                user_id=user_id,
                source_type=source_type,
                content=text,
                extracted_data={
                    'routines': extracted_items.get('routines', []),
                    'goals': extracted_items.get('goals', []),
                    'preferences': extracted_items.get('preferences', []),
                    'constraints': extracted_items.get('constraints', [])
                },
                category=category,
                confidence=confidence
            )
            
            # TODO: Save to database (requires database session)
            # For now, return the processed data
            
            return {
                'id': str(knowledge_entry.id),
                'category': category,
                'extracted_items': extracted_items,
                'confidence': confidence,
                'content': text[:200] + '...' if len(text) > 200 else text
            }
            
        except Exception as e:
            logger.error(f"Error processing text content: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error processing content: {str(e)}")
    
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
    
    def _extract_actionable_items(self, text: str) -> Dict[str, List[str]]:
        """Extract actionable items from text"""
        items = {
            'routines': [],
            'goals': [],
            'preferences': [],
            'constraints': []
        }
        
        # Simple pattern matching for different types of items
        lines = text.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            line_lower = line.lower()
            
            # Detect routines (daily/weekly patterns)
            if any(word in line_lower for word in ['daily', 'every day', 'morning', 'evening', 'routine']):
                items['routines'].append(line)
            
            # Detect goals (future-oriented statements)
            elif any(word in line_lower for word in ['goal', 'want to', 'plan to', 'achieve', 'target']):
                items['goals'].append(line)
            
            # Detect preferences (like/dislike statements)
            elif any(word in line_lower for word in ['prefer', 'like', 'enjoy', 'favorite', 'best time']):
                items['preferences'].append(line)
            
            # Detect constraints (limitations)
            elif any(word in line_lower for word in ['cannot', 'busy', 'unavailable', 'conflict', 'limited']):
                items['constraints'].append(line)
        
        return items
    
    def _calculate_confidence(self, text: str, category: str, extracted_items: Dict[str, List[str]]) -> float:
        """Calculate confidence score for the categorization and extraction"""
        base_confidence = 0.5
        
        # Increase confidence based on text length
        if len(text) > 100:
            base_confidence += 0.1
        if len(text) > 500:
            base_confidence += 0.1
        
        # Increase confidence based on extracted items
        total_items = sum(len(items) for items in extracted_items.values())
        if total_items > 0:
            base_confidence += min(0.3, total_items * 0.05)
        
        # Increase confidence based on category keyword matches
        category_keywords = self.category_keywords.get(category, [])
        keyword_matches = sum(1 for keyword in category_keywords if keyword in text.lower())
        if keyword_matches > 0:
            base_confidence += min(0.2, keyword_matches * 0.05)
        
        return min(1.0, base_confidence)

# Global service instance
upload_service = UploadProcessingService()