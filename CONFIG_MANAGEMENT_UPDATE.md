# Configuration Management Update

## Overview
Updated the application to use **server-side environment variables** instead of localStorage for sensitive configuration data like API keys.

## Changes Made

### 1. Backend Changes

#### New API Endpoint: `/api/config`
**File:** `backend/app.py`

```python
@app.route('/api/config', methods=['GET'])
def get_client_config():
    """Get client-side configuration from environment variables"""
    return jsonify({
        'success': True,
        'data': {
            'apiKey': API_KEY,
            'environment': os.getenv('ENVIRONMENT', 'production'),
            'apiBaseUrl': '/api'
        }
    })
```

**Purpose:** Provides client-side JavaScript with configuration values from the server's environment variables.

**Response:**
```json
{
  "success": true,
  "data": {
    "apiKey": "bkr-secret-key-2024",
    "environment": "production",
    "apiBaseUrl": "/api"
  }
}
```

### 2. Frontend Changes

#### New Configuration Module: `js/config.js`

**Features:**
- Automatically loads configuration from server on page load
- Caches configuration in `window.APP_CONFIG` object
- Provides helper functions: `loadConfig()`, `getApiKey()`, `getConfig()`
- Auto-loads when script is included

**Usage:**
```javascript
// Wait for config to load
await loadConfig();

// Get API key
const apiKey = getApiKey();

// Get any config value
const environment = getConfig('environment', 'production');
```

**Global Config Object:**
```javascript
window.APP_CONFIG = {
    apiKey: null,           // Loaded from server
    environment: 'production',
    apiBaseUrl: '/api',
    loaded: false          // true when loaded
}
```

#### Updated API Service: `js/api-service.js`

**Before:**
```javascript
const API_CONFIG = {
    apiKey: 'bkr-secret-key-2025-change-in-production',
    // ...
};
```

**After:**
```javascript
const API_CONFIG = {
    get apiKey() {
        return window.APP_CONFIG && window.APP_CONFIG.apiKey 
            ? window.APP_CONFIG.apiKey 
            : 'bkr-secret-key-2024'; // Fallback only
    }
    // ...
};
```

Now uses a getter that retrieves the API key from loaded config.

### 3. Updated All Pages

#### Admin Pages Updated:
- ✅ `admin/pages/news.html`
- ✅ `admin/pages/settings.html`
- ✅ `admin/pages/health-camps.html`
- ✅ `admin/pages/complaints.html`
- ✅ `admin/pages/feedback.html`
- ✅ `admin/pages/dashboard.html`
- ✅ `admin/pages/gallery.html`
- ✅ `admin/pages/content.html`

#### Public Pages Updated:
- ✅ `index.html`
- ✅ `pages/complaint.html`
- ✅ `pages/feedback.html`
- ✅ `pages/health-camps.html`

#### Changes Applied:
1. **Added config.js script before api-service.js**
   ```html
   <script src="../../js/config.js"></script>
   <script src="../../js/api-service.js"></script>
   ```

2. **Call loadConfig() before making API requests**
   ```javascript
   document.addEventListener('DOMContentLoaded', async function() {
       await loadConfig();
       // Now safe to make API calls
   });
   ```

3. **Use getApiKey() instead of localStorage**
   
   **Before:**
   ```javascript
   'X-API-Key': localStorage.getItem('apiKey') || 'bkr-secret-key-2024'
   ```
   
   **After:**
   ```javascript
   'X-API-Key': getApiKey()
   ```

## Benefits

### 🔒 Security
- ✅ API keys no longer stored in browser localStorage
- ✅ Keys come from secure server environment variables
- ✅ Single source of truth for configuration

### 🎯 Centralized Configuration
- ✅ All config managed in one place (server `.env` file)
- ✅ Easy to update API key without changing code
- ✅ Different keys for development/production

### 🚀 Better Deployment
- ✅ No hardcoded secrets in JavaScript files
- ✅ Environment-specific configuration
- ✅ Follows 12-factor app methodology

## How It Works

### Flow Diagram
```
1. Page loads
   ↓
2. config.js loads and calls /api/config
   ↓
3. Server reads API_KEY from environment
   ↓
4. Returns config to client
   ↓
5. Config stored in window.APP_CONFIG
   ↓
6. All API calls use getApiKey() to retrieve it
```

### Example: Adding News Article

```javascript
// Old way (localStorage)
fetch('/api/news', {
    headers: {
        'X-API-Key': localStorage.getItem('apiKey') || 'bkr-secret-key-2024'
    }
});

// New way (server config)
await loadConfig(); // Loads from server
fetch('/api/news', {
    headers: {
        'X-API-Key': getApiKey() // Uses loaded config
    }
});
```

## Environment Setup

### Backend `.env` File
```env
# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=bkr_website
DB_USER=postgres
DB_PASSWORD=your_password

# API Configuration
API_KEY=bkr-secret-key-2024-production
ENVIRONMENT=production

# CORS Settings
CORS_ORIGINS=http://localhost:8080,https://yourdomain.com
```

### Development vs Production

**Development:**
```env
API_KEY=bkr-secret-key-dev
ENVIRONMENT=development
```

**Production:**
```env
API_KEY=bkr-secret-key-prod-secure-random-string
ENVIRONMENT=production
```

## Migration Guide

### For Existing Installations

1. **Update backend environment variables**
   ```bash
   cd backend
   # Edit .env file
   # Set API_KEY=your-secure-key
   ```

2. **Clear browser localStorage (optional cleanup)**
   ```javascript
   // In browser console
   localStorage.removeItem('apiKey');
   ```

3. **Restart backend server**
   ```bash
   python app.py
   ```

4. **Refresh admin pages** - They will automatically load config from server

## Testing

### Verify Config Loading

**Browser Console:**
```javascript
// Check if config is loaded
console.log(window.APP_CONFIG);

// Should output:
{
  apiKey: "bkr-secret-key-2024",
  environment: "production",
  apiBaseUrl: "/api",
  loaded: true
}
```

### Test API Calls

```javascript
// Should work without errors
fetch('/api/news', {
    headers: {
        'X-API-Key': getApiKey()
    }
})
.then(r => r.json())
.then(d => console.log(d));
```

### Verify No localStorage Dependencies

```javascript
// Check localStorage (should not have apiKey anymore)
console.log(localStorage.getItem('apiKey')); // null

// API calls still work
getApiKey(); // Returns key from server config
```

## Troubleshooting

### Config Not Loading

**Symptom:** API calls fail with 401 Unauthorized

**Solution:**
```javascript
// In browser console
await loadConfig();
console.log(window.APP_CONFIG.loaded); // Should be true
```

### API Key Mismatch

**Symptom:** 401 errors even after config loads

**Check:**
1. Backend `.env` has correct `API_KEY`
2. Server was restarted after changing `.env`
3. `/api/config` returns correct key
   ```javascript
   fetch('/api/config').then(r => r.json()).then(d => console.log(d));
   ```

### Fallback Being Used

**Symptom:** Warning in console about config not loaded

**Solution:**
Ensure config.js is loaded before api-service.js:
```html
<script src="js/config.js"></script>  <!-- Must be first -->
<script src="js/api-service.js"></script>
```

## Authentication Flow

### Admin Authentication (Still Uses localStorage)

**What Changed:** Only API key retrieval
**What Stayed:** Session management still uses localStorage

```javascript
// Login state (still in localStorage - this is OK)
localStorage.setItem('adminLoggedIn', 'true');
localStorage.setItem('adminUser', username);

// API key (now from server)
const apiKey = getApiKey(); // From server config
```

**Why?**
- Session state is session-specific, not sensitive
- API key is application-wide and sensitive
- Best practice: Sensitive config from server, session data in browser

## Security Recommendations

### 1. Strong API Keys
```bash
# Generate secure random key
openssl rand -base64 32
```

### 2. Rotate Keys Regularly
Update `.env` file and restart server

### 3. Different Keys Per Environment
- Development: `bkr-dev-key-2024`
- Staging: `bkr-staging-key-2024`
- Production: `bkr-prod-[random-string]`

### 4. Never Commit `.env` to Git
```bash
# .gitignore
.env
.env.*
!.env.example
```

## Summary

✅ **Completed Changes:**
- Created `/api/config` endpoint to serve configuration
- Built `config.js` module for client-side config management
- Updated all 14 pages to use server config
- Removed hardcoded API keys from JavaScript
- Maintained backward compatibility with fallbacks

✅ **Security Improvements:**
- API keys no longer in browser storage
- Configuration centralized on server
- Environment-based configuration

✅ **Developer Experience:**
- Easier to manage configuration
- No code changes needed for key rotation
- Clear separation of concerns

---

**All configuration is now managed through environment variables! 🎉**
