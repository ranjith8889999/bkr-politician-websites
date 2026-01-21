# 🤖 AI Chatbot Implementation Guide

## Overview
Successfully implemented an AI-powered chatbot using Groq API (Llama 3.1-8B) that answers questions about B Kishore Reddy and BKR Foundation based exclusively on website data.

## ✨ Features

### 🎯 Core Capabilities
- **Context-Aware Conversations**: Remembers previous messages in the conversation
- **Website Data Only**: Answers strictly from website_data.py constants
- **Health Camps Promotion**: Automatically mentions health camps when relevant
- **Session Persistence**: Saves chat history in database and localStorage
- **Beautiful UI**: Modern floating chat widget with smooth animations
- **Mobile Responsive**: Works perfectly on all devices
- **Real-time Responses**: Fast AI-generated answers using Groq's Llama model

### 🛡️ Safety Features
- Only answers questions about B Kishore Reddy, BKR Foundation, and related topics
- Politely redirects off-topic questions
- Stores all conversations in database for analysis
- Rate limiting can be added to prevent abuse

## 📁 Files Created

### Backend Files
1. **backend/website_data.py** - All website content as constants
2. **backend/ai_service.py** - Groq API integration and AI logic
3. **backend/app.py** - Added chat API endpoints
4. **backend/database.py** - Added chat database functions
5. **backend/models.py** - Added chat tables schema
6. **backend/.env** - Added GROQ_API_KEY

### Frontend Files
1. **css/chatbot.css** - Complete chatbot styling
2. **js/chatbot.js** - Chatbot functionality and UI
3. **index.html** - Integrated chatbot

## 🔧 API Endpoints

### 1. Create Chat Session
```
POST /api/chat/session
```
Creates a new chat session and returns session_id.

### 2. Send Message
```
POST /api/chat/message
Content-Type: application/json

{
  "message": "Who is B Kishore Reddy?",
  "session_id": "uuid-here" // optional
}
```
Returns AI response based on website data.

### 3. Get Chat History
```
GET /api/chat/history/{session_id}?limit=50
```
Retrieves chat history for a session.

### 4. Chat Statistics (Protected)
```
GET /api/chat/stats
X-API-Key: your-api-key
```
Returns statistics about chat usage.

## 🗄️ Database Tables

### chat_conversations
```sql
- id (SERIAL PRIMARY KEY)
- session_id (VARCHAR UNIQUE)
- user_ip (VARCHAR)
- user_agent (TEXT)
- created_at (TIMESTAMP)
- updated_at (TIMESTAMP)
```

### chat_messages
```sql
- id (SERIAL PRIMARY KEY)
- session_id (VARCHAR FK)
- role (VARCHAR: user/assistant/system)
- content (TEXT)
- tokens_used (INTEGER)
- created_at (TIMESTAMP)
```

## 🚀 How It Works

### 1. User Opens Chat
- Floating chat button appears on website
- Click to open chat window
- Welcome message with quick suggestions

### 2. User Asks Question
- Types question and sends
- Frontend sends to `/api/chat/message`
- Backend retrieves chat history for context

### 3. AI Processing (RAG-like Approach)
```python
# 1. Build context from website data
context = get_all_website_data()

# 2. Add system prompt with rules
system_prompt = SYSTEM_PROMPT + context

# 3. Add chat history (last 10 messages)
messages = [system, history..., user_message]

# 4. Call Groq API
response = groq.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=messages,
    temperature=0.7
)

# 5. Enhance with health camps info if relevant
enhanced_response = add_health_camps_info(response)
```

### 4. Response Delivery
- AI response saved to database
- Sent back to frontend
- Displayed in chat window
- Session maintained for context

## 📝 Website Data Structure

All information is in `backend/website_data.py`:

```python
KISHORE_REDDY_INFO = {
    "name": "B Kishore Reddy",
    "position": "Congress Party Youth President",
    "constituency": "Quthbullapur",
    "experience": {...},
    "vision": [...],
    "key_agendas": [...],
    "initiatives": [...],
    "contact": {...}
}

HEALTH_CAMPS_INFO = "Details about health camps..."
VOLUNTEER_INFO = "Volunteer information..."
COMPLAINT_PROCESS = "How to file complaints..."
FAQ = [list of common Q&A]
```

## 🎨 UI Components

### Chat Widget Elements
- **Toggle Button**: Floating orange gradient button
- **Chat Window**: 380px x 550px popup
- **Header**: Shows "BKR Assistant" with robot icon
- **Messages Area**: Scrollable message history
- **Input Area**: Text input with send button
- **Quick Suggestions**: Pre-defined questions for easy start

### Styling Features
- Gradient backgrounds (orange & blue)
- Smooth animations (slide-in, typing indicator)
- User messages: Orange gradient bubbles (right side)
- AI messages: White bubbles with border (left side)
- Responsive design for mobile

## 🧪 Testing

### 1. Install Dependencies
```bash
cd backend
pip install groq==0.4.2
```

### 2. Start Server
```bash
python app.py
```

### 3. Test Chat
1. Open http://localhost:5000
2. Click the floating chat button
3. Try asking:
   - "Who is B Kishore Reddy?"
   - "Tell me about health camps"
   - "How can I volunteer?"
   - "What are his key agendas?"

### 4. Test Off-Topic
Ask: "Who is the president of Russia?"
**Expected**: AI redirects to BKR-related topics

## 🎯 Example Conversations

### Example 1: About Kishore Reddy
```
User: Who is B Kishore Reddy?

AI: B Kishore Reddy is the Congress Party Youth President for 
Quthbullapur Constituency in Telangana. With 18 years of 
political experience, he has served over 50,000 people and 
organized 100+ health camps...

💡 Did you know?
BKR Foundation regularly organizes FREE Health Camps...
```

### Example 2: Health Camps
```
User: Tell me about health camps

AI: BKR Foundation organizes regular FREE health camps across 
Quthbullapur constituency. Recent camps have benefited 500+ 
people. Services include:
- Free medical check-ups
- Blood pressure testing
- Free medicines
...
```

### Example 3: Contact Info
```
User: How can I contact him?

AI: You can contact B Kishore Reddy through:
📞 Phone: +91-9XXXXXX363
📧 Email: ranjith888999@gmail.com
🏢 Office: Quthbullapur Constituency Office
...
```

## ⚙️ Configuration

### Environment Variables (.env)
```env
# Groq API
GROQ_API_KEY=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

# Database (required for chat storage)
DB_HOST=your_host
DB_NAME=bkr_db
DB_USER=your_user
DB_PASSWORD=your_password
```

### AI Parameters
```python
# In ai_service.py
model = "llama-3.1-8b-instant"  # Fast and efficient
temperature = 0.7               # Balanced creativity
max_tokens = 800                # Reasonable length
top_p = 0.9                     # Sampling parameter
```

## 🔒 Security Considerations

### ✅ What's Protected
- API Key stored in .env (not exposed to frontend)
- Chat statistics endpoint protected with API key
- Input validation on all endpoints
- SQL injection prevention with parameterized queries
- XSS protection with content sanitization

### ⚠️ Recommendations for Production
1. **Add Rate Limiting**
   ```python
   from flask_limiter import Limiter
   
   limiter = Limiter(app, key_func=lambda: request.remote_addr)
   
   @app.route('/api/chat/message')
   @limiter.limit("20 per minute")  # Max 20 messages/minute
   def send_chat_message():
       ...
   ```

2. **Add Content Moderation**
   - Filter inappropriate language
   - Block spam messages
   - Detect and prevent abuse

3. **Monitor Usage**
   - Track token usage (costs money!)
   - Alert on unusual patterns
   - Set daily token limits

4. **User Authentication (Optional)**
   - Link conversations to user accounts
   - Provide personalized experiences
   - Better abuse prevention

## 📊 Analytics & Monitoring

### Available Statistics
```
GET /api/chat/stats
{
  "total_conversations": 150,
  "total_messages": 450,
  "avg_messages_per_conversation": 3.0
}
```

### What to Monitor
- Total conversations created
- Messages per day
- Average conversation length
- Token usage (costs)
- Response times
- Error rates
- Most common questions

## 🎓 Customization Guide

### Update Website Data
Edit `backend/website_data.py`:
```python
# Add new information
KISHORE_REDDY_INFO['new_field'] = "New information"

# Update FAQs
FAQ.append({
    "question": "New question?",
    "answer": "New answer"
})
```

### Modify AI Behavior
Edit `backend/ai_service.py`:
```python
# Change temperature (0.0-2.0)
temperature = 0.5  # More focused
temperature = 1.0  # More creative

# Change model
model = "llama-3.1-70b-versatile"  # More powerful

# Adjust context window
chat_history[-20:]  # Include last 20 messages
```

### Customize UI
Edit `css/chatbot.css`:
```css
/* Change colors */
.chat-toggle-btn {
    background: linear-gradient(135deg, #your-color, #another-color);
}

/* Change size */
.chat-window {
    width: 400px;
    height: 600px;
}
```

### Add New Quick Suggestions
Edit `js/chatbot.js`:
```javascript
<button class="chat-suggestion" data-message="Your question here">
    Your question here
</button>
```

## 🐛 Troubleshooting

### Chat Not Appearing?
1. Check console for errors
2. Verify chatbot.css is loaded
3. Verify chatbot.js is loaded
4. Check if `bkrChat` exists in console

### No AI Responses?
1. Check Groq API key is set correctly
2. Verify backend server is running
3. Check browser Network tab for errors
4. Look at backend console for errors

### Database Errors?
1. Ensure tables are created (run app.py once)
2. Check database connection in .env
3. Verify PostgreSQL is running

### Rate Limiting?
Groq free tier limits:
- 30 requests per minute
- 14,400 requests per day
- Contact Groq for higher limits

## 💡 Tips & Best Practices

### For Better AI Responses
1. Keep website_data.py updated
2. Add more FAQs based on real questions
3. Review chat logs to improve responses
4. Fine-tune temperature for your needs

### For Better Performance
1. Use streaming responses for real-time feel
2. Cache common questions
3. Implement lazy loading for chat history
4. Compress API responses

### For Better UX
1. Add "Did this answer help?" feedback
2. Provide quick action buttons
3. Show typing indicator always
4. Add emoji support in messages
5. Enable file attachments for complaints

## 📈 Future Enhancements

### Possible Improvements
- [ ] Voice input/output
- [ ] Multi-language support
- [ ] Image understanding (send photos of issues)
- [ ] Sentiment analysis
- [ ] Auto-escalation to phone call for urgent issues
- [ ] Integration with WhatsApp/Telegram
- [ ] Export chat transcripts
- [ ] Admin dashboard for chat management
- [ ] Automated follow-ups
- [ ] User satisfaction ratings

## 🆘 Support

### Getting Help
- Check EMAIL_IMPLEMENTATION_GUIDE.md for setup help
- Review backend/test_email.py for testing patterns
- Check Groq documentation: https://console.groq.com/docs

### Common Issues
**Issue**: "GROQ_API_KEY not set"
**Fix**: Add key to backend/.env

**Issue**: "Table doesn't exist"
**Fix**: Restart app.py to create tables

**Issue**: "Chat doesn't remember context"
**Fix**: Check session_id is being saved in localStorage

---

**Implementation Date:** January 18, 2026
**AI Model:** Llama 3.1-8B-Instant via Groq
**Status:** ✅ Complete and Ready for Testing
