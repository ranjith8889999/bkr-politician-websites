"""
Flask API Server for BKR Politician Website
Provides REST API endpoints for dynamic content management
Also serves static frontend files
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from functools import wraps
import os
from dotenv import load_dotenv
from database import Database

# Load environment variables
load_dotenv()

# Initialize Flask app with static file serving
# Set static folder to parent directory to serve all frontend files
app = Flask(__name__, 
            static_folder='../',  # Parent directory contains index.html, css, js, etc.
            static_url_path='')

# Configure CORS - allow requests from frontend
# Get allowed origins from environment variable or use defaults
cors_origins = os.getenv('CORS_ORIGINS', 'http://localhost:8080,http://127.0.0.1:8080').split(',')

CORS(app, resources={
    r"/api/*": {
        "origins": cors_origins if cors_origins != ['*'] else "*",
        "methods": ["GET", "POST", "PUT", "DELETE", "PATCH"],
        "allow_headers": ["Content-Type", "X-API-Key"]
    }
})

# Initialize Database with PostgreSQL connection
# Connection parameters from environment variables or defaults
DB_HOST = os.getenv('DB_HOST', '72.60.101.93')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'bkr_db')
DB_USER = os.getenv('DB_USER', 'ranjith')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'ranjith123')

db = Database(
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD
)

# Get API Key from environment
API_KEY = os.getenv('API_KEY', 'bkr-secret-key-2025-change-in-production')

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
