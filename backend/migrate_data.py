"""
Data Migration Script
Migrates data from localStorage backup to SQLite database
"""

import json
import sys
from database import Database
from datetime import datetime

def migrate_from_json(json_file_path):
    """Migrate data from a JSON backup file to the database"""
    
    print("=" * 60)
    print("📦 BKR Data Migration Tool")
    print("=" * 60)
    
    # Initialize database
    db = Database('bkr_database.db')
    print("✓ Database initialized")
    
    # Load JSON data
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            backup = json.load(f)
        print(f"✓ Loaded data from {json_file_path}")
    except FileNotFoundError:
        print(f"✗ Error: File '{json_file_path}' not found")
        return
    except json.JSONDecodeError:
        print(f"✗ Error: Invalid JSON format in '{json_file_path}'")
        return
    
    data = backup.get('data', {})
    
    # Migrate Health Camps
    print("\n📋 Migrating Health Camps...")
    health_camps = data.get('healthCamps', [])
    camps_count = 0
    for camp in health_camps:
        try:
            db.create_health_camp(camp)
            camps_count += 1
        except Exception as e:
            print(f"  ⚠ Warning: Failed to migrate camp '{camp.get('title')}': {e}")
    print(f"✓ Migrated {camps_count} health camps")
    
    # Migrate Complaints
    print("\n📝 Migrating Complaints...")
    complaints = data.get('complaints', [])
    complaints_count = 0
    for complaint in complaints:
        try:
            db.create_complaint(complaint)
            complaints_count += 1
        except Exception as e:
            print(f"  ⚠ Warning: Failed to migrate complaint: {e}")
    print(f"✓ Migrated {complaints_count} complaints")
    
    # Migrate Feedback
    print("\n⭐ Migrating Feedback...")
    feedback_list = data.get('feedback', [])
    feedback_count = 0
    for feedback in feedback_list:
        try:
            db.create_feedback(feedback)
            feedback_count += 1
        except Exception as e:
            print(f"  ⚠ Warning: Failed to migrate feedback: {e}")
    print(f"✓ Migrated {feedback_count} feedback entries")
    
    # Migrate News
    print("\n📰 Migrating News...")
    news_list = data.get('news', [])
    if not news_list:
        news_list = data.get('newsUpdates', [])
    news_count = 0
    for news in news_list:
        try:
            db.create_news(news)
            news_count += 1
        except Exception as e:
            print(f"  ⚠ Warning: Failed to migrate news '{news.get('title')}': {e}")
    print(f"✓ Migrated {news_count} news articles")
    
    # Summary
    print("\n" + "=" * 60)
    print("✅ Migration Complete!")
    print("=" * 60)
    print(f"Health Camps:  {camps_count}")
    print(f"Complaints:    {complaints_count}")
    print(f"Feedback:      {feedback_count}")
    print(f"News:          {news_count}")
    print(f"Total:         {camps_count + complaints_count + feedback_count + news_count}")
    print("=" * 60)

def create_sample_data():
    """Create sample data for testing"""
    
    print("=" * 60)
    print("🎨 Creating Sample Data")
    print("=" * 60)
    
    db = Database('bkr_database.db')
    
    # Sample Health Camps
    sample_camps = [
        {
            'title': 'Free Eye Check-up Camp',
            'date': '2025-12-20',
            'time': '9:00 AM - 5:00 PM',
            'location': 'Community Hall, Quthbullapur',
            'services': 'Eye Screening, Free Spectacles Distribution',
            'description': 'Free comprehensive eye check-up camp for all age groups',
            'contact': '+91-9XXXXXX363',
            'status': 'upcoming'
        },
        {
            'title': 'General Health Check-up Camp',
            'date': '2025-12-25',
            'time': '8:00 AM - 4:00 PM',
            'location': 'Municipal Office, Balanagar',
            'services': 'Blood Pressure, Diabetes Screening, General Consultation',
            'description': 'Free general health check-up for senior citizens',
            'contact': '+91-9XXXXXX363',
            'status': 'upcoming'
        },
        {
            'title': 'Dental Care Camp',
            'date': '2025-12-15',
            'time': '10:00 AM - 6:00 PM',
            'location': 'Government School, Quthbullapur',
            'services': 'Dental Check-up, Free Cleaning, Consultation',
            'description': 'Special dental care camp for children and adults',
            'contact': '+91-9XXXXXX363',
            'status': 'completed'
        }
    ]
    
    for camp in sample_camps:
        db.create_health_camp(camp)
    
    print(f"✓ Created {len(sample_camps)} sample health camps")
    
    # Sample News
    sample_news = [
        {
            'title': 'New Development Projects Announced',
            'category': 'Announcement',
            'summary': 'Major infrastructure projects to begin in Quthbullapur',
            'content': 'We are pleased to announce new development projects including road improvements, water supply enhancement, and new community centers.',
            'status': 'published',
            'date': '2025-12-10'
        },
        {
            'title': 'Health Camp Success - 5000+ Beneficiaries',
            'category': 'Event',
            'summary': 'Recent health camp sees overwhelming response',
            'content': 'Our recent mega health camp was a huge success with over 5000 citizens benefiting from free medical services.',
            'status': 'published',
            'date': '2025-12-08'
        }
    ]
    
    for news in sample_news:
        db.create_news(news)
    
    print(f"✓ Created {len(sample_news)} sample news articles")
    print("=" * 60)
    print("✅ Sample data created successfully!")
    print("=" * 60)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == '--sample':
            create_sample_data()
        else:
            migrate_from_json(sys.argv[1])
    else:
        print("\nUsage:")
        print("  python migrate_data.py <backup_file.json>  - Migrate from JSON backup")
        print("  python migrate_data.py --sample            - Create sample data")
        print("\nExample:")
        print("  python migrate_data.py bkr_backup_2025-12-12.json")
