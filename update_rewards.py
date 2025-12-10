import sqlite3

conn = sqlite3.connect('visitor_feedback.db')
cursor = conn.cursor()

# Update rewards
cursor.execute("UPDATE rewards_catalog SET reward_name = 'Discounted Coffee With Meal' WHERE reward_name = 'Free Coffee With Meal'")
cursor.execute("UPDATE rewards_catalog SET reward_name = 'Discounted Oriental Koshary With Meal', description = 'Discounted Traditional Egyptian Koshary dish with meal' WHERE reward_name = 'Free Oriental Koshary With Meal'")

conn.commit()

# Verify
cursor.execute("SELECT reward_name, reward_category, points_required FROM rewards_catalog ORDER BY points_required")
print("\n✅ Updated Rewards Catalog:")
print("-" * 70)
for row in cursor.fetchall():
    print(f"   {row[0]:<50} ({row[1]}, {row[2]} pts)")

conn.close()
