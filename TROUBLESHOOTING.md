# ⚠️ TROUBLESHOOTING: ERR_CONNECTION_REFUSED

## Problem
```
GET http://localhost:5000/api/health-camps net::ERR_CONNECTION_REFUSED
```

## Cause
The Flask API server is not running on port 5000.

## ✅ SOLUTION (Follow These Steps)

### Step 1: Check if API Server is Running

Open PowerShell and run:
```powershell
netstat -ano | findstr :5000
```

**If you see output:** Server is running (skip to Step 3)  
**If you see nothing:** Server is not running (continue to Step 2)

### Step 2: Start the Flask API Server

Option A - **Using Batch File (Recommended)**:
```powershell
cd c:\Users\Ranjit\Desktop\bkr\bkr4
.\start-servers.bat
```

Option B - **Manual Start**:
```powershell
cd c:\Users\Ranjit\Desktop\bkr\bkr4\backend
python app.py
```

You should see:
```
============================================================
🚀 BKR API Server Starting...
============================================================
📁 Database: bkr_database.db
🔑 API Key: bkr-secret...
🌐 Server: http://localhost:5000
📡 Health Check: http://localhost:5000/api/health
============================================================
 * Running on http://127.0.0.1:5000
```

**IMPORTANT:** Keep this terminal window open! Don't close it.

### Step 3: Test the API

Open browser and go to:
```
http://localhost:5000/api/health
```

You should see:
```json
{
  "success": true,
  "message": "BKR API Server is running",
  "version": "1.0.0"
}
```

### Step 4: Test Health Camps Endpoint

```
http://localhost:5000/api/health-camps
```

You should see JSON with health camps data.

### Step 5: Refresh Your Website

Now go to your website:
```
http://localhost:8080
http://localhost:8080/pages/health-camps.html
http://localhost:8080/admin/pages/health-camps.html
```

Health camps should now load from the database!

## 🔄 If Server Stops/Crashes

### Quick Restart:
```powershell
# Kill any stuck processes
Stop-Process -Name python -Force

# Wait 2 seconds
Start-Sleep -Seconds 2

# Restart server
cd c:\Users\Ranjit\Desktop\bkr\bkr4\backend
python app.py
```

## 🚨 Common Issues

### Issue 1: "Port 5000 already in use"

**Solution:**
```powershell
# Find what's using port 5000
netstat -ano | findstr :5000

# Output will show something like:
# TCP    0.0.0.0:5000    0.0.0.0:0    LISTENING    1234

# Kill that process (replace 1234 with the actual PID)
taskkill /PID 1234 /F

# Restart Flask
cd c:\Users\Ranjit\Desktop\bkr\bkr4\backend
python app.py
```

### Issue 2: "ModuleNotFoundError: No module named 'flask'"

**Solution:**
```powershell
cd c:\Users\Ranjit\Desktop\bkr\bkr4\backend
pip install -r requirements.txt
```

### Issue 3: Frontend Shows "Loading..." Forever

**Causes:**
1. Flask server not running
2. CORS issue
3. Wrong API URL

**Solution:**
1. Check Flask is running: http://localhost:5000/api/health
2. Check browser console (F12) for exact error
3. Verify `js/api-service.js` has correct URL:
   ```javascript
   const API_CONFIG = {
       baseURL: 'http://localhost:5000/api',
       ...
   };
   ```

### Issue 4: Database Not Found

**Solution:**
```powershell
cd c:\Users\Ranjit\Desktop\bkr\bkr4\backend
python migrate_data.py --sample
```

## ✅ Verification Checklist

Before reporting an issue, verify:

- [ ] Flask server terminal is open and running
- [ ] You see "Running on http://127.0.0.1:5000" message
- [ ] http://localhost:5000/api/health returns JSON
- [ ] http://localhost:5000/api/health-camps returns JSON with camps
- [ ] Frontend server is running on port 8080
- [ ] Browser console (F12) shows no CORS errors
- [ ] `bkr_database.db` file exists in `backend/` folder

## 🎯 Quick Test Commands

```powershell
# Test 1: Check if Flask is running
netstat -ano | findstr :5000

# Test 2: Check if frontend is running
netstat -ano | findstr :8080

# Test 3: Test API health
curl http://localhost:5000/api/health

# Test 4: Test health camps API
curl http://localhost:5000/api/health-camps

# Test 5: View Python processes
Get-Process python
```

## 📞 Still Not Working?

1. **Close ALL terminals**
2. **Restart fresh:**
   ```powershell
   cd c:\Users\Ranjit\Desktop\bkr\bkr4
   .\start-servers.bat
   ```
3. **Wait for both servers to start** (you'll see two terminal windows)
4. **Open browser:** http://localhost:8080

## 💡 Pro Tip: Keep Servers Running

**Don't close the terminal windows!**

You need **TWO terminals running**:
1. **Terminal 1** - Flask API (port 5000) - Shows "Running on http://127.0.0.1:5000"
2. **Terminal 2** - Frontend (port 8080) - Shows "Serving HTTP on :: port 8080"

Both must stay open while you're using the website.

## 🎬 Visual Guide

```
Step 1: Open PowerShell
Step 2: cd c:\Users\Ranjit\Desktop\bkr\bkr4
Step 3: .\start-servers.bat
Step 4: Wait for 2 terminal windows to appear
Step 5: Browser opens automatically at http://localhost:8080
Step 6: Login to admin and add a health camp!
```

---

**Need more help?** Check `QUICK_REFERENCE.md` or `README_DYNAMIC.md`
