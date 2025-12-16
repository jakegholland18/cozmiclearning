#!/usr/bin/env python3
"""
Migration: Add Chapter & Lesson Progress Tracking Tables
Creates tables for hierarchical chapter/lesson progress, quizzes, and badges
"""

import sys
import os

# Add parent directory to path so we can import app modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db
import sqlite3


def run_migration_sqlite(db_path):
    """Run migration for SQLite database"""
    print(f"📁 Database path: {db_path}")

    if not os.path.exists(db_path):
        print(f"❌ Database file not found at {db_path}")
        return False

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # List of tables to create
    tables = ['chapter_progress', 'lesson_progress', 'chapter_quizzes', 'chapter_badges', 'student_chapter_badges']

    print("\n🔍 Checking existing tables...")

    # Track which tables need to be created
    tables_to_create = []
    for table in tables:
        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'")
        table_exists = cursor.fetchone() is not None
        if table_exists:
            print(f"   ✅ {table} already exists")
        else:
            print(f"   ➕ {table} needs to be created")
            tables_to_create.append(table)

    if not tables_to_create:
        print("\n✅ All tables already exist, nothing to migrate")
        conn.close()
        return True

    try:
        # Create chapter_progress table
        if 'chapter_progress' in tables_to_create:
            print("\n   Creating chapter_progress table...")
            cursor.execute("""
                CREATE TABLE chapter_progress (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id INTEGER NOT NULL,
                    subject VARCHAR(50) NOT NULL,
                    grade VARCHAR(10) NOT NULL,
                    chapter_id VARCHAR(100) NOT NULL,
                    lessons_completed INTEGER DEFAULT 0,
                    total_lessons INTEGER NOT NULL,
                    is_complete BOOLEAN DEFAULT 0,
                    quiz_score REAL,
                    quiz_attempts INTEGER DEFAULT 0,
                    quiz_passed BOOLEAN DEFAULT 0,
                    started_at TIMESTAMP,
                    completed_at TIMESTAMP,
                    last_accessed TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (student_id) REFERENCES students(id),
                    UNIQUE (student_id, subject, grade, chapter_id)
                )
            """)

            # Create indices for chapter_progress
            cursor.execute("CREATE INDEX idx_chapter_progress_student_id ON chapter_progress(student_id)")
            cursor.execute("CREATE INDEX idx_chapter_progress_subject_grade ON chapter_progress(subject, grade)")
            cursor.execute("CREATE INDEX idx_chapter_progress_chapter_id ON chapter_progress(chapter_id)")
            cursor.execute("CREATE INDEX idx_chapter_progress_student_chapter ON chapter_progress(student_id, subject, grade, chapter_id)")
            print("   ✅ chapter_progress table created")

        # Create lesson_progress table
        if 'lesson_progress' in tables_to_create:
            print("\n   Creating lesson_progress table...")
            cursor.execute("""
                CREATE TABLE lesson_progress (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id INTEGER NOT NULL,
                    subject VARCHAR(50) NOT NULL,
                    grade VARCHAR(10) NOT NULL,
                    chapter_id VARCHAR(100) NOT NULL,
                    lesson_title VARCHAR(200) NOT NULL,
                    is_complete BOOLEAN DEFAULT 0,
                    time_spent_minutes INTEGER DEFAULT 0,
                    practice_score REAL,
                    practice_attempts INTEGER DEFAULT 0,
                    first_viewed TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    completed_at TIMESTAMP,
                    last_accessed TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (student_id) REFERENCES students(id),
                    UNIQUE (student_id, subject, grade, chapter_id, lesson_title)
                )
            """)

            # Create indices for lesson_progress
            cursor.execute("CREATE INDEX idx_lesson_progress_student_id ON lesson_progress(student_id)")
            cursor.execute("CREATE INDEX idx_lesson_progress_chapter_id ON lesson_progress(chapter_id)")
            cursor.execute("CREATE INDEX idx_lesson_progress_student_lesson ON lesson_progress(student_id, subject, grade, chapter_id)")
            print("   ✅ lesson_progress table created")

        # Create chapter_quizzes table
        if 'chapter_quizzes' in tables_to_create:
            print("\n   Creating chapter_quizzes table...")
            cursor.execute("""
                CREATE TABLE chapter_quizzes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    subject VARCHAR(50) NOT NULL,
                    grade VARCHAR(10) NOT NULL,
                    chapter_id VARCHAR(100) NOT NULL,
                    question_text TEXT NOT NULL,
                    question_type VARCHAR(20) DEFAULT 'multiple_choice',
                    choice_a VARCHAR(255),
                    choice_b VARCHAR(255),
                    choice_c VARCHAR(255),
                    choice_d VARCHAR(255),
                    correct_answer VARCHAR(255) NOT NULL,
                    explanation TEXT,
                    difficulty VARCHAR(20) DEFAULT 'medium',
                    question_order INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Create indices for chapter_quizzes
            cursor.execute("CREATE INDEX idx_chapter_quiz_subject_grade_chapter ON chapter_quizzes(subject, grade, chapter_id)")
            cursor.execute("CREATE INDEX idx_chapter_quiz_question_order ON chapter_quizzes(question_order)")
            print("   ✅ chapter_quizzes table created")

        # Create chapter_badges table
        if 'chapter_badges' in tables_to_create:
            print("\n   Creating chapter_badges table...")
            cursor.execute("""
                CREATE TABLE chapter_badges (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    badge_key VARCHAR(100) UNIQUE NOT NULL,
                    name VARCHAR(100) NOT NULL,
                    description VARCHAR(255),
                    icon VARCHAR(50),
                    subject VARCHAR(50) NOT NULL,
                    grade VARCHAR(10) NOT NULL,
                    chapter_id VARCHAR(100) NOT NULL,
                    tier VARCHAR(20) DEFAULT 'bronze',
                    badge_type VARCHAR(50) DEFAULT 'chapter_complete',
                    requirement_type VARCHAR(50) DEFAULT 'completion',
                    requirement_value INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Create indices for chapter_badges
            cursor.execute("CREATE INDEX idx_chapter_badge_badge_key ON chapter_badges(badge_key)")
            cursor.execute("CREATE INDEX idx_chapter_badge_subject_grade_chapter ON chapter_badges(subject, grade, chapter_id)")
            print("   ✅ chapter_badges table created")

        # Create student_chapter_badges table
        if 'student_chapter_badges' in tables_to_create:
            print("\n   Creating student_chapter_badges table...")
            cursor.execute("""
                CREATE TABLE student_chapter_badges (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id INTEGER NOT NULL,
                    badge_id INTEGER NOT NULL,
                    quiz_score REAL,
                    completion_time_minutes INTEGER,
                    earned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (student_id) REFERENCES students(id),
                    FOREIGN KEY (badge_id) REFERENCES chapter_badges(id)
                )
            """)

            # Create indices for student_chapter_badges
            cursor.execute("CREATE INDEX idx_student_chapter_badge_student_id ON student_chapter_badges(student_id)")
            cursor.execute("CREATE INDEX idx_student_chapter_badge_badge_id ON student_chapter_badges(badge_id)")
            print("   ✅ student_chapter_badges table created")

        conn.commit()
        print("\n✅ All tables and indices created successfully")

    except Exception as e:
        print(f"   ❌ Error creating tables: {e}")
        conn.rollback()
        conn.close()
        return False

    conn.close()
    print("\n✅ SQLite migration completed successfully!")
    return True


def run_migration_postgres():
    """Run migration for PostgreSQL database"""
    print("\n🐘 Running PostgreSQL migration...")

    # List of tables to create
    tables = ['chapter_progress', 'lesson_progress', 'chapter_quizzes', 'chapter_badges', 'student_chapter_badges']

    print("\n🔍 Checking existing tables...")

    # Track which tables need to be created
    tables_to_create = []

    try:
        for table in tables:
            result = db.session.execute(db.text(f"""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables
                    WHERE table_name = '{table}'
                )
            """))
            table_exists = result.scalar()
            if table_exists:
                print(f"   ✅ {table} already exists")
            else:
                print(f"   ➕ {table} needs to be created")
                tables_to_create.append(table)

        if not tables_to_create:
            print("\n✅ All tables already exist, nothing to migrate")
            return True

        # Create chapter_progress table
        if 'chapter_progress' in tables_to_create:
            print("\n   Creating chapter_progress table...")
            db.session.execute(db.text("""
                CREATE TABLE chapter_progress (
                    id SERIAL PRIMARY KEY,
                    student_id INTEGER NOT NULL REFERENCES students(id),
                    subject VARCHAR(50) NOT NULL,
                    grade VARCHAR(10) NOT NULL,
                    chapter_id VARCHAR(100) NOT NULL,
                    lessons_completed INTEGER DEFAULT 0,
                    total_lessons INTEGER NOT NULL,
                    is_complete BOOLEAN DEFAULT FALSE,
                    quiz_score REAL,
                    quiz_attempts INTEGER DEFAULT 0,
                    quiz_passed BOOLEAN DEFAULT FALSE,
                    started_at TIMESTAMP,
                    completed_at TIMESTAMP,
                    last_accessed TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE (student_id, subject, grade, chapter_id)
                )
            """))

            # Create indices for chapter_progress
            db.session.execute(db.text("CREATE INDEX idx_chapter_progress_student_id ON chapter_progress(student_id)"))
            db.session.execute(db.text("CREATE INDEX idx_chapter_progress_subject_grade ON chapter_progress(subject, grade)"))
            db.session.execute(db.text("CREATE INDEX idx_chapter_progress_chapter_id ON chapter_progress(chapter_id)"))
            db.session.execute(db.text("CREATE INDEX idx_chapter_progress_student_chapter ON chapter_progress(student_id, subject, grade, chapter_id)"))
            print("   ✅ chapter_progress table created")

        # Create lesson_progress table
        if 'lesson_progress' in tables_to_create:
            print("\n   Creating lesson_progress table...")
            db.session.execute(db.text("""
                CREATE TABLE lesson_progress (
                    id SERIAL PRIMARY KEY,
                    student_id INTEGER NOT NULL REFERENCES students(id),
                    subject VARCHAR(50) NOT NULL,
                    grade VARCHAR(10) NOT NULL,
                    chapter_id VARCHAR(100) NOT NULL,
                    lesson_title VARCHAR(200) NOT NULL,
                    is_complete BOOLEAN DEFAULT FALSE,
                    time_spent_minutes INTEGER DEFAULT 0,
                    practice_score REAL,
                    practice_attempts INTEGER DEFAULT 0,
                    first_viewed TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    completed_at TIMESTAMP,
                    last_accessed TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE (student_id, subject, grade, chapter_id, lesson_title)
                )
            """))

            # Create indices for lesson_progress
            db.session.execute(db.text("CREATE INDEX idx_lesson_progress_student_id ON lesson_progress(student_id)"))
            db.session.execute(db.text("CREATE INDEX idx_lesson_progress_chapter_id ON lesson_progress(chapter_id)"))
            db.session.execute(db.text("CREATE INDEX idx_lesson_progress_student_lesson ON lesson_progress(student_id, subject, grade, chapter_id)"))
            print("   ✅ lesson_progress table created")

        # Create chapter_quizzes table
        if 'chapter_quizzes' in tables_to_create:
            print("\n   Creating chapter_quizzes table...")
            db.session.execute(db.text("""
                CREATE TABLE chapter_quizzes (
                    id SERIAL PRIMARY KEY,
                    subject VARCHAR(50) NOT NULL,
                    grade VARCHAR(10) NOT NULL,
                    chapter_id VARCHAR(100) NOT NULL,
                    question_text TEXT NOT NULL,
                    question_type VARCHAR(20) DEFAULT 'multiple_choice',
                    choice_a VARCHAR(255),
                    choice_b VARCHAR(255),
                    choice_c VARCHAR(255),
                    choice_d VARCHAR(255),
                    correct_answer VARCHAR(255) NOT NULL,
                    explanation TEXT,
                    difficulty VARCHAR(20) DEFAULT 'medium',
                    question_order INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """))

            # Create indices for chapter_quizzes
            db.session.execute(db.text("CREATE INDEX idx_chapter_quiz_subject_grade_chapter ON chapter_quizzes(subject, grade, chapter_id)"))
            db.session.execute(db.text("CREATE INDEX idx_chapter_quiz_question_order ON chapter_quizzes(question_order)"))
            print("   ✅ chapter_quizzes table created")

        # Create chapter_badges table
        if 'chapter_badges' in tables_to_create:
            print("\n   Creating chapter_badges table...")
            db.session.execute(db.text("""
                CREATE TABLE chapter_badges (
                    id SERIAL PRIMARY KEY,
                    badge_key VARCHAR(100) UNIQUE NOT NULL,
                    name VARCHAR(100) NOT NULL,
                    description VARCHAR(255),
                    icon VARCHAR(50),
                    subject VARCHAR(50) NOT NULL,
                    grade VARCHAR(10) NOT NULL,
                    chapter_id VARCHAR(100) NOT NULL,
                    tier VARCHAR(20) DEFAULT 'bronze',
                    badge_type VARCHAR(50) DEFAULT 'chapter_complete',
                    requirement_type VARCHAR(50) DEFAULT 'completion',
                    requirement_value INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """))

            # Create indices for chapter_badges
            db.session.execute(db.text("CREATE INDEX idx_chapter_badge_badge_key ON chapter_badges(badge_key)"))
            db.session.execute(db.text("CREATE INDEX idx_chapter_badge_subject_grade_chapter ON chapter_badges(subject, grade, chapter_id)"))
            print("   ✅ chapter_badges table created")

        # Create student_chapter_badges table
        if 'student_chapter_badges' in tables_to_create:
            print("\n   Creating student_chapter_badges table...")
            db.session.execute(db.text("""
                CREATE TABLE student_chapter_badges (
                    id SERIAL PRIMARY KEY,
                    student_id INTEGER NOT NULL REFERENCES students(id),
                    badge_id INTEGER NOT NULL REFERENCES chapter_badges(id),
                    quiz_score REAL,
                    completion_time_minutes INTEGER,
                    earned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """))

            # Create indices for student_chapter_badges
            db.session.execute(db.text("CREATE INDEX idx_student_chapter_badge_student_id ON student_chapter_badges(student_id)"))
            db.session.execute(db.text("CREATE INDEX idx_student_chapter_badge_badge_id ON student_chapter_badges(badge_id)"))
            print("   ✅ student_chapter_badges table created")

        db.session.commit()
        print("\n✅ All tables and indices created successfully")

    except Exception as e:
        print(f"   ❌ Error: {e}")
        db.session.rollback()
        return False

    print("\n✅ PostgreSQL migration completed successfully!")
    return True


def run_migration():
    """Detect database type and run appropriate migration"""
    db_uri = app.config.get('SQLALCHEMY_DATABASE_URI', '')

    if 'postgresql' in db_uri:
        # PostgreSQL database
        return run_migration_postgres()
    elif 'sqlite' in db_uri:
        # SQLite database
        db_path = db_uri.replace('sqlite:///', '')
        return run_migration_sqlite(db_path)
    else:
        print(f"❌ Unsupported database type: {db_uri}")
        return False


if __name__ == "__main__":
    print("=" * 70)
    print("🔧 Chapter & Lesson Progress Migration")
    print("=" * 70)

    with app.app_context():
        success = run_migration()

    if success:
        print("\n✨ All done! Chapter and lesson progress tables are ready to use.")
        sys.exit(0)
    else:
        print("\n⚠️  Migration failed. Please check the errors above.")
        sys.exit(1)
