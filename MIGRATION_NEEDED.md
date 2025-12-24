# 🚨 Migration Required for Production

## Issue
Production database is missing the `email_weekly_summary` column in the `parents` table, causing 500 errors on dashboard.

**Error:**
```
sqlalchemy.exc.ProgrammingError: (psycopg2.errors.UndefinedColumn)
column parents.email_weekly_summary does not exist
```

## Solution
Run the migration script to add the missing column.

### Option 1: Run via Render Shell (Recommended)
1. Go to your Render dashboard
2. Select the `cozmiclearning` web service
3. Click "Shell" tab
4. Run the migration:
```bash
python3 migrations/add_email_weekly_summary.py
```

### Option 2: Run via SSH (if enabled)
```bash
ssh render-service-name
python3 migrations/add_email_weekly_summary.py
```

### Option 3: Add to Build Command (Automatic)
Update your Render build command to run migrations automatically:

**Current:** `pip install -r requirements.txt`

**New:** `pip install -r requirements.txt && python3 migrations/add_email_weekly_summary.py`

This will run the migration every time the service deploys (safe to run multiple times).

## What the Migration Does
- Adds `email_weekly_summary BOOLEAN DEFAULT TRUE` column to `parents` table
- Checks if column exists before adding (idempotent - safe to run multiple times)
- Verifies the column was added successfully

## After Running
- Dashboard will load without errors
- Parent accounts will have weekly summary emails enabled by default
- No data loss or downtime
