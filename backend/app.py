"""
Flask API Server for BKR Politician Website
Provides REST API endpoints for dynamic content management
Also serves static frontend files
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from functools import wraps
import os
import uuid
from dotenv import load_dotenv
from database import Database
from email_service import EmailService
from ai_service import AIService
from upload_handler import save_upload, allowed_file

# Load environment variables
load_dotenv()

# Initialize Flask app with static file serving
# Set static folder to parent directory to serve all frontend files
app = Flask(__name__, 
            static_folder='../',  # Parent directory contains index.html, css, js, etc.
            static_url_path='')

# Configure CORS - allow requests from frontend
# Get allowed origins from environment variable or use defaults
cors_origins = os.getenv('CORS_ORIGINS', 'http://localhost:8080,http://127.0.0.1:8080,https://affiliate-bkr.nwp2mw.easypanel.host').split(',')

CORS(app, resources={
    r"/api/*": {
        "origins": cors_origins if cors_origins != ['*'] else "*",
        "methods": ["GET", "POST", "PUT", "DELETE", "PATCH"],
        "allow_headers": ["Content-Type", "X-API-Key"],
        "supports_credentials": True
    }
})

# Initialize Database with PostgreSQL connection
# Connection parameters from environment variables (REQUIRED)
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')

if not all([DB_HOST, DB_NAME, DB_USER, DB_PASSWORD]):
    raise ValueError('Database credentials must be set in environment variables')

db = Database(
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD
)

# Initialize Email Service
email_service = EmailService()

# Initialize AI Service with database instance
ai_service = AIService(db)

# Get API Key from environment (REQUIRED)
API_KEY = os.getenv('API_KEY')
if not API_KEY:
    raise ValueError('API_KEY must be set in environment variables')

# ==================== STATIC FILE ROUTES ====================

@app.route('/')
def serve_index():
    """Serve the homepage"""
    return send_from_directory('..', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    """Serve static files (HTML, CSS, JS, images)"""
    # Don't serve API routes as static files
    if path.startswith('api/'):
        return jsonify({'error': 'Not found'}), 404
    
    try:
        return send_from_directory('..', path)
    except:
        # If file not found, return 404 page or redirect to home
        return send_from_directory('..', 'index.html')

# ==================== MIDDLEWARE ====================

def require_api_key(f):
    """Decorator to require API key for protected endpoints"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        
        if not api_key or api_key != API_KEY:
            return jsonify({
                'success': False,
                'error': 'Invalid or missing API key'
            }), 401
        
        return f(*args, **kwargs)
    return decorated_function

# ==================== HEALTH ENDPOINTS ====================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'success': True,
        'message': 'BKR API Server is running',
        'version': '1.0.0'
    })

# ==================== HEALTH CAMPS ENDPOINTS ====================

@app.route('/api/health-camps', methods=['GET'])
def get_health_camps():
    """Get all health camps or filter by status/upcoming"""
    try:
        status = request.args.get('status')
        limit = request.args.get('limit', type=int)
        upcoming = request.args.get('upcoming', type=str)
        
        # Convert 'true'/'false' string to boolean
        upcoming_bool = upcoming.lower() == 'true' if upcoming else None
        
        camps = db.get_health_camps(status=status, limit=limit, upcoming=upcoming_bool)
        
        return jsonify({
            'success': True,
            'data': camps,
            'count': len(camps)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/health-camps/<int:camp_id>', methods=['GET'])
def get_health_camp(camp_id):
    """Get a single health camp by ID"""
    try:
        camp = db.get_health_camp_by_id(camp_id)
        
        if not camp:
            return jsonify({
                'success': False,
                'error': 'Health camp not found'
            }), 404
        
        return jsonify({
            'success': True,
            'data': camp
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/health-camps', methods=['POST'])
@require_api_key
def create_health_camp():
    """Create a new health camp (Protected)"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['title', 'date', 'time', 'location']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400
        
        camp_id = db.create_health_camp(data)
        
        return jsonify({
            'success': True,
            'message': 'Health camp created successfully',
            'data': {'id': camp_id}
        }), 201
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/health-camps/<int:camp_id>', methods=['PUT'])
@require_api_key
def update_health_camp(camp_id):
    """Update an existing health camp (Protected)"""
    try:
        data = request.get_json()
        
        success = db.update_health_camp(camp_id, data)
        
        if not success:
            return jsonify({
                'success': False,
                'error': 'Health camp not found'
            }), 404
        
        return jsonify({
            'success': True,
            'message': 'Health camp updated successfully'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/health-camps/<int:camp_id>', methods=['DELETE'])
@require_api_key
def delete_health_camp(camp_id):
    """Delete a health camp (Protected)"""
    try:
        success = db.delete_health_camp(camp_id)
        
        if not success:
            return jsonify({
                'success': False,
                'error': 'Health camp not found'
            }), 404
        
        return jsonify({
            'success': True,
            'message': 'Health camp deleted successfully'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ==================== COMPLAINTS ENDPOINTS ====================

@app.route('/api/complaints', methods=['GET'])
@require_api_key
def get_complaints():
    """Get all complaints (Protected)"""
    try:
        status = request.args.get('status')
        limit = request.args.get('limit', type=int)
        
        complaints = db.get_complaints(status=status, limit=limit)
        
        return jsonify({
            'success': True,
            'data': complaints,
            'count': len(complaints)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/complaints', methods=['POST'])
def create_complaint():
    """Create a new complaint (Public)"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'phone', 'category', 'subject', 'message']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400
        
        complaint_id = db.create_complaint(data)
        
        return jsonify({
            'success': True,
            'message': 'Complaint submitted successfully',
            'data': {'id': complaint_id}
        }), 201
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/complaints/<int:complaint_id>/status', methods=['PATCH'])
@require_api_key
def update_complaint_status(complaint_id):
    """Update complaint status (Protected)"""
    try:
        data = request.get_json()
        status = data.get('status')
        
        if not status:
            return jsonify({
                'success': False,
                'error': 'Status is required'
            }), 400
        
        success = db.update_complaint_status(complaint_id, status)
        
        if not success:
            return jsonify({
                'success': False,
                'error': 'Complaint not found'
            }), 404
        
        return jsonify({
            'success': True,
            'message': 'Complaint status updated successfully'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ==================== FEEDBACK ENDPOINTS ====================

@app.route('/api/feedback', methods=['GET'])
@require_api_key
def get_feedback():
    """Get all feedback (Protected)"""
    try:
        limit = request.args.get('limit', type=int)
        
        feedback = db.get_feedback(limit=limit)
        
        return jsonify({
            'success': True,
            'data': feedback,
            'count': len(feedback)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/feedback', methods=['POST'])
def create_feedback():
    """Create new feedback (Public)"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'phone', 'rating', 'message']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400
        
        # Validate rating range
        rating = int(data.get('rating'))
        if rating < 1 or rating > 5:
            return jsonify({
                'success': False,
                'error': 'Rating must be between 1 and 5'
            }), 400
        
        feedback_id = db.create_feedback(data)
        
        return jsonify({
            'success': True,
            'message': 'Feedback submitted successfully',
            'data': {'id': feedback_id}
        }), 201
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ==================== NEWS ENDPOINTS ====================

@app.route('/api/news', methods=['GET'])
def get_news():
    """Get all news articles"""
    try:
        status = request.args.get('status', 'published')
        limit = request.args.get('limit', type=int)
        
        news = db.get_news(status=status, limit=limit)
        
        return jsonify({
            'success': True,
            'data': news,
            'count': len(news)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/news/<int:news_id>', methods=['GET'])
def get_news_by_id(news_id):
    """Get a single news article by ID"""
    try:
        news = db.get_news_by_id(news_id)
        
        if not news:
            return jsonify({
                'success': False,
                'error': 'News article not found'
            }), 404
        
        return jsonify({
            'success': True,
            'data': news
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/news', methods=['POST'])
@require_api_key
def create_news():
    """Create a new news article (Protected)"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['title', 'category', 'content']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400
        
        news_id = db.create_news(data)
        
        return jsonify({
            'success': True,
            'message': 'News article created successfully',
            'data': {'id': news_id}
        }), 201
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/news/<int:news_id>', methods=['PUT'])
@require_api_key
def update_news(news_id):
    """Update an existing news article (Protected)"""
    try:
        data = request.get_json()
        
        success = db.update_news(news_id, data)
        
        if not success:
            return jsonify({
                'success': False,
                'error': 'News article not found'
            }), 404
        
        return jsonify({
            'success': True,
            'message': 'News article updated successfully'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/news/<int:news_id>', methods=['DELETE'])
@require_api_key
def delete_news(news_id):
    """Delete a news article (Protected)"""
    try:
        success = db.delete_news(news_id)
        
        if not success:
            return jsonify({
                'success': False,
                'error': 'News article not found'
            }), 404
        
        return jsonify({
            'success': True,
            'message': 'News article deleted successfully'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ==================== SETTINGS ENDPOINTS ====================

@app.route('/api/upload', methods=['POST'])
@require_api_key
def upload_file():
    """Upload an image file (Protected)"""
    try:
        # Check if file is in request
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No file provided'
            }), 400
        
        file = request.files['file']
        
        # Validate file
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No file selected'
            }), 400
        
        if not allowed_file(file.filename):
            return jsonify({
                'success': False,
                'error': 'Invalid file type. Allowed: png, jpg, jpeg, gif, webp'
            }), 400
        
        # Save file
        result = save_upload(file)
        
        if result['success']:
            return jsonify({
                'success': True,
                'url': result['url'],
                'filename': result['filename'],
                'message': 'File uploaded successfully'
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': result['error']
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/config', methods=['GET'])
def get_client_config():
    """Get client-side configuration from environment variables"""
    try:
        return jsonify({
            'success': True,
            'data': {
                'apiKey': API_KEY,
                'environment': os.getenv('ENVIRONMENT', 'production'),
                'apiBaseUrl': '/api'
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/settings', methods=['GET'])
def get_settings():
    """Get all settings"""
    try:
        settings = db.get_settings()
        
        # Convert to dictionary format
        settings_dict = {s['setting_key']: s['setting_value'] for s in settings}
        
        return jsonify({
            'success': True,
            'data': settings_dict
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/settings/<key>', methods=['GET'])
def get_setting(key):
    """Get a specific setting"""
    try:
        value = db.get_setting(key)
        
        if value is None:
            return jsonify({
                'success': False,
                'error': 'Setting not found'
            }), 404
        
        return jsonify({
            'success': True,
            'data': {key: value}
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/settings', methods=['PUT'])
@require_api_key
def update_settings():
    """Update multiple settings (Protected)"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No settings provided'
            }), 400
        
        # Update each setting
        for key, value in data.items():
            db.update_setting(key, str(value))
        
        return jsonify({
            'success': True,
            'message': 'Settings updated successfully'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/settings/<key>', methods=['PUT'])
@require_api_key
def update_setting(key):
    """Update a specific setting (Protected)"""
    try:
        data = request.get_json()
        value = data.get('value')
        
        if value is None:
            return jsonify({
                'success': False,
                'error': 'Value is required'
            }), 400
        
        db.update_setting(key, str(value))
        
        return jsonify({
            'success': True,
            'message': f'Setting {key} updated successfully'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ==================== DASHBOARD ENDPOINTS ====================

@app.route('/api/dashboard/stats', methods=['GET'])
@require_api_key
def get_dashboard_stats():
    """Get dashboard statistics (Protected)"""
    try:
        stats = db.get_dashboard_stats()
        
        return jsonify({
            'success': True,
            'data': stats
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ==================== EMAIL ENDPOINTS ====================

@app.route('/api/email/complaint', methods=['POST'])
def send_complaint():
    """Send complaint email to helpdesk"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'phone', 'subject', 'message', 'category', 'area']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400
        
        # Send email
        success, message = email_service.send_complaint_email(data)
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Complaint submitted successfully. We will respond within 48 hours.'
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': message
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/email/volunteer', methods=['POST'])
def send_volunteer():
    """Send volunteer registration email"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'phone', 'email', 'area']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400
        
        # Send email
        success, message = email_service.send_volunteer_email(data)
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Thank you for registering! We will contact you soon.'
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': message
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/email/contact', methods=['POST'])
def send_contact():
    """Send contact/get-in-touch email"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'email', 'subject', 'message']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400
        
        # Send email
        success, message = email_service.send_contact_email(data)
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Message sent successfully. We will get back to you soon.'
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': message
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/email/feedback', methods=['POST'])
def send_feedback():
    """Send feedback email"""
    try:
        data = request.get_json()
        
        # Validate required fields - rating and category are required
        required_fields = ['rating', 'category']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400
        
        # Send email
        success, message = email_service.send_feedback_email(data)
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Thank you for your feedback! We appreciate your input.'
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': message
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ==================== CHAT AI ENDPOINTS ====================

@app.route('/api/chat/session', methods=['POST'])
def create_chat_session():
    """Create a new chat session"""
    try:
        # Get user info for session tracking
        user_data = {
            'ip': request.remote_addr,
            'user_agent': request.headers.get('User-Agent', '')
        }
        
        # Create session with UUID
        session_id = str(uuid.uuid4())
        
        # Save to database
        db.create_chat_session({'session_id': session_id, **user_data})
        
        return jsonify({
            'success': True,
            'session_id': session_id
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/chat/message', methods=['POST'])
def send_chat_message():
    """Send a message and get AI response"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data.get('message'):
            return jsonify({
                'success': False,
                'error': 'Message is required'
            }), 400
        
        session_id = data.get('session_id')
        user_message = data.get('message')
        
        # Create new session if not provided
        if not session_id:
            session_id = str(uuid.uuid4())
            user_data = {
                'ip': request.remote_addr,
                'user_agent': request.headers.get('User-Agent', ''),
                'session_id': session_id
            }
            db.create_chat_session(user_data)
        
        # Get chat history for context
        chat_history = db.get_chat_history(session_id, limit=10)
        
        # Format history for AI
        formatted_history = [
            {'role': msg['role'], 'content': msg['content']}
            for msg in chat_history
        ]
        
        # Save user message to database
        db.save_chat_message(session_id, 'user', user_message)
        
        # Get AI response
        ai_response = ai_service.chat(
            user_message=user_message,
            chat_history=formatted_history,
            session_id=session_id
        )
        
        if ai_response['success']:
            # Save AI response to database
            db.save_chat_message(
                session_id,
                'assistant',
                ai_response['message'],
                tokens_used=ai_response.get('usage', {}).get('total_tokens')
            )
            
            return jsonify({
                'success': True,
                'session_id': session_id,
                'message': ai_response['message'],
                'model': ai_response.get('model')
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': ai_response.get('error'),
                'message': ai_response.get('message')
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/chat/history/<session_id>', methods=['GET'])
def get_chat_history_endpoint(session_id):
    """Get chat history for a session"""
    try:
        limit = request.args.get('limit', 50, type=int)
        history = db.get_chat_history(session_id, limit=limit)
        
        return jsonify({
            'success': True,
            'history': history,
            'count': len(history)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/chat/stats', methods=['GET'])
@require_api_key
def get_chat_stats():
    """Get chat statistics (Protected)"""
    try:
        stats = db.get_chat_stats()
        
        return jsonify({
            'success': True,
            'data': stats
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500

# ==================== MAIN ====================

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 BKR API Server Starting...")
    print("=" * 60)
    print(f"�️  PostgreSQL Database: {DB_HOST}:{DB_PORT}/{DB_NAME}")
    print(f"👤 Database User: {DB_USER}")
    print(f"🔑 API Key: {API_KEY[:10]}...")
    print(f"🌐 Server: http://localhost:5000")
    print(f"📡 Health Check: http://localhost:5000/api/health")
    print(f"🌍 Static Files: Serving from parent directory")
    print("=" * 60)
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        use_reloader=False  # Disable reloader to prevent crashes
    )
