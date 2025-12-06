# Known Issues and Recent Fixes

Last Updated: 2025-12-05

## ✅ RECENTLY FIXED

### Fixed Today (2025-12-05)

#### 1. Homeschool Lesson Plan Generation API Error ⚡ CRITICAL FIX
**Issue**: Homeschool lesson plan generation failing with error: "Could not resolve authentication method. Expected either api_key or auth_token to be set"
**Root Cause**: `lesson_plan_generator.py` was using `anthropic.Anthropic()` but production only has `OPENAI_API_KEY` configured, not `ANTHROPIC_API_KEY`
**Fix**:
- Switched to use `get_client()` from `shared_ai` module (uses OpenAI)
- Changed from Claude Messages API to OpenAI Chat Completions API
- Updated model from `claude-3-5-sonnet` to `gpt-4o`
**Files**: `modules/lesson_plan_generator.py`
**Status**: ✅ Fixed and deployed
**Test**: Login as homeschool parent → Generate lesson plan → Should work now

#### 2. Admin Mode Authentication Fixed
**Issue**: Admin mode was redirecting to /teacher/login when accessing teacher features
**Fix**: Reordered authentication checks to verify admin status BEFORE checking parent accounts
**Files**: `app.py` lines 4530-4558, 4609-4637
**Routes Affected**:
- `/teacher/generate_lesson_plan`
- `/teacher/lesson_plans`
**Status**: ✅ Fixed and deployed

#### 3. SQLAlchemy 2.x Compatibility
**Issue**: `TypeError: Function.__init__() got an unexpected keyword argument 'else_'`
**Fix**: Changed from `func.case()` to importing `case` directly from sqlalchemy
**Files**: `app.py` line 1989
**Status**: ✅ Fixed and deployed

#### 4. Join Code Migration
**Issue**: Production database missing `join_code` column, causing crashes
**Fix**: Added automatic migration to app startup
**Files**: `app.py` lines 346-380
**Status**: ✅ Fixed and deployed

### Fixed Yesterday (2025-12-04)

#### 5. Teacher Dashboard Compacting
**Issue**: Dashboard had too much padding/whitespace, wasn't space-efficient
**Fix**: Reduced padding, margins, and font sizes across dashboard elements
**Files**: `teacher_dashboard.html` lines 537-638
**Status**: ✅ Fixed and deployed

#### 6. Teacher Dashboard Horizontal Layout
**Issue**: Dashboard was single-column, wasting horizontal space
**Fix**: Changed to 2-column grid layout with responsive breakpoint
**Files**: `teacher_dashboard.html` lines 160-175
**Status**: ✅ Fixed and deployed

---

## ⚠️ POTENTIAL ISSUES TO TEST

### High Priority

#### 1. Assignment Preview/Publish Flow
**Potential Issue**: After generating AI questions, preview page might have issues
**Test Cases**:
- Generate questions
- Preview loads correctly
- Can edit questions
- Publish works
- Published assignment visible to students
**Status**: ⚠️ Needs systematic testing

#### 2. Mobile Responsiveness of New Layout
**Potential Issue**: New horizontal 2-column layout might not work well on mobile
**Test Cases**:
- View teacher dashboard on phone
- Check if cards stack vertically below 1024px
- Verify all content is readable
- Check if forms are usable
**Status**: ⚠️ Needs testing on mobile devices

### Medium Priority

#### 3. Parent Account Routing Edge Cases
**Potential Issue**: Parent accounts switching between views might have edge cases
**Test Cases**:
- Parent with multiple students
- Parent trying to access teacher routes
- Parent plan limits enforcement
**Status**: ⚠️ Needs comprehensive testing

---

## 🔍 AREAS THAT NEED SYSTEMATIC TESTING

### Not Yet Tested Since Recent Changes

1. **Student Assignment Submission Flow**
   - [ ] Student can see published assignments
   - [ ] Student can complete assignments
   - [ ] Submission saves correctly
   - [ ] Teacher can grade submissions

2. **Class Join Code System**
   - [ ] All new classes get join codes
   - [ ] Students can join with code
   - [ ] Invalid codes rejected
   - [ ] Students see class after joining

3. **AI Question Generation Quality**
   - [ ] Questions match requested topic
   - [ ] Questions appropriate for grade level
   - [ ] Regeneration works
   - [ ] Explanations are helpful

4. **Parent Plan Limits**
   - [ ] Basic plan limited to 3 students
   - [ ] Homeschool Essential limited to 5 students
   - [ ] Lesson plan limits enforced
   - [ ] Assignment limits enforced

5. **Admin Mode Functionality**
   - [ ] Can access all views
   - [ ] Demo teacher account created
   - [ ] Actions don't interfere with real users
   - [ ] Can view moderation panel

---

## 🎯 RECOMMENDED TESTING ORDER

### Phase 1: Critical Path Testing (30 min)
Test the most important user flows:
1. Student signup → Join class → Complete assignment
2. Teacher signup → Create class → Create AI assignment → Grade submission
3. Homeschool signup → Create lesson plan (test the fix)
4. Admin mode → Access teacher features (test the fix)

### Phase 2: Feature Testing (1-2 hours)
Test each major feature:
1. All student features (practice, assignments, dashboard)
2. All teacher features (classes, assignments, grading, lesson plans)
3. All parent features (student management, progress tracking)
4. All homeschool features (hybrid parent + teacher)

### Phase 3: Edge Case Testing (1-2 hours)
Test unusual scenarios:
1. Empty states (no classes, no students, no assignments)
2. Limits (plan limits, character limits, validation)
3. Error handling (bad input, network errors, timeouts)
4. Security (accessing other users' data, SQL injection attempts)

---

## 📝 TESTING NOTES

### What We Know Works Well
- Basic authentication (login/logout/signup)
- Student practice sessions
- Teacher dashboard layout (after recent fixes)
- Class creation
- Database migrations

### What Needs More Testing
- Assignment preview → publish → student completion → grading (full flow)
- Homeschool parent account routing (reported issues today)
- Admin mode edge cases
- Mobile responsiveness
- Plan limit enforcement

### What's Never Been Tested
- High load (many concurrent users)
- Long-running sessions (memory leaks?)
- Large classes (100+ students)
- Many assignments per class (performance?)
- AI generation failures (what happens if Claude API fails?)

---

## 🚨 RED FLAGS TO WATCH FOR

During testing, immediately report if you see:

1. **Redirect Loops**: Page keeps redirecting to itself or bounces between pages
2. **500 Errors**: Server errors indicate code bugs
3. **Blank Pages**: Usually means JavaScript error or template issue
4. **Slow AI Generation**: Taking longer than 60 seconds suggests timeout issue
5. **Data Not Saving**: Forms submit but data doesn't persist
6. **Wrong User Data**: Seeing another user's classes/students/assignments
7. **Plan Limits Not Enforced**: Can exceed stated limits
8. **Authentication Bypass**: Can access pages without logging in

---

## 🔄 WHAT TO DO WHEN YOU FIND AN ISSUE

1. **Reproduce**: Can you make it happen again?
2. **Document**: Write down exact steps
3. **Check Console**: Open browser dev tools, check for errors
4. **Screenshot**: Capture what you're seeing
5. **Report**: Add to issues list with all details
6. **Workaround**: Is there a way to accomplish the task differently?

---

## 📊 TESTING PROGRESS TRACKER

### Critical Flows
- [ ] Student assignment completion (end-to-end)
- [ ] Teacher assignment creation (end-to-end)
- [ ] Homeschool lesson plan creation (recent fix)
- [ ] Admin mode teacher access (recent fix)

### Student Features
- [ ] Signup/login
- [ ] Practice sessions
- [ ] Join class
- [ ] View assignments
- [ ] Complete assignment
- [ ] View grades

### Teacher Features
- [ ] Signup/login
- [ ] Create class
- [ ] Create AI assignment
- [ ] View submissions
- [ ] Grade submissions
- [ ] Generate lesson plan
- [ ] View lesson plan library

### Parent Features
- [ ] Signup/login (Basic)
- [ ] Add students
- [ ] View student progress
- [ ] Plan limits enforced

### Homeschool Features
- [ ] Signup/login (Homeschool Essential)
- [ ] Create classes
- [ ] Create assignments
- [ ] Generate lesson plans
- [ ] View lesson plan library
- [ ] Student management
- [ ] Plan limits enforced

### Admin Features
- [ ] Enable admin mode
- [ ] Access teacher dashboard
- [ ] Create lesson plans
- [ ] View all users
- [ ] Moderation panel

---

## 💡 AUTOMATION IDEAS FOR FUTURE

### Selenium/Playwright Test Suite
Could automate:
- Login flows for all account types
- Form submissions
- Navigation testing
- Screenshot regression testing

### API Testing
Could test:
- Authentication endpoints
- Assignment creation API
- Lesson plan generation API
- Grading endpoints

### Load Testing
Could test:
- Concurrent user sessions
- AI generation under load
- Database query performance
- Memory usage over time

---

## 📞 ESCALATION

If you find a **critical** issue (site down, data loss, security vulnerability):
1. Stop testing immediately
2. Document exactly what you did
3. Note the URL and timestamp
4. Report with severity: CRITICAL
5. Don't try to reproduce if it might cause more damage
