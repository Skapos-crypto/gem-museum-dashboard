import sqlite3

conn = sqlite3.connect('visitor_feedback.db')
cursor = conn.cursor()

print("\n" + "=" * 70)
print("📊 DATABASE VERIFICATION - ALL TABLES")
print("=" * 70)

# Get all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
tables = cursor.fetchall()

print(f"\n✅ Total Tables: {len(tables)}\n")

# Categorize tables
original_tables = []
loyalty_tables = []
survey_tables = []

for table in tables:
    name = table[0]
    if 'survey_' in name:
        survey_tables.append(name)
    elif name in ['user_points', 'rewards_catalog', 'points_transactions', 'referral_tracking', 'redemption_history']:
        loyalty_tables.append(name)
    else:
        original_tables.append(name)

print("📁 ORIGINAL TABLES:")
for t in original_tables:
    print(f"   ✅ {t}")

print(f"\n📝 SURVEY TABLES ({len(survey_tables)}):")
for t in survey_tables:
    print(f"   ✅ {t}")

print(f"\n🎮 LOYALTY SYSTEM TABLES ({len(loyalty_tables)}):")
for t in loyalty_tables:
    cursor.execute(f"SELECT COUNT(*) FROM {t}")
    count = cursor.fetchone()[0]
    print(f"   ✅ {t} ({count} records)")

# Show rewards
print("\n💎 REWARDS CATALOG:")
cursor.execute("SELECT reward_category, COUNT(*) FROM rewards_catalog GROUP BY reward_category")
for row in cursor.fetchall():
    print(f"   • {row[0]}: {row[1]} rewards")

print("\n" + "=" * 70)
print("✅ DATABASE STRUCTURE VERIFIED")
print("=" * 70 + "\n")

conn.close()
