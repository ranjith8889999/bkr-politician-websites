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
    def analyze_complaints(self, user_message, complaints, chat_history=None):
        """
        AI-powered complaint analysis for administrative decision making
        
        Args:
            user_message (str): Admin's question about complaints
            complaints (list): List of complaint objects
            chat_history (list): Previous conversation context
            
        Returns:
            dict: Analysis response with success status and message
        """
        try:
            # Build complaint summary for context
            total_complaints = len(complaints)
            
            # Categorize complaints
            category_counts = {}
            area_counts = {}
            status_counts = {}
            
            for complaint in complaints:
                category = complaint.get('category', 'Unknown')
                area = complaint.get('area', 'Unknown')
                status = complaint.get('status', 'pending')
                
                category_counts[category] = category_counts.get(category, 0) + 1
                area_counts[area] = area_counts.get(area, 0) + 1
                status_counts[status] = status_counts.get(status, 0) + 1
            
            # Build analysis context
            analysis_context = f"""
You are an AI assistant helping an administrator analyze citizen complaints for B Kishore Reddy's constituency. 
Your role is to provide data-driven insights to help prioritize and resolve complaints efficiently.

TOTAL COMPLAINTS: {total_complaints}

COMPLAINTS BY CATEGORY:
"""
            for category, count in sorted(category_counts.items(), key=lambda x: x[1], reverse=True):
                analysis_context += f"- {category}: {count} complaints\n"
            
            analysis_context += f"\nCOMPLAINTS BY AREA:\n"
            for area, count in sorted(area_counts.items(), key=lambda x: x[1], reverse=True)[:10]:
                analysis_context += f"- {area}: {count} complaints\n"
            
            analysis_context += f"\nCOMPLAINTS BY STATUS:\n"
            for status, count in status_counts.items():
                analysis_context += f"- {status}: {count} complaints\n"
            
            # Add prioritization criteria
            analysis_context += """

PRIORITIZATION CRITERIA:
1. **HIGH PRIORITY** - Safety hazards (electrical, flooding, structural risks), health emergencies (dengue, contaminated water), issues affecting many people
2. **MEDIUM PRIORITY** - Infrastructure issues (roads, drainage), frequent but non-urgent problems, quality of life improvements
3. **LOW PRIORITY** - Individual requests, minor inconveniences, long-term development projects

TIME TO RESOLVE ESTIMATES:
- Quick fixes (1-2 weeks): Street lights, fogging, minor repairs
- Medium duration (1-2 months): Drainage cleaning, pothole filling, water pipeline repairs
- Long-term (3-6 months): New water connections, road construction, major infrastructure

COST ESTIMATES:
- Low cost (<₹50,000): Street light installation, fogging, minor repairs
- Medium cost (₹50,000-₹5,00,000): Drainage work, water pipeline repairs, road resurfacing
- High cost (>₹5,00,000): New water infrastructure, major road construction, electrical upgrades

When analyzing:
- Identify patterns and clusters of similar complaints
- Consider impact (how many people affected)
- Assess urgency (safety vs convenience)
- Suggest quick wins (low cost, high impact)
- Recommend strategic long-term solutions
- Be specific with areas and complaint types
- Provide actionable recommendations

Always base your analysis on the actual complaint data provided.
"""
            
            # Build messages for AI
            messages = [
                {"role": "system", "content": analysis_context}
            ]
            
            # Add chat history if provided
            if chat_history:
                messages.extend(chat_history[-5:])  # Last 5 messages for context
            
            # Add current question with complaint details
            detailed_message = f"{user_message}\n\nCOMPLAINT DETAILS:\n"
            for i, complaint in enumerate(complaints[:50], 1):  # Limit to 50 for token management
                detailed_message += f"\n{i}. {complaint.get('category')} - {complaint.get('area')}"
                detailed_message += f"\n   Subject: {complaint.get('subject')}"
                detailed_message += f"\n   Status: {complaint.get('status')}"
                detailed_message += f"\n   Date: {complaint.get('date')}"
            
            if len(complaints) > 50:
                detailed_message += f"\n... and {len(complaints) - 50} more complaints"
            
            messages.append({"role": "user", "content": detailed_message})
            
            # Get AI response
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=2000
            )
            
            response_message = completion.choices[0].message.content
            
            return {
                'success': True,
                'message': response_message,
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
                'message': f"I encountered an error while analyzing the complaints: {str(e)}"
            }