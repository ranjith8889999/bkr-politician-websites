# 🚨 CRITICAL FIX: EasyPanel App Type is WRONG

## The Problem:

Your logs show:
```
2025/12/13 12:11:42 [notice] 1#1: worker process 11 exited with code 0
[error] 11#11: *2 open() "/app/api/health-camps" failed (2: No such file or directory)
```

**This is nginx, NOT Python/Flask!**

Your app is deployed as a **Static Site** when it should be a **Python App**.

---

## ✅ THE FIX:

### You MUST Deploy as a Python Application

In EasyPanel, you likely clicked "Static Site" or "HTML" instead of "Python".

### Step-by-Step Fix:

#### Option 1: Change Existing App Settings

1. **Go to your EasyPanel app settings**
2. **Look for "App Type" or "Build Pack"**
3. **Change to: Python** (not Static, not HTML)
4. **Redeploy**

#### Option 2: Create New Python App (Recommended)

1. **Delete current app** `affiliate-bkr`
2. **Create NEW app:**
   - Click **"+ New App"**
   - Choose **"Python"** (NOT Static Site)
   - Connect to GitHub: `ranjith8889999/bkr-politician-websites`
   - Branch: `feature/added_db`

3. **Configure Build:**
   ```
   Root Directory: /
   Build Command: cd backend && pip install -r requirements.txt
   Start Command: cd backend && gunicorn wsgi:app --bind 0.0.0.0:$PORT --workers 2
   ```

4. **Environment Variables:**
   ```
   API_KEY=bkr-secret-key-2025-change-in-production
   DATABASE_PATH=bkr_database.db
   FLASK_ENV=production
   FLASK_DEBUG=False
   CORS_ORIGINS=*
   ```

5. **Deploy**

6. **After deployment, open Terminal:**
   ```bash
   cd backend
   python migrate_data.py --sample
   ```

---

## 🔍 How to Verify It's Working:

### ❌ WRONG (Static Site - Current State):
```
Logs show: nginx worker process
Error: open() "/app/api/health-camps" failed
```

### ✅ CORRECT (Python App):
```
Logs show:
[INFO] Starting gunicorn 21.2.0
[INFO] Listening at: http://0.0.0.0:5000
[INFO] Using worker: sync
[INFO] Booting worker with pid: 123
```

---

## 🎯 Key Points:

1. **Static sites** = nginx serves files only (no Python)
2. **Python apps** = Runs Flask/Django/Python code
3. **You NEED Python app type** to run Flask

---

## 🆘 If You Can't Find App Type Setting:

You may need to **delete and recreate** the app as a Python app.

**Before deleting:** Note down your custom domain settings if any.

---

## 📸 What to Look For:

When creating the app, you should see options like:
- ✓ **Python** ← Choose this
- ✗ Static Site
- ✗ Docker
- ✗ Node.js

---

## 💡 Alternative: Check Start Command

If EasyPanel doesn't have explicit "App Type", it detects based on files:

**Make sure these files exist in ROOT directory:**
- `runtime.txt` - Tells EasyPanel it's Python
- `Procfile` - But this should be in backend/

**Try moving files to root:**

