"""
Add grade_released column to student_submissions table
Allows teachers to control when students can see their grades
"""

import sqlite3
import os

def migrate():
    # Try both database locations
    base_dir = os.path.dirname(os.path.dirname(__file__))
    db_paths = [
        os.path.join(base_dir, "persistent_db/cozmiclearning.db"),
        os.path.join(base_dir, "instance/cozmiclearning.db"),
    ]

    db_path = None
    for path in db_paths:
        if os.path.exists(path):
            db_path = path
            break

    if not db_path:
        print(f"❌ Database not found in any expected location")
        return False

    print(f"📍 Using database: {db_path}")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Check if column already exists
        cursor.execute("PRAGMA table_info(student_submissions)")
        columns = [col[1] for col in cursor.fetchall()]

        if "grade_released" in columns:
            print("✅ Column 'grade_released' already exists in student_submissions")
            return True

        # Add the column
        cursor.execute("""
            ALTER TABLE student_submissions
            ADD COLUMN grade_released BOOLEAN DEFAULT 0
        """)

        conn.commit()
        print("✅ Successfully added 'grade_released' column to student_submissions")

        # Set existing graded submissions to released=True for backward compatibility
        cursor.execute("""
            UPDATE student_submissions
            SET grade_released = 1
            WHERE status = 'graded'
        """)

        conn.commit()
        rows_updated = cursor.rowcount
        print(f"✅ Set grade_released=True for {rows_updated} existing graded submissions")

        return True

    except Exception as e:
        print(f"❌ Migration failed: {e}")
        conn.rollback()
        return False

    finally:
        conn.close()

if __name__ == "__main__":
    print("Running migration: Add grade_released column...")
    success = migrate()
    if success:
        print("\n✅ Migration completed successfully!")
    else:
        print("\n❌ Migration failed!")
