# How Students Receive Assignments - Complete Flow

## Overview
Students automatically see assignments in their student portal once the teacher publishes them. The system uses **class-based assignment distribution** where assignments are linked to classes, and all students in that class can access them.

---

## The Complete Flow

### 1️⃣ Teacher Creates Assignment

**Using the New Wizard:**
```
Teacher → 🚀 Create Wizard → Choose Type → Configure Settings → Review → Click "Create"
```

**What Happens:**
- Assignment is created with `is_published = False` (draft mode)
- Assignment is linked to a specific **class** via `class_id`
- AI generates questions automatically
- Questions stored in `preview_json` field
- Teacher can preview/edit before publishing

**Key Database Fields:**
```python
AssignedPractice(
    teacher_id=5,           # Teacher who created it
    class_id=12,            # Which class gets this assignment
    title="Fractions Quiz",
    subject="num_forge",
    is_published=False,     # NOT visible to students yet
    preview_json="{...}"    # Generated questions
)
```

---

### 2️⃣ Teacher Publishes Assignment

**How to Publish:**
1. Teacher creates assignment via wizard (or traditional method)
2. Reviews questions on preview page
3. Clicks **"Publish to Students"** button
4. Route: `/teacher/assignments/<id>/publish`

**What Changes:**
```python
# Before publish
is_published = False  # Students can't see it

# After publish
is_published = True   # ✅ Students can now see it!
```

**Publish Validation:**
- ✅ Must have `preview_json` (questions exist)
- ✅ Only creator can publish
- ✅ Flash message confirms success

**Code Reference:**
```python
# app.py line 8214
@app.route("/teacher/assignments/<int:assignment_id>/publish")
def assignment_publish(assignment_id):
    # Verify questions exist
    if not assignment.preview_json:
        flash("You must preview this mission before publishing.", "error")
        return redirect(...)

    # Publish it!
    assignment.is_published = True
    db.session.commit()

    flash("Mission published successfully!", "success")
```

---

### 3️⃣ Student Sees Assignment in Their Portal

**Automatic Display:**
Once published, the assignment **automatically appears** on the student's assignments page.

**Student Access Route:**
```
Student Login → Dashboard → "Missions" or "/student/assignments"
```

**How It Works:**
```python
# app.py line 6325-6330
# Get all PUBLISHED assignments for this student's class
assignments = (
    AssignedPractice.query
    .filter_by(class_id=student.class_id, is_published=True)
    .order_by(AssignedPractice.created_at.desc())
    .all()
)
```

**Query Breakdown:**
- `class_id=student.class_id` → Only assignments for student's class
- `is_published=True` → Only published assignments
- Ordered by newest first

---

### 4️⃣ Student Views Available Assignments

**What Students See:**

```
┌─────────────────────────────────────────┐
│ 📝 My Assignments                       │
├─────────────────────────────────────────┤
│                                         │
│ 🎯 Fractions Quiz                       │
│ Math • 10 questions                     │
│ Due: Dec 25, 2025                       │
│ [Start Mission] or [Continue]          │
│                                         │
│ ✅ Photosynthesis                       │
│ Science • Completed (92%)               │
│ [View Results]                          │
│                                         │
│ 📚 Reading Comprehension                │
│ Reading • In Progress (5/10)            │
│ [Continue Assignment]                   │
│                                         │
└─────────────────────────────────────────┘
```

**Assignment Statuses:**
- **Not Started**: "Start Mission" button
- **In Progress**: "Continue Assignment" button
- **Completed**: "View Results" button

---

### 5️⃣ Student Starts Assignment

**Click Flow:**
```
Student clicks "Start Mission" → Route: /student/assignments/<id>/start
```

**What Happens:**
1. System verifies student is in correct class
2. System checks assignment is published
3. System checks open/due dates
4. Creates `StudentSubmission` record if first time
5. Loads questions from `preview_json`
6. Displays first question

**Security Checks:**
```python
# app.py line 6488-6494
# Must be published
if not assignment.is_published:
    flash("This assignment is not yet available.", "error")
    return redirect("/student/assignments")

# Must be in same class
if assignment.class_id != student.class_id:
    flash("You don't have access to this assignment.", "error")
    return redirect("/student/assignments")
```

---

## Class-Based Distribution System

### How Classes Work

**Teacher Creates Class:**
```
Teacher Dashboard → "Add Class" → Name: "5th Grade Math" → Add Students
```

**Database Structure:**
```
Class Table
├── id: 12
├── class_name: "5th Grade Math"
├── grade_level: "5"
└── teacher_id: 5

Student Table
├── id: 42
├── first_name: "Sarah"
├── last_name: "Johnson"
└── class_id: 12  ← Links student to class

AssignedPractice Table
├── id: 100
├── title: "Fractions Quiz"
├── teacher_id: 5
└── class_id: 12  ← Links assignment to class
```

**The Magic:**
When assignment is published with `class_id=12`, **ALL students with `class_id=12` see it automatically!**

---

## Assignment Visibility Rules

### ✅ Student CAN See Assignment When:
1. `is_published = True` ✅
2. `assignment.class_id = student.class_id` ✅
3. Assignment is within open/due dates (if set) ✅
4. Assignment hasn't been deleted ✅

### ❌ Student CANNOT See Assignment When:
1. `is_published = False` (draft mode)
2. Student is in different class
3. Assignment is before open date
4. Assignment is past due date (may vary by settings)

---

## Timeline Example

Let's follow an assignment from creation to completion:

### Monday 9:00 AM - Teacher Creates
```
Teacher uses wizard → Creates "Fractions Quiz" for Class 12
Status: is_published = False (DRAFT)
Students see: Nothing yet
```

### Monday 9:15 AM - Teacher Reviews
```
Teacher clicks Preview → Reviews 10 AI-generated questions
Teacher clicks "Edit" → Adjusts question #7
Status: Still draft
Students see: Nothing yet
```

### Monday 9:30 AM - Teacher Publishes
```
Teacher clicks "Publish to Students"
Status: is_published = True ✅
Students see: Assignment appears in their list!
```

### Monday 10:00 AM - Sarah Starts
```
Sarah (class_id=12) logs in
Sees "Fractions Quiz" in her assignments
Clicks "Start Mission"
StudentSubmission record created
Begins answering questions
```

### Monday 10:25 AM - Sarah Completes
```
Sarah finishes last question
Submission marked as complete
Status: Completed (score: 85%)
Teacher sees in Live Dashboard ✅
```

---

## How Different Creation Methods Work

### Method 1: Assignment Wizard (NEW ✨)
```
🚀 Create Wizard → Configure → AI Generates → Preview → Publish
```
- **Default**: `is_published = False`
- **Questions**: Auto-generated by AI
- **Preview Required**: Yes, before publishing

### Method 2: Templates Library (NEW ✨)
```
📚 Templates → Select Template → Customize → Publish
```
- **Default**: `is_published = False`
- **Questions**: Pre-built from template
- **Preview Required**: Optional (questions already validated)

### Method 3: Traditional Creation
```
Assignments → Create → Add Details → Generate Questions → Publish
```
- **Default**: `is_published = False`
- **Questions**: AI-generated or manual
- **Preview Required**: Yes

**All methods end the same way**: Teacher must click "Publish" to make it visible to students!

---

## Live Dashboard Integration

Once assignments are published and students start working:

### Teacher Sees Real-Time:
```
📡 Live Dashboard
├── Sarah Johnson - Working Now 🔥
│   └── Fractions Quiz: 7/10 (70%)
├── Mike Chen - Completed ✅
│   └── Fractions Quiz: 10/10 (100%)
└── Emma Davis - Needs Help ⚠️
    └── Fractions Quiz: 3/10 (30% accuracy)
```

**Auto-Refresh**: Updates every 10 seconds
**Actions**: Send encouragement, view work, grade

---

## API Flow Diagram

```
┌──────────────┐
│   Teacher    │
│  Dashboard   │
└──────┬───────┘
       │
       ├─→ Creates Assignment (is_published=False)
       │   POST /teacher/assignments/wizard/create
       │
       ├─→ Reviews Preview
       │   GET /teacher/assignments/<id>/preview
       │
       └─→ Publishes (is_published=True)
           GET /teacher/assignments/<id>/publish

┌──────────────────────────────────────────┐
│         Database Change                  │
│  AssignedPractice.is_published = True    │
└──────────────┬───────────────────────────┘
               │
               ▼
    ┌──────────────────────┐
    │   ALL Students in    │
    │   that Class can     │
    │   now see it!        │
    └──────────┬───────────┘
               │
               ▼
┌──────────────────────────┐
│  Student Portal          │
│  /student/assignments    │
└──────────┬───────────────┘
           │
           ├─→ Student Clicks "Start"
           │   GET /student/assignments/<id>/start
           │
           ├─→ Creates StudentSubmission
           │
           └─→ Student Answers Questions
               POST /student/assignments/<id>/answer
```

---

## Key Database Tables

### AssignedPractice
```sql
id              INT PRIMARY KEY
teacher_id      INT → Who created it
class_id        INT → Which class gets it
title           VARCHAR
subject         VARCHAR
is_published    BOOLEAN ← KEY FIELD!
preview_json    TEXT (stores questions)
open_date       DATETIME
due_date        DATETIME
```

### Student
```sql
id              INT PRIMARY KEY
first_name      VARCHAR
last_name       VARCHAR
class_id        INT → Which class they're in
```

### StudentSubmission
```sql
id              INT PRIMARY KEY
student_id      INT → Who's doing it
assignment_id   INT → Which assignment
answers         TEXT (JSON of responses)
is_complete     BOOLEAN
score           FLOAT
started_at      DATETIME
completed_at    DATETIME
```

---

## Common Questions

### Q: Do I need to invite students to each assignment?
**A:** No! Once you publish an assignment to a class, ALL students in that class see it automatically.

### Q: Can I control when students see it?
**A:** Yes! Use `open_date` and `due_date` fields. Assignment only appears between those dates.

### Q: Can students from other classes see the assignment?
**A:** No. Students ONLY see assignments where `assignment.class_id = student.class_id`.

### Q: What if I publish by accident?
**A:** You can "unpublish" by setting `is_published = False` (would need to add this feature).

### Q: How do students know there's a new assignment?
**A:** Currently, they see it when they login. Future: Add email/push notifications (Priority 2, Feature 4).

---

## Next Steps for Enhanced Student Access

### Recommended Additions:

1. **Email Notifications** (Priority 2, Feature 4)
   - Send email when assignment is published
   - Reminder emails before due date
   - Parent CC option

2. **Push Notifications**
   - Browser notifications
   - Mobile app notifications

3. **Assignment Calendar**
   - Students see upcoming assignments
   - Due date reminders

4. **Unpublish Feature**
   - Teacher can hide published assignment temporarily
   - Useful for fixing issues

5. **Scheduled Publishing**
   - Set assignment to auto-publish at specific time
   - Set auto-close after due date

---

## Summary

**The Flow is Simple:**

1. **Teacher Creates** → Assignment is **DRAFT** (`is_published=False`)
2. **Teacher Publishes** → Assignment becomes **VISIBLE** (`is_published=True`)
3. **Students See It** → Automatically in `/student/assignments` for their class
4. **Students Start** → Click "Start Mission" to begin
5. **Teacher Monitors** → Live Dashboard shows real-time progress

**Key Principle**: Class-based distribution means you assign to a **class**, not individual students. All students in that class automatically receive it when published!

---

**Questions? Check these routes:**
- Student assignments list: `/student/assignments` (line 6325)
- Assignment publish: `/teacher/assignments/<id>/publish` (line 8214)
- Student start assignment: `/student/assignments/<id>/start` (line 6486)
- Live dashboard API: `/teacher/api/live-progress` (line 5546)
