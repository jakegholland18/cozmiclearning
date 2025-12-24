# 🧠 Learning Lab Integration Guide

## How Students Use Their Learning Strategies Throughout CozmicLearning

###  What We Just Built

The Learning Lab is now **deeply integrated** into the student experience. Instead of being a standalone feature, it provides **contextual, personalized support** wherever students are learning.

---

## 🎯 Integration Points

### 1. **PowerGrid Study Guides** ✅ LIVE (Dec 24, 2025)

When students generate a PowerGrid study guide, they now see:

**For Students WITH a Learning Profile:**
- Personalized tips banner at the top of the study guide
- Tips customized to their learning style (visual, auditory, kinesthetic, reading/writing)
- Quick links to relevant tools (Pomodoro timer, text-to-speech, task breakdown)
- Context-aware suggestions (e.g., "Study one section at a time with 5-minute breaks")

**Example for Visual Learners:**
```
💡 Tips for Visual Learners
✓ Pay special attention to diagrams and visual explanations
✓ Highlight key concepts in different colors

Helpful Tools: 🔊 Text-to-Speech | ⏰ Focus Timer
```

**For Students WITHOUT a Profile:**
- Friendly CTA banner encouraging them to take the quiz
- "Discover your learning superpowers!" message
- Direct link to Learning Lab quiz

---

### 2. **Student Dashboard** ✅ LIVE (Dec 24, 2025)

The dashboard now displays a Learning Toolkit widget in the main content area:

**For Students WITH a Learning Profile:**
- Learning style badge with icon and name
- First strength from their profile highlighted
- Top 3 most-used learning tools (or recommended tools if new)
- Quick links to Learning Lab main page and strategies
- Persistent reminder of their learning superpowers

**For Students WITHOUT a Profile:**
- Prominent CTA to take the quiz
- "Unlock your learning superpowers!" message
- Direct link to start the quiz

**Implementation:**
- Route: [app.py:14443-14474](app.py#L14443-L14474) - Dashboard route with toolkit widget
- Template: [dashboard.html:547-642](website/templates/dashboard.html#L547-L642) - Widget display
- Helper: `get_learning_toolkit_widget(student_id)` from learning_lab_helper.py

---

### 3. **Assignment Pages** ✅ LIVE (Dec 24, 2025)

All assignment types now show personalized learning tips:

**Supported Assignment Types:**
- ✅ Hybrid Adaptive (MC + Free Response)
- ✅ Scaffold (Progressive hints)
- ✅ Adaptive (Difficulty-based routing)
- ✅ Gap Fill (Diagnostic + targeted practice)
- ✅ Mastery (Tiered progression)
- ✅ Standard (All questions at once)

**Context-Aware Tips for Assignments:**
- Task breakdown suggestions for step-by-step learners
- Movement break reminders for kinesthetic learners
- Time management tips based on their patterns
- Focus duration recommendations
- Tool suggestions (task breakdown, Pomodoro timer)

**Implementation:**
- Route: [app.py:7176-7178](app.py#L7176-L7178) - Learning tips in student_start_assignment()
- Templates:
  - [student_take_assignment.html:287-318](website/templates/student_take_assignment.html#L287-L318) - Tips banner
  - [student_take_assignment_sequential.html:333-364](website/templates/student_take_assignment_sequential.html#L333-L364) - Tips banner
- Helper: `get_contextual_learning_tips(student_id, context='assignment')`

---

### 4. **Practice Sessions** ✅ LIVE (Dec 24, 2025)

Practice/quiz pages now include learning strategy support:

**Supported Practice Modes:**
- ✅ Interactive Practice
- ✅ Quick Quiz
- ✅ Full Practice
- ✅ Timed Challenge
- ✅ Teach Me More
- ✅ Related Topics

**Context-Aware Tips for Practice:**
- Break frequency reminders based on profile
- Focus duration suggestions
- Drawing/visualization tips for visual learners
- Audio support suggestions for auditory learners
- Movement break timing for kinesthetic learners
- Tool recommendations (Pomodoro timer, break reminders)

**Implementation:**
- Route: [app.py:13642-13645](app.py#L13642-L13645) - Learning tips in practice() route
- Template: [practice.html:669-700](website/templates/practice.html#L669-L700) - Tips banner
- Helper: `get_contextual_learning_tips(student_id, context='practice')`

---

## 🔧 How It Works Behind the Scenes

### Context-Aware Recommendations

The system uses `get_contextual_learning_tips(student_id, context)` to provide smart suggestions:

**Contexts:**
- `'powergrid'` - Study guide reading tips
- `'assignment'` - Homework/task tips
- `'test_prep'` - Test preparation strategies
- `'practice'` - Quiz/practice tips
- `'general'` - Dashboard and other pages

**What It Considers:**
1. **Learning Style** - Visual, auditory, kinesthetic, reading/writing
2. **Focus Preference** - Short bursts vs. long sessions
3. **Processing Style** - Step-by-step vs. big picture
4. **Time of Day** - Matches optimal study time from profile
5. **Break Frequency** - Movement needs and break patterns

### Example: PowerGrid for Short-Burst Learner

```python
# Student profile: focus_preference = 'short_bursts'
tips = get_contextual_learning_tips(student_id, 'powergrid')

# Returns:
{
    'tips': [
        "Study one section at a time with 5-minute breaks"
    ],
    'tools': [
        {'name': 'Pomodoro Timer', 'icon': '⏰', 'link': '/learning-lab/tools#pomodoro'}
    ]
}
```

---

## 📋 Ready-to-Use Helper Functions

### 1. `get_contextual_learning_tips(student_id, context)`

**Use this to:** Add personalized tips to any page

**Example - Assignment Page:**
```python
@app.route("/assignment/<int:id>")
def view_assignment(id):
    student_id = session.get('student_id')
    learning_tips = get_contextual_learning_tips(student_id, context='assignment')

    return render_template('assignment.html',
                         assignment=assignment,
                         learning_tips=learning_tips)
```

**In Template:**
```html
{% if learning_tips and learning_tips.has_profile %}
    <div class="tips-box">
        {% for tip in learning_tips.tips %}
            <p>💡 {{ tip }}</p>
        {% endfor %}
        {% for tool in learning_tips.tools %}
            <a href="{{ tool.link }}">{{ tool.icon }} {{ tool.name }}</a>
        {% endfor %}
    </div>
{% endif %}
```

### 2. `adapt_content_to_learning_style(content, learning_style)`

**Use this to:** Add learning-style-specific tips to generated content

**Example - Enhance AI-Generated Content:**
```python
study_guide = generate_study_guide(topic)  # AI generates content

# Get student's learning style
profile = LearningProfile.query.filter_by(student_id=student_id).first()
if profile:
    study_guide = adapt_content_to_learning_style(study_guide, profile.primary_learning_style)
```

**What It Adds:**
- **Visual learners:** "Try sketching a diagram of these concepts"
- **Auditory learners:** "Read this aloud or use text-to-speech"
- **Kinesthetic learners:** "Take a 2-minute movement break every 15 minutes"
- **Reading/writing learners:** "Take detailed notes as you read"

### 3. `get_learning_toolkit_widget(student_id)`

**Use this to:** Add a persistent "My Learning Tools" widget

**Example - Dashboard Sidebar:**
```python
@app.route("/dashboard")
def dashboard():
    student_id = session.get('student_id')
    from modules.learning_lab_helper import get_learning_toolkit_widget
    toolkit_widget = get_learning_toolkit_widget(student_id)

    return render_template('dashboard.html', toolkit_widget=toolkit_widget)
```

**In Template:**
```html
{{ toolkit_widget|safe }}
```

**What Students See:**
- Their learning style icon and name
- Top 3 most-used tools (or recommended tools if new)
- Quick links to Learning Lab
- "Discover your superpowers" CTA if no profile

---

## 🚀 Next Steps - Where to Integrate

### High Priority (Big Impact)

**1. Student Dashboard**
Add toolkit widget to sidebar showing:
- Learning style badge
- Quick tool access
- Most-used strategies

**2. Assignment View Page**
Show context-aware tips when viewing assigned work:
- Task breakdown suggestions for step-by-step learners
- Movement break reminders for kinesthetic learners
- Time management tips based on their patterns

**3. Practice/Quiz Pages**
During practice sessions:
- Break frequency reminders
- Drawing/visualization tips for visual learners
- Audio support suggestions for auditory learners

### Medium Priority (Good UX)

**4. Subject Explorer**
When choosing what to learn:
- Suggest learning approaches based on style
- Recommend relevant PowerGrid modes

**5. Arcade/Games**
Match game types to learning preferences:
- Visual learners → Memory cards with images
- Kinesthetic learners → Interactive drag-and-drop
- Auditory learners → Sound-based games

### Low Priority (Nice to Have)

**6. Progress/Analytics Pages**
Show correlation between:
- Strategy usage and performance
- Study time patterns and optimal times
- Tool adoption and engagement

---

## 💡 Implementation Template

Here's a copy-paste template for adding tips to any page:

```python
# In your route (app.py):
from modules.learning_lab_helper import get_contextual_learning_tips

@app.route("/your-page")
def your_page():
    init_user()
    student_id = session.get('student_id')

    # Choose context: 'assignment', 'powergrid', 'test_prep', 'practice', 'general'
    learning_tips = get_contextual_learning_tips(student_id, context='general') if student_id else None

    return render_template('your_template.html',
                         learning_tips=learning_tips,
                         # ... other variables
                         )
```

```html
<!-- In your template: -->
{% if learning_tips and learning_tips.has_profile %}
<div style="background: rgba(132,255,0,0.1); border: 1px solid rgba(132,255,0,0.3); border-radius: 12px; padding: 15px; margin: 15px 0;">
    <div style="font-weight: 700; color: #84ff00; margin-bottom: 10px;">
        💡 Tips for {{ learning_tips.primary_style }} Learners
    </div>
    {% for tip in learning_tips.tips %}
        <div style="color: #c4d1ff; margin: 8px 0;">✓ {{ tip }}</div>
    {% endfor %}
    {% if learning_tips.tools %}
        <div style="margin-top: 12px;">
            {% for tool in learning_tips.tools %}
                <a href="{{ tool.link }}" style="display: inline-block; padding: 6px 12px; background: rgba(0,242,255,0.2); border-radius: 16px; color: #00f2ff; text-decoration: none; margin-right: 8px;">
                    {{ tool.icon }} {{ tool.name }}
                </a>
            {% endfor %}
        </div>
    {% endif %}
</div>
{% elif learning_tips and not learning_tips.has_profile %}
<div style="background: rgba(102,126,234,0.1); border: 1px solid rgba(102,126,234,0.3); border-radius: 12px; padding: 15px; margin: 15px 0; text-align: center;">
    <span style="font-size: 1.3rem;">🧠</span>
    <span style="color: #c4d1ff;">{{ learning_tips.cta }}</span>
    <a href="{{ learning_tips.cta_link }}" style="display: inline-block; margin-left: 12px; padding: 8px 20px; background: linear-gradient(135deg, #667eea, #764ba2); color: white; border-radius: 20px; text-decoration: none; font-weight: 600;">
        Get Started →
    </a>
</div>
{% endif %}
```

---

## 📊 Strategy Tracking

When students click "I'll try this!" on the strategies page:

**What Happens:**
1. **Backend** - Creates/updates `StrategyUsage` record
2. **Database** - Tracks times_used, last_used_at, helpfulness_rating
3. **Profile** - Updates most-used strategies list
4. **Widget** - Shows top 3 tools in toolkit widget

**Current Implementation:**
- ✅ Tracking endpoint: `/learning-lab/strategies/<key>/use`
- ✅ Rating endpoint: `/learning-lab/strategies/<key>/rate`
- ✅ Database table: `strategy_usage`
- ✅ User feedback: "Great! Strategy tracked"

**Future Enhancement:**
Make it more actionable:
- Instead of just "Strategy tracked", open the tool directly
- Auto-add to student's favorites
- Show progress badges ("You've used this 5 times!")

---

## 🎨 Design Consistency

All Learning Lab elements use the **Cosmic Gradient Theme**:

**Colors:**
- Primary: `#667eea` (Purple)
- Accent: `#764ba2` (Deep purple)
- Secondary: `#f093fb` (Pink)
- Tertiary: `#f5576c` (Coral)
- Success: `#84ff00` (Electric green)
- Info: `#00f2ff` (Cyan)

**Glassmorphism:**
- `backdrop-filter: blur(10px)`
- Semi-transparent backgrounds
- Soft shadows with glow effects

---

## ✅ What's Live Now

- ✅ **PowerGrid study guides** - Personalized learning tips banner at top of study guides
- ✅ **Dashboard** - Learning toolkit widget showing learning style and quick tool access
- ✅ **Assignment pages** - Context-aware tips for all assignment types (adaptive, scaffold, mastery, standard)
- ✅ **Practice sessions** - Break frequency reminders and practice strategies for all practice modes
- ✅ Tips adapt to visual/auditory/kinesthetic/reading-writing styles
- ✅ Tool recommendations based on focus preferences (Pomodoro timer, text-to-speech, task breakdown)
- ✅ Time-of-day awareness (morning vs. night learners)
- ✅ CTA for students without profiles (encourages Learning Lab quiz completion)
- ✅ Helper functions ready for additional pages

## 🔜 Ready to Integrate Next

- Subject explorer recommendations
- Arcade/game pages with learning style matching
- Progress/analytics correlation displays

---

## 📖 For More Info

### Documentation
- **Full deployment docs:** [LEARNING_LAB_DEPLOYMENT.md](LEARNING_LAB_DEPLOYMENT.md)
- **Helper module:** [modules/learning_lab_helper.py](modules/learning_lab_helper.py)
- **Database models:** [models.py](models.py) (LearningProfile, StrategyUsage)

### Live Integrations
- **PowerGrid:** [app.py:13400-13415](app.py#L13400-L13415) | [powergrid.html:782-813](website/templates/powergrid.html#L782-L813)
- **Dashboard:** [app.py:14443-14474](app.py#L14443-L14474) | [dashboard.html:547-642](website/templates/dashboard.html#L547-L642)
- **Assignments:** [app.py:7176-7178](app.py#L7176-L7178) | [student_take_assignment.html:287-318](website/templates/student_take_assignment.html#L287-L318)
- **Practice:** [app.py:13642-13645](app.py#L13642-L13645) | [practice.html:669-700](website/templates/practice.html#L669-L700)

---

**Built:** December 24, 2025
**Last Updated:** December 24, 2025
**Status:** ✅ Live and Growing
**Coverage:** 4 major student-facing features (PowerGrid, Dashboard, Assignments, Practice)
**Impact:** Students now get personalized learning support throughout their entire CozmicLearning experience!
