"""
Quick Deployment Preparation Script
Run this before deploying to any platform
"""

import os
import subprocess

def check_files():
    """Check if all required files exist"""
    print("🔍 Checking required files...")
    
    required_files = [
        'requirements.txt',
        '.gitignore',
        '.streamlit/config.toml',
        'dashboard/staff_dashboard.py',
        'webapp/visitor_app.py',
        'visitor_feedback.db'
    ]
    
    missing = []
    for file in required_files:
        if os.path.exists(file):
            print(f"   ✅ {file}")
        else:
            print(f"   ❌ {file} - MISSING!")
            missing.append(file)
    
    if missing:
        print(f"\n⚠️  Missing {len(missing)} required files!")
        return False
    
    print("\n✅ All required files present!")
    return True

def test_imports():
    """Test if all required packages are installed"""
    print("\n📦 Testing package imports...")
    
    packages = [
        'streamlit',
        'pandas',
        'plotly',
        'openpyxl',
        'textblob'
    ]
    
    missing = []
    for package in packages:
        try:
            __import__(package)
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package} - NOT INSTALLED!")
            missing.append(package)
    
    if missing:
        print(f"\n⚠️  Install missing packages:")
        print(f"   pip install {' '.join(missing)}")
        return False
    
    print("\n✅ All packages installed!")
    return True

def check_dashboard():
    """Check if dashboard can load"""
    print("\n🖥️  Checking dashboard...")
    
    try:
        # Check if file exists and has no syntax errors
        with open('dashboard/staff_dashboard.py', 'r') as f:
            compile(f.read(), 'staff_dashboard.py', 'exec')
        print("   ✅ Dashboard file valid")
        return True
    except Exception as e:
        print(f"   ❌ Dashboard error: {e}")
        return False

def check_database():
    """Check database"""
    print("\n🗄️  Checking database...")
    
    if os.path.exists('visitor_feedback.db'):
        size = os.path.getsize('visitor_feedback.db') / 1024 / 1024  # MB
        print(f"   ✅ Database exists ({size:.2f} MB)")
        
        # Check if it has data
        import sqlite3
        conn = sqlite3.connect('visitor_feedback.db')
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT COUNT(*) FROM users")
            users = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM user_points")
            loyalty_users = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM redemption_history")
            redemptions = cursor.fetchone()[0]
            
            print(f"   📊 Data: {users} users, {loyalty_users} loyalty members, {redemptions} redemptions")
            conn.close()
            return True
        except Exception as e:
            print(f"   ⚠️  Database may need setup: {e}")
            conn.close()
            return False
    else:
        print("   ❌ Database not found!")
        return False

def git_status():
    """Check git status"""
    print("\n📝 Checking git status...")
    
    if not os.path.exists('.git'):
        print("   ❌ Not a git repository!")
        print("\n   Initialize with:")
        print("   git init")
        print("   git add .")
        print("   git commit -m 'Initial commit'")
        return False
    
    try:
        # Check if there are uncommitted changes
        result = subprocess.run(['git', 'status', '--short'], 
                              capture_output=True, text=True)
        
        if result.stdout.strip():
            print("   ⚠️  Uncommitted changes:")
            print(result.stdout)
            print("\n   Commit with:")
            print("   git add .")
            print("   git commit -m 'Ready for deployment'")
        else:
            print("   ✅ All changes committed")
        
        return True
    except Exception as e:
        print(f"   ❌ Git error: {e}")
        return False

def deployment_instructions():
    """Show deployment instructions"""
    print("\n" + "="*70)
    print("🚀 READY TO DEPLOY!")
    print("="*70)
    
    print("\n📌 OPTION 1: Streamlit Cloud (FREE)")
    print("   1. Push to GitHub:")
    print("      git remote add origin https://github.com/YOUR_USERNAME/gem-museum.git")
    print("      git push -u origin main")
    print("   2. Go to: https://share.streamlit.io/")
    print("   3. Deploy dashboard: dashboard/staff_dashboard.py")
    print("   4. Deploy visitor app: webapp/visitor_app.py")
    
    print("\n📌 OPTION 2: Railway.app (EASIEST with Database)")
    print("   1. Go to: https://railway.app/")
    print("   2. Sign in with GitHub")
    print("   3. Deploy from GitHub repo")
    print("   4. Add PostgreSQL database (one-click)")
    print("   Cost: $5/month")
    
    print("\n📌 OPTION 3: Local Network (FREE, Internal Only)")
    print("   1. Find your IP: ipconfig")
    print("   2. Run dashboard:")
    print("      streamlit run dashboard/staff_dashboard.py --server.address 0.0.0.0")
    print("   3. Access from any device on network:")
    print("      http://YOUR_IP:8501")
    
    print("\n📖 See DEPLOYMENT_GUIDE.md for detailed instructions!")
    print("="*70)

def main():
    """Run all checks"""
    print("="*70)
    print("🚀 GEM MUSEUM DASHBOARD - DEPLOYMENT PREPARATION")
    print("="*70)
    
    checks = [
        check_files(),
        test_imports(),
        check_dashboard(),
        check_database(),
        git_status()
    ]
    
    print("\n" + "="*70)
    print("📊 SUMMARY")
    print("="*70)
    
    passed = sum(checks)
    total = len(checks)
    
    print(f"\n   Checks passed: {passed}/{total}")
    
    if passed == total:
        print("   ✅ ALL CHECKS PASSED!")
        deployment_instructions()
    else:
        print("   ⚠️  Some checks failed. Fix issues above before deploying.")
        print("\n   Run this script again after fixing issues:")
        print("   python prepare_deployment.py")

if __name__ == "__main__":
    main()
