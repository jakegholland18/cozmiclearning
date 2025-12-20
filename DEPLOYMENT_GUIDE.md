# 🚀 Deployment Guide - Self-Practice Tracking Feature

## Overview
This deployment adds self-practice tracking to the student gradebook with clear visual distinction from teacher-assigned work.

## Pre-Deployment Checklist

### ✅ Files to Deploy
All changes are committed in the last 9 commits. Deploy the entire repository or these specific files:

**Database & Models:**
- `models.py` - New PracticeSession model
- `migrate_practice_sessions.py` - Migration script
- `create_practice_sessions_table.sql` - SQL migration

**Backend:**
- `app.py` - New save route + updated gradebook route

**Frontend:**
- `website/templates/student_gradebook.html` - Two distinct sections
- `website/templates/full_practice.html` - Auto-save integration
- `website/templates/practice_unified.html` - Auto-save integration

**Documentation:**
- `PRACTICE_TRACKING_README.md` - Implementation guide
- `DEPLOYMENT_GUIDE.md` - This file

---

## Deployment Steps

### Step 1: Pull Latest Code
```bash
git pull origin main
```

### Step 2: Database Migration

**Option A: Python Migration (Recommended)**
```bash
python3 migrate_practice_sessions.py
```

**Option B: SQL Migration**
```bash
sqlite3 persistent_db/cozmiclearning.db < create_practice_sessions_table.sql
```

**Option C: Auto-create on startup**
The table will be created automatically when the app starts with the new models.

### Step 3: Verify Migration
```bash
sqlite3 persistent_db/cozmiclearning.db "SELECT sql FROM sqlite_master WHERE name='practice_sessions';"
```

Expected output should show the table schema.

### Step 4: Restart Application
```bash
# If using systemd
sudo systemctl restart cozmiclearning

# If using PM2
pm2 restart cozmiclearning

# If running manually
# Kill the current process and restart
```

### Step 5: Verify Deployment

1. **Test Practice Session Creation:**
   - Log in as a student
   - Complete a practice session in Learning Planets
   - Check browser console for: `✅ Practice session saved to gradebook!`

2. **Test Gradebook Display:**
   - Navigate to `/student/gradebook`
   - Verify two sections appear:
     - "👨‍🏫 Teacher-Assigned Work" (blue)
     - "🌟 My Self-Practice" (gold/yellow)

3. **Test Database:**
   ```bash
   sqlite3 persistent_db/cozmiclearning.db "SELECT COUNT(*) FROM practice_sessions;"
   ```

---

## Expected Changes

### What Students Will See:

**Before:**
- Only teacher-assigned work in gradebook
- No practice history
- Single unified view

**After:**
- Clear section headers with color coding
- Teacher work (blue) separate from self-practice (gold)
- Complete practice history with stats
- Automatic saving when practice completes

### What Teachers Will See:
- No changes to teacher views
- Teachers only see assigned work in their dashboards

---

## Rollback Plan

If issues occur, rollback to previous version:

```bash
# Rollback code
git reset --hard HEAD~9
git push --force origin main

# Remove practice_sessions table (optional)
sqlite3 persistent_db/cozmiclearning.db "DROP TABLE IF EXISTS practice_sessions;"

# Restart application
sudo systemctl restart cozmiclearning
```

---

## Monitoring

### Things to Monitor:

1. **Database Growth:**
   ```bash
   sqlite3 persistent_db/cozmiclearning.db "SELECT COUNT(*) FROM practice_sessions;"
   ```

2. **Error Logs:**
   Check for errors related to `/save_practice_session`

3. **Student Feedback:**
   - Are practice sessions being saved?
   - Is the gradebook displaying correctly?
   - Are students seeing both sections?

### Success Metrics:

- Practice sessions being saved (check database)
- No 500 errors on `/save_practice_session`
- Students can view gradebook without errors
- Browser console shows successful saves

---

## Troubleshooting

### Issue: Migration fails
**Solution:** Use Option B (SQL migration) or Option C (auto-create)

### Issue: Practice sessions not appearing in gradebook
**Possible causes:**
1. Student not logged in when completing practice
2. Migration not run (table doesn't exist)
3. Frontend not calling save endpoint

**Debug:**
```bash
# Check if table exists
sqlite3 persistent_db/cozmiclearning.db ".tables" | grep practice

# Check for recent sessions
sqlite3 persistent_db/cozmiclearning.db "SELECT * FROM practice_sessions ORDER BY started_at DESC LIMIT 5;"
```

### Issue: 500 error on /save_practice_session
**Check:**
- PracticeSession imported in app.py
- Database table exists
- Student is logged in (student_id in session)

---

## Performance Considerations

### Database Indices
The following indices are created automatically:
- `idx_practice_session_student_id` - Fast student lookups
- `idx_practice_session_started_at` - Fast date sorting

### Expected Load
- Practice session save: ~1-2 seconds per completion
- Gradebook query: Fast (indexed queries)
- Minimal impact on existing functionality

---

## Security Notes

- ✅ CSRF protection on save route (exempt for JSON API)
- ✅ Student authentication required
- ✅ Students can only see their own practice sessions
- ✅ No sensitive data in practice_data_json
- ✅ Cascade delete on student deletion

---

## Post-Deployment Verification

Run this checklist after deployment:

- [ ] Database migration successful
- [ ] Application restarted without errors
- [ ] Student can complete practice in Learning Planets
- [ ] Browser console shows save success message
- [ ] Gradebook shows two distinct sections
- [ ] Practice sessions appear in gold section
- [ ] Stats calculate correctly
- [ ] No errors in application logs
- [ ] Performance acceptable (< 2s page loads)

---

## Support

If issues occur:

1. Check application logs
2. Check browser console for JavaScript errors
3. Verify database migration
4. Review [PRACTICE_TRACKING_README.md](PRACTICE_TRACKING_README.md)
5. Test with a fresh student account

---

## Future Enhancements

Planned improvements (not in this deployment):
- Practice streak tracking
- Practice analytics charts
- Achievement badges
- Practice recommendations
- Export to PDF

