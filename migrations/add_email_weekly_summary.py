#!/usr/bin/env python3
"""
Add email_weekly_summary column to parents table

This column was added to the Parent model but missing from production database.
"""

import psycopg2
import os

# Get database URL from environment
DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://localhost/cozmiclearning')

# Fix old postgres:// URLs (SQLAlchemy requires postgresql://)
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

def run_migration():
    """Add email_weekly_summary column to parents table"""

    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()

        print("=" * 60)
        print("🔧 Adding email_weekly_summary column to parents table")
        print("=" * 60)

        # Check if column already exists
        cur.execute("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name='parents'
            AND column_name='email_weekly_summary'
        """)

        if cur.fetchone():
            print("✅ Column 'email_weekly_summary' already exists - skipping")
        else:
            # Add the column
            cur.execute("""
                ALTER TABLE parents
                ADD COLUMN email_weekly_summary BOOLEAN DEFAULT TRUE
            """)
            conn.commit()
            print("✅ Added column 'email_weekly_summary' to parents table")

        # Verify the column exists now
        cur.execute("""
            SELECT column_name, data_type, column_default
            FROM information_schema.columns
            WHERE table_name='parents'
            AND column_name='email_weekly_summary'
        """)

        result = cur.fetchone()
        if result:
            print(f"\n✓ Verified: {result[0]} ({result[1]}) default={result[2]}")

        cur.close()
        conn.close()

        print("=" * 60)
        print("✨ Migration complete!")
        print("=" * 60)

    except Exception as e:
        print(f"❌ Migration failed: {e}")
        import traceback
        traceback.print_exc()
        raise

if __name__ == '__main__':
    run_migration()
