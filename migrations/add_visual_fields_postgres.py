"""
Add visual aid fields to AssignedQuestion table (PostgreSQL version)
Adds fields for storing ASCII diagrams, Mermaid charts, and visual descriptions
"""

import os
import sys

def migrate():
    """Add visual fields to assigned_questions table"""

    # Set environment variable to skip Stripe validation for migrations
    os.environ['SKIP_STRIPE_CHECK'] = 'true'

    # Import after adding parent directory to path
    sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

    from app import app, db
    from sqlalchemy import text

    print("Starting migration: add visual fields to assigned_questions")

    with app.app_context():
        try:
            print(f"Connected to database: {db.engine.url}")

            # Check if columns already exist
            result = db.session.execute(
                text("""
                SELECT column_name
                FROM information_schema.columns
                WHERE table_name = 'assigned_questions'
                AND column_name IN ('visual_type', 'visual_content', 'visual_caption')
                """)
            )

            existing_columns = [row[0] for row in result.fetchall()]
            result.close()

            columns_to_add = []
            if 'visual_type' not in existing_columns:
                columns_to_add.append(('visual_type', 'TEXT'))
            if 'visual_content' not in existing_columns:
                columns_to_add.append(('visual_content', 'TEXT'))
            if 'visual_caption' not in existing_columns:
                columns_to_add.append(('visual_caption', 'TEXT'))

            if not columns_to_add:
                print("⏭️  All columns already exist. Nothing to do.")
                return True

            # Add columns
            for column_name, column_def in columns_to_add:
                print(f"Adding column '{column_name}' to assigned_questions...")
                db.session.execute(
                    text(f"""
                    ALTER TABLE assigned_questions
                    ADD COLUMN {column_name} {column_def}
                    """)
                )
                db.session.commit()
                print(f"✅ Added column '{column_name}'")

            print(f"\n✅ Migration completed successfully!")
            print(f"   Added {len(columns_to_add)} column(s)")
            return True

        except Exception as e:
            print(f"❌ Migration failed with error: {e}")
            import traceback
            traceback.print_exc()
            db.session.rollback()
            return False

if __name__ == "__main__":
    print("Running migration: Add visual fields to questions...")
    success = migrate()
    if success:
        print("\n✅ Migration completed successfully!")
    else:
        print("\n❌ Migration failed!")
        sys.exit(1)
