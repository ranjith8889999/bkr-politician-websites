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
            status VARCHAR(50) DEFAULT 'published',
            date DATE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
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
                       'status', 'date', 'created_at', 'updated_at'],
            'required': ['title', 'category', 'content', 'date']
        }
    }
    return schemas.get(table_name, {})
