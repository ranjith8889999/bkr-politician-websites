"""
Database Models for BKR Politician Website
Defines the schema for all database tables
"""

import sqlite3
from datetime import datetime

def create_tables(conn):
    """Create all database tables"""
    cursor = conn.cursor()
    
    # Health Camps Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS health_camps (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            location TEXT NOT NULL,
            services TEXT,
            description TEXT,
            contact TEXT,
            status TEXT DEFAULT 'upcoming',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Complaints Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS complaints (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT,
            area TEXT,
            category TEXT NOT NULL,
            subject TEXT NOT NULL,
            message TEXT NOT NULL,
            address TEXT,
            status TEXT DEFAULT 'pending',
            date TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Feedback Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT,
            area TEXT,
            rating INTEGER NOT NULL CHECK(rating >= 1 AND rating <= 5),
            category TEXT,
            message TEXT NOT NULL,
            suggestions TEXT,
            date TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # News Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            summary TEXT,
            content TEXT NOT NULL,
            status TEXT DEFAULT 'published',
            date TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Gallery Table (for future use)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS gallery (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            image_url TEXT NOT NULL,
            caption TEXT,
            category TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Admin Users Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admin_users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
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
