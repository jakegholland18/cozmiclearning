"""
Add stripe_customer_id and stripe_subscription_id to all user models
Run this ONCE after deploying the model changes
"""

import sqlite3
import os
import sys

def get_db_path():
    """Find the database file"""
    possible_paths = [
        'instance/cozmiclearning.db',
        'persistent_db/cozmiclearning.db',
        '/opt/render/project/src/instance/cozmiclearning.db',
        '/opt/render/project/src/persistent_db/cozmiclearning.db',
    ]

    for path in possible_paths:
        if os.path.exists(path):
            return path

    if 'DB_PATH' in os.environ:
        return os.environ['DB_PATH']

    return None

def check_column_exists(cursor, table_name, column_name):
    """Check if a column exists in a table"""
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [col[1] for col in cursor.fetchall()]
    return column_name in columns

def add_stripe_columns():
    """Add stripe_customer_id and stripe_subscription_id columns"""
    print("🔧 Adding Stripe Customer/Subscription ID Fields")
    print("=" * 60)

    db_path = get_db_path()

    if not db_path:
        print("❌ ERROR: Could not find database file")
        print("\nSearched locations:")
        print("  - instance/cozmiclearning.db")
        print("  - persistent_db/cozmiclearning.db")
        print("  - /opt/render/project/src/instance/cozmiclearning.db")
        print("  - /opt/render/project/src/persistent_db/cozmiclearning.db")
        return False

    print(f"📁 Database found: {db_path}")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        tables = ['parents', 'teachers', 'students']

        for table in tables:
            print(f"\n📋 Migrating {table} table...")

            # Check if columns already exist
            if not check_column_exists(cursor, table, 'stripe_customer_id'):
                cursor.execute(f"ALTER TABLE {table} ADD COLUMN stripe_customer_id VARCHAR(255)")
                print(f"  ✅ Added stripe_customer_id to {table}")
            else:
                print(f"  ⏭️  stripe_customer_id already exists in {table}")

            if not check_column_exists(cursor, table, 'stripe_subscription_id'):
                cursor.execute(f"ALTER TABLE {table} ADD COLUMN stripe_subscription_id VARCHAR(255)")
                print(f"  ✅ Added stripe_subscription_id to {table}")
            else:
                print(f"  ⏭️  stripe_subscription_id already exists in {table}")

        conn.commit()

        print("\n" + "=" * 60)
        print("✅ Migration Complete!")
        print("\nStripe integration is now ready:")
        print("  • Customer IDs will be saved on new subscriptions")
        print("  • Subscription IDs will be tracked")
        print("  • Webhooks can now find users by customer_id")
        print("  • Cancellations will sync with Stripe")
        print("=" * 60)
        return True

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        print(traceback.format_exc())
        conn.rollback()
        return False

    finally:
        conn.close()

if __name__ == "__main__":
    success = add_stripe_columns()
    sys.exit(0 if success else 1)
