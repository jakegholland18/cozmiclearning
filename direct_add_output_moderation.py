#!/usr/bin/env python3
"""
Direct database migration - adds output moderation columns WITHOUT importing app
This avoids the chicken-and-egg problem where app won't start without columns
"""

import os
import sys
import psycopg2
from urllib.parse import urlparse

def migrate():
    """Add output moderation columns directly to PostgreSQL"""

    # Get database URL from environment
    database_url = os.getenv('DATABASE_URL')

    if not database_url:
        print("❌ DATABASE_URL not found in environment")
        return False

    # Parse database URL
    url = urlparse(database_url)

    print(f"🔗 Connecting to database: {url.hostname}")

    try:
        # Connect directly to PostgreSQL
        conn = psycopg2.connect(
            host=url.hostname,
            port=url.port,
            database=url.path[1:],  # Remove leading /
            user=url.username,
            password=url.password
        )

        cursor = conn.cursor()

        print("✅ Connected successfully")

        # Check if columns already exist
        cursor.execute("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name = 'question_logs'
            AND column_name IN ('output_flagged', 'output_moderation_reason')
        """)

        existing_columns = [row[0] for row in cursor.fetchall()]

        columns_to_add = []
        if 'output_flagged' not in existing_columns:
            columns_to_add.append(('output_flagged', 'BOOLEAN DEFAULT FALSE'))
        if 'output_moderation_reason' not in existing_columns:
            columns_to_add.append(('output_moderation_reason', 'TEXT'))

        if not columns_to_add:
            print("⏭️  All columns already exist. Nothing to do.")
            cursor.close()
            conn.close()
            return True

        # Add columns
        for column_name, column_def in columns_to_add:
            print(f"📝 Adding column '{column_name}' to question_logs...")
            cursor.execute(f"""
                ALTER TABLE question_logs
                ADD COLUMN {column_name} {column_def}
            """)
            conn.commit()
            print(f"✅ Added column '{column_name}'")

        cursor.close()
        conn.close()

        print(f"\n✅ Migration completed successfully!")
        print(f"   Added {len(columns_to_add)} column(s)")
        return True

    except Exception as e:
        print(f"❌ Migration failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("DIRECT DATABASE MIGRATION: Add Output Moderation Columns")
    print("=" * 60)
    success = migrate()
    if success:
        print("\n✅ Migration completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Migration failed!")
        sys.exit(1)
