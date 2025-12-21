"""
Add performance indexes to database tables for scalability
Adds indexes to Parent, Teacher, Class, Student, AssignedPractice, AssignedQuestion, and StudentSubmission tables
"""

import os
import sys

def migrate():
    """Add performance indexes to database tables"""

    # Import after adding parent directory to path
    sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

    from app import app, db
    from sqlalchemy import text

    print("Starting migration: add performance indexes")

    with app.app_context():
        try:
            print(f"Connected to database: {db.engine.url}")

            # Define all indexes to create
            indexes = [
                # Parent table indexes
                ("idx_parent_email", "parents", "email"),
                ("idx_parent_access_code", "parents", "access_code"),
                ("idx_parent_stripe_customer", "parents", "stripe_customer_id"),

                # Teacher table indexes
                ("idx_teacher_email", "teachers", "email"),
                ("idx_teacher_stripe_customer", "teachers", "stripe_customer_id"),

                # Class table indexes
                ("idx_class_teacher", "classes", "teacher_id"),
                ("idx_class_join_code", "classes", "join_code"),

                # Student table indexes
                ("idx_student_email", "students", "student_email"),
                ("idx_student_parent", "students", "parent_id"),
                ("idx_student_id", "students", "student_id"),
                ("idx_student_stripe_customer", "students", "stripe_customer_id"),

                # AssignedPractice table indexes
                ("idx_assignment_teacher", "assigned_practice", "teacher_id"),
                ("idx_assignment_class", "assigned_practice", "class_id"),
                ("idx_assignment_published", "assigned_practice", "is_published"),

                # AssignedQuestion table indexes
                ("idx_question_practice", "assigned_questions", "practice_id"),

                # StudentSubmission table indexes
                ("idx_submission_student", "student_submissions", "student_id"),
                ("idx_submission_assignment", "student_submissions", "assignment_id"),
                ("idx_submission_status", "student_submissions", "status"),
            ]

            # Composite indexes
            composite_indexes = [
                # AssignedPractice dates
                ("idx_assignment_dates", "assigned_practice", ["open_date", "due_date"]),
                # StudentSubmission timestamps
                ("idx_submission_timestamps", "student_submissions", ["started_at", "submitted_at"]),
            ]

            created_count = 0
            skipped_count = 0

            # Create single-column indexes
            for index_name, table_name, column_name in indexes:
                # Check if index already exists
                result = db.session.execute(
                    text("""
                    SELECT indexname
                    FROM pg_indexes
                    WHERE indexname = :index_name
                    """),
                    {"index_name": index_name}
                )

                row = result.fetchone()
                result.close()

                if row:
                    print(f"⏭️  Index '{index_name}' already exists on {table_name}({column_name})")
                    skipped_count += 1
                else:
                    print(f"Creating index '{index_name}' on {table_name}({column_name})...")
                    db.session.execute(
                        text(f"""
                        CREATE INDEX {index_name} ON {table_name}({column_name})
                        """)
                    )
                    db.session.commit()
                    created_count += 1
                    print(f"✅ Created index '{index_name}'")

            # Create composite indexes
            for index_name, table_name, columns in composite_indexes:
                # Check if index already exists
                result = db.session.execute(
                    text("""
                    SELECT indexname
                    FROM pg_indexes
                    WHERE indexname = :index_name
                    """),
                    {"index_name": index_name}
                )

                row = result.fetchone()
                result.close()

                if row:
                    print(f"⏭️  Index '{index_name}' already exists on {table_name}({', '.join(columns)})")
                    skipped_count += 1
                else:
                    columns_str = ', '.join(columns)
                    print(f"Creating composite index '{index_name}' on {table_name}({columns_str})...")
                    db.session.execute(
                        text(f"""
                        CREATE INDEX {index_name} ON {table_name}({columns_str})
                        """)
                    )
                    db.session.commit()
                    created_count += 1
                    print(f"✅ Created composite index '{index_name}'")

            print(f"\n✅ Migration completed successfully!")
            print(f"   Created: {created_count} indexes")
            print(f"   Skipped: {skipped_count} indexes (already exist)")
            return True

        except Exception as e:
            print(f"❌ Migration failed with error: {e}")
            import traceback
            traceback.print_exc()
            db.session.rollback()
            return False

if __name__ == "__main__":
    print("Running migration: Add performance indexes...")
    success = migrate()
    if success:
        print("\n✅ Migration completed successfully!")
    else:
        print("\n❌ Migration failed!")
        sys.exit(1)
