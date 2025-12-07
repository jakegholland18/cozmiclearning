#!/usr/bin/env python3
"""
Migration: Add Stripe customer and subscription ID columns
Adds stripe_customer_id and stripe_subscription_id to teachers, students, and parents tables
"""

import sys
import os

# Add parent directory to path so we can import app modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db
import sqlite3

def run_migration():
    """Add Stripe columns to all user tables"""

    db_path = app.config.get('SQLALCHEMY_DATABASE_URI', '').replace('sqlite:///', '')
    if not db_path:
        print("❌ Could not find database path")
        return False

    print(f"📁 Database path: {db_path}")

    if not os.path.exists(db_path):
        print(f"❌ Database file not found at {db_path}")
        return False

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    tables_to_update = ['teachers', 'students', 'parents']

    for table in tables_to_update:
        print(f"\n🔍 Checking {table} table...")

        # Check if columns already exist
        cursor.execute(f"PRAGMA table_info({table})")
        columns = [row[1] for row in cursor.fetchall()]

        has_customer_id = 'stripe_customer_id' in columns
        has_subscription_id = 'stripe_subscription_id' in columns

        if has_customer_id and has_subscription_id:
            print(f"   ✅ {table} already has Stripe columns")
            continue

        # Add missing columns
        try:
            if not has_customer_id:
                print(f"   ➕ Adding stripe_customer_id to {table}...")
                cursor.execute(f"ALTER TABLE {table} ADD COLUMN stripe_customer_id VARCHAR(255)")
                print(f"   ✅ Added stripe_customer_id")

            if not has_subscription_id:
                print(f"   ➕ Adding stripe_subscription_id to {table}...")
                cursor.execute(f"ALTER TABLE {table} ADD COLUMN stripe_subscription_id VARCHAR(255)")
                print(f"   ✅ Added stripe_subscription_id")

            conn.commit()
            print(f"   💾 Changes committed for {table}")

        except Exception as e:
            print(f"   ❌ Error updating {table}: {e}")
            conn.rollback()
            return False

    # Verify the changes
    print("\n🔍 Verifying migration...")
    for table in tables_to_update:
        cursor.execute(f"PRAGMA table_info({table})")
        columns = [row[1] for row in cursor.fetchall()]

        if 'stripe_customer_id' in columns and 'stripe_subscription_id' in columns:
            print(f"   ✅ {table} - Both columns present")
        else:
            print(f"   ❌ {table} - Missing columns!")
            conn.close()
            return False

    conn.close()
    print("\n✅ Migration completed successfully!")
    return True

if __name__ == "__main__":
    print("=" * 60)
    print("🔧 Stripe Columns Migration")
    print("=" * 60)

    with app.app_context():
        success = run_migration()

    if success:
        print("\n✨ All done! The database schema is now up to date.")
        sys.exit(0)
    else:
        print("\n⚠️  Migration failed. Please check the errors above.")
        sys.exit(1)
