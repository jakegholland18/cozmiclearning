# Asynchronous Multiplayer Implementation Guide

## Overview

This guide explains how to integrate the asynchronous multiplayer challenge system into CozmicLearning.

## What's Included

### 1. **Database Models** (Already in models.py)
- `AsyncChallenge` - Stores challenge data with questions
- `ChallengeParticipant` - Tracks participants and their scores
- `ArcadeTeam` - Team management (for future team battles)
- `TeamMember` - Team membership
- `TeamMatch` - Team vs team matches

### 2. **Flask Routes** (arcade_multiplayer_routes.py)
- `/arcade/create_challenge` - Create challenge after playing
- `/arcade/challenges` - View sent/received challenges
- `/arcade/challenge/<id>` - Accept and play a challenge
- `/arcade/challenge/<id>/submit` - Submit results
- `/arcade/challenge/<id>/results` - View leaderboard
- `/arcade/friends` - Get list of challengeable friends
- `/arcade/challenges/count` - Notification badge count

### 3. **UI Templates**
- `arcade_multiplayer_challenges.html` - List of challenges
- `arcade_challenge_play.html` - Play the challenge
- `arcade_challenge_results.html` - Results leaderboard

### 4. **Migration Script** (create_multiplayer_tables.py)
- Creates all new database tables

---

## Installation Steps

### Step 1: Run Database Migration

```bash
cd /Users/tamara/Desktop/cozmiclearning
python create_multiplayer_tables.py
```

This creates the 5 new tables in your database.

### Step 2: Add Routes to app.py

Open `app.py` and add the routes from `arcade_multiplayer_routes.py`.

**Option A: Copy/Paste**
Copy all the routes from `arcade_multiplayer_routes.py` and paste them into `app.py` (recommended location: after the existing arcade routes, around line 5000-6000).

**Option B: Import**
Add at the top of app.py:
```python
from arcade_multiplayer_routes import *
```
(Note: This requires modifying arcade_multiplayer_routes.py to not have the @app decorator if app isn't imported there)

### Step 3: Add "Challenge Friends" Button to Game Results

After a student completes an arcade game, show a "Challenge Friends" button.

Find the game completion route (e.g., `/arcade/game/<game_key>/complete`) and add:

```python
@app.route('/arcade/game/<game_key>/complete', methods=['POST'])
def complete_arcade_game(game_key):
    # ... existing code ...

    # After saving score to database
    return render_template('arcade_game_complete.html',
        game=game,
        score=score,
        time_taken=time_taken,
        questions=questions_played,  # Store questions for challenge
        can_challenge=True  # Enable challenge button
    )
```

### Step 4: Add Challenge Button to Game Complete Template

In your game completion template (or create a new one), add:

```html
<!-- After showing score -->
<div class="challenge-section">
    <h3>Challenge Your Friends!</h3>
    <button id="challenge-btn" class="btn btn-primary">
        ⚔️ Challenge Friends to Beat Your Score
    </button>
</div>

<script>
document.getElementById('challenge-btn').addEventListener('click', async () => {
    // Get friends list
    const friendsResp = await fetch('/arcade/friends');
    const friendsData = await friendsResp.json();

    // Show friend selection modal
    showFriendSelector(friendsData.friends);
});

function showFriendSelector(friends) {
    // Create modal with checkboxes for each friend
    const modal = document.createElement('div');
    modal.className = 'modal';
    modal.innerHTML = `
        <div class="modal-content">
            <h2>Select Friends to Challenge</h2>
            <div class="friends-list">
                ${friends.map(f => `
                    <label>
                        <input type="checkbox" value="${f.id}" />
                        ${f.name} (Grade ${f.grade})
                    </label>
                `).join('')}
            </div>
            <button id="send-challenge-btn">Send Challenge</button>
            <button id="cancel-btn">Cancel</button>
        </div>
    `;
    document.body.appendChild(modal);

    document.getElementById('send-challenge-btn').addEventListener('click', async () => {
        const selected = Array.from(
            modal.querySelectorAll('input:checked')
        ).map(input => parseInt(input.value));

        if (selected.length === 0) {
            alert('Please select at least one friend');
            return;
        }

        // Send challenge
        const response = await fetch('/arcade/create_challenge', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                game_key: '{{ game.game_key }}',
                difficulty: '{{ difficulty }}',
                score: {{ score }},
                time_taken: {{ time_taken }},
                questions: {{ questions|tojson }},
                friend_ids: selected
            })
        });

        const data = await response.json();
        if (data.success) {
            alert(`Challenge sent to ${data.friends_challenged} friend(s)!`);
            modal.remove();
        }
    });

    document.getElementById('cancel-btn').addEventListener('click', () => {
        modal.remove();
    });
}
</script>
```

### Step 5: Add Navigation Links

Add links to the challenges page in your navigation:

```html
<!-- In your navbar or arcade hub -->
<a href="/arcade/challenges" class="nav-link">
    🏆 Challenges
    <span id="challenge-badge" class="notification-badge"></span>
</a>

<script>
// Update notification badge
async function updateChallengeBadge() {
    const resp = await fetch('/arcade/challenges/count');
    const data = await resp.json();
    const badge = document.getElementById('challenge-badge');
    if (data.count > 0) {
        badge.textContent = data.count;
        badge.style.display = 'inline';
    } else {
        badge.style.display = 'none';
    }
}

// Update every 30 seconds
setInterval(updateChallengeBadge, 30000);
updateChallengeBadge(); // Initial load
</script>
```

---

## How It Works

### User Flow

1. **Student A plays a game**
   - Completes Speed Math, scores 85 points in 45 seconds
   - Clicks "Challenge Friends"

2. **Student A selects friends**
   - Chooses siblings or classmates from list
   - Sends challenge

3. **Student B receives notification**
   - Sees challenge in /arcade/challenges
   - Badge shows "1 new challenge"

4. **Student B accepts challenge**
   - Clicks "Accept Challenge"
   - Plays the EXACT same questions Student A had
   - Tries to beat 85 points in under 45 seconds

5. **Results comparison**
   - Both can view leaderboard at /arcade/challenge/123/results
   - Winner determined by:
     - Higher score wins
     - If tied, faster time wins

### Data Flow

```
Student A completes game
        ↓
Questions stored in AsyncChallenge.questions_json
        ↓
ChallengeParticipant records created for each friend
        ↓
Student B loads challenge
        ↓
Questions parsed from JSON
        ↓
Student B plays same questions
        ↓
Results stored in ChallengeParticipant
        ↓
Leaderboard shows all results sorted by score/time
```

---

## Testing Checklist

### Database
- [ ] Tables created successfully
- [ ] Can insert AsyncChallenge record
- [ ] Can insert ChallengeParticipant records
- [ ] Foreign keys work properly

### Routes
- [ ] `/arcade/challenges` loads without error
- [ ] `/arcade/friends` returns list of students
- [ ] Can create challenge with POST to `/arcade/create_challenge`
- [ ] Can accept challenge at `/arcade/challenge/<id>`
- [ ] Can submit results with POST to `/arcade/challenge/<id>/submit`
- [ ] Results page loads at `/arcade/challenge/<id>/results`

### User Experience
- [ ] Student can create challenge after completing game
- [ ] Student can select multiple friends
- [ ] Challenge appears in friend's challenge list
- [ ] Friend can accept and play challenge
- [ ] Questions are identical to original
- [ ] Results submit successfully
- [ ] Leaderboard displays correctly
- [ ] Winner is calculated correctly (score, then time)

### Edge Cases
- [ ] Expired challenges are handled properly
- [ ] Can't accept challenge twice
- [ ] Can't submit results twice
- [ ] Invalid challenge IDs return 404
- [ ] Unauthorized access is blocked
- [ ] Empty friend list handled gracefully

---

## Customization Options

### 1. Change Expiration Time

In `arcade_multiplayer_routes.py`:
```python
expires_at=datetime.utcnow() + timedelta(hours=48),  # Change to 24 or 72
```

### 2. Add Email Notifications

After creating challenge:
```python
from flask_mail import Message, Mail

def send_challenge_notification(friend_id, challenger_id, game_key, challenge_id):
    friend = Student.query.get(friend_id)
    challenger = Student.query.get(challenger_id)
    parent = Parent.query.get(friend.parent_id)

    if parent and parent.email:
        msg = Message(
            subject=f"{challenger.name} challenged {friend.name} to {game_key}!",
            recipients=[parent.email],
            body=f"View challenge: {url_for('accept_arcade_challenge', challenge_id=challenge_id, _external=True)}"
        )
        mail.send(msg)
```

### 3. Add Points/XP Rewards

In `submit_challenge_result`:
```python
if won:
    participant.student.xp += 50  # Bonus XP for winning
    db.session.commit()
```

### 4. Add Achievements

```python
# Check if student has won 10 challenges
wins = ChallengeParticipant.query.filter_by(student_id=student_id, completed=True).count()
if wins >= 10:
    award_achievement(student_id, 'challenge_master')
```

---

## Troubleshooting

### "Table doesn't exist" error
Run: `python create_multiplayer_tables.py`

### Challenge questions not loading
Check that questions are being JSON serialized correctly:
```python
import json
questions_json = json.dumps(questions)
loaded_questions = json.loads(questions_json)
```

### Friends list empty
Verify students have `parent_id` (homeschool) or `class_id` (classroom) set.

### Challenge expired immediately
Check server timezone matches database timezone.

---

## Future Enhancements

### Phase 2: Real-Time Multiplayer
- Use Flask-SocketIO for live head-to-head battles
- Both students play simultaneously
- Live score updates

### Phase 3: Team Battles
- Use `ArcadeTeam`, `TeamMember`, `TeamMatch` models
- 2v2 or 3v3 team competitions
- Family vs family battles

### Phase 4: Tournaments
- Weekly/monthly brackets
- Single elimination or leaderboard style
- Prizes for winners

---

## Support

For questions or issues:
1. Check the [MULTIPLAYER_ARCHITECTURE.md](MULTIPLAYER_ARCHITECTURE.md) for technical details
2. Review [ARCADE_ENHANCEMENT_PLAN.md](ARCADE_ENHANCEMENT_PLAN.md) for roadmap
3. Test with `python -m pytest tests/test_multiplayer.py` (create tests)

---

## Summary

You now have a complete asynchronous multiplayer challenge system!

**Quick Start:**
1. Run `python create_multiplayer_tables.py`
2. Add routes from `arcade_multiplayer_routes.py` to `app.py`
3. Add "Challenge Friends" button to game completion
4. Add navigation link to `/arcade/challenges`
5. Test with 2+ students

Students can now challenge friends, compete for high scores, and see leaderboards - all without needing to be online at the same time!
