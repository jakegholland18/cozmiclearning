"""
Add output moderation columns to QuestionLog table (SQLite version)
Tracks when AI-generated responses are flagged for inappropriate content
"""

import sqlite3
import os

def migrate():
    """Add output moderation columns to question_logs table"""

    db_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "persistent_db",
        "cozmiclearning.db"
    )

    print(f"Starting migration: add output moderation columns to question_logs")
    print(f"Database: {db_path}")

    if not os.path.exists(db_path):
        print(f"❌ Database not found at {db_path}")
        return False

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Check if columns already exist
        cursor.execute("PRAGMA table_info(question_logs)")
        columns = [col[1] for col in cursor.fetchall()]

        columns_to_add = []
        if 'output_flagged' not in columns:
            columns_to_add.append(('output_flagged', 'BOOLEAN DEFAULT 0'))
        if 'output_moderation_reason' not in columns:
            columns_to_add.append(('output_moderation_reason', 'TEXT'))

        if not columns_to_add:
            print("⏭️  All columns already exist. Nothing to do.")
            conn.close()
            return True

        # Add columns
        for column_name, column_def in columns_to_add:
            print(f"Adding column '{column_name}' to question_logs...")
            cursor.execute(f"""
                ALTER TABLE question_logs
                ADD COLUMN {column_name} {column_def}
            """)
            print(f"✅ Added column '{column_name}'")

        conn.commit()
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
    print("Running migration: Add output moderation columns (SQLite)...")
    success = migrate()
    if success:
        print("\n✅ Migration completed successfully!")
    else:
        print("\n❌ Migration failed!")
        exit(1)
