# 🛠️ Interactive Learning Tools - Quick Implementation Guide

## Overview

This guide provides the code you need to implement all 5 interactive learning tools. Due to the scope, I'm providing:
- Complete database models
- Key backend routes
- Essential frontend code snippets
- Instructions for OpenAI API integration

---

## 📦 Step 1: Database Models

Add these to `models.py`:

```python
class PomodoroSession(db.Model):
    """Tracks Pomodoro timer sessions"""
    __tablename__ = 'pomodoro_session'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    session_date = db.Column(db.DateTime, default=datetime.utcnow)
    work_duration = db.Column(db.Integer)  # minutes completed
    break_duration = db.Column(db.Integer)  # minutes
    completed = db.Column(db.Boolean, default=False)
    focus_rating = db.Column(db.Integer, nullable=True)  # 1-5

    student = db.relationship('Student', backref='pomodoro_sessions')


class StudyBuddyMessage(db.Model):
    """Stores AI Study Buddy conversations"""
    __tablename__ = 'study_buddy_message'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    is_student = db.Column(db.Boolean, nullable=False)  # True = student, False = AI
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    topic = db.Column(db.String(100), nullable=True)
    learning_style_used = db.Column(db.String(50), nullable=True)  # Which style AI used

    student = db.relationship('Student', backref='study_buddy_messages')


class TaskBreakdown(db.Model):
    """AI-generated task breakdowns"""
    __tablename__ = 'task_breakdown'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed = db.Column(db.Boolean, default=False)

    student = db.relationship('Student', backref='task_breakdowns')
    steps = db.relationship('TaskStep', backref='breakdown', cascade='all, delete-orphan')


class TaskStep(db.Model):
    """Individual steps in a task breakdown"""
    __tablename__ = 'task_step'

    id = db.Column(db.Integer, primary_key=True)
    breakdown_id = db.Column(db.Integer, db.ForeignKey('task_breakdown.id'), nullable=False)
    step_number = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)
    estimated_minutes = db.Column(db.Integer, nullable=True)
    completed = db.Column(db.Boolean, default=False)
    completed_at = db.Column(db.DateTime, nullable=True)


class AIAssignment(db.Model):
    """AI-generated multi-modal assignments for teachers"""
    __tablename__ = 'ai_assignment'

    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'), nullable=False)
    topic = db.Column(db.String(200), nullable=False)
    grade_level = db.Column(db.String(20))
    objectives = db.Column(db.Text)
    generated_content = db.Column(db.JSON)  # All 4 learning style versions
    rubric = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    teacher = db.relationship('Teacher', backref='ai_assignments')
```

**Migration command:**
```bash
# After adding models to models.py
python3
>>> from app import db
>>> db.create_all()
>>> exit()
```

---

## 🎯 Step 2: Environment Variables

Add to `.env`:
```bash
# OpenAI API (required for AI features)
OPENAI_API_KEY=sk-your-key-here

# Optional: Use GPT-3.5 for cost savings
OPENAI_MODEL=gpt-4  # or gpt-3.5-turbo
```

---

## 🔧 Step 3: Backend Routes

### Pomodoro Timer Routes

Add to `app.py`:

```python
@app.route("/learning-lab/pomodoro/start", methods=["POST"])
def pomodoro_start():
    """Start a new Pomodoro session"""
    init_user()
    student_id = session.get('student_id')
    if not student_id:
        return jsonify({'error': 'Unauthorized'}), 403

    work_duration = request.json.get('work_duration', 25)

    # Create new session
    pomodoro = PomodoroSession(
        student_id=student_id,
        work_duration=work_duration,
        completed=False
    )
    db.session.add(pomodoro)
    db.session.commit()

    return jsonify({
        'success': True,
        'session_id': pomodoro.id
    })


@app.route("/learning-lab/pomodoro/complete", methods=["POST"])
def pomodoro_complete():
    """Mark Pomodoro session as complete"""
    init_user()
    student_id = session.get('student_id')
    if not student_id:
        return jsonify({'error': 'Unauthorized'}), 403

    session_id = request.json.get('session_id')
    focus_rating = request.json.get('focus_rating')

    pomodoro = PomodoroSession.query.get(session_id)
    if pomodoro and pomodoro.student_id == student_id:
        pomodoro.completed = True
        pomodoro.focus_rating = focus_rating
        db.session.commit()

        return jsonify({'success': True})

    return jsonify({'error': 'Session not found'}), 404


@app.route("/learning-lab/pomodoro/stats")
def pomodoro_stats():
    """Get Pomodoro statistics"""
    init_user()
    student_id = session.get('student_id')
    if not student_id:
        return redirect('/student/login')

    # Last 7 days
    from datetime import timedelta
    week_ago = datetime.utcnow() - timedelta(days=7)

    sessions = PomodoroSession.query.filter(
        PomodoroSession.student_id == student_id,
        PomodoroSession.session_date >= week_ago,
        PomodoroSession.completed == True
    ).all()

    total_sessions = len(sessions)
    total_minutes = sum(s.work_duration for s in sessions if s.work_duration)
    avg_focus = sum(s.focus_rating for s in sessions if s.focus_rating) / total_sessions if total_sessions > 0 else 0

    return jsonify({
        'total_sessions': total_sessions,
        'total_minutes': total_minutes,
        'average_focus': round(avg_focus, 1),
        'sessions_today': len([s for s in sessions if s.session_date.date() == datetime.utcnow().date()])
    })
```

### Study Buddy AI Routes

```python
import openai
import os

openai.api_key = os.getenv('OPENAI_API_KEY')

@app.route("/learning-lab/study-buddy", methods=["GET"])
def study_buddy():
    """Study Buddy AI chat interface"""
    init_user()
    student_id = session.get('student_id')
    if not student_id:
        flash("Learning Lab is for students only", "error")
        return redirect(url_for('dashboard'))

    student = Student.query.get(student_id)
    profile = LearningProfile.query.filter_by(student_id=student_id).first()

    # Get recent messages
    messages = StudyBuddyMessage.query.filter_by(
        student_id=student_id
    ).order_by(StudyBuddyMessage.timestamp.desc()).limit(50).all()
    messages.reverse()  # Show oldest first

    return render_template('study_buddy.html',
                         student=student,
                         profile=profile,
                         messages=messages)


@app.route("/learning-lab/study-buddy/send", methods=["POST"])
def study_buddy_send():
    """Send message to Study Buddy AI"""
    init_user()
    student_id = session.get('student_id')
    if not student_id:
        return jsonify({'error': 'Unauthorized'}), 403

    user_message = request.json.get('message', '').strip()
    if not user_message:
        return jsonify({'error': 'Empty message'}), 400

    # Get student profile for personalization
    profile = LearningProfile.query.filter_by(student_id=student_id).first()
    learning_style = profile.primary_learning_style if profile else 'reading_writing'

    # Save student message
    student_msg = StudyBuddyMessage(
        student_id=student_id,
        message=user_message,
        is_student=True
    )
    db.session.add(student_msg)
    db.session.commit()

    # Get conversation history
    recent_messages = StudyBuddyMessage.query.filter_by(
        student_id=student_id
    ).order_by(StudyBuddyMessage.timestamp.desc()).limit(10).all()
    recent_messages.reverse()

    # Build context for AI
    conversation_history = []
    for msg in recent_messages:
        role = "user" if msg.is_student else "assistant"
        conversation_history.append({
            "role": role,
            "content": msg.message
        })

    # System prompt based on learning style
    system_prompts = {
        'visual': "You are a helpful study buddy AI. When explaining concepts, prioritize visual descriptions, suggest creating diagrams, and use spatial language. Encourage the student to draw or visualize concepts.",
        'auditory': "You are a helpful study buddy AI. When explaining concepts, use verbal explanations, suggest reading aloud, and use sound/rhythm analogies. Encourage discussion and talking through problems.",
        'kinesthetic': "You are a helpful study buddy AI. When explaining concepts, suggest hands-on activities, use movement metaphors, and encourage physical demonstrations. Recommend building or acting out concepts.",
        'reading_writing': "You are a helpful study buddy AI. When explaining concepts, provide detailed text explanations, suggest taking notes, and encourage written summaries. Use organized lists and outlines."
    }

    system_prompt = system_prompts.get(learning_style, system_prompts['reading_writing'])
    system_prompt += "\n\nIMPORTANT: Never give direct answers to homework. Use the Socratic method - ask questions that guide the student to discover the answer themselves. Be encouraging and supportive."

    try:
        # Call OpenAI API
        response = openai.ChatCompletion.create(
            model=os.getenv('OPENAI_MODEL', 'gpt-4'),
            messages=[
                {"role": "system", "content": system_prompt},
                *conversation_history
            ],
            max_tokens=300,
            temperature=0.7
        )

        ai_message = response.choices[0].message.content

        # Save AI response
        ai_msg = StudyBuddyMessage(
            student_id=student_id,
            message=ai_message,
            is_student=False,
            learning_style_used=learning_style
        )
        db.session.add(ai_msg)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': ai_message
        })

    except Exception as e:
        print(f"OpenAI API error: {e}")
        return jsonify({
            'error': 'Sorry, I encountered an error. Please try again.',
            'details': str(e)
        }), 500
```

### Task Breakdown Routes

```python
@app.route("/learning-lab/task-breakdown/create", methods=["POST"])
def create_task_breakdown():
    """Create AI-powered task breakdown"""
    init_user()
    student_id = session.get('student_id')
    if not student_id:
        return jsonify({'error': 'Unauthorized'}), 403

    title = request.json.get('title', '')
    description = request.json.get('description', '')

    # Get student profile
    profile = LearningProfile.query.filter_by(student_id=student_id).first()

    # Create breakdown
    breakdown = TaskBreakdown(
        student_id=student_id,
        title=title,
        description=description
    )
    db.session.add(breakdown)
    db.session.flush()  # Get ID

    try:
        # Use AI to generate steps
        focus_pref = profile.focus_preference if profile else 'medium_sessions'
        step_size = "15-20 minutes" if focus_pref == 'short_bursts' else "30-45 minutes" if focus_pref == 'medium_sessions' else "60+ minutes"

        prompt = f"""Break down this assignment into manageable steps for a student:

Assignment: {title}
Description: {description}

Student prefers working in {step_size} chunks.

Provide 5-8 steps with estimated time for each. Format as JSON:
[
  {{"step": 1, "description": "...", "minutes": 20}},
  ...
]"""

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500
        )

        steps_json = json.loads(response.choices[0].message.content)

        # Create steps
        for step_data in steps_json:
            step = TaskStep(
                breakdown_id=breakdown.id,
                step_number=step_data['step'],
                description=step_data['description'],
                estimated_minutes=step_data.get('minutes', 30)
            )
            db.session.add(step)

        db.session.commit()

        return jsonify({
            'success': True,
            'breakdown_id': breakdown.id,
            'steps': steps_json
        })

    except Exception as e:
        db.session.rollback()
        print(f"Task breakdown error: {e}")
        return jsonify({'error': str(e)}), 500
```

---

## 🎨 Step 4: Frontend Templates

Due to length, here's the structure. I recommend creating separate template files:

### 1. `study_buddy.html` - AI Chat Interface
Key features:
- Chat message display
- Input box with send button
- Voice input option
- Learning style indicator

### 2. Enhanced `learning_tools.html`
Add interactive sections for each tool with JavaScript

### 3. `ai_assignment_generator.html` (for teachers)
Form to input topic, objectives, grade level
Display 4 learning-style variations

---

## ⚙️ Step 5: JavaScript for Interactive Tools

### Pomodoro Timer

```javascript
class PomodoroTimer {
    constructor() {
        this.workMinutes = 25;
        this.breakMinutes = 5;
        this.isWorking = true;
        this.isPaused = false;
        this.timeRemaining = this.workMinutes * 60;
        this.sessionId = null;
    }

    async start() {
        // Start session on server
        const response = await fetch('/learning-lab/pomodoro/start', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({work_duration: this.workMinutes})
        });

        const data = await response.json();
        this.sessionId = data.session_id;

        this.tick();
    }

    tick() {
        if (this.isPaused) return;

        this.timeRemaining--;
        this.updateDisplay();

        if (this.timeRemaining <= 0) {
            this.complete();
        } else {
            setTimeout(() => this.tick(), 1000);
        }
    }

    updateDisplay() {
        const minutes = Math.floor(this.timeRemaining / 60);
        const seconds = this.timeRemaining % 60;
        document.getElementById('timer-display').textContent =
            `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    }

    async complete() {
        // Play sound
        new Audio('/static/sounds/bell.mp3').play();

        if (this.isWorking) {
            alert('Time for a break! 🎉');

            // Ask for focus rating
            const rating = prompt('How focused were you? (1-5)');

            await fetch('/learning-lab/pomodoro/complete', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    session_id: this.sessionId,
                    focus_rating: parseInt(rating)
                })
            });

            // Switch to break
            this.isWorking = false;
            this.timeRemaining = this.breakMinutes * 60;
            this.tick();
        } else {
            alert('Break over! Back to work. 💪');
            this.isWorking = true;
            this.start();
        }
    }
}

// Initialize
const timer = new PomodoroTimer();
```

---

## 📊 Next Steps

1. **Add models to `models.py`**
2. **Run database migration**
3. **Add routes to `app.py`**
4. **Create frontend templates**
5. **Test each feature**
6. **Add OpenAI API key for AI features**

---

## 💰 Cost Management

With OpenAI API:
- Study Buddy: ~$0.05 per conversation
- Task Breakdown: ~$0.02 per breakdown
- Assignment Generator: ~$0.10 per assignment

For 100 daily active students: ~$5-10/day

**Optimization:**
- Use GPT-3.5-turbo for simple tasks
- Cache common responses
- Rate limit per student (5 AI calls per hour)

---

## 🔐 Safety

- Content filtering via OpenAI moderation API
- Age-appropriate responses
- Parent controls for AI access
- Conversation history auto-delete after 90 days

---

Ready to implement! Start with database models, then routes, then frontend.
