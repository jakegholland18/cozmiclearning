#!/usr/bin/env python3
"""Create Learning Lab tables in PostgreSQL"""

import os
import sys

# Ensure we're using PostgreSQL
os.environ['DATABASE_URL'] = 'postgresql://localhost/cozmiclearning'

from app import app, db
from models import LearningProfile, StrategyUsage

if __name__ == '__main__':
    with app.app_context():
        print('=' * 60)
        print('🧠 Creating Learning Lab tables in PostgreSQL...')
        print('=' * 60)

        # Create tables
        db.create_all()

        # Verify they exist
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()

        print(f'\n📊 Database contains {len(tables)} tables')

        if 'learning_profiles' in tables:
            print('✅ learning_profiles table exists')

            # Get column info
            columns = inspector.get_columns('learning_profiles')
            print(f'   {len(columns)} columns:')
            for col in columns[:5]:
                print(f'   - {col["name"]} ({col["type"]})')
            if len(columns) > 5:
                print(f'   ... and {len(columns) - 5} more columns')
        else:
            print('❌ learning_profiles table NOT found')

        if 'strategy_usage' in tables:
            print('✅ strategy_usage table exists')

            # Get column info
            columns = inspector.get_columns('strategy_usage')
            print(f'   {len(columns)} columns')
        else:
            print('❌ strategy_usage table NOT found')

        print('=' * 60)
        print('✨ Migration complete!')
        print('=' * 60)
