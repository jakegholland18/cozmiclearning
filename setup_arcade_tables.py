"""
Create all arcade-related database tables
This creates the tables directly in SQLite without requiring Flask app context
"""

import sqlite3
import os

db_path = 'instance/cozmiclearning.db'

if not os.path.exists(db_path):
    print(f"❌ Database not found at {db_path}")
    exit(1)

print("🎮 Setting up Arcade Tables...")
print("=" * 60)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    # Create arcade_games table
    print("\n📋 Creating arcade_games table...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS arcade_games (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            game_key VARCHAR(50) UNIQUE,
            name VARCHAR(100),
            description VARCHAR(255),
            subject VARCHAR(50),
            icon VARCHAR(50),
            difficulty_levels VARCHAR(100),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    print("✅ arcade_games table created")

    # Create game_sessions table
    print("📋 Creating game_sessions table...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS game_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            game_key VARCHAR(50),
            grade_level VARCHAR(10),
            difficulty VARCHAR(20),
            game_mode VARCHAR(20) DEFAULT 'timed',
            score INTEGER,
            time_seconds INTEGER,
            accuracy FLOAT,
            questions_answered INTEGER,
            questions_correct INTEGER,
            powerups_used TEXT,
            xp_earned INTEGER DEFAULT 0,
            tokens_earned INTEGER DEFAULT 0,
            started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES students(id)
        )
    """)
    print("✅ game_sessions table created")

    # Create game_leaderboards table
    print("📋 Creating game_leaderboards table...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS game_leaderboards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            game_key VARCHAR(50),
            grade_level VARCHAR(10),
            high_score INTEGER,
            best_time INTEGER,
            best_accuracy FLOAT,
            total_plays INTEGER DEFAULT 0,
            last_played TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES students(id)
        )
    """)
    print("✅ game_leaderboards table created")

    # Create arcade_badges table
    print("📋 Creating arcade_badges table...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS arcade_badges (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            badge_key VARCHAR(50) UNIQUE,
            name VARCHAR(100),
            description VARCHAR(255),
            icon VARCHAR(50),
            category VARCHAR(50),
            requirement_type VARCHAR(50),
            requirement_value INTEGER,
            game_key VARCHAR(50),
            tier VARCHAR(20),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    print("✅ arcade_badges table created")

    # Create student_badges table
    print("📋 Creating student_badges table...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS student_badges (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            badge_id INTEGER,
            game_key VARCHAR(50),
            earned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES students(id),
            FOREIGN KEY (badge_id) REFERENCES arcade_badges(id)
        )
    """)
    print("✅ student_badges table created")

    # Create powerups table
    print("📋 Creating powerups table...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS powerups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            powerup_key VARCHAR(50) UNIQUE,
            name VARCHAR(100),
            description VARCHAR(255),
            icon VARCHAR(50),
            token_cost INTEGER,
            effect_duration INTEGER,
            uses_per_game INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    print("✅ powerups table created")

    # Create student_powerups table
    print("📋 Creating student_powerups table...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS student_powerups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            powerup_id INTEGER,
            quantity INTEGER DEFAULT 1,
            FOREIGN KEY (student_id) REFERENCES students(id),
            FOREIGN KEY (powerup_id) REFERENCES powerups(id)
        )
    """)
    print("✅ student_powerups table created")

    # Create daily_challenges table
    print("📋 Creating daily_challenges table...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS daily_challenges (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            game_key VARCHAR(50),
            challenge_date DATE UNIQUE,
            target_score INTEGER,
            target_accuracy FLOAT,
            target_time INTEGER,
            grade_level VARCHAR(10),
            bonus_xp INTEGER DEFAULT 100,
            bonus_tokens INTEGER DEFAULT 50,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    print("✅ daily_challenges table created")

    # Create student_challenge_progress table
    print("📋 Creating student_challenge_progress table...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS student_challenge_progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            challenge_id INTEGER,
            completed BOOLEAN DEFAULT 0,
            completed_at TIMESTAMP,
            best_score INTEGER,
            best_accuracy FLOAT,
            best_time INTEGER,
            FOREIGN KEY (student_id) REFERENCES students(id),
            FOREIGN KEY (challenge_id) REFERENCES daily_challenges(id)
        )
    """)
    print("✅ student_challenge_progress table created")

    # Create game_streaks table
    print("📋 Creating game_streaks table...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS game_streaks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER UNIQUE,
            current_streak INTEGER DEFAULT 0,
            longest_streak INTEGER DEFAULT 0,
            last_played_date DATE,
            FOREIGN KEY (student_id) REFERENCES students(id)
        )
    """)
    print("✅ game_streaks table created")

    # Create indices
    print("\n📊 Creating database indices...")
    indices = [
        "CREATE INDEX IF NOT EXISTS idx_game_session_student_id ON game_sessions(student_id)",
        "CREATE INDEX IF NOT EXISTS idx_game_session_game_key ON game_sessions(game_key)",
        "CREATE INDEX IF NOT EXISTS idx_game_leaderboard_student_id ON game_leaderboards(student_id)",
        "CREATE INDEX IF NOT EXISTS idx_student_badge_student_id ON student_badges(student_id)",
        "CREATE INDEX IF NOT EXISTS idx_student_powerup_student_id ON student_powerups(student_id)",
        "CREATE INDEX IF NOT EXISTS idx_game_streak_student_id ON game_streaks(student_id)",
    ]

    for index_sql in indices:
        cursor.execute(index_sql)

    print("✅ Indices created")

    conn.commit()

    # Verify tables
    print("\n🔍 Verifying tables...")
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tables = [row[0] for row in cursor.fetchall()]
    print(f"Total tables in database: {len(tables)}")

    arcade_tables = [t for t in tables if 'game' in t or 'arcade' in t or 'powerup' in t or 'challenge' in t or 'streak' in t or 'badge' in t]
    print(f"Arcade-related tables: {', '.join(arcade_tables)}")

    print("\n" + "=" * 60)
    print("✅ All Arcade Tables Created Successfully!")
    print("\nNext steps:")
    print("1. Run: python3 init_arcade_enhancements.py")
    print("   (This will populate badges and powerups)")
    print("2. Restart your Flask app")
    print("3. Visit /arcade to test!")
    print("=" * 60)

except Exception as e:
    print(f"\n❌ Error: {e}")
    conn.rollback()
    raise

finally:
    conn.close()
