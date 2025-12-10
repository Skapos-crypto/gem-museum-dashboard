"""
Visitor Web App - Frontend for collecting feedback
Built with Streamlit
"""

import streamlit as st
import sys
from pathlib import Path

# Add database directory to path
sys.path.append(str(Path(__file__).parent))
from database.db_manager import DatabaseManager

# Page configuration
st.set_page_config(
    page_title="Visitor Feedback System",
    page_icon="📝",
    layout="centered"
)

# Initialize database
db = DatabaseManager()

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        padding: 0.5rem;
        font-size: 1.1rem;
    }
    .success-message {
        padding: 1rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 0.25rem;
        color: #155724;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'demographics'
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'surveys_completed' not in st.session_state:
    st.session_state.surveys_completed = []

# Header
st.title("📝 Visitor Feedback System")
st.markdown("---")

# ==================== DEMOGRAPHICS PAGE ====================
def demographics_page():
    st.header("👤 Your Information")
    st.write("Please provide your basic information to get started.")
    
    with st.form("demographics_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Full Name *", placeholder="John Doe")
            email = st.text_input("Email Address *", placeholder="john@example.com")
            nationality = st.text_input("Nationality", placeholder="e.g., American")
        
        with col2:
            age = st.number_input("Age", min_value=1, max_value=120, value=25)
            gender = st.selectbox("Gender", ["", "Male", "Female", "Non-binary", "Prefer not to say"])
            language = st.selectbox("Preferred Language", 
                                   ["", "English", "Arabic", "Spanish", "French", "German", "Chinese", "Other"])
        
        submitted = st.form_submit_button("Continue to Surveys")
        
        if submitted:
            if not name or not email:
                st.error("Please fill in all required fields (*)")
            else:
                # Create user in database
                user_data = {
                    'name': name,
                    'email': email,
                    'nationality': nationality if nationality else None,
                    'age': age if age > 0 else None,
                    'gender': gender if gender else None,
                    'language': language if language else None
                }
                
                try:
                    user_id = db.create_user(user_data)
                    st.session_state.user_id = user_id
                    st.session_state.page = 'survey_selection'
                    st.rerun()
                except Exception as e:
                    st.error(f"Error saving your information: {str(e)}")

# ==================== SURVEY SELECTION PAGE ====================
def survey_selection_page():
    st.header("📋 Available Surveys")
    st.write("Please complete one or more surveys below. You can complete them all or just the ones relevant to you.")
    
    surveys = [
        {
            'name': 'General Experience',
            'key': 'general',
            'icon': '⭐',
            'description': 'Overall satisfaction, staff, cleanliness'
        },
        {
            'name': 'Exhibition Feedback',
            'key': 'exhibition',
            'icon': '🎨',
            'description': 'Content quality, educational value, exhibits'
        },
        {
            'name': 'Facilities & Amenities',
            'key': 'facilities',
            'icon': '🏢',
            'description': 'Parking, restrooms, café, accessibility'
        },
        {
            'name': 'Digital Experience',
            'key': 'digital',
            'icon': '💻',
            'description': 'Website, app, online booking, digital guides'
        }
    ]
    
    cols = st.columns(2)
    
    for idx, survey in enumerate(surveys):
        with cols[idx % 2]:
            with st.container():
                st.markdown(f"### {survey['icon']} {survey['name']}")
                st.write(survey['description'])
                
                if survey['key'] in st.session_state.surveys_completed:
                    st.success("✓ Completed")
                else:
                    if st.button(f"Start Survey", key=f"btn_{survey['key']}"):
                        st.session_state.page = survey['key']
                        st.rerun()
                
                st.markdown("---")
    
    if st.session_state.surveys_completed:
        st.success(f"✓ You've completed {len(st.session_state.surveys_completed)} survey(s)")
        
        if st.button("🎉 Finish and Submit All Feedback"):
            st.session_state.page = 'thank_you'
            st.rerun()

# ==================== GENERAL EXPERIENCE SURVEY ====================
def general_experience_survey():
    st.header("⭐ General Experience Survey")
    
    with st.form("general_experience_form"):
        st.subheader("Rate your experience (1-5 stars)")
        
        overall = st.slider("Overall Satisfaction", 1, 5, 3)
        recommend = st.slider("Would you recommend us to others?", 1, 5, 3)
        navigation = st.slider("Ease of Navigation", 1, 5, 3)
        staff = st.slider("Staff Helpfulness", 1, 5, 3)
        cleanliness = st.slider("Cleanliness", 1, 5, 3)
        
        st.subheader("Additional Feedback")
        comments = st.text_area("Any additional comments?", 
                               placeholder="Share your thoughts...")
        
        col1, col2 = st.columns(2)
        with col1:
            back = st.form_submit_button("← Back to Surveys")
        with col2:
            submit = st.form_submit_button("Submit Survey")
        
        if back:
            st.session_state.page = 'survey_selection'
            st.rerun()
        
        if submit:
            survey_data = {
                'overall_satisfaction': overall,
                'would_recommend': recommend,
                'ease_of_navigation': navigation,
                'staff_helpfulness': staff,
                'cleanliness_rating': cleanliness,
                'additional_comments': comments
            }
            
            try:
                db.submit_general_experience(st.session_state.user_id, survey_data)
                if 'general' not in st.session_state.surveys_completed:
                    st.session_state.surveys_completed.append('general')
                st.session_state.page = 'survey_selection'
                st.success("Survey submitted successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"Error submitting survey: {str(e)}")

# ==================== EXHIBITION FEEDBACK SURVEY ====================
def exhibition_feedback_survey():
    st.header("🎨 Exhibition Feedback Survey")
    
    with st.form("exhibition_feedback_form"):
        st.subheader("Rate the exhibitions (1-5 stars)")
        
        content = st.slider("Content Quality", 1, 5, 3)
        educational = st.slider("Educational Value", 1, 5, 3)
        interactive = st.slider("Interactive Elements", 1, 5, 3)
        
        st.subheader("Tell us more")
        favorite = st.text_input("What was your favorite exhibit?",
                                placeholder="e.g., Ancient Artifacts Gallery")
        improvements = st.text_area("Suggestions for improvement?",
                                   placeholder="How can we make the exhibitions better?")
        
        col1, col2 = st.columns(2)
        with col1:
            back = st.form_submit_button("← Back to Surveys")
        with col2:
            submit = st.form_submit_button("Submit Survey")
        
        if back:
            st.session_state.page = 'survey_selection'
            st.rerun()
        
        if submit:
            survey_data = {
                'content_quality': content,
                'educational_value': educational,
                'interactive_elements': interactive,
                'favorite_exhibit': favorite,
                'improvement_suggestions': improvements
            }
            
            try:
                db.submit_exhibition_feedback(st.session_state.user_id, survey_data)
                if 'exhibition' not in st.session_state.surveys_completed:
                    st.session_state.surveys_completed.append('exhibition')
                st.session_state.page = 'survey_selection'
                st.success("Survey submitted successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"Error submitting survey: {str(e)}")

# ==================== FACILITIES SURVEY ====================
def facilities_survey():
    st.header("🏢 Facilities & Amenities Survey")
    
    with st.form("facilities_form"):
        st.subheader("Rate our facilities (1-5 stars)")
        
        parking = st.slider("Parking", 1, 5, 3)
        restrooms = st.slider("Restroom Cleanliness", 1, 5, 3)
        cafe = st.slider("Café/Restaurant Quality", 1, 5, 3)
        accessibility = st.slider("Accessibility for Disabled Visitors", 1, 5, 3)
        wifi = st.slider("WiFi Quality", 1, 5, 3)
        
        st.subheader("Additional Feedback")
        comments = st.text_area("Comments about facilities?",
                               placeholder="Share your thoughts on our facilities...")
        
        col1, col2 = st.columns(2)
        with col1:
            back = st.form_submit_button("← Back to Surveys")
        with col2:
            submit = st.form_submit_button("Submit Survey")
        
        if back:
            st.session_state.page = 'survey_selection'
            st.rerun()
        
        if submit:
            survey_data = {
                'parking_rating': parking,
                'restroom_cleanliness': restrooms,
                'cafe_restaurant_quality': cafe,
                'accessibility_rating': accessibility,
                'wifi_quality': wifi,
                'facility_comments': comments
            }
            
            try:
                db.submit_facilities_survey(st.session_state.user_id, survey_data)
                if 'facilities' not in st.session_state.surveys_completed:
                    st.session_state.surveys_completed.append('facilities')
                st.session_state.page = 'survey_selection'
                st.success("Survey submitted successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"Error submitting survey: {str(e)}")

# ==================== DIGITAL EXPERIENCE SURVEY ====================
def digital_experience_survey():
    st.header("💻 Digital Experience Survey")
    
    with st.form("digital_experience_form"):
        st.subheader("Rate our digital services (1-5 stars)")
        
        mobile_app = st.slider("Mobile App", 1, 5, 3)
        website = st.slider("Website Usability", 1, 5, 3)
        booking = st.slider("Online Booking Ease", 1, 5, 3)
        guides = st.slider("Digital Guides Usefulness", 1, 5, 3)
        
        st.subheader("Additional Feedback")
        feedback = st.text_area("Comments about digital experience?",
                               placeholder="How can we improve our digital services?")
        
        col1, col2 = st.columns(2)
        with col1:
            back = st.form_submit_button("← Back to Surveys")
        with col2:
            submit = st.form_submit_button("Submit Survey")
        
        if back:
            st.session_state.page = 'survey_selection'
            st.rerun()
        
        if submit:
            survey_data = {
                'mobile_app_rating': mobile_app,
                'website_usability': website,
                'online_booking_ease': booking,
                'digital_guides_usefulness': guides,
                'digital_feedback': feedback
            }
            
            try:
                db.submit_digital_experience(st.session_state.user_id, survey_data)
                if 'digital' not in st.session_state.surveys_completed:
                    st.session_state.surveys_completed.append('digital')
                st.session_state.page = 'survey_selection'
                st.success("Survey submitted successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"Error submitting survey: {str(e)}")

# ==================== THANK YOU PAGE ====================
def thank_you_page():
    st.balloons()
    st.success("🎉 Thank You for Your Feedback!")
    
    st.markdown("""
    ### Your feedback has been submitted successfully!
    
    We greatly appreciate you taking the time to share your thoughts with us. 
    Your feedback helps us improve our services and provide better experiences for all visitors.
    
    You completed **{}** survey(s).
    """.format(len(st.session_state.surveys_completed)))
    
    if st.button("Submit More Feedback"):
        # Reset session
        st.session_state.page = 'demographics'
        st.session_state.user_id = None
        st.session_state.surveys_completed = []
        st.rerun()

# ==================== MAIN ROUTER ====================
def main():
    if st.session_state.page == 'demographics':
        demographics_page()
    elif st.session_state.page == 'survey_selection':
        survey_selection_page()
    elif st.session_state.page == 'general':
        general_experience_survey()
    elif st.session_state.page == 'exhibition':
        exhibition_feedback_survey()
    elif st.session_state.page == 'facilities':
        facilities_survey()
    elif st.session_state.page == 'digital':
        digital_experience_survey()
    elif st.session_state.page == 'thank_you':
        thank_you_page()

if __name__ == "__main__":
    main()
