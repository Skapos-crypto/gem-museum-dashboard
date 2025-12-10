"""
Database Manager for Visitor Feedback System
Handles all database operations and data pipeline
"""

import sqlite3
import pandas as pd
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import json


class DatabaseManager:
    def __init__(self, db_path: str = "visitor_feedback.db"):
        """Initialize database connection"""
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        
    def connect(self):
        """Establish database connection"""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row  # Return rows as dictionaries
        self.cursor = self.conn.cursor()
        
    def disconnect(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            
    def initialize_database(self):
        """Create all tables and views from schema"""
        self.connect()
        with open('database/schema.sql', 'r') as f:
            schema_sql = f.read()
            self.cursor.executescript(schema_sql)
        self.conn.commit()
        self.disconnect()
        
    # ==================== USER MANAGEMENT ====================
    
    def create_user(self, user_data: Dict) -> int:
        """
        Create a new user and return user_id
        
        Args:
            user_data: Dictionary containing email, name, nationality, age, language, gender
        
        Returns:
            user_id of the created user
        """
        self.connect()
        
        query = """
        INSERT INTO users (email, name, nationality, age, language, gender)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        
        try:
            self.cursor.execute(query, (
                user_data['email'],
                user_data['name'],
                user_data.get('nationality'),
                user_data.get('age'),
                user_data.get('language'),
                user_data.get('gender')
            ))
            self.conn.commit()
            user_id = self.cursor.lastrowid
            return user_id
        except sqlite3.IntegrityError:
            # User with this email already exists
            self.cursor.execute("SELECT user_id FROM users WHERE email = ?", (user_data['email'],))
            result = self.cursor.fetchone()
            return result[0]
        finally:
            self.disconnect()
    
    def get_user_by_email(self, email: str) -> Optional[Dict]:
        """Get user information by email"""
        self.connect()
        self.cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        result = self.cursor.fetchone()
        self.disconnect()
        return dict(result) if result else None
    
    # ==================== SURVEY SUBMISSIONS ====================
    
    def submit_general_experience(self, user_id: int, survey_data: Dict) -> int:
        """Submit general experience survey"""
        self.connect()
        
        query = """
        INSERT INTO survey_general_experience 
        (user_id, overall_satisfaction, would_recommend, ease_of_navigation, 
         staff_helpfulness, cleanliness_rating, additional_comments)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        
        self.cursor.execute(query, (
            user_id,
            survey_data.get('overall_satisfaction'),
            survey_data.get('would_recommend'),
            survey_data.get('ease_of_navigation'),
            survey_data.get('staff_helpfulness'),
            survey_data.get('cleanliness_rating'),
            survey_data.get('additional_comments')
        ))
        self.conn.commit()
        response_id = self.cursor.lastrowid
        self.disconnect()
        return response_id
    
    def submit_exhibition_feedback(self, user_id: int, survey_data: Dict) -> int:
        """Submit exhibition feedback survey"""
        self.connect()
        
        query = """
        INSERT INTO survey_exhibition_feedback 
        (user_id, content_quality, educational_value, interactive_elements, 
         favorite_exhibit, improvement_suggestions)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        
        self.cursor.execute(query, (
            user_id,
            survey_data.get('content_quality'),
            survey_data.get('educational_value'),
            survey_data.get('interactive_elements'),
            survey_data.get('favorite_exhibit'),
            survey_data.get('improvement_suggestions')
        ))
        self.conn.commit()
        response_id = self.cursor.lastrowid
        self.disconnect()
        return response_id
    
    def submit_facilities_survey(self, user_id: int, survey_data: Dict) -> int:
        """Submit facilities & amenities survey"""
        self.connect()
        
        query = """
        INSERT INTO survey_facilities 
        (user_id, parking_rating, restroom_cleanliness, cafe_restaurant_quality, 
         accessibility_rating, wifi_quality, facility_comments)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        
        self.cursor.execute(query, (
            user_id,
            survey_data.get('parking_rating'),
            survey_data.get('restroom_cleanliness'),
            survey_data.get('cafe_restaurant_quality'),
            survey_data.get('accessibility_rating'),
            survey_data.get('wifi_quality'),
            survey_data.get('facility_comments')
        ))
        self.conn.commit()
        response_id = self.cursor.lastrowid
        self.disconnect()
        return response_id
    
    def submit_digital_experience(self, user_id: int, survey_data: Dict) -> int:
        """Submit digital experience survey"""
        self.connect()
        
        query = """
        INSERT INTO survey_digital_experience 
        (user_id, mobile_app_rating, website_usability, online_booking_ease, 
         digital_guides_usefulness, digital_feedback)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        
        self.cursor.execute(query, (
            user_id,
            survey_data.get('mobile_app_rating'),
            survey_data.get('website_usability'),
            survey_data.get('online_booking_ease'),
            survey_data.get('digital_guides_usefulness'),
            survey_data.get('digital_feedback')
        ))
        self.conn.commit()
        response_id = self.cursor.lastrowid
        self.disconnect()
        return response_id
    
    # ==================== DATA RETRIEVAL FOR DASHBOARD ====================
    
    def get_consolidated_feedback(self) -> pd.DataFrame:
        """Get all feedback data in consolidated view"""
        self.connect()
        df = pd.read_sql_query("SELECT * FROM consolidated_feedback", self.conn)
        self.disconnect()
        return df
    
    def get_user_demographics(self) -> pd.DataFrame:
        """Get user demographics data"""
        self.connect()
        df = pd.read_sql_query("SELECT * FROM users", self.conn)
        self.disconnect()
        return df
    
    def get_survey_responses(self, survey_type: str) -> pd.DataFrame:
        """
        Get responses for a specific survey type
        
        Args:
            survey_type: One of 'general', 'exhibition', 'facilities', 'digital'
        """
        table_map = {
            'general': 'survey_general_experience',
            'exhibition': 'survey_exhibition_feedback',
            'facilities': 'survey_facilities',
            'digital': 'survey_digital_experience'
        }
        
        if survey_type not in table_map:
            raise ValueError(f"Invalid survey type. Choose from: {list(table_map.keys())}")
        
        self.connect()
        query = f"SELECT * FROM {table_map[survey_type]}"
        df = pd.read_sql_query(query, self.conn)
        self.disconnect()
        return df
    
    # ==================== ANALYTICS QUERIES ====================
    
    def get_response_statistics(self) -> Dict:
        """Get overall response statistics"""
        self.connect()
        
        stats = {}
        
        # Total users
        self.cursor.execute("SELECT COUNT(*) FROM users")
        stats['total_users'] = self.cursor.fetchone()[0]
        
        # Total responses by survey type
        for survey_type, table in [
            ('general_experience', 'survey_general_experience'),
            ('exhibition_feedback', 'survey_exhibition_feedback'),
            ('facilities', 'survey_facilities'),
            ('digital_experience', 'survey_digital_experience')
        ]:
            self.cursor.execute(f"SELECT COUNT(*) FROM {table}")
            stats[f'{survey_type}_responses'] = self.cursor.fetchone()[0]
        
        self.disconnect()
        return stats
    
    def get_average_ratings(self) -> Dict:
        """Get average ratings across all surveys"""
        self.connect()
        
        ratings = {}
        
        # General Experience averages
        self.cursor.execute("""
            SELECT 
                AVG(overall_satisfaction) as avg_satisfaction,
                AVG(would_recommend) as avg_recommend,
                AVG(ease_of_navigation) as avg_navigation,
                AVG(staff_helpfulness) as avg_staff,
                AVG(cleanliness_rating) as avg_cleanliness
            FROM survey_general_experience
        """)
        result = self.cursor.fetchone()
        if result:
            ratings['general_experience'] = {
                'overall_satisfaction': round(result[0], 2) if result[0] else 0,
                'would_recommend': round(result[1], 2) if result[1] else 0,
                'ease_of_navigation': round(result[2], 2) if result[2] else 0,
                'staff_helpfulness': round(result[3], 2) if result[3] else 0,
                'cleanliness_rating': round(result[4], 2) if result[4] else 0
            }
        
        self.disconnect()
        return ratings
    
    def get_demographics_breakdown(self) -> Dict:
        """Get breakdown of user demographics"""
        self.connect()
        
        breakdown = {}
        
        # Age distribution
        self.cursor.execute("""
            SELECT 
                CASE 
                    WHEN age < 18 THEN 'Under 18'
                    WHEN age BETWEEN 18 AND 25 THEN '18-25'
                    WHEN age BETWEEN 26 AND 35 THEN '26-35'
                    WHEN age BETWEEN 36 AND 50 THEN '36-50'
                    WHEN age > 50 THEN 'Over 50'
                    ELSE 'Unknown'
                END as age_group,
                COUNT(*) as count
            FROM users
            GROUP BY age_group
        """)
        breakdown['age_distribution'] = [dict(row) for row in self.cursor.fetchall()]
        
        # Nationality distribution
        self.cursor.execute("""
            SELECT nationality, COUNT(*) as count
            FROM users
            WHERE nationality IS NOT NULL
            GROUP BY nationality
            ORDER BY count DESC
            LIMIT 10
        """)
        breakdown['top_nationalities'] = [dict(row) for row in self.cursor.fetchall()]
        
        # Gender distribution
        self.cursor.execute("""
            SELECT gender, COUNT(*) as count
            FROM users
            WHERE gender IS NOT NULL
            GROUP BY gender
        """)
        breakdown['gender_distribution'] = [dict(row) for row in self.cursor.fetchall()]
        
        # Language distribution
        self.cursor.execute("""
            SELECT language, COUNT(*) as count
            FROM users
            WHERE language IS NOT NULL
            GROUP BY language
            ORDER BY count DESC
        """)
        breakdown['language_distribution'] = [dict(row) for row in self.cursor.fetchall()]
        
        self.disconnect()
        return breakdown
    
    # ==================== UTILITY METHODS ====================
    
    def export_to_csv(self, table_name: str, output_path: str):
        """Export any table to CSV"""
        self.connect()
        df = pd.read_sql_query(f"SELECT * FROM {table_name}", self.conn)
        df.to_csv(output_path, index=False)
        self.disconnect()
        
    def export_consolidated_to_excel(self, output_path: str):
        """Export all data to Excel with multiple sheets"""
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            # Get all data
            self.connect()
            
            # Users
            df_users = pd.read_sql_query("SELECT * FROM users", self.conn)
            df_users.to_excel(writer, sheet_name='Users', index=False)
            
            # Surveys
            df_general = pd.read_sql_query("SELECT * FROM survey_general_experience", self.conn)
            df_general.to_excel(writer, sheet_name='General Experience', index=False)
            
            df_exhibition = pd.read_sql_query("SELECT * FROM survey_exhibition_feedback", self.conn)
            df_exhibition.to_excel(writer, sheet_name='Exhibition Feedback', index=False)
            
            df_facilities = pd.read_sql_query("SELECT * FROM survey_facilities", self.conn)
            df_facilities.to_excel(writer, sheet_name='Facilities', index=False)
            
            df_digital = pd.read_sql_query("SELECT * FROM survey_digital_experience", self.conn)
            df_digital.to_excel(writer, sheet_name='Digital Experience', index=False)
            
            # Consolidated view
            df_consolidated = pd.read_sql_query("SELECT * FROM consolidated_feedback", self.conn)
            df_consolidated.to_excel(writer, sheet_name='Consolidated', index=False)
            
            self.disconnect()


# Example usage
if __name__ == "__main__":
    # Initialize database
    db = DatabaseManager()
    db.initialize_database()
    
    print("Database initialized successfully!")
    print("\nDatabase structure:")
    print("- users table (demographics)")
    print("- survey_general_experience table")
    print("- survey_exhibition_feedback table")
    print("- survey_facilities table")
    print("- survey_digital_experience table")
    print("- consolidated_feedback view (merges all data)")
