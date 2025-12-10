"""
Populate Loyalty System with Realistic Data
Generates points, referrals, redemptions, and profile completions for all 400 users
"""

import sqlite3
import random
from datetime import datetime, timedelta
from loyalty_engine import LoyaltyPointsEngine

def populate_loyalty_data():
    """Generate realistic loyalty data for all users"""
    
    print("=" * 80)
    print("🎮 POPULATING LOYALTY SYSTEM WITH REALISTIC DATA")
    print("=" * 80)
    
    conn = sqlite3.connect('visitor_feedback.db')
    cursor = conn.cursor()
    engine = LoyaltyPointsEngine()
    
    # Get all users
    cursor.execute("SELECT user_id FROM users ORDER BY user_id")
    all_users = [row[0] for row in cursor.fetchall()]
    total_users = len(all_users)
    
    print(f"\n📊 Found {total_users} users to process")
    
    # Statistics
    stats = {
        'profiles_completed': 0,
        'surveys_awarded': 0,
        'referrals_made': 0,
        'redemptions': 0,
        'total_points_distributed': 0
    }
    
    # Get existing survey data
    cursor.execute("""
        SELECT user_id, COUNT(*) as survey_count
        FROM (
            SELECT user_id FROM survey_overall_experience
            UNION ALL SELECT user_id FROM survey_service_operations
            UNION ALL SELECT user_id FROM survey_tour_educational
            UNION ALL SELECT user_id FROM survey_facilities_spending
            UNION ALL SELECT user_id FROM survey_marketing_loyalty
            UNION ALL SELECT user_id FROM survey_immersive_experience
            UNION ALL SELECT user_id FROM survey_childrens_museum
        ) surveys
        GROUP BY user_id
    """)
    
    user_survey_counts = {row[0]: row[1] for row in cursor.fetchall()}
    
    print(f"\n1️⃣ AWARDING POINTS FOR EXISTING SURVEYS")
    print("-" * 80)
    
    # Award points for existing surveys
    for user_id in all_users:
        survey_count = user_survey_counts.get(user_id, 0)
        if survey_count > 0:
            # Initialize user points
            engine.initialize_user_points(user_id)
            
            # Award 20 points per survey
            for i in range(survey_count):
                result = engine.award_survey_points(user_id, f"survey_type_{i}", i)
                if result['success']:
                    stats['surveys_awarded'] += 1
                    stats['total_points_distributed'] += 20
    
    print(f"✅ Awarded points for {stats['surveys_awarded']} survey completions")
    
    # Profile completion (70% of users complete their profile)
    print(f"\n2️⃣ AWARDING PROFILE COMPLETION BONUSES")
    print("-" * 80)
    
    profile_completion_rate = 0.70
    users_to_complete_profile = random.sample(all_users, int(total_users * profile_completion_rate))
    
    for user_id in users_to_complete_profile:
        result = engine.award_profile_completion_points(user_id)
        if result['success']:
            stats['profiles_completed'] += 1
            stats['total_points_distributed'] += 40
    
    print(f"✅ {stats['profiles_completed']} users completed their profiles (40 points each)")
    
    # Referrals (20% of users made successful referrals)
    print(f"\n3️⃣ CREATING REFERRAL BONUSES")
    print("-" * 80)
    
    referral_rate = 0.20
    num_referrers = int(total_users * referral_rate)
    potential_referrers = [u for u in all_users if u <= total_users - 10]  # Leave room for referred users
    
    if len(potential_referrers) >= num_referrers:
        referrers = random.sample(potential_referrers, num_referrers)
        
        for referrer_id in referrers:
            # Each referrer brings 1-2 friends
            num_referrals = random.randint(1, 2)
            
            for _ in range(num_referrals):
                # Find a user who could be referred (random user different from referrer)
                possible_referred = [u for u in all_users if u != referrer_id]
                referred_id = random.choice(possible_referred)
                
                result = engine.award_referral_points(referrer_id, referred_id, f"REF{referrer_id}{referred_id}")
                if result['success']:
                    stats['referrals_made'] += 1
                    stats['total_points_distributed'] += 30
    
    print(f"✅ {stats['referrals_made']} successful referrals created (30 points each)")
    
    # Redemptions (40% of users with points redeem rewards)
    print(f"\n4️⃣ PROCESSING REWARD REDEMPTIONS")
    print("-" * 80)
    
    # Get users with points
    cursor.execute("SELECT user_id, current_points_balance FROM user_points WHERE current_points_balance >= 20")
    users_with_points = cursor.fetchall()
    
    redemption_rate = 0.40
    num_redeemers = int(len(users_with_points) * redemption_rate)
    redeemers = random.sample(users_with_points, min(num_redeemers, len(users_with_points)))
    
    # Reward distribution preferences (realistic)
    reward_preferences = [
        ("Explorer Badge", 0.35),           # Most popular - lowest cost
        ("Sticker Sheet", 0.20),
        ("Premium Raffle Ticket", 0.15),
        ("Postcard", 0.10),
        ("Guardian Badge", 0.08),
        ("Mini Papyrus Bookmark", 0.05),
        ("Sticker + Postcard Bundle", 0.03),
        ("Keychain", 0.02),
        ("Free Coffee With Meal", 0.01),
        ("Legend Badge", 0.01)
    ]
    
    for user_id, balance in redeemers:
        # Determine how many redemptions (1-3 based on balance)
        if balance >= 200:
            num_redemptions = random.randint(2, 4)
        elif balance >= 100:
            num_redemptions = random.randint(1, 3)
        elif balance >= 50:
            num_redemptions = random.randint(1, 2)
        else:
            num_redemptions = 1
        
        for _ in range(num_redemptions):
            # Get current balance
            cursor.execute("SELECT current_points_balance FROM user_points WHERE user_id = ?", (user_id,))
            current_balance = cursor.fetchone()
            if not current_balance:
                break
            current_balance = current_balance[0]
            
            # Choose affordable reward based on preferences
            affordable_rewards = [
                (name, prob) for name, prob in reward_preferences
                if engine.get_available_rewards(user_id).get('success') and
                any(r['reward_name'] == name and r['can_afford'] 
                    for r in engine.get_available_rewards(user_id).get('available_rewards', []))
            ]
            
            if not affordable_rewards:
                break
            
            # Weighted random choice
            rewards, weights = zip(*affordable_rewards)
            chosen_reward = random.choices(rewards, weights=weights, k=1)[0]
            
            result = engine.redeem_reward(user_id, chosen_reward)
            if result['success']:
                stats['redemptions'] += 1
    
    print(f"✅ {stats['redemptions']} reward redemptions processed")
    
    conn.close()
    
    # Final statistics
    print(f"\n" + "=" * 80)
    print("📊 FINAL STATISTICS")
    print("=" * 80)
    print(f"👥 Total Users: {total_users}")
    print(f"📝 Survey Points Awarded: {stats['surveys_awarded']} × 20 = {stats['surveys_awarded'] * 20} points")
    print(f"✅ Profiles Completed: {stats['profiles_completed']} × 40 = {stats['profiles_completed'] * 40} points")
    print(f"👥 Successful Referrals: {stats['referrals_made']} × 30 = {stats['referrals_made'] * 30} points")
    print(f"💰 Total Points Distributed: {stats['total_points_distributed']} points")
    print(f"🎁 Total Redemptions: {stats['redemptions']}")
    
    # Get final analytics
    print(f"\n📈 SYSTEM ANALYTICS")
    print("-" * 80)
    analytics = engine.get_loyalty_analytics()
    if analytics['success']:
        a = analytics['analytics_summary']
        print(f"Users Enrolled: {a['total_users_enrolled']}")
        print(f"Users with Points: {a['users_with_points']}")
        print(f"Average Points per User: {a['avg_points_per_user']:.2f}")
        print(f"Redemption Rate: {a['redemption_rate_percent']:.2f}%")
        print(f"\n🏆 Badge Progress:")
        print(f"   Explorer (20+ pts): {a['users_reached_explorer']} users")
        print(f"   Guardian (60+ pts): {a['users_reached_guardian']} users")
        print(f"   Legend (120+ pts): {a['users_reached_legend']} users")
        
        if a['most_redeemed_reward_all_time']:
            print(f"\n🎁 Most Popular Reward: {a['most_redeemed_reward_all_time']}")
    
    print(f"\n" + "=" * 80)
    print("✅ LOYALTY DATA POPULATION COMPLETE")
    print("=" * 80)

if __name__ == "__main__":
    populate_loyalty_data()
