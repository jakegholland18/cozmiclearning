"""
Migration Script: Add Stripe Columns to Students Table
Adds stripe_customer_id and stripe_subscription_id columns to the students table
"""

import sqlite3
from pathlib import Path

def add_stripe_columns_to_students():
    """Add Stripe customer and subscription ID columns to students table"""

    # Database path
    db_path = Path("instance/cozmic.db")

    if not db_path.exists():
        print(f"❌ Database not found at {db_path}")
        print("   Make sure you're running this from the project root directory")
        return False

    try:
        # Connect to database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Check if columns already exist
        cursor.execute("PRAGMA table_info(students)")
        columns = [column[1] for column in cursor.fetchall()]

        columns_to_add = []
        if 'stripe_customer_id' not in columns:
            columns_to_add.append(('stripe_customer_id', 'VARCHAR(255)'))
        if 'stripe_subscription_id' not in columns:
            columns_to_add.append(('stripe_subscription_id', 'VARCHAR(255)'))

        if not columns_to_add:
            print("✅ Stripe columns already exist in students table")
            conn.close()
            return True

        # Add missing columns
        for column_name, column_type in columns_to_add:
            print(f"📝 Adding column: {column_name} ({column_type})")
            cursor.execute(f"ALTER TABLE students ADD COLUMN {column_name} {column_type}")
            print(f"✅ Added {column_name}")

        # Commit changes
        conn.commit()
        conn.close()

        print("\n" + "="*60)
        print("✅ Migration completed successfully!")
        print("="*60)
        print(f"   Added {len(columns_to_add)} column(s) to students table:")
        for column_name, _ in columns_to_add:
            print(f"   - {column_name}")
        print("="*60)

        return True

    except Exception as e:
        print(f"\n❌ Error during migration: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("="*60)
    print("  Stripe Columns Migration for Students Table")
    print("="*60)
    print()

    success = add_stripe_columns_to_students()

    if success:
        print("\n✅ You can now run your app without the database error!")
    else:
        print("\n❌ Migration failed. Please check the error messages above.")
