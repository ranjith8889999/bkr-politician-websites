"""
Handles image uploads for news articles
"""

import os
import uuid
from werkzeug.utils import secure_filename
from datetime import datetime

# Configure upload settings
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'images', 'news')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

# Create upload folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_file_extension(filename):
    """Get file extension"""
    return filename.rsplit('.', 1)[1].lower() if '.' in filename else ''

def generate_unique_filename(original_filename):
    """Generate unique filename using UUID"""
    ext = get_file_extension(original_filename)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    unique_id = str(uuid.uuid4())[:8]
    return f"news_{timestamp}_{unique_id}.{ext}"

def save_upload(file):
    """
    Save uploaded file and return the URL
    
    Args:
        file: FileStorage object from Flask request
        
    Returns:
        dict: {'success': bool, 'url': str, 'error': str}
    """
    try:
        # Check if file exists
        if not file:
            return {'success': False, 'error': 'No file provided'}
        
        # Check if filename is valid
        if file.filename == '':
            return {'success': False, 'error': 'No file selected'}
        
        # Check file type
        if not allowed_file(file.filename):
            return {
                'success': False, 
                'error': f'Invalid file type. Allowed: {", ".join(ALLOWED_EXTENSIONS)}'
            }
        
        # Check file size (this should be done before, but as backup)
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)
        
        if file_size > MAX_FILE_SIZE:
            return {
                'success': False, 
                'error': f'File too large. Maximum size: {MAX_FILE_SIZE / 1024 / 1024}MB'
            }
        
        # Generate unique filename
        filename = generate_unique_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        
        # Save file
        file.save(filepath)
        
        # Return relative URL path (without leading slash for compatibility)
        url = f'images/news/{filename}'
        
        return {
            'success': True,
            'url': url,
            'filename': filename,
            'size': file_size
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': f'Upload failed: {str(e)}'
        }

def delete_upload(filename):
    """
    Delete uploaded file
    
    Args:
        filename: Name of file to delete
        
    Returns:
        bool: True if deleted, False otherwise
    """
    try:
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        if os.path.exists(filepath):
            os.remove(filepath)
            return True
        return False
    except Exception as e:
        print(f"Error deleting file: {e}")
        return False
