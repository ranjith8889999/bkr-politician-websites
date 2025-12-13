#!/bin/bash
# Startup script for EasyPanel

echo "🚀 Starting BKR Backend API..."

# Create database if it doesn't exist
if [ ! -f "bkr_database.db" ]; then
    echo "📦 Creating database..."
    python migrate_data.py --sample
fi

# Start the application
echo "✅ Starting Gunicorn..."
exec gunicorn wsgi:app \
    --bind 0.0.0.0:${PORT:-5000} \
    --workers 2 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    --log-level info
