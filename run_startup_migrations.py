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

    if success:
        logger.info("\n✅ All startup migrations completed successfully!")
    else:
        logger.warning("\n⚠️  Some migrations failed - check logs above")

    return success

if __name__ == "__main__":
    run_migrations()
