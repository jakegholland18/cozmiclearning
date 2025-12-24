"""
Add visual aid fields to AssignedQuestion table (SQLite version)
Adds fields for storing ASCII diagrams, Mermaid charts, and visual descriptions
"""

import sqlite3
import os

def migrate():
    """Add visual fields to assigned_questions table"""

    db_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "persistent_db",
        "cozmiclearning.db"
    )

    print(f"Starting migration: add visual fields to assigned_questions")
    print(f"Database: {db_path}")

    if not os.path.exists(db_path):
        print(f"❌ Database not found at {db_path}")
        return False

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Check if columns already exist
        cursor.execute("PRAGMA table_info(assigned_questions)")
        columns = [col[1] for col in cursor.fetchall()]

        columns_to_add = []
        if 'visual_type' not in columns:
            columns_to_add.append(('visual_type', 'TEXT'))  # ascii, mermaid, description, none
        if 'visual_content' not in columns:
            columns_to_add.append(('visual_content', 'TEXT'))  # The actual visual content
        if 'visual_caption' not in columns:
            columns_to_add.append(('visual_caption', 'TEXT'))  # Caption for the visual

        if not columns_to_add:
            print("⏭️  All columns already exist. Nothing to do.")
            conn.close()
            return True

        # Add columns
        for column_name, column_def in columns_to_add:
            print(f"Adding column '{column_name}' to assigned_questions...")
            cursor.execute(f"""
                ALTER TABLE assigned_questions
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
    print("Running migration: Add visual fields to questions (SQLite)...")
    success = migrate()
    if success:
        print("\n✅ Migration completed successfully!")
    else:
        print("\n❌ Migration failed!")
        exit(1)
