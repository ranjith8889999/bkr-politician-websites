#!/bin/bash
# Startup script for EasyPanel with persistent database support

echo "🚀 Starting BKR Backend API..."

# Create data directory for persistent storage
mkdir -p data
echo "📁 Data directory: $(pwd)/data"

# Set database path
DB_PATH="${DATABASE_PATH:-data/bkr_database.db}"
echo "💾 Database path: $DB_PATH"

# Create database if it doesn't exist
if [ ! -f "$DB_PATH" ]; then
    echo "📦 Database not found. Creating new database with sample data..."
    python migrate_data.py --sample
    # Move database to data directory if not already there
    if [ -f "bkr_database.db" ] && [ "$DB_PATH" != "bkr_database.db" ]; then
        mv bkr_database.db "$DB_PATH"
        echo "✅ Database moved to $DB_PATH"
    fi
else
    echo "✅ Using existing database at $DB_PATH"
fi

# Start the application
echo "🚀 Starting Gunicorn..."
exec gunicorn wsgi:app \
    --bind 0.0.0.0:${PORT:-5000} \
    --workers 2 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    --log-level info
