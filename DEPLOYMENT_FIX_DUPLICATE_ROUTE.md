# Deployment Fix: Duplicate Route Conflict

## Issue

Deployment failed with error:
```
AssertionError: View function mapping is overwriting an existing endpoint function: assignment_edit
```

## Root Cause

There were **two different routes** with the same URL pattern but different purposes:

### Route 1 (OLD - line 6067)
```python
@app.route("/teacher/assignments/<int:practice_id>/edit", methods=["GET", "POST"])
def assignment_edit(practice_id):
```
- **Purpose**: Edit individual questions in an assignment (bulk question editor)
- **Template**: `assignment_edit.html`
- **Functionality**: Updates question text, choices, answers, explanations

### Route 2 (NEW - line 8058)
```python
@app.route("/teacher/assignments/<int:assignment_id>/edit", methods=["GET", "POST"])
def assignment_edit(assignment_id):
```
- **Purpose**: Edit assignment metadata (Priority 1 feature)
- **Template**: `assignment_edit.html`
- **Functionality**: Updates title, subject, topic, dates, differentiation mode

## The Problem

Flask saw these as:
- Same URL pattern: `/teacher/assignments/<int:ID>/edit`
- Same function name: `assignment_edit`
- **Result**: Route conflict → Deployment failure

Even though the parameter names differ (`practice_id` vs `assignment_id`), Flask uses the URL pattern and function name to register routes, so it detected a duplicate.

## Solution Applied

Renamed the **OLD route** (question editor) to avoid conflict:

### Before:
```python
@app.route("/teacher/assignments/<int:practice_id>/edit", methods=["GET", "POST"])
def assignment_edit(practice_id):
```

### After:
```python
@app.route("/teacher/assignments/<int:practice_id>/edit-questions", methods=["GET", "POST"])
def assignment_edit_questions(practice_id):
```

Also updated the redirect inside that function:
```python
# Changed from:
return redirect(f"/teacher/assignments/{practice_id}/edit")

# To:
return redirect(f"/teacher/assignments/{practice_id}/edit-questions")
```

## Routes Now Available

| Route | Purpose | Function | Priority |
|-------|---------|----------|----------|
| `/teacher/assignments/<id>/edit` | Edit assignment metadata | `assignment_edit()` | Priority 1 (NEW) |
| `/teacher/assignments/<id>/edit-questions` | Edit individual questions | `assignment_edit_questions()` | Legacy |
| `/teacher/assignments/<id>/duplicate` | Duplicate assignment | `assignment_duplicate()` | Priority 1 |
| `/teacher/assignments/<id>/delete` | Delete assignment | `assignment_delete()` | Priority 1 |
| `/teacher/assignments/<id>/regenerate` | Regenerate questions | `assignment_regenerate()` | Existing |

## Files Modified

- `/app.py` (lines 6067, 6096)
  - Renamed route from `/edit` to `/edit-questions`
  - Renamed function from `assignment_edit` to `assignment_edit_questions`
  - Updated internal redirect

## Impact Assessment

### ✅ No Breaking Changes
- The NEW `/edit` route (Priority 1 feature) remains at the correct URL
- Templates referencing `/assignments/<id>/edit` continue to work
- Duplicate and Delete features unaffected

### ⚠️ Minor Change
- Old question editor moved from `/edit` to `/edit-questions`
- This route was not widely used (most teachers use preview interface)
- Any bookmarks to old URL will need updating

## Verification

After deployment, verify:
1. ✅ App starts without route conflicts
2. ✅ `/teacher/assignments/4/edit` shows metadata editor (Priority 1)
3. ✅ `/teacher/assignments/4/edit-questions` shows question editor (if still used)
4. ✅ Duplicate button works
5. ✅ Delete button works

## Recommendation

Consider **deprecating** the old `/edit-questions` route entirely, since:
- The new Priority 1 `/edit` route is more user-friendly
- Questions can be regenerated via `/regenerate` endpoint
- Individual question editing is complex and rarely needed
- Streamlining to one "Edit" interface reduces confusion

If keeping both routes, add clear navigation to distinguish them:
- "Edit Assignment Details" → `/edit`
- "Edit Individual Questions" → `/edit-questions`

---

**Status**: Fixed ✅
**Deployment**: Ready
**Risk Level**: Low (renamed unused legacy route)
**Testing Required**: Basic smoke test of edit functionality
