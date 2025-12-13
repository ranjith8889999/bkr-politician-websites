# Single Deployment Solution - Flask Serves Everything

## ✅ UPDATED: Single Deployment Architecture

```
┌─────────────────────────────────────────────────────┐
│  Single EasyPanel App (Python/Flask)                │
│  https://affiliate-bkr.nwp2mw.easypanel.host       │
│                                                      │
│  Flask serves BOTH:                                 │
│  ├── / → index.html, pages/, css/, js/, images/   │
│  └── /api/* → REST API endpoints                   │
└─────────────────────────────────────────────────────┘
```

---

## 🚀 Deployment Steps:

### Step 1: Push Updated Code to GitHub

```bash
git add .
git commit -m "Single deployment: Flask serves frontend and API"
git push origin feature/added_db
```

### Step 2: Configure EasyPanel App

**App Settings:**
```
Name: affiliate-bkr (or your current app name)
Type: Python
Source: GitHub (bkr-politician-websites)
Branch: feature/added_db
Root Directory: /          ← Root of repo (NOT backend)
```

**Build Command:**
```bash
cd backend && pip install -r requirements.txt
```

**Start Command:**
```bash
cd backend && gunicorn wsgi:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120
```

**OR use the start script:**
```bash
cd backend && bash start.sh
```

**Environment Variables:**
```
API_KEY=bkr-secret-key-2025-change-in-production
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123
DATABASE_PATH=bkr_database.db
FLASK_ENV=production
FLASK_DEBUG=False
CORS_ORIGINS=*
PORT=5000
```

### Step 3: Initialize Database After Deployment

Open the terminal in EasyPanel and run:
```bash
cd backend
python migrate_data.py --sample
```

### Step 4: Test Everything

**Frontend (HTML pages):**
- https://affiliate-bkr.nwp2mw.easypanel.host/
- https://affiliate-bkr.nwp2mw.easypanel.host/pages/health-camps.html
- https://affiliate-bkr.nwp2mw.easypanel.host/admin/pages/login.html

**API Endpoints:**
```bash
curl https://affiliate-bkr.nwp2mw.easypanel.host/api/health
curl https://affiliate-bkr.nwp2mw.easypanel.host/api/health-camps
```

---

## 📝 What Changed:

### 1. **backend/app.py** - Now serves static files
```python
app = Flask(__name__, 
            static_folder='../',  # Parent directory
            static_url_path='')

@app.route('/')
def serve_index():
    return send_from_directory('..', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    if path.startswith('api/'):
        return jsonify({'error': 'Not found'}), 404
    return send_from_directory('..', path)
```

### 2. **js/api-service.js** - Uses relative URLs in production
```javascript
const API_CONFIG = {
    baseURL: isLocalhost 
        ? 'http://localhost:5000/api' 
        : '/api',  // Relative URL - same server
    ...
};
```

### 3. **backend/Procfile** - Runs from backend directory
```
web: cd backend && gunicorn wsgi:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120
```

---

## 🔍 How It Works:

1. **Flask app starts** and serves static files from parent directory
2. **API routes** (`/api/*`) are handled by Flask routes
3. **All other requests** (`/`, `/pages/`, `/css/`, etc.) serve static files
4. **Frontend JavaScript** uses `/api` (relative URL) in production
5. **Single server, single deployment, single URL**

---

## ✅ Advantages:

- ✓ **One deployment** instead of two
- ✓ **No CORS issues** (same origin)
- ✓ **Simpler configuration**
- ✓ **Easy local testing** (still works with localhost:5000)

---

## 🆘 Troubleshooting:

**If images/CSS don't load:**
Check browser console for 404s on static files.

**If API returns 404:**
```bash
# Check if Flask is running
curl https://affiliate-bkr.nwp2mw.easypanel.host/api/health

# Check EasyPanel logs for Python errors
```

**If database errors:**
```bash
# Initialize database in EasyPanel terminal
cd backend
python migrate_data.py --sample
```

---

## 🎯 Expected Logs (Good):

```
[INFO] Booting worker with pid: 123
[INFO] Listening at: http://0.0.0.0:5000
GET / 200 OK
GET /api/health-camps 200 OK
GET /css/style.css 200 OK
```

**NOT nginx file errors!**

---

**Deploy root directory = `/` (not `backend`)**
**Start command must `cd backend` first**
**Use relative API URLs in production (`/api`)**
