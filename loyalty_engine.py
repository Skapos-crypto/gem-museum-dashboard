"""
GEM Museum Loyalty Points Engine
Manages points, rewards, referrals, and redemptions
Created: December 10, 2025
"""

import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import json

# Constants
POINTS_PER_SURVEY = 20
POINTS_PER_REFERRAL = 30
POINTS_PER_PROFILE_COMPLETION = 40

class LoyaltyPointsEngine:
    """Main engine for managing the museum's loyalty program"""
    
    def __init__(self, db_path: str = "visitor_feedback.db"):
        self.db_path = db_path
    
    def _get_connection(self):
        """Get database connection"""
        return sqlite3.connect(self.db_path)
    
    # ============================================================
    # INITIALIZATION
    # ============================================================
    
    def initialize_user_points(self, user_id: int) -> bool:
        """Initialize points tracking for a new user"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT OR IGNORE INTO user_points 
                (user_id, total_points_earned, total_points_spent, current_points_balance,
                 points_from_surveys, points_from_referrals, surveys_completed, referrals_completed)
                VALUES (?, 0, 0, 0, 0, 0, 0, 0)
            """, (user_id,))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error initializing user points: {e}")
            return False
    
    # ============================================================
    # POINT GENERATION
    # ============================================================
    
    def award_survey_points(self, user_id: int, survey_type: str, survey_id: int) -> Dict:
        """Award points for completing a survey"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Check if user exists in points table
            self.initialize_user_points(user_id)
            
            # Get current balance
            cursor.execute("SELECT current_points_balance FROM user_points WHERE user_id = ?", (user_id,))
            result = cursor.fetchone()
            current_balance = result[0] if result else 0
            
            new_balance = current_balance + POINTS_PER_SURVEY
            
            # Update user_points
            cursor.execute("""
                UPDATE user_points 
                SET total_points_earned = total_points_earned + ?,
                    current_points_balance = ?,
                    points_from_surveys = points_from_surveys + ?,
                    surveys_completed = surveys_completed + 1,
                    updated_at = CURRENT_TIMESTAMP
                WHERE user_id = ?
            """, (POINTS_PER_SURVEY, new_balance, POINTS_PER_SURVEY, user_id))
            
            # Log transaction
            cursor.execute("""
                INSERT INTO points_transactions 
                (user_id, transaction_type, points_change, balance_after, reference_id, reference_type, description)
                VALUES (?, 'SURVEY', ?, ?, ?, ?, ?)
            """, (user_id, POINTS_PER_SURVEY, new_balance, survey_id, survey_type, 
                  f"Survey completed: {survey_type}"))
            
            conn.commit()
            conn.close()
            
            return {
                "success": True,
                "points_awarded": POINTS_PER_SURVEY,
                "new_balance": new_balance,
                "message": f"Earned {POINTS_PER_SURVEY} points for completing survey!"
            }
        except Exception as e:
            print(f"Error awarding survey points: {e}")
            return {"success": False, "error": str(e)}
    
    def award_referral_points(self, referrer_user_id: int, referred_user_id: int, referral_code: Optional[str] = None) -> Dict:
        """Award points when a referred friend completes their first visit check-in"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Check if referral already exists and is completed
            cursor.execute("""
                SELECT referral_id, visit_completed 
                FROM referral_tracking 
                WHERE referrer_user_id = ? AND referred_user_id = ?
            """, (referrer_user_id, referred_user_id))
            
            existing = cursor.fetchone()
            
            if existing:
                if existing[1] == 1:
                    return {"success": False, "error": "Referral already completed"}
                referral_id = existing[0]
            else:
                # Create new referral record
                cursor.execute("""
                    INSERT INTO referral_tracking 
                    (referrer_user_id, referred_user_id, referral_code, visit_completed, points_awarded)
                    VALUES (?, ?, ?, 0, 0)
                """, (referrer_user_id, referred_user_id, referral_code))
                referral_id = cursor.lastrowid
            
            # Mark referral as completed
            cursor.execute("""
                UPDATE referral_tracking 
                SET visit_completed = 1, 
                    points_awarded = ?,
                    visit_completed_at = CURRENT_TIMESTAMP
                WHERE referral_id = ?
            """, (POINTS_PER_REFERRAL, referral_id))
            
            # Initialize points for referrer if needed
            self.initialize_user_points(referrer_user_id)
            
            # Get current balance
            cursor.execute("SELECT current_points_balance FROM user_points WHERE user_id = ?", (referrer_user_id,))
            current_balance = cursor.fetchone()[0]
            new_balance = current_balance + POINTS_PER_REFERRAL
            
            # Update referrer's points
            cursor.execute("""
                UPDATE user_points 
                SET total_points_earned = total_points_earned + ?,
                    current_points_balance = ?,
                    points_from_referrals = points_from_referrals + ?,
                    referrals_completed = referrals_completed + 1,
                    updated_at = CURRENT_TIMESTAMP
                WHERE user_id = ?
            """, (POINTS_PER_REFERRAL, new_balance, POINTS_PER_REFERRAL, referrer_user_id))
            
            # Log transaction
            cursor.execute("""
                INSERT INTO points_transactions 
                (user_id, transaction_type, points_change, balance_after, reference_id, reference_type, description)
                VALUES (?, 'REFERRAL', ?, ?, ?, 'referral', ?)
            """, (referrer_user_id, POINTS_PER_REFERRAL, new_balance, referral_id,
                  f"Referral bonus: Friend completed first visit"))
            
            conn.commit()
            conn.close()
            
            return {
                "success": True,
                "points_awarded": POINTS_PER_REFERRAL,
                "new_balance": new_balance,
                "message": f"Earned {POINTS_PER_REFERRAL} points for successful referral!"
            }
        except Exception as e:
            print(f"Error awarding referral points: {e}")
            return {"success": False, "error": str(e)}
    
    def award_profile_completion_points(self, user_id: int) -> Dict:
        """Award points for completing user profile"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Initialize points for user if needed
            self.initialize_user_points(user_id)
            
            # Check if profile already completed
            cursor.execute("SELECT profile_completed FROM user_points WHERE user_id = ?", (user_id,))
            result = cursor.fetchone()
            
            if result and result[0] == 1:
                return {"success": False, "error": "Profile completion bonus already claimed"}
            
            # Get current balance
            cursor.execute("SELECT current_points_balance FROM user_points WHERE user_id = ?", (user_id,))
            current_balance = cursor.fetchone()[0]
            new_balance = current_balance + POINTS_PER_PROFILE_COMPLETION
            
            # Update user_points
            cursor.execute("""
                UPDATE user_points 
                SET total_points_earned = total_points_earned + ?,
                    current_points_balance = ?,
                    points_from_profile_completion = ?,
                    profile_completed = 1,
                    profile_completed_at = CURRENT_TIMESTAMP,
                    updated_at = CURRENT_TIMESTAMP
                WHERE user_id = ?
            """, (POINTS_PER_PROFILE_COMPLETION, new_balance, POINTS_PER_PROFILE_COMPLETION, user_id))
            
            # Log transaction
            cursor.execute("""
                INSERT INTO points_transactions 
                (user_id, transaction_type, points_change, balance_after, reference_id, reference_type, description)
                VALUES (?, 'PROFILE_COMPLETION', ?, ?, ?, 'profile', ?)
            """, (user_id, POINTS_PER_PROFILE_COMPLETION, new_balance, user_id,
                  f"Profile completion bonus"))
            
            conn.commit()
            conn.close()
            
            return {
                "success": True,
                "points_awarded": POINTS_PER_PROFILE_COMPLETION,
                "new_balance": new_balance,
                "message": f"Earned {POINTS_PER_PROFILE_COMPLETION} points for completing your profile!"
            }
        except Exception as e:
            print(f"Error awarding profile completion points: {e}")
            return {"success": False, "error": str(e)}
    
    # ============================================================
    # REWARD REDEMPTION
    # ============================================================
    
    def redeem_reward(self, user_id: int, reward_name: str) -> Dict:
        """Redeem a reward if user has enough points"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Get reward details
            cursor.execute("""
                SELECT reward_id, reward_category, points_required, is_active 
                FROM rewards_catalog 
                WHERE reward_name = ?
            """, (reward_name,))
            
            reward = cursor.fetchone()
            if not reward:
                return {"success": False, "error": "Reward not found"}
            
            reward_id, reward_category, points_required, is_active = reward
            
            if not is_active:
                return {"success": False, "error": "Reward is no longer available"}
            
            # Get user's current balance
            cursor.execute("SELECT current_points_balance FROM user_points WHERE user_id = ?", (user_id,))
            result = cursor.fetchone()
            
            if not result:
                return {"success": False, "error": "User not enrolled in loyalty program"}
            
            current_balance = result[0]
            
            # Validate sufficient points
            if current_balance < points_required:
                return {
                    "success": False, 
                    "error": f"Insufficient points. Need {points_required}, have {current_balance}"
                }
            
            # Calculate new balance
            new_balance = current_balance - points_required
            
            # Update user_points
            cursor.execute("""
                UPDATE user_points 
                SET total_points_spent = total_points_spent + ?,
                    current_points_balance = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE user_id = ?
            """, (points_required, new_balance, user_id))
            
            # Log redemption
            cursor.execute("""
                INSERT INTO redemption_history 
                (user_id, reward_id, reward_name, reward_category, points_spent, remaining_balance)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (user_id, reward_id, reward_name, reward_category, points_required, new_balance))
            
            redemption_id = cursor.lastrowid
            
            # Log transaction
            cursor.execute("""
                INSERT INTO points_transactions 
                (user_id, transaction_type, points_change, balance_after, reference_id, reference_type, description)
                VALUES (?, 'REDEMPTION', ?, ?, ?, 'redemption', ?)
            """, (user_id, -points_required, new_balance, redemption_id,
                  f"Redeemed: {reward_name}"))
            
            conn.commit()
            conn.close()
            
            return {
                "success": True,
                "reward_name": reward_name,
                "points_spent": points_required,
                "new_balance": new_balance,
                "message": f"Successfully redeemed {reward_name}!"
            }
        except Exception as e:
            print(f"Error redeeming reward: {e}")
            return {"success": False, "error": str(e)}
    
    # ============================================================
    # USER QUERIES
    # ============================================================
    
    def get_user_points_summary(self, user_id: int) -> Dict:
        """Get complete points summary for a user"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Get points data
            cursor.execute("""
                SELECT total_points_earned, total_points_spent, current_points_balance,
                       points_from_surveys, points_from_referrals, points_from_profile_completion,
                       surveys_completed, referrals_completed, profile_completed
                FROM user_points 
                WHERE user_id = ?
            """, (user_id,))
            
            result = cursor.fetchone()
            if not result:
                return {"success": False, "error": "User not enrolled in loyalty program"}
            
            points_data = {
                "total_points_earned": result[0],
                "total_points_spent": result[1],
                "current_points_balance": result[2],
                "points_from_surveys": result[3],
                "points_from_referrals": result[4],
                "points_from_profile_completion": result[5],
                "surveys_completed": result[6],
                "referrals_completed": result[7],
                "profile_completed": result[8]
            }
            
            # Get recent transactions (last 10)
            cursor.execute("""
                SELECT transaction_type, points_change, description, created_at
                FROM points_transactions
                WHERE user_id = ?
                ORDER BY created_at DESC
                LIMIT 10
            """, (user_id,))
            
            recent_activity = []
            for row in cursor.fetchall():
                recent_activity.append({
                    "type": row[0],
                    "points": row[1],
                    "description": row[2],
                    "date": row[3]
                })
            
            conn.close()
            
            return {
                "success": True,
                "points_balance": points_data["current_points_balance"],
                "points_data": points_data,
                "recent_activity": recent_activity
            }
        except Exception as e:
            print(f"Error getting user summary: {e}")
            return {"success": False, "error": str(e)}
    
    def get_available_rewards(self, user_id: int) -> Dict:
        """Get all rewards with affordability status"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Get user balance
            cursor.execute("SELECT current_points_balance FROM user_points WHERE user_id = ?", (user_id,))
            result = cursor.fetchone()
            user_balance = result[0] if result else 0
            
            # Get all active rewards
            cursor.execute("""
                SELECT reward_id, reward_name, reward_category, points_required, description
                FROM rewards_catalog
                WHERE is_active = 1
                ORDER BY points_required ASC
            """)
            
            rewards = []
            for row in cursor.fetchall():
                rewards.append({
                    "reward_id": row[0],
                    "reward_name": row[1],
                    "category": row[2],
                    "points_required": row[3],
                    "description": row[4],
                    "can_afford": user_balance >= row[3],
                    "points_needed": max(0, row[3] - user_balance)
                })
            
            conn.close()
            
            return {
                "success": True,
                "user_balance": user_balance,
                "available_rewards": rewards
            }
        except Exception as e:
            print(f"Error getting available rewards: {e}")
            return {"success": False, "error": str(e)}
    
    def get_user_redemption_history(self, user_id: int, limit: int = 20) -> Dict:
        """Get user's redemption history"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT reward_name, reward_category, points_spent, remaining_balance, redeemed_at
                FROM redemption_history
                WHERE user_id = ?
                ORDER BY redeemed_at DESC
                LIMIT ?
            """, (user_id, limit))
            
            history = []
            for row in cursor.fetchall():
                history.append({
                    "reward_name": row[0],
                    "category": row[1],
                    "points_spent": row[2],
                    "balance_after": row[3],
                    "redeemed_at": row[4]
                })
            
            conn.close()
            
            return {
                "success": True,
                "redemption_history": history
            }
        except Exception as e:
            print(f"Error getting redemption history: {e}")
            return {"success": False, "error": str(e)}
    
    # ============================================================
    # ANALYTICS
    # ============================================================
    
    def get_loyalty_analytics(self) -> Dict:
        """Get comprehensive loyalty program analytics"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Get analytics from view
            cursor.execute("SELECT * FROM loyalty_analytics")
            result = cursor.fetchone()
            
            if not result:
                return {"success": False, "error": "No analytics data available"}
            
            analytics = {
                "users_with_points": result[0],
                "total_users_enrolled": result[1],
                "avg_points_per_user": round(result[2], 2) if result[2] else 0,
                "total_points_distributed": result[3],
                "total_points_redeemed": result[4],
                "total_surveys_completed": result[5],
                "total_points_from_surveys": result[6],
                "successful_referrals": result[7],
                "total_points_from_referrals": result[8],
                "total_redemptions": result[9],
                "users_who_redeemed": result[10],
                "most_redeemed_reward_all_time": result[11],
                "most_redeemed_reward_30_days": result[12],
                "users_reached_explorer": result[13],
                "users_reached_guardian": result[14],
                "users_reached_legend": result[15],
                "redemption_rate_percent": round(result[16], 2) if result[16] else 0
            }
            
            # Get top rewards by category
            cursor.execute("""
                SELECT reward_category, COUNT(*) as redemptions, SUM(points_spent) as total_points
                FROM redemption_history
                GROUP BY reward_category
                ORDER BY redemptions DESC
            """)
            
            category_stats = []
            for row in cursor.fetchall():
                category_stats.append({
                    "category": row[0],
                    "redemptions": row[1],
                    "total_points": row[2]
                })
            
            # Get most active users
            cursor.execute("""
                SELECT u.name, u.email, up.surveys_completed, up.current_points_balance, up.total_points_earned
                FROM user_points up
                JOIN users u ON up.user_id = u.user_id
                ORDER BY up.surveys_completed DESC
                LIMIT 10
            """)
            
            most_active_users = []
            for row in cursor.fetchall():
                most_active_users.append({
                    "name": row[0],
                    "email": row[1],
                    "surveys_completed": row[2],
                    "current_balance": row[3],
                    "total_earned": row[4]
                })
            
            conn.close()
            
            return {
                "success": True,
                "analytics_summary": analytics,
                "category_stats": category_stats,
                "most_active_users": most_active_users
            }
        except Exception as e:
            print(f"Error getting analytics: {e}")
            return {"success": False, "error": str(e)}
    
    def get_reward_redemption_stats(self) -> Dict:
        """Get detailed redemption statistics per reward"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT 
                    r.reward_name,
                    r.reward_category,
                    r.points_required,
                    COUNT(rh.redemption_id) as total_redemptions,
                    SUM(rh.points_spent) as total_points_spent,
                    COUNT(CASE WHEN rh.redeemed_at >= datetime('now', '-30 days') THEN 1 END) as redemptions_last_30_days
                FROM rewards_catalog r
                LEFT JOIN redemption_history rh ON r.reward_id = rh.reward_id
                GROUP BY r.reward_id
                ORDER BY total_redemptions DESC
            """)
            
            stats = []
            for row in cursor.fetchall():
                stats.append({
                    "reward_name": row[0],
                    "category": row[1],
                    "points_required": row[2],
                    "total_redemptions": row[3],
                    "total_points_spent": row[4],
                    "redemptions_last_30_days": row[5]
                })
            
            conn.close()
            
            return {
                "success": True,
                "reward_stats": stats
            }
        except Exception as e:
            print(f"Error getting reward stats: {e}")
            return {"success": False, "error": str(e)}
    
    # ============================================================
    # FRONTEND OUTPUT
    # ============================================================
    
    def get_user_frontend_data(self, user_id: int) -> str:
        """Get complete user data formatted for frontend (JSON)"""
        summary = self.get_user_points_summary(user_id)
        rewards = self.get_available_rewards(user_id)
        analytics = self.get_loyalty_analytics()
        
        output = {
            "points_balance": summary.get("points_balance", 0),
            "recent_activity": summary.get("recent_activity", []),
            "available_rewards": rewards.get("available_rewards", []),
            "analytics_summary": analytics.get("analytics_summary", {})
        }
        
        return json.dumps(output, indent=2)


# ============================================================
# CONVENIENCE FUNCTIONS
# ============================================================

def award_points_for_survey(user_id: int, survey_type: str, survey_id: int, db_path: str = "visitor_feedback.db"):
    """Convenience function to award survey points"""
    engine = LoyaltyPointsEngine(db_path)
    return engine.award_survey_points(user_id, survey_type, survey_id)

def award_points_for_referral(referrer_id: int, referred_id: int, db_path: str = "visitor_feedback.db"):
    """Convenience function to award referral points"""
    engine = LoyaltyPointsEngine(db_path)
    return engine.award_referral_points(referrer_id, referred_id)

def redeem_user_reward(user_id: int, reward_name: str, db_path: str = "visitor_feedback.db"):
    """Convenience function to redeem a reward"""
    engine = LoyaltyPointsEngine(db_path)
    return engine.redeem_reward(user_id, reward_name)
