#!/usr/bin/env python3
"""
Migration: Add join_code field to classes table and generate codes for existing classes
"""

import sqlite3
import os
import random
import string

def generate_join_code():
    """Generate a unique 8-character join code"""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

def run_migration():
    """Add join_code column to classes table"""

    # Try production path first, then development path
    production_db = '/opt/render/project/src/persistent_db/cozmiclearning.db'
    dev_db = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'instance', 'cozmiclearning.db')

    if os.path.exists(production_db):
        db_path = production_db
        print(f"🔧 Using production database: {db_path}")
    elif os.path.exists(dev_db):
        db_path = dev_db
        print(f"🔧 Using development database: {db_path}")
    else:
        print(f"❌ Database not found at {production_db} or {dev_db}")
        return False

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Check if join_code column already exists
        cursor.execute("PRAGMA table_info(classes)")
        columns = [col[1] for col in cursor.fetchall()]

        if 'join_code' in columns:
            print("✅ join_code column already exists in classes table")
        else:
            print("📝 Adding join_code column to classes table...")
            cursor.execute("ALTER TABLE classes ADD COLUMN join_code VARCHAR(8)")
            print("✅ join_code column added successfully")

        # Generate unique join codes for existing classes that don't have one
        cursor.execute("SELECT id FROM classes WHERE join_code IS NULL")
        classes_without_codes = cursor.fetchall()

        if classes_without_codes:
            print(f"🔄 Generating join codes for {len(classes_without_codes)} existing classes...")

            for (class_id,) in classes_without_codes:
                # Generate unique code
                while True:
                    code = generate_join_code()
                    cursor.execute("SELECT id FROM classes WHERE join_code = ?", (code,))
                    if not cursor.fetchone():
                        break

                cursor.execute("UPDATE classes SET join_code = ? WHERE id = ?", (code, class_id))
                print(f"   Class {class_id}: {code}")

            print(f"✅ Generated {len(classes_without_codes)} join codes")
        else:
            print("✅ All classes already have join codes")

        conn.commit()
        conn.close()

        print("\n✅ Migration completed successfully!")
        return True

    except Exception as e:
        print(f"❌ Migration failed: {e}")
        return False

if __name__ == "__main__":
    print("🔄 Running class join code migration...\n")
    success = run_migration()
    exit(0 if success else 1)
