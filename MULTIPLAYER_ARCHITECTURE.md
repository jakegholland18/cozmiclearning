# CozmicLearning Arcade Multiplayer Architecture

## Overview

CozmicLearning multiplayer enables students to compete head-to-head, form teams, and participate in tournaments. The system supports both real-time and asynchronous gameplay.

---

## Multiplayer Modes

### 1. Head-to-Head (1v1)

**How It Works:**
1. Student A clicks "Challenge Friend" from arcade hub
2. Selects a game (e.g., Speed Math) and difficulty
3. Chooses opponent from friends list OR gets random matchmaking
4. System creates a "Match Room" with unique code
5. Student B receives notification/invitation
6. Both students click "Ready"
7. Game starts simultaneously with identical questions
8. First to answer correctly gets the point
9. Best of 5/10/15 questions (configurable)
10. Winner announced, XP awarded, stats recorded

**Technical Flow:**
```
Student A                    Server                      Student B
    |                          |                             |
    |-- Create Match --------->|                             |
    |                          |<---- Match Code: ABC123     |
    |                          |---- Send Invite ----------->|
    |                          |                             |
    |                          |<---- Accept Invite ---------|
    |                          |                             |
    |<---- Both Ready -------->|<---- Both Ready ----------->|
    |                          |                             |
    |<---- Question 1 -------->|<---- Question 1 ----------->|
    |-- Answer (2.3s) -------->|                             |
    |                          |<---- Answer (3.1s) ---------|
    |<---- You Win! (faster)   |                             |
    |                          |---- Next Question --------->|
    |                          |                             |
   ... (repeat for 5-15 questions)
    |                          |                             |
    |<---- Final Score: You Win!                             |
    |                          |---- Final Score: You Lose ->|
```

---

### 2. Asynchronous Challenge Mode

**How It Works:**
1. Student A plays a game and sets a high score
2. Clicks "Challenge Friends to Beat This"
3. Selects friends from list
4. Friends receive challenge notification
5. Friends have 24-48 hours to attempt
6. They play the SAME questions (stored from Student A's session)
7. Scores compared at the end
8. Winner declared when time expires or all complete

**Benefits:**
- No need for both students online simultaneously
- Works across time zones
- Perfect for homeschool families with different schedules
- Less technical complexity (no WebSockets needed)

**Technical Implementation:**
```python
class AsyncChallenge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    challenger_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    game_key = db.Column(db.String(100))
    difficulty = db.Column(db.String(20))
    questions_json = db.Column(db.Text)  # Store the exact questions
    challenger_score = db.Column(db.Integer)
    challenger_time = db.Column(db.Float)
    expires_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ChallengeParticipant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    challenge_id = db.Column(db.Integer, db.ForeignKey('async_challenges.id'))
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    score = db.Column(db.Integer)
    time_taken = db.Column(db.Float)
    completed = db.Column(db.Boolean, default=False)
    completed_at = db.Column(db.DateTime)
```

---

### 3. Team Battles (2v2 or 3v3)

**How It Works:**
1. Student creates team or joins existing team
2. Team captain selects game/difficulty
3. Challenges another team
4. All players ready up
5. Game starts simultaneously for all players
6. Each player answers independently
7. Team score = sum of individual scores
8. Highest team score wins
9. All team members receive shared victory/XP

**Team Types:**
- **Family Teams**: Parents + kids on same team
- **Homeschool Co-op Teams**: Students from same co-op
- **Classroom Teams**: Teacher-created teams
- **Friend Teams**: Students create custom teams

**Technical Implementation:**
```python
class ArcadeTeam(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    team_code = db.Column(db.String(10), unique=True)  # Join code
    captain_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    team_type = db.Column(db.String(50))  # family, coop, classroom, custom
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class TeamMember(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('arcade_teams.id'))
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    role = db.Column(db.String(20))  # captain, member
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)

class TeamMatch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_a_id = db.Column(db.Integer, db.ForeignKey('arcade_teams.id'))
    team_b_id = db.Column(db.Integer, db.ForeignKey('arcade_teams.id'))
    game_key = db.Column(db.String(100))
    difficulty = db.Column(db.String(20))
    team_a_score = db.Column(db.Integer, default=0)
    team_b_score = db.Column(db.Integer, default=0)
    winner_team_id = db.Column(db.Integer)
    match_status = db.Column(db.String(20))  # waiting, active, completed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
```

---

### 4. Tournament Mode

**How It Works:**
1. Admin/system creates tournament (weekly, monthly)
2. Students register during registration window
3. Bracket auto-generated based on registrations
4. Round 1: All students compete (asynchonously or scheduled time)
5. Top 50% advance to Round 2
6. Continues until finals
7. Champion crowned, prizes awarded

**Tournament Types:**

**Single-Elimination Bracket:**
```
Round 1 (16 players)    Round 2 (8)    Semifinals (4)    Finals (2)    Champion
Player 1 ─┐
          ├─ Winner A ─┐
Player 2 ─┘            │
                       ├─ Winner E ─┐
Player 3 ─┐            │            │
          ├─ Winner B ─┘            │
Player 4 ─┘                         ├─ Winner I ─┐
                                    │            │
Player 5 ─┐                         │            │
          ├─ Winner C ─┐            │            │
Player 6 ─┘            │            │            │
                       ├─ Winner F ─┘            ├─ CHAMPION
Player 7 ─┐            │                         │
          ├─ Winner D ─┘                         │
Player 8 ─┘                                      │
                                                 │
... (mirror for other half of bracket)          │
                                                 │
                       ────────────────────────────┘
```

**Leaderboard Tournament (Simpler):**
- All students play same challenge
- Scores ranked on leaderboard
- Top 10 win prizes
- No bracket needed

**Technical Implementation:**
```python
class Tournament(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    tournament_type = db.Column(db.String(50))  # elimination, leaderboard
    game_key = db.Column(db.String(100))
    difficulty = db.Column(db.String(20))
    registration_start = db.Column(db.DateTime)
    registration_end = db.Column(db.DateTime)
    tournament_start = db.Column(db.DateTime)
    tournament_end = db.Column(db.DateTime)
    max_participants = db.Column(db.Integer)
    prize_description = db.Column(db.Text)
    status = db.Column(db.String(20))  # registration, active, completed

class TournamentParticipant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tournament_id = db.Column(db.Integer, db.ForeignKey('tournaments.id'))
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    seed = db.Column(db.Integer)  # Bracket seeding
    current_round = db.Column(db.Integer, default=1)
    eliminated = db.Column(db.Boolean, default=False)
    final_rank = db.Column(db.Integer)

class TournamentMatch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tournament_id = db.Column(db.Integer, db.ForeignKey('tournaments.id'))
    round_number = db.Column(db.Integer)
    match_number = db.Column(db.Integer)
    player_1_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    player_2_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    player_1_score = db.Column(db.Integer)
    player_2_score = db.Column(db.Integer)
    winner_id = db.Column(db.Integer)
    completed = db.Column(db.Boolean, default=False)
```

---

## Real-Time vs Asynchronous

### Real-Time Multiplayer (WebSockets)

**Best For:**
- Head-to-head battles
- Live tournaments with scheduled times
- Same-time team battles
- Spectator mode

**Technical Stack:**
```python
# Using Flask-SocketIO
from flask_socketio import SocketIO, emit, join_room, leave_room

socketio = SocketIO(app, cors_allowed_origins="*")

# Match room management
active_matches = {}  # {match_id: {players: [], questions: [], scores: {}}}

@socketio.on('join_match')
def handle_join_match(data):
    match_id = data['match_id']
    student_id = data['student_id']

    join_room(match_id)

    if match_id not in active_matches:
        active_matches[match_id] = {
            'players': [],
            'ready': {},
            'current_question': 0,
            'scores': {}
        }

    active_matches[match_id]['players'].append(student_id)
    active_matches[match_id]['scores'][student_id] = 0

    emit('player_joined', {'student_id': student_id}, room=match_id)

@socketio.on('player_ready')
def handle_player_ready(data):
    match_id = data['match_id']
    student_id = data['student_id']

    active_matches[match_id]['ready'][student_id] = True

    # Check if all players ready
    if len(active_matches[match_id]['ready']) == len(active_matches[match_id]['players']):
        # Start the match
        emit('match_start', {
            'question': get_next_question(match_id)
        }, room=match_id)

@socketio.on('submit_answer')
def handle_submit_answer(data):
    match_id = data['match_id']
    student_id = data['student_id']
    answer = data['answer']
    time_taken = data['time_taken']

    # Check answer
    is_correct = check_answer(match_id, answer)

    if is_correct:
        # Award points (faster = more points)
        points = calculate_points(time_taken)
        active_matches[match_id]['scores'][student_id] += points

        emit('answer_result', {
            'correct': True,
            'points': points,
            'scores': active_matches[match_id]['scores']
        }, room=match_id)

    # Check if round complete
    if all_players_answered(match_id):
        active_matches[match_id]['current_question'] += 1

        if active_matches[match_id]['current_question'] < TOTAL_QUESTIONS:
            # Next question
            emit('next_question', {
                'question': get_next_question(match_id)
            }, room=match_id)
        else:
            # Match over
            winner_id = get_winner(match_id)
            emit('match_complete', {
                'winner': winner_id,
                'final_scores': active_matches[match_id]['scores']
            }, room=match_id)

            # Save to database
            save_match_results(match_id)
```

**Client-Side (JavaScript):**
```javascript
// Connect to WebSocket
const socket = io();

// Join match
socket.emit('join_match', {
    match_id: matchId,
    student_id: studentId
});

// Player ready
document.getElementById('ready-btn').addEventListener('click', () => {
    socket.emit('player_ready', {
        match_id: matchId,
        student_id: studentId
    });
});

// Receive question
socket.on('next_question', (data) => {
    displayQuestion(data.question);
    startTimer();
});

// Submit answer
function submitAnswer(answer) {
    const timeTaken = stopTimer();
    socket.emit('submit_answer', {
        match_id: matchId,
        student_id: studentId,
        answer: answer,
        time_taken: timeTaken
    });
}

// Display results
socket.on('answer_result', (data) => {
    if (data.correct) {
        showCorrectFeedback(data.points);
    }
    updateScoreboard(data.scores);
});

// Match complete
socket.on('match_complete', (data) => {
    displayWinner(data.winner, data.final_scores);
});
```

---

### Asynchronous Multiplayer (Simpler, No WebSockets)

**Best For:**
- Challenge friends across time zones
- Homeschool flexible scheduling
- No need for real-time coordination
- Lower server load

**How It Works:**
```python
# app.py routes

@app.route('/arcade/create_challenge', methods=['POST'])
def create_challenge():
    student_id = session['student_id']
    game_key = request.json['game_key']
    difficulty = request.json['difficulty']
    friend_ids = request.json['friend_ids']  # List of friends to challenge

    # Student plays the game first
    questions = generate_game_questions(game_key, difficulty, count=10)

    # Create challenge
    challenge = AsyncChallenge(
        challenger_id=student_id,
        game_key=game_key,
        difficulty=difficulty,
        questions_json=json.dumps(questions),  # Store exact questions
        challenger_score=0,  # Will be set when they play
        expires_at=datetime.utcnow() + timedelta(hours=48)
    )
    db.session.add(challenge)
    db.session.flush()

    # Add participants
    for friend_id in friend_ids:
        participant = ChallengeParticipant(
            challenge_id=challenge.id,
            student_id=friend_id
        )
        db.session.add(participant)

        # Send notification
        send_challenge_notification(friend_id, student_id, game_key)

    db.session.commit()

    return jsonify({
        'challenge_id': challenge.id,
        'questions': questions
    })

@app.route('/arcade/accept_challenge/<int:challenge_id>')
def accept_challenge(challenge_id):
    student_id = session['student_id']

    challenge = AsyncChallenge.query.get_or_404(challenge_id)

    # Check if expired
    if datetime.utcnow() > challenge.expires_at:
        return jsonify({'error': 'Challenge expired'}), 400

    # Load the exact same questions the challenger had
    questions = json.loads(challenge.questions_json)

    return render_template('arcade_challenge.html',
        challenge=challenge,
        questions=questions
    )

@app.route('/arcade/submit_challenge_result', methods=['POST'])
def submit_challenge_result():
    student_id = session['student_id']
    challenge_id = request.json['challenge_id']
    score = request.json['score']
    time_taken = request.json['time_taken']

    # Update participant
    participant = ChallengeParticipant.query.filter_by(
        challenge_id=challenge_id,
        student_id=student_id
    ).first()

    participant.score = score
    participant.time_taken = time_taken
    participant.completed = True
    participant.completed_at = datetime.utcnow()
    db.session.commit()

    # Check if all participants completed
    challenge = AsyncChallenge.query.get(challenge_id)
    all_participants = ChallengeParticipant.query.filter_by(
        challenge_id=challenge_id
    ).all()

    if all(p.completed for p in all_participants):
        # Determine winner
        winner = max(all_participants, key=lambda p: (p.score, -p.time_taken))

        # Notify all participants
        for p in all_participants:
            send_challenge_complete_notification(
                p.student_id,
                winner.student_id,
                challenge
            )

    return jsonify({'success': True})

@app.route('/arcade/challenge_results/<int:challenge_id>')
def challenge_results(challenge_id):
    challenge = AsyncChallenge.query.get_or_404(challenge_id)
    participants = ChallengeParticipant.query.filter_by(
        challenge_id=challenge_id
    ).all()

    # Sort by score (desc), then time (asc)
    participants.sort(key=lambda p: (-p.score if p.score else 0, p.time_taken if p.time_taken else float('inf')))

    return render_template('challenge_results.html',
        challenge=challenge,
        participants=participants
    )
```

---

## Matchmaking System

### Random Matchmaking

**How It Works:**
1. Student clicks "Play Random Opponent"
2. Server adds them to matchmaking queue
3. Server pairs with another student of similar skill level
4. Both notified, match starts

**Implementation:**
```python
# Matchmaking queue (in-memory or Redis)
matchmaking_queue = {
    'speed_math': {
        'easy': [],
        'medium': [],
        'hard': []
    },
    # ... other games
}

@app.route('/arcade/find_match', methods=['POST'])
def find_match():
    student_id = session['student_id']
    game_key = request.json['game_key']
    difficulty = request.json['difficulty']

    # Get student's skill level for matchmaking
    student = Student.query.get(student_id)
    skill_rating = get_skill_rating(student_id, game_key)

    # Check if someone waiting in queue
    queue = matchmaking_queue[game_key][difficulty]

    # Find opponent with similar skill (±200 rating points)
    opponent = None
    for queued_student in queue:
        opponent_rating = get_skill_rating(queued_student['student_id'], game_key)
        if abs(skill_rating - opponent_rating) <= 200:
            opponent = queued_student
            queue.remove(opponent)
            break

    if opponent:
        # Create match
        match = create_head_to_head_match(
            student_id,
            opponent['student_id'],
            game_key,
            difficulty
        )

        # Notify both players
        return jsonify({
            'match_found': True,
            'match_id': match.id,
            'opponent': get_student_display_name(opponent['student_id'])
        })
    else:
        # Add to queue
        queue.append({
            'student_id': student_id,
            'joined_at': time.time()
        })

        return jsonify({
            'match_found': False,
            'queue_position': len(queue)
        })

# Periodic cleanup of old queue entries
def cleanup_matchmaking_queue():
    current_time = time.time()
    for game in matchmaking_queue:
        for difficulty in matchmaking_queue[game]:
            queue = matchmaking_queue[game][difficulty]
            # Remove entries older than 5 minutes
            matchmaking_queue[game][difficulty] = [
                entry for entry in queue
                if current_time - entry['joined_at'] < 300
            ]
```

### Skill-Based Matching

**ELO-Style Rating System:**
```python
class StudentGameRating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    game_key = db.Column(db.String(100))
    rating = db.Column(db.Integer, default=1000)  # Start at 1000
    matches_played = db.Column(db.Integer, default=0)
    wins = db.Column(db.Integer, default=0)
    losses = db.Column(db.Integer, default=0)

def update_ratings_after_match(winner_id, loser_id, game_key):
    """Update ELO ratings after a match"""
    K = 32  # K-factor (how much ratings change)

    winner_rating = get_or_create_rating(winner_id, game_key)
    loser_rating = get_or_create_rating(loser_id, game_key)

    # Expected scores
    expected_winner = 1 / (1 + 10**((loser_rating.rating - winner_rating.rating)/400))
    expected_loser = 1 / (1 + 10**((winner_rating.rating - loser_rating.rating)/400))

    # Update ratings
    winner_rating.rating += K * (1 - expected_winner)
    loser_rating.rating += K * (0 - expected_loser)

    # Update stats
    winner_rating.matches_played += 1
    winner_rating.wins += 1
    loser_rating.matches_played += 1
    loser_rating.losses += 1

    db.session.commit()
```

---

## Notification System

### In-App Notifications
```python
class ArcadeNotification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    notification_type = db.Column(db.String(50))  # challenge, match_found, tournament_start
    title = db.Column(db.String(200))
    message = db.Column(db.Text)
    action_url = db.Column(db.String(500))  # URL to navigate to
    read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

def send_challenge_notification(recipient_id, challenger_id, game_key):
    challenger = Student.query.get(challenger_id)
    game = next(g for g in ARCADE_GAMES if g['game_key'] == game_key)

    notification = ArcadeNotification(
        student_id=recipient_id,
        notification_type='challenge',
        title='New Arcade Challenge!',
        message=f'{challenger.name} challenged you to {game["name"]}!',
        action_url=f'/arcade/challenge/{challenge_id}'
    )
    db.session.add(notification)
    db.session.commit()

    # Optional: Send email/push notification
    send_email_notification(recipient_id, notification)
```

### Email Notifications (Optional)
```python
def send_email_notification(student_id, notification):
    student = Student.query.get(student_id)
    parent = Parent.query.get(student.parent_id)

    if parent.email_notifications_enabled:
        send_email(
            to=parent.email,
            subject=notification.title,
            body=notification.message,
            action_button_url=notification.action_url
        )
```

---

## Anti-Cheating Measures

### 1. Time Limits
- Minimum time to answer (prevent auto-clickers)
- Maximum time to answer
- Server-side validation

### 2. Question Rotation
- Never reuse exact same questions
- Shuffle answer order
- Randomize numerical values

### 3. Session Validation
```python
def validate_match_session(match_id, student_id):
    """Ensure student is authorized for this match"""
    match = HeadToHeadMatch.query.get(match_id)

    if student_id not in [match.player_1_id, match.player_2_id]:
        raise Unauthorized("Not a participant in this match")

    if match.status != 'active':
        raise BadRequest("Match not active")

    return True

def validate_answer_timing(question_served_at, answer_submitted_at):
    """Ensure answer wasn't submitted too quickly (bot) or too slowly (cheating)"""
    time_elapsed = (answer_submitted_at - question_served_at).total_seconds()

    if time_elapsed < 0.5:  # Too fast - likely automated
        return False

    if time_elapsed > 60:  # Too slow - question expired
        return False

    return True
```

### 4. Answer Hashing
```python
# Don't send correct answer to client
# Server-side only validation

def send_question_to_client(question):
    """Remove answer before sending to client"""
    client_question = {
        'question_id': question['id'],
        'question': question['question'],
        'options': question['options'],
        # DO NOT include: 'answer': question['answer']
    }
    return client_question

def check_answer(question_id, submitted_answer):
    """Server-side answer validation"""
    question = get_question_from_db(question_id)
    return submitted_answer == question['answer']
```

---

## Scalability Considerations

### 1. WebSocket Connection Limits
- Use Socket.IO rooms for matches
- Limit concurrent connections per server
- Load balance across multiple servers

### 2. Database Optimization
- Index on student_id, game_key, match_id
- Archive completed matches after 90 days
- Use Redis for matchmaking queue

### 3. Caching
```python
# Cache leaderboards
@cache.memoize(timeout=300)  # 5 minutes
def get_global_leaderboard(game_key):
    return GameLeaderboard.query.filter_by(game_key=game_key)\
        .order_by(GameLeaderboard.high_score.desc())\
        .limit(100).all()
```

---

## Implementation Phases

### Phase 1: Asynchronous Multiplayer (Easiest)
- ✅ Challenge friends
- ✅ Same questions, compare scores
- ✅ 48-hour time window
- No WebSockets needed

### Phase 2: Real-Time 1v1 (Medium)
- WebSocket integration
- Matchmaking queue
- Live scoring
- Skill-based matching

### Phase 3: Team Battles (Complex)
- Team management
- Multi-player coordination
- Team leaderboards

### Phase 4: Tournaments (Most Complex)
- Bracket generation
- Round progression
- Prize distribution
- Admin tools

---

## Recommendation

**Start with Asynchronous Multiplayer:**
1. Simpler to implement (no WebSockets)
2. Works better for homeschool schedules
3. Lower server requirements
4. Can add real-time later

**Then add Real-Time for premium users:**
- Makes a great Premium tier feature
- Higher engagement
- More exciting for competitive students

This gives you multiplayer functionality quickly while leaving room to grow!
