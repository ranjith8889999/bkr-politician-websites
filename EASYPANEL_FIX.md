# 🔧 EasyPanel Deployment Fix Guide

## Problem: Backend Returns 404 on https://affiliate-bkr.nwp2mw.easypanel.host/api/health-camps

---

## ✅ Solution Steps:

### Step 1: Update Backend Files in GitHub

The following files have been created/updated:
- ✅ `backend/wsgi.py` - WSGI entry point
- ✅ `backend/Procfile` - Updated start command
- ✅ `backend/runtime.txt` - Python version
- ✅ `backend/start.sh` - Startup script
- ✅ `backend/uwsgi.ini` - UWSGI config

**Push to GitHub:**
```bash
git add backend/
git commit -m "Fix: Add proper deployment configuration for EasyPanel"
git push origin feature/added_db
```

---

### Step 2: Configure EasyPanel Backend Application

1. **Login to EasyPanel**
2. **Go to your backend app** (affiliate-bkr)
3. **Update Settings:**

#### Build Settings:
- **Source:** GitHub Repository
- **Branch:** `feature/added_db` (or `main`)
- **Root Directory:** `backend`
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** Choose ONE of these:

**Option 1 (Recommended):**
```bash
bash start.sh
```

**Option 2:**
```bash
gunicorn wsgi:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120
```

**Option 3:**
```bash
python app.py
```

#### Environment Variables:
Make sure these are set in EasyPanel:
```
API_KEY=bkr-secret-key-2025-change-in-production
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123
DATABASE_PATH=bkr_database.db
FLASK_ENV=production
FLASK_DEBUG=False
CORS_ORIGINS=https://affiliate-bkr.nwp2mw.easypanel.host
PORT=5000
```

---

### Step 3: Initialize Database

After deployment, open **EasyPanel Terminal** for your backend app:

```bash
python migrate_data.py --sample
```

This creates the database with sample data.

---

### Step 4: Test Backend Directly

**Test Health Endpoint:**
```bash
curl https://affiliate-bkr.nwp2mw.easypanel.host/api/health
```

**Expected Response:**
```json
{
  "success": true,
  "message": "BKR API Server is running",
  "version": "1.0.0"
}
```

**Test Health Camps:**
```bash
curl https://affiliate-bkr.nwp2mw.easypanel.host/api/health-camps
```

---

### Step 5: Check Logs

In EasyPanel:
1. Go to your backend app
2. Click **Logs** tab
3. Look for errors

**Common Issues:**

**Error:** `ModuleNotFoundError: No module named 'app'`
- **Fix:** Change start command to `gunicorn wsgi:app` (not `app:app`)

**Error:** `Address already in use`
- **Fix:** EasyPanel handles ports automatically, use `$PORT` variable

**Error:** `Database not found`
- **Fix:** Run `python migrate_data.py --sample` in terminal

---

### Step 6: Verify Routes

Check if your app.py has the routes defined. Look for:

```python
@app.route('/api/health', methods=['GET'])
def health_check():
    # ...

@app.route('/api/health-camps', methods=['GET'])
def get_health_camps():
    # ...
```

These should be BEFORE the `if __name__ == '__main__':` block.

---

### Step 7: Alternative Deployment Approach

If the above doesn't work, try this simpler approach:

**In EasyPanel Backend Settings:**

**Start Command:**
```bash
python -m flask run --host=0.0.0.0 --port=$PORT
```

**Environment Variables (add these):**
```
FLASK_APP=app.py
FLASK_ENV=production
```

---

## 🧪 Testing Checklist

After redeployment, test these URLs:

- [ ] `https://affiliate-bkr.nwp2mw.easypanel.host/api/health` - Should return JSON
- [ ] `https://affiliate-bkr.nwp2mw.easypanel.host/api/health-camps` - Should return camps list
- [ ] Frontend should load health camps without errors
- [ ] Admin panel should work

---

## 🔍 Debug Commands

**Check if Flask is running:**
```bash
ps aux | grep gunicorn
```

**Check environment variables:**
```bash
env | grep FLASK
env | grep PORT
```

**Test locally in EasyPanel terminal:**
```bash
python -c "from app import app; print(app.url_map)"
```

This shows all registered routes.

---

## 📝 Quick Fix Summary

1. ✅ Created `wsgi.py` entry point
2. ✅ Updated `Procfile` with correct command
3. ✅ Added `start.sh` startup script
4. ✅ Push changes to GitHub
5. ⚙️ Update EasyPanel start command
6. 🔄 Redeploy
7. 🗄️ Initialize database
8. ✅ Test endpoints

---

## 🆘 If Still Not Working

**Check these:**

1. **Port Binding:** Make sure app is using `$PORT` environment variable
2. **WSGI Entry:** Use `wsgi:app` not `app:app`
3. **File Location:** Backend files must be in `backend/` folder
4. **Python Version:** Python 3.11+ recommended
5. **Dependencies:** All packages in `requirements.txt` installed

**View Full Logs:**
In EasyPanel, go to Logs and filter for:
- `ERROR`
- `WARNING`
- `ModuleNotFoundError`
- `404`

---

## 💡 Alternative: Deploy Backend Separately

If EasyPanel isn't working, consider:

1. **PythonAnywhere** - Free tier available
2. **Render.com** - Free tier with auto-deploy
3. **Railway.app** - Easy Python deployment
4. **Heroku** - Classic PaaS

All support Flask + Gunicorn out of the box.

---

**Need more help?** Share the EasyPanel logs and I can help debug further!
