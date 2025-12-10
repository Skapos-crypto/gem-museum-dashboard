# 🎯 Visitor Feedback System

**A clean 3-part system for collecting and analyzing visitor feedback**

---

## ✅ Current Status

- ✅ **203 users** with **480+ survey responses** loaded
- ✅ Clean structure: Web App → Database → Dashboard
- ✅ Ready to launch immediately!

---

## 🚀 Quick Start (2 Commands)

### Launch Visitor Web App
```powershell
streamlit run webapp/visitor_app.py
```
→ Opens at **http://localhost:8501**

### Launch Staff Dashboard
```powershell
streamlit run dashboard/staff_dashboard.py --server.port=8502
```
→ Opens at **http://localhost:8502**

---

## 📂 Project Structure

```
gem_hackthon/
├── webapp/
│   └── visitor_app.py          # Visitor interface (surveys)
├── dashboard/
│   └── staff_dashboard.py      # Staff analytics
├── database/
│   ├── schema.sql              # Database structure
│   └── db_manager.py           # Database operations
├── visitor_feedback.db         # SQLite database (203 users!)
├── generate_dummy_data.py      # Generate test data
├── check_database.py           # View statistics
└── setup.py                    # Initialize database
```

---

## 🎨 Features

### Visitor Web App (Port 8501)
- Demographics collection
- 4 survey types:
  - ⭐ General Experience
  - 🎨 Exhibition Feedback
  - 🏢 Facilities & Amenities
  - 💻 Digital Experience
- Progress tracking
- Thank you confirmation

### Staff Dashboard (Port 8502)
- Real-time statistics
- Demographics breakdown
- Interactive charts (Plotly)
- Ratings analysis
- Text feedback viewer
- Export to Excel/CSV
- Consolidated data view

### Database
- **5 tables**: users + 4 survey types
- **1 view**: consolidated_feedback (all data merged)
- Foreign key relationships
- Data validation
- Indexed for performance

---

## 📊 Current Database Contents

- **203 users** from 40+ countries
- **117** General Experience surveys
- **136** Exhibition Feedback surveys
- **118** Facilities surveys
- **109** Digital Experience surveys
- **480+** total responses

---

## 🛠️ Useful Commands

### View Database Stats
```powershell
python check_database.py
```

### Generate More Data
```powershell
# Add 100 more users
python generate_dummy_data.py 100
```

### Reset Database
```powershell
Remove-Item visitor_feedback.db
python setup.py
```

### Install Dependencies
```powershell
pip install -r requirements.txt
```

---

## 📚 Database Schema

### Tables

**1. users** (Demographics - PRIMARY)
- user_id, email, name, nationality, age, language, gender

**2. survey_general_experience**
- overall_satisfaction, would_recommend, ease_of_navigation, staff_helpfulness, cleanliness_rating
- Links to user_id

**3. survey_exhibition_feedback**
- content_quality, educational_value, interactive_elements, favorite_exhibit
- Links to user_id

**4. survey_facilities**
- parking_rating, restroom_cleanliness, cafe_restaurant_quality, accessibility_rating, wifi_quality
- Links to user_id

**5. survey_digital_experience**
- mobile_app_rating, website_usability, online_booking_ease, digital_guides_usefulness
- Links to user_id

### View

**consolidated_feedback** - Merges all surveys with user demographics for easy reporting

---

## 🎯 What You Can Do

1. **Test the visitor flow**: Add your own feedback via the web app
2. **Analyze data**: View charts and statistics in the dashboard
3. **Export reports**: Download Excel/CSV from dashboard
4. **Generate more data**: Use `generate_dummy_data.py` to add test users
5. **Customize surveys**: Edit forms in `webapp/visitor_app.py`

---

## 💡 Tips

- Both apps can run simultaneously (different ports)
- Dashboard shows real-time data (refresh to update)
- Export to Excel creates multiple sheets (one per table)
- Database uses SQLite (single file, no server needed)
- Generate more data to test dashboard with large datasets

---

## 🔧 Troubleshooting

**Port already in use:**
```powershell
streamlit run webapp/visitor_app.py --server.port=8503
```

**Module not found:**
```powershell
pip install -r requirements.txt
```

**Database locked:**
Close all apps accessing the database, then restart

---

## 📈 Data Pipeline

```
Visitor → Web App → Database (with FK relationships) → Dashboard → Analytics
```

Each survey is in its own table, all linked to users via `user_id` foreign key. The consolidated view automatically merges everything!

---

## 🎉 You're Ready!

**Next step:** Run the commands above and open the dashboard to see your data visualized!

---

**Built with:** Python • Streamlit • SQLite • Pandas • Plotly  
**Created:** December 2025  
**Status:** ✅ Production Ready
