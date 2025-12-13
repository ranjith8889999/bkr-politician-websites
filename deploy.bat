@echo off
REM Quick Deployment Script for BKR Website (Windows)

echo ==========================================
echo BKR Website - Deployment Preparation
echo ==========================================
echo.

REM Check if git is initialized
if not exist ".git" (
    echo [*] Initializing Git repository...
    git init
    echo [OK] Git initialized
) else (
    echo [OK] Git repository already exists
)

REM Add all files
echo.
echo [*] Adding files to Git...
git add .

REM Commit changes
set /p commit_msg="Enter commit message (or press Enter for default): "
if "%commit_msg%"=="" set commit_msg=Update for deployment

git commit -m "%commit_msg%"
echo [OK] Changes committed

REM Check for remote
git remote | findstr /C:"origin" >nul
if errorlevel 1 (
    echo.
    echo [!] No remote repository found
    set /p repo_url="Enter GitHub repository URL: "
    git remote add origin %repo_url%
    echo [OK] Remote added
)

REM Push to GitHub
echo.
echo [*] Pushing to GitHub...
git push -u origin main

if errorlevel 0 (
    echo [OK] Successfully pushed to GitHub!
    echo.
    echo ==========================================
    echo Next Steps:
    echo ==========================================
    echo 1. Go to your Hostinger EasyPanel
    echo 2. Create new Python app for backend
    echo 3. Connect to your GitHub repository
    echo 4. Set environment variables ^(see DEPLOYMENT_GUIDE.md^)
    echo 5. Deploy backend
    echo 6. Update js/api-service.js with backend URL
    echo 7. Upload frontend files to public_html
    echo.
    echo Full guide: DEPLOYMENT_GUIDE.md
    echo ==========================================
) else (
    echo [X] Push failed. Check your credentials and try again.
)

pause
