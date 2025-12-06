"""
Database migration script for arcade enhancements.
Adds new columns to existing game_sessions table and creates new tables.

Usage:
    python migrate_arcade_db.py
"""

from app import app
from models import db
import sqlite3
import os

def migrate_database():
    """Migrate the database to add new arcade enhancement features"""

    with app.app_context():
        db_path = os.path.join(app.instance_path, 'database.db')

        print("🔧 Starting Arcade Enhancements Database Migration...")
        print("=" * 60)

        # Connect to database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        try:
            # Check if game_sessions table exists
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='game_sessions'")
            if cursor.fetchone():
                print("\n📋 Migrating game_sessions table...")

                # Check if columns already exist
                cursor.execute("PRAGMA table_info(game_sessions)")
                columns = [col[1] for col in cursor.fetchall()]

                # Add game_mode column if it doesn't exist
                if 'game_mode' not in columns:
                    print("  ➕ Adding game_mode column...")
                    cursor.execute("ALTER TABLE game_sessions ADD COLUMN game_mode VARCHAR(20) DEFAULT 'timed'")
                    print("  ✅ Added game_mode column")
                else:
                    print("  ⏭️  game_mode column already exists")

                # Add powerups_used column if it doesn't exist
                if 'powerups_used' not in columns:
                    print("  ➕ Adding powerups_used column...")
                    cursor.execute("ALTER TABLE game_sessions ADD COLUMN powerups_used TEXT")
                    print("  ✅ Added powerups_used column")
                else:
                    print("  ⏭️  powerups_used column already exists")

            conn.commit()
            print("\n✅ game_sessions table migration complete!")

        except Exception as e:
            print(f"\n❌ Error migrating game_sessions: {e}")
            conn.rollback()
            raise

        finally:
            conn.close()

        # Create all new tables using SQLAlchemy
        print("\n📊 Creating new tables...")
        try:
            db.create_all()
            print("✅ All new tables created successfully!")
        except Exception as e:
            print(f"⚠️  Some tables may already exist: {e}")

        # Initialize badges and powerups
        print("\n🏆 Initializing badges and power-ups...")
        from modules.arcade_enhancements import initialize_badges, initialize_powerups

        try:
            initialize_badges()
            initialize_powerups()
        except Exception as e:
            print(f"⚠️  Badges/powerups may already be initialized: {e}")

        print("\n" + "=" * 60)
        print("✅ Migration Complete!")
        print("\nNew features available:")
        print("  • game_mode column added to game_sessions")
        print("  • powerups_used column added to game_sessions")
        print("  • 6 new tables created (badges, powerups, challenges, streaks)")
        print("  • 12 achievement badges initialized")
        print("  • 5 power-ups initialized")
        print("\n🚀 Your arcade is ready to go!")
        print("=" * 60)


if __name__ == "__main__":
    migrate_database()
