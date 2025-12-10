"""
Quick verification that the dashboard file has correct structure
"""

print("🔍 Verifying Dashboard Structure...")

with open('dashboard/staff_dashboard.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Check for all 7 tabs
tabs = []
for i in range(1, 8):
    if f'with tab{i}:' in content:
        tabs.append(i)
        print(f"✅ Tab {i} found")
    else:
        print(f"❌ Tab {i} MISSING!")

# Check tab headers
expected_headers = [
    ("tab1", "Dashboard Overview"),
    ("tab2", "Visitor Demographics"),
    ("tab3", "Survey Analysis"),
    ("tab4", "🎮 Loyalty Points System"),
    ("tab5", "🔍 Spam Detection"),
    ("tab6", "📈 Marketing Insights"),
    ("tab7", "💾 Data Export")
]

print("\n📋 Checking Tab Headers:")
for tab_var, expected_header in expected_headers:
    # Find the tab section
    tab_start = content.find(f'with {tab_var}:')
    if tab_start != -1:
        # Look for st.header within next 200 chars
        section = content[tab_start:tab_start+200]
        if expected_header in section:
            print(f"✅ {tab_var}: {expected_header}")
        else:
            print(f"⚠️  {tab_var}: Header may be different")
    else:
        print(f"❌ {tab_var}: NOT FOUND")

print("\n✅ Dashboard structure verification complete!")
print("\n💡 Dashboard should now display:")
print("   1. Overview")
print("   2. Demographics")
print("   3. Survey Analysis")
print("   4. Loyalty Points (NEW!)")
print("   5. Spam Detection")
print("   6. Marketing")
print("   7. Export")
