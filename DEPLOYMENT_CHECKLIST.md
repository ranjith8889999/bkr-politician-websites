# 🚀 Deployment Checklist for Hostinger/EasyPanel

## Before Pushing to GitHub

- [ ] Review all files are ready
- [ ] Check .gitignore excludes .env files
- [ ] Database file (*.db) is in .gitignore
- [ ] No sensitive data in code

## Step 1: Push to GitHub

- [ ] Initialize Git: `git init`
- [ ] Create .gitignore
- [ ] Add files: `git add .`
- [ ] Commit: `git commit -m "Initial commit"`
- [ ] Create GitHub repository
- [ ] Add remote: `git remote add origin <URL>`
- [ ] Push: `git push -u origin main`

## Step 2: Backend Deployment (EasyPanel)

- [ ] Login to Hostinger EasyPanel
- [ ] Create new Python application
- [ ] Connect GitHub repository
- [ ] Set root directory: `backend`
- [ ] Configure environment variables:
  - [ ] API_KEY (generate strong key)
  - [ ] ADMIN_USERNAME
  - [ ] ADMIN_PASSWORD (change from default)
  - [ ] DATABASE_PATH=bkr_database.db
  - [ ] FLASK_ENV=production
  - [ ] FLASK_DEBUG=False
  - [ ] CORS_ORIGINS (your domain)
- [ ] Build command: `pip install -r requirements.txt`
- [ ] Start command: `gunicorn app:app --bind 0.0.0.0:$PORT`
- [ ] Deploy backend
- [ ] Wait for successful deployment
- [ ] Open terminal/shell in EasyPanel
- [ ] Run: `python migrate_data.py --sample`
- [ ] Test backend: Visit /api/health endpoint
- [ ] Note your backend URL: ___________________________

## Step 3: Frontend Configuration

- [ ] Copy backend URL from Step 2
- [ ] Open `js/api-service.js`
- [ ] Update `API_CONFIG.baseURL` to: `https://your-backend-url/api`
- [ ] Update `API_CONFIG.apiKey` to match backend API_KEY
- [ ] Save file

## Step 4: Frontend Deployment

### Option A: Hostinger File Manager
- [ ] Login to Hostinger File Manager
- [ ] Navigate to `public_html` or domain folder
- [ ] Upload all files:
  - [ ] index.html
  - [ ] css/ folder
  - [ ] js/ folder
  - [ ] images/ folder
  - [ ] pages/ folder
  - [ ] admin/ folder

### Option B: EasyPanel Static Site
- [ ] Create new app in EasyPanel
- [ ] Type: Static Site
- [ ] Connect same GitHub repository
- [ ] Root directory: `/` (root)
- [ ] Deploy

## Step 5: Update CORS

- [ ] Go back to backend app in EasyPanel
- [ ] Update environment variable:
  - [ ] CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
- [ ] Restart backend application

## Step 6: Testing

- [ ] Visit your website
- [ ] Check homepage loads
- [ ] Scroll to "Health Camps" section
- [ ] Verify health camps are displayed
- [ ] Test admin login: /admin/pages/login.html
- [ ] Login with credentials
- [ ] Try adding a new health camp
- [ ] Verify it appears on homepage
- [ ] Test complaint form
- [ ] Test feedback form

## Step 7: Security Verification

- [ ] Changed default API_KEY
- [ ] Changed default ADMIN_PASSWORD
- [ ] FLASK_DEBUG=False
- [ ] FLASK_ENV=production
- [ ] CORS_ORIGINS set correctly
- [ ] SSL certificate active (https://)
- [ ] .env file NOT in repository
- [ ] Database file NOT publicly accessible

## Step 8: Final Touches

- [ ] Add real health camp data
- [ ] Upload actual images
- [ ] Test on mobile devices
- [ ] Test all admin features
- [ ] Set up domain (if custom)
- [ ] Configure email notifications (optional)
- [ ] Set up database backups

## 🎉 Deployment Complete!

Website URL: ___________________________
Backend API URL: ___________________________
Admin Panel: ___________________________/admin/pages/login.html

## 📝 Post-Deployment Notes

Date deployed: ___________________________
Issues encountered: ___________________________
___________________________________________
___________________________________________

Next maintenance date: ___________________________
