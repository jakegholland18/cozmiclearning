#!/usr/bin/env python3
"""
Script to fix session key access patterns in app.py
Replaces session["key"] with session.get("key", default)
"""

import re

# Read the file
with open('app.py', 'r') as f:
    content = f.read()

original_content = content

# Session key replacements with safe defaults
replacements = {
    'session["character"]': 'session.get("character", "everly")',
    'session["level"]': 'session.get("level", 1)',
    'session["xp"]': 'session.get("xp", 0)',
    'session["tokens"]': 'session.get("tokens", 100)',
    'session["grade"]': 'session.get("grade", "8")',
    'session["ability"]': 'session.get("ability", "on_level")',
    'session["practice_step"]': 'session.get("practice_step", 0)',
    'session["total_questions"]': 'session.get("total_questions", 0)',
    'session["correct_answers"]': 'session.get("correct_answers", 0)',
}

# Count replacements
total_replacements = 0

for old, new in replacements.items():
    count = content.count(old)
    if count > 0:
        print(f"Replacing {count} occurrences of {old}")
        content = content.replace(old, new)
        total_replacements += count

print(f"\nTotal replacements: {total_replacements}")

# Only write if changes were made
if content != original_content:
    # Backup original
    with open('app.py.backup_session_fix', 'w') as f:
        f.write(original_content)
    print("✅ Backup created: app.py.backup_session_fix")

    # Write fixed version
    with open('app.py', 'w') as f:
        f.write(content)
    print("✅ Fixed version written to app.py")
else:
    print("⚠️  No changes needed")
