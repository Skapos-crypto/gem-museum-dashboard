"""
Generate 400 realistic visitor records with varied feedback
Includes spam detection based on submission time
"""

import sqlite3
import random
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()

# Configuration
TOTAL_USERS = 400
SPAM_PERCENTAGE = 0.08  # 8% spam rate
SPAM_THRESHOLD = 10  # submissions under 10 seconds are spam

# Data options
NATIONALITIES = [
    'Egyptian', 'American', 'British', 'German', 'French', 'Italian', 'Spanish',
    'Chinese', 'Japanese', 'Korean', 'Indian', 'Brazilian', 'Australian', 'Canadian',
    'Mexican', 'Russian', 'Turkish', 'Saudi Arabian', 'Emirati', 'Qatari',
    'Kuwaiti', 'Jordanian', 'Lebanese', 'Moroccan', 'Tunisian', 'Algerian',
    'South African', 'Nigerian', 'Kenyan', 'Swedish', 'Norwegian', 'Danish',
    'Dutch', 'Belgian', 'Swiss', 'Austrian', 'Polish', 'Greek', 'Portuguese',
    'Indonesian', 'Malaysian', 'Thai', 'Vietnamese', 'Filipino', 'Singaporean'
]

LANGUAGES = [
    'English', 'Arabic', 'French', 'German', 'Spanish', 'Italian', 'Chinese',
    'Japanese', 'Korean', 'Portuguese', 'Russian', 'Turkish', 'Hindi', 'Dutch',
    'Swedish', 'Polish', 'Greek', 'Thai', 'Vietnamese', 'Indonesian'
]

EXHIBITS = ['Tutankhamun', 'Royal Mummies', 'Grand Hall', 'Pyramids Gallery', 
            'Temporary Exhibition', 'Other']

VISIT_TYPES = ['Solo', 'With Family', 'With Friends', 'Group Tour']

WAIT_TIMES = ['Less than 5 minutes', '5–15 minutes', '15–30 minutes', 'More than 30 minutes']

ISSUES = ['No issues', 'Ticketing', 'Security check', 'Signage & directions', 'Crowd congestion']

SPENDING_MOTIVATIONS = [
    "I didn't spend", 'Souvenirs / gifts', 'Food & drinks', 'Family & kids',
    'Discounts / offers', 'Just browsing'
]

FUTURE_SPENDING = [
    'Better product variety', 'Lower prices', 'More food options',
    'Kids & family zones', 'Exclusive souvenirs', 
    "Nothing, I'm just here for the exhibits"
]

HEARD_ABOUT = [
    'Social media', 'Search engines', 'Friends / Family', 'Tour company',
    'Hotel recommendation', 'Other'
]

PLATFORMS = ['Instagram', 'Facebook', 'TikTok', 'YouTube', 'Google', 'None']

EXPERIENCE_LENGTH = ['Too Short', 'Just Right', 'Too Long']

RECOMMENDATION_LIKELIHOOD = ['Not Likely', 'Maybe', 'Likely', 'Very Likely', 'Definitely']

WOULD_RECOMMEND = ['Yes', 'Maybe', 'No']

YES_NO = ['Yes', 'No']

YES_NO_MAYBE = ['Yes', 'Maybe', 'No']

LEARNED_OPTIONS = ['Yes, a lot', 'Yes, a little', 'Not really']

NO_TOUR_REASONS = [
    'Not interested', 'No time', 'Too expensive', 
    "Didn't know it was available", 'I took a self-guided visit'
]

CHILD_AGES = ['3–5 years', '6–8 years', '9–12 years', '13–15 years']

HEARD_CHILDRENS = [
    'Social media', 'Friends/Family', 'School/Teacher', 
    'GEM website', 'Walk-in', 'Other'
]

# Positive and negative comments
POSITIVE_COMMENTS = [
    "Absolutely amazing experience! The exhibits were breathtaking and well-curated.",
    "Best museum I've ever visited. The Tutankhamun collection is incredible!",
    "Staff were incredibly helpful and friendly. Highly recommend!",
    "The immersive experience was mind-blowing. Worth every penny!",
    "Beautiful facility, clean, organized, and educational. Will come again!",
    "Outstanding! The audio guide added so much value to the visit.",
    "Exceeded all expectations. The children's museum kept my kids engaged for hours.",
    "Wonderful journey through Egyptian history. A must-visit destination!",
    "The Grand Hall is magnificent. Such attention to detail everywhere.",
    "Professional service, well-managed crowds, and fascinating exhibits.",
    "Truly world-class museum. The VR experience was unforgettable!",
    "Everything was perfect from entry to exit. Thank you GEM!",
    "The Royal Mummies exhibit gave me goosebumps. Phenomenal!",
    "Great value for money. So much to see and learn.",
    "Clean facilities, great food options, and incredible artifacts.",
    "The staff went above and beyond to help us. 5 stars!",
    "Kids absolutely loved it! Educational and fun at the same time.",
    "The best way to experience Egyptian culture and history.",
    "I learned so much today. The information was clear and engaging.",
    "Will definitely return and bring more friends next time!"
]

NEGATIVE_COMMENTS = [
    "Very disappointed. Long queues and poor crowd management.",
    "Overpriced and underwhelming. Expected much more for the ticket price.",
    "Staff were unhelpful and seemed disinterested. Poor service overall.",
    "The facilities were dirty and poorly maintained. Needs improvement.",
    "Too crowded, couldn't enjoy the exhibits properly. Very frustrating experience.",
    "Audio guide didn't work half the time. Waste of money.",
    "Not suitable for young children despite being called a children's museum.",
    "Signage was confusing. Got lost multiple times inside the museum.",
    "Food was overpriced and low quality. Better options needed.",
    "VR experience was glitchy and uncomfortable. Technical issues throughout.",
    "Waited over an hour to get in. Terrible organization.",
    "Gift shop prices are ridiculous. Won't be buying anything.",
    "The exhibits felt rushed and lacked proper context or explanation.",
    "Bathrooms were filthy. Unacceptable for such a major museum.",
    "Staff were rude when I asked for help. Very disappointing.",
    "Not worth the hype. Left feeling underwhelmed and frustrated.",
    "Security checks were invasive and took forever. Poor experience.",
    "Many exhibits were closed without prior notice. False advertising.",
    "The children's area was boring and poorly designed.",
    "Would not recommend. Save your money and visit elsewhere."
]

NEUTRAL_COMMENTS = [
    "It was okay. Nothing special but not bad either.",
    "Average experience. Some parts were good, others not so much.",
    "Fine for a one-time visit, but probably won't come back.",
    "Decent museum but could use some improvements.",
    "Met my expectations, nothing more, nothing less.",
    ""
]

def generate_comment(rating, is_spam=False):
    """Generate realistic comment based on rating"""
    if is_spam:
        return random.choice(["good", "ok", "nice", "great", "cool", ""])
    
    if rating >= 4:
        return random.choice(POSITIVE_COMMENTS + [""])
    elif rating <= 2:
        return random.choice(NEGATIVE_COMMENTS + [""])
    else:
        return random.choice(NEUTRAL_COMMENTS + [""])

def generate_time_spent(is_spam=False):
    """Generate realistic time spent on survey"""
    if is_spam:
        return random.randint(3, 9)  # 3-9 seconds for spam
    else:
        return random.randint(45, 300)  # 45 seconds to 5 minutes for genuine

def weighted_rating(positive_bias=0.7):
    """Generate ratings with bias toward positive or negative"""
    if random.random() < positive_bias:
        # Positive ratings (4-5)
        return random.choice([4, 4, 4, 5, 5])
    else:
        # Mixed or negative ratings (1-3)
        return random.choice([1, 1, 2, 2, 3, 3, 3])

def generate_nps_score(overall_rating):
    """Generate NPS score based on overall rating"""
    if overall_rating >= 4:
        return random.randint(7, 10)  # Promoters
    elif overall_rating == 3:
        return random.randint(5, 8)   # Passive
    else:
        return random.randint(0, 6)   # Detractors

# Connect to database
print("🔄 Connecting to database...")
conn = sqlite3.connect('visitor_feedback.db')
cursor = conn.cursor()

# Apply new schema
print("📋 Applying new schema...")
with open('database/new_schema.sql', 'r', encoding='utf-8') as f:
    schema_sql = f.read()
    cursor.executescript(schema_sql)

print(f"✅ Schema applied successfully!\n")
print(f"🎯 Generating {TOTAL_USERS} users with realistic feedback...")
print(f"📊 Target: ~{int(TOTAL_USERS * SPAM_PERCENTAGE)} spam records (~{SPAM_PERCENTAGE*100}%)\n")

# Determine which users will be spammers
spam_user_ids = random.sample(range(1, TOTAL_USERS + 1), int(TOTAL_USERS * SPAM_PERCENTAGE))

# Statistics
stats = {
    'users': 0,
    'overall': 0,
    'service': 0,
    'tour': 0,
    'facilities': 0,
    'marketing': 0,
    'immersive': 0,
    'childrens': 0,
    'spam_count': 0
}

# Generate users and surveys
start_date = datetime.now() - timedelta(days=90)

for i in range(1, TOTAL_USERS + 1):
    is_spam_user = i in spam_user_ids
    
    # Generate user
    name = fake.name()
    email = fake.email()
    nationality = random.choice(NATIONALITIES)
    age = random.randint(18, 75)
    language = random.choice(LANGUAGES)
    gender = random.choice(['Male', 'Female', 'Other'])
    
    cursor.execute('''
        INSERT INTO users (email, name, nationality, age, language, gender, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (email, name, nationality, age, language, gender, 
          start_date + timedelta(hours=random.randint(0, 2160))))
    
    user_id = cursor.lastrowid
    stats['users'] += 1
    
    # Determine survey participation (80-100% participation rate)
    surveys_to_fill = random.randint(3, 7)  # Fill 3 to all 7 surveys
    available_surveys = [1, 2, 3, 4, 5, 6, 7]
    selected_surveys = random.sample(available_surveys, surveys_to_fill)
    
    # Survey 1: Overall Experience (85% participation)
    if 1 in selected_surveys:
        time_spent = generate_time_spent(is_spam_user)
        is_spam = 1 if time_spent < SPAM_THRESHOLD else 0
        if is_spam:
            stats['spam_count'] += 1
        
        rating = random.randint(1, 5) if is_spam_user else weighted_rating()
        nps = generate_nps_score(rating)
        
        cursor.execute('''
            INSERT INTO survey_overall_experience 
            (user_id, overall_rating, favorite_exhibit, visit_type, nps_score, 
             additional_comments, time_spent_seconds, is_spam, submitted_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, rating, random.choice(EXHIBITS), random.choice(VISIT_TYPES),
              nps, generate_comment(rating, is_spam_user), time_spent, is_spam,
              start_date + timedelta(hours=random.randint(0, 2160))))
        stats['overall'] += 1
    
    # Survey 2: Service & Operations (75% participation)
    if 2 in selected_surveys:
        time_spent = generate_time_spent(is_spam_user)
        is_spam = 1 if time_spent < SPAM_THRESHOLD else 0
        if is_spam:
            stats['spam_count'] += 1
        
        rating = random.randint(1, 5) if is_spam_user else weighted_rating()
        
        cursor.execute('''
            INSERT INTO survey_service_operations
            (user_id, staff_hospitality_rating, cleanliness_rating, 
             crowd_management_rating, entry_wait_time, issues_faced,
             additional_comments, time_spent_seconds, is_spam, submitted_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, rating, weighted_rating(), weighted_rating(),
              random.choice(WAIT_TIMES), random.choice(ISSUES),
              generate_comment(rating, is_spam_user), time_spent, is_spam,
              start_date + timedelta(hours=random.randint(0, 2160))))
        stats['service'] += 1
    
    # Survey 3: Tour & Educational (65% participation)
    if 3 in selected_surveys:
        time_spent = generate_time_spent(is_spam_user)
        is_spam = 1 if time_spent < SPAM_THRESHOLD else 0
        if is_spam:
            stats['spam_count'] += 1
        
        used_guide = random.choice(YES_NO)
        rating = random.randint(1, 5) if is_spam_user else weighted_rating()
        
        cursor.execute('''
            INSERT INTO survey_tour_educational
            (user_id, used_audio_guide, tour_experience_rating, 
             information_clarity_rating, learned_something, no_tour_reason,
             additional_comments, time_spent_seconds, is_spam, submitted_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, used_guide, 
              rating if used_guide == 'Yes' else None,
              weighted_rating() if used_guide == 'Yes' else None,
              random.choice(LEARNED_OPTIONS),
              random.choice(NO_TOUR_REASONS) if used_guide == 'No' else None,
              generate_comment(rating, is_spam_user), time_spent, is_spam,
              start_date + timedelta(hours=random.randint(0, 2160))))
        stats['tour'] += 1
    
    # Survey 4: Facilities & Spending (80% participation)
    if 4 in selected_surveys:
        time_spent = generate_time_spent(is_spam_user)
        is_spam = 1 if time_spent < SPAM_THRESHOLD else 0
        if is_spam:
            stats['spam_count'] += 1
        
        rating = random.randint(1, 5) if is_spam_user else weighted_rating()
        
        cursor.execute('''
            INSERT INTO survey_facilities_spending
            (user_id, spending_motivation, facilities_rating, 
             future_spending_driver, additional_comments, 
             time_spent_seconds, is_spam, submitted_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, random.choice(SPENDING_MOTIVATIONS), rating,
              random.choice(FUTURE_SPENDING),
              generate_comment(rating, is_spam_user), time_spent, is_spam,
              start_date + timedelta(hours=random.randint(0, 2160))))
        stats['facilities'] += 1
    
    # Survey 5: Marketing & Loyalty (70% participation)
    if 5 in selected_surveys:
        time_spent = generate_time_spent(is_spam_user)
        is_spam = 1 if time_spent < SPAM_THRESHOLD else 0
        if is_spam:
            stats['spam_count'] += 1
        
        cursor.execute('''
            INSERT INTO survey_marketing_loyalty
            (user_id, heard_about_gem, platform_influence, first_visit,
             would_visit_again, would_follow_social, additional_comments,
             time_spent_seconds, is_spam, submitted_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, random.choice(HEARD_ABOUT), random.choice(PLATFORMS),
              random.choice(YES_NO), random.choice(['Definitely', 'Maybe', 'Unlikely']),
              random.choice(YES_NO_MAYBE), 
              random.choice(POSITIVE_COMMENTS + NEGATIVE_COMMENTS + [""]),
              time_spent, is_spam,
              start_date + timedelta(hours=random.randint(0, 2160))))
        stats['marketing'] += 1
    
    # Survey 6: Immersive Experience (40% participation - specialty)
    if 6 in selected_surveys:
        time_spent = generate_time_spent(is_spam_user)
        is_spam = 1 if time_spent < SPAM_THRESHOLD else 0
        if is_spam:
            stats['spam_count'] += 1
        
        rating = random.randint(1, 5) if is_spam_user else weighted_rating()
        
        cursor.execute('''
            INSERT INTO survey_immersive_experience
            (user_id, overall_immersive_rating, equipment_comfort_rating,
             experience_length, storytelling_satisfaction, value_for_money_rating,
             recommendation_likelihood, additional_comments,
             time_spent_seconds, is_spam, submitted_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, rating, weighted_rating(), random.choice(EXPERIENCE_LENGTH),
              weighted_rating(), weighted_rating(),
              random.choice(RECOMMENDATION_LIKELIHOOD),
              generate_comment(rating, is_spam_user), time_spent, is_spam,
              start_date + timedelta(hours=random.randint(0, 2160))))
        stats['immersive'] += 1
    
    # Survey 7: Children's Museum (30% participation - family-focused)
    if 7 in selected_surveys and random.random() < 0.3:
        time_spent = generate_time_spent(is_spam_user)
        is_spam = 1 if time_spent < SPAM_THRESHOLD else 0
        if is_spam:
            stats['spam_count'] += 1
        
        rating = random.randint(1, 5) if is_spam_user else weighted_rating()
        
        cursor.execute('''
            INSERT INTO survey_childrens_museum
            (user_id, overall_experience_rating, age_appropriateness_rating,
             educational_value_rating, fun_entertainment_rating, interactivity_rating,
             instructions_clarity_rating, staff_support_rating, cleanliness_rating,
             value_for_money_rating, would_recommend, heard_about_us,
             child_age_group, additional_comments, time_spent_seconds, is_spam, submitted_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, rating, weighted_rating(), weighted_rating(),
              weighted_rating(), weighted_rating(), weighted_rating(),
              weighted_rating(), weighted_rating(), weighted_rating(),
              random.choice(WOULD_RECOMMEND), random.choice(HEARD_CHILDRENS),
              ','.join(random.sample(CHILD_AGES, random.randint(1, 2))),
              generate_comment(rating, is_spam_user), time_spent, is_spam,
              start_date + timedelta(hours=random.randint(0, 2160))))
        stats['childrens'] += 1
    
    # Progress indicator
    if i % 50 == 0:
        print(f"  ✓ Generated {i}/{TOTAL_USERS} users...")

conn.commit()

# Display statistics
print(f"\n{'='*60}")
print(f"✅ DATA GENERATION COMPLETE!")
print(f"{'='*60}\n")

print(f"📊 STATISTICS:")
print(f"{'─'*60}")
print(f"  👥 Users created:                    {stats['users']}")
print(f"  📋 Survey responses:")
print(f"     ├─ Overall Experience:            {stats['overall']}")
print(f"     ├─ Service & Operations:          {stats['service']}")
print(f"     ├─ Tour & Educational:            {stats['tour']}")
print(f"     ├─ Facilities & Spending:         {stats['facilities']}")
print(f"     ├─ Marketing & Loyalty:           {stats['marketing']}")
print(f"     ├─ Immersive Experience:          {stats['immersive']}")
print(f"     └─ Children's Museum:             {stats['childrens']}")
print(f"\n  📝 Total survey responses:           {sum([stats['overall'], stats['service'], stats['tour'], stats['facilities'], stats['marketing'], stats['immersive'], stats['childrens']])}")
print(f"  🚫 Spam records flagged:             {stats['spam_count']}")
print(f"  ✓  Valid records:                    {sum([stats['overall'], stats['service'], stats['tour'], stats['facilities'], stats['marketing'], stats['immersive'], stats['childrens']]) - stats['spam_count']}")

# Get actual spam count
cursor.execute('''
    SELECT 
        (SELECT COUNT(*) FROM survey_overall_experience WHERE is_spam=1) +
        (SELECT COUNT(*) FROM survey_service_operations WHERE is_spam=1) +
        (SELECT COUNT(*) FROM survey_tour_educational WHERE is_spam=1) +
        (SELECT COUNT(*) FROM survey_facilities_spending WHERE is_spam=1) +
        (SELECT COUNT(*) FROM survey_marketing_loyalty WHERE is_spam=1) +
        (SELECT COUNT(*) FROM survey_immersive_experience WHERE is_spam=1) +
        (SELECT COUNT(*) FROM survey_childrens_museum WHERE is_spam=1) as total_spam
''')

actual_spam = cursor.fetchone()[0]
print(f"  🔍 Actual spam in database:          {actual_spam}")

# Sample data check
print(f"\n{'─'*60}")
print(f"📋 SAMPLE DATA CHECK:\n")

cursor.execute("SELECT COUNT(*) FROM users")
print(f"  Users table: {cursor.fetchone()[0]} records")

cursor.execute("SELECT COUNT(*) FROM survey_overall_experience")
print(f"  Overall Experience: {cursor.fetchone()[0]} records")

cursor.execute("SELECT COUNT(*) FROM survey_overall_experience WHERE is_spam=0")
print(f"    └─ Valid (non-spam): {cursor.fetchone()[0]} records")

cursor.execute('''
    SELECT overall_rating, COUNT(*) 
    FROM survey_overall_experience 
    WHERE is_spam=0 
    GROUP BY overall_rating 
    ORDER BY overall_rating
''')
print(f"\n  📊 Rating Distribution (non-spam):")
for rating, count in cursor.fetchall():
    bar = '█' * (count // 10)
    print(f"    {rating} ⭐: {count:3d} {bar}")

print(f"\n{'='*60}")
print(f"🎉 Database ready! Use the dashboard to explore the data.")
print(f"{'='*60}\n")

conn.close()
