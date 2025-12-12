#!/usr/bin/env python3
"""
Migration: Add AssignmentTemplate table for shared teacher/homeschool templates
Creates assignment_templates table for reusable assignment templates
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

    print("\n🔍 Checking if assignment_templates table exists...")

    # Check if table already exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='assignment_templates'")
    table_exists = cursor.fetchone() is not None

    if table_exists:
        print("   ✅ assignment_templates table already exists")
        conn.close()
        return True

    print("   ➕ Creating assignment_templates table...")

    try:
        cursor.execute("""
            CREATE TABLE assignment_templates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                teacher_id INTEGER,
                parent_id INTEGER,
                title VARCHAR(200) NOT NULL,
                description TEXT,
                subject VARCHAR(50),
                grade_level VARCHAR(20),
                template_data TEXT NOT NULL,
                is_public BOOLEAN DEFAULT 0,
                use_count INTEGER DEFAULT 0,
                tags TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (teacher_id) REFERENCES teachers(id),
                FOREIGN KEY (parent_id) REFERENCES parents(id)
            )
        """)

        # Create indices for performance
        cursor.execute("CREATE INDEX idx_assignment_template_teacher_id ON assignment_templates(teacher_id)")
        cursor.execute("CREATE INDEX idx_assignment_template_parent_id ON assignment_templates(parent_id)")
        cursor.execute("CREATE INDEX idx_assignment_template_subject ON assignment_templates(subject)")
        cursor.execute("CREATE INDEX idx_assignment_template_is_public ON assignment_templates(is_public)")
        cursor.execute("CREATE INDEX idx_assignment_template_created_at ON assignment_templates(created_at)")

        conn.commit()
        print("   ✅ Table created successfully")
        print("   ✅ Indices created successfully")

    except Exception as e:
        print(f"   ❌ Error creating table: {e}")
        conn.rollback()
        conn.close()
        return False

    conn.close()
    print("\n✅ SQLite migration completed successfully!")
    return True


def run_migration_postgres():
    """Run migration for PostgreSQL database"""
    print("\n🐘 Running PostgreSQL migration...")

    try:
        # Check if table already exists
        result = db.session.execute(db.text("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables
                WHERE table_name = 'assignment_templates'
            )
        """))
        table_exists = result.scalar()

        if table_exists:
            print("   ✅ assignment_templates table already exists")
            return True

        print("   ➕ Creating assignment_templates table...")

        # Create table
        db.session.execute(db.text("""
            CREATE TABLE assignment_templates (
                id SERIAL PRIMARY KEY,
                teacher_id INTEGER REFERENCES teachers(id),
                parent_id INTEGER REFERENCES parents(id),
                title VARCHAR(200) NOT NULL,
                description TEXT,
                subject VARCHAR(50),
                grade_level VARCHAR(20),
                template_data TEXT NOT NULL,
                is_public BOOLEAN DEFAULT FALSE,
                use_count INTEGER DEFAULT 0,
                tags TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """))

        # Create indices
        db.session.execute(db.text("CREATE INDEX idx_assignment_template_teacher_id ON assignment_templates(teacher_id)"))
        db.session.execute(db.text("CREATE INDEX idx_assignment_template_parent_id ON assignment_templates(parent_id)"))
        db.session.execute(db.text("CREATE INDEX idx_assignment_template_subject ON assignment_templates(subject)"))
        db.session.execute(db.text("CREATE INDEX idx_assignment_template_is_public ON assignment_templates(is_public)"))
        db.session.execute(db.text("CREATE INDEX idx_assignment_template_created_at ON assignment_templates(created_at)"))

        db.session.commit()
        print("   ✅ Table created successfully")
        print("   ✅ Indices created successfully")

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
    print("🔧 Assignment Templates Migration")
    print("=" * 70)

    with app.app_context():
        success = run_migration()

    if success:
        print("\n✨ All done! The assignment_templates table is ready to use.")
        sys.exit(0)
    else:
        print("\n⚠️  Migration failed. Please check the errors above.")
        sys.exit(1)
