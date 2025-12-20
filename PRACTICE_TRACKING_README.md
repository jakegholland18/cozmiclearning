# Self-Practice Tracking Implementation

## Overview
This system tracks student self-created practice sessions from Learning Planets and displays them in the gradebook with clear distinction from teacher-assigned work.

## How It Works

### 1. Database Model (PracticeSession)
Located in `models.py`, tracks:
- Student ID, subject, topic, grade level, mode
- Performance metrics (total questions, correct, score %)
- Time tracking
- Completion status
- Practice data and answers (JSON)

### 2. Backend Route
**Endpoint:** `POST /save_practice_session`

**Purpose:** Save completed practice session to database

**Request Body (JSON):**
```json
{
  "topic": "Algebra Basics",
  "time_spent_seconds": 420
}
```

**Response:**
```json
{
  "success": true,
  "session_id": 123,
  "score_percent": 85.5,
  "questions_correct": 8,
  "total_questions": 10
}
```

**Data Sources:**
- Session data: `session['practice']`, `session['practice_progress']`
- Metadata: `session['subject']`, `session['grade']`, `session['practice_mode']`

### 3. Frontend Integration Needed

The practice completion pages need to call `/save_practice_session` when:
1. Student completes all questions in a practice session
2. Student explicitly finishes/exits a practice session

**Example JavaScript:**
```javascript
async function savePracticeSession(timeSpentSeconds) {
    try {
        const response = await fetch('/save_practice_session', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                topic: 'Practice Topic',  // Optional, will use session data if not provided
                time_spent_seconds: timeSpentSeconds
            })
        });

        const data = await response.json();
        if (data.success) {
            console.log('Practice saved!', data);
            // Optionally show success message to student
        }
    } catch (error) {
        console.error('Failed to save practice:', error);
    }
}
```

### 4. Gradebook Display

The gradebook at `/student/gradebook` now shows:

**Teacher-Assigned Work (Blue Theme)**
- Class assignments
- Graded submissions
- Missing assignments
- Class performance breakdown

**Self-Practice (Gold/Yellow Theme)**
- Practice sessions from Learning Planets
- Practice statistics
- Subject breakdown
- Practice history table

## Database Migration

Run the SQL migration:
```bash
sqlite3 persistent_db/cozmiclearning.db < create_practice_sessions_table.sql
```

Or let SQLAlchemy create the table automatically on next run:
```python
from models import db
db.create_all()
```

## Testing

1. Log in as a student
2. Complete a practice session in Learning Planets
3. Call `/save_practice_session` from the frontend
4. Visit `/student/gradebook`
5. Verify self-practice section appears with the session

## Future Enhancements

- Automatic save on practice completion (add to practice templates)
- Practice analytics charts
- Practice streak tracking
- Integration with XP/rewards system
- Export practice history
