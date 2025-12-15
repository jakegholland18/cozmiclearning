# 🧪 How to Test Everything in CozmicLearning

## QUICK START (5 Minutes)

### Option 1: Run Complete Workflow Test (RECOMMENDED)
```bash
cd /Users/tamara/Desktop/cozmiclearning
python3 test_complete_workflow.py
```

**This tests:**
- ✅ Creates teacher, students, and parent accounts
- ✅ Teacher creates class and assigns work
- ✅ All 12 subjects load correctly
- ✅ RespectRealm with 44 lessons
- ✅ Student completes practice
- ✅ Teacher views analytics
- ✅ Parent views progress reports
- ✅ Lesson plans work correctly

**Output:** JSON report with all issues found

### Option 2: Run Basic Test Suite
```bash
python3 test_website.py
```

**This tests:**
- ✅ Homepage loads
- ✅ Student/Teacher/Parent signup
- ✅ Login flows
- ✅ Basic dashboards

---

## DETAILED TESTING GUIDE

### 1. Test Locally

```bash
# Start your local server first
python3 main.py

# In another terminal, run tests
python3 test_complete_workflow.py
```

### 2. Test Production

Edit `test_complete_workflow.py` line 9:
```python
BASE_URL = "https://cozmiclearning-1.onrender.com"
```

Then run:
```bash
python3 test_complete_workflow.py
```

---

## WHAT GETS TESTED

### ✅ User Authentication (All 3 Types)
- Student signup/login
- Teacher signup/login
- Parent signup/login (Basic & Homeschool plans)

### ✅ Teacher → Student Workflow
- Teacher creates class
- Teacher assigns practice to students
- Students receive assignments
- Students complete work
- Teacher views analytics and progress

### ✅ All 12 Subject Planets
1. NumForge (Math)
2. AtomSphere (Science)
3. ChronoCore (History)
4. StoryVerse (Reading)
5. InkHaven (Writing)
6. FaithRealm (Bible)
7. CoinQuest (Money)
8. StockStar (Investing)
9. TerraNova (General Knowledge)
10. PowerGrid (Deep Study)
11. TruthForge (Apologetics)
12. **RespectRealm (Life Skills) - 44 lessons across 10 categories**

### ✅ RespectRealm Specific Tests
- Landing page loads
- All 10 categories visible
- 44 lessons accessible
- Rocky-style motivational tone
- Follow-up chat works

### ✅ Practice & Analytics
- Practice mode generates questions
- Student progress tracked
- Analytics display correctly
- XP and mastery calculated

### ✅ Parent Features
- Parent dashboard loads
- Progress reports visible
- Weekly summaries available
- Can view student work

### ✅ Homeschool Features
- Lesson plan library accessible
- Can create lesson plans
- Back button navigation works
- Export/print functionality

---

## READING THE TEST RESULTS

### Success Output
```
✅ Teacher Signup: Created teacher account
✅ Class Creation: Teacher created class successfully
✅ Subject Load: RespectRealm (Life Skills) accessible
```

### Issue Output
```
❌ [HIGH] Assignment Creation
   Failed to create assignment
   Details: Status: 500
```

### Severity Levels
- **CRITICAL** = Core functionality broken (can't login, homepage down)
- **HIGH** = Major feature broken (can't assign work, subjects don't load)
- **MEDIUM** = Minor feature issue (analytics missing data)
- **LOW** = Cosmetic issue (button text wrong)

---

## MANUAL TESTING CHECKLIST

If you want to manually verify specific features:

### Test RespectRealm (5 min)
1. Login as student
2. Go to Subjects → Click RespectRealm icon
3. Select "Physical Discipline & Fitness"
4. Click "Building an Exercise Habit"
5. **Verify:** Rocky-style tone ("Here's the truth...", "Listen up...")
6. **Verify:** 6 sections present (Overview, Key Facts, Christian View, Agreement, Difference, Practice)
7. **Verify:** Practice section ends with "You've got what it takes. Now GO PROVE IT."
8. Test follow-up chat

### Test Teacher → Student Flow (10 min)
1. Login as teacher
2. Create a class
3. Add students to class
4. Assign practice (NumForge - Algebra)
5. Logout
6. Login as student
7. **Verify:** Assignment visible in dashboard
8. Complete assignment
9. Logout, login as teacher
10. **Verify:** Analytics show student completion

### Test Parent Reports (5 min)
1. Login as parent
2. Go to dashboard
3. **Verify:** Student list shows
4. **Verify:** Weekly progress visible
5. **Verify:** Analytics charts load
6. Go to Lesson Plans
7. **Verify:** "Back to Dashboard" goes to correct place

### Test Admin Mode (3 min)
1. Login as owner
2. Go to Admin Mode
3. **Verify:** Sidebar only shows Quick Switch buttons
4. **Verify:** No extra navigation clutter
5. Switch to Student view
6. Test a subject
7. Switch back to Admin

---

## TROUBLESHOOTING

### Test Script Fails to Run
```bash
# Install dependencies
pip install requests

# Check Python version (need 3.7+)
python3 --version
```

### "Cannot reach website" Error
- Make sure your server is running
- Check the BASE_URL is correct
- Try accessing homepage in browser first

### Tests Pass But Feature Doesn't Work
- Test script may have false positive
- Do manual testing to confirm
- Check browser console for JavaScript errors
- Check server logs for backend errors

### RespectRealm Tests Fail
- Verify lessons exist in manners_helper.py
- Check AI prompt is correct
- Test lesson manually in browser
- Check for JavaScript console errors

---

## AFTER TESTING

### If All Tests Pass ✅
1. Review JSON report
2. Do spot-check manual testing
3. Test on different browsers
4. Deploy with confidence

### If Tests Fail ❌
1. Review JSON report for issues
2. Fix critical issues first
3. Rerun tests
4. Fix high-priority issues
5. Rerun tests again
6. Document any medium/low issues for later

---

## QUICK REFERENCE

**Run full test:** `python3 test_complete_workflow.py`
**Run basic test:** `python3 test_website.py`
**Test locally:** Edit BASE_URL to `http://localhost:5000`
**Test production:** Edit BASE_URL to `https://cozmiclearning-1.onrender.com`

**Reports saved to:** `workflow_test_report_TIMESTAMP.json`

---

Last Updated: December 14, 2024
