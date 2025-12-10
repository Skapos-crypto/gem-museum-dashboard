"""
Update user_points.total_points_spent from redemption_history
"""

import sqlite3

conn = sqlite3.connect('visitor_feedback.db')
cursor = conn.cursor()

print("🔄 Updating total_points_spent in user_points table...")

# Update total_points_spent for all users who have redemptions
cursor.execute("""
    UPDATE user_points
    SET total_points_spent = COALESCE((
        SELECT SUM(points_spent)
        FROM redemption_history
        WHERE redemption_history.user_id = user_points.user_id
    ), 0)
""")

conn.commit()

# Verify the update
cursor.execute("SELECT SUM(total_points_spent) FROM user_points")
total_spent = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM user_points WHERE total_points_spent > 0")
users_with_spending = cursor.fetchone()[0]

print(f"\n✅ Update Complete!")
print(f"   Total Points Spent: {total_spent:,}")
print(f"   Users with Spending: {users_with_spending}/400")

# Verify it matches redemption_history
cursor.execute("SELECT SUM(points_spent) FROM redemption_history")
redemption_total = cursor.fetchone()[0]

if total_spent == redemption_total:
    print(f"\n✅ Verification PASSED: Totals match ({total_spent:,} points)")
else:
    print(f"\n❌ Verification FAILED: user_points={total_spent}, redemption_history={redemption_total}")

conn.close()
