"""
Migration Script: Add Stripe Columns to All User Tables
Adds stripe_customer_id and stripe_subscription_id columns to:
- students table
- teachers table
- parents table
"""

import sqlite3
from pathlib import Path

def add_stripe_columns_to_all_tables():
    """Add Stripe customer and subscription ID columns to all user tables"""

    # Try multiple possible database paths
    possible_paths = [
        Path("persist/cozmiclearning.db"),  # Render production path
        Path("instance/cozmic.db"),  # Local development path
        Path("/opt/render/project/src/persist/cozmiclearning.db"),  # Absolute Render path
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

        # Tables to update
        tables = ['students', 'teachers', 'parents']
        total_columns_added = 0

        for table in tables:
            print(f"\n📋 Checking {table} table...")

            # Check if table exists
            cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'")
            if not cursor.fetchone():
                print(f"   ⚠️  Table {table} does not exist, skipping")
                continue

            # Check if columns already exist
            cursor.execute(f"PRAGMA table_info({table})")
            columns = [column[1] for column in cursor.fetchall()]

            columns_to_add = []
            if 'stripe_customer_id' not in columns:
                columns_to_add.append(('stripe_customer_id', 'VARCHAR(255)'))
            if 'stripe_subscription_id' not in columns:
                columns_to_add.append(('stripe_subscription_id', 'VARCHAR(255)'))

            if not columns_to_add:
                print(f"   ✅ Stripe columns already exist in {table}")
                continue

            # Add missing columns
            for column_name, column_type in columns_to_add:
                print(f"   📝 Adding column: {column_name} ({column_type})")
                cursor.execute(f"ALTER TABLE {table} ADD COLUMN {column_name} {column_type}")
                print(f"   ✅ Added {column_name}")
                total_columns_added += 1

        # Commit changes
        conn.commit()
        conn.close()

        print("\n" + "="*60)
        print("✅ Migration completed successfully!")
        print("="*60)
        print(f"   Added {total_columns_added} total column(s) across all tables")
        print("   Tables updated: students, teachers, parents")
        print("="*60)

        return True

    except Exception as e:
        print(f"\n❌ Error during migration: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("="*60)
    print("  Stripe Columns Migration for All User Tables")
    print("="*60)
    print()

    success = add_stripe_columns_to_all_tables()

    if success:
        print("\n✅ You can now run your app without the database error!")
    else:
        print("\n❌ Migration failed. Please check the error messages above.")
