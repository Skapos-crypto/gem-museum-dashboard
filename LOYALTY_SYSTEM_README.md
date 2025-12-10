# 🎮 GEM Museum Loyalty Points System

## Overview
Complete loyalty program management system for the Grand Egyptian Museum, tracking user points, reward redemptions, survey completions, and referral bonuses.

## 📊 System Components

### 1. Database Tables

#### `user_points` - Main Balance Tracking
- `user_id` - Primary key, links to users table
- `total_points_earned` - Lifetime points earned
- `total_points_spent` - Lifetime points spent on rewards
- `current_points_balance` - Available points
- `points_from_surveys` - Points earned from surveys
- `points_from_referrals` - Points earned from referrals
- `surveys_completed` - Total surveys completed
- `referrals_completed` - Total successful referrals

#### `rewards_catalog` - Available Rewards
Contains 12 rewards across 5 categories:
- **Digital Rewards** (3 rewards)
  - Explorer Badge: 20 points
  - Guardian Badge: 60 points
  - Legend Badge: 120 points
- **Low-Cost Physical** (2 rewards)
  - Sticker Sheet: 40 points
  - Postcard: 50 points
- **Medium-Cost** (3 rewards)
  - Mini Papyrus Bookmark: 80 points
  - Keychain: 100 points
  - Sticker + Postcard Bundle: 90 points
- **Partner Rewards** (2 rewards)
  - Free Coffee With Meal: 120 points
  - Free Oriental Koshary With Meal: 150 points
- **Museum Experience** (2 rewards)
  - 20% Discount on Paid Experience: 200 points
  - Premium Raffle Ticket: 40 points

#### `points_transactions` - Transaction History
Logs every point movement:
- `SURVEY` - Points earned from survey completion
- `REFERRAL` - Points earned from successful referral
- `REDEMPTION` - Points spent on rewards
- `ADJUSTMENT` - Manual adjustments

#### `referral_tracking` - Referral Management
- Tracks referrer and referred user
- Records referral code
- Tracks visit completion status
- Records points awarded

#### `redemption_history` - Redemption Records
- Complete history of all reward redemptions
- Tracks points spent and balance after redemption
- Includes timestamp for analytics

#### `loyalty_analytics` - Analytics View
Pre-computed metrics including:
- Total users enrolled
- Average points per user
- Total points distributed/redeemed
- Most popular rewards (all-time and 30-day)
- Badge progression tracking
- Redemption rate percentage

## 🎯 Point Generation Rules

### Survey Completion
- **All surveys count equally** (5-6 questions each)
- **Points awarded: 20 points per survey**
- Surveys cannot be repeated within the same exhibit session
- Points awarded immediately upon completion

### Referral Bonus
- **Points awarded: 30 points per successful referral**
- Points awarded **only when referred friend completes first visit check-in**
- Referral must be tracked with referral code
- Cannot claim same referral twice

### No Other Actions Generate Points
Only surveys and successful referrals generate points

## 💎 Reward Categories & Costs

| Reward Name | Category | Points Required |
|------------|----------|-----------------|
| Explorer Badge | Digital | 20 |
| Premium Raffle Ticket | Museum Experience | 40 |
| Sticker Sheet | Low-Cost Physical | 40 |
| Postcard | Low-Cost Physical | 50 |
| Guardian Badge | Digital | 60 |
| Mini Papyrus Bookmark | Medium-Cost | 80 |
| Sticker + Postcard Bundle | Medium-Cost | 90 |
| Keychain | Medium-Cost | 100 |
| Legend Badge | Digital | 120 |
| Free Coffee With Meal | Partner | 120 |
| Free Oriental Koshary With Meal | Partner | 150 |
| 20% Discount on Paid Experience | Museum Experience | 200 |

## 🔧 Usage

### Initialize the Engine

```python
from loyalty_engine import LoyaltyPointsEngine

engine = LoyaltyPointsEngine(db_path="visitor_feedback.db")
```

### Award Survey Points

```python
result = engine.award_survey_points(
    user_id=123,
    survey_type="survey_overall_experience",
    survey_id=456
)

# Result:
# {
#     "success": True,
#     "points_awarded": 20,
#     "new_balance": 100,
#     "message": "Earned 20 points for completing survey!"
# }
```

### Award Referral Points

```python
result = engine.award_referral_points(
    referrer_user_id=123,
    referred_user_id=456,
    referral_code="FRIEND2024"
)

# Result:
# {
#     "success": True,
#     "points_awarded": 30,
#     "new_balance": 130,
#     "message": "Earned 30 points for successful referral!"
# }
```

### Redeem a Reward

```python
result = engine.redeem_reward(
    user_id=123,
    reward_name="Explorer Badge"
)

# Result:
# {
#     "success": True,
#     "reward_name": "Explorer Badge",
#     "points_spent": 20,
#     "new_balance": 110,
#     "message": "Successfully redeemed Explorer Badge!"
# }
```

### Get User Summary

```python
summary = engine.get_user_points_summary(user_id=123)

# Result:
# {
#     "success": True,
#     "points_balance": 110,
#     "points_data": {
#         "total_points_earned": 130,
#         "total_points_spent": 20,
#         "current_points_balance": 110,
#         "points_from_surveys": 100,
#         "points_from_referrals": 30,
#         "surveys_completed": 5,
#         "referrals_completed": 1
#     },
#     "recent_activity": [...]
# }
```

### Get Available Rewards

```python
rewards = engine.get_available_rewards(user_id=123)

# Result:
# {
#     "success": True,
#     "user_balance": 110,
#     "available_rewards": [
#         {
#             "reward_id": 1,
#             "reward_name": "Explorer Badge",
#             "category": "Digital Rewards",
#             "points_required": 20,
#             "description": "...",
#             "can_afford": True,
#             "points_needed": 0
#         },
#         ...
#     ]
# }
```

### Get Analytics

```python
analytics = engine.get_loyalty_analytics()

# Result:
# {
#     "success": True,
#     "analytics_summary": {
#         "users_with_points": 250,
#         "total_users_enrolled": 400,
#         "avg_points_per_user": 75.5,
#         "total_points_distributed": 30200,
#         "total_points_redeemed": 15600,
#         "total_surveys_completed": 1200,
#         "successful_referrals": 145,
#         "total_redemptions": 420,
#         "users_reached_explorer": 300,
#         "users_reached_guardian": 180,
#         "users_reached_legend": 45,
#         "redemption_rate_percent": 62.5
#     },
#     "category_stats": [...],
#     "most_active_users": [...]
# }
```

### Frontend JSON Output

```python
frontend_data = engine.get_user_frontend_data(user_id=123)
print(frontend_data)  # Returns clean JSON string
```

## ✅ Validation Rules

1. **Sufficient Balance Check**: Users can only redeem rewards if they have enough points
2. **Immediate Point Deduction**: Points subtracted immediately upon redemption
3. **No Duplicate Redemptions**: Rewards cannot be redeemed twice in one action
4. **Referral Verification**: Referrals only count when referred visitor performs real check-in
5. **Survey Uniqueness**: Surveys cannot be repeated within same exhibit session
6. **Balance Integrity**: All transactions maintain accurate point balances

## 📈 Analytics Tracked

### User Metrics
- Users with points vs. total enrolled
- Average points per user
- Most active users (by surveys completed)

### Points Distribution
- Total points distributed
- Total points redeemed
- Points from surveys vs. referrals
- Current unredeemed points

### Redemption Metrics
- Total redemptions
- Redemption rate (% of users who redeemed)
- Most redeemed reward (all-time)
- Most redeemed reward (last 30 days)
- Total rewards cost (based on point spend)
- Redemptions by category

### Badge Progression (Funnel Analysis)
- Users reached Explorer (20+ points): Entry level
- Users reached Guardian (60+ points): Mid level
- Users reached Legend (120+ points): Top tier

### Referral Metrics
- Successful referrals
- Pending referrals
- Total points from referrals
- Top referrers

## 🔐 Security Features

- Transaction logging for audit trail
- Balance validation before redemption
- Referral verification before point award
- Duplicate prevention mechanisms
- Database constraints and foreign keys

## 📁 Files

- `database/loyalty_schema.sql` - Database schema definition
- `loyalty_engine.py` - Main loyalty engine class
- `apply_loyalty_schema.py` - Script to apply schema to database
- `test_loyalty_system.py` - Demonstration and test script

## 🚀 Installation

1. Apply the schema to your database:
```bash
python apply_loyalty_schema.py
```

2. Import the loyalty engine in your code:
```python
from loyalty_engine import LoyaltyPointsEngine
```

3. Start using the system!

## 🧪 Testing

Run the test script to see the system in action:
```bash
python test_loyalty_system.py
```

## 📊 Database Indexes

Optimized for performance with indexes on:
- User points balance
- Transaction user and date
- Transaction type
- Referral tracking (referrer, referred, completion status)
- Redemption history (user, reward, date)

## 🎯 Key Features

✅ **Automatic Point Tracking**: Points automatically awarded upon survey/referral completion  
✅ **Real-time Balance Updates**: All balances updated immediately  
✅ **Comprehensive Analytics**: Pre-computed metrics for instant insights  
✅ **Transaction History**: Complete audit trail of all point movements  
✅ **Flexible Rewards**: Easy to add/modify rewards in catalog  
✅ **Referral System**: Track and reward successful referrals  
✅ **JSON Output**: Clean API for frontend integration  
✅ **Validation Rules**: Prevent fraud and ensure data integrity  

## 💡 Usage Examples

### Web App Integration
```python
# When user completes survey
from loyalty_engine import award_points_for_survey
result = award_points_for_survey(user_id, "survey_overall_experience", survey_id)
if result['success']:
    flash(f"Earned {result['points_awarded']} points!")
```

### Dashboard Integration
```python
# Show loyalty analytics on staff dashboard
from loyalty_engine import LoyaltyPointsEngine
engine = LoyaltyPointsEngine()
analytics = engine.get_loyalty_analytics()
# Display analytics['analytics_summary'] in dashboard
```

### API Endpoint
```python
@app.route('/api/user/<int:user_id>/points')
def get_user_points(user_id):
    engine = LoyaltyPointsEngine()
    return jsonify(engine.get_user_points_summary(user_id))
```

## 🔄 Future Enhancements

- Point expiration (e.g., expire after 1 year)
- Tiered rewards based on badge level
- Seasonal/limited-time rewards
- Bonus point multipliers for special events
- Group referral challenges
- Integration with mobile app
- Push notifications for point awards
- Gamification elements (streaks, achievements)

---

**Created**: December 10, 2025  
**Version**: 1.0  
**License**: Internal use for GEM Museum
