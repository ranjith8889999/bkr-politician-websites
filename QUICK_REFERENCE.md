# BKR Website - Quick Reference Guide

## 🚀 Starting the Website

### Windows (Double-click)
```
start-servers.bat
```

### Manual Start
```powershell
# Terminal 1 - Backend API
cd backend
python app.py

# Terminal 2 - Frontend
python -m http.server 8080
```

## 🔗 Access URLs

| Service | URL | Notes |
|---------|-----|-------|
| **Website** | http://localhost:8080 | Main public site |
| **Admin Login** | http://localhost:8080/admin/pages/login.html | Login page |
| **Admin Dashboard** | http://localhost:8080/admin/pages/dashboard.html | After login |
| **API Server** | http://localhost:5000 | Backend API |
| **API Health** | http://localhost:5000/api/health | Test API |

## 🔐 Login Credentials

```
Username: admin
Password: admin123
```

## 📊 Admin Panel Pages

| Page | URL | Purpose |
|------|-----|---------|
| Dashboard | `/admin/pages/dashboard.html` | Overview & stats |
| Health Camps | `/admin/pages/health-camps.html` | Manage camps |
| Complaints | `/admin/pages/complaints.html` | View complaints |
| Feedback | `/admin/pages/feedback.html` | View feedback |
| News | `/admin/pages/news.html` | Manage news |
| Gallery | `/admin/pages/gallery.html` | Manage images |
| Content | `/admin/pages/content.html` | Edit content |
| Settings | `/admin/pages/settings.html` | Admin settings |

## 🎯 Common Tasks

### Add a New Health Camp

1. Go to: http://localhost:8080/admin/pages/login.html
2. Login with admin/admin123
3. Click "Health Camps" in sidebar
4. Click "Add New Camp" button
5. Fill in the form:
   - **Title**: e.g., "Free Eye Check-up Camp"
   - **Date**: Select date
   - **Time**: e.g., "9:00 AM - 5:00 PM"
   - **Location**: e.g., "Community Hall, Quthbullapur"
   - **Services**: e.g., "Eye Screening, Free Spectacles"
   - **Description**: Additional details
   - **Contact**: Phone number
6. Click "Add Camp"
7. Check the frontend: http://localhost:8080

### View Submitted Complaints

1. Login to admin panel
2. Go to "Complaints" page
3. View all complaints with status
4. Filter by category or status
5. Update status as needed

### Create Sample Data

```powershell
cd backend
python migrate_data.py --sample
```

This creates:
- 3 sample health camps
- 2 sample news articles

## 🔧 Configuration

### Change API Key

Edit `backend/.env`:
```env
API_KEY=your-new-secret-key
```

Edit `js/api-service.js`:
```javascript
const API_CONFIG = {
    apiKey: 'your-new-secret-key'
};
```

### Change Admin Password

Edit `backend/.env`:
```env
ADMIN_PASSWORD=your-new-password
```

## 🐛 Troubleshooting

### "API Server is not responding"

**Solution:**
```powershell
# Check if Flask is running
# Look for terminal with Flask output
# If not running:
cd backend
python app.py
```

### "Port 5000 already in use"

**Solution:**
```powershell
# Find process
netstat -ano | findstr :5000

# Kill process (replace PID)
taskkill /PID <process_id> /F

# Restart server
cd backend
python app.py
```

### "Port 8080 already in use"

**Solution:**
```powershell
# Find process
netstat -ano | findstr :8080

# Kill process
taskkill /PID <process_id> /F

# Restart server
python -m http.server 8080
```

### "No health camps showing"

**Causes:**
1. API server not running
2. No data in database
3. Browser console errors

**Solutions:**
1. Check API: http://localhost:5000/api/health
2. Create sample data: `python migrate_data.py --sample`
3. Check browser console (F12) for errors
4. Verify API URL in `js/api-service.js`

### Database Errors

**Reset database:**
```powershell
cd backend
del bkr_database.db
python migrate_data.py --sample
```

## 📦 Database Management

### View Data

```powershell
cd backend
python

>>> import sqlite3
>>> conn = sqlite3.connect('bkr_database.db')
>>> cursor = conn.cursor()
>>> cursor.execute("SELECT * FROM health_camps")
>>> for row in cursor.fetchall():
...     print(row)
>>> conn.close()
```

### Backup Database

```powershell
cd backend
copy bkr_database.db bkr_database_backup_2025-12-12.db
```

### Export as JSON

Use Admin Panel → Settings → Backup Data

## 🧪 Testing API

### Test Health Check

```powershell
curl http://localhost:5000/api/health
```

### Get Health Camps

```powershell
curl http://localhost:5000/api/health-camps
```

### Get Upcoming Camps

```powershell
curl http://localhost:5000/api/health-camps?status=upcoming
```

### Get Dashboard Stats (Protected)

```powershell
curl -H "X-API-Key: bkr-secret-key-2025-change-in-production" http://localhost:5000/api/dashboard/stats
```

## 📝 API Response Format

### Success Response

```json
{
  "success": true,
  "data": [...],
  "count": 3
}
```

### Error Response

```json
{
  "success": false,
  "error": "Error message here"
}
```

## 🔄 Update Flow

```
User Action → Frontend (JavaScript) → API Call → Flask Server → SQLite Database → Response → UI Update
```

Example:
```
Admin adds camp → admin.js → POST /api/health-camps → app.py → database.py → Success → Reload table
```

## 📱 Mobile Testing

Access from phone on same network:
```
http://192.168.1.4:8080
```

(Replace with your computer's IP address)

## 🚀 Production Deployment

### Backend (Flask API)

Deploy to:
- PythonAnywhere (Free tier available)
- Render.com (Free tier available)
- Railway.app
- Heroku

Update in `js/api-service.js`:
```javascript
const API_CONFIG = {
    baseURL: 'https://your-api-domain.com/api',
    apiKey: 'production-api-key'
};
```

### Frontend

Deploy to:
- GitHub Pages (Free)
- Netlify (Free)
- Vercel (Free)

## 📞 Need Help?

- Email: ranjith888999@gmail.com
- Check browser console (F12) for errors
- Check Flask terminal for API errors
- Review backend/README.md for API docs

## ✅ Checklist

Before going live:

- [ ] Change API key in `.env` and `api-service.js`
- [ ] Change admin password in `.env`
- [ ] Test all CRUD operations
- [ ] Test on mobile device
- [ ] Backup database
- [ ] Update contact information
- [ ] Test form submissions
- [ ] Check CORS settings for production URL
- [ ] Set `FLASK_ENV=production` in `.env`
- [ ] Use production WSGI server (gunicorn)

---

**Quick Commands:**

```powershell
# Start everything
.\start-servers.bat

# Create sample data
cd backend; python migrate_data.py --sample

# Reset database
cd backend; del bkr_database.db; python migrate_data.py --sample

# Test API
curl http://localhost:5000/api/health

# Open website
start http://localhost:8080

# Open admin
start http://localhost:8080/admin/pages/login.html
```
