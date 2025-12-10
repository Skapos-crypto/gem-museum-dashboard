# 🚀 DEPLOYMENT GUIDE - GEM Museum Dashboard

## Option 1: Deploy to Streamlit Community Cloud (FREE) ⭐

### Step 1: Prepare Your Code

1. **Update requirements.txt** (add missing packages):
```bash
cd c:\Users\Void\gem_hackthon
```

Add to requirements.txt:
```
plotly==5.17.0
openpyxl==3.1.2
textblob==0.17.1
```

### Step 2: Initialize Git Repository

```bash
git init
git add .
git commit -m "Initial commit - GEM Museum Feedback System"
```

### Step 3: Create GitHub Repository

1. Go to https://github.com/new
2. Name: `gem-museum-feedback`
3. Keep it Public (required for free Streamlit Cloud)
4. Don't initialize with README (we already have one)
5. Click "Create repository"

### Step 4: Push to GitHub

```bash
git remote add origin https://github.com/YOUR_USERNAME/gem-museum-feedback.git
git branch -M main
git push -u origin main
```

### Step 5: Deploy on Streamlit Cloud

1. Go to https://share.streamlit.io/
2. Click "Sign in" (use GitHub)
3. Click "New app"
4. Select:
   - **Repository**: `YOUR_USERNAME/gem-museum-feedback`
   - **Branch**: `main`
   - **Main file path**: `dashboard/staff_dashboard.py`
5. Click "Deploy!"

### Step 6: Deploy Visitor App (Second App)

Repeat Step 5 but use:
- **Main file path**: `webapp/visitor_app.py`

---

## Your Live URLs Will Be:

✅ **Staff Dashboard**: `https://YOUR_USERNAME-gem-museum-feedback-dashboard-staff-dashboard-abc123.streamlit.app`

✅ **Visitor App**: `https://YOUR_USERNAME-gem-museum-feedback-webapp-visitor-app-abc123.streamlit.app`

---

## ⚠️ Important Notes for Streamlit Cloud:

### Issue: Database File Not Persistent

Streamlit Cloud's file system is temporary. Your SQLite database will reset when the app sleeps.

**Solutions:**

### A) Keep SQLite (Simple, Good for Demo)
- Accept that data resets
- Re-run population scripts after deploy
- Good for hackathon/demo purposes

### B) Upgrade to PostgreSQL (Recommended for Production)

1. **Get Free PostgreSQL Database:**
   - Sign up at https://www.elephantsql.com/ (FREE tier)
   - Or use https://supabase.com/ (FREE tier with more features)
   - Copy the connection URL

2. **Add Connection String to Streamlit Secrets:**
   - In Streamlit Cloud dashboard, go to your app
   - Click "⚙️ Settings" → "Secrets"
   - Add:
   ```toml
   [connections.postgresql]
   url = "postgresql://user:password@host:5432/database"
   ```

3. **Update Your Code** (I can help with this)

---

## Option 2: Deploy to Railway.app (EASIEST with Database) 🚂

### Step 1: Sign Up
1. Go to https://railway.app/
2. Sign in with GitHub

### Step 2: Create New Project
1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. Choose your repository

### Step 3: Add PostgreSQL Database
1. Click "New" → "Database" → "PostgreSQL"
2. Railway automatically creates and connects it

### Step 4: Configure Apps
1. Add two services:
   - Service 1: `streamlit run dashboard/staff_dashboard.py`
   - Service 2: `streamlit run webapp/visitor_app.py`

### Step 5: Set Environment Variables
Railway auto-configures DATABASE_URL for you!

**Cost**: $5/month (includes PostgreSQL)

---

## Option 3: Deploy to Render.com (Good Balance) 🎨

### Pros:
- Free tier available
- Free PostgreSQL database (90 days, then $7/month)
- Easy setup

### Steps:

1. Go to https://render.com/
2. Sign up with GitHub
3. Click "New +" → "Web Service"
4. Connect repository
5. Configure:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run dashboard/staff_dashboard.py --server.port $PORT --server.address 0.0.0.0`
6. Add PostgreSQL database from dashboard

---

## 🎯 MY RECOMMENDATION FOR YOU:

### For Quick Demo/Hackathon:
→ **Streamlit Cloud** with SQLite (accept data resets)

### For Real Production Use:
→ **Railway.app** (easiest with persistent database)

---

## 📋 PRE-DEPLOYMENT CHECKLIST

Run these commands before deploying:

```bash
# 1. Update requirements.txt
cd c:\Users\Void\gem_hackthon
echo "plotly==5.17.0" >> requirements.txt
echo "openpyxl==3.1.2" >> requirements.txt
echo "textblob==0.17.1" >> requirements.txt

# 2. Test locally one more time
streamlit run dashboard/staff_dashboard.py

# 3. Initialize git (if not done)
git init
git add .
git commit -m "Ready for deployment"

# 4. Push to GitHub
# (Follow steps above)
```

---

## 🆘 TROUBLESHOOTING

### Error: "ModuleNotFoundError"
→ Add missing package to requirements.txt

### Error: "Database is locked"
→ Use PostgreSQL instead of SQLite

### Error: "Port already in use"
→ Streamlit Cloud handles ports automatically

### Dashboard shows old data
→ Streamlit Cloud caches data. Click "⋮" → "Rerun"

---

## 🔄 AUTO-DEPLOY ON PUSH

Once connected to GitHub:
1. Make changes locally
2. Commit and push
3. Streamlit Cloud auto-deploys!

```bash
git add .
git commit -m "Update dashboard"
git push
# Wait 1-2 minutes, app auto-updates!
```

---

## 📞 NEED HELP?

Tell me which option you want to use:
1. **Streamlit Cloud** (free, easiest)
2. **Railway.app** (best overall)
3. **Render.com** (good middle ground)

I'll walk you through it step-by-step! 🚀
