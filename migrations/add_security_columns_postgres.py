#!/usr/bin/env python3
"""
Database Migration: Add Security Columns (PostgreSQL)
Adds failed_login_attempts and account_locked_until to students table
"""

import sys
import os

# Add parent directory to path to import app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Bypass environment variable checks for migration
os.environ['SKIP_ENV_CHECK'] = 'true'
os.environ.setdefault('STRIPE_SECRET_KEY', 'sk_test_dummy')
os.environ.setdefault('STRIPE_PUBLISHABLE_KEY', 'pk_test_dummy')

from app import app, db
from sqlalchemy import text

def add_security_columns():
    """Add security-related columns to students table"""

    with app.app_context():
        try:
            # Check if columns already exist
            check_query = text("""
                SELECT column_name
                FROM information_schema.columns
                WHERE table_name = 'students'
                AND column_name IN ('failed_login_attempts', 'account_locked_until')
            """)

            existing_columns = db.session.execute(check_query).fetchall()
            existing_column_names = [row[0] for row in existing_columns]

            print(f"Existing security columns: {existing_column_names}")

            # Add failed_login_attempts if it doesn't exist
            if 'failed_login_attempts' not in existing_column_names:
                print("Adding failed_login_attempts column...")
                alter_query = text("""
                    ALTER TABLE students
                    ADD COLUMN failed_login_attempts INTEGER DEFAULT 0
                """)
                db.session.execute(alter_query)
                print("✅ Added failed_login_attempts column")
            else:
                print("⏭️  failed_login_attempts column already exists")

            # Add account_locked_until if it doesn't exist
            if 'account_locked_until' not in existing_column_names:
                print("Adding account_locked_until column...")
                alter_query = text("""
                    ALTER TABLE students
                    ADD COLUMN account_locked_until TIMESTAMP
                """)
                db.session.execute(alter_query)
                print("✅ Added account_locked_until column")
            else:
                print("⏭️  account_locked_until column already exists")

            db.session.commit()
            print("\n✅ Security columns migration completed successfully!")

        except Exception as e:
            db.session.rollback()
            print(f"\n❌ Migration failed: {e}")
            import traceback
            traceback.print_exc()
            raise

if __name__ == "__main__":
    print("=" * 60)
    print("DATABASE MIGRATION: Add Security Columns (PostgreSQL)")
    print("=" * 60)
    print()

    add_security_columns()

    print()
    print("=" * 60)
    print("Migration complete!")
    print("=" * 60)
