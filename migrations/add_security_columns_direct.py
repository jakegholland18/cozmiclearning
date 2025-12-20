#!/usr/bin/env python3
"""
Database Migration: Add Security Columns (Direct SQLite)
Adds failed_login_attempts and account_locked_until to students table
"""

import sqlite3
import os

# Database path
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'persistent_db', 'cozmiclearning.db')

def add_security_columns():
    """Add security-related columns to students and teachers tables"""

    print(f"Connecting to database: {DB_PATH}")

    if not os.path.exists(DB_PATH):
        print(f"❌ Database not found at {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # Migrate STUDENTS table
        print("\n" + "="*60)
        print("Migrating STUDENTS table")
        print("="*60)

        cursor.execute("PRAGMA table_info(students)")
        columns = cursor.fetchall()
        column_names = [col[1] for col in columns]

        print(f"Existing columns in students table: {len(column_names)}")

        if 'failed_login_attempts' not in column_names:
            print("Adding failed_login_attempts column to students...")
            cursor.execute("""
                ALTER TABLE students
                ADD COLUMN failed_login_attempts INTEGER DEFAULT 0
            """)
            print("✅ Added failed_login_attempts to students")
        else:
            print("⏭️  students.failed_login_attempts already exists")

        if 'account_locked_until' not in column_names:
            print("Adding account_locked_until column to students...")
            cursor.execute("""
                ALTER TABLE students
                ADD COLUMN account_locked_until TIMESTAMP
            """)
            print("✅ Added account_locked_until to students")
        else:
            print("⏭️  students.account_locked_until already exists")

        # Migrate TEACHERS table
        print("\n" + "="*60)
        print("Migrating TEACHERS table")
        print("="*60)

        cursor.execute("PRAGMA table_info(teachers)")
        columns = cursor.fetchall()
        column_names = [col[1] for col in columns]

        print(f"Existing columns in teachers table: {len(column_names)}")

        if 'failed_login_attempts' not in column_names:
            print("Adding failed_login_attempts column to teachers...")
            cursor.execute("""
                ALTER TABLE teachers
                ADD COLUMN failed_login_attempts INTEGER DEFAULT 0
            """)
            print("✅ Added failed_login_attempts to teachers")
        else:
            print("⏭️  teachers.failed_login_attempts already exists")

        if 'account_locked_until' not in column_names:
            print("Adding account_locked_until column to teachers...")
            cursor.execute("""
                ALTER TABLE teachers
                ADD COLUMN account_locked_until TIMESTAMP
            """)
            print("✅ Added account_locked_until to teachers")
        else:
            print("⏭️  teachers.account_locked_until already exists")

        conn.commit()
        print("\n" + "="*60)
        print("✅ Security columns migration completed successfully!")
        print("="*60)

    except Exception as e:
        conn.rollback()
        print(f"\n❌ Migration failed: {e}")
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    print("=" * 60)
    print("DATABASE MIGRATION: Add Security Columns")
    print("=" * 60)
    print()

    add_security_columns()

    print()
    print("=" * 60)
    print("Migration complete!")
    print("=" * 60)
