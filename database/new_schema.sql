-- NEW GEM VISITOR FEEDBACK SYSTEM DATABASE SCHEMA
-- Created: December 10, 2025

-- Drop existing tables if they exist
DROP TABLE IF EXISTS survey_childrens_museum;
DROP TABLE IF EXISTS survey_immersive_experience;
DROP TABLE IF EXISTS survey_marketing_loyalty;
DROP TABLE IF EXISTS survey_facilities_spending;
DROP TABLE IF EXISTS survey_tour_educational;
DROP TABLE IF EXISTS survey_service_operations;
DROP TABLE IF EXISTS survey_overall_experience;
DROP TABLE IF EXISTS users;
DROP VIEW IF EXISTS consolidated_feedback;

-- ============================================================
-- USERS TABLE (Demographics)
-- ============================================================
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    nationality TEXT NOT NULL,
    age INTEGER NOT NULL,
    language TEXT NOT NULL,
    gender TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- SURVEY 1: OVERALL EXPERIENCE (Core Emotion + NPS)
-- ============================================================
CREATE TABLE survey_overall_experience (
    response_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    overall_rating INTEGER CHECK(overall_rating BETWEEN 1 AND 5),
    favorite_exhibit TEXT,
    visit_type TEXT,
    nps_score INTEGER CHECK(nps_score BETWEEN 0 AND 10),
    additional_comments TEXT,
    time_spent_seconds INTEGER NOT NULL,
    is_spam INTEGER DEFAULT 0,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- ============================================================
-- SURVEY 2: SERVICE & OPERATIONS (Performance & Flow)
-- ============================================================
CREATE TABLE survey_service_operations (
    response_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    staff_hospitality_rating INTEGER CHECK(staff_hospitality_rating BETWEEN 1 AND 5),
    cleanliness_rating INTEGER CHECK(cleanliness_rating BETWEEN 1 AND 5),
    crowd_management_rating INTEGER CHECK(crowd_management_rating BETWEEN 1 AND 5),
    entry_wait_time TEXT,
    issues_faced TEXT,
    additional_comments TEXT,
    time_spent_seconds INTEGER NOT NULL,
    is_spam INTEGER DEFAULT 0,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- ============================================================
-- SURVEY 3: TOUR & EDUCATIONAL EXPERIENCE
-- ============================================================
CREATE TABLE survey_tour_educational (
    response_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    used_audio_guide TEXT,
    tour_experience_rating INTEGER CHECK(tour_experience_rating BETWEEN 1 AND 5),
    information_clarity_rating INTEGER CHECK(information_clarity_rating BETWEEN 1 AND 5),
    learned_something TEXT,
    no_tour_reason TEXT,
    additional_comments TEXT,
    time_spent_seconds INTEGER NOT NULL,
    is_spam INTEGER DEFAULT 0,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- ============================================================
-- SURVEY 4: FACILITIES & SPENDING
-- ============================================================
CREATE TABLE survey_facilities_spending (
    response_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    spending_motivation TEXT,
    facilities_rating INTEGER CHECK(facilities_rating BETWEEN 1 AND 5),
    future_spending_driver TEXT,
    additional_comments TEXT,
    time_spent_seconds INTEGER NOT NULL,
    is_spam INTEGER DEFAULT 0,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- ============================================================
-- SURVEY 5: MARKETING & LOYALTY (Growth Engine)
-- ============================================================
CREATE TABLE survey_marketing_loyalty (
    response_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    heard_about_gem TEXT,
    platform_influence TEXT,
    first_visit TEXT,
    would_visit_again TEXT,
    would_follow_social TEXT,
    additional_comments TEXT,
    time_spent_seconds INTEGER NOT NULL,
    is_spam INTEGER DEFAULT 0,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- ============================================================
-- SURVEY 6: IMMERSIVE EXPERIENCE (VR/AR/MR)
-- ============================================================
CREATE TABLE survey_immersive_experience (
    response_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    overall_immersive_rating INTEGER CHECK(overall_immersive_rating BETWEEN 1 AND 5),
    equipment_comfort_rating INTEGER CHECK(equipment_comfort_rating BETWEEN 1 AND 5),
    experience_length TEXT,
    storytelling_satisfaction INTEGER CHECK(storytelling_satisfaction BETWEEN 1 AND 5),
    value_for_money_rating INTEGER CHECK(value_for_money_rating BETWEEN 1 AND 5),
    recommendation_likelihood TEXT,
    additional_comments TEXT,
    time_spent_seconds INTEGER NOT NULL,
    is_spam INTEGER DEFAULT 0,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- ============================================================
-- SURVEY 7: CHILDREN'S MUSEUM EXPERIENCE
-- ============================================================
CREATE TABLE survey_childrens_museum (
    response_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    overall_experience_rating INTEGER CHECK(overall_experience_rating BETWEEN 1 AND 5),
    age_appropriateness_rating INTEGER CHECK(age_appropriateness_rating BETWEEN 1 AND 5),
    educational_value_rating INTEGER CHECK(educational_value_rating BETWEEN 1 AND 5),
    fun_entertainment_rating INTEGER CHECK(fun_entertainment_rating BETWEEN 1 AND 5),
    interactivity_rating INTEGER CHECK(interactivity_rating BETWEEN 1 AND 5),
    instructions_clarity_rating INTEGER CHECK(instructions_clarity_rating BETWEEN 1 AND 5),
    staff_support_rating INTEGER CHECK(staff_support_rating BETWEEN 1 AND 5),
    cleanliness_rating INTEGER CHECK(cleanliness_rating BETWEEN 1 AND 5),
    value_for_money_rating INTEGER CHECK(value_for_money_rating BETWEEN 1 AND 5),
    would_recommend TEXT,
    heard_about_us TEXT,
    child_age_group TEXT,
    additional_comments TEXT,
    time_spent_seconds INTEGER NOT NULL,
    is_spam INTEGER DEFAULT 0,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- ============================================================
-- CONSOLIDATED VIEW (All Feedback Merged)
-- ============================================================
CREATE VIEW consolidated_feedback AS
SELECT 
    u.user_id,
    u.email,
    u.name,
    u.nationality,
    u.age,
    u.language,
    u.gender,
    u.created_at as user_created_at,
    
    -- Overall Experience
    soe.response_id as overall_response_id,
    soe.overall_rating,
    soe.favorite_exhibit,
    soe.visit_type,
    soe.nps_score,
    soe.additional_comments as overall_comments,
    soe.time_spent_seconds as overall_time_spent,
    soe.is_spam as overall_is_spam,
    soe.submitted_at as overall_submitted_at,
    
    -- Service & Operations
    sso.response_id as service_response_id,
    sso.staff_hospitality_rating,
    sso.cleanliness_rating,
    sso.crowd_management_rating,
    sso.entry_wait_time,
    sso.issues_faced,
    sso.additional_comments as service_comments,
    sso.time_spent_seconds as service_time_spent,
    sso.is_spam as service_is_spam,
    sso.submitted_at as service_submitted_at,
    
    -- Tour & Educational
    ste.response_id as tour_response_id,
    ste.used_audio_guide,
    ste.tour_experience_rating,
    ste.information_clarity_rating,
    ste.learned_something,
    ste.no_tour_reason,
    ste.additional_comments as tour_comments,
    ste.time_spent_seconds as tour_time_spent,
    ste.is_spam as tour_is_spam,
    ste.submitted_at as tour_submitted_at,
    
    -- Facilities & Spending
    sfs.response_id as facilities_response_id,
    sfs.spending_motivation,
    sfs.facilities_rating,
    sfs.future_spending_driver,
    sfs.additional_comments as facilities_comments,
    sfs.time_spent_seconds as facilities_time_spent,
    sfs.is_spam as facilities_is_spam,
    sfs.submitted_at as facilities_submitted_at,
    
    -- Marketing & Loyalty
    sml.response_id as marketing_response_id,
    sml.heard_about_gem,
    sml.platform_influence,
    sml.first_visit,
    sml.would_visit_again,
    sml.would_follow_social,
    sml.additional_comments as marketing_comments,
    sml.time_spent_seconds as marketing_time_spent,
    sml.is_spam as marketing_is_spam,
    sml.submitted_at as marketing_submitted_at,
    
    -- Immersive Experience
    sie.response_id as immersive_response_id,
    sie.overall_immersive_rating,
    sie.equipment_comfort_rating,
    sie.experience_length,
    sie.storytelling_satisfaction,
    sie.value_for_money_rating,
    sie.recommendation_likelihood,
    sie.additional_comments as immersive_comments,
    sie.time_spent_seconds as immersive_time_spent,
    sie.is_spam as immersive_is_spam,
    sie.submitted_at as immersive_submitted_at,
    
    -- Children's Museum
    scm.response_id as childrens_response_id,
    scm.overall_experience_rating as childrens_overall_rating,
    scm.age_appropriateness_rating,
    scm.educational_value_rating,
    scm.fun_entertainment_rating,
    scm.interactivity_rating,
    scm.instructions_clarity_rating,
    scm.staff_support_rating,
    scm.cleanliness_rating as childrens_cleanliness,
    scm.value_for_money_rating as childrens_value_rating,
    scm.would_recommend,
    scm.heard_about_us,
    scm.child_age_group,
    scm.additional_comments as childrens_comments,
    scm.time_spent_seconds as childrens_time_spent,
    scm.is_spam as childrens_is_spam,
    scm.submitted_at as childrens_submitted_at
    
FROM users u
LEFT JOIN survey_overall_experience soe ON u.user_id = soe.user_id
LEFT JOIN survey_service_operations sso ON u.user_id = sso.user_id
LEFT JOIN survey_tour_educational ste ON u.user_id = ste.user_id
LEFT JOIN survey_facilities_spending sfs ON u.user_id = sfs.user_id
LEFT JOIN survey_marketing_loyalty sml ON u.user_id = sml.user_id
LEFT JOIN survey_immersive_experience sie ON u.user_id = sie.user_id
LEFT JOIN survey_childrens_museum scm ON u.user_id = scm.user_id;

-- ============================================================
-- INDEXES FOR PERFORMANCE
-- ============================================================
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_nationality ON users(nationality);
CREATE INDEX idx_overall_user_spam ON survey_overall_experience(user_id, is_spam);
CREATE INDEX idx_service_user_spam ON survey_service_operations(user_id, is_spam);
CREATE INDEX idx_tour_user_spam ON survey_tour_educational(user_id, is_spam);
CREATE INDEX idx_facilities_user_spam ON survey_facilities_spending(user_id, is_spam);
CREATE INDEX idx_marketing_user_spam ON survey_marketing_loyalty(user_id, is_spam);
CREATE INDEX idx_immersive_user_spam ON survey_immersive_experience(user_id, is_spam);
CREATE INDEX idx_childrens_user_spam ON survey_childrens_museum(user_id, is_spam);
