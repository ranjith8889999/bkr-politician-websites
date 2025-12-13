# BKR Politician Website - Dynamic Version

A modern, professional website for **B Kishore Reddy** - Congress MLA Candidate for Quthbullapur Constituency.

**Now with Flask Backend + SQLite Database for Dynamic Content Management!**

![Congress Hand](images/congresshand.png)

## 🌐 Live Website

- **Frontend**: [http://localhost:8080](http://localhost:8080) (when running locally)
- **Backend API**: [http://localhost:5000](http://localhost:5000/api/health)
- **Admin Panel**: [http://localhost:8080/admin/pages/login.html](http://localhost:8080/admin/pages/login.html)

## 🚀 Quick Start (3 Easy Steps)

### Option 1: Automated Startup (Recommended)

**Windows:**
```powershell
# Double-click start-servers.bat
# OR run in PowerShell:
.\start-servers.bat
```

**Mac/Linux:**
```bash
chmod +x start-servers.sh
./start-servers.sh
```

This will:
- ✅ Install Python dependencies automatically
- ✅ Create database with sample data
- ✅ Start Flask API server (Port 5000)
- ✅ Start frontend server (Port 8080)
- ✅ Open website in your browser

### Option 2: Manual Startup

**Step 1: Install Backend Dependencies**
```powershell
cd backend
pip install -r requirements.txt
```

**Step 2: Initialize Database**
```powershell
# Create sample data
python migrate_data.py --sample

# OR migrate from localStorage backup
python migrate_data.py path/to/backup.json
```

**Step 3: Start Servers**

Terminal 1 - API Server:
```powershell
cd backend
python app.py
```

Terminal 2 - Frontend Server:
```powershell
python -m http.server 8080
```

**Step 4: Open Website**
- Frontend: http://localhost:8080
- Admin: http://localhost:8080/admin/pages/login.html

## 🔐 Admin Login

```
Username: admin
Password: admin123
```

⚠️ **Change these in production!** Edit `backend/.env` file.

## 📋 What's New - Dynamic Features

### 🎯 Now Database-Driven!

All website content is now stored in SQLite database and managed through REST API:

✅ **Health Camps** - Create, update, delete from admin panel  
✅ **Complaints** - Stored in database, viewable in admin  
✅ **Feedback** - All ratings and reviews in database  
✅ **News Updates** - Publish articles dynamically  
✅ **Dashboard Stats** - Real-time statistics  

### 🔄 How It Works

```
User submits complaint → POST /api/complaints → SQLite Database
Admin views complaints → GET /api/complaints (with API key) → Display in admin panel
Admin adds health camp → POST /api/health-camps → Database → Updates on website instantly
```

## 📁 Project Structure

```
bkr4/
├── backend/                        # NEW: Flask API Backend
│   ├── app.py                      # Flask application & API routes
│   ├── database.py                 # Database operations (CRUD)
│   ├── models.py                   # Database schema
│   ├── migrate_data.py             # Data migration tool
│   ├── requirements.txt            # Python dependencies
│   ├── .env                        # Environment variables (API key)
│   ├── .env.example                # Environment template
│   └── bkr_database.db             # SQLite database (auto-created)
│
├── js/
│   ├── api-service.js              # NEW: API client for frontend
│   ├── admin.js                    # Admin panel (updated for API)
│   └── main.js                     # Main website functionality
│
├── admin/pages/                    # Admin panel pages (updated)
│   ├── login.html
│   ├── dashboard.html
│   ├── health-camps.html
│   └── ... (all updated to use API)
│
├── pages/                          # Public pages (updated)
│   ├── health-camps.html           # Now loads from API
│   ├── complaint.html
│   └── feedback.html
│
├── index.html                      # Main page (updated)
├── start-servers.bat               # NEW: Windows startup script
├── start-servers.sh                # NEW: Mac/Linux startup script
└── README.md                       # This file
```

## 🛠️ API Endpoints

### Public Endpoints (No Authentication)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Health check |
| GET | `/api/health-camps` | Get all health camps |
| GET | `/api/health-camps?status=upcoming` | Filter by status |
| GET | `/api/health-camps/<id>` | Get single camp |
| POST | `/api/complaints` | Submit complaint |
| POST | `/api/feedback` | Submit feedback |
| GET | `/api/news` | Get published news |

### Protected Endpoints (Require API Key)

**Header Required:** `X-API-Key: your-api-key`

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/health-camps` | Create health camp |
| PUT | `/api/health-camps/<id>` | Update health camp |
| DELETE | `/api/health-camps/<id>` | Delete health camp |
| GET | `/api/complaints` | Get all complaints |
| PATCH | `/api/complaints/<id>/status` | Update status |
| GET | `/api/feedback` | Get all feedback |
| POST/PUT/DELETE | `/api/news` | Manage news |
| GET | `/api/dashboard/stats` | Dashboard stats |

## 🔒 Security Configuration

### API Key Setup

Edit `backend/.env`:
```env
# Change this to a strong secret key
API_KEY=bkr-secret-key-2025-change-in-production

# Also update in js/api-service.js
const API_CONFIG = {
    apiKey: 'bkr-secret-key-2025-change-in-production'
};
```

### Admin Password

Edit `backend/.env`:
```env
ADMIN_USERNAME=admin
ADMIN_PASSWORD=your-strong-password-here
```

## 📊 Database Schema

### health_camps
```sql
id, title, date, time, location, services, 
description, contact, status, created_at, updated_at
```

### complaints
```sql
id, name, phone, email, area, category, subject, 
message, address, status, date, created_at, updated_at
```

### feedback
```sql
id, name, phone, email, area, rating, category, 
message, suggestions, date, created_at
```

### news
```sql
id, title, category, summary, content, status, 
date, created_at, updated_at
```

## 🔄 Data Migration

### From localStorage Backup

1. Export data from admin panel (Settings → Backup Data)
2. Run migration:
```powershell
cd backend
python migrate_data.py path/to/backup.json
```

### Create Sample Data

```powershell
cd backend
python migrate_data.py --sample
```

This creates:
- 3 sample health camps
- 2 sample news articles

## 🧪 Testing

### Test API Server

```powershell
curl http://localhost:5000/api/health
```

Expected response:
```json
{
  "success": true,
  "message": "BKR API Server is running",
  "version": "1.0.0"
}
```

### Test Health Camps Endpoint

```powershell
curl http://localhost:5000/api/health-camps
```

### Test Protected Endpoint

```powershell
curl -H "X-API-Key: your-api-key" http://localhost:5000/api/complaints
```

## 🚨 Troubleshooting

### Port Already in Use

**Windows:**
```powershell
# Check port 5000
netstat -ano | findstr :5000
taskkill /PID <process_id> /F

# Check port 8080
netstat -ano | findstr :8080
taskkill /PID <process_id> /F
```

**Mac/Linux:**
```bash
# Check and kill port 5000
lsof -ti:5000 | xargs kill -9

# Check and kill port 8080
lsof -ti:8080 | xargs kill -9
```

### API Not Responding

1. Check if Flask server is running
2. Check console for errors
3. Verify `.env` file exists in `backend/` folder
4. Check firewall settings

### Database Errors

```powershell
cd backend
# Delete and recreate database
rm bkr_database.db
python migrate_data.py --sample
```

### Frontend Not Loading Data

1. Open browser console (F12)
2. Check for CORS errors
3. Verify API URL in `js/api-service.js`
4. Ensure Flask server is running

## 🌐 Deployment

### Deploy to Production

1. **Backend**: Deploy Flask to PythonAnywhere, Render, or Railway
   - Set environment variables
   - Update CORS origins in `app.py`

2. **Frontend**: Deploy to GitHub Pages, Netlify, or Vercel
   - Update API URL in `js/api-service.js`

3. **Database**: 
   - For production, consider PostgreSQL or MySQL
   - Update `database.py` connection string

### Environment Variables for Production

```env
API_KEY=strong-random-secret-key-here
ADMIN_PASSWORD=strong-admin-password
DATABASE_PATH=/path/to/production/database.db
FLASK_ENV=production
FLASK_DEBUG=False
```

## 📚 Technology Stack

**Frontend:**
- HTML5, CSS3, JavaScript (ES6+)
- Font Awesome 6.5.1
- Google Fonts (Poppins)

**Backend:**
- Python 3.7+
- Flask 3.0.0
- SQLite3
- Flask-CORS
- python-dotenv

**Features:**
- ✅ REST API architecture
- ✅ API key authentication
- ✅ SQLite database
- ✅ CORS enabled
- ✅ Real-time updates
- ✅ Mobile responsive
- ✅ Error handling

## 🔗 Useful Links

- Flask Documentation: https://flask.palletsprojects.com/
- SQLite Documentation: https://www.sqlite.org/docs.html
- REST API Tutorial: https://restfulapi.net/

## 📞 Support & Contact

- **Email**: ranjith888999@gmail.com
- **Phone**: +91-9XXXXXX363

## 📄 License

Copyright © 2025 B Kishore Reddy. All rights reserved.

---

**Version**: 2.0.0 (Dynamic)  
**Last Updated**: December 12, 2025  
**Developed for**: BONGUNURI KISHORE REDDY - Congress MLA Candidate, Quthbullapur Constituency

## 🎉 What Changed from v1.0.0?

### Before (v1.0.0 - Static)
- ❌ Data stored in browser localStorage only
- ❌ No cross-device synchronization
- ❌ Limited to ~5MB storage
- ❌ Data lost when clearing browser
- ❌ No real authentication

### Now (v2.0.0 - Dynamic)
- ✅ Data stored in SQLite database
- ✅ Works across all devices
- ✅ Unlimited storage
- ✅ Persistent data
- ✅ API key authentication
- ✅ Real-time updates
- ✅ Better security
- ✅ Production-ready
