@echo off
REM BKR Website - Start Both Frontend and Backend Servers

echo ============================================================
echo  BKR Politician Website - Starting Servers
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.7+ from https://www.python.org/
    pause
    exit /b 1
)

echo [1/4] Checking backend dependencies...
cd backend
pip show flask >nul 2>&1
if errorlevel 1 (
    echo [INFO] Installing backend dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [ERROR] Failed to install dependencies
        pause
        exit /b 1
    )
)

echo [2/4] Checking database...
if not exist bkr_database.db (
    echo [INFO] Database not found. Creating sample data...
    python migrate_data.py --sample
)

echo [3/4] Starting Flask API Server (Port 5000)...
start "BKR API Server" cmd /k "python app.py"

cd ..

echo [4/4] Starting Frontend Server (Port 8080)...
timeout /t 2 /nobreak >nul
start "BKR Frontend" cmd /k "python -m http.server 8080"

echo.
echo ============================================================
echo  Servers Started Successfully!
echo ============================================================
echo.
echo  Frontend:  http://localhost:8080
echo  API:       http://localhost:5000
echo  Admin:     http://localhost:8080/admin/pages/login.html
echo.
echo  Username:  admin
echo  Password:  admin123
echo.
echo ============================================================
echo  Press any key to open the website in your browser...
pause >nul

start http://localhost:8080

echo.
echo To stop the servers, close both command windows.
echo.
pause
