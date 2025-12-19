# Assignment #4 Issue - Complete Summary & Fix

## The Problem

Assignment #4 ("Money") was showing no questions for students despite appearing to have 7 questions on the teacher side.

## Root Cause Analysis

### What We Discovered

Using the debug endpoint (`/admin/assignment/4/debug`), we found:

```json
{
  "assignment_id": 4,
  "title": "Money",
  "differentiation_mode": "none",
  "is_published": true,          ← Published to students
  "has_preview_json": false,     ← NO QUESTIONS DATA!
  "preview_json_length": 0,
  "total_questions": 0
}
```

**The assignment has NO `preview_json` data, which means NO questions in the database.**

### Why Teachers Could See Questions

The preview endpoint ([app.py:7449-7467](app.py#L7449-L7467)) **generates questions on-the-fly** when `preview_json` is NULL. This means:

1. Teacher visits `/teacher/assignments/4/preview`
2. System sees `preview_json` is NULL
3. AI generates 7 questions in memory
4. Questions are displayed AND saved to `preview_json`
5. Teacher sees the questions

However, if the assignment was created before the PostgreSQL migration or if there was a database issue, the save might have failed.

### Why It Was Published Without Questions

This is the concerning part - the publish endpoint ([app.py:7592](app.py#L7592)) has a check that should prevent publishing without `preview_json`:

```python
if not assignment.preview_json:
    flash("You must preview this mission before publishing.", "error")
    return redirect(f"/teacher/assignments/{assignment.id}")
```

**Possible explanations:**
1. Assignment was created in SQLite, published there, then migrated to PostgreSQL without the `preview_json` data
2. Someone manually set `is_published=True` in the database
3. There was a code path that bypassed this check (now fixed)

## Fixes Implemented

### Fix 1: Better Error Handling for Students
- Added check for empty questions array ([app.py:6186-6189](app.py#L6186-L6189))
- Students now see: "This assignment has no questions. Please contact your teacher."
- Prevents blank/broken pages

### Fix 2: Regenerate Questions Endpoint
- New route: `/teacher/assignments/<id>/regenerate`
- Clears `preview_json` and forces fresh question generation
- Teachers can fix broken assignments easily

### Fix 3: Improved Publish Validation
- Better error message when trying to publish without questions
- Redirects to preview page to generate questions first

### Fix 4: Database Schema Migration
- Fixed the original PostgreSQL migration issue
- Added `current_question_index` and `mc_phase_complete` columns
- Migration successful via `/admin/migrate-adaptive`

### Fix 5: Debug Tools
- Added `/admin/assignment/<id>/debug` endpoint
- Shows complete assignment structure
- Helps diagnose similar issues in the future

## How to Fix Assignment #4

### Option 1: Regenerate Questions (Recommended)

1. Login as the teacher who created assignment #4
2. Visit: `https://cozmiclearning.com/teacher/assignments/4/regenerate`
3. This will:
   - Clear the empty `preview_json`
   - Redirect to preview
   - Generate fresh questions
   - Save them to the database
4. Review the generated questions
5. If satisfied, publish again

### Option 2: Create a New Assignment

1. Delete assignment #4 (or unpublish it)
2. Create a new assignment on the topic "Money"
3. Follow the proper workflow:
   - Create assignment
   - Preview (generates questions)
   - Review questions
   - Publish

### Option 3: Manual Database Fix (Advanced)

If you know what questions should be in the assignment, I can help you create a SQL script to insert them directly.

## Prevention Measures

### Changes Made:
1. ✅ Students now get helpful error messages instead of blank pages
2. ✅ Teachers can regenerate questions for broken assignments
3. ✅ Publish validation improved
4. ✅ Debug tools added for future issues

### Recommended Actions:
1. **Audit all published assignments** - Run this query to find others with no questions:
   ```sql
   SELECT id, title, is_published,
          CASE WHEN preview_json IS NULL OR preview_json = '' THEN 0
               ELSE 1 END as has_questions
   FROM assigned_practice
   WHERE is_published = true
   AND (preview_json IS NULL OR preview_json = '');
   ```

2. **Add a pre-publish checklist** in the UI:
   - ✓ Questions generated
   - ✓ Preview reviewed
   - ✓ Difficulty levels appropriate
   - ✓ Due date set

3. **Monitor assignment creation** in logs for AI generation failures

## Files Modified

1. **[app.py](app.py)**:
   - Added empty questions check (L6186-6189)
   - Added regenerate endpoint (L7558-7577)
   - Improved publish validation (L7592-7594)
   - Added debug endpoint (L3919-3968)
   - Added hybrid adaptive error handling (L6225-6238)

2. **[migrations/add_adaptive_tracking_postgres.py](migrations/add_adaptive_tracking_postgres.py)**:
   - Improved error handling
   - Added result set cleanup
   - Better logging

3. **[ADAPTIVE_MIGRATION_GUIDE.md](ADAPTIVE_MIGRATION_GUIDE.md)**:
   - Complete migration documentation

4. **[manual_migrate_adaptive.py](manual_migrate_adaptive.py)**:
   - Standalone migration script

## Testing Checklist

- [x] Database migration successful
- [x] Debug endpoint working
- [x] Empty assignment detection working
- [ ] Regenerate questions tested
- [ ] New assignment creation tested
- [ ] Student view fixed

## Next Steps

1. **Immediate**: Visit `/teacher/assignments/4/regenerate` to fix assignment #4
2. **Short-term**: Test the regenerate flow with a test assignment
3. **Long-term**: Audit all published assignments for similar issues

---

## Quick Reference

### Useful URLs (while logged in as admin):
- Debug assignment: `https://cozmiclearning.com/admin/assignment/4/debug`
- Regenerate questions: `https://cozmiclearning.com/teacher/assignments/4/regenerate`
- Preview assignment: `https://cozmiclearning.com/teacher/assignments/4/preview`
- Migrate database: `https://cozmiclearning.com/admin/migrate-adaptive`

### Logs to Check:
```bash
# On Render, check for:
📊 Assignment 4 loaded: 0 total questions
⚠️ No questions found in assignment 4
🔄 [REGENERATE] Forcing question regeneration for assignment 4
✅ [ASSIGNMENT_PREVIEW] Generated X questions
💾 [ASSIGNMENT_PREVIEW] Stored preview_json for assignment 4
```
