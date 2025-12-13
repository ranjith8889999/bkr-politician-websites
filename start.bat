@echo off
REM ============================================
REM BKR Website Startup Script
REM ============================================

echo.
echo ============================================
echo  BKR Website - Starting Servers
echo ============================================
echo.

REM Check if Python is installed
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7+ from https://www.python.org/
    pause
    exit /b 1
)

echo [1/4] Installing Python dependencies...
cd backend
python -m pip install -r requirements.txt --quiet
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo [2/4] Creating database with sample data...
python migrate_data.py --sample
cd ..

echo [3/4] Starting Flask API Server (Port 5000)...
start "BKR Backend API" /MIN powershell -NoExit -Command "cd backend; python app.py"

timeout /t 3 /nobreak >nul

echo [4/4] Starting Frontend Server (Port 8080)...
start "BKR Frontend" /MIN powershell -NoExit -Command "python -m http.server 8080"

timeout /t 2 /nobreak >nul

echo.
echo ============================================
echo  SUCCESS! Servers are running
echo ============================================
echo.
echo  Frontend: http://localhost:8080
echo  Backend API: http://localhost:5000
echo  Admin Panel: http://localhost:8080/admin/pages/login.html
echo.
echo  Admin Login:
echo    Username: admin
echo    Password: admin123
echo.
echo ============================================
echo  Press any key to open website...
echo ============================================
pause >nul

start http://localhost:8080

echo.
echo Servers are running in minimized windows.
echo Close those windows to stop the servers.
echo.
pause
