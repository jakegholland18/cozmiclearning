# CozmicLearning Website Testing Checklist

Generated: 2025-12-05

## Test Accounts to Create

### Students
- [ ] `teststudent1@cozmictest.com` / Password: `TestPass123!`
- [ ] `teststudent2@cozmictest.com` / Password: `TestPass123!`
- [ ] `teststudent3@cozmictest.com` / Password: `TestPass123!`

### Teachers
- [ ] `testteacher@cozmictest.com` / Password: `TeacherPass123!`

### Parents (Basic Plan)
- [ ] `testparent@cozmictest.com` / Password: `ParentPass123!`

### Homeschool Parents (Homeschool Essential Plan)
- [ ] `homeschool@cozmictest.com` / Password: `HomeschoolPass123!`

---

## 1. STUDENT ACCOUNT TESTING

### Signup & Login
- [ ] Can create new student account
- [ ] Receives appropriate welcome/confirmation
- [ ] Can logout
- [ ] Can login again with credentials
- [ ] Password validation works (rejects weak passwords)
- [ ] Email validation works (rejects invalid emails)

### Student Dashboard
- [ ] Dashboard loads without errors
- [ ] Can see list of available subjects
- [ ] Navigation menu works
- [ ] Profile/settings accessible
- [ ] Visual design is consistent and appealing

### Practice Sessions
- [ ] Can start a practice session
- [ ] AI generates appropriate questions for grade level
- [ ] Multiple choice questions display correctly
- [ ] Can submit answers
- [ ] Receives immediate feedback
- [ ] Explanation shows after answering
- [ ] Can navigate between questions
- [ ] Session completion shows results
- [ ] Score is calculated correctly
- [ ] Can start new session after finishing

### Assignments
- [ ] Can see assigned homework/missions
- [ ] Can click into assignment
- [ ] Assignment questions display correctly
- [ ] Can answer all question types (MC, short answer, etc.)
- [ ] Can save progress (if feature exists)
- [ ] Can submit assignment
- [ ] Submission confirmation appears
- [ ] Cannot edit after submission

### Class Joining
- [ ] Can join a class with join code
- [ ] Join code validation works (rejects invalid codes)
- [ ] Sees class name after joining
- [ ] Can see assignments from that class

---

## 2. TEACHER ACCOUNT TESTING

### Signup & Login
- [ ] Can create new teacher account
- [ ] Email verification works (if applicable)
- [ ] Can logout
- [ ] Can login again
- [ ] Password reset flow works (if exists)

### Teacher Dashboard
- [ ] Dashboard loads without errors
- [ ] Stats display correctly (classes, students, assignments)
- [ ] Layout is compact and horizontal (recent changes)
- [ ] All cards visible and readable
- [ ] Responsive design works on smaller screens

### Class Management
- [ ] Can create a new class
- [ ] Class appears in class list
- [ ] Join code is generated and displayed
- [ ] Can view class details
- [ ] Can see students enrolled in class
- [ ] Can edit class name/details
- [ ] Can delete/archive class (if feature exists)

### Assignment Creation (AI-Generated)
- [ ] Can click "Create Assignment"
- [ ] Assignment creation form appears
- [ ] Can select subject, topic, grade level
- [ ] Can set due date
- [ ] Can choose number of questions
- [ ] Can preview AI-generated questions
- [ ] Questions are grade-appropriate
- [ ] Questions are relevant to topic
- [ ] Can regenerate individual questions
- [ ] Can regenerate all questions
- [ ] Can edit questions manually
- [ ] Can add/delete questions
- [ ] Can reorder questions (drag and drop)
- [ ] Can publish assignment to class
- [ ] Published assignment appears in class

### Assignment Creation (Manual)
- [ ] Can add manual question
- [ ] Multiple choice question creation works
- [ ] Short answer question creation works
- [ ] Can set correct answer
- [ ] Can add explanation
- [ ] Question saves correctly

### Viewing Submissions
- [ ] Can click "View Submissions" on assignment
- [ ] Sees list of all students in class
- [ ] Sees submission status for each student
- [ ] Can see who submitted vs. not started
- [ ] Timestamps display correctly

### Grading Submissions
- [ ] Can click to grade individual submission
- [ ] Student's answers display clearly
- [ ] Correct answers shown for reference
- [ ] Can enter score (0-100%)
- [ ] Can enter points earned/possible
- [ ] Can add feedback
- [ ] Grade saves correctly
- [ ] Student can see grade after saving

### Lesson Plan Generation
- [ ] Can access lesson plan generator
- [ ] Can enter subject, topic, grade
- [ ] AI generates comprehensive lesson plan
- [ ] Lesson plan has all 6 sections
- [ ] Can preview lesson plan
- [ ] Can edit lesson plan sections
- [ ] Can save lesson plan
- [ ] Can export lesson plan (PDF/print if exists)
- [ ] Saved lesson plans appear in library
- [ ] Can view previously saved lesson plans

### Lesson Plan Library
- [ ] Can access lesson plan library
- [ ] All saved lesson plans appear
- [ ] Can search/filter plans (if feature exists)
- [ ] Can click to view plan details
- [ ] Can delete old plans

---

## 3. PARENT ACCOUNT TESTING (Basic Plan)

### Signup & Login
- [ ] Can create parent account
- [ ] Can select "Basic" plan during signup
- [ ] Login works correctly
- [ ] Dashboard loads

### Parent Dashboard
- [ ] Can see student limit (3 students max)
- [ ] Can add student accounts (up to 3)
- [ ] Student creation form works
- [ ] Students appear in parent dashboard
- [ ] Can view each student's progress
- [ ] Can see student's completed assignments
- [ ] Can see student's practice session history
- [ ] Cannot access teacher features (no lesson plans, no assignments)

### Plan Limits
- [ ] Shows "Basic Plan" or plan type
- [ ] Blocks adding 4th student
- [ ] Shows upgrade prompt when limit reached
- [ ] Cannot create lesson plans (button hidden or blocked)
- [ ] Cannot create assignments (button hidden or blocked)

---

## 4. HOMESCHOOL PARENT TESTING (Homeschool Essential Plan)

### Signup & Login
- [ ] Can create homeschool parent account
- [ ] Can select "Homeschool Essential" plan
- [ ] Login redirects to appropriate dashboard

### Dashboard Access
- [ ] Can access parent dashboard
- [ ] Can access teacher dashboard/features
- [ ] Both dashboards show appropriate data
- [ ] No confusion about which mode is active

### Teacher Features (as Homeschool Parent)
- [ ] Can create classes
- [ ] Can create assignments
- [ ] Can generate lesson plans
- [ ] Lesson plan limit enforced (50/month)
- [ ] Assignment limit enforced (100/month)
- [ ] Cannot create unlimited content (blocks at limit)

### Parent Features (as Homeschool Parent)
- [ ] Can add up to 5 students
- [ ] Can track all students' progress
- [ ] Can see all student submissions
- [ ] 6th student blocked with upgrade prompt

### Navigation
- [ ] Clear way to switch between parent/teacher views
- [ ] Doesn't get stuck in wrong dashboard
- [ ] Lesson plan creation doesn't redirect to wrong place
- [ ] "Teacher" links work correctly

---

## 5. ADMIN MODE TESTING

### Admin Authentication
- [ ] Can enable admin mode with correct password
- [ ] Admin bypass toggle works
- [ ] Sidebar shows admin options
- [ ] Can access all account types without logging out

### Admin Dashboard Access
- [ ] Can view teacher dashboard in admin mode
- [ ] Can create lesson plans in admin mode
- [ ] Admin actions use demo teacher account
- [ ] Doesn't redirect to login incorrectly

### Admin Features
- [ ] Can view all users
- [ ] Can view system stats
- [ ] Moderation panel accessible
- [ ] Can view flagged content
- [ ] All admin routes work without errors

---

## 6. CROSS-CUTTING CONCERNS

### Navigation & UX
- [ ] All navigation links work
- [ ] Breadcrumbs accurate (if present)
- [ ] Back buttons go to correct pages
- [ ] No broken links
- [ ] Logout works from all pages

### Forms & Validation
- [ ] All forms have proper validation
- [ ] Error messages are clear and helpful
- [ ] Success messages appear
- [ ] Required fields marked clearly
- [ ] Can't submit empty forms

### Security
- [ ] Can't access student data without login
- [ ] Can't access teacher data without login
- [ ] Can't access other users' data
- [ ] Session expires appropriately
- [ ] SQL injection attempts fail safely

### Performance
- [ ] Pages load within reasonable time (<3 seconds)
- [ ] AI generation completes within expected time (15-30s)
- [ ] No infinite loading states
- [ ] Loading indicators show during AI generation

### Visual Design
- [ ] Color scheme consistent across pages
- [ ] Text readable on all backgrounds
- [ ] Buttons clearly clickable
- [ ] Forms well-organized
- [ ] Mobile responsive (test on phone/tablet)

### Error Handling
- [ ] 404 pages show friendly error
- [ ] 500 errors don't expose sensitive info
- [ ] Database errors handled gracefully
- [ ] Network errors show user-friendly message

---

## COMMON ISSUES TO CHECK

### Routing Issues
- [ ] Homeschool parents not redirected incorrectly when creating lessons
- [ ] Admin mode doesn't redirect to login
- [ ] Parent lesson plan links don't go to teacher login
- [ ] Join code links work correctly

### Database Issues
- [ ] Join codes exist for all classes
- [ ] No missing foreign keys
- [ ] Submissions save correctly
- [ ] Grades persist after saving

### AI Generation Issues
- [ ] Questions appropriate for grade level
- [ ] Questions match the topic requested
- [ ] No inappropriate content generated
- [ ] Explanations are helpful and accurate
- [ ] Lesson plans are comprehensive

### UI Issues
- [ ] No overlapping text
- [ ] All buttons visible and clickable
- [ ] Modals close properly
- [ ] Forms don't cut off on small screens
- [ ] Images load correctly

---

## PRIORITY ISSUES TO FIX

Based on recent work, these should be tested thoroughly:

1. **Homeschool lesson plan creation** - ensure it doesn't redirect to wrong dashboard
2. **Admin mode authentication** - verify it works without redirecting to login
3. **Teacher dashboard layout** - confirm horizontal stacking works on all screen sizes
4. **Join code generation** - verify all classes have codes
5. **Assignment preview/publish flow** - ensure it works end-to-end

---

## REPORT TEMPLATE

After testing, document findings:

### Critical Issues (Must Fix)
- Issue description
- Steps to reproduce
- Expected behavior
- Actual behavior

### High Priority Issues (Should Fix Soon)
- Issue description
- Impact on users
- Suggested fix

### Medium Priority Issues (Nice to Have)
- Issue description
- UX improvement

### Low Priority Issues (Future Enhancement)
- Enhancement ideas
- Feature requests

### Successful Features (Working Well)
- Features that work great
- Good UX elements to keep
