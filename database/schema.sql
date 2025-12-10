-- Database Schema for Visitor Feedback System
-- Created: December 9, 2025

-- Table 1: User Demographics
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    nationality VARCHAR(100),
    age INTEGER,
    language VARCHAR(50),
    gender VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table 2: General Experience Survey
CREATE TABLE IF NOT EXISTS survey_general_experience (
    response_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    overall_satisfaction INTEGER CHECK(overall_satisfaction BETWEEN 1 AND 5),
    would_recommend INTEGER CHECK(would_recommend BETWEEN 1 AND 5),
    ease_of_navigation INTEGER CHECK(ease_of_navigation BETWEEN 1 AND 5),
    staff_helpfulness INTEGER CHECK(staff_helpfulness BETWEEN 1 AND 5),
    cleanliness_rating INTEGER CHECK(cleanliness_rating BETWEEN 1 AND 5),
    additional_comments TEXT,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- Table 3: Exhibition Feedback Survey
CREATE TABLE IF NOT EXISTS survey_exhibition_feedback (
    response_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    content_quality INTEGER CHECK(content_quality BETWEEN 1 AND 5),
    educational_value INTEGER CHECK(educational_value BETWEEN 1 AND 5),
    interactive_elements INTEGER CHECK(interactive_elements BETWEEN 1 AND 5),
    favorite_exhibit TEXT,
    improvement_suggestions TEXT,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- Table 4: Facilities & Amenities Survey
CREATE TABLE IF NOT EXISTS survey_facilities (
    response_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    parking_rating INTEGER CHECK(parking_rating BETWEEN 1 AND 5),
    restroom_cleanliness INTEGER CHECK(restroom_cleanliness BETWEEN 1 AND 5),
    cafe_restaurant_quality INTEGER CHECK(cafe_restaurant_quality BETWEEN 1 AND 5),
    accessibility_rating INTEGER CHECK(accessibility_rating BETWEEN 1 AND 5),
    wifi_quality INTEGER CHECK(wifi_quality BETWEEN 1 AND 5),
    facility_comments TEXT,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- Table 5: Digital Experience Survey
CREATE TABLE IF NOT EXISTS survey_digital_experience (
    response_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    mobile_app_rating INTEGER CHECK(mobile_app_rating BETWEEN 1 AND 5),
    website_usability INTEGER CHECK(website_usability BETWEEN 1 AND 5),
    online_booking_ease INTEGER CHECK(online_booking_ease BETWEEN 1 AND 5),
    digital_guides_usefulness INTEGER CHECK(digital_guides_usefulness BETWEEN 1 AND 5),
    digital_feedback TEXT,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- Consolidated View: Merging all feedbacks
CREATE VIEW IF NOT EXISTS consolidated_feedback AS
SELECT 
    u.user_id,
    u.email,
    u.name,
    u.nationality,
    u.age,
    u.language,
    u.gender,
    u.created_at as user_registered_at,
    
    -- General Experience
    ge.response_id as general_response_id,
    ge.overall_satisfaction,
    ge.would_recommend,
    ge.ease_of_navigation,
    ge.staff_helpfulness,
    ge.cleanliness_rating,
    ge.additional_comments,
    ge.submitted_at as general_submitted_at,
    
    -- Exhibition Feedback
    ef.response_id as exhibition_response_id,
    ef.content_quality,
    ef.educational_value,
    ef.interactive_elements,
    ef.favorite_exhibit,
    ef.improvement_suggestions,
    ef.submitted_at as exhibition_submitted_at,
    
    -- Facilities
    f.response_id as facilities_response_id,
    f.parking_rating,
    f.restroom_cleanliness,
    f.cafe_restaurant_quality,
    f.accessibility_rating,
    f.wifi_quality,
    f.facility_comments,
    f.submitted_at as facilities_submitted_at,
    
    -- Digital Experience
    de.response_id as digital_response_id,
    de.mobile_app_rating,
    de.website_usability,
    de.online_booking_ease,
    de.digital_guides_usefulness,
    de.digital_feedback,
    de.submitted_at as digital_submitted_at
    
FROM users u
LEFT JOIN survey_general_experience ge ON u.user_id = ge.user_id
LEFT JOIN survey_exhibition_feedback ef ON u.user_id = ef.user_id
LEFT JOIN survey_facilities f ON u.user_id = f.user_id
LEFT JOIN survey_digital_experience de ON u.user_id = de.user_id;

-- Indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_nationality ON users(nationality);
CREATE INDEX IF NOT EXISTS idx_survey_general_user ON survey_general_experience(user_id);
CREATE INDEX IF NOT EXISTS idx_survey_exhibition_user ON survey_exhibition_feedback(user_id);
CREATE INDEX IF NOT EXISTS idx_survey_facilities_user ON survey_facilities(user_id);
CREATE INDEX IF NOT EXISTS idx_survey_digital_user ON survey_digital_experience(user_id);
