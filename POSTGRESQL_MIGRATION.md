# PostgreSQL Migration Guide

## Overview
This document describes the migration from SQLite to PostgreSQL for the BKR application.

## Database Connection Details

**PostgreSQL Server:**
- Host: 72.60.101.93
- Port: 5432
- Database: bkr_db
- Username: ranjith
- Password: ranjith123

## Changes Made

### 1. Dependencies Updated
- Added `psycopg2-binary==2.9.9` to `requirements.txt` for PostgreSQL support
- Removed SQLite3 dependency (it was built-in)

### 2. Database Models (`models.py`)
- Replaced `INTEGER PRIMARY KEY AUTOINCREMENT` with `SERIAL PRIMARY KEY`
- Changed `TEXT` columns to appropriate `VARCHAR(n)` or `TEXT` types
- Updated `TEXT` date fields to `DATE` type
- Maintained all constraints and default values

### 3. Database Connection (`database.py`)
- Replaced `sqlite3` import with `psycopg2`
- Updated `Database` class constructor to accept PostgreSQL connection parameters
- Changed all SQL parameter placeholders from `?` to `%s` (PostgreSQL style)
- Updated `get_connection()` to use `psycopg2.connect()`
- Added `cursor_factory=psycopg2.extras.RealDictCursor` for dictionary-like row access
- Changed `cursor.lastrowid` to `RETURNING id` clause in INSERT statements

### 4. Application Configuration (`app.py`)
- Removed SQLite file path logic
- Added environment variables for PostgreSQL connection:
  - `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`
- Updated Database initialization to use new connection parameters

### 5. Environment Configuration (`.env.example`)
- Added PostgreSQL connection parameters
- Removed `DATABASE_PATH` variable

## Setup Instructions

### Step 1: Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### Step 2: Initialize Database

Run the initialization script to create all tables:

```bash
python init_postgres_db.py
```

This will:
- Connect to the PostgreSQL server
- Create all necessary tables
- Verify table creation
- Display success/error messages

### Step 3: Configure Environment (Optional)

If you need to use different database credentials, create a `.env` file:

```bash
cp .env.example .env
# Edit .env with your specific configuration
```

### Step 4: Start the Application

```bash
python app.py
# or
gunicorn -w 4 -b 0.0.0.0:8080 wsgi:app
```

## Database Tables Created

The following tables will be created in PostgreSQL:

1. **health_camps**
   - Stores health camp information
   - Fields: id, title, date, time, location, services, description, contact, status, created_at, updated_at

2. **complaints**
   - Stores citizen complaints
   - Fields: id, name, phone, email, area, category, subject, message, address, status, date, created_at, updated_at

3. **feedback**
   - Stores user feedback
   - Fields: id, name, phone, email, area, rating, category, message, suggestions, date, created_at

4. **news**
   - Stores news articles
   - Fields: id, title, category, summary, content, status, date, created_at, updated_at

5. **gallery**
   - Stores gallery images (for future use)
   - Fields: id, image_url, caption, category, created_at

6. **admin_users**
   - Stores admin user credentials
   - Fields: id, username, password, created_at

## Data Migration (Optional)

If you have existing SQLite data to migrate, you can use the following approach:

1. Export data from SQLite:
```python
import sqlite3
import json

conn = sqlite3.connect('bkr_database.db')
cursor = conn.cursor()

# Export each table
for table in ['health_camps', 'complaints', 'feedback', 'news']:
    cursor.execute(f"SELECT * FROM {table}")
    rows = cursor.fetchall()
    # Save to JSON or process as needed
```

2. Import data to PostgreSQL using the existing API endpoints or direct SQL

## Verification

After setup, verify the connection:

```bash
python -c "from database import Database; db = Database(); print('✓ Connection successful!')"
```

## Troubleshooting

### Connection Errors
- Verify PostgreSQL server is running on 72.60.101.93:5432
- Check firewall rules allow connections from your IP
- Verify database `bkr_db` exists
- Confirm user `ranjith` has proper permissions

### Permission Errors
```sql
-- Grant necessary permissions (run as PostgreSQL admin)
GRANT ALL PRIVILEGES ON DATABASE bkr_db TO ranjith;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO ranjith;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO ranjith;
```

### Module Not Found
```bash
pip install psycopg2-binary
```

## Rollback (If Needed)

To rollback to SQLite:
1. Restore the original files from git history
2. Run: `pip install -r requirements.txt`
3. The app will recreate SQLite database automatically

## Performance Notes

PostgreSQL advantages over SQLite:
- ✓ Better concurrent access handling
- ✓ More robust for production environments
- ✓ Better performance with larger datasets
- ✓ Advanced query optimization
- ✓ Full ACID compliance with better reliability
- ✓ Support for complex queries and joins

## Support

For issues or questions:
1. Check the PostgreSQL logs
2. Verify all environment variables are set correctly
3. Review the application logs for detailed error messages
