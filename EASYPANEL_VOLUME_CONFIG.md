# 🔧 EASYPANEL DEPLOYMENT CONFIGURATION

## Required Configuration for Database Persistence

### 1. Environment Variables (REQUIRED)

Add these in your EasyPanel app settings:

```bash
# Database Configuration
DATABASE_PATH=/app/backend/data/bkr_database.db

# API Configuration
API_KEY=bkr-secret-key-2025
FLASK_ENV=production
FLASK_DEBUG=False
CORS_ORIGINS=*

# Optional: Admin credentials
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123
```

### 2. Persistent Volume/Mount (REQUIRED for Database Persistence)

**To prevent database from being deleted on every deployment:**

```
Mount Configuration:
├── Type: Volume
├── Mount Path: /app/backend/data
└── Size: 1GB (or adjust based on your needs)
```

**How to add in EasyPanel:**
1. Go to your app → Settings
2. Find "Volumes" or "Mounts" section
3. Click "Add Volume"
4. Set mount path: `/app/backend/data`
5. Set size: `1GB`
6. Save and redeploy

### 3. Start Command

```bash
cd backend && bash start.sh
```

OR

```bash
cd backend && gunicorn wsgi:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120
```

### 4. Build Command

```bash
cd backend && pip install -r requirements.txt
```

---

## 📂 Directory Structure in Production

```
/app/
├── backend/
│   ├── data/              ← PERSISTENT VOLUME (survives redeploys)
│   │   └── bkr_database.db  ← Your database
│   ├── app.py
│   ├── wsgi.py
│   └── start.sh
├── css/
├── js/
└── index.html
```

---

## 🔄 How It Works

### Without Persistent Volume:
```
Deploy → Clear filesystem → No database → Create new DB with sample data
         ↓
    ❌ Data lost on every deployment
```

### With Persistent Volume:
```
Deploy → Clear filesystem → Mount volume → Database exists in volume
         ↓                      ↓
    Ephemeral files     Persistent data (survives)
         ↓                      ↓
    ✅ Code updates     ✅ Database preserved
```

---

## ✅ Verification Steps

After adding persistent volume and redeploying:

1. **Check if volume is mounted:**
   ```bash
   ls -la /app/backend/data/
   ```
   Should show: `bkr_database.db`

2. **Add some test data** via admin panel

3. **Redeploy the app**

4. **Check if data persists** - visit frontend, data should still be there

---

## 🆘 Troubleshooting

### Database still getting cleared?

1. **Verify volume mount path:** Must be `/app/backend/data`
2. **Check DATABASE_PATH env var:** Should be `/app/backend/data/bkr_database.db`
3. **Check EasyPanel logs:** Look for "Using existing database" message

### Can't see data directory?

```bash
# In EasyPanel terminal
cd /app/backend
ls -la
mkdir -p data
```

### Database permissions error?

```bash
# In EasyPanel terminal
chmod 777 /app/backend/data
chmod 666 /app/backend/data/bkr_database.db
```

---

## 📝 Alternative: Use PostgreSQL (Production Grade)

For a more robust solution, consider using PostgreSQL:

1. Create PostgreSQL database in EasyPanel
2. Update Python dependencies: `psycopg2-binary`
3. Update database.py to use PostgreSQL instead of SQLite
4. Connection string in environment variable

---

**With persistent volume configured, your database will survive all deployments! 🎉**
