"""
AI Service for BKR Website Chatbot
Uses Groq API with Llama model to answer questions about B Kishore Reddy
Implements RAG-like approach with website data
"""

import os
from groq import Groq
import httpx
from website_data import (
    SYSTEM_PROMPT, 
    get_all_website_data,
    get_health_camps_info,
    KISHORE_REDDY_INFO,
    FAQ
)


class AIService:
    """AI service for chatbot using Groq API"""
    
    def __init__(self, db=None):
        """Initialize Groq client with API key from environment
        
        Args:
            db: Database instance for fetching dynamic content
        """
        api_key = os.getenv('GROQ_API_KEY')
        if not api_key:
            raise ValueError('GROQ_API_KEY must be set in environment variables')
        
        
        http_client = httpx.Client(proxies=None)

        self.client = Groq(api_key=api_key, http_client=http_client)
        self.model = "llama-3.1-8b-instant"
        self.db = db
        self.website_context = get_all_website_data(db)
        
    def _build_context_prompt(self, user_message, chat_history=None):
        """
        Build a prompt with website context and chat history
        
        Args:
            user_message (str): Current user question
            chat_history (list): Previous messages in conversation
            
        Returns:
            list: Formatted messages for Groq API
        """
        messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "system",
                "content": f"Here is the information you can use to answer questions:\n\n{self.website_context}"
            }
        ]
        
        # Add chat history for context awareness
        if chat_history:
            for msg in chat_history[-10:]:  # Last 10 messages for context
                messages.append({
                    "role": msg.get('role', 'user'),
                    "content": msg.get('content', '')
                })
        
        # Add current user message
        messages.append({
            "role": "user",
            "content": user_message
        })
        
        return messages
    
    def _enhance_response_with_health_camps(self, response):
        """
        Append health camps information to relevant responses
        
        Args:
            response (str): AI generated response
            
        Returns:
            str: Enhanced response with health camps info
        """
        # Keywords that trigger health camp info addition
        health_keywords = [
            'health', 'camp', 'medical', 'doctor', 'service', 'free',
            'help', 'community', 'initiative', 'what does', 'what can'
        ]
        
        response_lower = response.lower()
        
        # Check if response is relevant to add health camps info
        if any(keyword in response_lower for keyword in health_keywords):
            if 'health camp' not in response_lower:
                # Add health camps information dynamically from database
                response += f"\n\n💡 **Did you know?**\n{get_health_camps_info(self.db).strip()}"
        
        return response
    
    def chat(self, user_message, chat_history=None, session_id=None):
        """
        Generate AI response for user message
        
        Args:
            user_message (str): User's question
            chat_history (list): Previous conversation messages
            session_id (str): Session identifier for tracking
            
        Returns:
            dict: Response with message, success status, and metadata
        """
        try:
            # Build messages with context
            messages = self._build_context_prompt(user_message, chat_history)
            
            # Call Groq API
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,  # Lower temperature for more focused responses
                max_tokens=800,  # Reasonable length
                top_p=0.9,
                stream=False,  # We'll use non-streaming for simpler implementation
                stop=None
            )
            
            # Extract response
            ai_response = completion.choices[0].message.content
            
            # Enhance with health camps info if relevant
            ai_response = self._enhance_response_with_health_camps(ai_response)
            
            return {
                'success': True,
                'message': ai_response,
                'model': self.model,
                'usage': {
                    'prompt_tokens': completion.usage.prompt_tokens,
                    'completion_tokens': completion.usage.completion_tokens,
                    'total_tokens': completion.usage.total_tokens
                }
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': "I'm having trouble responding right now. Please try again or contact us directly at +91-9XXXXXX363."
            }
    
    def chat_stream(self, user_message, chat_history=None):
        """
        Generate streaming AI response for real-time display
        
        Args:
            user_message (str): User's question
            chat_history (list): Previous conversation messages
            
        Yields:
            str: Chunks of the response as they're generated
        """
        try:
            messages = self._build_context_prompt(user_message, chat_history)
            
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=800,
                top_p=0.9,
                stream=True,
                stop=None
            )
            
            full_response = ""
            for chunk in completion:
                if chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    full_response += content
                    yield content
            
            # After streaming is complete, check if we should add health camps info
            if full_response:
                additional_info = self._enhance_response_with_health_camps(full_response)
                if len(additional_info) > len(full_response):
                    # There's additional content to send
                    yield additional_info[len(full_response):]
                    
        except Exception as e:
            yield f"\n\n❌ Error: {str(e)}\nPlease try again or contact us directly."
    
    def get_quick_response(self, question_type):
        """
        Get quick predefined responses for common questions
        
        Args:
            question_type (str): Type of quick question
            
        Returns:
            str: Quick response
        """
        quick_responses = {
            'contact': f"📞 Contact Information:\n- Phone: {KISHORE_REDDY_INFO['contact']['phone']}\n- Email: {KISHORE_REDDY_INFO['contact']['email']}\n- Office: {KISHORE_REDDY_INFO['contact']['office']}",
            'health_camps': get_health_camps_info(self.db),
            'volunteer': "You can register as a volunteer through our website's Volunteer Registration form. We'll contact you with opportunities!",
            'complaint': "File a complaint through our website's 'File Complaint' page. We respond within 48 hours!"
        }
        
        return quick_responses.get(question_type, "How can I help you today?")
    
    def is_relevant_question(self, user_message):
        """
        Check if user question is relevant to BKR/Kishore Reddy
        
        Args:
            user_message (str): User's question
            
        Returns:
            bool: True if relevant, False otherwise
        """
        relevant_keywords = [
            'bongnuri','kishore','bongnuri kishore reddy',
            'reddy', 'bkr', 'foundation', 'quthbullapur',
            'health camp', 'volunteer', 'congress', 'complaint',
            'contact', 'help', 'service', 'initiative', 'agenda'
        ]
        
        message_lower = user_message.lower()
        return any(keyword in message_lower for keyword in relevant_keywords)
