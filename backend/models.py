"""
Database Models for BKR Politician Website
Defines the schema for all database tables
"""

import psycopg2
from datetime import datetime

def create_tables(conn):
    """Create all database tables"""
    cursor = conn.cursor()
    
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
    
    # News Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS news (
            id SERIAL PRIMARY KEY,
            title VARCHAR(500) NOT NULL,
            category VARCHAR(100) NOT NULL,
            summary TEXT,
            content TEXT NOT NULL,
            image_url VARCHAR(500),
            status VARCHAR(50) DEFAULT 'published',
            date DATE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Settings Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS settings (
            id SERIAL PRIMARY KEY,
            setting_key VARCHAR(100) UNIQUE NOT NULL,
            setting_value TEXT,
            description TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Skills for Youth Registration Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS skills_registrations (
            id SERIAL PRIMARY KEY,
            name VARCHAR(200) NOT NULL,
            phone VARCHAR(20) NOT NULL,
            email VARCHAR(200) NOT NULL,
            dob DATE NOT NULL,
            education VARCHAR(100) NOT NULL,
            institution VARCHAR(300),
            location VARCHAR(200) NOT NULL,
            city VARCHAR(100) NOT NULL,
            motivation TEXT,
            status VARCHAR(50) DEFAULT 'pending',
            date DATE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Insert default settings if they don't exist
    cursor.execute('''
        INSERT INTO settings (setting_key, setting_value, description)
        VALUES 
            ('chat_page_enabled', 'true', 'Enable/disable the AI chat page'),
            ('show_news', 'true', 'Show news section on homepage'),
            ('show_health_camps', 'true', 'Show health camps section on homepage'),
            ('email_notifications', 'true', 'Enable email notifications for complaints and feedback')
        ON CONFLICT (setting_key) DO NOTHING
    ''')
    
    # Gallery Table (for future use)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS gallery (
            id SERIAL PRIMARY KEY,
            image_url VARCHAR(500) NOT NULL,
            caption TEXT,
            category VARCHAR(100),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Admin Users Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admin_users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(100) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Chat Conversations Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat_conversations (
            id SERIAL PRIMARY KEY,
            session_id VARCHAR(100) UNIQUE NOT NULL,
            user_ip VARCHAR(50),
            user_agent TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Chat Messages Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat_messages (
            id SERIAL PRIMARY KEY,
            session_id VARCHAR(100) NOT NULL,
            role VARCHAR(20) NOT NULL CHECK(role IN ('user', 'assistant', 'system')),
            content TEXT NOT NULL,
            tokens_used INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (session_id) REFERENCES chat_conversations(session_id) ON DELETE CASCADE
        )
    ''')
    
    # Create indexes for better query performance
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_chat_messages_session ON chat_messages(session_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_chat_messages_created ON chat_messages(created_at)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_chat_conversations_created ON chat_conversations(created_at)')
    
    conn.commit()
    print("✓ All database tables created successfully")

def get_table_schema(table_name):
    """Get the schema information for a table"""
    schemas = {
        'health_camps': {
            'columns': ['id', 'title', 'date', 'time', 'location', 'services', 
                       'description', 'contact', 'status', 'created_at', 'updated_at'],
            'required': ['title', 'date', 'time', 'location']
        },
        'complaints': {
            'columns': ['id', 'name', 'phone', 'email', 'area', 'category', 
                       'subject', 'message', 'address', 'status', 'date', 'created_at', 'updated_at'],
            'required': ['name', 'phone', 'category', 'subject', 'message', 'date']
        },
        'feedback': {
            'columns': ['id', 'name', 'phone', 'email', 'area', 'rating', 
                       'category', 'message', 'suggestions', 'date', 'created_at'],
            'required': ['name', 'phone', 'rating', 'message', 'date']
        },
        'news': {
            'columns': ['id', 'title', 'category', 'summary', 'content', 
                       'image_url', 'status', 'date', 'created_at', 'updated_at'],
            'required': ['title', 'category', 'content', 'date']
        }
    }
    return schemas.get(table_name, {})
