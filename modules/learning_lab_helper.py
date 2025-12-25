"""
Learning Lab Helper Functions
Handles quiz processing, profile generation, and parent/teacher notifications
"""

import json
from datetime import datetime
from flask_mail import Message
from models import db, Student, Parent, Teacher, LearningProfile, StrategyUsage


def process_quiz_results(student_id, quiz_answers):
    """
    Process quiz results and generate learning profile.

    Args:
        student_id: ID of the student
        quiz_answers: Dictionary of question_id: answer_value

    Returns:
        LearningProfile object
    """
    student = Student.query.get(student_id)
    if not student:
        return None

    # Get or create profile
    profile = LearningProfile.query.filter_by(student_id=student_id).first()
    if not profile:
        profile = LearningProfile(student_id=student_id)
        db.session.add(profile)

    # Update profile from quiz answers
    profile.quiz_completed = True
    profile.quiz_completed_at = datetime.utcnow()

    # Learning style preferences
    profile.primary_learning_style = quiz_answers.get('learning_style')
    if quiz_answers.get('memory_style') and quiz_answers.get('memory_style') != profile.primary_learning_style:
        profile.secondary_learning_style = quiz_answers.get('memory_style')

    # Study preferences
    profile.focus_preference = quiz_answers.get('focus_preference')
    profile.best_study_time = quiz_answers.get('best_study_time')
    profile.study_environment = quiz_answers.get('study_environment')
    profile.break_frequency = quiz_answers.get('break_frequency')

    # Processing preferences
    processing = quiz_answers.get('processing_style', '')
    profile.prefers_step_by_step = 'step_by_step' in processing
    profile.prefers_big_picture = 'big_picture' in processing
    profile.processing_speed = 'methodical' if quiz_answers.get('task_approach') in ['overwhelmed', 'make_plan'] else 'moderate'

    # Memory preferences
    profile.memory_style = quiz_answers.get('memory_style')
    profile.uses_mnemonics = quiz_answers.get('memory_style') in ['hear_words', 'see_images']

    # Reading preferences
    profile.reading_preference = quiz_answers.get('reading_preference')
    profile.prefers_large_text = quiz_answers.get('text_size') == 'larger'
    profile.prefers_colored_backgrounds = quiz_answers.get('reading_preference') == 'highlight_visual'

    # Generate strengths summary
    profile.strengths_summary = generate_strengths_summary(quiz_answers)

    db.session.commit()

    return profile


def generate_strengths_summary(quiz_answers):
    """Generate friendly summary of student's learning strengths."""

    strengths = []

    # Learning style strength
    style = quiz_answers.get('learning_style', '')
    if style == 'visual':
        strengths.append("Visual Learner - You remember what you see! Colors, diagrams, and videos help you learn.")
    elif style == 'auditory':
        strengths.append("Auditory Learner - You learn by listening! Discussions and explanations stick with you.")
    elif style == 'kinesthetic':
        strengths.append("Hands-On Learner - You learn by doing! Building and moving helps you understand.")
    elif style == 'reading_writing':
        strengths.append("Reading/Writing Learner - You learn through words! Notes and reading help you master concepts.")

    # Focus strength
    focus = quiz_answers.get('focus_preference', '')
    if focus == 'short_bursts':
        strengths.append("Sprint Learner - You work best in focused bursts with breaks.")
    elif focus in ['medium_sessions', 'long_sessions']:
        strengths.append("Deep Focus Thinker - You can concentrate for extended periods.")

    # Processing strength
    processing = quiz_answers.get('processing_style', '')
    if processing == 'step_by_step':
        strengths.append("Detail-Oriented - You excel at following step-by-step processes.")
    elif processing == 'big_picture':
        strengths.append("Big Picture Thinker - You understand concepts by seeing how everything connects.")
    elif processing == 'trial_and_error':
        strengths.append("Experimental Learner - You learn best by trying things out.")

    # Movement strength
    movement = quiz_answers.get('movement_while_learning', '')
    if movement == 'need_movement':
        strengths.append("Movement Thinker - Your brain works best when your body is active!")

    return " | ".join(strengths)


def send_parent_notification(student_id, profile):
    """
    Send email notification to parent about child's learning profile.
    """
    from app import mail

    student = Student.query.get(student_id)
    if not student or not student.parent_id:
        return False

    parent = Parent.query.get(student.parent_id)
    if not parent or not parent.email or not parent.email_reports_enabled:
        return False

    # Create email
    subject = f"🧠 {student.student_name}'s Learning Profile - CozmicLearning"

    html_body = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                margin: 0;
                padding: 20px;
            }}
            .container {{
                max-width: 600px;
                margin: 0 auto;
                background: #ffffff;
                border-radius: 16px;
                overflow: hidden;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            }}
            .header {{
                background: linear-gradient(135deg, #f093fb, #f5576c);
                color: white;
                padding: 30px;
                text-align: center;
            }}
            .header h1 {{
                margin: 0;
                font-size: 28px;
                font-weight: 700;
            }}
            .content {{
                padding: 30px;
            }}
            .disclaimer {{
                background: #fff3cd;
                border-left: 4px solid #ffc107;
                padding: 15px;
                border-radius: 8px;
                margin: 20px 0;
                color: #856404;
            }}
            .profile-section {{
                margin: 20px 0;
                padding: 20px;
                background: #f8f9ff;
                border-radius: 12px;
            }}
            .profile-section h3 {{
                color: #f5576c;
                margin: 0 0 15px 0;
            }}
            .strength {{
                padding: 10px;
                margin: 8px 0;
                background: white;
                border-left: 3px solid #667eea;
                border-radius: 6px;
            }}
            .btn {{
                display: inline-block;
                padding: 12px 30px;
                background: linear-gradient(135deg, #f093fb, #f5576c);
                color: white;
                text-decoration: none;
                border-radius: 8px;
                font-weight: 600;
                margin-top: 20px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🧠 Learning Profile Created</h1>
                <p>{student.student_name} completed the Learning Strengths Quiz!</p>
            </div>

            <div class="content">
                <div class="disclaimer">
                    <strong>⚠️ Important:</strong> This profile shows learning <strong>preferences</strong>,
                    not diagnoses. If you have concerns about learning challenges, please consult
                    with educational or medical professionals.
                </div>

                <div class="profile-section">
                    <h3>Learning Strengths</h3>
                    <p style="line-height: 1.8;">{profile.strengths_summary}</p>
                </div>

                <div class="profile-section">
                    <h3>Key Preferences</h3>
                    <div class="strength">
                        <strong>Primary Learning Style:</strong> {profile.primary_learning_style.replace('_', ' ').title()}
                    </div>
                    <div class="strength">
                        <strong>Focus Pattern:</strong> {profile.focus_preference.replace('_', ' ').title()}
                    </div>
                    <div class="strength">
                        <strong>Best Study Time:</strong> {profile.best_study_time.title() if profile.best_study_time else 'Not specified'}
                    </div>
                    <div class="strength">
                        <strong>Study Environment:</strong> {profile.study_environment.replace('_', ' ').title() if profile.study_environment else 'Not specified'}
                    </div>
                </div>

                <div class="profile-section">
                    <h3>What This Means</h3>
                    <p>
                        {student.student_name} will now see personalized learning strategies and tools
                        matched to their preferences. They can explore the Strategy Library to find
                        techniques that work for their unique learning style.
                    </p>
                    <p style="margin-top: 15px;">
                        As a parent, you can support their learning by:
                        <ul>
                            <li>Encouraging them to try recommended strategies</li>
                            <li>Providing a study environment that matches their preferences</li>
                            <li>Respecting their natural learning rhythms and break needs</li>
                        </ul>
                    </p>
                </div>

                <div style="text-align: center;">
                    <a href="https://cozmiclearning.com/parent/analytics" class="btn">View Full Profile →</a>
                </div>
            </div>

            <div style="background: #f8f9ff; padding: 20px; text-align: center; color: #666; font-size: 14px;">
                <p>Keep supporting {student.student_name}'s learning journey! 🌟</p>
                <p style="font-size: 12px; color: #999; margin-top: 10px;">
                    <a href="https://cozmiclearning.com/parent/email-preferences" style="color: #f5576c;">Update email preferences</a>
                </p>
            </div>
        </div>
    </body>
    </html>
    """

    text_body = f"""
CozmicLearning - Learning Profile Created

{student.student_name} completed the Learning Strengths Quiz!

IMPORTANT: This profile shows learning preferences, not diagnoses.

Learning Strengths:
{profile.strengths_summary}

Key Preferences:
- Primary Learning Style: {profile.primary_learning_style.replace('_', ' ').title()}
- Focus Pattern: {profile.focus_preference.replace('_', ' ').title()}
- Best Study Time: {profile.best_study_time.title() if profile.best_study_time else 'Not specified'}

View full profile: https://cozmiclearning.com/parent/analytics
    """

    msg = Message(
        subject=subject,
        recipients=[parent.email],
        html=html_body,
        body=text_body
    )

    try:
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Failed to send parent notification: {e}")
        return False


def send_teacher_notification(student_id, profile):
    """
    Send notification to teacher about student's learning profile (for assigned classes).
    """
    from app import mail

    student = Student.query.get(student_id)
    if not student:
        return False

    # Find teachers who have this student in their classes
    # Note: This assumes the student is enrolled in classes
    from models import Class
    classes = Class.query.filter(Class.students.contains(student)).all()

    if not classes:
        return False

    sent_count = 0
    for cls in classes:
        teacher = cls.teacher
        if not teacher or not teacher.email:
            continue

        subject = f"🧠 Student Learning Profile: {student.student_name}"

        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background: #f5f5f5;
                    padding: 20px;
                }}
                .container {{
                    max-width: 600px;
                    margin: 0 auto;
                    background: white;
                    border-radius: 12px;
                    overflow: hidden;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                }}
                .header {{
                    background: linear-gradient(135deg, #667eea, #764ba2);
                    color: white;
                    padding: 20px;
                }}
                .content {{
                    padding: 25px;
                }}
                .highlight {{
                    background: #f8f9ff;
                    padding: 15px;
                    border-radius: 8px;
                    margin: 15px 0;
                    border-left: 4px solid #667eea;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h2>Student Learning Profile Update</h2>
                    <p>{student.student_name} - {cls.class_name}</p>
                </div>
                <div class="content">
                    <p>Hello {teacher.name},</p>

                    <p>{student.student_name} has completed the Learning Lab quiz and discovered their learning preferences.</p>

                    <div class="highlight">
                        <strong>Primary Learning Style:</strong> {profile.primary_learning_style.replace('_', ' ').title()}<br>
                        <strong>Focus Pattern:</strong> {profile.focus_preference.replace('_', ' ').title()}<br>
                        <strong>Processing Style:</strong> {'Step-by-step' if profile.prefers_step_by_step else 'Big picture' if profile.prefers_big_picture else 'Mixed'}
                    </div>

                    <p><strong>Teaching Considerations:</strong></p>
                    <ul>
                        <li>Provide materials in formats matching their learning style</li>
                        <li>Allow for their preferred break and focus patterns</li>
                        <li>Consider these preferences when giving feedback and support</li>
                    </ul>

                    <p style="font-size: 0.9rem; color: #666; margin-top: 20px;">
                        <em>Note: This shows learning preferences, not diagnoses. This information can help you
                        better support {student.student_name}'s learning, but should not replace professional
                        assessments for accommodations.</em>
                    </p>
                </div>
            </div>
        </body>
        </html>
        """

        msg = Message(
            subject=subject,
            recipients=[teacher.email],
            html=html_body
        )

        try:
            mail.send(msg)
            sent_count += 1
        except Exception as e:
            print(f"Failed to send teacher notification to {teacher.email}: {e}")

    return sent_count > 0


def get_recommended_strategies(profile):
    """
    Get recommended learning strategies based on student's profile.

    Returns:
        List of strategy dictionaries with keys: category, name, description, key
    """
    strategies = []

    # Focus strategies
    if profile.focus_preference in ['short_bursts', 'every_15_min']:
        strategies.append({
            'category': 'focus',
            'name': 'Pomodoro Technique',
            'description': 'Study for 25 minutes, break for 5. Repeat 4 times, then take a longer break.',
            'key': 'pomodoro_timer'
        })
        strategies.append({
            'category': 'focus',
            'name': 'Movement Breaks',
            'description': 'Take a 2-minute movement break every 15-20 minutes to reset your focus.',
            'key': 'movement_breaks'
        })

    # Reading strategies
    if profile.reading_preference in ['hear_it', 'all_methods']:
        strategies.append({
            'category': 'reading',
            'name': 'Text-to-Speech',
            'description': 'Use built-in text-to-speech to hear content while reading along.',
            'key': 'text_to_speech'
        })

    if profile.prefers_large_text or profile.prefers_colored_backgrounds:
        strategies.append({
            'category': 'reading',
            'name': 'Reading Customization',
            'description': 'Adjust text size, fonts, and background colors to reduce eye strain.',
            'key': 'reading_customization'
        })

    # Visual learning strategies
    if profile.primary_learning_style == 'visual':
        strategies.append({
            'category': 'study',
            'name': 'Visual Note-Taking',
            'description': 'Use mind maps, diagrams, and color-coding to organize information visually.',
            'key': 'visual_notes'
        })
        strategies.append({
            'category': 'study',
            'name': 'Color Coding',
            'description': 'Assign colors to different topics or types of information.',
            'key': 'color_coding'
        })

    # Auditory learning strategies
    if profile.primary_learning_style == 'auditory':
        strategies.append({
            'category': 'study',
            'name': 'Explain Aloud',
            'description': 'Teach concepts to yourself or others out loud to reinforce learning.',
            'key': 'teach_aloud'
        })
        strategies.append({
            'category': 'study',
            'name': 'Record Summaries',
            'description': 'Record yourself explaining key concepts and listen back.',
            'key': 'audio_summaries'
        })

    # Kinesthetic learning strategies
    if profile.primary_learning_style == 'kinesthetic':
        strategies.append({
            'category': 'study',
            'name': 'Hands-On Practice',
            'description': 'Use physical objects, build models, or act out concepts.',
            'key': 'hands_on'
        })
        strategies.append({
            'category': 'study',
            'name': 'Walking Study Sessions',
            'description': 'Review flashcards or listen to lessons while walking or moving.',
            'key': 'walking_study'
        })

    # Organization strategies
    if profile.processing_speed == 'methodical' or profile.prefers_step_by_step:
        strategies.append({
            'category': 'organization',
            'name': 'Task Breakdown',
            'description': 'Break big assignments into tiny, manageable steps.',
            'key': 'task_breakdown'
        })
        strategies.append({
            'category': 'organization',
            'name': 'Checklist System',
            'description': 'Use checklists to track progress and stay organized.',
            'key': 'checklists'
        })

    return strategies


def get_contextual_learning_tips(student_id, context='general'):
    """
    Get personalized learning tips based on context (assignment, study, test prep, etc.)
    Now returns MULTIPLE learning style approaches to prevent pigeon-holing students.

    Args:
        student_id: ID of the student
        context: Where the student is (assignment, powergrid, test_prep, general)

    Returns:
        Dictionary with tips, tools, strategies, and ALTERNATIVE approaches
    """
    profile = LearningProfile.query.filter_by(student_id=student_id).first()

    # Default tips if no profile
    if not profile or not profile.quiz_completed:
        return {
            'has_profile': False,
            'cta': 'Take the Learning Lab quiz to get personalized study tips!',
            'cta_link': '/learning-lab/quiz'
        }

    tips = []
    tools = []
    quick_strategies = []
    alternative_approaches = []  # NEW: Alternative learning style suggestions

    # Helper to generate style-specific tips for ANY style
    def get_style_tips_for_context(style, ctx):
        """Generate tips for any learning style and context"""
        style_tips = []

        if ctx == 'assignment':
            if style == 'visual':
                style_tips.append("Create a visual outline or diagram before starting")
            elif style == 'auditory':
                style_tips.append("Talk through the assignment steps out loud")
            elif style == 'kinesthetic':
                style_tips.append("Use physical objects or manipulatives to model the problem")
            elif style == 'reading_writing':
                style_tips.append("Write out a detailed plan with clear sections")

        elif ctx == 'powergrid':
            if style == 'visual':
                style_tips.append("Pay special attention to diagrams and visual explanations")
            elif style == 'auditory':
                style_tips.append("Read the study guide out loud or use text-to-speech")
            elif style == 'kinesthetic':
                style_tips.append("Take a 2-minute movement break every 15 minutes")
            elif style == 'reading_writing':
                style_tips.append("Take detailed notes as you read through each section")

        elif ctx == 'test_prep':
            if style == 'visual':
                style_tips.append("Create color-coded study cards and visual summaries")
            elif style == 'auditory':
                style_tips.append("Create songs or rhymes to remember key facts")
            elif style == 'kinesthetic':
                style_tips.append("Use flashcards you can shuffle and sort physically")
            elif style == 'reading_writing':
                style_tips.append("Write practice questions and detailed answer explanations")

        elif ctx == 'practice':
            if style == 'visual':
                style_tips.append("Draw out problems or create visual representations")
            elif style == 'auditory':
                style_tips.append("Explain your reasoning out loud as you solve each problem")
            elif style == 'kinesthetic':
                style_tips.append("Use movements or gestures to represent key concepts")
            elif style == 'reading_writing':
                style_tips.append("Write out your thought process step-by-step")

        return style_tips

    # PRIMARY STYLE TIPS (Recommended based on profile)
    primary_style = profile.primary_learning_style
    tips = get_style_tips_for_context(primary_style, context)

    # ALTERNATIVE STYLE TIPS (Prevent pigeon-holing)
    all_styles = ['visual', 'auditory', 'kinesthetic', 'reading_writing']
    other_styles = [s for s in all_styles if s != primary_style]

    # Add 2-3 alternative approaches
    for alt_style in other_styles[:2]:
        alt_tips = get_style_tips_for_context(alt_style, context)
        if alt_tips:
            alternative_approaches.append({
                'style': alt_style.replace('_', ' ').title(),
                'style_key': alt_style,
                'icon': {'visual': '👁️', 'auditory': '👂', 'kinesthetic': '🤸', 'reading_writing': '📝'}.get(alt_style, '💡'),
                'tip': alt_tips[0]
            })

    # Context-specific tools and strategies
    if context == 'assignment':
        if profile.focus_preference in ['short_bursts', 'every_15_min']:
            tips.append("Break this assignment into 15-minute chunks with quick breaks")
            tools.append({'name': 'Pomodoro Timer', 'icon': '⏰', 'link': '/learning-lab/tools#pomodoro'})

        if profile.primary_learning_style == 'visual':
            quick_strategies.append("Use colors to organize your work")

        if profile.prefers_step_by_step:
            tips.append("List out each small step before you begin")
            tools.append({'name': 'Task Breakdown Tool', 'icon': '✂️', 'link': '/learning-lab/tools#task-breakdown'})

    elif context == 'powergrid':
        if profile.reading_preference == 'hear_it':
            tools.append({'name': 'Text-to-Speech', 'icon': '🔊', 'link': '/learning-lab/tools#tts'})

        if profile.focus_preference in ['short_bursts', 'every_15_min']:
            tips.append("Study one section at a time with 5-minute breaks")

    elif context == 'test_prep':
        if profile.memory_style == 'hear_words':
            quick_strategies.append("Explain concepts aloud in your own words")

        tools.append({'name': 'Study Schedule Generator', 'icon': '📅', 'link': '/learning-lab/tools#schedule'})

    elif context == 'practice':
        if profile.focus_preference in ['short_bursts', 'every_15_min']:
            tips.append("Do 5-10 questions, then take a 2-minute break")

    # General tips based on time of day
    import datetime
    current_hour = datetime.datetime.now().hour

    if profile.best_study_time:
        if profile.best_study_time == 'morning' and current_hour > 14:
            tips.append("💡 You usually learn best in the morning - save harder tasks for tomorrow!")
        elif profile.best_study_time == 'evening' and current_hour < 12:
            tips.append("💡 Your peak learning time is often evening - this is great for review!")
        elif profile.best_study_time == 'night' and current_hour < 18:
            tips.append("💡 You often focus best at night - save deep learning for later!")

    # Add universal helpful tools
    if not tools:
        if profile.focus_preference in ['short_bursts', 'medium_sessions']:
            tools.append({'name': 'Focus Timer', 'icon': '⏰', 'link': '/learning-lab/tools#pomodoro'})

    return {
        'has_profile': True,
        'tips': tips[:2],  # Primary style tips (recommended)
        'tools': tools[:2],  # Helpful tools
        'quick_strategies': quick_strategies[:3],
        'primary_style': primary_style.replace('_', ' ').title(),
        'primary_style_key': primary_style,
        'alternative_approaches': alternative_approaches,  # NEW: Other learning styles to try
        'strengths_preview': profile.strengths_summary.split('|')[0].strip() if profile.strengths_summary else '',
        'profile_link': '/learning-lab/profile',
        'flexibility_message': 'These are your preferences - feel free to mix and match what works best!'  # NEW: Growth mindset message
    }


def adapt_content_to_learning_style(content, learning_style):
    """
    Add learning-style-specific prompts to content (for PowerGrid, etc.)

    Args:
        content: The original content text
        learning_style: visual, auditory, kinesthetic, reading_writing

    Returns:
        Enhanced content with style-specific suggestions
    """
    enhancements = []

    if learning_style == 'visual':
        enhancements.append("\n\n💡 **Visual Learner Tip**: Try sketching a diagram of these concepts as you read.")
        enhancements.append("Consider using highlighters or colored pens to organize information by category.")

    elif learning_style == 'auditory':
        enhancements.append("\n\n💡 **Auditory Learner Tip**: Read this guide aloud or use text-to-speech.")
        enhancements.append("Try explaining each section to yourself in your own words before moving on.")

    elif learning_style == 'kinesthetic':
        enhancements.append("\n\n💡 **Hands-On Learner Tip**: Take a 2-minute movement break every 15 minutes.")
        enhancements.append("If possible, create a hands-on activity or real-world example for each concept.")

    elif learning_style == 'reading_writing':
        enhancements.append("\n\n💡 **Reading/Writing Learner Tip**: Take detailed notes as you read.")
        enhancements.append("Write a summary in your own words at the end of each section.")

    return content + "\n".join(enhancements)


def send_parent_notification_flagged_content(student_id, message_content, flag_reason, flag_categories):
    """
    Send email notification to parent about flagged AI Study Buddy content.

    Args:
        student_id: ID of the student
        message_content: The flagged message text
        flag_reason: Human-readable reason for flagging
        flag_categories: Dictionary of flagged categories from moderation

    Returns:
        bool: True if notification sent successfully
    """
    from app import mail

    student = Student.query.get(student_id)
    if not student or not student.parent_id:
        return False

    parent = Parent.query.get(student.parent_id)
    if not parent or not parent.email or not parent.email_reports_enabled:
        return False

    # Determine severity level
    serious_categories = ['violence', 'violence/graphic', 'sexual', 'sexual/minors', 'self-harm', 'self-harm/intent', 'self-harm/instructions']
    has_serious_violation = any(flag_categories.get(cat, False) for cat in serious_categories)

    severity = "URGENT" if has_serious_violation else "Important"
    severity_color = "#dc3545" if has_serious_violation else "#ffc107"

    # Create email
    subject = f"🚨 {severity}: AI Study Buddy Content Alert - {student.student_name}"

    # Truncate message for email (show first 200 chars)
    message_preview = message_content[:200] + "..." if len(message_content) > 200 else message_content

    html_body = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                margin: 0;
                padding: 20px;
            }}
            .container {{
                max-width: 600px;
                margin: 0 auto;
                background: #ffffff;
                border-radius: 16px;
                overflow: hidden;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            }}
            .header {{
                background: {severity_color};
                color: white;
                padding: 30px;
                text-align: center;
            }}
            .header h1 {{
                margin: 0;
                font-size: 28px;
                font-weight: 700;
            }}
            .content {{
                padding: 30px;
            }}
            .alert-box {{
                background: #fff3cd;
                border-left: 4px solid {severity_color};
                padding: 20px;
                border-radius: 8px;
                margin: 20px 0;
            }}
            .message-preview {{
                background: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 8px;
                padding: 15px;
                margin: 15px 0;
                font-family: monospace;
                color: #495057;
            }}
            .categories {{
                margin: 15px 0;
            }}
            .category-tag {{
                display: inline-block;
                background: #dc3545;
                color: white;
                padding: 4px 12px;
                border-radius: 12px;
                font-size: 0.85rem;
                margin: 4px;
            }}
            .action-section {{
                background: #e7f3ff;
                border-left: 4px solid #0066cc;
                padding: 20px;
                border-radius: 8px;
                margin: 20px 0;
            }}
            .btn {{
                display: inline-block;
                padding: 12px 30px;
                background: linear-gradient(135deg, #667eea, #764ba2);
                color: white;
                text-decoration: none;
                border-radius: 8px;
                font-weight: 600;
                margin-top: 10px;
            }}
            .footer {{
                background: #f8f9ff;
                padding: 20px;
                text-align: center;
                color: #666;
                font-size: 14px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🚨 Content Safety Alert</h1>
                <p>AI Study Buddy - CozmicLearning</p>
            </div>

            <div class="content">
                <div class="alert-box">
                    <strong>⚠️ {severity} Notice:</strong><br>
                    {student.student_name}'s message to the AI Study Buddy was flagged for review.
                </div>

                <h3>Flagged Message:</h3>
                <div class="message-preview">
                    {message_preview}
                </div>

                <h3>Reason for Flagging:</h3>
                <p><strong>{flag_reason}</strong></p>

                <div class="categories">
                    <strong>Flagged Categories:</strong><br>
                    {' '.join([f'<span class="category-tag">{cat.replace("/", " / ").replace("_", " ").title()}</span>' for cat, flagged in flag_categories.items() if flagged])}
                </div>

                <div class="action-section">
                    <h3>What Happens Next?</h3>
                    <ul>
                        <li>The message has been blocked and saved for teacher review</li>
                        <li>{'A teacher will follow up within 24 hours' if has_serious_violation else 'This will be reviewed by your student\'s teacher'}</li>
                        <li>We recommend having a conversation with {student.student_name} about appropriate AI tool usage</li>
                    </ul>

                    <h3>Content Safety Guidelines:</h3>
                    <p>The AI Study Buddy is designed to help students learn through guided questions. Content that is violent, sexual, or involves cheating is not permitted.</p>
                </div>

                <div style="text-align: center;">
                    <p><strong>This is an automated notification from our content safety system.</strong></p>
                    <a href="https://cozmiclearning.com/parent/analytics" class="btn">View Student Activity →</a>
                </div>
            </div>

            <div class="footer">
                <p>Questions? Contact your student's teacher or CozmicLearning support.</p>
                <p style="font-size: 12px; color: #999; margin-top: 10px;">
                    <a href="https://cozmiclearning.com/parent/email-preferences" style="color: #667eea;">Update email preferences</a>
                </p>
            </div>
        </div>
    </body>
    </html>
    """

    text_body = f"""
CozmicLearning - Content Safety Alert

{severity} Notice:
{student.student_name}'s message to the AI Study Buddy was flagged for review.

Flagged Message:
{message_preview}

Reason: {flag_reason}

What Happens Next:
- The message has been blocked and saved for teacher review
- {'A teacher will follow up within 24 hours' if has_serious_violation else 'This will be reviewed by your student\'s teacher'}
- We recommend having a conversation with {student.student_name} about appropriate AI tool usage

Content Safety Guidelines:
The AI Study Buddy is designed to help students learn through guided questions. Content that is violent, sexual, or involves cheating is not permitted.

View student activity: https://cozmiclearning.com/parent/analytics
    """

    msg = Message(
        subject=subject,
        recipients=[parent.email],
        html=html_body,
        body=text_body
    )

    try:
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Failed to send parent notification for flagged content: {e}")
        return False


def get_learning_toolkit_widget(student_id):
    """
    Get HTML for a persistent learning toolkit widget

    Returns:
        HTML string for widget
    """
    profile = LearningProfile.query.filter_by(student_id=student_id).first()

    if not profile or not profile.quiz_completed:
        return f"""
        <div class="learning-toolkit-widget">
            <div class="toolkit-header">
                <span class="toolkit-icon">🧠</span>
                <span class="toolkit-title">Learning Lab</span>
            </div>
            <div class="toolkit-content">
                <p class="toolkit-cta">Discover your learning superpowers!</p>
                <a href="/learning-lab/quiz" class="toolkit-btn">Take Quiz →</a>
            </div>
        </div>
        """

    # Get top 3 most-used tools
    top_tools = StrategyUsage.query.filter_by(student_id=student_id).order_by(
        StrategyUsage.times_used.desc()
    ).limit(3).all()

    tools_html = ""
    tool_links = {
        'pomodoro_timer': '/learning-lab/tools#pomodoro',
        'text_to_speech': '/learning-lab/tools#tts',
        'task_breakdown': '/learning-lab/tools#task-breakdown',
        'reading_customization': '/learning-lab/tools#reading',
        'study_schedule': '/learning-lab/tools#schedule'
    }

    if top_tools:
        for tool in top_tools:
            link = tool_links.get(tool.strategy_key, '/learning-lab/tools')
            tools_html += f'<a href="{link}" class="toolkit-quick-link">🔧 {tool.strategy_key.replace("_", " ").title()}</a>'
    else:
        # Default tools based on profile
        if profile.focus_preference in ['short_burts', 'every_15_min']:
            tools_html += '<a href="/learning-lab/tools#pomodoro" class="toolkit-quick-link">⏰ Focus Timer</a>'
        if profile.reading_preference in ['hear_it', 'all_methods']:
            tools_html += '<a href="/learning-lab/tools#tts" class="toolkit-quick-link">🔊 Text-to-Speech</a>'
        if profile.prefers_step_by_step:
            tools_html += '<a href="/learning-lab/tools#task-breakdown" class="toolkit-quick-link">✂️ Task Breakdown</a>'

    style_emoji = {
        'visual': '👁️',
        'auditory': '👂',
        'kinesthetic': '🤸',
        'reading_writing': '📝'
    }

    return f"""
    <div class="learning-toolkit-widget">
        <div class="toolkit-header">
            <span class="toolkit-icon">{style_emoji.get(profile.primary_learning_style, '🧠')}</span>
            <span class="toolkit-title">My Learning Tools</span>
        </div>
        <div class="toolkit-content">
            <div class="toolkit-strength">{profile.strengths_summary.split('|')[0].strip() if profile.strengths_summary else 'Learning Profile Active'}</div>
            <div class="toolkit-tools">
                {tools_html if tools_html else '<a href="/learning-lab/tools" class="toolkit-quick-link">🔧 Explore Tools</a>'}
            </div>
            <a href="/learning-lab" class="toolkit-link">View All Strategies →</a>
        </div>
    </div>
    """
