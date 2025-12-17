# Analytics & Gradebook Visual Guide

## How to See Your Analytics & Gradebook

### Option 1: Generate Demo Data (Recommended)
```bash
python generate_demo_data.py
```

This will create:
- 1 demo teacher account
- 2 classes (5th Grade and 7th Grade)
- 16 students total
- 10-16 assignments with student submissions
- Realistic grade distributions

**Demo Login:**
- Email: `demo+teacher@cozmiclearning.com`
- Password: `demo123`

Then navigate to:
- **Gradebook**: `/teacher/gradebook`
- **Analytics**: `/teacher/analytics`

---

## What the Gradebook Looks Like

### 1. Gradebook Overview (`/teacher/gradebook`)

This is the first page teachers see when they click "Gradebook" in the nav menu.

**Layout:**

```
╔═══════════════════════════════════════════════════════════╗
║                    📊 Gradebook                           ║
║          Track student performance across all classes     ║
║                                                           ║
║              📥 Export All Classes to CSV                 ║
╚═══════════════════════════════════════════════════════════╝

┌───────────────────────────────────────────────────────────┐
│               📝 Grading Backlog (if ungraded)            │
├───────────────────────────────────────────────────────────┤
│  Total Ungraded: 23                                       │
│                                                           │
│  ┌─────────────┬─────────────┬──────────────┬───────────┐
│  │  Oldest     │ Avg Grading │ Critical (7+)│  Overdue  │
│  │  Jan 15     │  18 hours   │    5         │    12     │
│  └─────────────┴─────────────┴──────────────┴───────────┘
│                                                           │
│  Priority Queue (Oldest First):                          │
│  ┌─────────────────────────────────────────┬────────────┐
│  │ URGENT Emma Johnson · Fraction Addition │ Grade Now  │
│  │ 7th Grade Math · Submitted Jan 15 (7d ago)           │
│  ├─────────────────────────────────────────┼────────────┤
│  │ OVERDUE Liam Smith · Cell Biology      │ Grade Now  │
│  │ 5th Grade Science · Submitted Jan 18 (4d ago)        │
│  └─────────────────────────────────────────┴────────────┘
└───────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────┐
│  5th Grade Math & Science              👥 8 Students      │
├───────────────────────────────────────────────────────────┤
│  ┌──────────────┬──────────────┬──────────────┬─────────┐
│  │ PRACTICE     │ QUIZ         │ TEST         │ HOMEWORK│
│  │ Fractions    │ Multiplication│ Division    │ Geometry│
│  │ 6/8 graded   │ 8/8 graded   │ 5/8 graded  │4/8 graded│
│  │ 87.5%        │ 92.3%        │ 78.4%       │ 85.0%   │
│  │ 2 ungraded   │              │ 3 ungraded  │4 ungraded│
│  └──────────────┴──────────────┴──────────────┴─────────┘
│                                                           │
│  Click this card to view full class gradebook →          │
└───────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────┐
│  7th Grade English & History           👥 8 Students      │
├───────────────────────────────────────────────────────────┤
│  ┌──────────────┬──────────────┬──────────────┬─────────┐
│  │ QUIZ         │ PRACTICE     │ HOMEWORK     │ TEST    │
│  │ Grammar      │ Vocabulary   │ Essay Writing│Am. Rev. │
│  │ 7/8 graded   │ 8/8 graded   │ 6/8 graded   │5/8 graded│
│  │ 84.2%        │ 89.5%        │ 76.3%        │ 81.7%   │
│  │ 1 ungraded   │              │ 2 ungraded   │3 ungraded│
│  └──────────────┴──────────────┴──────────────┴─────────┘
└───────────────────────────────────────────────────────────┘
```

**Key Features:**
- **Grading Backlog Panel** (only shows if ungraded submissions exist)
  - Total ungraded count
  - Oldest submission date
  - Average grading time
  - Priority queue with URGENT/OVERDUE labels
  - Direct "Grade Now" buttons

- **Class Cards** (one per class)
  - Class name and student count
  - Assignment grid showing:
    * Assignment type badge (PRACTICE, QUIZ, TEST, HOMEWORK)
    * Assignment title
    * Graded count (e.g., "6/8 graded")
    * Class average for that assignment (color-coded)
    * Ungraded count badge (if any)

- **Color Coding for Averages:**
  - 🟢 Green (85%+): High performing
  - 🔵 Blue (70-84%): On-level
  - 🟡 Orange (<70%): Needs attention

- **Export Button**: Export all classes to CSV with one click

---

### 2. Class-Specific Gradebook (`/teacher/gradebook/class/{class_id}`)

When you click on a class card, you see the full gradebook table.

**Layout:**

```
╔═══════════════════════════════════════════════════════════╗
║            5th Grade Math & Science Gradebook             ║
║                  Grade 5 · 8 Students                     ║
║                                                           ║
║                 📊 Export to CSV                          ║
╚═══════════════════════════════════════════════════════════╝

┌───────────────────────────────────────────────────────────────────────────────────────┐
│ Student Name         │ Fraction   │ Multiply  │ Division │ Geometry │ Cell Bio │ Average │
│                      │ Addition   │ Mastery   │ Practice │ Quiz     │ Quiz     │         │
│                      │ PRACTICE   │ QUIZ      │ TEST     │ HOMEWORK │ QUIZ     │         │
│                      │ Due: 01/10 │ Due: 01/15│ Due: 01/20│Due: 01/25│Due: 01/30│         │
├──────────────────────┼────────────┼───────────┼──────────┼──────────┼──────────┼─────────┤
│ Emma Johnson         │    92%     │    95%    │    88%   │    90%   │    87%   │  90.4%  │
│ emma@demo.com        │   [GREEN]  │  [GREEN]  │ [GREEN]  │ [GREEN]  │ [GREEN]  │ [GREEN] │
├──────────────────────┼────────────┼───────────┼──────────┼──────────┼──────────┼─────────┤
│ Liam Smith           │    78%     │    82%    │    75%   │ Submitted│    --    │  78.3%  │
│ liam@demo.com        │   [BLUE]   │  [BLUE]   │ [BLUE]   │ [YELLOW] │   [--]   │ [BLUE]  │
├──────────────────────┼────────────┼───────────┼──────────┼──────────┼──────────┼─────────┤
│ Olivia Brown         │    65%     │    70%    │    68%   │    72%   │    69%   │  68.8%  │
│ olivia@demo.com      │  [ORANGE]  │  [BLUE]   │ [ORANGE] │ [BLUE]   │ [ORANGE] │[ORANGE] │
├──────────────────────┼────────────┼───────────┼──────────┼──────────┼──────────┼─────────┤
│ Noah Davis           │    88%     │    91%    │    --    │    85%   │    89%   │  88.3%  │
│ noah@demo.com        │   [GREEN]  │  [GREEN]  │   [--]   │ [GREEN]  │ [GREEN]  │ [GREEN] │
├──────────────────────┼────────────┼───────────┼──────────┼──────────┼──────────┼─────────┤
│ Ava Wilson           │    94%     │    98%    │    92%   │    96%   │    95%   │  95.0%  │
│ ava@demo.com         │   [GREEN]  │  [GREEN]  │ [GREEN]  │ [GREEN]  │ [GREEN]  │ [GREEN] │
├──────────────────────┼────────────┼───────────┼──────────┼──────────┼──────────┼─────────┤
│ Elijah Moore         │    82%     │    78%    │    80%   │    --    │ Submitted│  80.0%  │
│ elijah@demo.com      │   [BLUE]   │  [BLUE]   │ [BLUE]   │   [--]   │ [YELLOW] │ [BLUE]  │
├──────────────────────┼────────────┼───────────┼──────────┼──────────┼──────────┼─────────┤
│ Sophia Taylor        │    91%     │    87%    │    85%   │    88%   │    --    │  87.8%  │
│ sophia@demo.com      │   [GREEN]  │  [GREEN]  │ [GREEN]  │ [GREEN]  │   [--]   │ [GREEN] │
├──────────────────────┼────────────┼───────────┼──────────┼──────────┼──────────┼─────────┤
│ James Anderson       │    73%     │    75%    │    --    │    70%   │    74%   │  73.0%  │
│ james@demo.com       │   [BLUE]   │  [BLUE]   │   [--]   │ [BLUE]   │ [BLUE]   │ [BLUE]  │
├──────────────────────┼────────────┼───────────┼──────────┼──────────┼──────────┼─────────┤
│ CLASS AVERAGE        │   83.3%    │   84.5%   │  81.3%   │  83.5%   │  82.8%   │  83.1%  │
│                      │   [BLUE]   │  [BLUE]   │ [BLUE]   │ [BLUE]   │ [BLUE]   │ [BLUE]  │
└──────────────────────┴────────────┴───────────┴──────────┴──────────┴──────────┴─────────┘
```

**Key Features:**

- **Sticky Headers**: Column headers stick to top when scrolling
- **Sticky First Column**: Student names stick to left when scrolling horizontally

- **Assignment Columns**:
  - Assignment title
  - Type badge (PRACTICE, QUIZ, TEST, HOMEWORK)
  - Due date

- **Grade Cells**:
  - Color-coded badges:
    * 🟢 Green (85%+): High score
    * 🔵 Blue (70-84%): Satisfactory
    * 🟡 Orange (<70%): Below grade level
    * 🟡 Yellow "Submitted": Awaiting grading
    * Gray "--": Not submitted

- **Student Average Column**: Automatically calculated
- **Class Average Row**: Shows average per assignment + overall

- **Export Button**: Export this specific class to CSV

---

## What the Analytics Look Like

### 1. Analytics Overview (`/teacher/analytics`)

**Layout:**

```
╔═══════════════════════════════════════════════════════════╗
║                  📊 Class Analytics                       ║
║        View detailed analytics for each of your classes   ║
╚═══════════════════════════════════════════════════════════╝

┌───────────────────────────────────────────────────────────┐
│        📈 Performance Trend (Last 30 Days)                │
├───────────────────────────────────────────────────────────┤
│                                                           │
│   100% ┐                              ●                   │
│        │                         ●        ●               │
│    90% ┤                    ●                ●            │
│        │               ●                         ●        │
│    80% ┤          ●                                  ●    │
│        │     ●                                            │
│    70% ┤●                                                 │
│        │                                                  │
│     0% └──────────────────────────────────────────────────┤
│         Week 1   Week 2   Week 3   Week 4   Today        │
│                                                           │
│   [Shows class-wide average trending upward over time]   │
└───────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────┐
│          ⚠️ At-Risk Students Summary                      │
├───────────────────────────────────────────────────────────┤
│  ┌─────────┬──────────┬────────────┬──────────┐          │
│  │Critical │Declining │ Low Scores │ Inactive │          │
│  │   3     │    5     │     8      │    2     │          │
│  └─────────┴──────────┴────────────┴──────────┘          │
│                                                           │
│  Critical: Students with <60% average                     │
│  Declining: Performance dropped >15% in 2 weeks          │
│  Low Scores: Consistently scoring 60-70%                 │
│  Inactive: No activity in 7+ days                        │
│                                                           │
│                 View Full Details →                       │
└───────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────┐
│  5th Grade Math & Science              ID: 12             │
├───────────────────────────────────────────────────────────┤
│  Total Students:      8                                   │
│  Class Average:       83.3% [BLUE - Satisfactory]        │
│  Total Assessments:   24                                  │
│                                                           │
│  Ability Breakdown:                                       │
│  ┌─────────────┬─────────────┬─────────────┐            │
│  │ Struggling  │  On-Level   │  Advanced   │            │
│  │     2       │      4      │      2      │            │
│  │  [RED]      │  [YELLOW]   │  [GREEN]    │            │
│  └─────────────┴─────────────┴─────────────┘            │
│                                                           │
│  Click for detailed analytics →                          │
└───────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────┐
│  7th Grade English & History           ID: 13             │
├───────────────────────────────────────────────────────────┤
│  Total Students:      8                                   │
│  Class Average:       81.5% [BLUE - Satisfactory]        │
│  Total Assessments:   28                                  │
│                                                           │
│  Ability Breakdown:                                       │
│  ┌─────────────┬─────────────┬─────────────┐            │
│  │ Struggling  │  On-Level   │  Advanced   │            │
│  │     1       │      5      │      2      │            │
│  │  [RED]      │  [YELLOW]   │  [GREEN]    │            │
│  └─────────────┴─────────────┴─────────────┘            │
└───────────────────────────────────────────────────────────┘
```

**Key Features:**

- **Performance Trend Chart** (interactive Chart.js graph)
  - Shows class-wide average scores over last 30 days
  - Identifies upward/downward trends
  - Color-coded line (cyan gradient)

- **At-Risk Students Summary**
  - 4 categories of concern:
    * **Critical**: <60% average (urgent intervention)
    * **Declining**: Performance dropped >15% recently
    * **Low Scores**: Consistently 60-70%
    * **Inactive**: No activity in 7+ days
  - Color-coded alerts
  - Link to detailed early warning dashboard

- **Class Summary Cards**
  - Total students
  - Class average (color-coded)
  - Total assessments completed
  - **Ability Breakdown**:
    * Struggling (below grade level)
    * On-Level (meeting expectations)
    * Advanced (exceeding expectations)
  - Click to view detailed class analytics

---

### 2. Class-Specific Analytics (`/teacher/class/{class_id}/analytics`)

When you click on a class card, you see detailed analytics for that specific class.

**Features Include:**

- **Student Performance Grid**:
  - Each student's average
  - Subject-specific breakdowns
  - Trend indicators (improving/declining/stable)
  - Recent activity timestamps

- **Subject Analysis**:
  - Which subjects have highest/lowest class averages
  - Identify curriculum areas needing attention

- **Engagement Metrics**:
  - Questions answered per student
  - Time spent learning
  - Lesson completion rates
  - Arcade game participation

- **Individual Student Deep-Dive**:
  - Strengths and weaknesses by topic
  - Learning patterns (when they study most)
  - Recommended interventions

---

## Parent Analytics (`/parent/analytics`)

Parents see a simplified version focused on their linked students:

```
╔═══════════════════════════════════════════════════════════╗
║                 📊 Student Progress                       ║
║              Track your child's learning journey          ║
╚═══════════════════════════════════════════════════════════╝

┌───────────────────────────────────────────────────────────┐
│  Emma Johnson                         Grade 5             │
├───────────────────────────────────────────────────────────┤
│  Overall Performance: 90.4% [HIGH PERFORMING]             │
│  Current Ability: Advanced                                │
│  Learning Streak: 12 days                                 │
│                                                           │
│  Subject Breakdown:                                       │
│  ┌──────────────────────────────────────────────────┐    │
│  │ Math           ████████████████░░  92%  [Excellent]│   │
│  │ Science        █████████████████░  95%  [Excellent]│   │
│  │ Reading        ██████████████░░░  87%  [Good]     │   │
│  │ Writing        ███████████████░░  89%  [Good]     │   │
│  │ Bible          ████████████████░  91%  [Excellent]│   │
│  └──────────────────────────────────────────────────┘    │
│                                                           │
│  Recent Achievements:                                     │
│  🏆 Perfect Score - Math Chapter 5                        │
│  ⚡ 10-Day Learning Streak                                │
│  🎮 Arcade Master - 5 Games Completed                     │
│                                                           │
│  Time This Week: 4.5 hours                                │
│  Questions Answered: 127                                  │
│  Chapters Completed: 2                                    │
└───────────────────────────────────────────────────────────┘
```

**Parent Features:**
- Overall performance score
- Subject-by-subject progress bars
- Recent achievements and badges
- Weekly activity summary
- Learning streak tracking
- Safety/moderation alerts (if any flagged content)

---

## Student Analytics (`/student/dashboard` and `/student/analytics`)

Students see gamified analytics focused on motivation:

```
╔═══════════════════════════════════════════════════════════╗
║                    🚀 Your Progress                       ║
║                  Keep up the great work!                  ║
╚═══════════════════════════════════════════════════════════╝

┌───────────────────────────────────────────────────────────┐
│                    Your Stats Today                       │
├───────────────────────────────────────────────────────────┤
│  Level: 12          XP: 2,450 / 3,000                     │
│  [████████████████░░░░] 82%                               │
│                                                           │
│  🔥 Streak: 12 days        💰 Tokens: 845                │
│  ⭐ Badges: 18             🏆 Achievements: 24            │
└───────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────┐
│              Subject Progress (NumForge)                  │
├───────────────────────────────────────────────────────────┤
│  Chapter 1: Whole Numbers          ✅ 100% Complete       │
│  Chapter 2: Fractions              ✅ 100% Complete       │
│  Chapter 3: Decimals               🔄  67% Complete       │
│  Chapter 4: Percentages            🔒  Locked             │
│  Chapter 5: Algebra Basics         🔒  Locked             │
└───────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────┐
│                 Recent Achievements                       │
├───────────────────────────────────────────────────────────┤
│  🏆 Perfect Score - Math Chapter 2 Quiz    (2 days ago)   │
│  ⚡ 10-Day Streak Milestone               (Yesterday)     │
│  🎮 Speed Math Champion                   (3 days ago)    │
│  📚 Bookworm - 5 Chapters Complete        (1 week ago)    │
└───────────────────────────────────────────────────────────┘
```

**Student Features:**
- Level and XP progress bar
- Streak counter (motivational)
- Token balance (for arcade shop)
- Badge and achievement displays
- Chapter completion checklist
- Recent achievements feed

---

## Color Coding System

Throughout analytics and gradebook, consistent color coding:

| Color | Range | Meaning | CSS Class |
|-------|-------|---------|-----------|
| 🟢 **Green** | 85-100% | High performing / Advanced | `.grade-high`, `.good` |
| 🔵 **Blue** | 70-84% | On-level / Satisfactory | `.grade-mid`, `.warning` |
| 🟡 **Orange** | 0-69% | Below grade / Needs help | `.grade-low`, `.danger` |
| 🟡 **Yellow** | N/A | Submitted (awaiting grading) | `.grade-submitted` |
| ⚪ **Gray** | N/A | Not submitted / No data | `.grade-missing` |

---

## How to Test This Yourself

### Step 1: Generate Demo Data
```bash
cd /Users/tamara/Desktop/cozmiclearning
python generate_demo_data.py
```

Enter `yes` when prompted.

### Step 2: Login as Demo Teacher
1. Go to `/teacher/login`
2. Email: `demo+teacher@cozmiclearning.com`
3. Password: `demo123`

### Step 3: Explore Features
Navigate to:
- **Gradebook**: Click "Gradebook" in nav menu
  - See grading backlog
  - View class cards with assignment summaries
  - Click into a class to see full table
  - Try exporting to CSV

- **Analytics**: Click "Analytics" in nav menu
  - See performance trend chart
  - View at-risk student summary
  - Click into class for detailed analytics

### Step 4: Test Grading Workflow
1. From gradebook, click "Grade Now" on an ungraded submission
2. Review student answer
3. Add feedback
4. Assign grade
5. Save
6. Return to gradebook → see grade updated in real-time

---

## Export Functionality

### CSV Export Format

When you export a gradebook, you get a CSV file like this:

```csv
Student Name,Student Email,Assignment 1,Assignment 2,Assignment 3,Assignment 4,Assignment 5,Student Average
Emma Johnson,emma@demo.com,92%,95%,88%,90%,87%,90.4%
Liam Smith,liam@demo.com,78%,82%,75%,--,--,78.3%
Olivia Brown,olivia@demo.com,65%,70%,68%,72%,69%,68.8%
Noah Davis,noah@demo.com,88%,91%,--,85%,89%,88.3%
Ava Wilson,ava@demo.com,94%,98%,92%,96%,95%,95.0%
Class Average,--,83.3%,84.5%,81.3%,83.5%,82.8%,83.1%
```

**Uses:**
- Import into Excel/Google Sheets for further analysis
- Create charts and graphs
- Share with administrators
- Printable report cards
- SIS integration

---

## Key Insights You Can Gain

### From Gradebook:
1. **Who needs grading?** → Grading backlog with priority queue
2. **Which assignments are complete?** → X/Y graded counts
3. **How is the class performing?** → Color-coded averages
4. **Who's struggling?** → Orange/red scores
5. **What's the class average?** → Bottom row of gradebook table

### From Analytics:
1. **Is performance improving?** → Trend chart over 30 days
2. **Who's at risk?** → Early warning summary
3. **Which subjects need help?** → Subject breakdowns
4. **Who's advanced vs. struggling?** → Ability distribution
5. **Are students engaged?** → Activity metrics

---

## Responsive Design

All analytics and gradebook pages are:
- ✅ **Mobile-friendly** (responsive grid layouts)
- ✅ **Tablet-optimized** (touch-friendly interfaces)
- ✅ **Desktop-enhanced** (full data tables on large screens)

On smaller screens:
- Tables scroll horizontally
- Cards stack vertically
- Export buttons remain accessible
- Priority information shown first

---

## Next Steps

1. **Generate demo data**: Run `python generate_demo_data.py`
2. **Login and explore**: Use demo teacher account
3. **Test workflows**: Grade submissions, export gradebook
4. **Customize**: Adjust colors, layout, or add features as needed

Your analytics and gradebook are **production-ready** and provide comprehensive insights for teachers while maintaining a beautiful, intuitive interface!
