# Quick Testing Guide for CozmicLearning

## Test Account Credentials

Use these for consistent testing:

```
STUDENTS:
- teststudent1@cozmictest.com / TestPass123!
- teststudent2@cozmictest.com / TestPass123!

TEACHER:
- testteacher@cozmictest.com / TeacherPass123!

PARENT (Basic):
- testparent@cozmictest.com / ParentPass123!

HOMESCHOOL (Essential):
- homeschool@cozmictest.com / HomeschoolPass123!
```

---

## 🚨 CRITICAL PATHS TO TEST FIRST

### Test 1: Student Assignment Flow (15 min)
**Goal**: Verify students can complete assignments end-to-end

1. Create teacher account → Login
2. Create a class (note the join code)
3. Create assignment with AI generation
   - Click "Generate & Preview AI Mission"
   - Wait for questions to generate
   - Click "Approve & Publish"
4. Logout
5. Create student account → Login
6. Join class with join code
7. Click on assignment
8. Answer all questions
9. Submit
10. ✅ **Check**: Student sees confirmation

**Expected**: Smooth flow with no redirects to wrong pages

---

### Test 2: Homeschool Lesson Plan Creation (10 min)
**Goal**: Verify homeschool parents can create lesson plans without redirect issues

1. Create homeschool parent account (plan: homeschool_essential)
2. Login → Should see dashboard
3. Navigate to lesson plan creation
4. Fill in: Subject, Topic, Grade
5. Click "Generate Lesson Plan"
6. ✅ **Check**: Should see lesson plan, NOT redirect to homeschool dashboard

**Expected**: Lesson plan generates successfully without redirect loop

---

### Test 3: Admin Mode Access (5 min)
**Goal**: Verify admin mode doesn't redirect to login

1. Enable admin mode (sidebar or admin panel)
2. Navigate to teacher dashboard
3. Try to create lesson plan
4. ✅ **Check**: Should work, not redirect to /teacher/login

**Expected**: Admin can access all features

---

### Test 4: Teacher Dashboard Layout (5 min)
**Goal**: Verify recent compact + horizontal layout changes

1. Login as teacher
2. View dashboard
3. ✅ **Check**:
   - Layout is 2-column grid (on wide screens)
   - Spacing is compact (not too much padding)
   - "Your Classes" card spans full width
   - Other cards in 2 columns

**Expected**: Matches new compact horizontal design

---

## 🔍 DETAILED FEATURE TESTING

### Student Features

#### Practice Session
URL: `https://cozmiclearning-1.onrender.com/student/dashboard`

1. Login as student
2. Click "Start Practice Session"
3. Select subject (e.g., Math)
4. Select topic
5. Answer questions
6. Check:
   - [ ] Questions appear
   - [ ] Can select answers
   - [ ] Feedback shows after answering
   - [ ] Score calculated at end
   - [ ] Can start new session

#### Assignment Completion
1. Student must be in a class with published assignment
2. Go to dashboard → Click assignment
3. Answer all questions
4. Click "Submit"
5. Check:
   - [ ] Submission confirmation
   - [ ] Cannot edit after submit
   - [ ] Assignment shows "Submitted" status

---

### Teacher Features

#### Class Creation
URL: `https://cozmiclearning-1.onrender.com/teacher/dashboard`

1. Login as teacher
2. Find "Create Class" section
3. Enter class name (e.g., "Grade 8 Math")
4. Click create
5. Check:
   - [ ] Class appears in list
   - [ ] Join code is displayed
   - [ ] Can copy join code
   - [ ] Can click to view class details

#### AI Assignment Creation
URL: `https://cozmiclearning-1.onrender.com/teacher/assignments`

1. Login as teacher
2. Navigate to assignments
3. Click "Create Assignment"
4. Fill in:
   - Class: Select a class
   - Subject: Math
   - Topic: "Solving linear equations"
   - Grade: 8
   - Number of questions: 5
5. Click "Generate & Preview AI Mission"
6. Wait 15-30 seconds
7. Check:
   - [ ] Preview page loads (not redirect)
   - [ ] 5 questions generated
   - [ ] Questions relevant to topic
   - [ ] Questions appropriate for grade 8
   - [ ] Can click "Regenerate" on individual question
   - [ ] Can edit question text
   - [ ] Can edit answer choices
   - [ ] Can edit explanations
8. Click "Publish Mission"
9. Check:
   - [ ] Assignment now shows as "Published"
   - [ ] Students in that class can see it

#### Grading Submissions
URL: `https://cozmiclearning-1.onrender.com/teacher/assignments/{id}/submissions`

1. Login as teacher
2. Go to assignment that has submissions
3. Click "View Submissions"
4. Check:
   - [ ] List shows all students in class
   - [ ] Status shows correctly (Not Started, Submitted, Graded)
   - [ ] Can click "Grade" button
5. Click "Grade" for a submitted assignment
6. Check:
   - [ ] Student's answers visible
   - [ ] Correct answers shown for reference
   - [ ] Explanations visible
   - [ ] Can enter score (0-100)
   - [ ] Can enter feedback
7. Enter score and feedback → Click "Save Grade"
8. Check:
   - [ ] Grade saves (no errors)
   - [ ] Redirects back to submissions list
   - [ ] Score now appears in list

#### Lesson Plan Generation
URL: `https://cozmiclearning-1.onrender.com/teacher/dashboard`

1. Login as teacher
2. Find "Generate Lesson Plan" section
3. Fill in:
   - Subject: Science
   - Topic: "Photosynthesis"
   - Grade: 7
4. Click "Generate Lesson Plan"
5. Wait 20-30 seconds
6. Check:
   - [ ] Lesson plan page loads
   - [ ] Contains all 6 sections:
     1. Lesson Overview
     2. Learning Objectives
     3. Materials Needed
     4. Lesson Procedure
     5. Assessment
     6. Extension Activities
   - [ ] Content is comprehensive
   - [ ] Content is grade-appropriate
   - [ ] Can save lesson plan
7. Click "Save Lesson Plan"
8. Check:
   - [ ] Saves successfully
   - [ ] Appears in lesson plan library

#### Lesson Plan Library
URL: `https://cozmiclearning-1.onrender.com/teacher/lesson_plans`

1. Login as teacher (must have created lesson plans)
2. Navigate to lesson plan library
3. Check:
   - [ ] Page loads (doesn't redirect to login)
   - [ ] All saved lesson plans appear
   - [ ] Can click to view plan
   - [ ] Plan opens with all content
   - [ ] Can edit or delete plan (if feature exists)

---

### Parent Features

#### Basic Parent Account
URL: `https://cozmiclearning-1.onrender.com/parent/dashboard`

1. Signup with plan: "basic"
2. Login
3. Check:
   - [ ] Dashboard loads
   - [ ] Shows student limit (3 students)
   - [ ] Can add student account
   - [ ] Student appears after creation
4. Add 3 students (reach limit)
5. Try to add 4th student
6. Check:
   - [ ] Blocked with message
   - [ ] Shows upgrade prompt

#### Parent Viewing Student Progress
1. Login as parent (with students added)
2. One of the students must have completed assignments/practice
3. Click on student to view progress
4. Check:
   - [ ] Can see student's assignments
   - [ ] Can see scores
   - [ ] Can see practice session history
   - [ ] Cannot edit student work

---

### Homeschool Parent Features

#### Homeschool Account Setup
URL: `https://cozmiclearning-1.onrender.com/parent/signup`

1. Signup with plan: "homeschool_essential"
2. Login
3. Check:
   - [ ] Dashboard loads
   - [ ] Can see both parent AND teacher features
   - [ ] Shows student limit (5 students)
   - [ ] Shows lesson plan limit (50/month)
   - [ ] Shows assignment limit (100/month)

#### Homeschool Creating Classes
1. Login as homeschool parent
2. Navigate to teacher section/classes
3. Create a class
4. Check:
   - [ ] Class creation works
   - [ ] Can see class in list
   - [ ] Join code generated

#### Homeschool Creating Assignments
1. Login as homeschool parent
2. Navigate to assignments
3. Create assignment (same as teacher flow)
4. Check:
   - [ ] Assignment creation works
   - [ ] Can generate AI questions
   - [ ] Can publish to class
   - [ ] Counts toward monthly limit (100)

#### Homeschool Lesson Plans
URL: `https://cozmiclearning-1.onrender.com/teacher/lesson_plans` OR homeschool-specific route

1. Login as homeschool parent
2. Click to create lesson plan
3. Generate lesson plan
4. Check:
   - [ ] ⚠️ CRITICAL: Should NOT redirect to homeschool dashboard
   - [ ] Lesson plan generates successfully
   - [ ] Can save lesson plan
   - [ ] Counts toward monthly limit (50)
5. Navigate to lesson plan library
6. Check:
   - [ ] ⚠️ CRITICAL: Should NOT redirect to /teacher/login
   - [ ] Shows all saved lesson plans
   - [ ] Can view/edit plans

---

## 🔧 ADMIN MODE TESTING

### Enabling Admin Mode
1. Logout of all accounts
2. Access admin panel (URL or sidebar)
3. Enter admin password
4. Enable admin mode
5. Check:
   - [ ] Admin sidebar appears
   - [ ] Can access admin dashboard

### Admin Accessing Teacher Features
1. Enable admin mode
2. Navigate to teacher dashboard
3. Check:
   - [ ] ⚠️ CRITICAL: Should NOT redirect to /teacher/login
   - [ ] Dashboard loads with demo teacher account
   - [ ] Shows "Admin Mode" indicator somewhere
4. Try to create lesson plan
5. Check:
   - [ ] ⚠️ CRITICAL: Should NOT redirect
   - [ ] Lesson plan generation works
   - [ ] Saves under demo teacher account

### Admin Accessing All Account Types
1. Enable admin mode
2. Navigate between:
   - Student view
   - Teacher view
   - Parent view
3. Check:
   - [ ] Can switch between views
   - [ ] No authentication errors
   - [ ] Can perform actions in each view

---

## 📊 EXPECTED RESULTS SUMMARY

### What Should Work (Recent Fixes)
✅ Admin mode accessing teacher features (fixed today)
✅ Teacher dashboard horizontal layout (fixed yesterday)
✅ Join codes for all classes (migration added)
✅ SQLAlchemy 2.x compatibility (fixed today)

### What to Watch For (Potential Issues)
⚠️ Homeschool lesson plan creation redirecting
⚠️ Admin mode redirect loops
⚠️ Parent account routing confusion
⚠️ Assignment preview/publish flow
⚠️ Mobile responsiveness of new layout

---

## 🐛 HOW TO REPORT ISSUES

When you find a bug, document:

1. **URL**: Exact page where issue occurred
2. **Account Type**: Student/Teacher/Parent/Homeschool/Admin
3. **Steps**: Numbered steps to reproduce
4. **Expected**: What should happen
5. **Actual**: What actually happened
6. **Screenshots**: If applicable
7. **Browser**: Chrome/Safari/Firefox/etc.

Example:
```
URL: https://cozmiclearning-1.onrender.com/teacher/lesson_plans
Account: homeschool@cozmictest.com (Homeschool Essential)
Steps:
  1. Login as homeschool parent
  2. Click "Lesson Plan Library" link
  3. Page loads
Expected: Should show list of saved lesson plans
Actual: Redirects to /teacher/login
Browser: Chrome 120
```

---

## 📈 TESTING PRIORITIES

**Priority 1 (Test First):**
- Homeschool lesson plan flow
- Admin mode authentication
- Student assignment submission
- Teacher grading flow

**Priority 2 (Test Next):**
- Class creation and join codes
- AI question generation quality
- Parent dashboard functionality
- Mobile responsiveness

**Priority 3 (Test If Time):**
- Password reset
- Profile editing
- Analytics/stats
- Edge cases (empty states, errors)
