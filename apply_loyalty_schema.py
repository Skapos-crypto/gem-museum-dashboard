"""
Apply Loyalty Points Schema to Database
"""

import sqlite3

def apply_loyalty_schema():
    """Apply the loyalty points schema to the database"""
    
    # Read the schema file
    with open('database/loyalty_schema.sql', 'r') as f:
        schema_sql = f.read()
    
    # Connect to database
    conn = sqlite3.connect('visitor_feedback.db')
    cursor = conn.cursor()
    
    try:
        # Execute the schema
        cursor.executescript(schema_sql)
        conn.commit()
        print("✅ Loyalty points schema applied successfully!")
        
        # Verify tables were created
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name LIKE '%points%' OR name LIKE '%reward%' OR name LIKE '%referral%' OR name LIKE '%redemption%'
            ORDER BY name
        """)
        
        tables = cursor.fetchall()
        print(f"\n📊 Created {len(tables)} loyalty tables:")
        for table in tables:
            print(f"   - {table[0]}")
        
        # Check rewards catalog
        cursor.execute("SELECT COUNT(*) FROM rewards_catalog")
        reward_count = cursor.fetchone()[0]
        print(f"\n🎁 Loaded {reward_count} rewards into catalog")
        
        # Show reward categories
        cursor.execute("""
            SELECT reward_category, COUNT(*) as count 
            FROM rewards_catalog 
            GROUP BY reward_category
        """)
        
        print("\n📦 Rewards by category:")
        for row in cursor.fetchall():
            print(f"   - {row[0]}: {row[1]} rewards")
        
    except Exception as e:
        print(f"❌ Error applying schema: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    apply_loyalty_schema()
