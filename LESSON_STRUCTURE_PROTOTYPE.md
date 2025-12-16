# Lesson Structure Prototype - Hierarchical Organization

## New Data Structure: Subject → Chapters → Lessons

This prototype shows the new hierarchical organization for **NumForge (Math)** as an example.

---

## Example: NumForge (Math) - Grade 3

### Current Structure (Flat)
```python
"num_forge": {
    3: ["Multiplication Tables", "Division Basics", "Fractions Introduction", "Area & Perimeter"]
}
```
❌ **Problems:**
- No context or progression
- Topics are isolated
- Can't show relationships between concepts
- Hard to track learning paths

---

### New Structure (Hierarchical)

```python
"num_forge": {
    3: {
        "chapters": [
            {
                "id": "mult_mastery",
                "title": "Multiplication Mastery",
                "description": "Learn the fundamentals of multiplication and become fluent in your times tables",
                "icon": "✖️",
                "color": "purple",
                "estimated_time": "2-3 weeks",
                "lessons": [
                    "What is Multiplication?",
                    "Multiplication by 2s and 5s",
                    "Multiplication by 3s and 4s",
                    "Multiplication by 10s and 100s",
                    "Multiplication Tables (6-9)",
                    "Multiplication Word Problems"
                ]
            },
            {
                "id": "division_intro",
                "title": "Understanding Division",
                "description": "Discover division as the opposite of multiplication and learn to share equally",
                "icon": "➗",
                "color": "blue",
                "estimated_time": "2 weeks",
                "prerequisite": "mult_mastery",  # Must complete previous chapter
                "lessons": [
                    "Division as Sharing",
                    "Division and Multiplication Connection",
                    "Division Facts (÷2, ÷5, ÷10)",
                    "Division with Remainders",
                    "Division Word Problems"
                ]
            },
            {
                "id": "fractions_begin",
                "title": "Fraction Foundations",
                "description": "Explore parts of a whole and learn to work with simple fractions",
                "icon": "🍕",
                "color": "orange",
                "estimated_time": "3 weeks",
                "lessons": [
                    "What Are Fractions?",
                    "Fractions on a Number Line",
                    "Comparing Fractions",
                    "Equivalent Fractions",
                    "Adding Like Fractions",
                    "Subtracting Like Fractions"
                ]
            },
            {
                "id": "measurement_geo",
                "title": "Measurement & Geometry Basics",
                "description": "Learn to measure shapes and calculate area and perimeter",
                "icon": "📏",
                "color": "green",
                "estimated_time": "2 weeks",
                "lessons": [
                    "Understanding Perimeter",
                    "Calculating Perimeter of Rectangles",
                    "Introduction to Area",
                    "Finding Area of Rectangles",
                    "Real-World Measurement Problems"
                ]
            }
        ]
    }
}
```

---

## Visual Flow: How Students Navigate

```
NumForge (Subject)
    │
    ├─ Select Grade (3)
    │
    ├─ View Chapter Map (4 chapters displayed as cards)
    │   │
    │   ├─ Chapter 1: Multiplication Mastery [6 lessons] ⭐ Start here!
    │   ├─ Chapter 2: Understanding Division [5 lessons] 🔒 Complete Chapter 1 first
    │   ├─ Chapter 3: Fraction Foundations [6 lessons]
    │   └─ Chapter 4: Measurement & Geometry Basics [5 lessons]
    │
    ├─ Select Chapter (Multiplication Mastery)
    │
    ├─ View Lessons in Chapter
    │   │
    │   ├─ Lesson 1: What is Multiplication? ✅ Completed
    │   ├─ Lesson 2: Multiplication by 2s and 5s ▶️ In Progress
    │   ├─ Lesson 3: Multiplication by 3s and 4s 🔒 Locked
    │   ├─ Lesson 4: Multiplication by 10s and 100s 🔒 Locked
    │   ├─ Lesson 5: Multiplication Tables (6-9) 🔒 Locked
    │   └─ Lesson 6: Multiplication Word Problems 🔒 Locked
    │
    └─ Take Lesson → Chat → Mark Complete → Next Lesson
```

---

## Complete Example: All Grades for NumForge

```python
LESSON_CHAPTERS = {
    "num_forge": {
        1: {
            "chapters": [
                {
                    "id": "counting_basics",
                    "title": "Counting & Number Sense",
                    "description": "Master counting, number recognition, and understanding quantities",
                    "icon": "🔢",
                    "lessons": [
                        "Numbers 1-20",
                        "Counting to 100",
                        "Comparing Numbers (Greater/Less)",
                        "Number Patterns"
                    ]
                },
                {
                    "id": "addition_intro",
                    "title": "Beginning Addition",
                    "description": "Learn to add numbers together and solve simple problems",
                    "icon": "➕",
                    "lessons": [
                        "What is Addition?",
                        "Adding Within 10",
                        "Adding Within 20",
                        "Addition Word Problems"
                    ]
                },
                {
                    "id": "subtraction_intro",
                    "title": "Beginning Subtraction",
                    "description": "Understand taking away and finding the difference",
                    "icon": "➖",
                    "lessons": [
                        "What is Subtraction?",
                        "Subtracting Within 10",
                        "Subtracting Within 20",
                        "Subtraction Word Problems"
                    ]
                },
                {
                    "id": "shapes_patterns",
                    "title": "Shapes & Patterns",
                    "description": "Explore 2D shapes and create patterns",
                    "icon": "🔷",
                    "lessons": [
                        "Basic 2D Shapes",
                        "Comparing Shapes",
                        "Creating Patterns",
                        "Extending Patterns"
                    ]
                }
            ]
        },

        2: {
            "chapters": [
                {
                    "id": "place_value",
                    "title": "Place Value Foundations",
                    "description": "Understand tens and ones in two-digit numbers",
                    "icon": "💯",
                    "lessons": [
                        "Tens and Ones",
                        "Expanded Form",
                        "Comparing Two-Digit Numbers",
                        "Skip Counting by 2s, 5s, 10s"
                    ]
                },
                {
                    "id": "addition_2digit",
                    "title": "Two-Digit Addition",
                    "description": "Add larger numbers with and without regrouping",
                    "icon": "➕",
                    "prerequisite": "place_value",
                    "lessons": [
                        "Adding Without Regrouping",
                        "Adding With Regrouping",
                        "Mental Math Strategies",
                        "Multi-Step Word Problems"
                    ]
                },
                {
                    "id": "subtraction_2digit",
                    "title": "Two-Digit Subtraction",
                    "description": "Subtract larger numbers with and without regrouping",
                    "icon": "➖",
                    "lessons": [
                        "Subtracting Without Regrouping",
                        "Subtracting With Regrouping",
                        "Checking Subtraction with Addition",
                        "Real-World Subtraction Problems"
                    ]
                },
                {
                    "id": "time_money",
                    "title": "Time & Money Basics",
                    "description": "Learn to tell time and count money",
                    "icon": "🕐",
                    "lessons": [
                        "Telling Time (Hour & Half Hour)",
                        "Telling Time (Quarter Hour & 5 Minutes)",
                        "Counting Coins (Pennies to Quarters)",
                        "Making Change"
                    ]
                }
            ]
        },

        3: {
            "chapters": [
                {
                    "id": "mult_mastery",
                    "title": "Multiplication Mastery",
                    "description": "Learn multiplication fundamentals and master times tables",
                    "icon": "✖️",
                    "lessons": [
                        "What is Multiplication?",
                        "Multiplication by 2s and 5s",
                        "Multiplication by 3s and 4s",
                        "Multiplication by 10s and 100s",
                        "Multiplication Tables (6-9)",
                        "Multiplication Word Problems"
                    ]
                },
                {
                    "id": "division_intro",
                    "title": "Understanding Division",
                    "description": "Discover division and learn to share equally",
                    "icon": "➗",
                    "prerequisite": "mult_mastery",
                    "lessons": [
                        "Division as Sharing",
                        "Division and Multiplication Connection",
                        "Division Facts (÷2, ÷5, ÷10)",
                        "Division with Remainders",
                        "Division Word Problems"
                    ]
                },
                {
                    "id": "fractions_begin",
                    "title": "Fraction Foundations",
                    "description": "Explore fractions and parts of a whole",
                    "icon": "🍕",
                    "lessons": [
                        "What Are Fractions?",
                        "Fractions on a Number Line",
                        "Comparing Fractions",
                        "Equivalent Fractions",
                        "Adding Like Fractions",
                        "Subtracting Like Fractions"
                    ]
                },
                {
                    "id": "measurement_geo",
                    "title": "Measurement & Geometry",
                    "description": "Learn about area, perimeter, and shapes",
                    "icon": "📏",
                    "lessons": [
                        "Understanding Perimeter",
                        "Calculating Perimeter",
                        "Introduction to Area",
                        "Finding Area of Rectangles",
                        "Real-World Measurement"
                    ]
                }
            ]
        },

        6: {
            "chapters": [
                {
                    "id": "ratios_rates",
                    "title": "Ratios & Rates",
                    "description": "Understand relationships between quantities",
                    "icon": "⚖️",
                    "lessons": [
                        "Introduction to Ratios",
                        "Equivalent Ratios",
                        "Unit Rates",
                        "Ratio Tables",
                        "Ratio Word Problems",
                        "Percent Introduction"
                    ]
                },
                {
                    "id": "negative_numbers",
                    "title": "Negative Numbers & Integers",
                    "description": "Extend the number line to include negative numbers",
                    "icon": "➖➕",
                    "lessons": [
                        "What Are Negative Numbers?",
                        "Integers on a Number Line",
                        "Comparing Integers",
                        "Adding Integers",
                        "Subtracting Integers",
                        "Real-World Integer Applications"
                    ]
                },
                {
                    "id": "algebraic_thinking",
                    "title": "Introduction to Algebra",
                    "description": "Start working with variables and expressions",
                    "icon": "🔤",
                    "lessons": [
                        "Variables and Expressions",
                        "Writing Algebraic Expressions",
                        "Evaluating Expressions",
                        "One-Step Equations",
                        "Two-Step Equations",
                        "Inequality Solutions"
                    ]
                },
                {
                    "id": "geometry_6",
                    "title": "Advanced Geometry",
                    "description": "Calculate area and volume of complex shapes",
                    "icon": "📐",
                    "lessons": [
                        "Area of Triangles",
                        "Area of Parallelograms",
                        "Area of Trapezoids",
                        "Surface Area of Prisms",
                        "Volume of Rectangular Prisms"
                    ]
                }
            ]
        },

        9: {
            "chapters": [
                {
                    "id": "linear_equations",
                    "title": "Linear Equations & Inequalities",
                    "description": "Master solving equations and inequalities",
                    "icon": "📈",
                    "lessons": [
                        "Multi-Step Equations",
                        "Equations with Variables on Both Sides",
                        "Literal Equations",
                        "Compound Inequalities",
                        "Absolute Value Equations",
                        "Systems of Linear Equations"
                    ]
                },
                {
                    "id": "functions",
                    "title": "Functions & Graphing",
                    "description": "Understand functions and their representations",
                    "icon": "📊",
                    "prerequisite": "linear_equations",
                    "lessons": [
                        "What is a Function?",
                        "Function Notation",
                        "Linear Functions",
                        "Slope-Intercept Form",
                        "Point-Slope Form",
                        "Graphing Linear Inequalities"
                    ]
                },
                {
                    "id": "quadratics",
                    "title": "Quadratic Functions",
                    "description": "Explore parabolas and quadratic equations",
                    "icon": "🎯",
                    "prerequisite": "functions",
                    "lessons": [
                        "Introduction to Quadratics",
                        "Graphing Parabolas",
                        "Factoring Quadratics",
                        "Quadratic Formula",
                        "Completing the Square",
                        "Applications of Quadratics"
                    ]
                },
                {
                    "id": "exponents_radicals",
                    "title": "Exponents & Radicals",
                    "description": "Work with powers and roots",
                    "icon": "²√",
                    "lessons": [
                        "Laws of Exponents",
                        "Zero and Negative Exponents",
                        "Scientific Notation",
                        "Simplifying Radicals",
                        "Operations with Radicals",
                        "Rational Exponents"
                    ]
                }
            ]
        }
    }
}
```

---

## UI Mockup: Chapter Selection Page

```
╔══════════════════════════════════════════════════════════════╗
║                   NumForge (Math) - Grade 3                  ║
║                  Choose Your Chapter to Begin                ║
╚══════════════════════════════════════════════════════════════╝

┌─────────────────────────┐  ┌─────────────────────────┐
│   ✖️ CHAPTER 1          │  │   ➗ CHAPTER 2          │
│ Multiplication Mastery  │  │ Understanding Division  │
│ ─────────────────────── │  │ ─────────────────────── │
│ Learn multiplication    │  │ Discover division as    │
│ fundamentals and master │  │ the opposite of         │
│ your times tables       │  │ multiplication          │
│                         │  │                         │
│ 📚 6 Lessons            │  │ 📚 5 Lessons            │
│ ⏱️ 2-3 weeks            │  │ ⏱️ 2 weeks              │
│                         │  │                         │
│ Progress: ▓▓▓▓░░ 67%    │  │ 🔒 Complete Chapter 1   │
│                         │  │    first                │
│ [Continue Learning →]   │  │                         │
└─────────────────────────┘  └─────────────────────────┘

┌─────────────────────────┐  ┌─────────────────────────┐
│   🍕 CHAPTER 3          │  │   📏 CHAPTER 4          │
│  Fraction Foundations   │  │ Measurement & Geometry  │
│ ─────────────────────── │  │ ─────────────────────── │
│ Explore fractions and   │  │ Learn about area,       │
│ parts of a whole        │  │ perimeter, and shapes   │
│                         │  │                         │
│ 📚 6 Lessons            │  │ 📚 5 Lessons            │
│ ⏱️ 3 weeks              │  │ ⏱️ 2 weeks              │
│                         │  │                         │
│ Progress: ░░░░░░ 0%     │  │ Progress: ░░░░░░ 0%     │
│                         │  │                         │
│ [Start Chapter →]       │  │ [Start Chapter →]       │
└─────────────────────────┘  └─────────────────────────┘
```

---

## UI Mockup: Lesson Selection Within Chapter

```
╔══════════════════════════════════════════════════════════════╗
║          ✖️ Multiplication Mastery - Grade 3 Math            ║
║              Master multiplication fundamentals              ║
╚══════════════════════════════════════════════════════════════╝

Progress: ▓▓▓▓░░ 4/6 lessons completed (67%)

┌──────────────────────────────────────────────────────────────┐
│ 1️⃣ What is Multiplication?                          ✅ Complete │
│    Learn the concept of repeated addition                    │
│    [Review Lesson]                                           │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│ 2️⃣ Multiplication by 2s and 5s                      ✅ Complete │
│    Practice your 2 and 5 times tables                        │
│    [Review Lesson]                                           │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│ 3️⃣ Multiplication by 3s and 4s                      ✅ Complete │
│    Master the 3 and 4 times tables                           │
│    [Review Lesson]                                           │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│ 4️⃣ Multiplication by 10s and 100s                   ✅ Complete │
│    Learn patterns in multiplying by 10 and 100               │
│    [Review Lesson]                                           │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│ 5️⃣ Multiplication Tables (6-9)                      ▶️ Next Up  │
│    Practice your 6, 7, 8, and 9 times tables                 │
│    [Start Lesson →]                                          │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│ 6️⃣ Multiplication Word Problems                     🔒 Locked  │
│    Apply multiplication to real-world situations             │
│    Complete Lesson 5 to unlock                               │
└──────────────────────────────────────────────────────────────┘

[← Back to Chapters]              [Take Chapter Quiz →]
```

---

## Benefits of New Structure

### ✅ For Students:
1. **Clear Learning Path** - Know exactly what comes next
2. **Sense of Progress** - See completion % for each chapter
3. **Prerequisites** - Understand what you need to know first
4. **Grouped by Topic** - Related lessons are together
5. **Estimated Time** - Know how long each chapter takes
6. **Visual Icons** - Quickly identify chapters

### ✅ For Parents/Teachers:
1. **Better Planning** - See full curriculum scope
2. **Track Progress** - Monitor chapter completion
3. **Identify Gaps** - See which chapters are incomplete
4. **Logical Sequence** - Understand skill progression
5. **Time Estimates** - Plan learning schedules

### ✅ For Platform:
1. **Better Organization** - Scalable structure
2. **Progress Tracking** - Can track chapter/lesson completion
3. **Adaptive Learning** - Can recommend next chapters
4. **Prerequisites** - Can enforce learning sequences
5. **Chapter Assessments** - Can add quizzes at chapter end
6. **Badges/Rewards** - Can give chapter completion badges

---

## Database Schema (Future Enhancement)

```python
# models.py - New tables for progress tracking

class ChapterProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    subject = db.Column(db.String(50))  # e.g., "num_forge"
    grade = db.Column(db.Integer)
    chapter_id = db.Column(db.String(50))  # e.g., "mult_mastery"
    lessons_completed = db.Column(db.Integer, default=0)
    total_lessons = db.Column(db.Integer)
    started_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime, nullable=True)
    quiz_score = db.Column(db.Integer, nullable=True)

class LessonProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    subject = db.Column(db.String(50))
    grade = db.Column(db.Integer)
    chapter_id = db.Column(db.String(50))
    lesson_title = db.Column(db.String(200))
    completed = db.Column(db.Boolean, default=False)
    completed_at = db.Column(db.DateTime, nullable=True)
    time_spent_minutes = db.Column(db.Integer, default=0)
```

---

## Implementation Phases

### Phase 1 (MVP - This Week)
- ✅ Create new chapter structure in `student_lessons.py`
- ✅ Add `/chapter-library` route
- ✅ Create `chapter_library.html` template
- ✅ Update `/lesson-library` to show lessons for selected chapter
- ✅ Add breadcrumb navigation: Subject → Chapter → Lesson

### Phase 2 (Next Week)
- Add chapter progress tracking (session-based)
- Show progress bars on chapter cards
- Add "locked" state for prerequisite chapters
- Add chapter icons and colors

### Phase 3 (Future)
- Database storage for progress
- Chapter quizzes
- Chapter completion badges
- Adaptive recommendations
- Chapter roadmap visualization

---

## Next Steps

1. **Review this prototype** - Does this structure make sense?
2. **Approve Phase 1** - Should I start implementing the MVP?
3. **Customize** - Want to adjust chapter names, add more/less lessons?
4. **Other Subjects** - Should I create similar structures for all 12 subjects?

Let me know if you'd like me to proceed with implementation!
