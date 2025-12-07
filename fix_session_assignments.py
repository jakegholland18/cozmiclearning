#!/usr/bin/env python3
"""Fix session.get() assignments that cause syntax errors"""

import re

# Read the file
with open('app.py', 'r') as f:
    content = f.read()

# Pattern to find session.get(...) = value (invalid syntax)
# We need to convert these to session[key] = value

# Pattern: session.get("key", default) = value
# Replace with: session["key"] = value

replacements = [
    (r'session\.get\("practice_step", 0\) = (\d+)', r'session["practice_step"] = \1'),
    (r'session\.get\("practice_step", 0\) = ([\w_]+\s*\+\s*\d+)', r'session["practice_step"] = \1'),
    (r'session\.get\("practice_step", 0\) = ([\w_]+)', r'session["practice_step"] = \1'),
    (r'session\.get\("character", "everly"\) = (.+)', r'session["character"] = \1'),
    (r'session\.get\("grade", "8"\) = (.+)', r'session["grade"] = \1'),
]

for pattern, replacement in replacements:
    content = re.sub(pattern, replacement, content)

# Write back
with open('app.py', 'w') as f:
    f.write(content)

print("✅ Fixed all session.get() assignment syntax errors")
