-- ============================================================
-- LOYALTY POINTS SYSTEM FOR GEM MUSEUM
-- Created: December 10, 2025
-- ============================================================

-- Drop existing loyalty tables if they exist
DROP TABLE IF EXISTS redemption_history;
DROP TABLE IF EXISTS referral_tracking;
DROP TABLE IF EXISTS points_transactions;
DROP TABLE IF EXISTS user_points;
DROP TABLE IF EXISTS rewards_catalog;
DROP VIEW IF EXISTS loyalty_analytics;

-- ============================================================
-- USER POINTS TABLE (Main Balance Tracking)
-- ============================================================
CREATE TABLE user_points (
    user_id INTEGER PRIMARY KEY,
    total_points_earned INTEGER DEFAULT 0,
    total_points_spent INTEGER DEFAULT 0,
    current_points_balance INTEGER DEFAULT 0,
    points_from_surveys INTEGER DEFAULT 0,
    points_from_referrals INTEGER DEFAULT 0,
    points_from_profile_completion INTEGER DEFAULT 0,
    surveys_completed INTEGER DEFAULT 0,
    referrals_completed INTEGER DEFAULT 0,
    profile_completed INTEGER DEFAULT 0,
    profile_completed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- ============================================================
-- REWARDS CATALOG (All Available Rewards)
-- ============================================================
CREATE TABLE rewards_catalog (
    reward_id INTEGER PRIMARY KEY AUTOINCREMENT,
    reward_name TEXT NOT NULL UNIQUE,
    reward_category TEXT NOT NULL,
    points_required INTEGER NOT NULL,
    description TEXT,
    is_active INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert all rewards into catalog
INSERT INTO rewards_catalog (reward_name, reward_category, points_required, description) VALUES
-- Digital Rewards
('Explorer Badge', 'Digital Rewards', 20, 'Digital achievement badge for new explorers'),
('Guardian Badge', 'Digital Rewards', 60, 'Digital achievement badge for dedicated visitors'),
('Legend Badge', 'Digital Rewards', 120, 'Digital achievement badge for legendary supporters'),

-- Low-Cost Physical Rewards
('Sticker Sheet', 'Low-Cost Physical', 40, 'Collection of museum-themed stickers'),
('Postcard', 'Low-Cost Physical', 50, 'Beautiful museum postcard'),

-- Medium-Cost Rewards
('Mini Papyrus Bookmark', 'Medium-Cost', 80, 'Authentic mini papyrus bookmark'),
('Keychain', 'Medium-Cost', 100, 'Museum-themed keychain'),
('Sticker + Postcard Bundle', 'Medium-Cost', 90, 'Bundle of stickers and postcard'),

-- Partner Rewards
('Free Coffee With Meal', 'Partner Rewards', 120, 'Complimentary coffee with any meal purchase'),
('Free Oriental Koshary With Meal', 'Partner Rewards', 150, 'Traditional Egyptian Koshary dish with meal'),

-- Museum Experience Rewards
('20% Discount on Paid Experience', 'Museum Experience', 200, 'Get 20% off any paid museum experience'),
('Premium Raffle Ticket', 'Museum Experience', 40, 'Entry ticket for premium prize raffle');

-- ============================================================
-- POINTS TRANSACTIONS (All Point Movements)
-- ============================================================
CREATE TABLE points_transactions (
    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    transaction_type TEXT NOT NULL, -- 'SURVEY', 'REFERRAL', 'REDEMPTION', 'PROFILE_COMPLETION', 'ADJUSTMENT'
    points_change INTEGER NOT NULL, -- positive for earn, negative for spend
    balance_after INTEGER NOT NULL,
    reference_id INTEGER, -- survey_id, referral_id, or redemption_id
    reference_type TEXT, -- 'survey_overall_experience', 'referral', 'redemption', 'profile'
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- ============================================================
-- REFERRAL TRACKING (Who Referred Whom)
-- ============================================================
CREATE TABLE referral_tracking (
    referral_id INTEGER PRIMARY KEY AUTOINCREMENT,
    referrer_user_id INTEGER NOT NULL, -- user who made the referral
    referred_user_id INTEGER NOT NULL, -- user who was referred
    referral_code TEXT,
    visit_completed INTEGER DEFAULT 0, -- 0 = pending, 1 = completed
    points_awarded INTEGER DEFAULT 0,
    referred_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    visit_completed_at TIMESTAMP,
    FOREIGN KEY (referrer_user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (referred_user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- ============================================================
-- REDEMPTION HISTORY (All Reward Redemptions)
-- ============================================================
CREATE TABLE redemption_history (
    redemption_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    reward_id INTEGER NOT NULL,
    reward_name TEXT NOT NULL,
    reward_category TEXT NOT NULL,
    points_spent INTEGER NOT NULL,
    remaining_balance INTEGER NOT NULL,
    redemption_status TEXT DEFAULT 'COMPLETED', -- 'COMPLETED', 'PENDING', 'CANCELLED'
    redeemed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (reward_id) REFERENCES rewards_catalog(reward_id)
);

-- ============================================================
-- INDEXES FOR PERFORMANCE
-- ============================================================
CREATE INDEX idx_user_points_balance ON user_points(current_points_balance);
CREATE INDEX idx_points_transactions_user ON points_transactions(user_id, created_at);
CREATE INDEX idx_points_transactions_type ON points_transactions(transaction_type);
CREATE INDEX idx_referral_tracking_referrer ON referral_tracking(referrer_user_id);
CREATE INDEX idx_referral_tracking_referred ON referral_tracking(referred_user_id);
CREATE INDEX idx_referral_tracking_completed ON referral_tracking(visit_completed);
CREATE INDEX idx_redemption_history_user ON redemption_history(user_id, redeemed_at);
CREATE INDEX idx_redemption_history_reward ON redemption_history(reward_id);
CREATE INDEX idx_redemption_history_date ON redemption_history(redeemed_at);

-- ============================================================
-- ANALYTICS VIEW (Pre-computed Metrics)
-- ============================================================
CREATE VIEW loyalty_analytics AS
SELECT
    -- User Stats
    (SELECT COUNT(*) FROM user_points WHERE current_points_balance > 0) as users_with_points,
    (SELECT COUNT(*) FROM user_points) as total_users_enrolled,
    (SELECT AVG(current_points_balance) FROM user_points) as avg_points_per_user,
    (SELECT SUM(total_points_earned) FROM user_points) as total_points_distributed,
    (SELECT SUM(total_points_spent) FROM user_points) as total_points_redeemed,
    
    -- Survey Stats
    (SELECT SUM(surveys_completed) FROM user_points) as total_surveys_completed,
    (SELECT SUM(points_from_surveys) FROM user_points) as total_points_from_surveys,
    
    -- Referral Stats
    (SELECT COUNT(*) FROM referral_tracking WHERE visit_completed = 1) as successful_referrals,
    (SELECT SUM(points_from_referrals) FROM user_points) as total_points_from_referrals,
    
    -- Redemption Stats
    (SELECT COUNT(*) FROM redemption_history) as total_redemptions,
    (SELECT COUNT(DISTINCT user_id) FROM redemption_history) as users_who_redeemed,
    
    -- Most Popular Reward (All Time)
    (SELECT reward_name FROM redemption_history 
     GROUP BY reward_name 
     ORDER BY COUNT(*) DESC LIMIT 1) as most_redeemed_reward_all_time,
    
    -- Most Popular Reward (Last 30 Days)
    (SELECT reward_name FROM redemption_history 
     WHERE redeemed_at >= datetime('now', '-30 days')
     GROUP BY reward_name 
     ORDER BY COUNT(*) DESC LIMIT 1) as most_redeemed_reward_30_days,
    
    -- Badge Progress
    (SELECT COUNT(*) FROM user_points WHERE total_points_earned >= 20) as users_reached_explorer,
    (SELECT COUNT(*) FROM user_points WHERE total_points_earned >= 60) as users_reached_guardian,
    (SELECT COUNT(*) FROM user_points WHERE total_points_earned >= 120) as users_reached_legend,
    
    -- Engagement Rate
    (SELECT CAST(COUNT(DISTINCT user_id) AS FLOAT) / 
            (SELECT COUNT(*) FROM users) * 100 
     FROM redemption_history) as redemption_rate_percent;
