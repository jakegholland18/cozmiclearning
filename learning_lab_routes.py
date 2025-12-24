"""
Learning Lab Routes
Add these routes to app.py after student assignment routes (around line 8435)
"""

LEARNING_LAB_ROUTES = """
# ============================================================
# LEARNING LAB - Discover Learning Preferences
# ============================================================

@app.route("/learning-lab")
def learning_lab():
    init_user()
    if g.role != 'student':
        flash("Learning Lab is for students only", "error")
        return redirect(url_for('dashboard'))

    student = Student.query.get(g.user_id)
    profile = LearningProfile.query.filter_by(student_id=g.user_id).first()

    # Get strategy usage count
    strategies_count = 0
    favorite_tools_count = 0
    if profile:
        strategies_count = StrategyUsage.query.filter_by(student_id=g.user_id).count()
        # Count enabled tools
        favorite_tools_count = sum([
            profile.uses_text_to_speech,
            profile.uses_focus_timer,
            profile.uses_task_breakdown,
            profile.uses_visual_organizers,
            profile.uses_movement_breaks
        ])

    # Daily tip (rotate based on day of year)
    tips = [
        "Try the Pomodoro Technique: 25 minutes of focused work, then a 5-minute break!",
        "Teach what you learn to someone else - it's one of the best ways to remember!",
        "Use color coding to organize your notes - your brain loves colors!",
        "Take a 2-minute movement break every 20 minutes to boost your focus.",
        "Study the hardest subjects when you have the most energy (usually morning).",
        "Create silly mnemonics or songs to remember lists - the sillier, the better!",
        "Practice spaced repetition: review material at increasing intervals over time."
    ]
    import datetime
    day_of_year = datetime.datetime.now().timetuple().tm_yday
    daily_tip = tips[day_of_year % len(tips)]

    return render_template('learning_lab.html',
                         student=student,
                         has_profile=profile is not None and profile.quiz_completed,
                         profile=profile,
                         strategies_count=strategies_count,
                         favorite_tools_count=favorite_tools_count,
                         daily_tip=daily_tip)


@app.route("/learning-lab/quiz")
def learning_lab_quiz():
    init_user()
    if g.role != 'student':
        flash("Learning Lab is for students only", "error")
        return redirect(url_for('dashboard'))

    return render_template('learning_quiz.html')


@app.route("/learning-lab/quiz/submit", methods=["POST"])
def learning_lab_quiz_submit():
    init_user()
    if g.role != 'student':
        return jsonify({'error': 'Unauthorized'}), 403

    from modules.learning_lab_helper import process_quiz_results, send_parent_notification, send_teacher_notification

    # Collect quiz answers
    quiz_answers = {}
    for key in request.form:
        if key != 'csrf_token':
            quiz_answers[key] = request.form.get(key)

    # Process and save profile
    profile = process_quiz_results(g.user_id, quiz_answers)

    if profile:
        # Send notifications to parent and teachers
        try:
            send_parent_notification(g.user_id, profile)
            send_teacher_notification(g.user_id, profile)
        except Exception as e:
            print(f"Error sending notifications: {e}")

        flash("Your Learning Profile has been created! Check out your results below.", "success")
        return redirect(url_for('learning_lab_profile'))
    else:
        flash("There was an error creating your profile. Please try again.", "error")
        return redirect(url_for('learning_lab_quiz'))


@app.route("/learning-lab/profile")
def learning_lab_profile():
    init_user()
    if g.role != 'student':
        flash("Learning Lab is for students only", "error")
        return redirect(url_for('dashboard'))

    student = Student.query.get(g.user_id)
    profile = LearningProfile.query.filter_by(student_id=g.user_id).first()

    if not profile or not profile.quiz_completed:
        flash("Please take the Learning Strengths Quiz first!", "info")
        return redirect(url_for('learning_lab_quiz'))

    from modules.learning_lab_helper import get_recommended_strategies

    # Get recommended strategies based on profile
    recommended_strategies = get_recommended_strategies(profile)

    # Get usage stats
    strategy_usage = StrategyUsage.query.filter_by(student_id=g.user_id).all()
    most_used = sorted(strategy_usage, key=lambda x: x.times_used, reverse=True)[:5]

    return render_template('learning_profile.html',
                         student=student,
                         profile=profile,
                         recommended_strategies=recommended_strategies,
                         most_used_strategies=most_used)


@app.route("/learning-lab/strategies")
def learning_lab_strategies():
    init_user()
    if g.role != 'student':
        flash("Learning Lab is for students only", "error")
        return redirect(url_for('dashboard'))

    student = Student.query.get(g.user_id)
    profile = LearningProfile.query.filter_by(student_id=g.user_id).first()

    return render_template('learning_strategies.html',
                         student=student,
                         profile=profile)


@app.route("/learning-lab/strategies/<strategy_key>/use", methods=["POST"])
def track_strategy_use(strategy_key):
    \"\"\"Track when a student uses a learning strategy\"\"\"
    init_user()
    if g.role != 'student':
        return jsonify({'error': 'Unauthorized'}), 403

    from datetime import datetime

    # Find or create strategy usage record
    usage = StrategyUsage.query.filter_by(
        student_id=g.user_id,
        strategy_key=strategy_key
    ).first()

    if usage:
        usage.times_used += 1
        usage.last_used_at = datetime.utcnow()
    else:
        category = request.json.get('category', 'general')
        usage = StrategyUsage(
            student_id=g.user_id,
            strategy_key=strategy_key,
            category=category,
            times_used=1
        )
        db.session.add(usage)

    db.session.commit()

    return jsonify({'success': True, 'times_used': usage.times_used})


@app.route("/learning-lab/strategies/<strategy_key>/rate", methods=["POST"])
def rate_strategy(strategy_key):
    \"\"\"Rate how helpful a strategy was\"\"\"
    init_user()
    if g.role != 'student':
        return jsonify({'error': 'Unauthorized'}), 403

    rating = request.json.get('rating')  # 1-5 stars
    notes = request.json.get('notes', '')

    usage = StrategyUsage.query.filter_by(
        student_id=g.user_id,
        strategy_key=strategy_key
    ).first()

    if usage:
        usage.helpfulness_rating = rating
        usage.student_notes = notes
        db.session.commit()
        return jsonify({'success': True})
    else:
        return jsonify({'error': 'Strategy not found'}), 404


@app.route("/learning-lab/tools")
def learning_lab_tools():
    \"\"\"Learning tools page with interactive tools\"\"\"
    init_user()
    if g.role != 'student':
        flash("Learning Lab is for students only", "error")
        return redirect(url_for('dashboard'))

    student = Student.query.get(g.user_id)
    profile = LearningProfile.query.filter_by(student_id=g.user_id).first()

    return render_template('learning_tools.html',
                         student=student,
                         profile=profile)
"""

# Print the routes for manual addition
if __name__ == "__main__":
    print(LEARNING_LAB_ROUTES)
