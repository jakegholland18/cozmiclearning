"""
Asynchronous Multiplayer Routes for Arcade
Add these routes to app.py to enable async challenges

FEATURES:
- Create challenges after playing a game
- Challenge friends with same questions
- 48-hour time window to complete
- Compare scores when all complete
- Winner notification
"""

from flask import request, jsonify, render_template, session, redirect, url_for
from datetime import datetime, timedelta
from models import db, AsyncChallenge, ChallengeParticipant, Student, ArcadeGame
import json


# ============================================================
# CHALLENGE CREATION
# ============================================================

@app.route('/arcade/create_challenge', methods=['POST'])
def create_arcade_challenge():
    """
    Create an asynchronous challenge after completing a game.
    Student plays game, then challenges friends with same questions.
    """
    if 'student_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401

    data = request.json
    student_id = session['student_id']
    game_key = data.get('game_key')
    difficulty = data.get('difficulty')
    score = data.get('score')
    time_taken = data.get('time_taken')
    questions = data.get('questions')  # List of questions from game
    friend_ids = data.get('friend_ids', [])  # List of student IDs to challenge

    # Validate
    if not all([game_key, difficulty, score is not None, time_taken, questions]):
        return jsonify({'error': 'Missing required fields'}), 400

    if not friend_ids:
        return jsonify({'error': 'Must select at least one friend to challenge'}), 400

    # Create challenge
    challenge = AsyncChallenge(
        challenger_id=student_id,
        game_key=game_key,
        difficulty=difficulty,
        questions_json=json.dumps(questions),
        challenger_score=score,
        challenger_time=time_taken,
        expires_at=datetime.utcnow() + timedelta(hours=48),
        status='active'
    )
    db.session.add(challenge)
    db.session.flush()

    # Add participants
    for friend_id in friend_ids:
        # Verify friend exists
        friend = Student.query.get(friend_id)
        if friend:
            participant = ChallengeParticipant(
                challenge_id=challenge.id,
                student_id=friend_id
            )
            db.session.add(participant)

            # TODO: Send notification to friend
            # send_challenge_notification(friend_id, student_id, game_key, challenge.id)

    db.session.commit()

    return jsonify({
        'success': True,
        'challenge_id': challenge.id,
        'friends_challenged': len(friend_ids),
        'expires_at': challenge.expires_at.isoformat()
    })


# ============================================================
# VIEW PENDING CHALLENGES
# ============================================================

@app.route('/arcade/challenges')
def view_arcade_challenges():
    """
    View all challenges (sent and received)
    """
    if 'student_id' not in session:
        return redirect('/login')

    student_id = session['student_id']

    # Challenges I created
    challenges_sent = AsyncChallenge.query.filter_by(
        challenger_id=student_id,
        status='active'
    ).order_by(AsyncChallenge.created_at.desc()).all()

    # Challenges I received
    my_participations = ChallengeParticipant.query.filter_by(
        student_id=student_id
    ).join(AsyncChallenge).filter(
        AsyncChallenge.status == 'active',
        AsyncChallenge.expires_at > datetime.utcnow()
    ).order_by(AsyncChallenge.created_at.desc()).all()

    # Get game names
    game_map = {g.game_key: g.name for g in ArcadeGame.query.all()}

    return render_template('arcade_challenges.html',
        challenges_sent=challenges_sent,
        challenges_received=my_participations,
        game_map=game_map
    )


# ============================================================
# ACCEPT CHALLENGE
# ============================================================

@app.route('/arcade/challenge/<int:challenge_id>')
def accept_arcade_challenge(challenge_id):
    """
    Accept and play a challenge.
    Loads the exact same questions the challenger had.
    """
    if 'student_id' not in session:
        return redirect('/login')

    student_id = session['student_id']

    # Get challenge
    challenge = AsyncChallenge.query.get_or_404(challenge_id)

    # Check if expired
    if datetime.utcnow() > challenge.expires_at:
        challenge.status = 'expired'
        db.session.commit()
        return render_template('challenge_expired.html', challenge=challenge)

    # Verify student is a participant
    participant = ChallengeParticipant.query.filter_by(
        challenge_id=challenge_id,
        student_id=student_id
    ).first()

    if not participant:
        return "You are not part of this challenge", 403

    # Mark as viewed
    if not participant.viewed:
        participant.viewed = True
        participant.viewed_at = datetime.utcnow()
        db.session.commit()

    # Check if already completed
    if participant.completed:
        return redirect(url_for('view_challenge_results', challenge_id=challenge_id))

    # Load questions
    questions = json.loads(challenge.questions_json)

    # Get game info
    game = ArcadeGame.query.filter_by(game_key=challenge.game_key).first()
    challenger = Student.query.get(challenge.challenger_id)

    return render_template('arcade_challenge_play.html',
        challenge=challenge,
        questions=questions,
        game=game,
        challenger=challenger,
        participant=participant
    )


# ============================================================
# SUBMIT CHALLENGE RESULT
# ============================================================

@app.route('/arcade/challenge/<int:challenge_id>/submit', methods=['POST'])
def submit_challenge_result(challenge_id):
    """
    Submit results after completing a challenge
    """
    if 'student_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401

    student_id = session['student_id']
    data = request.json

    score = data.get('score')
    time_taken = data.get('time_taken')

    if score is None or time_taken is None:
        return jsonify({'error': 'Missing score or time'}), 400

    # Get participant record
    participant = ChallengeParticipant.query.filter_by(
        challenge_id=challenge_id,
        student_id=student_id
    ).first_or_404()

    # Update results
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

    all_complete = all(p.completed for p in all_participants)

    if all_complete:
        challenge.status = 'completed'
        db.session.commit()

        # Determine winner
        # Sort by score (desc), then time (asc)
        participants_sorted = sorted(
            all_participants,
            key=lambda p: (-p.score, p.time_taken)
        )
        winner = participants_sorted[0]

        # TODO: Send completion notifications
        # for p in all_participants:
        #     send_challenge_complete_notification(p.student_id, winner.student_id, challenge)

    return jsonify({
        'success': True,
        'all_complete': all_complete,
        'redirect_url': url_for('view_challenge_results', challenge_id=challenge_id)
    })


# ============================================================
# VIEW CHALLENGE RESULTS
# ============================================================

@app.route('/arcade/challenge/<int:challenge_id>/results')
def view_challenge_results(challenge_id):
    """
    View results of a challenge (leaderboard)
    """
    if 'student_id' not in session:
        return redirect('/login')

    student_id = session['student_id']

    challenge = AsyncChallenge.query.get_or_404(challenge_id)

    # Verify student is involved
    is_challenger = (challenge.challenger_id == student_id)
    participant = ChallengeParticipant.query.filter_by(
        challenge_id=challenge_id,
        student_id=student_id
    ).first()

    if not is_challenger and not participant:
        return "You are not part of this challenge", 403

    # Get all participants
    participants = ChallengeParticipant.query.filter_by(
        challenge_id=challenge_id
    ).all()

    # Add challenger to list
    class ChallengerResult:
        def __init__(self, challenge):
            self.student_id = challenge.challenger_id
            self.student = Student.query.get(challenge.challenger_id)
            self.score = challenge.challenger_score
            self.time_taken = challenge.challenger_time
            self.completed = True
            self.completed_at = challenge.created_at

    all_results = [ChallengerResult(challenge)] + [
        p for p in participants if p.completed
    ]

    # Sort by score (desc), then time (asc)
    all_results.sort(key=lambda r: (-r.score, r.time_taken))

    # Determine winner
    winner = all_results[0] if all_results else None

    # Get game info
    game = ArcadeGame.query.filter_by(game_key=challenge.game_key).first()

    # Check if all complete
    pending_count = sum(1 for p in participants if not p.completed)

    return render_template('arcade_challenge_results.html',
        challenge=challenge,
        results=all_results,
        winner=winner,
        game=game,
        student_id=student_id,
        pending_count=pending_count,
        total_participants=len(participants) + 1  # +1 for challenger
    )


# ============================================================
# GET FRIENDS LIST FOR CHALLENGES
# ============================================================

@app.route('/arcade/friends')
def get_challenge_friends():
    """
    Get list of students who can be challenged.
    For homeschool: siblings
    For classroom: classmates
    """
    if 'student_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401

    student_id = session['student_id']
    student = Student.query.get(student_id)

    friends = []

    if student.parent_id:
        # Homeschool: Get siblings
        siblings = Student.query.filter(
            Student.parent_id == student.parent_id,
            Student.id != student_id
        ).all()
        friends = siblings

    elif student.teacher_id and student.class_id:
        # Classroom: Get classmates
        classmates = Student.query.filter(
            Student.class_id == student.class_id,
            Student.id != student_id
        ).all()
        friends = classmates

    # Format for JSON
    friends_list = [{
        'id': f.id,
        'name': f.name,
        'grade': f.grade
    } for f in friends]

    return jsonify({
        'friends': friends_list
    })


# ============================================================
# CHALLENGE NOTIFICATIONS COUNT
# ============================================================

@app.route('/arcade/challenges/count')
def get_pending_challenges_count():
    """
    Get count of pending challenges (for notification badge)
    """
    if 'student_id' not in session:
        return jsonify({'count': 0})

    student_id = session['student_id']

    # Count unviewed challenges
    count = ChallengeParticipant.query.filter_by(
        student_id=student_id,
        viewed=False,
        completed=False
    ).join(AsyncChallenge).filter(
        AsyncChallenge.status == 'active',
        AsyncChallenge.expires_at > datetime.utcnow()
    ).count()

    return jsonify({'count': count})


# ============================================================
# CLEANUP EXPIRED CHALLENGES (Periodic Task)
# ============================================================

def cleanup_expired_challenges():
    """
    Mark expired challenges as expired.
    Run this periodically (e.g., daily cron job)
    """
    expired = AsyncChallenge.query.filter(
        AsyncChallenge.status == 'active',
        AsyncChallenge.expires_at < datetime.utcnow()
    ).all()

    for challenge in expired:
        challenge.status = 'expired'

    db.session.commit()
    print(f"Marked {len(expired)} challenges as expired")
