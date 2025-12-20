# Database Migrations

This directory contains database migration scripts for CozmicLearning.

## Available Migrations

### Security Columns Migration
**Purpose:** Add `failed_login_attempts` and `account_locked_until` columns to the `students` table for account security features.

**Files:**
- `add_security_columns_direct.py` - Direct SQLite migration (no dependencies)
- `add_security_columns_postgres.py` - PostgreSQL migration using Flask app context
- `add_security_columns.sql` - Raw SQL script for both databases

**Error This Fixes:**
```
psycopg2.errors.UndefinedColumn: column students.failed_login_attempts does not exist
```

## How to Run Migrations

### For SQLite (Local Development)

**Option 1: Direct Python Script (Recommended)**
```bash
python3 migrations/add_security_columns_direct.py
```

**Option 2: SQL Script**
```bash
sqlite3 persistent_db/cozmiclearning.db < migrations/add_security_columns.sql
```

### For PostgreSQL (Production/Render)

**Option 1: Python Script**
```bash
# Make sure .env has database credentials
source .venv/bin/activate
python3 migrations/add_security_columns_postgres.py
```

**Option 2: SQL Script via psql**
```bash
psql -U username -d database_name -f migrations/add_security_columns.sql
```

**Option 3: Via Render Dashboard**
1. Go to your Render PostgreSQL dashboard
2. Click "Connect" → "External Connection"
3. Use the connection string to connect via psql or pgAdmin
4. Run the SQL script manually

**Option 4: Via Render Shell**
```bash
# In Render web service shell
python migrations/add_security_columns_postgres.py
```

## Migration Safety

All migration scripts include:
- ✅ Column existence checks (won't duplicate columns)
- ✅ Transaction support (rollback on error)
- ✅ Clear error messages
- ✅ Verbose output for debugging

## Practice Tracking Migration

**Files:**
- `migrate_practice_tracking.py` - Adds practice session tracking to database
- `migrate_practice_tracking.sql` - SQL version

**Run:**
```bash
python3 migrations/migrate_practice_tracking.py
```

## Troubleshooting

### "ModuleNotFoundError: No module named 'dotenv'"
**Solution:** Activate virtual environment first
```bash
source .venv/bin/activate
python3 migrations/your_migration.py
```

### "Missing Required Environment Variables"
**Solution:** Use the direct script or set dummy values
```bash
# For migrations only, set dummy Stripe keys
export STRIPE_SECRET_KEY="sk_test_dummy"
export STRIPE_PUBLISHABLE_KEY="pk_test_dummy"
python3 migrations/add_security_columns_postgres.py
```

### "Table doesn't exist"
**Solution:** Run initial database setup first
```bash
python3 -c "from app import app, db; app.app_context().push(); db.create_all()"
```

### PostgreSQL on Render
If you're seeing psycopg2 errors but running SQLite locally:
1. The error is from your Render deployment (PostgreSQL)
2. Run the migration on Render via shell or SQL script
3. Your local SQLite database is already migrated
