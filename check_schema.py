import sqlite3
conn = sqlite3.connect('visitor_feedback.db')
cursor = conn.cursor()
cursor.execute('PRAGMA table_info(redemption_history)')
for col in cursor.fetchall():
    print(f"{col[1]} {col[2]} {'NOT NULL' if col[3] else ''}")
