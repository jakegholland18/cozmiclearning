"""
Quick database migration - adds new columns to game_sessions table
Run this before starting your Flask app with the arcade enhancements
"""

import sqlite3
import os

# Path to your database
db_path = 'instance/cozmiclearning.db'

if not os.path.exists(db_path):
    print(f"❌ Database not found at {db_path}")
    print("Please update the db_path variable to point to your database file")
    exit(1)

print("🔧 Starting Quick Migration...")
print("=" * 50)

# Connect to database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    # Check current columns
    cursor.execute("PRAGMA table_info(game_sessions)")
    columns = [col[1] for col in cursor.fetchall()]
    print(f"Current columns in game_sessions: {', '.join(columns)}")

    # Add game_mode column if it doesn't exist
    if 'game_mode' not in columns:
        print("\n➕ Adding game_mode column...")
        cursor.execute("ALTER TABLE game_sessions ADD COLUMN game_mode VARCHAR(20) DEFAULT 'timed'")
        print("✅ Added game_mode column")
    else:
        print("\n⏭️  game_mode column already exists")

    # Add powerups_used column if it doesn't exist
    if 'powerups_used' not in columns:
        print("➕ Adding powerups_used column...")
        cursor.execute("ALTER TABLE game_sessions ADD COLUMN powerups_used TEXT")
        print("✅ Added powerups_used column")
    else:
        print("⏭️  powerups_used column already exists")

    conn.commit()

    # Verify changes
    cursor.execute("PRAGMA table_info(game_sessions)")
    new_columns = [col[1] for col in cursor.fetchall()]
    print(f"\nUpdated columns: {', '.join(new_columns)}")

    print("\n" + "=" * 50)
    print("✅ Migration Complete!")
    print("\nNext steps:")
    print("1. Run: python3 init_arcade_enhancements.py")
    print("2. Restart your Flask app")
    print("3. Visit /arcade to test!")
    print("=" * 50)

except Exception as e:
    print(f"\n❌ Error: {e}")
    conn.rollback()
    raise

finally:
    conn.close()
