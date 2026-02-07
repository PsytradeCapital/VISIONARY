import os
import json
import re
from typing import Dict, List, Any
import google.generativeai as genai
from datetime import datetime, timedelta

class GeminiAIService:
    """AI service using Google Gemini API (FREE)"""
    
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-pro')
            self.enabled = True
        else:
            self.enabled = False
            print("⚠️ GEMINI_API_KEY not set - AI features will use fallback")
    
    async def generate_schedule(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate personalized schedule using Gemini AI"""
        if not self.enabled:
            return self._generate_fallback_schedule(user_data)
        
        try:
            prompt = f"""Generate a personalized daily schedule in JSON format.

User Information:
- Goals: {', '.join(user_data.get('goals', ['productivity', 'health']))}
- Preferences: {user_data.get('preferences', {})}
- Available time: {user_data.get('available_hours', 8)} hours

Create a schedule with 5-8 time blocks. Each block should have:
- title: Activity name
- start_time: HH:MM format
- end_time: HH:MM format
- category: one of (health, work, personal, learning, break)
- priority: 1-5 (5 is highest)
- description: Brief description

Return ONLY valid JSON in this format:
{{
  "schedule_id": "unique_id",
  "blocks": [
    {{
      "id": "block_1",
      "title": "Morning Exercise",
      "start_time": "07:00",
      "end_time": "08:00",
      "category": "health",
      "priority": 4,
      "description": "30-minute workout session"
    }}
  ],
  "generated_at": "{datetime.now().isoformat()}"
}}"""

            response = self.model.generate_content(prompt)
            text = response.text.strip()
            
            # Extract JSON from response
            json_match = re.search(r'\{.*\}', text, re.DOTALL)
            if json_match:
                schedule_data = json.loads(json_match.group())
                return schedule_data
            else:
                return self._generate_fallback_schedule(user_data)
                
        except Exception as e:
            print(f"Gemini AI error: {e}")
            return self._generate_fallback_schedule(user_data)
    
    async def generate_motivational_content(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate motivational content using Gemini"""
        if not self.enabled:
            return self._generate_fallback_motivation(user_data)
        
        try:
            prompt = f"""Generate motivational content for a user.

User: {user_data.get('userName', 'Champion')}
Goals: {', '.join(user_data.get('goals', ['success']))}
Progress: {user_data.get('currentProgress', {})}

Create a short, inspiring message (2-3 sentences) that:
1. Acknowledges their progress
2. Encourages them to keep going
3. Is personal and warm

Return JSON:
{{
  "title": "Motivational title",
  "message": "Your inspiring message here",
  "tone": "supportive"
}}"""

            response = self.model.generate_content(prompt)
            text = response.text.strip()
            
            json_match = re.search(r'\{.*\}', text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                return self._generate_fallback_motivation(user_data)
                
        except Exception as e:
            print(f"Gemini AI error: {e}")
            return self._generate_fallback_motivation(user_data)
    
    async def analyze_document(self, text: str) -> Dict[str, Any]:
        """Analyze document content using Gemini"""
        if not self.enabled:
            return self._analyze_document_fallback(text)
        
        try:
            prompt = f"""Analyze this text and extract actionable items.

Text: {text[:1000]}

Identify:
1. Tasks or action items
2. Goals or objectives
3. Deadlines or time references
4. Category (health, financial, work, personal, learning)

Return JSON:
{{
  "category": "main category",
  "confidence": 0.8,
  "tasks": ["task 1", "task 2"],
  "goals": ["goal 1"],
  "deadlines": ["deadline 1"],
  "summary": "Brief summary"
}}"""

            response = self.model.generate_content(prompt)
            text_response = response.text.strip()
            
            json_match = re.search(r'\{.*\}', text_response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                return self._analyze_document_fallback(text)
                
        except Exception as e:
            print(f"Gemini AI error: {e}")
            return self._analyze_document_fallback(text)
    
    def _generate_fallback_schedule(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback schedule when AI is unavailable"""
        return {
            "schedule_id": f"schedule_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "blocks": [
                {
                    "id": "block_1",
                    "title": "Morning Routine",
                    "start_time": "07:00",
                    "end_time": "08:00",
                    "category": "health",
                    "priority": 4,
                    "description": "Start your day with exercise and breakfast"
                },
                {
                    "id": "block_2",
                    "title": "Focus Work",
                    "start_time": "09:00",
                    "end_time": "12:00",
                    "category": "work",
                    "priority": 5,
                    "description": "Deep work on priority tasks"
                },
                {
                    "id": "block_3",
                    "title": "Lunch Break",
                    "start_time": "12:00",
                    "end_time": "13:00",
                    "category": "break",
                    "priority": 3,
                    "description": "Healthy meal and rest"
                },
                {
                    "id": "block_4",
                    "title": "Afternoon Tasks",
                    "start_time": "13:00",
                    "end_time": "16:00",
                    "category": "work",
                    "priority": 4,
                    "description": "Complete remaining tasks"
                },
                {
                    "id": "block_5",
                    "title": "Personal Time",
                    "start_time": "18:00",
                    "end_time": "20:00",
                    "category": "personal",
                    "priority": 3,
                    "description": "Hobbies, family, relaxation"
                }
            ],
            "generated_at": datetime.now().isoformat()
        }
    
    def _generate_fallback_motivation(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback motivation when AI is unavailable"""
        name = user_data.get('userName', 'Champion')
        return {
            "title": f"Keep Going, {name}!",
            "message": f"You're making great progress on your goals. Every step forward counts, no matter how small. Stay focused and keep pushing!",
            "tone": "supportive"
        }
    
    def _analyze_document_fallback(self, text: str) -> Dict[str, Any]:
        """Fallback document analysis"""
        # Simple keyword-based categorization
        text_lower = text.lower()
        
        category = "task"
        if any(word in text_lower for word in ['save', 'money', 'budget', 'invest']):
            category = "financial"
        elif any(word in text_lower for word in ['exercise', 'workout', 'health', 'fitness']):
            category = "health"
        elif any(word in text_lower for word in ['eat', 'meal', 'diet', 'nutrition']):
            category = "nutrition"
        elif any(word in text_lower for word in ['learn', 'study', 'course', 'skill']):
            category = "learning"
        
        return {
            "category": category,
            "confidence": 0.6,
            "tasks": [],
            "goals": [],
            "deadlines": [],
            "summary": text[:200] + "..." if len(text) > 200 else text
        }

# Global instance
gemini_service = GeminiAIService()
