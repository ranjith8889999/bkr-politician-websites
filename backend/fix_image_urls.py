"""
Fix image URLs - Remove leading slashes
"""

import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')

def fix_image_urls():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = conn.cursor()
        
        print("🔍 Checking for image URLs with leading slashes...")
        
        # Find news with leading slash in image_url
        cursor.execute("""
            SELECT id, title, image_url 
            FROM news 
            WHERE image_url LIKE '/%'
        """)
        
        news_to_fix = cursor.fetchall()
        
        if news_to_fix:
            print(f"Found {len(news_to_fix)} news article(s) to fix:")
            
            for id, title, image_url in news_to_fix:
                # Remove leading slash
                new_url = image_url.lstrip('/')
                
                print(f"\n  ID {id}: {title}")
                print(f"    Old: {image_url}")
                print(f"    New: {new_url}")
                
                # Update the database
                cursor.execute("""
                    UPDATE news 
                    SET image_url = %s 
                    WHERE id = %s
                """, (new_url, id))
            
            conn.commit()
            print(f"\n✅ Fixed {len(news_to_fix)} image URL(s)!")
        else:
            print("✅ No image URLs need fixing.")
        
        # Show final state
        cursor.execute("SELECT id, title, image_url FROM news")
        all_news = cursor.fetchall()
        
        print("\n" + "="*60)
        print("CURRENT STATE:")
        print("="*60)
        for id, title, image_url in all_news:
            print(f"ID {id}: {image_url or 'No image'}")
        print("="*60)
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    print("="*60)
    print("FIX IMAGE URLs - Remove Leading Slashes")
    print("="*60)
    fix_image_urls()
