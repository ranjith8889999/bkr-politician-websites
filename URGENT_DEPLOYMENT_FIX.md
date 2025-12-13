# URGENT: EasyPanel Backend Deployment Fix

## Problem Identified:
Your logs show **nginx serving static files**, not Flask!

```
[error] 9#9: *1 open() "/app/api/health-camps" failed (2: No such file or directory)
```

This means nginx is looking for a FILE called `/app/api/health-camps` - **the Flask app is NOT running!**

---

## ✅ CORRECT DEPLOYMENT ARCHITECTURE:

```
┌─────────────────────────────────────────────────────┐
│  Frontend (Static Site)                             │
│  https://affiliate-bkr.nwp2mw.easypanel.host       │
│  ├── index.html                                     │
│  ├── pages/                                         │
│  ├── css/                                           │
│  └── js/api-service.js  ────────────┐              │
└─────────────────────────────────────│───────────────┘
                                      │
                                      │ API Calls
                                      │
                                      ▼
┌─────────────────────────────────────────────────────┐
│  Backend (Python/Flask)                             │
│  https://bkr-backend-NEW-URL.easypanel.host        │
│  ├── app.py                                         │
│  ├── wsgi.py                                        │
│  ├── database.py                                    │
│  └── bkr_database.db                                │
└─────────────────────────────────────────────────────┘
```

---

## 🚀 Step-by-Step Fix:

### 1. Create NEW Backend App in EasyPanel

**App Configuration:**
```
Name: bkr-backend
Type: Python
Source: GitHub (bkr-politician-websites)
Branch: feature/added_db
Root Directory: backend          ← CRITICAL!
```

**Build Command:**
```bash
pip install -r requirements.txt
```

**Start Command:**
```bash
gunicorn wsgi:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120 --access-logfile - --error-logfile -
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

### 2. After Backend Deployment

**Open Backend Terminal** and run:
```bash
python migrate_data.py --sample
```

**Test Backend:**
```bash
curl https://YOUR-BACKEND-URL.easypanel.host/api/health
```

Expected:
```json
{"success": true, "message": "BKR API Server is running", "version": "1.0.0"}
```

### 3. Update Frontend API URL

**Copy your backend URL** from EasyPanel (e.g., `https://bkr-backend-xyz.easypanel.host`)

**Update `js/api-service.js`:**
```javascript
const API_CONFIG = {
    baseURL: isLocalhost 
        ? 'http://localhost:5000/api' 
        : 'https://YOUR-ACTUAL-BACKEND-URL.easypanel.host/api',
    apiKey: 'bkr-secret-key-2025-change-in-production',
    timeout: 10000
};
```

### 4. Redeploy Frontend

Upload updated `js/api-service.js` to your frontend app.

---

## 🔍 How to Verify It's Working:

**Backend (should show Flask logs):**
```
✓ Serving Flask app 'app'
✓ Running on all addresses
✓ Gunicorn workers started
```

**NOT nginx file errors!**

**Frontend (browser console):**
```
✓ Loaded 3 health camps on homepage
✓ No CORS errors
✓ No 404 errors
```

---

## 🆘 If You Can't Create Two Apps

**Alternative: Use Same Domain with Different Paths**

You'll need to configure nginx in EasyPanel to proxy `/api/*` to Flask.

**But the EASIEST solution is:**
1. Deploy backend as separate Python app
2. Deploy frontend as static site
3. Update API URL in frontend

---

## 📝 Summary:

**Current State:**
- ❌ Backend NOT deployed (nginx serving files)
- ✅ Frontend deployed (HTML works)
- ❌ API calls fail (no Flask app)

**Required State:**
- ✅ Backend: Python app running Flask
- ✅ Frontend: Static site with HTML
- ✅ Frontend calls backend via HTTPS

---

**The key issue:** You deployed frontend code where backend should be!

Create a separate **Python app** for backend, not a static site!
