#!/usr/bin/env python3
"""
Clean up all existing visual diagrams from database
Removes visual_type, visual_content, visual_caption from all questions
"""

from app import app, db
from models import AssignedQuestion

if __name__ == '__main__':
    with app.app_context():
        print("🧹 Cleaning up visual diagrams from database...")
        print("=" * 60)

        # Count questions with visuals
        questions_with_visuals = AssignedQuestion.query.filter(
            AssignedQuestion.visual_type.isnot(None),
            AssignedQuestion.visual_type != 'none'
        ).count()

        print(f"Found {questions_with_visuals} questions with visual diagrams")

        if questions_with_visuals == 0:
            print("✅ No visuals to clean up!")
        else:
            # Update all questions to remove visuals
            updated = AssignedQuestion.query.update({
                'visual_type': 'none',
                'visual_content': '',
                'visual_caption': ''
            })

            db.session.commit()

            print(f"✅ Cleaned up {updated} questions")
            print("   - Set visual_type to 'none'")
            print("   - Cleared visual_content")
            print("   - Cleared visual_caption")

        print("=" * 60)
        print("✨ Cleanup complete!")
