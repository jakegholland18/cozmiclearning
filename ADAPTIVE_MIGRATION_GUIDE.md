# Adaptive Tracking Migration Guide

## Problem
The production PostgreSQL database is missing two columns in the `student_submissions` table:
- `current_question_index`
- `mc_phase_complete`

This causes 500 errors when students try to view assignments.

## Solution
Run the migration using one of the methods below.

---

## Method 1: Browser-Based Migration (Recommended)

This is the easiest method - just visit a URL while logged in as admin.

### Steps:
1. **Login to the site** as an admin user
2. **Visit this URL** in your browser:
   ```
   https://cozmiclearning.com/admin/migrate-adaptive
   ```
3. **Check the response** - you should see:
   ```json
   {
     "success": true,
     "message": "Migration completed successfully",
     "output": "... migration details ..."
   }
   ```

### Expected Output:
```
======================================================================
MANUAL MIGRATION: Add Adaptive Tracking Columns
======================================================================

Database dialect: postgresql

Checking existing columns in student_submissions table...

----------------------------------------------------------------------
❌ Column 'current_question_index' is MISSING - adding now...
✅ Successfully added 'current_question_index' column

----------------------------------------------------------------------
❌ Column 'mc_phase_complete' is MISSING - adding now...
✅ Successfully added 'mc_phase_complete' column

======================================================================
VERIFICATION: Checking final table structure...
======================================================================
✅ current_question_index: integer (default: 0)
✅ mc_phase_complete: boolean (default: false)

======================================================================
✅ MIGRATION SUCCESSFUL!
======================================================================
```

---

## Method 2: Shell Command (Advanced)

If you have SSH access to the Render instance:

### Steps:
1. **SSH into Render** (if available)
2. **Navigate to project directory**:
   ```bash
   cd /opt/render/project/src
   ```
3. **Run the migration script**:
   ```bash
   python3 manual_migrate_adaptive.py
   ```

---

## Method 3: Wait for Auto-Deploy

The migration is configured to run automatically on startup:
- It's registered in `run_startup_migrations.py` as Migration 6
- Every time the app deploys, it should run automatically
- However, if this fails silently, use Method 1 or 2 above

---

## Verification

After running the migration, verify it worked:

### 1. Check the assignments page works:
Visit: `https://cozmiclearning.com/student/assignments`

You should NOT see this error anymore:
```
column student_submissions.current_question_index does not exist
```

### 2. Check Render logs:
Look for these success messages in the deployment logs:
```
📋 Migration 6: Add adaptive assignment tracking columns
✅ Successfully added 'current_question_index' column
✅ Successfully added 'mc_phase_complete' column
```

---

## Troubleshooting

### Issue: "Access denied" when visiting /admin/migrate-adaptive
**Solution:** Make sure you're logged in as an admin user first.

### Issue: Migration shows columns already exist
**Solution:** This is good! The columns are already there. The error might be from cached code. Try:
1. Clear browser cache
2. Restart the Render service
3. Check if a different database is being used

### Issue: Migration fails with connection error
**Solution:**
1. Check that `DATABASE_URL` environment variable is set in Render
2. Verify the PostgreSQL database is running
3. Check Render logs for database connection errors

### Issue: Columns added but still getting errors
**Solution:**
1. Restart the Render service to reload the database schema
2. Check if SQLAlchemy is caching the old schema
3. Verify no code is using a different database connection

---

## Files Involved

- [models.py:332-333](models.py#L332-L333) - Model definition with the columns
- [migrations/add_adaptive_tracking_postgres.py](migrations/add_adaptive_tracking_postgres.py) - Auto-migration script
- [run_startup_migrations.py:80-89](run_startup_migrations.py#L80-L89) - Migration registration
- [app.py:3919-4048](app.py#L3919-L4048) - Manual migration endpoint
- [manual_migrate_adaptive.py](manual_migrate_adaptive.py) - Standalone migration script

---

## What These Columns Do

These columns support the hybrid adaptive assignment feature:

- **`current_question_index`**: Tracks which question the student is currently on (0-based index)
- **`mc_phase_complete`**: Boolean flag indicating when student finishes multiple choice questions and moves to free response phase

They're used to implement a two-phase assignment system:
1. **Phase 1**: Multiple choice questions (adaptive difficulty)
2. **Phase 2**: Free response questions (unlocked after completing MC phase)

---

## Next Steps After Migration

Once the migration is successful:
1. ✅ Test the `/student/assignments` page - should load without errors
2. ✅ Test creating and viewing assignments
3. ✅ Monitor Render logs for any new errors
4. ✅ Consider adding this migration to your deployment checklist

---

## Support

If you continue to see errors after running the migration:
1. Check the Render deployment logs
2. Verify the migration completed successfully
3. Restart the Render service
4. Contact support with the error details from the logs
