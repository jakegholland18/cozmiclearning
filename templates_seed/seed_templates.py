"""
Seed script to load assignment templates into the database.

This script:
1. Scans the templates/ directory for JSON files
2. Parses each template file
3. Creates AssignmentTemplate records in the database
4. Sets system templates (teacher_id=None, is_public=True)

Usage:
    python3 templates_seed/seed_templates.py
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Add parent directory to path to import app modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from app import app, db
from models import AssignmentTemplate

def load_template_file(file_path):
    """Load and parse a template JSON file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except Exception as e:
        print(f"❌ Error loading {file_path}: {e}")
        return None

def create_template_from_data(data):
    """Create an AssignmentTemplate record from template data."""
    try:
        # Extract metadata
        title = data.get('title')
        description = data.get('description')
        subject = data.get('subject')
        grade_level = data.get('grade_level')
        tags = data.get('tags', [])
        template_data = data.get('template_data', {})

        # Check if template already exists (by title and subject)
        existing = AssignmentTemplate.query.filter_by(
            title=title,
            subject=subject,
            teacher_id=None  # System templates only
        ).first()

        if existing:
            print(f"⏭️  Skipping (already exists): {title}")
            return None

        # Create new template
        template = AssignmentTemplate(
            teacher_id=None,  # System template
            parent_id=None,
            title=title,
            description=description,
            subject=subject,
            grade_level=grade_level,
            template_data=json.dumps(template_data),
            is_public=True,  # All system templates are public
            use_count=0,
            tags=json.dumps(tags),
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

        db.session.add(template)
        return template

    except Exception as e:
        print(f"❌ Error creating template: {e}")
        return None

def seed_templates():
    """Main seeding function."""
    print("\n" + "="*60)
    print("🌱 SEEDING ASSIGNMENT TEMPLATES")
    print("="*60 + "\n")

    templates_dir = Path(__file__).parent / "templates"

    if not templates_dir.exists():
        print(f"❌ Templates directory not found: {templates_dir}")
        return

    # Scan for all JSON files
    json_files = list(templates_dir.rglob("*.json"))

    if not json_files:
        print(f"❌ No template JSON files found in {templates_dir}")
        return

    print(f"📁 Found {len(json_files)} template files\n")

    created_count = 0
    skipped_count = 0
    error_count = 0

    # Process each template file
    for json_file in sorted(json_files):
        relative_path = json_file.relative_to(templates_dir)
        print(f"📄 Processing: {relative_path}")

        # Load template data
        data = load_template_file(json_file)
        if not data:
            error_count += 1
            continue

        # Create template in database
        template = create_template_from_data(data)

        if template:
            created_count += 1
            print(f"   ✅ Created: {data.get('title')}")
            print(f"      Subject: {data.get('subject')} | Grade: {data.get('grade_level')}")
            print(f"      Questions: {len(data.get('template_data', {}).get('questions', []))}")
        else:
            skipped_count += 1

        print()

    # Commit all changes
    try:
        db.session.commit()
        print("="*60)
        print(f"✅ DATABASE COMMIT SUCCESSFUL")
        print("="*60)
    except Exception as e:
        db.session.rollback()
        print("="*60)
        print(f"❌ DATABASE COMMIT FAILED: {e}")
        print("="*60)
        return

    # Print summary
    print(f"\n📊 SUMMARY:")
    print(f"   ✅ Created: {created_count}")
    print(f"   ⏭️  Skipped: {skipped_count}")
    print(f"   ❌ Errors: {error_count}")
    print(f"   📁 Total: {len(json_files)}")

    # Verify in database
    total_system_templates = AssignmentTemplate.query.filter_by(teacher_id=None).count()
    print(f"\n🗄️  Total system templates in database: {total_system_templates}\n")

if __name__ == "__main__":
    with app.app_context():
        seed_templates()
