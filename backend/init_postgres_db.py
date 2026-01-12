"""
PostgreSQL Database Initialization Script
Creates all necessary tables in the PostgreSQL database
Run this script once to set up the database schema
"""

import psycopg2
from psycopg2 import sql

# PostgreSQL connection parameters
DB_CONFIG = {
    'host': '72.60.101.93',
    'port': '5432',
    'database': 'bkr_db',
    'user': 'ranjith',
    'password': 'ranjith123'
}

def create_tables():
    """Create all database tables"""
    print("Connecting to PostgreSQL database...")
    
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        print("✓ Connected successfully!")
        print("\nCreating database tables...")
        
        # Health Camps Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS health_camps (
                id SERIAL PRIMARY KEY,
                title VARCHAR(500) NOT NULL,
                date DATE NOT NULL,
                time VARCHAR(50) NOT NULL,
                location VARCHAR(500) NOT NULL,
                services TEXT,
                description TEXT,
                contact VARCHAR(200),
                status VARCHAR(50) DEFAULT 'upcoming',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        print("✓ health_camps table created")
        
        # Complaints Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS complaints (
                id SERIAL PRIMARY KEY,
                name VARCHAR(200) NOT NULL,
                phone VARCHAR(20) NOT NULL,
                email VARCHAR(200),
                area VARCHAR(200),
                category VARCHAR(100) NOT NULL,
                subject VARCHAR(500) NOT NULL,
                message TEXT NOT NULL,
                address TEXT,
                status VARCHAR(50) DEFAULT 'pending',
                date DATE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        print("✓ complaints table created")
        
        # Feedback Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS feedback (
                id SERIAL PRIMARY KEY,
                name VARCHAR(200) NOT NULL,
                phone VARCHAR(20) NOT NULL,
                email VARCHAR(200),
                area VARCHAR(200),
                rating INTEGER NOT NULL CHECK(rating >= 1 AND rating <= 5),
                category VARCHAR(100),
                message TEXT NOT NULL,
                suggestions TEXT,
                date DATE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        print("✓ feedback table created")
        
        # News Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS news (
                id SERIAL PRIMARY KEY,
                title VARCHAR(500) NOT NULL,
                category VARCHAR(100) NOT NULL,
                summary TEXT,
                content TEXT NOT NULL,
                status VARCHAR(50) DEFAULT 'published',
                date DATE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        print("✓ news table created")
        
        # Gallery Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS gallery (
                id SERIAL PRIMARY KEY,
                image_url VARCHAR(500) NOT NULL,
                caption TEXT,
                category VARCHAR(100),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        print("✓ gallery table created")
        
        # Admin Users Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS admin_users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(100) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        print("✓ admin_users table created")
        
        # Commit changes
        conn.commit()
        
        # Verify tables
        print("\n" + "="*50)
        print("Verifying created tables...")
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name
        """)
        
        tables = cursor.fetchall()
        print(f"\nTotal tables created: {len(tables)}")
        for table in tables:
            print(f"  - {table[0]}")
        
        print("\n" + "="*50)
        print("✅ Database initialization completed successfully!")
        print("\nYou can now start the application using:")
        print("  cd backend")
        print("  python app.py")
        
        cursor.close()
        conn.close()
        
    except psycopg2.Error as e:
        print(f"\n❌ Database error: {e}")
        print(f"Error code: {e.pgcode}")
        print("\nPlease check:")
        print("  1. PostgreSQL server is running")
        print("  2. Database 'bkr_db' exists")
        print("  3. User 'ranjith' has proper permissions")
        print("  4. Connection details are correct")
        return False
    
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("="*50)
    print("BKR PostgreSQL Database Initialization")
    print("="*50)
    print(f"\nDatabase Configuration:")
    print(f"  Host: {DB_CONFIG['host']}")
    print(f"  Port: {DB_CONFIG['port']}")
    print(f"  Database: {DB_CONFIG['database']}")
    print(f"  User: {DB_CONFIG['user']}")
    print("\n" + "="*50 + "\n")
    
    create_tables()
