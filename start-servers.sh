#!/bin/bash
# BKR Website - Start Both Frontend and Backend Servers

echo "============================================================"
echo " BKR Politician Website - Starting Servers"
echo "============================================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is not installed"
    echo "Please install Python 3.7+ from https://www.python.org/"
    exit 1
fi

echo "[1/4] Checking backend dependencies..."
cd backend

if ! python3 -c "import flask" &> /dev/null; then
    echo "[INFO] Installing backend dependencies..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "[ERROR] Failed to install dependencies"
        exit 1
    fi
fi

echo "[2/4] Checking database..."
if [ ! -f "bkr_database.db" ]; then
    echo "[INFO] Database not found. Creating sample data..."
    python3 migrate_data.py --sample
fi

echo "[3/4] Starting Flask API Server (Port 5000)..."
python3 app.py &
API_PID=$!

cd ..

echo "[4/4] Starting Frontend Server (Port 8080)..."
sleep 2
python3 -m http.server 8080 &
FRONTEND_PID=$!

echo ""
echo "============================================================"
echo " Servers Started Successfully!"
echo "============================================================"
echo ""
echo "  Frontend:  http://localhost:8080"
echo "  API:       http://localhost:5000"
echo "  Admin:     http://localhost:8080/admin/pages/login.html"
echo ""
echo "  Username:  admin"
echo "  Password:  admin123"
echo ""
echo "============================================================"
echo "  Opening website in browser..."
echo ""

# Open browser
if command -v xdg-open &> /dev/null; then
    xdg-open http://localhost:8080
elif command -v open &> /dev/null; then
    open http://localhost:8080
fi

echo "Press Ctrl+C to stop all servers"
echo ""

# Wait for interrupt
trap "kill $API_PID $FRONTEND_PID 2>/dev/null; echo 'Servers stopped'; exit" INT
wait
