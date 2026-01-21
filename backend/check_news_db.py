"""
Quick Database Check - Verify news exists
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

def check_news():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = conn.cursor()
        
        # Check total news count
        cursor.execute("SELECT COUNT(*) FROM news")
        total = cursor.fetchone()[0]
        print(f"\n📊 Total news articles: {total}")
        
        # Check published news count
        cursor.execute("SELECT COUNT(*) FROM news WHERE status = 'published'")
        published = cursor.fetchone()[0]
        print(f"✅ Published news articles: {published}")
        
        # Show all news
        cursor.execute("""
            SELECT id, title, category, date, status, image_url 
            FROM news 
            ORDER BY date DESC
        """)
        
        news = cursor.fetchall()
        
        if news:
            print("\n" + "="*80)
            print("NEWS ARTICLES IN DATABASE:")
            print("="*80)
            for item in news:
                id, title, category, date, status, image_url = item
                status_icon = "✅" if status == 'published' else "📝"
                img_icon = "🖼️" if image_url else "❌"
                print(f"\n{status_icon} ID: {id}")
                print(f"   Title: {title}")
                print(f"   Category: {category}")
                print(f"   Date: {date}")
                print(f"   Status: {status}")
                print(f"   {img_icon} Image: {image_url or 'No image'}")
            print("="*80)
        else:
            print("\n⚠️ No news articles found in database!")
            print("Add some news in the admin panel first.")
        
        conn.close()
        
        return total, published
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return 0, 0

if __name__ == '__main__':
    print("="*80)
    print("DATABASE NEWS CHECK")
    print("="*80)
    total, published = check_news()
    
    print("\n" + "="*80)
    print("SUMMARY:")
    print("="*80)
    if total == 0:
        print("❌ No news found. Add news articles in admin panel.")
    elif published == 0:
        print("⚠️ News exists but none are published. Change status to 'published'.")
    else:
        print(f"✅ Database has {published} published news article(s).")
        print("✅ These should appear on the homepage.")
    print("="*80)
