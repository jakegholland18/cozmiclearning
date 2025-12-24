"""
Parent Weekly Summary Email System
Sends automated weekly progress reports to parents
"""

from datetime import datetime, timedelta
from typing import List, Dict
from flask_mail import Message
from models import db, Parent, Student, AssessmentResult, AssignedQuestion
from sqlalchemy import func

def generate_weekly_summary(parent_id: int) -> Dict:
    """
    Generate weekly summary data for a parent.

    Returns dict with:
    - student_summaries: List of per-student summaries
    - week_start: Start date of the week
    - week_end: End date of the week
    """
    parent = Parent.query.get(parent_id)
    if not parent:
        return None

    # Get week boundaries (Monday to Sunday)
    today = datetime.today()
    week_start = today - timedelta(days=today.weekday())  # Monday
    week_end = week_start + timedelta(days=6)  # Sunday

    week_start_str = week_start.strftime('%Y-%m-%d')
    week_end_str = week_end.strftime('%Y-%m-%d')

    # Get all students for this parent
    students = Student.query.filter_by(parent_id=parent_id).all()

    student_summaries = []

    for student in students:
        summary = generate_student_summary(student, week_start_str, week_end_str)
        student_summaries.append(summary)

    return {
        'parent': parent,
        'student_summaries': student_summaries,
        'week_start': week_start.strftime('%B %d, %Y'),
        'week_end': week_end.strftime('%B %d, %Y')
    }


def generate_student_summary(student: Student, week_start: str, week_end: str) -> Dict:
    """
    Generate summary for a single student for the week.
    """
    # Get assignments completed this week
    assignments_completed = db.session.query(func.count(AssignedQuestion.id)).filter(
        AssignedQuestion.student_id == student.id,
        AssignedQuestion.submitted_at >= week_start,
        AssignedQuestion.submitted_at <= week_end
    ).scalar() or 0

    # Get grades received this week
    grades = AssessmentResult.query.filter(
        AssessmentResult.student_id == student.id,
        AssessmentResult.completed_at >= week_start,
        AssessmentResult.completed_at <= week_end
    ).all()

    avg_score = 0
    if grades:
        total_score = sum(g.score or 0 for g in grades)
        avg_score = round(total_score / len(grades), 1)

    # Get subjects practiced
    subjects_practiced = db.session.query(
        func.distinct(AssignedQuestion.subject)
    ).filter(
        AssignedQuestion.student_id == student.id,
        AssignedQuestion.submitted_at >= week_start,
        AssignedQuestion.submitted_at <= week_end
    ).all()

    subjects_list = [s[0].replace('_', ' ').title() for s in subjects_practiced]

    # Estimate time spent (rough calculation)
    # Assume 2 minutes per question on average
    time_spent_minutes = assignments_completed * 2
    time_spent_hours = round(time_spent_minutes / 60, 1)

    # Get new badges (if tracking exists)
    # For now, we'll skip badges - can be added later

    # Determine areas needing attention
    areas_needing_attention = []

    # Check for assignments with low scores
    low_score_assignments = [g for g in grades if g.score and g.score < 70]
    if low_score_assignments:
        low_subjects = set(a.assignment.subject if hasattr(a.assignment, 'subject') else 'Unknown'
                          for a in low_score_assignments[:3])
        for subj in low_subjects:
            areas_needing_attention.append(f"{subj.replace('_', ' ').title()} - scores below 70%")

    # Check for incomplete assignments
    incomplete_count = db.session.query(func.count(AssignedQuestion.id)).filter(
        AssignedQuestion.student_id == student.id,
        AssignedQuestion.submitted_at.is_(None)
    ).scalar() or 0

    if incomplete_count > 3:
        areas_needing_attention.append(f"{incomplete_count} incomplete assignments")

    return {
        'student': student,
        'assignments_completed': assignments_completed,
        'average_score': avg_score,
        'subjects_practiced': subjects_list,
        'time_spent_hours': time_spent_hours,
        'areas_needing_attention': areas_needing_attention,
        'grades_count': len(grades)
    }


def send_weekly_summary_email(mail, parent_id: int) -> bool:
    """
    Send weekly summary email to a parent.

    Args:
        mail: Flask-Mail instance
        parent_id: ID of the parent

    Returns:
        True if sent successfully, False otherwise
    """
    summary_data = generate_weekly_summary(parent_id)

    if not summary_data:
        print(f"No summary data for parent {parent_id}")
        return False

    parent = summary_data['parent']

    if not parent.email:
        print(f"No email for parent {parent_id}")
        return False

    # Generate HTML email
    html_body = render_email_template(summary_data)

    # Generate plain text version
    text_body = render_text_email(summary_data)

    # Create message
    msg = Message(
        subject=f"CozmicLearning Weekly Summary - {summary_data['week_end']}",
        recipients=[parent.email],
        html=html_body,
        body=text_body
    )

    try:
        mail.send(msg)
        print(f"✅ Weekly summary sent to {parent.email}")
        return True
    except Exception as e:
        print(f"❌ Failed to send weekly summary to {parent.email}: {e}")
        return False


def render_email_template(data: Dict) -> str:
    """Generate HTML email content."""
    parent = data['parent']
    summaries = data['student_summaries']
    week_start = data['week_start']
    week_end = data['week_end']

    html = f"""
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
                background: linear-gradient(135deg, #5c6bff, #4facfe);
                color: white;
                padding: 30px;
                text-align: center;
            }}
            .header h1 {{
                margin: 0;
                font-size: 28px;
                font-weight: 700;
            }}
            .header p {{
                margin: 10px 0 0;
                font-size: 16px;
                opacity: 0.9;
            }}
            .content {{
                padding: 30px;
            }}
            .greeting {{
                font-size: 18px;
                color: #333;
                margin-bottom: 20px;
            }}
            .student-section {{
                background: #f8f9ff;
                border-radius: 12px;
                padding: 20px;
                margin-bottom: 20px;
                border-left: 4px solid #5c6bff;
            }}
            .student-name {{
                font-size: 20px;
                font-weight: 700;
                color: #5c6bff;
                margin-bottom: 15px;
            }}
            .stat-grid {{
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 15px;
                margin-bottom: 15px;
            }}
            .stat-box {{
                background: white;
                padding: 15px;
                border-radius: 8px;
                text-align: center;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
            }}
            .stat-number {{
                font-size: 32px;
                font-weight: 700;
                color: #5c6bff;
                margin-bottom: 5px;
            }}
            .stat-label {{
                font-size: 14px;
                color: #666;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }}
            .subjects-list {{
                background: white;
                padding: 15px;
                border-radius: 8px;
                margin-bottom: 15px;
            }}
            .subjects-list h4 {{
                margin: 0 0 10px;
                color: #333;
                font-size: 14px;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }}
            .subject-tag {{
                display: inline-block;
                padding: 6px 12px;
                background: linear-gradient(135deg, #5c6bff, #4facfe);
                color: white;
                border-radius: 6px;
                font-size: 13px;
                margin: 4px;
            }}
            .attention-box {{
                background: #fff3cd;
                border-left: 4px solid #ffc107;
                padding: 15px;
                border-radius: 8px;
                margin-top: 15px;
            }}
            .attention-box h4 {{
                margin: 0 0 10px;
                color: #856404;
                font-size: 14px;
            }}
            .attention-box ul {{
                margin: 0;
                padding-left: 20px;
                color: #856404;
            }}
            .footer {{
                background: #f8f9ff;
                padding: 20px 30px;
                text-align: center;
                color: #666;
                font-size: 14px;
            }}
            .btn {{
                display: inline-block;
                padding: 12px 30px;
                background: linear-gradient(135deg, #5c6bff, #4facfe);
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
                <h1>🚀 Weekly Progress Summary</h1>
                <p>{week_start} - {week_end}</p>
            </div>

            <div class="content">
                <div class="greeting">
                    Hi {parent.name or 'Parent'},
                </div>
                <p>Here's how your {'child' if len(summaries) == 1 else 'children'} did on CozmicLearning this week!</p>
    """

    # Add each student's summary
    for summary in summaries:
        student = summary['student']
        html += f"""
                <div class="student-section">
                    <div class="student-name">📚 {student.name}</div>

                    <div class="stat-grid">
                        <div class="stat-box">
                            <div class="stat-number">{summary['assignments_completed']}</div>
                            <div class="stat-label">Assignments Done</div>
                        </div>
                        <div class="stat-box">
                            <div class="stat-number">{summary['average_score']}%</div>
                            <div class="stat-label">Average Score</div>
                        </div>
                        <div class="stat-box">
                            <div class="stat-number">{summary['time_spent_hours']}</div>
                            <div class="stat-label">Hours Learned</div>
                        </div>
                        <div class="stat-box">
                            <div class="stat-number">{summary['grades_count']}</div>
                            <div class="stat-label">Grades Received</div>
                        </div>
                    </div>
        """

        if summary['subjects_practiced']:
            html += f"""
                    <div class="subjects-list">
                        <h4>Subjects Practiced</h4>
                        <div>
            """
            for subject in summary['subjects_practiced']:
                html += f'<span class="subject-tag">{subject}</span>'
            html += """
                        </div>
                    </div>
            """

        if summary['areas_needing_attention']:
            html += """
                    <div class="attention-box">
                        <h4>⚠️ Areas Needing Attention</h4>
                        <ul>
            """
            for area in summary['areas_needing_attention']:
                html += f"<li>{area}</li>"
            html += """
                        </ul>
                    </div>
            """

        html += """
                </div>
        """

    html += f"""
                <div style="text-align: center;">
                    <a href="https://cozmiclearning.com/parent/analytics" class="btn">View Detailed Analytics →</a>
                </div>
            </div>

            <div class="footer">
                <p>Keep up the great work! 🌟</p>
                <p style="font-size: 12px; color: #999; margin-top: 10px;">
                    You're receiving this because you enabled weekly summaries.<br>
                    <a href="https://cozmiclearning.com/parent/email-preferences" style="color: #5c6bff;">Update email preferences</a>
                </p>
            </div>
        </div>
    </body>
    </html>
    """

    return html


def render_text_email(data: Dict) -> str:
    """Generate plain text email content."""
    parent = data['parent']
    summaries = data['student_summaries']
    week_start = data['week_start']
    week_end = data['week_end']

    text = f"""
CozmicLearning Weekly Summary
{week_start} - {week_end}

Hi {parent.name or 'Parent'},

Here's how your {'child' if len(summaries) == 1 else 'children'} did on CozmicLearning this week!

"""

    for summary in summaries:
        student = summary['student']
        text += f"""
═══════════════════════════════════════
{student.name}
═══════════════════════════════════════

📊 This Week's Stats:
  • Assignments Completed: {summary['assignments_completed']}
  • Average Score: {summary['average_score']}%
  • Time Spent: {summary['time_spent_hours']} hours
  • Grades Received: {summary['grades_count']}

"""
        if summary['subjects_practiced']:
            text += f"📚 Subjects Practiced: {', '.join(summary['subjects_practiced'])}\n\n"

        if summary['areas_needing_attention']:
            text += "⚠️  Areas Needing Attention:\n"
            for area in summary['areas_needing_attention']:
                text += f"  • {area}\n"
            text += "\n"

    text += """
View detailed analytics: https://cozmiclearning.com/parent/analytics

Keep up the great work! 🌟

---
You're receiving this because you enabled weekly summaries.
Update preferences: https://cozmiclearning.com/parent/email-preferences
"""

    return text


def send_all_weekly_summaries(mail) -> Dict:
    """
    Send weekly summaries to all parents who have opted in.

    Returns dict with stats on how many were sent successfully.
    """
    # Get all parents with email enabled
    parents = Parent.query.filter(
        Parent.email.isnot(None),
        Parent.email_weekly_summary == True
    ).all()

    stats = {
        'total': len(parents),
        'sent': 0,
        'failed': 0
    }

    for parent in parents:
        success = send_weekly_summary_email(mail, parent.id)
        if success:
            stats['sent'] += 1
        else:
            stats['failed'] += 1

    return stats
