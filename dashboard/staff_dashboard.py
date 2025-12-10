"""
GEM Staff Dashboard - Analytics and Reporting
Displays visitor feedback with spam detection and sentiment analysis
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import sqlite3
from io import BytesIO
import sys
sys.path.append('.')
from sentiment_analysis import (
    AdvancedSentimentAnalyzer, 
    AdvancedTopicModeler, 
    analyze_comments_advanced,
    generate_recommendations
)

# Page configuration
st.set_page_config(
    page_title="GEM Staff Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main > div {padding-top: 2rem;}
    .stMetric {background-color: #f0f2f6; padding: 15px; border-radius: 10px;}
    h1 {color: #1f77b4;}
    h2 {color: #ff7f0e;}
    .spam-warning {background-color: #ffebee; padding: 10px; border-radius: 5px; border-left: 4px solid #f44336;}
    .recommendation {background-color: #f1f8e9; padding: 10px; border-radius: 5px; margin: 5px 0;}
    
    /* GEM Museum colors for sidebar Quick Stats only */
    [data-testid="stSidebar"] .stMetric {
        background: linear-gradient(135deg, #E8DCC8 0%, #D4C4A8 100%);
        padding: 18px;
        border-radius: 12px;
        border-left: 4px solid #1F4788;
        box-shadow: 0 2px 8px rgba(31, 71, 136, 0.15);
    }
    [data-testid="stSidebar"] .stMetric label {
        color: #2C1810 !important;
        font-weight: 600;
    }
    [data-testid="stSidebar"] .stMetric [data-testid="stMetricValue"] {
        color: #1F4788 !important;
        font-weight: 700;
    }
    </style>
""", unsafe_allow_html=True)

# Database connection
@st.cache_resource
def get_db_connection():
    return sqlite3.connect('visitor_feedback.db', check_same_thread=False)

# Data loading functions
@st.cache_data(ttl=60)
def load_data(table_name, include_spam=False):
    """Load data from specific survey table"""
    conn = get_db_connection()
    query = f"SELECT * FROM {table_name}"
    if not include_spam:
        query += " WHERE is_spam = 0"
    df = pd.read_sql_query(query, conn)
    return df

@st.cache_data(ttl=60)
def load_users():
    """Load user demographics"""
    conn = get_db_connection()
    df = pd.read_sql_query("SELECT * FROM users", conn)
    return df

def get_survey_stats():
    """Get statistics for all surveys"""
    conn = get_db_connection()
    
    tables = {
        'Overall Experience': 'survey_overall_experience',
        'Service & Operations': 'survey_service_operations',
        'Tour & Educational': 'survey_tour_educational',
        'Facilities & Spending': 'survey_facilities_spending',
        'Marketing & Loyalty': 'survey_marketing_loyalty',
        'Tut Immersive Experience': 'survey_immersive_experience',
        "Children's Museum": 'survey_childrens_museum'
    }
    
    stats = {}
    for name, table in tables.items():
        cursor = conn.cursor()
        cursor.execute(f"SELECT COUNT(*) as total, SUM(is_spam) as spam FROM {table}")
        row = cursor.fetchone()
        stats[name] = {'total': row[0], 'spam': row[1] or 0, 'valid': row[0] - (row[1] or 0)}
    
    return stats

# Header
st.title("📊 GEM Staff Dashboard")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    include_spam = st.checkbox("Include spam data", value=False)
    
    st.markdown("---")
    st.header("📋 Quick Stats")
    
    try:
        users_df = load_users()
        st.metric("Total Visitors", len(users_df))
        
        stats = get_survey_stats()
        total_responses = sum(s['total'] for s in stats.values())
        total_spam = sum(s['spam'] for s in stats.values())
        spam_rate = (total_spam / total_responses * 100) if total_responses > 0 else 0
        
        st.metric("Total Responses", total_responses, 
                 delta=f"-{spam_rate:.1f}% spam", 
                 delta_color="inverse")
        
        avg_responses = total_responses / len(users_df) if len(users_df) > 0 else 0
        st.metric("Avg Responses/Visitor", f"{avg_responses:.1f}")
        
    except Exception as e:
        st.error(f"Error: {str(e)}")

# Main tabs
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📊 Overview", 
    "👥 Demographics", 
    "⭐ Survey Analysis",
    "🎮 Loyalty Points",
    "🔍 Spam Detection",
    "📈 Marketing",
    "💾 Export"
])

# TAB 1: OVERVIEW
with tab1:
    st.header("Dashboard Overview")
    
    try:
        stats = get_survey_stats()
        col1, col2, col3 = st.columns(3)
        
        for i, (name, s) in enumerate(stats.items()):
            col = [col1, col2, col3][i % 3]
            with col:
                st.metric(name, f"{s['total']}", delta=f"↓ {s['spam']} spam" if s['spam'] > 0 else "No spam", delta_color="inverse")
        
        st.markdown("---")
        st.subheader("Survey Participation")
        
        chart_data = pd.DataFrame([{'Survey': name, 'Responses': s['valid']} for name, s in stats.items()])
        chart_data = chart_data.sort_values('Responses', ascending=False)
        
        fig = px.bar(chart_data, x='Survey', y='Responses', color='Responses', color_continuous_scale='Teal')
        fig.update_xaxes(tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("Overall Experience Ratings")
        
        overall_df = load_data('survey_overall_experience', include_spam)
        if not overall_df.empty:
            col1, col2 = st.columns(2)
            
            with col1:
                rating_counts = overall_df['overall_rating'].value_counts().sort_index()
                colors = ['#d32f2f', '#ff6f00', '#fbc02d', '#7cb342', '#388e3c']
                fig = go.Figure(data=[go.Bar(x=rating_counts.index, y=rating_counts.values, marker_color=[colors[int(r)-1] for r in rating_counts.index])])
                fig.update_layout(title='Overall Rating Distribution', xaxis_title='Rating', yaxis_title='Count')
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                if 'nps_score' in overall_df.columns:
                    avg_nps = overall_df['nps_score'].mean()
                    detractors = len(overall_df[overall_df['nps_score'] <= 6])
                    passives = len(overall_df[(overall_df['nps_score'] >= 7) & (overall_df['nps_score'] <= 8)])
                    promoters = len(overall_df[overall_df['nps_score'] >= 9])
                    
                    fig = go.Figure(data=[go.Pie(labels=['Promoters', 'Passives', 'Detractors'], values=[promoters, passives, detractors], hole=.6, marker_colors=['#4caf50', '#ffc107', '#f44336'])])
                    fig.update_layout(title=f'NPS<br><sub>Avg: {avg_nps:.1f}/10</sub>', annotations=[dict(text=f'{avg_nps:.1f}', x=0.5, y=0.5, font_size=40, showarrow=False)])
                    st.plotly_chart(fig, use_container_width=True)
        
    except Exception as e:
        st.error(f"Error: {str(e)}")

# TAB 2: DEMOGRAPHICS
with tab2:
    st.header("Visitor Demographics")
    
    try:
        users_df = load_users()
        # Remove "Other" gender from data
        users_df = users_df[users_df['gender'] != 'Other']
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Top 10 Nationalities by Gender")
            # Get top 10 nationalities
            top_nationalities = users_df['nationality'].value_counts().head(10).index
            nat_gender_df = users_df[users_df['nationality'].isin(top_nationalities)]
            
            # Create stacked bar data
            nat_gender_counts = nat_gender_df.groupby(['nationality', 'gender']).size().reset_index(name='count')
            nat_gender_counts = nat_gender_counts.sort_values('count', ascending=True)
            
            fig = px.bar(nat_gender_counts, y='nationality', x='count', color='gender',
                        orientation='h',
                        color_discrete_map={'Male': '#2196f3', 'Female': '#e91e63'},
                        barmode='stack')
            fig.update_layout(xaxis_title='Count', yaxis_title='Nationality')
            st.plotly_chart(fig, use_container_width=True)
            
            st.subheader("Gender Distribution")
            gender_counts = users_df['gender'].value_counts()
            fig = px.pie(values=gender_counts.values, names=gender_counts.index, 
                        hole=0.4, color_discrete_sequence=['#2196f3', '#e91e63'])
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Age Distribution")
            fig = px.histogram(users_df, x='age', nbins=20, color_discrete_sequence=['#1f77b4'])
            fig.update_traces(marker_line_width=2, marker_line_color='white')
            fig.update_layout(bargap=0.2)
            st.plotly_chart(fig, use_container_width=True)
            
            st.subheader("Top 10 Languages by Gender")
            # Get top 10 languages
            top_languages = users_df['language'].value_counts().head(10).index
            lang_gender_df = users_df[users_df['language'].isin(top_languages)]
            
            # Create stacked bar data
            lang_gender_counts = lang_gender_df.groupby(['language', 'gender']).size().reset_index(name='count')
            lang_gender_counts = lang_gender_counts.sort_values('count', ascending=True)
            
            fig = px.bar(lang_gender_counts, y='language', x='count', color='gender',
                        orientation='h',
                        color_discrete_map={'Male': '#2196f3', 'Female': '#e91e63'},
                        barmode='stack')
            fig.update_layout(xaxis_title='Count', yaxis_title='Language')
            st.plotly_chart(fig, use_container_width=True)
        
    except Exception as e:
        st.error(f"Error: {str(e)}")

# TAB 3: SURVEY ANALYSIS
with tab3:
    st.header("Survey Analysis")
    
    try:
        overall_df = load_data('survey_overall_experience', include_spam)
        service_df = load_data('survey_service_operations', include_spam)
        tour_df = load_data('survey_tour_educational', include_spam)
        facilities_df = load_data('survey_facilities_spending', include_spam)
        immersive_df = load_data('survey_immersive_experience', include_spam)
        childrens_df = load_data('survey_childrens_museum', include_spam)
        
        ratings_data = []
        if not overall_df.empty:
            ratings_data.append({'Category': 'Overall Experience', 'Rating': overall_df['overall_rating'].mean()})
        if not service_df.empty:
            ratings_data.append({'Category': 'Staff Hospitality', 'Rating': service_df['staff_hospitality_rating'].mean()})
            ratings_data.append({'Category': 'Cleanliness', 'Rating': service_df['cleanliness_rating'].mean()})
            ratings_data.append({'Category': 'Crowd Management', 'Rating': service_df['crowd_management_rating'].mean()})
        if not tour_df.empty:
            tour_ratings = tour_df['tour_experience_rating'].dropna()
            if len(tour_ratings) > 0:
                ratings_data.append({'Category': 'Tour Experience', 'Rating': tour_ratings.mean()})
        if not facilities_df.empty:
            ratings_data.append({'Category': 'Facilities', 'Rating': facilities_df['facilities_rating'].mean()})
        if not immersive_df.empty:
            ratings_data.append({'Category': 'Tut Immersive', 'Rating': immersive_df['overall_immersive_rating'].mean()})
        if not childrens_df.empty:
            ratings_data.append({'Category': "Children's Museum", 'Rating': childrens_df['overall_experience_rating'].mean()})
        
        if ratings_data:
            ratings_df = pd.DataFrame(ratings_data).sort_values('Rating', ascending=True)
            overall_avg = ratings_df['Rating'].mean()
            
            fig = px.bar(ratings_df, y='Category', x='Rating', orientation='h', color='Rating', color_continuous_scale='RdYlGn', range_x=[0, 5])
            fig.add_vline(x=overall_avg, line_dash="dash", line_color="gray", annotation_text=f"{overall_avg:.2f}")
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        st.subheader("Detailed Survey Responses")
        
        survey_type = st.selectbox("Select Survey", ["Overall Experience", "Service & Operations", "Tour & Educational", "Facilities & Spending", "Marketing & Loyalty", "Tut Immersive Experience", "Children's Museum"])
        
        table_map = {"Overall Experience": "survey_overall_experience", "Service & Operations": "survey_service_operations", "Tour & Educational": "survey_tour_educational", "Facilities & Spending": "survey_facilities_spending", "Marketing & Loyalty": "survey_marketing_loyalty", "Tut Immersive Experience": "survey_immersive_experience", "Children's Museum": "survey_childrens_museum"}
        
        df = load_data(table_map[survey_type], include_spam)
        
        if not df.empty:
            st.metric("Total Responses", len(df))
            st.dataframe(df, use_container_width=True)
            
            comment_cols = [col for col in df.columns if 'comment' in col.lower()]
            if comment_cols:
                st.markdown("---")
                st.subheader("💡 Advanced Insights & Recommendations")
                
                for col in comment_cols:
                    comments = df[col].dropna()
                    if len(comments) > 5:  # Need at least 5 comments for meaningful analysis
                        st.markdown(f"### {col.replace('_', ' ').title()}")
                        
                        # Run advanced sentiment analysis
                        analysis_results = analyze_comments_advanced(comments)
                        summary = analysis_results['summary']
                        topics_df = analysis_results['topics']
                        
                        # Display sentiment metrics with ratings
                        col1, col2, col3, col4 = st.columns(4)
                        
                        with col1:
                            st.metric("😊 Positive", summary['positive'], 
                                     delta=f"{summary['positive']/summary['total_comments']*100:.1f}%")
                        with col2:
                            st.metric("😐 Neutral", summary['neutral'])
                        with col3:
                            st.metric("😞 Negative", summary['negative'],
                                     delta=f"-{summary['negative']/summary['total_comments']*100:.1f}%",
                                     delta_color="inverse")
                        with col4:
                            st.metric("📊 Avg Rating", f"{summary['avg_rating']:.2f}/5",
                                     delta=f"{summary['avg_confidence']:.0f}% confidence")
                        
                        # Display topic analysis
                        if topics_df is not None and not topics_df.empty:
                            st.markdown("**🔑 Key Topics Identified:**")
                            
                            # Show top 5 topics with bar chart
                            top_topics = topics_df.head(5)
                            fig = px.bar(top_topics, x='Total_Score', y='Topic', 
                                        orientation='h',
                                        color='Total_Score',
                                        color_continuous_scale='Viridis',
                                        text='Mentions')
                            fig.update_traces(texttemplate='%{text} mentions', textposition='outside')
                            fig.update_layout(showlegend=False, height=300)
                            st.plotly_chart(fig, use_container_width=True)
                        
                        # Generate and display recommendations
                        recommendations = generate_recommendations(summary, topics_df)
                        
                        if recommendations:
                            st.markdown("**🎯 Actionable Recommendations:**")
                            
                            for rec in recommendations:
                                priority_colors = {
                                    'HIGH': '#ffebee',
                                    'MEDIUM': '#fff3e0',
                                    'OPPORTUNITY': '#e8f5e9'
                                }
                                bg_color = priority_colors.get(rec['priority'], '#f5f5f5')
                                
                                st.markdown(f"""
                                <div style="background-color: {bg_color}; padding: 15px; border-radius: 8px; margin: 10px 0; border-left: 4px solid #2196f3;">
                                    <div style="display: flex; justify-content: space-between;">
                                        <strong>{rec['icon']} {rec['category']}</strong>
                                        <span style="background-color: white; padding: 2px 8px; border-radius: 4px; font-size: 12px;">
                                            {rec['priority']}
                                        </span>
                                    </div>
                                    <p style="margin: 5px 0;"><strong>Issue:</strong> {rec['issue']}</p>
                                    <p style="margin: 5px 0;"><strong>Action:</strong> {rec['action']}</p>
                                </div>
                                """, unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"Error: {str(e)}")

# TAB 4: LOYALTY POINTS
with tab4:
    st.header("🎮 Loyalty Points System")
    
    try:
        conn = get_db_connection()
        
        # Get loyalty analytics
        analytics_query = "SELECT * FROM loyalty_analytics"
        analytics_df = pd.read_sql_query(analytics_query, conn)
        
        if not analytics_df.empty:
            analytics = analytics_df.iloc[0]
            
            st.subheader("📊 Program Overview")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Users Enrolled", f"{int(analytics['total_users_enrolled']):,}")
            with col2:
                st.metric("Users with Points", f"{int(analytics['users_with_points']):,}")
            with col3:
                st.metric("Total Points Distributed", f"{int(analytics['total_points_distributed']):,}")
            with col4:
                st.metric("Avg Points per User", f"{analytics['avg_points_per_user']:.1f}")
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Redemptions", f"{int(analytics['total_redemptions']):,}")
            with col2:
                st.metric("Users Who Redeemed", f"{int(analytics['users_who_redeemed']):,}")
            with col3:
                st.metric("Redemption Rate", f"{analytics['redemption_rate_percent']:.1f}%")
            with col4:
                st.metric("Points Redeemed", f"{int(analytics['total_points_redeemed']):,}")
            
            st.markdown("---")
            
            # Points Sources Breakdown
            st.subheader("💰 Points Distribution")
            col1, col2 = st.columns(2)
            
            with col1:
                # Points by source
                sources_query = """
                    SELECT 
                        SUM(points_from_surveys) as from_surveys,
                        SUM(points_from_referrals) as from_referrals,
                        SUM(points_from_profile_completion) as from_profile
                    FROM user_points
                """
                sources_df = pd.read_sql_query(sources_query, conn)
                
                if not sources_df.empty:
                    sources = sources_df.iloc[0]
                    source_data = pd.DataFrame({
                        'Source': ['Surveys', 'Referrals', 'Profile Completion'],
                        'Points': [sources['from_surveys'] or 0, sources['from_referrals'] or 0, sources['from_profile'] or 0]
                    })
                    
                    fig = px.bar(source_data, x='Source', y='Points', 
                                title='Points Earned by Source',
                                color='Source',
                                color_discrete_map={
                                    'Surveys': '#2196F3',
                                    'Referrals': '#4CAF50',
                                    'Profile Completion': '#FF9800'
                                })
                    st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Badge distribution
                badge_query = """
                    SELECT 
                        CASE 
                            WHEN total_points_earned >= 120 THEN 'Legend'
                            WHEN total_points_earned >= 60 THEN 'Guardian'
                            WHEN total_points_earned >= 20 THEN 'Explorer'
                            ELSE 'None'
                        END as badge_level,
                        COUNT(*) as count
                    FROM user_points
                    GROUP BY badge_level
                    ORDER BY 
                        CASE badge_level
                            WHEN 'Legend' THEN 1
                            WHEN 'Guardian' THEN 2
                            WHEN 'Explorer' THEN 3
                            ELSE 4
                        END
                """
                badge_data = pd.read_sql_query(badge_query, conn)
                
                fig = px.funnel(badge_data, x='count', y='badge_level',
                              title='Badge Progression Funnel',
                              color='badge_level',
                              color_discrete_map={
                                  'Legend': '#FFD700',
                                  'Guardian': '#C0C0C0',
                                  'Explorer': '#CD7F32',
                                  'None': '#9E9E9E'
                              })
                st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("---")
            
            # Top Users and Rewards
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("🏆 Top 10 Users by Points")
                top_users_query = """
                    SELECT 
                        u.name,
                        up.current_points_balance,
                        up.total_points_earned,
                        up.surveys_completed,
                        CASE 
                            WHEN up.total_points_earned >= 120 THEN '🥇 Legend'
                            WHEN up.total_points_earned >= 60 THEN '🥈 Guardian'
                            WHEN up.total_points_earned >= 20 THEN '🥉 Explorer'
                            ELSE '⭐ None'
                        END as badge
                    FROM user_points up
                    JOIN users u ON up.user_id = u.user_id
                    ORDER BY up.current_points_balance DESC
                    LIMIT 10
                """
                top_users = pd.read_sql_query(top_users_query, conn)
                top_users.columns = ['Name', 'Balance', 'Total Earned', 'Surveys', 'Badge']
                st.dataframe(top_users, use_container_width=True, hide_index=True)
            
            with col2:
                st.subheader("🎁 Rewards Catalog")
                rewards_query = """
                    SELECT 
                        reward_name,
                        reward_category,
                        points_required,
                        COALESCE(redemptions, 0) as times_redeemed
                    FROM rewards_catalog rc
                    LEFT JOIN (
                        SELECT reward_id, COUNT(*) as redemptions
                        FROM redemption_history
                        GROUP BY reward_id
                    ) rh ON rc.reward_id = rh.reward_id
                    ORDER BY points_required
                """
                rewards = pd.read_sql_query(rewards_query, conn)
                rewards.columns = ['Reward', 'Category', 'Points', 'Redeemed']
                st.dataframe(rewards, use_container_width=True, hide_index=True)
            
            st.markdown("---")
            
            # Transaction History
            st.subheader("📜 Recent Transactions")
            transactions_query = """
                SELECT 
                    pt.created_at,
                    u.name,
                    pt.transaction_type,
                    pt.points_change,
                    pt.balance_after,
                    pt.description
                FROM points_transactions pt
                JOIN users u ON pt.user_id = u.user_id
                ORDER BY pt.created_at DESC
                LIMIT 20
            """
            transactions = pd.read_sql_query(transactions_query, conn)
            transactions.columns = ['Date', 'User', 'Type', 'Points', 'Balance', 'Description']
            st.dataframe(transactions, use_container_width=True, hide_index=True)
            
            # Points Balance Distribution
            st.markdown("---")
            st.subheader("📊 Points Balance Distribution")
            balances_query = "SELECT current_points_balance FROM user_points WHERE current_points_balance > 0"
            balances_df = pd.read_sql_query(balances_query, conn)
            
            if not balances_df.empty:
                fig = px.histogram(balances_df, x='current_points_balance', nbins=30, 
                                 title='User Points Balance Distribution',
                                 labels={'current_points_balance': 'Points Balance', 'count': 'Number of Users'})
                fig.update_layout(showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
        
        else:
            st.info("No loyalty data available yet.")
    
    except Exception as e:
        st.error(f"Error loading loyalty data: {str(e)}")

# TAB 5: SPAM DETECTION
with tab5:
    st.header("🔍 Spam Detection")
    
    st.markdown('<div class="spam-warning">⚠️ Surveys completed in <10 seconds are flagged as spam.</div>', unsafe_allow_html=True)
    
    try:
        stats = get_survey_stats()
        total_responses = sum(s['total'] for s in stats.values())
        total_spam = sum(s['spam'] for s in stats.values())
        spam_rate = (total_spam / total_responses * 100) if total_responses > 0 else 0
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Spam Detected", total_spam)
        with col2:
            st.metric("Spam Rate", f"{spam_rate:.1f}%")
        with col3:
            st.metric("Quality Score", f"{100-spam_rate:.1f}%")
        
        st.markdown("---")
        st.subheader("Time Distribution Analysis")
        
        overall_df = load_data('survey_overall_experience', include_spam=True)
        
        if not overall_df.empty:
            valid_avg = overall_df[overall_df['is_spam'] == 0]['time_spent_seconds'].mean()
            spam_avg = overall_df[overall_df['is_spam'] == 1]['time_spent_seconds'].mean() if len(overall_df[overall_df['is_spam'] == 1]) > 0 else 0
            
            valid_times = overall_df[overall_df['is_spam'] == 0]['time_spent_seconds']
            spam_times = overall_df[overall_df['is_spam'] == 1]['time_spent_seconds']
            
            fig = go.Figure()
            fig.add_trace(go.Histogram(x=valid_times, name='Valid Responses', opacity=0.7, marker_color='green', nbinsx=50))
            if len(spam_times) > 0:
                fig.add_trace(go.Histogram(x=spam_times, name='Spam', opacity=0.7, marker_color='red', nbinsx=50))
            
            fig.add_vline(x=valid_avg, line_color="green", line_width=3, line_dash="dash", annotation_text=f"Valid Avg: {valid_avg:.1f}s")
            if len(spam_times) > 0:
                fig.add_vline(x=spam_avg, line_color="red", line_width=3, line_dash="dash", annotation_text=f"Spam Avg: {spam_avg:.1f}s")
            
            fig.update_layout(title='Survey Completion Time Distribution', xaxis_title='Seconds', yaxis_title='Count', barmode='overlay')
            st.plotly_chart(fig, use_container_width=True)
        
    except Exception as e:
        st.error(f"Error: {str(e)}")

# TAB 6: MARKETING
with tab6:
    st.header("📈 Marketing Insights")
    
    try:
        marketing_df = load_data('survey_marketing_loyalty', include_spam)
        
        if not marketing_df.empty:
            col1, col2 = st.columns(2)
            
            with col1:
                heard_counts = marketing_df['heard_about_gem'].value_counts()
                fig = px.pie(values=heard_counts.values, names=heard_counts.index, hole=0.4)
                st.plotly_chart(fig, use_container_width=True)
                
                platform_counts = marketing_df['platform_influence'].value_counts()
                platform_colors = {'Instagram': '#E4405F', 'Facebook': '#1877F2', 'TikTok': '#000000', 'YouTube': '#FF0000', 'Google': '#4285F4', 'None': '#9E9E9E'}
                colors = [platform_colors.get(p, '#9E9E9E') for p in platform_counts.index]
                
                fig = go.Figure(data=[go.Bar(y=platform_counts.index, x=platform_counts.values, orientation='h', marker_color=colors)])
                fig.update_layout(title='Platform Influence')
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                first_visit_counts = marketing_df['first_visit'].value_counts()
                fig = px.pie(values=first_visit_counts.values, names=first_visit_counts.index, color_discrete_sequence=['#ff6b6b', '#4ecdc4'])
                st.plotly_chart(fig, use_container_width=True)
                
                return_counts = marketing_df['would_visit_again'].value_counts()
                fig = px.bar(x=return_counts.index, y=return_counts.values, color=return_counts.values, color_continuous_scale='Greens')
                st.plotly_chart(fig, use_container_width=True)
        
    except Exception as e:
        st.error(f"Error: {str(e)}")

# TAB 7: EXPORT
with tab7:
    st.header("💾 Data Export")
    
    export_options = st.multiselect("Select tables", ["Users", "Overall", "Service", "Tour", "Facilities", "Marketing", "Tut Immersive", "Children's"], default=["Users"])
    
    if st.button("📥 Export to Excel"):
        try:
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                if "Users" in export_options:
                    load_users().to_excel(writer, sheet_name='Users', index=False)
            
            output.seek(0)
            st.download_button("📥 Download", data=output, file_name=f"gem_export_{datetime.now().strftime('%Y%m%d')}.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            st.success("✅ Ready!")
        except Exception as e:
            st.error(f"Error: {str(e)}")

st.markdown("---")
st.markdown('<div style="text-align: center; color: #666;"><p>GEM Dashboard | {}</p></div>'.format(datetime.now().strftime("%Y-%m-%d %H:%M")), unsafe_allow_html=True)
