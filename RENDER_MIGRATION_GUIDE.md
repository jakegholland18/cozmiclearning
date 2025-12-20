# Render Migration Guide

## Quick Fix: Run Migration on Render

Your Render deployment is missing the security columns. Follow these steps:

### Step 1: Pull Latest Code on Render

In the Render shell, run:
```bash
git pull origin main
```

If you get any errors about uncommitted changes, run:
```bash
git stash
git pull origin main
```

### Step 2: Run the Migration

```bash
python migrations/add_security_columns_postgres.py
```

### Step 3: Restart the Service

In Render dashboard:
1. Go to your web service
2. Click "Manual Deploy" → "Clear build cache & deploy"

OR just wait for Render to auto-redeploy after you push changes.

---

## Alternative: Run SQL Directly on PostgreSQL

If you can't pull code or the Python script doesn't work, run SQL directly:

### Option A: Via Render Shell

```bash
# Connect to PostgreSQL
psql $DATABASE_URL

# Run these commands
ALTER TABLE students ADD COLUMN failed_login_attempts INTEGER DEFAULT 0;
ALTER TABLE students ADD COLUMN account_locked_until TIMESTAMP;

# Verify columns were added
\d students

# Exit
\q
```

### Option B: Via Render PostgreSQL Dashboard

1. Go to your Render PostgreSQL database
2. Click "Connect" → "External Connection"
3. Copy the connection string
4. On your local machine:
```bash
psql "postgresql://user:pass@host/database" -c "ALTER TABLE students ADD COLUMN failed_login_attempts INTEGER DEFAULT 0;"
psql "postgresql://user:pass@host/database" -c "ALTER TABLE students ADD COLUMN account_locked_until TIMESTAMP;"
```

### Option C: Manual SQL via pgAdmin or TablePlus

1. Get connection details from Render PostgreSQL dashboard
2. Connect using your favorite PostgreSQL client
3. Run:
```sql
ALTER TABLE students ADD COLUMN failed_login_attempts INTEGER DEFAULT 0;
ALTER TABLE students ADD COLUMN account_locked_until TIMESTAMP;
```

---

## Verify Migration Success

```bash
# In Render shell or via psql
psql $DATABASE_URL -c "\d students"
```

You should see both new columns:
- `failed_login_attempts` (integer)
- `account_locked_until` (timestamp without time zone)

---

## Troubleshooting

### "git pull" doesn't work
**Solution:** Your Render service might be using a specific commit hash. Instead:
1. Trigger a manual redeploy from Render dashboard
2. Render will automatically pull latest code from GitHub

### "psql: command not found"
**Solution:** Use the Python script instead:
```bash
python migrations/add_security_columns_postgres.py
```

### "No module named 'app'"
**Solution:** You might be in the wrong directory:
```bash
cd ~/project/src
python migrations/add_security_columns_postgres.py
```

### "Missing Required Environment Variables"
**Solution:** The migration script has been updated to bypass this check. If you still see it:
```bash
export SKIP_ENV_CHECK=true
python migrations/add_security_columns_postgres.py
```

---

## After Migration

Once the migration completes successfully:
1. Your app should start working without the psycopg2 error
2. The error about missing `failed_login_attempts` column will be resolved
3. Account lockout security features will be functional

No code changes needed - just run the migration once!
