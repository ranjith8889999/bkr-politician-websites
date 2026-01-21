"""
Migration Script: Add image_url column to news table
Run this script to update your database with the new column
"""

import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')

def migrate_database():
    """Add image_url column to news table if it doesn't exist"""
    try:
        # Connect to database
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = conn.cursor()
        
        print("🔍 Checking if migration is needed...")
        
        # Check if image_url column exists
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='news' AND column_name='image_url'
        """)
        
        if cursor.fetchone():
            print("✅ Column 'image_url' already exists in news table. No migration needed.")
        else:
            print("📝 Adding image_url column to news table...")
            
            # Add image_url column
            cursor.execute("""
                ALTER TABLE news 
                ADD COLUMN image_url VARCHAR(500)
            """)
            
            conn.commit()
            print("✅ Successfully added image_url column to news table!")
        
        # Verify the column exists
        cursor.execute("""
            SELECT column_name, data_type, character_maximum_length
            FROM information_schema.columns 
            WHERE table_name='news'
            ORDER BY ordinal_position
        """)
        
        print("\n📋 Current news table structure:")
        print("-" * 60)
        for row in cursor.fetchall():
            col_name, data_type, max_length = row
            length_info = f"({max_length})" if max_length else ""
            print(f"  {col_name:20} {data_type}{length_info}")
        print("-" * 60)
        
        cursor.close()
        conn.close()
        print("\n✅ Migration completed successfully!")
        
    except Exception as e:
        print(f"❌ Error during migration: {e}")
        raise

if __name__ == '__main__':
    print("=" * 60)
    print("DATABASE MIGRATION: Add image_url to news table")
    print("=" * 60)
    migrate_database()
