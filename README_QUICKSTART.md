# BKR Website - Quick Start Guide

## 🚀 EASIEST WAY TO START

**Just double-click:** `START.bat`

That's it! The website will open automatically.

---

## 📝 MANUAL START (If you prefer)

### Terminal 1 - Backend API:
```powershell
cd backend
python app.py
```
**Keep this running!** Backend API at http://localhost:5000

### Terminal 2 - Frontend:
```powershell
python -m http.server 8080
```
**Keep this running!** Website at http://localhost:8080

---

## 🔐 Admin Login

**URL:** http://localhost:8080/admin/pages/login.html

```
Username: admin
Password: admin123
```

---

## 📂 Single Database Location

`backend/bkr_database.db` - All your data is here!

---

## ❌ Stop Servers

Close the PowerShell windows or press `CTRL+C` in terminals.

---

## 🔧 Troubleshooting

**Port already in use?**
```powershell
# Kill process on port 5000
netstat -ano | findstr :5000
taskkill /PID <process_id> /F

# Kill process on port 8080
netstat -ano | findstr :8080
taskkill /PID <process_id> /F
```

**Need fresh database?**
```powershell
cd backend
del bkr_database.db
python migrate_data.py --sample
```

---

## 📞 Support

Email: ranjith888999@gmail.com  
Phone: +91-9XXXXXX363
