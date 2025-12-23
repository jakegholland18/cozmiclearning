#!/usr/bin/env python3
"""
Startup migrations - runs AFTER persistent disk is mounted
This runs once when the app starts up in production
"""

import os
import sys
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_migrations():
    """Run all necessary startup migrations"""

    logger.info("🚀 Running startup migrations...")

    # Only run in production (when persistent disk exists)
    if not os.path.exists('/opt/render/project/src/persistent_db'):
        logger.info("⏭️  Skipping migrations (not in production)")
        return True

    success = True

    # Migration 1: Fix production DB structure
    try:
        logger.info("\n📋 Migration 1: Fix production DB structure")
        from fix_production_db import migrate_production_db
        if not migrate_production_db():
            logger.error("❌ Failed to fix production DB")
            success = False
    except Exception as e:
        logger.error(f"❌ Error in fix_production_db: {e}")
        success = False

    # Migration 2: Initialize arcade enhancements
    try:
        logger.info("\n📋 Migration 2: Initialize arcade enhancements")
        from init_arcade_enhancements import init_arcade_enhancements
        init_arcade_enhancements()
    except Exception as e:
        logger.error(f"❌ Error in init_arcade_enhancements: {e}")
        # Don't fail startup if arcade init fails

    # Migration 3: Add Stripe customer/subscription IDs
    try:
        logger.info("\n📋 Migration 3: Add Stripe fields")
        from add_stripe_ids import add_stripe_columns
        if not add_stripe_columns():
            logger.error("❌ Failed to add Stripe fields")
            success = False
    except Exception as e:
        logger.error(f"❌ Error in add_stripe_ids: {e}")
        success = False

    # Migration 4: Add Assignment Templates table
    try:
        logger.info("\n📋 Migration 4: Add Assignment Templates")
        from add_assignment_templates_migration import add_assignment_templates
        if not add_assignment_templates():
            logger.error("❌ Failed to add assignment templates table")
            success = False
    except Exception as e:
        logger.error(f"❌ Error in add_assignment_templates: {e}")
        success = False

    # Migration 5: Add grade_released column to student_submissions
    try:
        logger.info("\n📋 Migration 5: Add grade_released column")
        sys.path.insert(0, os.path.dirname(__file__))
        from migrations.add_grade_released_postgres import migrate
        if not migrate():
            logger.error("❌ Failed to add grade_released column")
            success = False
    except Exception as e:
        logger.error(f"❌ Error in add_grade_released: {e}")
        success = False

    # Migration 6: Add adaptive tracking columns to student_submissions
    # Adds current_question_index and mc_phase_complete for hybrid adaptive assignments
    try:
        logger.info("\n📋 Migration 6: Add adaptive assignment tracking columns")
        from migrations.add_adaptive_tracking_postgres import migrate as migrate_adaptive
        if not migrate_adaptive():
            logger.error("❌ Failed to add adaptive tracking columns")
            success = False
    except Exception as e:
        logger.error(f"❌ Error in add_adaptive_tracking: {e}")
        success = False

    # Migration 7: Add performance indexes for scalability
    # Adds indexes to Parent, Teacher, Class, Student, AssignedPractice, AssignedQuestion, and StudentSubmission tables
    try:
        logger.info("\n📋 Migration 7: Add performance indexes")
        from migrations.add_performance_indexes import migrate as migrate_indexes
        if not migrate_indexes():
            logger.error("❌ Failed to add performance indexes")
            success = False
    except Exception as e:
        logger.error(f"❌ Error in add_performance_indexes: {e}")
        success = False

    # Migration 8: Add output moderation columns to QuestionLog
    # Adds output_flagged and output_moderation_reason columns for tracking AI response moderation
    try:
        logger.info("\n📋 Migration 8: Add output moderation columns")
        from migrations.add_output_moderation_columns import migrate as migrate_output_moderation
        if not migrate_output_moderation():
            logger.error("❌ Failed to add output moderation columns")
            success = False
    except Exception as e:
        logger.error(f"❌ Error in add_output_moderation_columns: {e}")
        success = False

    if success:
        logger.info("\n✅ All startup migrations completed successfully!")
    else:
        logger.warning("\n⚠️  Some migrations failed - check logs above")

    return success

if __name__ == "__main__":
    run_migrations()
