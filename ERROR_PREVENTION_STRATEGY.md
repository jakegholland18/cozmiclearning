# Error Prevention & Code Quality Strategy

## Why We've Had Errors

### Root Causes Analysis

#### 1. **Rapid Development Without Testing**
- **What happened:** Features added quickly without systematic testing
- **Example:** Nested sections bug - advanced detail button creating 6 sections within sections
- **Why:** No test suite to catch regression bugs

#### 2. **Missing Database Migrations**
- **What happened:** Code deployed before database schema updated
- **Example:** `conversation_id does not exist` error
- **Why:** Migration not run on production PostgreSQL

#### 3. **Environment Differences**
- **What happened:** Works locally (SQLite) but breaks in production (PostgreSQL)
- **Example:** Different SQL syntax, different behavior
- **Why:** Not testing in production-like environment

#### 4. **HTML Escaping Issues**
- **What happened:** Apostrophes showing as `&#39;`
- **Example:** Chat messages displaying HTML entities
- **Why:** Jinja2 auto-escaping not handled properly

#### 5. **Query Parameter Loss**
- **What happened:** Back button losing context
- **Example:** Returning to `/subject` instead of `/subject?question=...`
- **Why:** URL parsing stripping query strings

#### 6. **No Code Review Process**
- **What happened:** Bugs merged directly to production
- **Why:** Solo developer, no second pair of eyes

---

## Comprehensive Prevention Strategy

### Phase 1: Immediate Actions (This Week)

#### 1. Set Up Staging Environment

**Priority: CRITICAL**

Follow the [STAGING_PRODUCTION_GUIDE.md](STAGING_PRODUCTION_GUIDE.md) to:
- Create `staging` branch
- Deploy to test.cozmiclearning.com
- Test ALL changes there first

**Benefit:** Catches 80% of bugs before production

#### 2. Create Pre-Deployment Checklist

**File: `PRE_DEPLOY_CHECKLIST.md`**

```markdown
# Before Deploying to Production

## Testing
- [ ] Feature works on staging (test.cozmiclearning.com)
- [ ] Tested as student, parent, teacher
- [ ] Tested on mobile device
- [ ] No console errors (F12 in browser)
- [ ] Database migrations run successfully on staging
- [ ] No broken links

## Security
- [ ] No sensitive data in code
- [ ] Environment variables configured
- [ ] Content moderation working
- [ ] Payment flows tested (test mode)

## Performance
- [ ] Page loads < 3 seconds
- [ ] No excessive OpenAI API calls
- [ ] Images optimized

## Deployment
- [ ] Database backup created
- [ ] Migration script ready (if needed)
- [ ] Rollback plan prepared
- [ ] Monitoring alerts active

## Sign-Off
Tested by: ___________
Date: ___________
```

#### 3. Add Error Tracking (Sentry)

**Install:**
```bash
pip install sentry-sdk[flask]
```

**Add to app.py:**
```python
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

if os.getenv('FLASK_ENV') == 'production':
    sentry_sdk.init(
        dsn="your-sentry-dsn-here",
        integrations=[FlaskIntegration()],
        traces_sample_rate=1.0,
        environment="production"
    )
```

**Benefits:**
- Instant email alerts when errors occur
- Stack traces to debug issues
- User context (what they were doing)

#### 4. Add Basic Health Monitoring

**Add to app.py:**
```python
@app.route("/health")
def health_check():
    """Health check endpoint for monitoring"""
    try:
        # Check database
        db.session.execute(text("SELECT 1"))

        return jsonify({
            "status": "healthy",
            "environment": os.getenv("FLASK_ENV"),
            "database": "connected",
            "timestamp": datetime.now().isoformat()
        }), 200
    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500
```

**Set up UptimeRobot.com (Free):**
- Monitor: `https://cozmiclearning.com/health`
- Check every: 5 minutes
- Alert if: Response is not 200 OK

---

### Phase 2: Testing Infrastructure (Next 2 Weeks)

#### 1. Add Automated Tests

**Install pytest:**
```bash
pip install pytest pytest-flask
```

**Create `tests/test_basic.py`:**
```python
import pytest
from app import app, db

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

def test_home_page(client):
    """Test home page loads"""
    response = client.get('/')
    assert response.status_code == 200

def test_subject_page_requires_params(client):
    """Test subject page requires question parameter"""
    response = client.get('/subject')
    assert response.status_code in [200, 302]  # Either shows page or redirects

def test_study_buddy_requires_login(client):
    """Test Study Buddy requires student login"""
    response = client.get('/learning-lab/study-buddy')
    assert response.status_code == 302  # Redirects to login

def test_health_endpoint(client):
    """Test health check endpoint"""
    response = client.get('/health')
    assert response.status_code == 200
    assert b'healthy' in response.data
```

**Run tests:**
```bash
pytest tests/
```

#### 2. Add Integration Tests for Critical Flows

**Create `tests/test_student_flow.py`:**
```python
def test_student_question_flow(client):
    """Test complete question asking flow"""
    # 1. Student logs in
    # 2. Asks question
    # 3. Gets answer
    # 4. Views in gradebook
    pass  # Implement based on your flows

def test_study_buddy_conversation(client):
    """Test Study Buddy conversation creation"""
    # 1. Start conversation
    # 2. Send message
    # 3. Get AI response
    # 4. View in conversation library
    pass
```

#### 3. Database Migration Testing

**Create `tests/test_migrations.py`:**
```python
def test_migration_script_runs():
    """Test that migration scripts execute without errors"""
    # Run migration
    # Check tables exist
    # Check columns exist
    pass
```

---

### Phase 3: Code Quality (Ongoing)

#### 1. Add Type Hints

**Before:**
```python
def get_student_id_from_session():
    return session.get('student_id')
```

**After:**
```python
from typing import Optional

def get_student_id_from_session() -> Optional[int]:
    """Get student ID from session"""
    return session.get('student_id')
```

#### 2. Add Docstrings

**Before:**
```python
def study_buddy():
    init_user()
    student_id = session.get('student_id')
    # ...
```

**After:**
```python
def study_buddy():
    """
    Study Buddy AI chat interface with conversation management.

    Handles:
    - Loading/creating conversations
    - Displaying message history
    - Managing active conversation state

    Returns:
        Rendered template with conversation data

    Raises:
        Redirects to dashboard if not student
    """
    init_user()
    student_id = session.get('student_id')
    # ...
```

#### 3. Add Input Validation

**Add helper functions:**
```python
def validate_grade(grade: str) -> bool:
    """Validate grade is between K-12"""
    if grade == 'K':
        return True
    try:
        return 1 <= int(grade) <= 12
    except (ValueError, TypeError):
        return False

def validate_subject(subject: str) -> bool:
    """Validate subject is in allowed list"""
    ALLOWED_SUBJECTS = ['math', 'science', 'history', 'english',
                        'geography', 'bible', 'art', 'music']
    return subject.lower() in ALLOWED_SUBJECTS

def sanitize_question(question: str) -> str:
    """Sanitize user question input"""
    # Remove excessive whitespace
    question = ' '.join(question.split())
    # Limit length
    return question[:500]
```

**Use in routes:**
```python
@app.route("/subject")
def subject():
    question = request.args.get('question', '')
    grade = request.args.get('grade', '5')
    subject = request.args.get('subject', 'math')

    # Validate inputs
    if not question:
        flash("Please ask a question", "error")
        return redirect('/')

    if not validate_grade(grade):
        grade = '5'  # Default

    if not validate_subject(subject):
        flash("Invalid subject", "error")
        return redirect('/')

    # Sanitize
    question = sanitize_question(question)

    # Continue with request...
```

#### 4. Add Error Handling

**Wrap database operations:**
```python
def safe_db_commit(session):
    """Safely commit database session with error handling"""
    try:
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        app.logger.error(f"Database commit failed: {e}")
        if os.getenv('FLASK_ENV') == 'production':
            # Send alert
            pass
        return False
```

**Wrap external API calls:**
```python
def safe_openai_call(prompt: str, max_retries: int = 3):
    """Call OpenAI API with retry logic"""
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        except Exception as e:
            app.logger.warning(f"OpenAI call failed (attempt {attempt + 1}): {e}")
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)  # Exponential backoff
```

---

### Phase 4: Development Workflow (New Standard)

#### Daily Development Process

**1. Morning: Pull latest changes**
```bash
git checkout staging
git pull origin staging
```

**2. Create feature branch (optional)**
```bash
git checkout -b feature/new-feature-name
```

**3. Make changes with tests**
- Write code
- Write test
- Run tests locally: `pytest tests/`

**4. Test locally**
```bash
python app.py
# Open http://localhost:5000
# Test the feature manually
```

**5. Push to staging**
```bash
git checkout staging
git merge feature/new-feature-name
git push origin staging
```

**6. Test on staging**
- Visit test.cozmiclearning.com
- Run through checklist
- Test as different users

**7. Deploy to production**
```bash
git checkout main
git merge staging
git push origin main
```

#### Code Review Checklist

Even when working solo, review your own code:

**Before committing:**
- [ ] Does it solve the problem?
- [ ] Is it the simplest solution?
- [ ] Are there any edge cases?
- [ ] What if the input is empty/null/wrong type?
- [ ] What if the database is down?
- [ ] What if the API call fails?
- [ ] Is there proper error handling?
- [ ] Are database changes backward compatible?

---

### Phase 5: Monitoring & Alerts

#### Set Up Monitoring Dashboard

**1. Uptime Monitoring (UptimeRobot)**
- Main site: cozmiclearning.com
- Health endpoint: cozmiclearning.com/health
- Study Buddy: cozmiclearning.com/learning-lab/study-buddy

**2. Error Tracking (Sentry)**
- Email alerts for all errors
- Slack notifications (if you use Slack)
- Weekly digest of errors

**3. Database Monitoring**
- Render/Heroku dashboard
- Track database size
- Monitor slow queries

**4. Cost Monitoring**
- OpenAI API usage
- Hosting costs
- Database storage

#### Create Alerts

**Critical Alerts (Immediate Action):**
- Site down (> 5 minutes)
- Database connection lost
- 500 errors increasing
- Payment processing failing

**Warning Alerts (Check Within Hour):**
- High API usage
- Slow page loads (> 5 seconds)
- Database backup failed

**Info Alerts (Check Daily):**
- New user signups
- Question volume
- Error count summary

---

### Phase 6: Documentation

#### Code Comments

**When to comment:**
```python
# ❌ Bad: Obvious comments
x = x + 1  # Increment x

# ✅ Good: Explain WHY
# Use exponential backoff to avoid rate limits
time.sleep(2 ** attempt)

# ✅ Good: Warn about edge cases
# Note: This will fail if student has no learning profile
learning_style = student.profile.primary_learning_style
```

#### Keep README Updated

Update README.md with:
- How to run locally
- How to run tests
- How to deploy
- Environment variables needed
- Common issues and fixes

---

## Common Error Patterns & Fixes

### 1. Database Errors

**Pattern:** Column doesn't exist
```python
# Error: column "conversation_id" does not exist
```

**Prevention:**
- Always run migrations on staging first
- Test with production database type (PostgreSQL)
- Check migration ran successfully

**Fix:**
```bash
# On production server
python add_conversation_system.py
```

### 2. HTML Escaping

**Pattern:** Special characters showing as entities
```python
# Shows: It&#39;s instead of: It's
```

**Prevention:**
- Use `|safe` filter for trusted content
- Use `|e` filter for user content
- Test with apostrophes in input

**Fix:**
```jinja2
{{ ai_response|safe }}  {# For AI responses #}
{{ user_input|e }}      {# For user input #}
```

### 3. Missing Parameters

**Pattern:** Required parameter is None
```python
# Error: 'NoneType' object has no attribute...
```

**Prevention:**
- Validate all inputs
- Provide defaults
- Handle None cases

**Fix:**
```python
question = request.args.get('question')
if not question:
    flash("Please ask a question", "error")
    return redirect('/')
```

### 4. Session Issues

**Pattern:** User logged out unexpectedly

**Prevention:**
- Use secure session configuration
- Set appropriate timeout
- Handle session expiry gracefully

**Fix:**
```python
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
app.config['SESSION_COOKIE_SECURE'] = True  # HTTPS only
app.config['SESSION_COOKIE_HTTPONLY'] = True
```

### 5. API Rate Limits

**Pattern:** Too many OpenAI requests

**Prevention:**
- Cache responses when possible
- Implement rate limiting per user
- Use retry logic with backoff

**Fix:**
```python
from functools import lru_cache

@lru_cache(maxsize=100)
def get_ai_response(question: str, grade: str):
    # This will cache responses for same questions
    return openai_call(question, grade)
```

---

## Quality Metrics to Track

### Weekly Review

**Error Rate:**
- Target: < 1% of requests result in error
- Track: Sentry dashboard

**Uptime:**
- Target: > 99.5% uptime
- Track: UptimeRobot

**Performance:**
- Target: < 3 second page load
- Track: Browser dev tools, Lighthouse

**Test Coverage:**
- Target: > 60% code coverage
- Track: `pytest --cov=app tests/`

---

## Emergency Response Plan

### If Production Breaks

**1. Immediate (< 5 minutes):**
```bash
# Rollback to previous version
git checkout main
git revert HEAD
git push origin main
```

**2. Investigate (< 30 minutes):**
- Check Sentry for error details
- Check server logs
- Identify root cause

**3. Fix (< 2 hours):**
- Fix on staging
- Test thoroughly
- Deploy to production

**4. Post-Mortem (< 24 hours):**
- Document what happened
- Update tests to prevent recurrence
- Update checklist if needed

---

## Summary: Prevention Checklist

### Before Writing Code
- [ ] Understand the requirement
- [ ] Plan the approach
- [ ] Consider edge cases

### While Writing Code
- [ ] Add input validation
- [ ] Add error handling
- [ ] Write comments for complex logic
- [ ] Keep functions small and focused

### Before Committing
- [ ] Run tests locally
- [ ] Check for console errors
- [ ] Review your own code
- [ ] Update documentation

### Before Deploying
- [ ] Test on staging
- [ ] Run migration on staging DB
- [ ] Test as all user types
- [ ] Create database backup
- [ ] Review deployment checklist

### After Deploying
- [ ] Monitor for errors
- [ ] Check site is responding
- [ ] Verify critical flows work
- [ ] Watch error tracking dashboard

---

## Tools to Install

**Essential:**
```bash
pip install pytest pytest-flask sentry-sdk
```

**Helpful:**
```bash
pip install black  # Code formatter
pip install flake8  # Linter
pip install mypy  # Type checker
```

**Usage:**
```bash
# Format code
black app.py

# Check code quality
flake8 app.py

# Check types
mypy app.py

# Run tests
pytest tests/
```

---

## Final Thoughts

**Why Errors Happen:**
1. Moving fast without testing
2. No staging environment
3. No automated tests
4. No monitoring
5. Complex codebase without guardrails

**How to Prevent:**
1. ✅ Use staging environment (test.cozmiclearning.com)
2. ✅ Follow deployment checklist
3. ✅ Add error tracking (Sentry)
4. ✅ Write tests for critical flows
5. ✅ Monitor production actively
6. ✅ Have rollback plan ready

**Result:**
- Fewer production bugs
- Faster debugging
- More confidence deploying
- Better user experience
- Less stress for you!
