"""
Populate realistic redemption data for the loyalty system
Generates redemptions based on user points and reward tiers
"""

import sqlite3
import random
from datetime import datetime, timedelta

conn = sqlite3.connect('visitor_feedback.db')
cursor = conn.cursor()

print("🎁 Populating Redemption Data...")

# Get all rewards with their details
cursor.execute("SELECT reward_id, reward_name, points_required, reward_category FROM rewards_catalog ORDER BY points_required")
rewards = cursor.fetchall()

print(f"\n📋 Available Rewards:")
for reward in rewards:
    print(f"   {reward[1]} - {reward[2]} pts ({reward[3]})")

# Get users with their points
cursor.execute("""
    SELECT user_id, current_points_balance, total_points_earned 
    FROM user_points 
    WHERE total_points_earned >= 20
    ORDER BY total_points_earned DESC
""")
users_with_points = cursor.fetchall()

print(f"\n👥 Users eligible for redemptions: {len(users_with_points)}")

# Redemption strategy based on user engagement level
# - High earners (120+ pts): 70% chance to redeem, prefer higher tier rewards
# - Medium earners (60-119 pts): 50% chance to redeem, prefer medium tier rewards
# - Low earners (20-59 pts): 30% chance to redeem, prefer low tier rewards

redemptions = []
redemption_date_start = datetime(2024, 12, 1)
redemption_date_end = datetime(2025, 12, 9)

for user_id, balance, total_earned in users_with_points:
    # Determine redemption likelihood based on engagement
    if total_earned >= 120:
        redemption_chance = 0.70  # 70% for high earners (Legend)
        preferred_rewards = [r for r in rewards if r[2] >= 80]  # Higher tier rewards
    elif total_earned >= 60:
        redemption_chance = 0.50  # 50% for medium earners (Guardian)
        preferred_rewards = [r for r in rewards if 40 <= r[2] <= 100]  # Medium tier
    else:
        redemption_chance = 0.30  # 30% for low earners (Explorer)
        preferred_rewards = [r for r in rewards if r[2] <= 60]  # Low tier

    # Decide if user redeems
    if random.random() < redemption_chance:
        # Ensure they have enough balance
        affordable_rewards = [r for r in preferred_rewards if r[2] <= balance + total_earned]
        
        if affordable_rewards:
            # Some active users redeem multiple times
            num_redemptions = 1
            if total_earned >= 200:
                num_redemptions = random.choices([1, 2, 3], weights=[0.5, 0.3, 0.2])[0]
            elif total_earned >= 120:
                num_redemptions = random.choices([1, 2], weights=[0.7, 0.3])[0]
            
            # Track balance for multiple redemptions
            current_balance = balance
            actual_redeemed = 0
            
            for _ in range(num_redemptions):
                # Select reward based on affordability
                still_affordable = [r for r in affordable_rewards if r[2] <= current_balance + total_earned - actual_redeemed]
                if not still_affordable:
                    break
                
                reward = random.choice(still_affordable)
                reward_id, reward_name, points_required, category = reward
                
                # Generate realistic redemption date
                redemption_date = redemption_date_start + timedelta(
                    days=random.randint(0, (redemption_date_end - redemption_date_start).days)
                )
                
                redemptions.append({
                    'user_id': user_id,
                    'reward_id': reward_id,
                    'reward_name': reward_name,
                    'points_spent': points_required,
                    'category': category,
                    'redeemed_at': redemption_date.strftime('%Y-%m-%d %H:%M:%S')
                })
                
                actual_redeemed += points_required

print(f"\n✨ Generated {len(redemptions)} redemptions")

# Category breakdown
category_counts = {}
for red in redemptions:
    cat = red['category']
    category_counts[cat] = category_counts.get(cat, 0) + 1

print("\n📊 Redemptions by Category:")
for cat, count in sorted(category_counts.items(), key=lambda x: x[1], reverse=True):
    print(f"   {cat}: {count}")

# Insert redemptions into database
print("\n💾 Inserting redemptions into database...")
for red in redemptions:
    # Get current balance before redemption
    cursor.execute("SELECT current_points_balance FROM user_points WHERE user_id = ?", (red['user_id'],))
    current_balance = cursor.fetchone()[0]
    remaining_balance = current_balance - red['points_spent']
    
    cursor.execute("""
        INSERT INTO redemption_history (user_id, reward_id, reward_name, reward_category, points_spent, remaining_balance, redemption_status, redeemed_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (red['user_id'], red['reward_id'], red['reward_name'], red['category'], red['points_spent'], remaining_balance, 'COMPLETED', red['redeemed_at']))

# Update user_points balances
print("🔄 Updating user point balances...")
cursor.execute("""
    UPDATE user_points 
    SET current_points_balance = total_points_earned - COALESCE((
        SELECT SUM(points_spent) 
        FROM redemption_history 
        WHERE redemption_history.user_id = user_points.user_id
    ), 0)
""")

# Create transactions for redemptions
print("📝 Creating transaction records...")
for red in redemptions:
    # Get current balance after all redemptions
    cursor.execute("""
        SELECT current_points_balance FROM user_points WHERE user_id = ?
    """, (red['user_id'],))
    balance_after = cursor.fetchone()[0]
    
    cursor.execute("""
        INSERT INTO points_transactions (user_id, transaction_type, points_change, balance_after, description, created_at)
        VALUES (?, 'REDEMPTION', ?, ?, ?, ?)
    """, (red['user_id'], -red['points_spent'], balance_after, f"Redeemed: {red['reward_name']}", red['redeemed_at']))

conn.commit()

# Final statistics
print("\n" + "="*50)
print("📈 FINAL STATISTICS")
print("="*50)

cursor.execute("SELECT COUNT(DISTINCT user_id) FROM redemption_history")
users_who_redeemed = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM redemption_history")
total_redemptions = cursor.fetchone()[0]

cursor.execute("SELECT SUM(points_spent) FROM redemption_history")
total_points_spent = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM user_points WHERE current_points_balance > 0")
users_with_balance = cursor.fetchone()[0]

cursor.execute("SELECT SUM(current_points_balance) FROM user_points")
total_balance_remaining = cursor.fetchone()[0]

redemption_rate = (users_who_redeemed / 400) * 100 if users_who_redeemed else 0

print(f"\n✅ Total Redemptions: {total_redemptions}")
print(f"✅ Users Who Redeemed: {users_who_redeemed}/400 ({redemption_rate:.1f}%)")
print(f"✅ Total Points Spent: {total_points_spent:,}")
print(f"✅ Points Still in Circulation: {total_balance_remaining:,}")
print(f"✅ Avg Redemptions per User: {total_redemptions/users_who_redeemed:.1f}")

# Most popular rewards
print("\n🏆 Most Popular Rewards:")
cursor.execute("""
    SELECT r.reward_name, r.reward_category, COUNT(*) as times_redeemed, r.points_required
    FROM redemption_history rh
    JOIN rewards_catalog r ON rh.reward_id = r.reward_id
    GROUP BY rh.reward_id
    ORDER BY times_redeemed DESC
    LIMIT 5
""")
for row in cursor.fetchall():
    print(f"   {row[0]} ({row[1]}) - {row[2]} redemptions @ {row[3]} pts")

# Top redeemers
print("\n👑 Top 5 Redeemers:")
cursor.execute("""
    SELECT u.name, COUNT(*) as redemptions, SUM(rh.points_spent) as total_spent
    FROM redemption_history rh
    JOIN users u ON rh.user_id = u.user_id
    GROUP BY rh.user_id
    ORDER BY redemptions DESC, total_spent DESC
    LIMIT 5
""")
for row in cursor.fetchall():
    print(f"   {row[0]} - {row[1]} redemptions ({row[2]} points)")

print("\n✅ Redemption data populated successfully!")
print("🔄 Ready to export for Power BI")

conn.close()
