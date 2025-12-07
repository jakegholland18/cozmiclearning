"""
Migration Script: Add Missing Arcade Columns
Adds difficulty and game_mode columns to arcade game tables
"""

import sqlite3
from pathlib import Path

def add_arcade_columns():
    """Add missing arcade columns to game tables"""

    # Try multiple possible database paths
    possible_paths = [
        Path("persist/cozmiclearning.db"),  # Render production path
        Path("instance/cozmic.db"),  # Local development path
        Path("/opt/render/project/src/persist/cozmiclearning.db"),  # Absolute Render path
        Path("persistent_db/cozmiclearning.db"),  # Alternative Render path
        Path("/opt/render/project/src/persistent_db/cozmiclearning.db"),  # Absolute alternative
    ]

    db_path = None
    for path in possible_paths:
        if path.exists():
            db_path = path
            print(f"✅ Found database at: {db_path}")
            break

    if not db_path:
        print(f"❌ Database not found at any of these locations:")
        for path in possible_paths:
            print(f"   - {path}")
        print("   Make sure you're running this from the project root directory")
        return False

    try:
        # Connect to database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        total_columns_added = 0

        # Add columns to game_sessions table
        print(f"\n📋 Checking game_sessions table...")
        cursor.execute("PRAGMA table_info(game_sessions)")
        columns = [column[1] for column in cursor.fetchall()]

        if 'difficulty' not in columns:
            print(f"   📝 Adding column: difficulty (TEXT)")
            cursor.execute("ALTER TABLE game_sessions ADD COLUMN difficulty TEXT")
            print(f"   ✅ Added difficulty")
            total_columns_added += 1
        else:
            print(f"   ✅ difficulty column already exists")

        if 'game_mode' not in columns:
            print(f"   📝 Adding column: game_mode (TEXT)")
            cursor.execute("ALTER TABLE game_sessions ADD COLUMN game_mode TEXT DEFAULT 'timed'")
            print(f"   ✅ Added game_mode")
            total_columns_added += 1
        else:
            print(f"   ✅ game_mode column already exists")

        # Add columns to game_leaderboards table
        print(f"\n📋 Checking game_leaderboards table...")
        cursor.execute("PRAGMA table_info(game_leaderboards)")
        columns = [column[1] for column in cursor.fetchall()]

        if 'difficulty' not in columns:
            print(f"   📝 Adding column: difficulty (TEXT)")
            cursor.execute("ALTER TABLE game_leaderboards ADD COLUMN difficulty TEXT")
            print(f"   ✅ Added difficulty")
            total_columns_added += 1
        else:
            print(f"   ✅ difficulty column already exists")

        # Commit changes
        conn.commit()
        conn.close()

        print("\n" + "="*60)
        print("✅ Migration completed successfully!")
        print("="*60)
        print(f"   Added {total_columns_added} total column(s)")
        print("   Tables updated: game_sessions, game_leaderboards")
        print("="*60)

        return True

    except Exception as e:
        print(f"\n❌ Error during migration: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("="*60)
    print("  Arcade Columns Migration")
    print("="*60)
    print()

    success = add_arcade_columns()

    if success:
        print("\n✅ Arcade tables updated successfully!")
    else:
        print("\n❌ Migration failed. Please check the error messages above.")
