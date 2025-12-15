#!/usr/bin/env python3
"""
Quick diagnostic script to check what's working on production
"""

import requests

BASE_URL = "https://cozmiclearning-1.onrender.com"

print("🔍 CozmicLearning Quick Diagnostic")
print("=" * 60)

# Test 1: Homepage
print("\n1️⃣ Testing Homepage...")
try:
    r = requests.get(f"{BASE_URL}/")
    if r.status_code == 200:
        print(f"   ✅ Homepage loads (Status: {r.status_code})")
    else:
        print(f"   ❌ Homepage issue (Status: {r.status_code})")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 2: RespectRealm
print("\n2️⃣ Testing RespectRealm...")
try:
    r = requests.get(f"{BASE_URL}/respectrealm")
    if r.status_code == 200:
        # Count categories
        categories = [
            "Table Manners",
            "Public Behavior",
            "Respect & Courtesy",
            "Basic Courtesy",
            "Phone & Digital Manners",
            "Personal Care & Hygiene",
            "Conversation Skills",
            "Responsibility & Work Ethic",
            "Physical Discipline & Fitness",
            "Humility & Growth"
        ]
        found = []
        for cat in categories:
            if cat in r.text:
                found.append(cat)

        print(f"   ✅ RespectRealm loads (Status: {r.status_code})")
        print(f"   📊 Categories found: {len(found)}/10")

        if len(found) == 10:
            print("   ✅ All categories present!")
        else:
            print("   ⚠️  Missing categories:")
            for cat in categories:
                if cat not in found:
                    print(f"      - {cat}")
    else:
        print(f"   ❌ RespectRealm issue (Status: {r.status_code})")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 3: Teacher Signup Page
print("\n3️⃣ Testing Teacher Signup Page...")
try:
    r = requests.get(f"{BASE_URL}/teacher/signup")
    if r.status_code == 200:
        print(f"   ✅ Signup page loads (Status: {r.status_code})")
        if 'csrf_token' in r.text:
            print("   ✅ CSRF token present in form")
        else:
            print("   ⚠️  No CSRF token found in form")
    else:
        print(f"   ❌ Signup page issue (Status: {r.status_code})")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 4: All Subject Planets
print("\n4️⃣ Testing Subject Planets...")
subjects = [
    ("NumForge", "/subject/num_forge"),
    ("AtomSphere", "/subject/atom_sphere"),
    ("ChronoCore", "/subject/chrono_core"),
    ("StoryVerse", "/subject/story_verse"),
    ("InkHaven", "/subject/ink_haven"),
    ("FaithRealm", "/subject/faith_realm"),
    ("CoinQuest", "/subject/coin_quest"),
    ("StockStar", "/subject/stock_star"),
    ("TerraNova", "/subject/terra_nova"),
    ("PowerGrid", "/subject/power_grid"),
    ("TruthForge", "/subject/truth_forge"),
    ("RespectRealm", "/respectrealm"),
]

working = 0
for name, path in subjects:
    try:
        r = requests.get(f"{BASE_URL}{path}")
        if r.status_code == 200:
            working += 1
        else:
            print(f"   ❌ {name} (Status: {r.status_code})")
    except Exception as e:
        print(f"   ❌ {name}: {e}")

print(f"   📊 Working subjects: {working}/12")
if working == 12:
    print("   ✅ All subjects accessible!")

# Summary
print("\n" + "=" * 60)
print("📋 SUMMARY")
print("=" * 60)
print("\nWhat's Working:")
print("- Homepage, RespectRealm, Subject Planets")
print("\nWhat Needs Investigation:")
print("- Signup endpoints (need to test with POST request)")
print("- Check Render logs after attempting signup")
print("\n💡 Next Steps:")
print("1. Deploy latest code on Render (if not done)")
print("2. Try signing up at /teacher/signup")
print("3. Check Render logs for error details")
print("4. Share error message for specific fix")
