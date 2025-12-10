"""
Test and Demonstrate Loyalty Points System
"""

from loyalty_engine import LoyaltyPointsEngine
import json

def test_loyalty_system():
    """Demonstrate the loyalty points system"""
    
    engine = LoyaltyPointsEngine()
    
    print("=" * 70)
    print("🎮 GEM MUSEUM LOYALTY POINTS SYSTEM - DEMONSTRATION")
    print("=" * 70)
    
    # Test User ID (using first user from database)
    test_user_id = 1
    
    # 1. Initialize user points
    print("\n1️⃣ INITIALIZING USER POINTS")
    print("-" * 70)
    engine.initialize_user_points(test_user_id)
    print(f"✅ User {test_user_id} enrolled in loyalty program")
    
    # 2. Award points for surveys
    print("\n2️⃣ AWARDING POINTS FOR SURVEYS")
    print("-" * 70)
    
    surveys = [
        ("survey_overall_experience", 1),
        ("survey_service_operations", 1),
        ("survey_tour_educational", 1)
    ]
    
    for survey_type, survey_id in surveys:
        result = engine.award_survey_points(test_user_id, survey_type, survey_id)
        if result['success']:
            print(f"✅ {survey_type}: +{result['points_awarded']} points → Balance: {result['new_balance']}")
    
    # 3. Award referral points
    print("\n3️⃣ AWARDING REFERRAL POINTS")
    print("-" * 70)
    result = engine.award_referral_points(test_user_id, 2, referral_code="FRIEND2024")
    if result['success']:
        print(f"✅ Referral completed: +{result['points_awarded']} points → Balance: {result['new_balance']}")
    
    # 4. Get user summary
    print("\n4️⃣ USER POINTS SUMMARY")
    print("-" * 70)
    summary = engine.get_user_points_summary(test_user_id)
    if summary['success']:
        points = summary['points_data']
        print(f"💰 Current Balance: {points['current_points_balance']} points")
        print(f"📊 Total Earned: {points['total_points_earned']} points")
        print(f"💸 Total Spent: {points['total_points_spent']} points")
        print(f"📝 Surveys Completed: {points['surveys_completed']}")
        print(f"👥 Referrals Completed: {points['referrals_completed']}")
        print(f"   - From Surveys: {points['points_from_surveys']} points")
        print(f"   - From Referrals: {points['points_from_referrals']} points")
    
    # 5. Show available rewards
    print("\n5️⃣ AVAILABLE REWARDS")
    print("-" * 70)
    rewards = engine.get_available_rewards(test_user_id)
    if rewards['success']:
        print(f"User Balance: {rewards['user_balance']} points\n")
        
        affordable = [r for r in rewards['available_rewards'] if r['can_afford']]
        not_affordable = [r for r in rewards['available_rewards'] if not r['can_afford']]
        
        print(f"✅ CAN AFFORD ({len(affordable)} rewards):")
        for reward in affordable:
            print(f"   🎁 {reward['reward_name']} ({reward['category']})")
            print(f"      Cost: {reward['points_required']} points | {reward['description']}")
        
        print(f"\n❌ CANNOT AFFORD YET ({len(not_affordable)} rewards):")
        for reward in not_affordable[:5]:  # Show first 5
            print(f"   🔒 {reward['reward_name']} ({reward['category']})")
            print(f"      Cost: {reward['points_required']} points | Need {reward['points_needed']} more points")
    
    # 6. Redeem a reward
    print("\n6️⃣ REDEEMING REWARD")
    print("-" * 70)
    result = engine.redeem_reward(test_user_id, "Explorer Badge")
    if result['success']:
        print(f"✅ Redeemed: {result['reward_name']}")
        print(f"   Cost: {result['points_spent']} points")
        print(f"   New Balance: {result['new_balance']} points")
    
    # 7. Show recent activity
    print("\n7️⃣ RECENT ACTIVITY")
    print("-" * 70)
    summary = engine.get_user_points_summary(test_user_id)
    if summary['success']:
        print("📜 Transaction History:")
        for activity in summary['recent_activity'][:5]:
            points_str = f"+{activity['points']}" if activity['points'] > 0 else str(activity['points'])
            print(f"   {activity['type']}: {points_str} points - {activity['description']}")
            print(f"      Date: {activity['date']}")
    
    # 8. Show analytics
    print("\n8️⃣ LOYALTY PROGRAM ANALYTICS")
    print("-" * 70)
    analytics = engine.get_loyalty_analytics()
    if analytics['success']:
        stats = analytics['analytics_summary']
        print(f"👥 Total Users Enrolled: {stats['total_users_enrolled']}")
        print(f"💰 Total Points Distributed: {stats['total_points_distributed']}")
        print(f"💸 Total Points Redeemed: {stats['total_points_redeemed']}")
        print(f"📊 Average Points Per User: {stats['avg_points_per_user']}")
        print(f"🎯 Total Redemptions: {stats['total_redemptions']}")
        print(f"📈 Redemption Rate: {stats['redemption_rate_percent']}%")
        print(f"\n🏆 Badge Progress:")
        print(f"   - Explorer (20+ points): {stats['users_reached_explorer']} users")
        print(f"   - Guardian (60+ points): {stats['users_reached_guardian']} users")
        print(f"   - Legend (120+ points): {stats['users_reached_legend']} users")
    
    # 9. Frontend JSON Output
    print("\n9️⃣ FRONTEND JSON OUTPUT")
    print("-" * 70)
    frontend_data = engine.get_user_frontend_data(test_user_id)
    print(frontend_data)
    
    print("\n" + "=" * 70)
    print("✅ LOYALTY SYSTEM DEMONSTRATION COMPLETE")
    print("=" * 70)

if __name__ == "__main__":
    test_loyalty_system()
