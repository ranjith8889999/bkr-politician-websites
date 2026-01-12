"""
Database Connection and Query Functions
Handles all database operations for the BKR website
"""

import psycopg2
import psycopg2.extras
import os
from datetime import datetime
from models import create_tables

class Database:
    def __init__(self, host=None, port='5432', database=None, 
                 user=None, password=None):
        if not all([host, database, user, password]):
            raise ValueError('All database parameters are required')
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.init_database()
    
    def get_connection(self):
        """Get a database connection"""
        conn = psycopg2.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password
        )
        return conn
    
    def init_database(self):
        """Initialize the database with tables"""
        conn = self.get_connection()
        create_tables(conn)
        conn.close()
    
    # ==================== HEALTH CAMPS ====================
    
    def get_health_camps(self, status=None, limit=None, upcoming=None):
        """Get all health camps or filter by status/upcoming"""
        conn = self.get_connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        
        # Get today's date in YYYY-MM-DD format for comparison
        from datetime import date
        today = date.today().isoformat()
        
        if upcoming:
            # Filter for upcoming camps (date >= today)
            query = "SELECT * FROM health_camps WHERE date >= %s ORDER BY date ASC"
            cursor.execute(query, (today,))
        elif status:
            query = "SELECT * FROM health_camps WHERE status = %s ORDER BY date DESC"
            cursor.execute(query, (status,))
        else:
            # All camps sorted by date descending (newest/upcoming first)
            query = "SELECT * FROM health_camps ORDER BY date DESC"
            if limit:
                query += f" LIMIT {limit}"
            cursor.execute(query)
        
        camps = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return camps
    
    def get_health_camp_by_id(self, camp_id):
        """Get a single health camp by ID"""
        conn = self.get_connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute("SELECT * FROM health_camps WHERE id = %s", (camp_id,))
        camp = cursor.fetchone()
        conn.close()
        return dict(camp) if camp else None
    
    def create_health_camp(self, data):
        """Create a new health camp"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = """
            INSERT INTO health_camps 
            (title, date, time, location, services, description, contact, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """
        
        cursor.execute(query, (
            data.get('title'),
            data.get('date'),
            data.get('time'),
            data.get('location'),
            data.get('services', ''),
            data.get('description', ''),
            data.get('contact', ''),
            data.get('status', 'upcoming')
        ))
        
        camp_id = cursor.fetchone()[0]
        conn.commit()
        conn.close()
        return camp_id
    
    def update_health_camp(self, camp_id, data):
        """Update an existing health camp"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = """
            UPDATE health_camps 
            SET title = %s, date = %s, time = %s, location = %s, 
                services = %s, description = %s, contact = %s, status = %s,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = %s
        """
        
        cursor.execute(query, (
            data.get('title'),
            data.get('date'),
            data.get('time'),
            data.get('location'),
            data.get('services', ''),
            data.get('description', ''),
            data.get('contact', ''),
            data.get('status', 'upcoming'),
            camp_id
        ))
        
        conn.commit()
        rows_affected = cursor.rowcount
        conn.close()
        return rows_affected > 0
    
    def delete_health_camp(self, camp_id):
        """Delete a health camp"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM health_camps WHERE id = %s", (camp_id,))
        conn.commit()
        rows_affected = cursor.rowcount
        conn.close()
        return rows_affected > 0
    
    # ==================== COMPLAINTS ====================
    
    def get_complaints(self, status=None, limit=None):
        """Get all complaints or filter by status"""
        conn = self.get_connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        
        if status:
            query = "SELECT * FROM complaints WHERE status = %s ORDER BY created_at DESC"
            cursor.execute(query, (status,))
        else:
            query = "SELECT * FROM complaints ORDER BY created_at DESC"
            if limit:
                query += f" LIMIT {limit}"
            cursor.execute(query)
        
        complaints = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return complaints
    
    def create_complaint(self, data):
        """Create a new complaint"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = """
            INSERT INTO complaints 
            (name, phone, email, area, category, subject, message, address, status, date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """
        
        cursor.execute(query, (
            data.get('name'),
            data.get('phone'),
            data.get('email', ''),
            data.get('area', ''),
            data.get('category'),
            data.get('subject'),
            data.get('message'),
            data.get('address', ''),
            data.get('status', 'pending'),
            data.get('date', datetime.now().strftime('%Y-%m-%d'))
        ))
        
        complaint_id = cursor.fetchone()[0]
        conn.commit()
        conn.close()
        return complaint_id
    
    def update_complaint_status(self, complaint_id, status):
        """Update complaint status"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = "UPDATE complaints SET status = %s, updated_at = CURRENT_TIMESTAMP WHERE id = %s"
        cursor.execute(query, (status, complaint_id))
        
        conn.commit()
        rows_affected = cursor.rowcount
        conn.close()
        return rows_affected > 0
    
    # ==================== FEEDBACK ====================
    
    def get_feedback(self, limit=None):
        """Get all feedback"""
        conn = self.get_connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        
        query = "SELECT * FROM feedback ORDER BY created_at DESC"
        if limit:
            query += f" LIMIT {limit}"
        cursor.execute(query)
        
        feedback = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return feedback
    
    def create_feedback(self, data):
        """Create new feedback"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = """
            INSERT INTO feedback 
            (name, phone, email, area, rating, category, message, suggestions, date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """
        
        cursor.execute(query, (
            data.get('name'),
            data.get('phone'),
            data.get('email', ''),
            data.get('area', ''),
            data.get('rating'),
            data.get('category', ''),
            data.get('message'),
            data.get('suggestions', ''),
            data.get('date', datetime.now().strftime('%Y-%m-%d'))
        ))
        
        feedback_id = cursor.fetchone()[0]
        conn.commit()
        conn.close()
        return feedback_id
    
    # ==================== NEWS ====================
    
    def get_news(self, status=None, limit=None):
        """Get all news or filter by status"""
        conn = self.get_connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        
        if status:
            query = "SELECT * FROM news WHERE status = %s ORDER BY date DESC"
            cursor.execute(query, (status,))
        else:
            query = "SELECT * FROM news ORDER BY date DESC"
            if limit:
                query += f" LIMIT {limit}"
            cursor.execute(query)
        
        news = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return news
    
    def create_news(self, data):
        """Create a new news article"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = """
            INSERT INTO news 
            (title, category, summary, content, status, date)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id
        """
        
        cursor.execute(query, (
            data.get('title'),
            data.get('category'),
            data.get('summary', ''),
            data.get('content'),
            data.get('status', 'published'),
            data.get('date', datetime.now().strftime('%Y-%m-%d'))
        ))
        
        news_id = cursor.fetchone()[0]
        conn.commit()
        conn.close()
        return news_id
    
    def update_news(self, news_id, data):
        """Update an existing news article"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = """
            UPDATE news 
            SET title = %s, category = %s, summary = %s, content = %s, status = %s,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = %s
        """
        
        cursor.execute(query, (
            data.get('title'),
            data.get('category'),
            data.get('summary', ''),
            data.get('content'),
            data.get('status', 'published'),
            news_id
        ))
        
        conn.commit()
        rows_affected = cursor.rowcount
        conn.close()
        return rows_affected > 0
    
    def delete_news(self, news_id):
        """Delete a news article"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM news WHERE id = %s", (news_id,))
        conn.commit()
        rows_affected = cursor.rowcount
        conn.close()
        return rows_affected > 0
    
    # ==================== STATS ====================
    
    def get_dashboard_stats(self):
        """Get statistics for dashboard"""
        conn = self.get_connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        
        stats = {}
        
        # Total health camps
        cursor.execute("SELECT COUNT(*) as count FROM health_camps")
        stats['total_camps'] = cursor.fetchone()['count']
        
        # Upcoming health camps
        cursor.execute("SELECT COUNT(*) as count FROM health_camps WHERE status = 'upcoming'")
        stats['upcoming_camps'] = cursor.fetchone()['count']
        
        # Total complaints
        cursor.execute("SELECT COUNT(*) as count FROM complaints")
        stats['total_complaints'] = cursor.fetchone()['count']
        
        # Pending complaints
        cursor.execute("SELECT COUNT(*) as count FROM complaints WHERE status = 'pending'")
        stats['pending_complaints'] = cursor.fetchone()['count']
        
        # Total feedback
        cursor.execute("SELECT COUNT(*) as count FROM feedback")
        stats['total_feedback'] = cursor.fetchone()['count']
        
        # Average rating
        cursor.execute("SELECT AVG(rating) as avg_rating FROM feedback")
        avg = cursor.fetchone()['avg_rating']
        stats['average_rating'] = round(float(avg), 1) if avg else 0
        
        # Total news
        cursor.execute("SELECT COUNT(*) as count FROM news WHERE status = 'published'")
        stats['total_news'] = cursor.fetchone()['count']
        
        conn.close()
        return stats
