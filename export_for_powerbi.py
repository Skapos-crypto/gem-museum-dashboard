"""
Export Data for Power BI Visualization
Generates CSV files optimized for Power BI analysis
"""

import sqlite3
import pandas as pd
from datetime import datetime
import os

def export_for_powerbi():
    """Export all data to CSV files for Power BI"""
    
    print("=" * 80)
    print("📊 EXPORTING DATA FOR POWER BI")
    print("=" * 80)
    
    # Create powerbi_exports folder
    export_folder = "powerbi_exports"
    if not os.path.exists(export_folder):
        os.makedirs(export_folder)
    
    conn = sqlite3.connect('visitor_feedback.db')
    
    # 1. Users Table
    print("\n1️⃣ Exporting Users Data...")
    df_users = pd.read_sql_query("""
        SELECT 
            user_id,
            email,
            name,
            nationality,
            age,
            language,
            gender,
            created_at
        FROM users
        ORDER BY user_id
    """, conn)
    df_users.to_csv(f"{export_folder}/01_users.csv", index=False, encoding='utf-8-sig')
    print(f"   ✅ {len(df_users)} users exported")
    
    # 2. User Points & Loyalty Status
    print("\n2️⃣ Exporting User Points & Loyalty...")
    df_points = pd.read_sql_query("""
        SELECT 
            up.user_id,
            u.name,
            u.nationality,
            u.age,
            u.gender,
            up.total_points_earned,
            up.total_points_spent,
            up.current_points_balance,
            up.points_from_surveys,
            up.points_from_referrals,
            up.points_from_profile_completion,
            up.surveys_completed,
            up.referrals_completed,
            up.profile_completed,
            up.profile_completed_at,
            up.created_at as enrolled_at,
            up.updated_at as last_activity,
            CASE 
                WHEN up.total_points_earned >= 120 THEN 'Legend'
                WHEN up.total_points_earned >= 60 THEN 'Guardian'
                WHEN up.total_points_earned >= 20 THEN 'Explorer'
                ELSE 'None'
            END as badge_level
        FROM user_points up
        JOIN users u ON up.user_id = u.user_id
        ORDER BY up.total_points_earned DESC
    """, conn)
    df_points.to_csv(f"{export_folder}/02_user_points.csv", index=False, encoding='utf-8-sig')
    print(f"   ✅ {len(df_points)} loyalty members exported")
    
    # 3. Points Transactions (Activity Log)
    print("\n3️⃣ Exporting Points Transactions...")
    df_transactions = pd.read_sql_query("""
        SELECT 
            pt.transaction_id,
            pt.user_id,
            u.name as user_name,
            u.nationality,
            u.age,
            u.gender,
            pt.transaction_type,
            pt.points_change,
            pt.balance_after,
            pt.reference_type,
            pt.description,
            pt.created_at as transaction_date,
            date(pt.created_at) as date_only,
            strftime('%Y-%m', pt.created_at) as year_month,
            strftime('%Y', pt.created_at) as year,
            strftime('%m', pt.created_at) as month,
            CASE strftime('%w', pt.created_at)
                WHEN '0' THEN 'Sunday'
                WHEN '1' THEN 'Monday'
                WHEN '2' THEN 'Tuesday'
                WHEN '3' THEN 'Wednesday'
                WHEN '4' THEN 'Thursday'
                WHEN '5' THEN 'Friday'
                WHEN '6' THEN 'Saturday'
            END as day_of_week
        FROM points_transactions pt
        JOIN users u ON pt.user_id = u.user_id
        ORDER BY pt.created_at DESC
    """, conn)
    df_transactions.to_csv(f"{export_folder}/03_points_transactions.csv", index=False, encoding='utf-8-sig')
    print(f"   ✅ {len(df_transactions)} transactions exported")
    
    # 4. Rewards Catalog
    print("\n4️⃣ Exporting Rewards Catalog...")
    df_rewards = pd.read_sql_query("""
        SELECT 
            reward_id,
            reward_name,
            reward_category,
            points_required,
            description,
            is_active
        FROM rewards_catalog
        ORDER BY points_required, reward_name
    """, conn)
    df_rewards.to_csv(f"{export_folder}/04_rewards_catalog.csv", index=False, encoding='utf-8-sig')
    print(f"   ✅ {len(df_rewards)} rewards exported")
    
    # 5. Redemption History
    print("\n5️⃣ Exporting Redemption History...")
    df_redemptions = pd.read_sql_query("""
        SELECT 
            rh.redemption_id,
            rh.user_id,
            u.name as user_name,
            u.nationality,
            u.age,
            u.gender,
            rh.reward_id,
            rh.reward_name,
            rh.reward_category,
            rh.points_spent,
            rh.remaining_balance,
            rh.redemption_status,
            rh.redeemed_at,
            date(rh.redeemed_at) as redemption_date,
            strftime('%Y-%m', rh.redeemed_at) as year_month,
            strftime('%Y', rh.redeemed_at) as year,
            strftime('%m', rh.redeemed_at) as month
        FROM redemption_history rh
        JOIN users u ON rh.user_id = u.user_id
        ORDER BY rh.redeemed_at DESC
    """, conn)
    df_redemptions.to_csv(f"{export_folder}/05_redemption_history.csv", index=False, encoding='utf-8-sig')
    print(f"   ✅ {len(df_redemptions)} redemptions exported")
    
    # 6. Referral Tracking
    print("\n6️⃣ Exporting Referral Data...")
    df_referrals = pd.read_sql_query("""
        SELECT 
            rt.referral_id,
            rt.referrer_user_id,
            u1.name as referrer_name,
            u1.nationality as referrer_nationality,
            rt.referred_user_id,
            u2.name as referred_name,
            u2.nationality as referred_nationality,
            rt.referral_code,
            rt.visit_completed,
            rt.points_awarded,
            rt.referred_at,
            rt.visit_completed_at,
            date(rt.referred_at) as referral_date
        FROM referral_tracking rt
        JOIN users u1 ON rt.referrer_user_id = u1.user_id
        JOIN users u2 ON rt.referred_user_id = u2.user_id
        ORDER BY rt.referred_at DESC
    """, conn)
    df_referrals.to_csv(f"{export_folder}/06_referral_tracking.csv", index=False, encoding='utf-8-sig')
    print(f"   ✅ {len(df_referrals)} referrals exported")
    
    # 7. Survey Responses Consolidated (Simple approach - count only)
    print("\n7️⃣ Exporting Survey Summary...")
    df_surveys = pd.read_sql_query("""
        SELECT 
            'Overall Experience' as survey_type,
            response_id,
            user_id,
            time_spent_seconds,
            is_spam,
            submitted_at
        FROM survey_overall_experience
        UNION ALL
        SELECT 
            'Service & Operations' as survey_type,
            response_id,
            user_id,
            time_spent_seconds,
            is_spam,
            submitted_at
        FROM survey_service_operations
        UNION ALL
        SELECT 
            'Tour & Educational' as survey_type,
            response_id,
            user_id,
            time_spent_seconds,
            is_spam,
            submitted_at
        FROM survey_tour_educational
        UNION ALL
        SELECT 
            'Facilities & Spending' as survey_type,
            response_id,
            user_id,
            time_spent_seconds,
            is_spam,
            submitted_at
        FROM survey_facilities_spending
        UNION ALL
        SELECT 
            'Marketing & Loyalty' as survey_type,
            response_id,
            user_id,
            time_spent_seconds,
            is_spam,
            submitted_at
        FROM survey_marketing_loyalty
        UNION ALL
        SELECT 
            'Tut Immersive Experience' as survey_type,
            response_id,
            user_id,
            time_spent_seconds,
            is_spam,
            submitted_at
        FROM survey_immersive_experience
        UNION ALL
        SELECT 
            'Childrens Museum' as survey_type,
            response_id,
            user_id,
            time_spent_seconds,
            is_spam,
            submitted_at
        FROM survey_childrens_museum
        ORDER BY submitted_at DESC
    """, conn)
    df_surveys['submitted_date'] = pd.to_datetime(df_surveys['submitted_at']).dt.date
    df_surveys['year_month'] = pd.to_datetime(df_surveys['submitted_at']).dt.strftime('%Y-%m')
    df_surveys.to_csv(f"{export_folder}/07_survey_responses.csv", index=False, encoding='utf-8-sig')
    print(f"   ✅ {len(df_surveys)} survey responses exported")
    
    # 8. User Survey Participation Summary
    print("\n8️⃣ Exporting User Survey Summary...")
    df_user_surveys = pd.read_sql_query("""
        SELECT 
            u.user_id,
            u.name,
            u.nationality,
            u.age,
            u.gender,
            u.language,
            COALESCE(survey_counts.total_surveys, 0) as total_surveys,
            COALESCE(survey_counts.valid_surveys, 0) as valid_surveys,
            COALESCE(survey_counts.spam_surveys, 0) as spam_surveys,
            COALESCE(up.surveys_completed, 0) as surveys_for_points,
            COALESCE(up.current_points_balance, 0) as points_balance,
            COALESCE(up.profile_completed, 0) as profile_completed
        FROM users u
        LEFT JOIN (
            SELECT user_id, 
                   COUNT(*) as total_surveys,
                   SUM(CASE WHEN is_spam = 0 THEN 1 ELSE 0 END) as valid_surveys,
                   SUM(CASE WHEN is_spam = 1 THEN 1 ELSE 0 END) as spam_surveys
            FROM (
                SELECT user_id, is_spam FROM survey_overall_experience
                UNION ALL SELECT user_id, is_spam FROM survey_service_operations
                UNION ALL SELECT user_id, is_spam FROM survey_tour_educational
                UNION ALL SELECT user_id, is_spam FROM survey_facilities_spending
                UNION ALL SELECT user_id, is_spam FROM survey_marketing_loyalty
                UNION ALL SELECT user_id, is_spam FROM survey_immersive_experience
                UNION ALL SELECT user_id, is_spam FROM survey_childrens_museum
            ) surveys
            GROUP BY user_id
        ) survey_counts ON u.user_id = survey_counts.user_id
        LEFT JOIN user_points up ON u.user_id = up.user_id
        ORDER BY total_surveys DESC, u.user_id
    """, conn)
    df_user_surveys.to_csv(f"{export_folder}/08_user_survey_summary.csv", index=False, encoding='utf-8-sig')
    print(f"   ✅ {len(df_user_surveys)} user summaries exported")
    
    # 9. Analytics Summary (Pre-aggregated for Power BI)
    print("\n9️⃣ Exporting Analytics Summary...")
    
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM loyalty_analytics")
    analytics = cursor.fetchone()
    
    analytics_dict = {
        'metric': [
            'Users with Points', 'Total Users Enrolled', 'Avg Points per User',
            'Total Points Distributed', 'Total Points Redeemed', 'Total Surveys Completed',
            'Total Points from Surveys', 'Successful Referrals', 'Total Points from Referrals',
            'Total Redemptions', 'Users Who Redeemed', 'Most Redeemed Reward (All Time)',
            'Most Redeemed Reward (30 Days)', 'Users Reached Explorer', 'Users Reached Guardian',
            'Users Reached Legend', 'Redemption Rate %'
        ],
        'value': list(analytics) if analytics else [0] * 17
    }
    
    df_analytics = pd.DataFrame(analytics_dict)
    df_analytics.to_csv(f"{export_folder}/09_analytics_summary.csv", index=False, encoding='utf-8-sig')
    print(f"   ✅ Analytics summary exported")
    
    # 10. Date Dimension Table (for time-based analysis)
    print("\n🔟 Creating Date Dimension...")
    df_dates = pd.read_sql_query("""
        SELECT DISTINCT 
            date(created_at) as date,
            strftime('%Y', created_at) as year,
            strftime('%m', created_at) as month,
            strftime('%d', created_at) as day,
            strftime('%Y-%m', created_at) as year_month,
            strftime('%Y-Q', created_at) as year_quarter,
            CASE strftime('%w', created_at)
                WHEN '0' THEN 'Sunday'
                WHEN '1' THEN 'Monday'
                WHEN '2' THEN 'Tuesday'
                WHEN '3' THEN 'Wednesday'
                WHEN '4' THEN 'Thursday'
                WHEN '5' THEN 'Friday'
                WHEN '6' THEN 'Saturday'
            END as day_of_week,
            CASE strftime('%w', created_at)
                WHEN '0' THEN 7
                WHEN '1' THEN 1
                WHEN '2' THEN 2
                WHEN '3' THEN 3
                WHEN '4' THEN 4
                WHEN '5' THEN 5
                WHEN '6' THEN 6
            END as day_number
        FROM (
            SELECT created_at FROM users
            UNION SELECT submitted_at as created_at FROM survey_overall_experience
            UNION SELECT redeemed_at as created_at FROM redemption_history
            UNION SELECT created_at FROM points_transactions
        )
        WHERE created_at IS NOT NULL
        ORDER BY date
    """, conn)
    df_dates.to_csv(f"{export_folder}/10_date_dimension.csv", index=False, encoding='utf-8-sig')
    print(f"   ✅ {len(df_dates)} dates exported")
    
    conn.close()
    
    # Summary
    print(f"\n" + "=" * 80)
    print("📊 EXPORT SUMMARY")
    print("=" * 80)
    print(f"📁 Export Location: {os.path.abspath(export_folder)}/")
    print(f"\n📊 Files Created:")
    print(f"   1. 01_users.csv - {len(df_users):,} records")
    print(f"   2. 02_user_points.csv - {len(df_points):,} records")
    print(f"   3. 03_points_transactions.csv - {len(df_transactions):,} records")
    print(f"   4. 04_rewards_catalog.csv - {len(df_rewards):,} records")
    print(f"   5. 05_redemption_history.csv - {len(df_redemptions):,} records")
    print(f"   6. 06_referral_tracking.csv - {len(df_referrals):,} records")
    print(f"   7. 07_survey_responses.csv - {len(df_surveys):,} records")
    print(f"   8. 08_user_survey_summary.csv - {len(df_user_surveys):,} records")
    print(f"   9. 09_analytics_summary.csv - {len(df_analytics):,} records")
    print(f"  10. 10_date_dimension.csv - {len(df_dates):,} records")
    
    print(f"\n" + "=" * 80)
    print("✅ POWER BI EXPORT COMPLETE")
    print("=" * 80)
    print(f"\n💡 Next Steps:")
    print(f"   1. Zip the 'powerbi_exports' folder")
    print(f"   2. Send to your data analyst")
    print(f"   3. They can import the CSV files into Power BI")
    print(f"   4. See POWERBI_IMPORT_GUIDE.md for detailed instructions")

if __name__ == "__main__":
    export_for_powerbi()
