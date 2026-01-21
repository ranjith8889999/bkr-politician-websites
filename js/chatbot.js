/* =============================================
   AI CHATBOT FUNCTIONALITY
   ============================================= */

class AIChat {
    constructor() {
        this.sessionId = null;
        this.messages = [];
        this.isTyping = false;
        this.init();
    }
    
    init() {
        // Create chat widget HTML
        this.createChatWidget();
        
        // Attach event listeners
        this.attachEventListeners();
        
        // Load existing session from localStorage
        this.loadSession();
    }
    
    createChatWidget() {
        const chatHTML = `
            <div class="chat-widget" id="chatWidget">
                <button class="chat-toggle-btn" id="chatToggleBtn">
                    <i class="fas fa-comments"></i>
                    <span class="chat-notification-dot"></span>
                </button>
                
                <div class="chat-window" id="chatWindow">
                    <div class="chat-header">
                        <div class="chat-header-info">
                            <div class="chat-avatar">
                                <i class="fas fa-robot"></i>
                            </div>
                            <div class="chat-header-text">
                                <h3>BKR Assistant</h3>
                                <p>Ask me about B Kishore Reddy</p>
                            </div>
                        </div>
                        <button class="chat-close-btn" id="chatCloseBtn">
                            <i class="fas fa-times"></i>
                        </button>
                    </div>
                    
                    <div class="chat-messages" id="chatMessages">
                        <div class="chat-welcome">
                            <h4>👋 Welcome!</h4>
                            <p>I'm here to help you learn about B Kishore Reddy and BKR Foundation. Ask me anything!</p>
                            <div class="chat-suggestions">
                                <button class="chat-suggestion" data-message="Who is B Kishore Reddy?">
                                    Who is B Kishore Reddy?
                                </button>
                                <button class="chat-suggestion" data-message="Tell me about health camps">
                                    Tell me about health camps
                                </button>
                                <button class="chat-suggestion" data-message="How can I volunteer?">
                                    How can I volunteer?
                                </button>
                                <button class="chat-suggestion" data-message="What are his key agendas?">
                                    What are his key agendas?
                                </button>
                            </div>
                        </div>
                    </div>
                    
                    <div class="chat-input-area">
                        <input 
                            type="text" 
                            class="chat-input" 
                            id="chatInput" 
                            placeholder="Type your message..."
                            autocomplete="off"
                        />
                        <button class="chat-send-btn" id="chatSendBtn">
                            <i class="fas fa-paper-plane"></i>
                        </button>
                    </div>
                </div>
            </div>
        `;
        
        // Append to body
        document.body.insertAdjacentHTML('beforeend', chatHTML);
    }
    
    attachEventListeners() {
        const toggleBtn = document.getElementById('chatToggleBtn');
        const closeBtn = document.getElementById('chatCloseBtn');
        const sendBtn = document.getElementById('chatSendBtn');
        const input = document.getElementById('chatInput');
        
        toggleBtn?.addEventListener('click', () => this.toggleChat());
        closeBtn?.addEventListener('click', () => this.closeChat());
        sendBtn?.addEventListener('click', () => this.sendMessage());
        
        input?.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !this.isTyping) {
                this.sendMessage();
            }
        });
        
        // Suggestion buttons
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('chat-suggestion')) {
                const message = e.target.dataset.message;
                this.sendPredefinedMessage(message);
            }
        });
    }
    
    toggleChat() {
        const chatWindow = document.getElementById('chatWindow');
        const toggleBtn = document.getElementById('chatToggleBtn');
        
        chatWindow.classList.toggle('active');
        toggleBtn.classList.toggle('active');
        
        if (chatWindow.classList.contains('active')) {
            document.getElementById('chatInput')?.focus();
        }
    }
    
    closeChat() {
        const chatWindow = document.getElementById('chatWindow');
        const toggleBtn = document.getElementById('chatToggleBtn');
        
        chatWindow.classList.remove('active');
        toggleBtn.classList.remove('active');
    }
    
    loadSession() {
        // Try to load existing session from localStorage
        const savedSessionId = localStorage.getItem('bkr_chat_session');
        if (savedSessionId) {
            this.sessionId = savedSessionId;
            this.loadChatHistory();
        }
    }
    
    async loadChatHistory() {
        if (!this.sessionId) return;
        
        try {
            const response = await fetch(`/api/chat/history/${this.sessionId}`);
            const data = await response.json();
            
            if (data.success && data.history.length > 0) {
                // Clear welcome message
                const messagesContainer = document.getElementById('chatMessages');
                messagesContainer.innerHTML = '';
                
                // Display history
                data.history.forEach(msg => {
                    this.displayMessage(msg.content, msg.role === 'user' ? 'user' : 'ai', false);
                });
                
                this.scrollToBottom();
            }
        } catch (error) {
            console.error('Error loading chat history:', error);
        }
    }
    
    async sendMessage() {
        const input = document.getElementById('chatInput');
        const message = input.value.trim();
        
        if (!message || this.isTyping) return;
        
        // Display user message
        this.displayMessage(message, 'user');
        input.value = '';
        
        // Show typing indicator
        this.showTypingIndicator();
        
        try {
            const response = await fetch('/api/chat/message', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    message: message,
                    session_id: this.sessionId
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                // Save session ID
                if (data.session_id && !this.sessionId) {
                    this.sessionId = data.session_id;
                    localStorage.setItem('bkr_chat_session', this.sessionId);
                }
                
                // Remove typing indicator and show response
                this.hideTypingIndicator();
                this.displayMessage(data.message, 'ai');
            } else {
                this.hideTypingIndicator();
                this.displayError(data.message || 'Sorry, something went wrong. Please try again.');
            }
        } catch (error) {
            console.error('Chat error:', error);
            this.hideTypingIndicator();
            this.displayError('Failed to connect to chat service. Please try again.');
        }
    }
    
    sendPredefinedMessage(message) {
        const input = document.getElementById('chatInput');
        input.value = message;
        this.sendMessage();
    }
    
    displayMessage(content, type, animate = true) {
        const messagesContainer = document.getElementById('chatMessages');
        
        // Remove welcome message if exists
        const welcome = messagesContainer.querySelector('.chat-welcome');
        if (welcome) {
            welcome.remove();
        }
        
        const messageDiv = document.createElement('div');
        messageDiv.className = `chat-message ${type}`;
        if (animate) {
            messageDiv.style.animation = 'slideIn 0.3s ease';
        }
        
        const avatar = type === 'ai' ? '<i class="fas fa-robot"></i>' : '<i class="fas fa-user"></i>';
        const time = new Date().toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
        
        // Format message content (support line breaks and basic markdown)
        const formattedContent = this.formatMessage(content);
        
        messageDiv.innerHTML = `
            <div class="chat-message-avatar">
                ${avatar}
            </div>
            <div>
                <div class="chat-message-content">
                    ${formattedContent}
                </div>
                <div class="chat-message-time">${time}</div>
            </div>
        `;
        
        messagesContainer.appendChild(messageDiv);
        this.scrollToBottom();
    }
    
    formatMessage(content) {
        // Convert line breaks to <br>
        let formatted = content.replace(/\n/g, '<br>');
        
        // Bold text: **text** or __text__
        formatted = formatted.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        formatted = formatted.replace(/__(.*?)__/g, '<strong>$1</strong>');
        
        // Italic text: *text* or _text_
        formatted = formatted.replace(/\*(.*?)\*/g, '<em>$1</em>');
        formatted = formatted.replace(/_(.*?)_/g, '<em>$1</em>');
        
        // Links: [text](url)
        formatted = formatted.replace(/\[(.*?)\]\((.*?)\)/g, '<a href="$2" target="_blank">$1</a>');
        
        return formatted;
    }
    
    showTypingIndicator() {
        this.isTyping = true;
        const messagesContainer = document.getElementById('chatMessages');
        
        const typingDiv = document.createElement('div');
        typingDiv.className = 'chat-message ai';
        typingDiv.id = 'typingIndicator';
        typingDiv.innerHTML = `
            <div class="chat-message-avatar">
                <i class="fas fa-robot"></i>
            </div>
            <div class="chat-typing">
                <span></span>
                <span></span>
                <span></span>
            </div>
        `;
        
        messagesContainer.appendChild(typingDiv);
        this.scrollToBottom();
    }
    
    hideTypingIndicator() {
        this.isTyping = false;
        const typingIndicator = document.getElementById('typingIndicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }
    
    displayError(message) {
        const messagesContainer = document.getElementById('chatMessages');
        
        const errorDiv = document.createElement('div');
        errorDiv.className = 'chat-error';
        errorDiv.innerHTML = `<i class="fas fa-exclamation-triangle"></i> ${message}`;
        
        messagesContainer.appendChild(errorDiv);
        this.scrollToBottom();
    }
    
    scrollToBottom() {
        const messagesContainer = document.getElementById('chatMessages');
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
    
    clearChat() {
        this.sessionId = null;
        this.messages = [];
        localStorage.removeItem('bkr_chat_session');
        
        const messagesContainer = document.getElementById('chatMessages');
        messagesContainer.innerHTML = `
            <div class="chat-welcome">
                <h4>👋 Welcome!</h4>
                <p>I'm here to help you learn about B Kishore Reddy and BKR Foundation. Ask me anything!</p>
            </div>
        `;
    }
}

// Initialize chatbot when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Only initialize if we're not on admin pages
    if (!window.location.pathname.includes('/admin/')) {
        window.bkrChat = new AIChat();
        console.log('✅ BKR AI Chatbot initialized');
    }
});
