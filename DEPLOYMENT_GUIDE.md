# BKR Website - Deployment Guide for Hostinger/EasyPanel

## 📋 Prerequisites

1. **Hostinger Account** with EasyPanel access
2. **GitHub Account**
3. **Your Domain** (if you have one)

---

## 🚀 Step-by-Step Deployment

### Step 1: Push to GitHub

1. **Initialize Git Repository** (if not already done):
```bash
cd c:\Users\Ranjit\Desktop\bkr\bkr4
git init
git add .
git commit -m "Initial commit - BKR Website"
```

2. **Create GitHub Repository**:
   - Go to https://github.com/new
   - Repository name: `bkr-politician-website`
   - Set to Public or Private
   - Click "Create repository"

3. **Push to GitHub**:
```bash
git remote add origin https://github.com/YOUR_USERNAME/bkr-politician-website.git
git branch -M main
git push -u origin main
```

---

### Step 2: Deploy Backend on EasyPanel

1. **Login to EasyPanel** on your Hostinger account

2. **Create New Application**:
   - Click "Create New App"
   - Choose "Python"
   - Name: `bkr-backend`

3. **Connect GitHub**:
   - Connect your GitHub account
   - Select repository: `bkr-politician-website`
   - Branch: `main`
   - Root directory: `backend`

4. **Configure Environment Variables** in EasyPanel:
```
API_KEY=YOUR_STRONG_SECRET_KEY_HERE
ADMIN_USERNAME=admin
ADMIN_PASSWORD=YOUR_SECURE_PASSWORD
DATABASE_PATH=bkr_database.db
FLASK_ENV=production
FLASK_DEBUG=False
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

**Generate Strong API Key**:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

5. **Build Settings**:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app --bind 0.0.0.0:$PORT`
   - Port: `5000` (or auto-assigned)

6. **Deploy** and wait for build to complete

7. **Initialize Database**:
   - Open EasyPanel Terminal/Shell
   - Run: `python migrate_data.py --sample`

8. **Note your Backend URL**: 
   - Example: `https://bkr-backend.yourdomain.com`

---

### Step 3: Deploy Frontend on Hostinger

**Option A: Using Hostinger File Manager**

1. **Upload Files**:
   - Login to Hostinger File Manager
   - Navigate to `public_html` (or your domain folder)
   - Upload these files/folders:
     - `index.html`
     - `css/`
     - `js/`
     - `images/`
     - `pages/`
     - `admin/`

2. **Update API Configuration**:
   - Edit `js/api-service.js`
   - Change API URL:
   ```javascript
   const API_CONFIG = {
       baseURL: 'https://bkr-backend.yourdomain.com/api',
       apiKey: 'YOUR_API_KEY_HERE',
       timeout: 10000
   };
   ```

**Option B: Using EasyPanel for Frontend**

1. Create another app in EasyPanel
2. Select "Static Site"
3. Deploy from same GitHub repo
4. Root directory: `/` (root)
5. Deploy

---

### Step 4: Update CORS Settings

After deploying frontend, update backend environment variables:

```
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com,https://bkr-frontend.yourdomain.com
```

Restart backend app in EasyPanel.

---

## 🔧 Configuration Files Created

1. **backend/requirements.txt** - Updated with `gunicorn`
2. **backend/Procfile** - For deployment platforms
3. **backend/.env.production** - Production environment template
4. **.gitignore** - Updated to exclude sensitive files

---

## ⚙️ Important Configuration Changes Needed

### 1. Update API URL in Frontend

Edit `js/api-service.js`:
```javascript
const API_CONFIG = {
    baseURL: 'https://YOUR-BACKEND-URL/api',  // ← Change this
    apiKey: 'YOUR_PRODUCTION_API_KEY',        // ← Change this
    timeout: 10000
};
```

### 2. Update Environment Variables

Copy `backend/.env.production` to `backend/.env` on server and update:
- `API_KEY` - Generate strong random key
- `ADMIN_PASSWORD` - Change default password
- `CORS_ORIGINS` - Add your domain

---

## 🧪 Testing After Deployment

1. **Test Backend API**:
```bash
curl https://your-backend-url.com/api/health
```

Expected response:
```json
{
  "success": true,
  "message": "BKR API Server is running",
  "version": "1.0.0"
}
```

2. **Test Frontend**:
   - Visit: `https://yourdomain.com`
   - Check health camps section loads
   - Test admin login: `https://yourdomain.com/admin/pages/login.html`

3. **Test Admin Panel**:
   - Login with your credentials
   - Try adding a health camp
   - Verify it appears on homepage

---

## 🔒 Security Checklist

- [ ] Changed default API_KEY
- [ ] Changed default ADMIN_PASSWORD
- [ ] Updated CORS_ORIGINS to your domain
- [ ] Set FLASK_DEBUG=False
- [ ] Set FLASK_ENV=production
- [ ] Database file is not publicly accessible
- [ ] .env file is not in Git (check .gitignore)

---

## 📱 Quick Commands

### Generate Strong API Key:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Create Database on Server:
```bash
cd backend
python migrate_data.py --sample
```

### View Backend Logs:
Check EasyPanel logs section for errors

---

## 🐛 Troubleshooting

### Issue: CORS Errors
**Solution**: Update `CORS_ORIGINS` in backend environment variables with your frontend domain

### Issue: 500 Internal Server Error
**Solution**: Check backend logs in EasyPanel. Usually missing environment variables.

### Issue: Database not found
**Solution**: Run `python migrate_data.py --sample` in backend terminal

### Issue: API calls failing
**Solution**: Update `API_CONFIG.baseURL` in `js/api-service.js` with correct backend URL

---

## 📞 Support

- Email: ranjith888999@gmail.com
- Phone: +91-9XXXXXX363

---

## 📝 Next Steps After Deployment

1. Test all functionality thoroughly
2. Add real health camp data
3. Upload actual images to `images/` folder
4. Set up SSL certificate (usually automatic on Hostinger)
5. Configure custom domain if you have one
6. Set up backups for database

---

**Ready to Deploy!** 🚀

Follow the steps above and your website will be live on Hostinger!
