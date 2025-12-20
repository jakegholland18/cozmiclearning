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
    """Add security-related columns to students table"""

    print(f"Connecting to database: {DB_PATH}")

    if not os.path.exists(DB_PATH):
        print(f"❌ Database not found at {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # Get existing columns
        cursor.execute("PRAGMA table_info(students)")
        columns = cursor.fetchall()
        column_names = [col[1] for col in columns]

        print(f"\nExisting columns in students table: {len(column_names)}")

        # Add failed_login_attempts if it doesn't exist
        if 'failed_login_attempts' not in column_names:
            print("Adding failed_login_attempts column...")
            cursor.execute("""
                ALTER TABLE students
                ADD COLUMN failed_login_attempts INTEGER DEFAULT 0
            """)
            print("✅ Added failed_login_attempts column")
        else:
            print("⏭️  failed_login_attempts column already exists")

        # Add account_locked_until if it doesn't exist
        if 'account_locked_until' not in column_names:
            print("Adding account_locked_until column...")
            cursor.execute("""
                ALTER TABLE students
                ADD COLUMN account_locked_until TIMESTAMP
            """)
            print("✅ Added account_locked_until column")
        else:
            print("⏭️  account_locked_until column already exists")

        conn.commit()
        print("\n✅ Security columns migration completed successfully!")

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
