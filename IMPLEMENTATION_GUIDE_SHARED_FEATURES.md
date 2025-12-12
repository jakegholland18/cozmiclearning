# Implementation Guide: Shared Teacher/Homeschool Features
**CozmicLearning - Priority Features Build Guide**

---

## 🎯 Overview

This guide provides step-by-step implementation specs for building shared features that work for BOTH teachers and homeschool parents. Each feature includes database models, routes, UI templates, and integration points.

---

## Feature 1: Assignment Template Library ⭐⭐⭐⭐⭐

**Impact:** Saves 10-15 minutes per assignment creation
**Effort:** 2-3 days
**Works For:** Teachers AND Homeschool Parents

### Database Model

Add to `models.py` after the Teacher model (around line 100):

```python
class AssignmentTemplate(db.Model):
    """
    Reusable assignment templates for teachers and homeschool parents.
    Save any assignment as a template for quick duplication.
    """
    __tablename__ = "assignment_templates"

    id = db.Column(db.Integer, primary_key=True)

    # Owner (can be teacher or parent with homeschool plan)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'), nullable=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('parents.id'), nullable=True)

    # Template metadata
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    subject = db.Column(db.String(50))  # math, science, reading, writing, bible, history
    grade_level = db.Column(db.String(20))  # e.g., "6-8", "9-12", "all"
    topic = db.Column(db.String(200))

    # Template content (stores assignment structure as JSON)
    template_data = db.Column(db.Text, nullable=False)  # JSON structure
    # Example template_data:
    # {
    #   "instructions": "Complete the following questions...",
    #   "differentiation_mode": "adaptive",
    #   "question_count": 10,
    #   "difficulty_levels": ["easy", "medium", "hard"],
    #   "topics": ["fractions", "decimals"],
    #   "custom_settings": {...}
    # }

    # Sharing settings
    is_public = db.Column(db.Boolean, default=False)  # Share with all users
    is_featured = db.Column(db.Boolean, default=False)  # Featured by admins

    # Usage tracking
    use_count = db.Column(db.Integer, default=0)  # How many times duplicated

    # Tags for searching
    tags = db.Column(db.Text)  # JSON array: ["multiplication", "grade3", "visual"]

    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<AssignmentTemplate {self.title}>'
```

### Database Migration

Run after adding the model:

```bash
# In terminal:
flask db migrate -m "Add assignment template system"
flask db upgrade
```

Or add manually in database:

```sql
CREATE TABLE assignment_templates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    teacher_id INTEGER,
    parent_id INTEGER,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    subject VARCHAR(50),
    grade_level VARCHAR(20),
    topic VARCHAR(200),
    template_data TEXT NOT NULL,
    is_public BOOLEAN DEFAULT 0,
    is_featured BOOLEAN DEFAULT 0,
    use_count INTEGER DEFAULT 0,
    tags TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (teacher_id) REFERENCES teachers(id),
    FOREIGN KEY (parent_id) REFERENCES parents(id)
);

CREATE INDEX idx_template_teacher ON assignment_templates(teacher_id);
CREATE INDEX idx_template_parent ON assignment_templates(parent_id);
CREATE INDEX idx_template_subject ON assignment_templates(subject);
CREATE INDEX idx_template_public ON assignment_templates(is_public);
```

### Routes to Add

Add to `app.py`:

#### 1. Save Assignment as Template

```python
@app.route("/save-assignment-template", methods=["POST"])
def save_assignment_template():
    """
    Save an existing assignment as a reusable template.
    Works for both teachers and homeschool parents.
    """
    # Check if user is teacher or homeschool parent
    user_role = session.get("user_role")
    if user_role not in ["teacher", "parent"]:
        flash("Only teachers and homeschool parents can create templates.", "error")
        return redirect("/")

    # Get form data
    title = request.form.get("title")
    description = request.form.get("description", "")
    subject = request.form.get("subject")
    grade_level = request.form.get("grade_level", "all")
    topic = request.form.get("topic", "")
    is_public = request.form.get("is_public") == "on"
    tags_input = request.form.get("tags", "")  # Comma-separated

    # Get template structure from assignment
    assignment_id = request.form.get("assignment_id")
    # TODO: Fetch assignment data and convert to template_data JSON

    template_data = {
        "instructions": request.form.get("instructions", ""),
        "differentiation_mode": request.form.get("differentiation_mode", "none"),
        "question_count": int(request.form.get("question_count", 10)),
        # Add more fields as needed
    }

    # Create template
    template = AssignmentTemplate(
        teacher_id=session.get("teacher_id") if user_role == "teacher" else None,
        parent_id=session.get("parent_id") if user_role == "parent" else None,
        title=title,
        description=description,
        subject=subject,
        grade_level=grade_level,
        topic=topic,
        template_data=json.dumps(template_data),
        is_public=is_public,
        tags=json.dumps([tag.strip() for tag in tags_input.split(",") if tag.strip()])
    )

    db.session.add(template)
    db.session.commit()

    flash(f"Template '{title}' saved successfully!", "success")

    # Redirect based on user role
    if user_role == "teacher":
        return redirect("/teacher/templates")
    else:
        return redirect("/homeschool/templates")
```

#### 2. View Template Library

```python
@app.route("/teacher/templates")
@app.route("/homeschool/templates")
def template_library():
    """
    Display all available templates (personal + public).
    Works for both teachers and homeschool parents.
    """
    user_role = session.get("user_role")

    if user_role == "teacher":
        teacher_id = session.get("teacher_id")
        # Get personal templates
        my_templates = AssignmentTemplate.query.filter_by(teacher_id=teacher_id).all()
        route_prefix = "/teacher"
    elif user_role == "parent":
        parent_id = session.get("parent_id")
        # Check if homeschool plan
        parent = Parent.query.get(parent_id)
        if parent.plan not in ["homeschool_essential", "homeschool_complete"]:
            flash("Template library is for homeschool plans only.", "error")
            return redirect("/parent_dashboard")
        # Get personal templates
        my_templates = AssignmentTemplate.query.filter_by(parent_id=parent_id).all()
        route_prefix = "/homeschool"
    else:
        flash("Access denied.", "error")
        return redirect("/")

    # Get public/featured templates
    public_templates = AssignmentTemplate.query.filter_by(is_public=True).order_by(AssignmentTemplate.use_count.desc()).limit(20).all()

    # Get filters from query params
    subject_filter = request.args.get("subject")
    grade_filter = request.args.get("grade")
    search_query = request.args.get("search")

    # Apply filters
    if subject_filter:
        my_templates = [t for t in my_templates if t.subject == subject_filter]
        public_templates = [t for t in public_templates if t.subject == subject_filter]

    if search_query:
        my_templates = [t for t in my_templates if search_query.lower() in t.title.lower()]
        public_templates = [t for t in public_templates if search_query.lower() in t.title.lower()]

    return render_template(
        "template_library.html",
        my_templates=my_templates,
        public_templates=public_templates,
        route_prefix=route_prefix,
        subjects=["math", "science", "reading", "writing", "bible", "history"]
    )
```

#### 3. Duplicate Template to Create Assignment

```python
@app.route("/duplicate-template/<int:template_id>", methods=["POST"])
def duplicate_template(template_id):
    """
    Create a new assignment from a template.
    Works for both teachers and homeschool parents.
    """
    template = AssignmentTemplate.query.get_or_404(template_id)
    user_role = session.get("user_role")

    # Check permissions
    if user_role == "teacher":
        # Teacher can use their own templates or public ones
        if template.teacher_id != session.get("teacher_id") and not template.is_public:
            flash("You don't have permission to use this template.", "error")
            return redirect("/teacher/templates")
    elif user_role == "parent":
        # Parent can use their own templates or public ones
        if template.parent_id != session.get("parent_id") and not template.is_public:
            flash("You don't have permission to use this template.", "error")
            return redirect("/homeschool/templates")

    # Increment use count
    template.use_count += 1
    db.session.commit()

    # Parse template data
    template_data = json.loads(template.template_data)

    # Store in session for assignment creation
    session["template_data"] = template_data
    session["template_title"] = template.title
    session["template_subject"] = template.subject

    # Redirect to assignment creation with pre-filled data
    if user_role == "teacher":
        return redirect("/teacher/assignments/create?from_template=true")
    else:
        return redirect("/homeschool/assignments/create?from_template=true")
```

#### 4. Delete Template

```python
@app.route("/delete-template/<int:template_id>", methods=["POST"])
def delete_template(template_id):
    """
    Delete a template (only owner can delete).
    """
    template = AssignmentTemplate.query.get_or_404(template_id)
    user_role = session.get("user_role")

    # Check ownership
    if user_role == "teacher" and template.teacher_id == session.get("teacher_id"):
        db.session.delete(template)
        db.session.commit()
        flash("Template deleted successfully.", "success")
        return redirect("/teacher/templates")
    elif user_role == "parent" and template.parent_id == session.get("parent_id"):
        db.session.delete(template)
        db.session.commit()
        flash("Template deleted successfully.", "success")
        return redirect("/homeschool/templates")
    else:
        flash("You can only delete your own templates.", "error")
        return redirect("/")
```

### UI Template: template_library.html

Create `/website/templates/template_library.html`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Assignment Templates - CozmicLearning</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}?v=20251202">
</head>
<body>
    <div class="container">
        <h1>📋 Assignment Template Library</h1>
        <p>Save time by reusing assignment templates!</p>

        <!-- Search & Filter -->
        <div class="template-filters">
            <form method="get" action="">
                <input type="text" name="search" placeholder="Search templates..." value="{{ request.args.get('search', '') }}">

                <select name="subject">
                    <option value="">All Subjects</option>
                    {% for subject in subjects %}
                    <option value="{{ subject }}" {% if request.args.get('subject') == subject %}selected{% endif %}>
                        {{ subject|title }}
                    </option>
                    {% endfor %}
                </select>

                <button type="submit">🔍 Filter</button>
            </form>
        </div>

        <!-- My Templates Section -->
        <section class="my-templates">
            <h2>📁 My Templates ({{ my_templates|length }})</h2>

            {% if my_templates %}
            <div class="template-grid">
                {% for template in my_templates %}
                <div class="template-card">
                    <h3>{{ template.title }}</h3>
                    <p class="template-meta">
                        <span class="badge">{{ template.subject|title }}</span>
                        <span class="badge-outline">Grade {{ template.grade_level }}</span>
                    </p>
                    <p>{{ template.description[:100] }}...</p>
                    <p class="template-stats">Used {{ template.use_count }} times</p>

                    <div class="template-actions">
                        <form method="post" action="/duplicate-template/{{ template.id }}" style="display: inline;">
                            <button type="submit" class="btn-primary">📋 Use Template</button>
                        </form>
                        <form method="post" action="/delete-template/{{ template.id }}" style="display: inline;" onsubmit="return confirm('Delete this template?')">
                            <button type="submit" class="btn-danger-outline">🗑️ Delete</button>
                        </form>
                    </div>
                </div>
                {% endfor %}
            </div>
            {% else %}
            <p class="empty-state">
                You haven't created any templates yet. Create an assignment and save it as a template!
            </p>
            {% endif %}
        </section>

        <!-- Public Templates Section -->
        <section class="public-templates">
            <h2>🌐 Community Templates ({{ public_templates|length }})</h2>
            <p>Shared by other teachers and homeschool parents</p>

            {% if public_templates %}
            <div class="template-grid">
                {% for template in public_templates %}
                <div class="template-card">
                    <h3>{{ template.title }}</h3>
                    <p class="template-meta">
                        <span class="badge">{{ template.subject|title }}</span>
                        <span class="badge-outline">Grade {{ template.grade_level }}</span>
                        {% if template.is_featured %}
                        <span class="badge-featured">⭐ Featured</span>
                        {% endif %}
                    </p>
                    <p>{{ template.description[:100] }}...</p>
                    <p class="template-stats">Used {{ template.use_count }} times by teachers</p>

                    <div class="template-actions">
                        <form method="post" action="/duplicate-template/{{ template.id }}">
                            <button type="submit" class="btn-primary">📋 Use Template</button>
                        </form>
                    </div>
                </div>
                {% endfor %}
            </div>
            {% else %}
            <p class="empty-state">No public templates available yet.</p>
            {% endif %}
        </section>

        <div class="template-actions-footer">
            <a href="{{ route_prefix }}/dashboard" class="btn-secondary">← Back to Dashboard</a>
        </div>
    </div>

    <style>
        .template-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }

        .template-card {
            background: white;
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }

        .template-card h3 {
            margin: 0 0 10px 0;
            color: #333;
        }

        .template-meta {
            margin: 10px 0;
        }

        .badge {
            background: #667eea;
            color: white;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 12px;
            margin-right: 8px;
        }

        .badge-outline {
            border: 1px solid #667eea;
            color: #667eea;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 12px;
        }

        .badge-featured {
            background: gold;
            color: #333;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: bold;
        }

        .template-stats {
            color: #666;
            font-size: 14px;
            margin: 10px 0;
        }

        .template-actions {
            margin-top: 15px;
            display: flex;
            gap: 10px;
        }

        .empty-state {
            text-align: center;
            padding: 40px;
            color: #666;
            font-style: italic;
        }

        .template-filters {
            background: #f5f5f5;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 30px;
        }

        .template-filters form {
            display: flex;
            gap: 10px;
            align-items: center;
        }

        .template-filters input[type="text"] {
            flex: 1;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
        }

        .template-filters select {
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
        }
    </style>
</body>
</html>
```

### Integration with Assignment Creation

Modify your existing `/teacher/assignments/create` and `/homeschool/assignments/create` routes:

```python
# In assignment creation routes, add:

# Check if creating from template
from_template = request.args.get("from_template") == "true"

if from_template and "template_data" in session:
    template_data = session.pop("template_data")
    template_title = session.pop("template_title", "New Assignment")
    template_subject = session.pop("template_subject", "")

    # Pre-fill form with template data
    prefilled_data = {
        "title": f"Copy of {template_title}",
        "subject": template_subject,
        "instructions": template_data.get("instructions", ""),
        "differentiation_mode": template_data.get("differentiation_mode", "none"),
        "question_count": template_data.get("question_count", 10)
    }

    return render_template("create_assignment.html", prefilled=prefilled_data)
```

### Add "Save as Template" Button

In your assignment creation/edit forms, add:

```html
<!-- After creating an assignment successfully -->
<div class="post-creation-actions">
    <h3>Assignment Created!</h3>
    <p>Would you like to save this as a template for future use?</p>

    <form method="post" action="/save-assignment-template">
        <input type="hidden" name="assignment_id" value="{{ assignment.id }}">

        <div class="form-group">
            <label>Template Name:</label>
            <input type="text" name="title" value="{{ assignment.title }} Template" required>
        </div>

        <div class="form-group">
            <label>Description (optional):</label>
            <textarea name="description" placeholder="What is this template for?"></textarea>
        </div>

        <div class="form-group">
            <label>
                <input type="checkbox" name="is_public">
                Share with other teachers/homeschool parents
            </label>
        </div>

        <div class="form-group">
            <label>Tags (comma-separated):</label>
            <input type="text" name="tags" placeholder="multiplication, grade3, visual">
        </div>

        <button type="submit" class="btn-primary">💾 Save as Template</button>
        <a href="/teacher/templates" class="btn-secondary">Skip</a>
    </form>
</div>
```

---

## Feature 2: Quick Grade Entry (Spreadsheet Style) ⭐⭐⭐⭐⭐

**Impact:** 2x faster grading
**Effort:** 2-3 days
**Works For:** Teachers AND Homeschool Parents

### Route to Add

```python
@app.route("/teacher/assignments/<int:assignment_id>/quick-grade")
@app.route("/homeschool/assignments/<int:assignment_id>/quick-grade")
def quick_grade_assignment(assignment_id):
    """
    Spreadsheet-style quick grade entry.
    Type grades directly into grid, tab through boxes.
    """
    user_role = session.get("user_role")

    # TODO: Fetch assignment and all submissions
    # assignment = Assignment.query.get_or_404(assignment_id)
    # submissions = Submission.query.filter_by(assignment_id=assignment_id).all()

    # For now, placeholder data
    students = [
        {"id": 1, "name": "Alice Johnson", "current_score": 85},
        {"id": 2, "name": "Bob Smith", "current_score": None},
        {"id": 3, "name": "Charlie Brown", "current_score": 92},
    ]

    return render_template(
        "quick_grade.html",
        assignment_id=assignment_id,
        students=students,
        route_prefix="/teacher" if user_role == "teacher" else "/homeschool"
    )


@app.route("/save-quick-grades", methods=["POST"])
def save_quick_grades():
    """
    Save all grades from quick grade entry at once.
    """
    assignment_id = request.form.get("assignment_id")

    # Get all grade inputs (format: grade_<student_id>)
    grades = {}
    for key, value in request.form.items():
        if key.startswith("grade_"):
            student_id = key.replace("grade_", "")
            if value.strip():  # Only save if grade entered
                grades[student_id] = float(value)

    # TODO: Save grades to database
    # for student_id, score in grades.items():
    #     submission = Submission.query.filter_by(
    #         assignment_id=assignment_id,
    #         student_id=student_id
    #     ).first()
    #     if submission:
    #         submission.score = score
    #         submission.status = "graded"

    # db.session.commit()

    flash(f"✅ Saved grades for {len(grades)} students!", "success")
    return redirect(f"/teacher/assignments/{assignment_id}/submissions")
```

### UI Template: quick_grade.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Quick Grade Entry</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    <div class="container">
        <h1>⚡ Quick Grade Entry</h1>
        <p>Enter grades quickly using Tab to move between students</p>

        <form method="post" action="/save-quick-grades" id="quickGradeForm">
            <input type="hidden" name="assignment_id" value="{{ assignment_id }}">

            <table class="grade-table">
                <thead>
                    <tr>
                        <th>Student Name</th>
                        <th>Grade (0-100)</th>
                        <th>Quick Feedback</th>
                        <th>Current</th>
                    </tr>
                </thead>
                <tbody>
                    {% for student in students %}
                    <tr>
                        <td>{{ student.name }}</td>
                        <td>
                            <input
                                type="number"
                                name="grade_{{ student.id }}"
                                class="grade-input"
                                min="0"
                                max="100"
                                step="0.5"
                                value="{{ student.current_score or '' }}"
                                placeholder="--"
                                autofocus="{{ loop.first }}"
                            >
                        </td>
                        <td>
                            <select name="feedback_{{ student.id }}" class="feedback-select">
                                <option value="">--</option>
                                <option value="excellent">✅ Excellent!</option>
                                <option value="good">👍 Good work</option>
                                <option value="needs_improvement">📝 Needs improvement</option>
                                <option value="incomplete">⚠️ Incomplete</option>
                            </select>
                        </td>
                        <td class="current-score">
                            {% if student.current_score %}
                                {{ student.current_score }}%
                            {% else %}
                                <span class="not-graded">Not graded</span>
                            {% endif %}
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>

            <div class="grade-summary">
                <p>Class Average: <strong id="classAverage">--</strong></p>
                <p>Graded: <strong id="gradedCount">0</strong> / {{ students|length }}</p>
            </div>

            <div class="form-actions">
                <button type="submit" class="btn-primary">💾 Save All Grades</button>
                <a href="{{ route_prefix }}/assignments/{{ assignment_id }}/submissions" class="btn-secondary">Cancel</a>
            </div>
        </form>
    </div>

    <style>
        .grade-table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }

        .grade-table th {
            background: #667eea;
            color: white;
            padding: 12px;
            text-align: left;
        }

        .grade-table td {
            padding: 10px;
            border-bottom: 1px solid #ddd;
        }

        .grade-input {
            width: 80px;
            padding: 8px;
            font-size: 16px;
            text-align: center;
            border: 2px solid #ddd;
            border-radius: 4px;
        }

        .grade-input:focus {
            border-color: #667eea;
            outline: none;
            background: #f0f4ff;
        }

        .feedback-select {
            padding: 8px;
            border: 1px solid #ddd;
            border-radius: 4px;
        }

        .current-score {
            color: #666;
            font-weight: bold;
        }

        .not-graded {
            color: #999;
            font-style: italic;
        }

        .grade-summary {
            background: #f5f5f5;
            padding: 15px;
            border-radius: 8px;
            margin: 20px 0;
            display: flex;
            gap: 30px;
        }

        .form-actions {
            margin-top: 20px;
            display: flex;
            gap: 10px;
        }
    </style>

    <script>
        // Auto-calculate class average as grades are entered
        document.querySelectorAll('.grade-input').forEach(input => {
            input.addEventListener('input', calculateAverage);
        });

        function calculateAverage() {
            const inputs = document.querySelectorAll('.grade-input');
            let total = 0;
            let count = 0;

            inputs.forEach(input => {
                if (input.value.trim()) {
                    total += parseFloat(input.value);
                    count++;
                }
            });

            const average = count > 0 ? (total / count).toFixed(1) : '--';
            document.getElementById('classAverage').textContent = average + (count > 0 ? '%' : '');
            document.getElementById('gradedCount').textContent = count;
        }

        // Initial calculation
        calculateAverage();

        // Enable Tab navigation through inputs
        document.getElementById('quickGradeForm').addEventListener('keydown', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                const inputs = Array.from(document.querySelectorAll('.grade-input'));
                const current = document.activeElement;
                const currentIndex = inputs.indexOf(current);
                if (currentIndex < inputs.length - 1) {
                    inputs[currentIndex + 1].focus();
                }
            }
        });
    </script>
</body>
</html>
```

---

## ⏭️ Next Features to Implement

Due to response length limits, I've created detailed specs for the top 2 shared features. The remaining features would follow similar patterns:

3. **Missing Assignment Alerts** - Cron job + email notifications
4. **Resource Library** - File upload + S3 storage + sharing
5. **Bulk Email (Teacher-Only)** - Email composition + parent list
6. **Automated Reports (Teacher-Only)** - Scheduled emails + analytics

---

## 🚀 Implementation Order

1. **Week 1:** Assignment Template Library (this provides immediate value)
2. **Week 2:** Quick Grade Entry (teachers will love this)
3. **Week 3:** Missing Assignment Alerts (automated engagement)
4. **Week 4:** Resource Library (file sharing capability)

---

**Ready to implement? Start with Feature 1 (Assignment Templates) as it's the easiest and provides immediate time savings!**

Generated by Claude Code - December 2025
