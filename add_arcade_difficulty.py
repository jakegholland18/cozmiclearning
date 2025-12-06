"""
Add difficulty column to arcade tables
Run this migration to add difficulty levels to the arcade system
"""

import sqlite3
import os
import sys

def get_db_path():
    """Find the database file"""
    possible_paths = [
        # Check persistent DB first (production)
        '/opt/render/project/src/persistent_db/cozmiclearning.db',
        'persistent_db/cozmiclearning.db',
        # Then check instance DB (local/build)
        '/opt/render/project/src/instance/cozmiclearning.db',
        'instance/cozmiclearning.db',
    ]

    for path in possible_paths:
        if os.path.exists(path):
            return path

    if 'DB_PATH' in os.environ:
        return os.environ['DB_PATH']

    raise FileNotFoundError("Could not find database file. Tried: " + ", ".join(possible_paths))


def add_difficulty_columns():
    """Add difficulty column to arcade tables"""
    db_path = get_db_path()
    print(f"📂 Using database: {db_path}")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Check if game_sessions table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='game_sessions'")
        if not cursor.fetchone():
            print("⚠️  game_sessions table doesn't exist yet. Run setup_arcade_tables.py first.")
            return False

        # Add difficulty column to game_sessions
        print("\n1️⃣  Adding difficulty column to game_sessions...")
        try:
            cursor.execute("ALTER TABLE game_sessions ADD COLUMN difficulty VARCHAR(20) DEFAULT 'medium'")
            print("   ✅ Added difficulty column to game_sessions")
        except sqlite3.OperationalError as e:
            if "duplicate column" in str(e).lower():
                print("   ℹ️  difficulty column already exists in game_sessions")
            else:
                raise

        # Add difficulty column to game_leaderboards
        print("\n2️⃣  Adding difficulty column to game_leaderboards...")
        try:
            cursor.execute("ALTER TABLE game_leaderboards ADD COLUMN difficulty VARCHAR(20) DEFAULT 'medium'")
            print("   ✅ Added difficulty column to game_leaderboards")
        except sqlite3.OperationalError as e:
            if "duplicate column" in str(e).lower():
                print("   ℹ️  difficulty column already exists in game_leaderboards")
            else:
                raise

        # Add difficulty column to daily_challenges
        print("\n3️⃣  Adding difficulty column to daily_challenges...")
        try:
            cursor.execute("ALTER TABLE daily_challenges ADD COLUMN difficulty VARCHAR(20) DEFAULT 'medium'")
            print("   ✅ Added difficulty column to daily_challenges")
        except sqlite3.OperationalError as e:
            if "duplicate column" in str(e).lower():
                print("   ℹ️  difficulty column already exists in daily_challenges")
            else:
                raise

        # Create index for game_key + difficulty on leaderboards
        print("\n4️⃣  Creating index for game_key + difficulty...")
        try:
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_leaderboard_game_difficulty
                ON game_leaderboards(game_key, difficulty)
            """)
            print("   ✅ Created index idx_leaderboard_game_difficulty")
        except sqlite3.OperationalError as e:
            print(f"   ⚠️  Index creation warning: {e}")

        # Commit changes
        conn.commit()
        print("\n" + "="*60)
        print("✅ MIGRATION COMPLETE!")
        print("="*60)
        print("\nDifficulty columns added successfully:")
        print("  • game_sessions.difficulty (easy/medium/hard)")
        print("  • game_leaderboards.difficulty (easy/medium/hard)")
        print("  • daily_challenges.difficulty (easy/medium/hard)")
        print("  • Index created for faster leaderboard queries")
        print("\n" + "="*60)

        return True

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        conn.rollback()
        import traceback
        traceback.print_exc()
        return False

    finally:
        conn.close()


if __name__ == "__main__":
    print("🎮 Arcade Difficulty Migration")
    print("="*60)
    success = add_difficulty_columns()
    sys.exit(0 if success else 1)
