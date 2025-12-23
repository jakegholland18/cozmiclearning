"""
Add output moderation columns to QuestionLog table (PostgreSQL version)
Tracks when AI-generated responses are flagged for inappropriate content
"""

import os
import sys

def migrate():
    """Add output moderation columns to question_logs table"""

    # Set environment variable to skip Stripe validation for migrations
    os.environ['SKIP_STRIPE_CHECK'] = 'true'

    # Import after adding parent directory to path
    sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

    from app import app, db
    from sqlalchemy import text

    print("Starting migration: add output moderation columns to question_logs")

    with app.app_context():
        try:
            print(f"Connected to database: {db.engine.url}")

            # Check if columns already exist
            result = db.session.execute(
                text("""
                SELECT column_name
                FROM information_schema.columns
                WHERE table_name = 'question_logs'
                AND column_name IN ('output_flagged', 'output_moderation_reason')
                """)
            )

            existing_columns = [row[0] for row in result.fetchall()]
            result.close()

            columns_to_add = []
            if 'output_flagged' not in existing_columns:
                columns_to_add.append(('output_flagged', 'BOOLEAN DEFAULT FALSE'))
            if 'output_moderation_reason' not in existing_columns:
                columns_to_add.append(('output_moderation_reason', 'TEXT'))

            if not columns_to_add:
                print("⏭️  All columns already exist. Nothing to do.")
                return True

            # Add columns
            for column_name, column_def in columns_to_add:
                print(f"Adding column '{column_name}' to question_logs...")
                db.session.execute(
                    text(f"""
                    ALTER TABLE question_logs
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
    print("Running migration: Add output moderation columns...")
    success = migrate()
    if success:
        print("\n✅ Migration completed successfully!")
    else:
        print("\n❌ Migration failed!")
        sys.exit(1)
