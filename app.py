import sys
import os
import logging
import traceback
import re
from datetime import datetime, timedelta
from collections import defaultdict

from flask import (
    Flask, render_template, request, redirect, session,
    flash, jsonify, send_file, Response
)
from flask import got_request_exception

# ============================================================
# STATIC + TEMPLATE PATHS
# ============================================================

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "website", "templates"),
    static_url_path="/static",
    static_folder=os.path.join(BASE_DIR, "website", "static"),
)

app.secret_key = "b3c2e773eaa84cd6841a9ffa54c918881b9fab30bb02f7128"

# ============================================================
# DATABASE + MODELS (FIRST TIME SETUP)
# ============================================================

from flask_bcrypt import Bcrypt
from models import db, Teacher, Class, Student, AssessmentResult
from sqlalchemy import func

# Configure SQLite DB
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cozmiclearning.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Init DB + bcrypt
db.init_app(app)
bcrypt = Bcrypt(app)

with app.app_context():
    db.create_all()

# ============================================================
# ERROR LOGGING
# ============================================================

logging.basicConfig(level=logging.INFO)

def log_exception(sender, exception, **extra):
    sender.logger.error("Exception during request: %s", traceback.format_exc())

got_request_exception.connect(log_exception, app)

# ============================================================
# LOAD MODULES
# ============================================================

sys.path.append(os.path.abspath(os.path.join(BASE_DIR, "modules")))

from modules.shared_ai import study_buddy_ai, powergrid_master_ai
from modules.personality_helper import get_all_characters
from modules.practice_helper import generate_practice_session
from modules.auto_logger import log_practice_event, normalize_subject
from modules.ability_helper import recalc_student_ability

import modules.math_helper as math_helper
import modules.text_helper as text_helper
import modules.question_helper as question_helper
import modules.science_helper as science_helper
import modules.bible_helper as bible_helper
import modules.history_helper as history_helper
import modules.writing_helper as writing_helper
import modules.study_helper as study_helper
import modules.apologetics_helper as apologetics_helper
import modules.investment_helper as investment_helper
import modules.money_helper as money_helper

# ============================================================
# SUBJECT → FUNCTION MAP
# ============================================================

subject_map = {
    "num_forge": math_helper.explain_math,
    "atom_sphere": science_helper.explain_science,
    "faith_realm": bible_helper.bible_lesson,
    "chrono_core": history_helper.explain_history,
    "ink_haven": writing_helper.help_write,
    "truth_forge": apologetics_helper.apologetics_answer,
    "stock_star": investment_helper.explain_investing,
    "coin_quest": money_helper.explain_money,
    "terra_nova": question_helper.answer_question,
    "story_verse": text_helper.explain_text,
    "power_grid": None,
}

# ============================================================
# USER SESSION DEFAULTS
# ============================================================

def init_user():
    defaults = {
        "tokens": 0,
        "xp": 0,
        "level": 1,
        "streak": 1,
        "last_visit": str(datetime.today().date()),
        "inventory": [],
        "character": "everly",
        "usage_minutes": 0,
        "progress": {},
        "conversation": [],
        "deep_study_chat": [],
        "practice": None,
        "practice_step": 0,
        "practice_attempts": 0,
        "practice_progress": [],
    }
    for k, v in defaults.items():
        if k not in session:
            session[k] = v
    update_streak()

# ============================================================
# DAILY STREAK
# ============================================================

def update_streak():
    today = datetime.today().date()
    last = datetime.strptime(session["last_visit"], "%Y-%m-%d").date()

    if today != last:
        if today - last == timedelta(days=1):
            session["streak"] += 1
        else:
            session["streak"] = 1
        session["last_visit"] = str(today)

# ============================================================
# XP SYSTEM
# ============================================================

def add_xp(amount):
    session["xp"] += amount
    xp_needed = session["level"] * 100

    if session["xp"] >= xp_needed:
        session["xp"] -= xp_needed
        session["level"] += 1
        flash(f"LEVEL UP! You are now Level {session['level']}!", "info")

# ============================================================
# HELPER: FLEXIBLE ANSWER MATCHING FOR PRACTICE
# ============================================================

def _normalize_numeric_token(text: str) -> str:
    t = text.lower().strip()
    for word in ["percent", "perc", "per cent", "dollars", "dollar", "usd"]:
        t = t.replace(word, "")
    t = t.replace(",", "")
    for ch in ["%", "$"]:
        t = t.replace(ch, "")
    return t.strip()

def _try_float(val: str):
    try:
        return float(val)
    except Exception:
        return None

def answers_match(user_raw: str, expected_raw: str) -> bool:
    if user_raw is None or expected_raw is None:
        return False

    u_norm = user_raw.strip().lower()
    e_norm = expected_raw.strip().lower()

    if u_norm == e_norm and u_norm != "":
        return True

    u_num_str = _normalize_numeric_token(user_raw)
    e_num_str = _normalize_numeric_token(expected_raw)

    if u_num_str and e_num_str and u_num_str == e_num_str:
        return True

    u_num = _try_float(u_num_str)
    e_num = _try_float(e_num_str)
    if u_num is not None and e_num is not None:
        if abs(u_num - e_num) < 1e-6:
            return True

    return False

# ============================================================
# ROUTES – CORE APP
# ============================================================

@app.route("/")
def home():
    init_user()
    return redirect("/subjects")

@app.route("/subjects")
def subjects():
    init_user()

    planets = [
        ("chrono_core", "chrono_core.png", "ChronoCore", "History"),
        ("num_forge", "num_forge.png", "NumForge", "Math"),
        ("atom_sphere", "atom_sphere.png", "AtomSphere", "Science"),
        ("story_verse", "story_verse.png", "StoryVerse", "Reading"),
        ("ink_haven", "ink_haven.png", "InkHaven", "Writing"),
        ("faith_realm", "faith_realm.png", "FaithRealm", "Bible"),
        ("coin_quest", "coin_quest.png", "CoinQuest", "Money"),
        ("stock_star", "stock_star.png", "StockStar", "Investing"),
        ("terra_nova", "terra_nova.png", "TerraNova", "General Knowledge"),
        ("power_grid", "power_grid.png", "PowerGrid", "Deep Study"),
        ("truth_forge", "truth_forge.png", "TruthForge", "Apologetics"),
    ]

    return render_template("subjects.html", planets=planets, character=session["character"])

# ============================================================
# CHARACTER SELECT
# ============================================================

@app.route("/choose-character")
def choose_character():
    init_user()
    return render_template("choose_character.html", characters=get_all_characters())

@app.route("/select-character", methods=["POST"])
def select_character():
    init_user()
    session["character"] = request.form.get("character")
    return redirect("/dashboard")

# ============================================================
# GRADE SELECT
# ============================================================

@app.route("/choose-grade")
def choose_grade():
    init_user()
    return render_template("subject_select_form.html", subject=request.args.get("subject"))

# ============================================================
# ASK QUESTION
# ============================================================

@app.route("/ask-question")
def ask_question():
    init_user()
    return render_template(
        "ask_question.html",
        subject=request.args.get("subject"),
        grade=request.args.get("grade"),
        character=session["character"],
        characters=get_all_characters(),
    )

# ============================================================
# POWERGRID SUBMISSION
# ============================================================

@app.route("/powergrid_submit", methods=["POST"])
def powergrid_submit():
    init_user()

    grade = request.form.get("grade")
    topic = request.form.get("topic", "").strip()
    uploaded = request.files.get("file")

    session["grade"] = grade

    text = ""
    if uploaded and uploaded.filename:
        ext = uploaded.filename.lower()
        path = os.path.join("/tmp", uploaded.filename)
        uploaded.save(path)

        if ext.endswith(".txt"):
            text = open(path, "r").read()
        elif ext.endswith(".pdf"):
            try:
                from PyPDF2 import PdfReader
                pdf = PdfReader(path)
                text = "\n".join(page.extract_text() or "" for page in pdf.pages)
            except Exception:
                text = "Could not read PDF content."
        else:
            text = f"Study this:\n\n{topic}"
    else:
        text = topic or "No topic provided."

    study_guide = study_helper.generate_powergrid_master_guide(
        text, grade, session["character"]
    )

    import uuid
    from textwrap import wrap
    pdf_path = f"/tmp/study_guide_{uuid.uuid4().hex}.pdf"

    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter

        c = canvas.Canvas(pdf_path, pagesize=letter)
        width, height = letter
        y = height - 50

        for line in study_guide.split("\n"):
            for wrapped in wrap(line, 110):
                c.drawString(40, y, wrapped)
                y -= 15
                if y < 40:
                    c.showPage()
                    y = height - 50

        c.save()
        session["study_pdf"] = pdf_path
        pdf_url = "/download_study_guide"

    except Exception as e:
        app.logger.error(f"PDF generation error: {e}")
        pdf_url = None

    session["conversation"] = []
    session["deep_study_chat"] = []
    session.modified = True

    return render_template(
        "subject.html",
        subject="power_grid",
        grade=grade,
        question=topic,
        answer=study_guide,
        character=session["character"],
        conversation=session["conversation"],
        pdf_url=pdf_url,
    )

# ============================================================
# PDF DOWNLOAD
# ============================================================

@app.route("/download_study_guide")
def download_study_guide():
    pdf = session.get("study_pdf")

    if not pdf or not os.path.exists(pdf):
        return "PDF not found."

    return send_file(pdf, as_attachment=True)

# ============================================================
# MAIN SUBJECT ANSWER
# ============================================================

@app.route("/subject", methods=["POST"])
def subject_answer():
    init_user()

    grade = request.form.get("grade")
    subject = request.form.get("subject")
    question = request.form.get("question")
    character = session["character"]

    session["grade"] = grade

    session["progress"].setdefault(subject, {"questions": 0, "correct": 0})
    session["progress"][subject]["questions"] += 1

    if subject == "power_grid":
        return redirect(f"/ask-question?subject=power_grid&grade={grade}")

    func = subject_map.get(subject)
    if func is None:
        flash("Unknown subject selected.", "error")
        return redirect("/subjects")

    result = func(question, grade, character)
    answer = result.get("raw_text") if isinstance(result, dict) else result

    session["conversation"] = []
    session.modified = True

    add_xp(20)
    session["tokens"] += 2

    return render_template(
        "subject.html",
        subject=subject,
        grade=grade,
        question=question,
        answer=answer,
        character=character,
        conversation=session["conversation"],
        pdf_url=None,
    )

# ============================================================
# FOLLOWUP MESSAGE
# ============================================================

@app.route("/followup_message", methods=["POST"])
def followup_message():
    init_user()

    data = request.get_json() or {}
    grade = data.get("grade")
    character = data.get("character") or session["character"]
    message = data.get("message", "")

    conversation = session.get("conversation", [])
    conversation.append({"role": "user", "content": message})

    reply = study_helper.deep_study_chat(conversation, grade, character)

    conversation.append({"role": "assistant", "content": reply})
    session["conversation"] = conversation
    session.modified = True

    return jsonify({"reply": reply})

# ============================================================
# DEEP STUDY MESSAGE
# ============================================================

@app.route("/deep_study_message", methods=["POST"])
def deep_study_message():
    init_user()

    data = request.get_json() or {}
    message = data.get("message", "")

    grade = session.get("grade", "8")
    character = session.get("character", "everly")

    conversation = session.get("deep_study_chat", [])
    conversation.append({"role": "user", "content": message})

    dialogue_text = ""
    for turn in conversation:
        speaker = "Student" if turn["role"] == "user" else "Tutor"
        dialogue_text += f"{speaker}: {turn['content']}\n"

    prompt = f"""
You are the DEEP STUDY TUTOR.
Warm, patient, conversational.

GRADE LEVEL: {grade}

Conversation so far:
{dialogue_text}

Rules:
• Only answer last student message
• No long essays
• No repeating study guide
• Encourage deeper thinking
"""

    reply = study_buddy_ai(prompt, grade, character)
    reply = reply.get("raw_text") if isinstance(reply, dict) else reply

    conversation.append({"role": "assistant", "content": reply})
    session["deep_study_chat"] = conversation
    session.modified = True

    return jsonify({"reply": reply})

# ============================================================
# PRACTICE MODE — PAGE ROUTE
# ============================================================

@app.route("/practice")
def practice():
    init_user()

    subject = request.args.get("subject", "")
    topic = request.args.get("topic", "")
    character = session.get("character", "everly")
    grade = session.get("grade", "8")

    return render_template(
        "practice.html",
        subject=subject,
        topic=topic,
        character=character,
        grade=grade,
    )

# ============================================================
# PRACTICE MODE — START (TOPIC → FIRST QUESTION)
# ============================================================

@app.route("/start_practice", methods=["POST"])
def start_practice():
    init_user()

    data = request.get_json() or {}
    topic = data.get("topic", "").strip()
    subject = data.get("subject", "")
    grade = session.get("grade", "8")
    character = session.get("character", "everly")

    practice_data = generate_practice_session(
        topic=topic,
        subject=subject,
        grade_level=grade,
        character=character,
    )

    steps = practice_data.get("steps") or []
    if not steps:
        return jsonify({
            "status": "error",
            "message": "No practice questions were generated. Try a different topic.",
            "character": character,
        })

    # Save subject inside practice_data so logger + analytics can use it later
    practice_data["subject"] = subject

    # Per-question progress: attempts, status, last_answer, chat
    progress = []
    for _ in steps:
        progress.append({
            "attempts": 0,
            "status": "unanswered",
            "last_answer": "",
            "chat": [],
        })

    session["practice"] = practice_data
    session["practice_progress"] = progress
    session["practice_step"] = 0
    session["practice_attempts"] = 0
    session.modified = True

    first = steps[0]

    return jsonify({
        "status": "ok",
        "index": 0,
        "total": len(steps),
        "prompt": first.get("prompt", "Let's start practicing!"),
        "type": first.get("type", "free"),
        "choices": first.get("choices", []),
        "character": character,
        "last_answer": "",
        "chat": [],
    })

# ============================================================
# PRACTICE MODE — NAVIGATE BETWEEN QUESTIONS
# ============================================================

@app.route("/navigate_question", methods=["POST"])
def navigate_question():
    init_user()

    data = request.get_json() or {}
    index = int(data.get("index", 0))

    practice_data = session.get("practice")
    progress = session.get("practice_progress", [])
    character = session.get("character", "everly")

    if not practice_data:
        return jsonify({"status": "error", "message": "No active practice mission.", "character": character})

    steps = practice_data.get("steps") or []
    total = len(steps)

    if index < 0:
        index = 0
    if index >= total:
        index = total - 1

    step = steps[index]
    state = progress[index] if index < len(progress) else {
        "attempts": 0, "status": "unanswered", "last_answer": "", "chat": []
    }

    session["practice_step"] = index
    session.modified = True

    return jsonify({
        "status": "ok",
        "index": index,
        "total": total,
        "prompt": step.get("prompt", ""),
        "type": step.get("type", "free"),
        "choices": step.get("choices", []),
        "last_answer": state.get("last_answer", ""),
        "question_status": state.get("status", "unanswered"),
        "chat": state.get("chat", []),
        "character": character,
    })

# ============================================================
# PRACTICE MODE — STEP PROCESS (ANSWER CHECK, HINTS, GUIDED)
# ============================================================

@app.route("/practice_step", methods=["POST"])
def practice_step():
    init_user()

    data = request.get_json() or {}
    user_answer_raw = data.get("answer") or ""
    user_answer_stripped = user_answer_raw.strip()

    practice_data = session.get("practice")
    index = session.get("practice_step", 0)
    character = session.get("character", "everly")

    if not practice_data:
        return jsonify({
            "status": "error",
            "message": "Practice session not found. Try starting a new practice mission.",
            "character": character
        })

    steps = practice_data.get("steps") or []
    if not steps or index < 0 or index >= len(steps):
        return jsonify({
            "status": "finished",
            "message": practice_data.get("final_message", "Mission complete!"),
            "character": character
        })

    step = steps[index]

    progress = session.get("practice_progress", [])
    if index >= len(progress):
        progress.extend(
            [{"attempts": 0, "status": "unanswered", "last_answer": "", "chat": []}
             for _ in range(index - len(progress) + 1)]
        )

    state = progress[index]
    attempts = state.get("attempts", 0)
    expected_list = step.get("expected", [])

    # If they sent blank, treat as incorrect but don't bump attempts
    if not user_answer_stripped:
        return jsonify({
            "status": "incorrect",
            "hint": step.get("hint", "Try giving your best guess, even if you're not sure."),
            "character": character
        })

    # Flexible correctness check
    is_correct = False
    for exp in expected_list:
        if answers_match(user_answer_raw, str(exp)):
            is_correct = True
            break

    # For logging
    student_id = session.get("student_id")
    subject = practice_data.get("subject", "")
    topic = practice_data.get("topic", "")
    question_text = step.get("prompt", "")
    question_type = step.get("type", "free")

    # ================= CORRECT ANSWER =================
    if is_correct:
        attempts += 1
        old_status = state.get("status", "unanswered")

        state["attempts"] = attempts
        state["status"] = "correct"
        state["last_answer"] = user_answer_raw
        progress[index] = state
        session["practice_progress"] = progress
        session.modified = True

        # Auto-log only on first time reaching "correct"
        if student_id and old_status != "correct":
            log_practice_event(
                student_id=student_id,
                subject=subject,
                topic=topic,
                question_text=question_text,
                is_correct=True,
                difficulty_level=None,
                question_type=question_type,
            )

        # Are all questions done?
        all_done = all(
            s.get("status") in ("correct", "given_up")
            for s in progress
        )

        if all_done:
            return jsonify({
                "status": "finished",
                "message": practice_data.get("final_message", "Great job! Mission complete 🚀"),
                "character": character
            })

        return jsonify({
            "status": "correct",
            "next_prompt": step.get("prompt", ""),
            "type": step.get("type", "free"),
            "choices": step.get("choices", []),
            "character": character
        })

    # ================= INCORRECT ANSWER =================
    attempts += 1
    state["attempts"] = attempts
    state["last_answer"] = user_answer_raw
    progress[index] = state
    session["practice_progress"] = progress
    session.modified = True

    # First two wrong tries → hints only
    if attempts < 2:
        return jsonify({
            "status": "incorrect",
            "hint": step.get("hint", "Try thinking about it step by step."),
            "character": character
        })

    # Third (or more) wrong try → guided walkthrough + mark given_up
    old_status = state.get("status", "unanswered")
    state["status"] = "given_up"
    progress[index] = state
    session["practice_progress"] = progress
    session.modified = True

    # Auto-log only on first time reaching "given_up"
    if student_id and old_status not in ("correct", "given_up"):
        log_practice_event(
            student_id=student_id,
            subject=subject,
            topic=topic,
            question_text=question_text,
            is_correct=False,
            difficulty_level=None,
            question_type=question_type,
        )

    explanation = step.get(
        "explanation",
        step.get("hint", "Let's walk through how to solve this carefully.")
    )

    # Are all questions done now?
    all_done = all(
        s.get("status") in ("correct", "given_up")
        for s in progress
    )

    if all_done:
        return jsonify({
            "status": "finished",
            "message": practice_data.get("final_message", "Great effort! Mission complete 🚀"),
            "explanation": explanation,
            "character": character
        })

    return jsonify({
        "status": "guided",
        "explanation": explanation,
        "next_prompt": step.get("prompt", ""),
        "type": step.get("type", "free"),
        "choices": step.get("choices", []),
        "character": character
    })

# ============================================================
# PRACTICE HELP CHAT — TUTOR + DISPUTE SOLVER
# ============================================================

@app.route("/practice_help_message", methods=["POST"])
def practice_help_message():
    init_user()

    data = request.get_json() or {}
    student_msg = data.get("message", "").strip()

    practice_data = session.get("practice")
    index = session.get("practice_step", 0)
    character = session.get("character", "everly")
    grade = session.get("grade", "8")

    if not practice_data:
        return jsonify({"reply": "I can't find an active practice mission. Try starting one again!"})

    steps = practice_data.get("steps", [])
    if not steps or index < 0 or index >= len(steps):
        return jsonify({"reply": "You've completed all the questions for this mission! Want to start a new one?"})

    progress = session.get("practice_progress", [])
    if index >= len(progress):
        progress.extend(
            [{"attempts": 0, "status": "unanswered", "last_answer": "", "chat": []}
             for _ in range(index - len(progress) + 1)]
        )

    state = progress[index]
    attempts = state.get("attempts", 0)
    chat_history = state.get("chat", [])

    step = steps[index]
    prompt = step.get("prompt", "")
    expected = step.get("expected", [])
    explanation = step.get("explanation", "")
    topic = practice_data.get("topic", "")

    chat_history.append({"role": "student", "content": student_msg})

    ai_prompt = f"""
You are COZMICLEARNING — a warm, patient cozmic mentor guiding students through the galaxy of learning.

The student is asking for help about a practice question.

CONTEXT:
- Topic: {topic}
- Grade level: {grade}
- Character voice: {character}

Current question:
\"\"\"{prompt}\"\"\"

Expected correct answers (could be letters or short answers):
{expected}

Official explanation / teacher notes:
\"\"\"{explanation}\"\"\"

Attempts used so far on this question: {attempts}

CHAT HISTORY for this question:
{chat_history}

STUDENT JUST SAID:
\"\"\"{student_msg}\"\"\"

RESPONSE RULES (VERY IMPORTANT):
- Tone: encouraging, calm, never harsh.
- 1–3 short guiding sentences first.
- Then up to 8 short bullet points that walk through the idea step-by-step.
- Keep language efficient and easy to follow.
- BEFORE 2 graded attempts: do NOT give the full direct answer. Use hints, guiding questions, and partial steps.
- AFTER 2 graded attempts: you MAY give the direct answer, but still explain why in a clear, kind way.
- Encourage the student to keep going and remind them you're there to help.
- If they dispute correctness, compare their reasoning with the expected answer gently and clearly.

Do NOT use markdown syntax markers like '*' or '-' in your bullets.
Instead, start each bullet with a simple symbol like '•'.
"""

    reply = study_buddy_ai(ai_prompt, grade, character)
    reply_text = reply.get("raw_text") if isinstance(reply, dict) else reply

    chat_history.append({"role": "tutor", "content": reply_text})
    state["chat"] = chat_history
    progress[index] = state
    session["practice_progress"] = progress
    session.modified = True

    return jsonify({"reply": reply_text, "chat": chat_history})

# ============================================================
# DASHBOARD
# ============================================================

@app.route("/dashboard")
def dashboard():
    init_user()

    xp = session["xp"]
    level = session["level"]
    tokens = session["tokens"]
    streak = session["streak"]

    xp_to_next = level * 100
    xp_percent = int((xp / xp_to_next) * 100) if xp_to_next > 0 else 0

    missions = [
        "Visit 2 different planets",
        "Ask 1 science question",
        "Earn 20 XP",
    ]

    locked = {
        "Princess Everly": "Reach Level 3",
        "Nova Circuit": "3-day streak",
        "Agent Cluehart": "Earn 200 XP",
        "Buddy Barkston": "Buy for 100 tokens",
    }

    return render_template(
        "dashboard.html",
        xp=xp,
        level=level,
        tokens=tokens,
        streak=streak,
        character=session["character"],
        xp_percent=xp_percent,
        xp_to_next=xp_to_next,
        missions=missions,
        locked_characters=locked,
    )

# ============================================================
# PARENT DASHBOARD (SESSION-BASED FOR NOW)
# ============================================================

@app.route("/parent_dashboard")
def parent_dashboard():
    init_user()

    progress = {
        s: (int(data["correct"] / data["questions"] * 100) if data["questions"] else 0)
        for s, data in session["progress"].items()
    }

    return render_template(
        "parent_dashboard.html",
        progress=progress,
        utilization=session["usage_minutes"],
        xp=session["xp"],
        level=session["level"],
        tokens=session["tokens"],
        character=session["character"],
    )

# ============================================================
# TEACHER AUTH + DASHBOARD
# ============================================================

@app.route("/teacher/signup", methods=["GET", "POST"])
def teacher_signup():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not name or not email or not password:
            flash("Please fill out all fields.", "error")
            return redirect("/teacher/signup")

        existing = Teacher.query.filter_by(email=email).first()
        if existing:
            flash("An account with that email already exists. Please log in.", "error")
            return redirect("/teacher/login")

        hashed = bcrypt.generate_password_hash(password).decode("utf-8")
        new_teacher = Teacher(name=name, email=email, password_hash=hashed)

        db.session.add(new_teacher)
        db.session.commit()

        session["teacher_id"] = new_teacher.id
        flash("Welcome to CozmicLearning Teacher Portal!", "info")
        return redirect("/teacher/dashboard")

    return render_template("teacher_signup.html")


@app.route("/teacher/login", methods=["GET", "POST"])
def teacher_login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        teacher = Teacher.query.filter_by(email=email).first()
        if teacher and bcrypt.check_password_hash(teacher.password_hash, password):
            session["teacher_id"] = teacher.id
            flash("Logged in successfully.", "info")
            return redirect("/teacher/dashboard")

        flash("Invalid email or password.", "error")

    return render_template("teacher_login.html")


@app.route("/teacher/logout")
def teacher_logout():
    session.pop("teacher_id", None)
    flash("You have been logged out.", "info")
    return redirect("/teacher/login")


@app.route("/teacher/dashboard")
def teacher_dashboard():
    teacher_id = session.get("teacher_id")
    if not teacher_id:
        return redirect("/teacher/login")

    teacher = Teacher.query.get(teacher_id)
    classes = teacher.classes if teacher else []

    return render_template(
        "teacher_dashboard.html",
        teacher=teacher,
        classes=classes,
    )


@app.route("/teacher/add_class", methods=["POST"])
def add_class():
    teacher_id = session.get("teacher_id")
    if not teacher_id:
        return redirect("/teacher/login")

    class_name = request.form.get("class_name", "").strip()
    grade = request.form.get("grade_level", "").strip()

    if not class_name:
        flash("Class name is required.", "error")
        return redirect("/teacher/dashboard")

    new_class = Class(teacher_id=teacher_id, class_name=class_name, grade_level=grade)
    db.session.add(new_class)
    db.session.commit()

    flash("Class created successfully.", "info")
    return redirect("/teacher/dashboard")


@app.route("/teacher/add_student/<int:class_id>", methods=["POST"])
def add_student(class_id):
    teacher_id = session.get("teacher_id")
    if not teacher_id:
        return redirect("/teacher/login")

    cls = Class.query.get(class_id)
    if not cls or cls.teacher_id != teacher_id:
        flash("Class not found or not authorized.", "error")
        return redirect("/teacher/dashboard")

    name = request.form.get("student_name", "").strip()
    email = request.form.get("email", "").strip()

    if not name:
        flash("Student name is required.", "error")
        return redirect("/teacher/dashboard")

    new_student = Student(class_id=class_id, student_name=name, student_email=email)
    db.session.add(new_student)
    db.session.commit()

    flash("Student added to class.", "info")
    return redirect("/teacher/dashboard")

# ============================================================
# TEACHER ANALYTICS + MANUAL RECORD ENTRY
# ============================================================

@app.route("/teacher/class/<int:class_id>/analytics")
def teacher_class_analytics(class_id):
    teacher_id = session.get("teacher_id")
    if not teacher_id:
        return redirect("/teacher/login")

    cls = Class.query.get(class_id)
    if not cls or cls.teacher_id != teacher_id:
        flash("Class not found or not authorized.", "error")
        return redirect("/teacher/dashboard")

    students = Student.query.filter_by(class_id=class_id).all()

    # Recalculate ability tiers for each student (based on latest data)
    for s in students:
        recalc_student_ability(s)

    # Subject-level averages
    subject_averages = {}
    rows = (
        db.session.query(
            AssessmentResult.subject,
            func.avg(AssessmentResult.score_percent)
        )
        .join(Student, AssessmentResult.student_id == Student.id)
        .filter(Student.class_id == class_id)
        .group_by(AssessmentResult.subject)
        .all()
    )
    for subj, avg_score in rows:
        subject_averages[subj] = round(avg_score, 1)

    # Ability distribution
    ability_counts = {"struggling": 0, "on_level": 0, "advanced": 0}
    for s in students:
        lvl = s.ability_level or "on_level"
        if lvl not in ability_counts:
            ability_counts[lvl] = 0
        ability_counts[lvl] += 1

    # Pivot-style heatmap: rows = students, columns = (subject|topic)
    all_results = (
        AssessmentResult.query
        .join(Student, AssessmentResult.student_id == Student.id)
        .filter(Student.class_id == class_id)
        .all()
    )

    topic_keys = []
    topic_seen = set()
    agg = defaultdict(lambda: {"sum": 0.0, "count": 0})

    for r in all_results:
        subj = (r.subject or "").strip() or "general"
        topic = (r.topic or "").strip() or "General"
        key = f"{subj.title()} | {topic}"

        if key not in topic_seen:
            topic_seen.add(key)
            topic_keys.append(key)

        idx = (r.student_id, key)
        agg[idx]["sum"] += (r.score_percent or 0.0)
        agg[idx]["count"] += 1

    student_topic_matrix = defaultdict(dict)
    for (student_id, key), data in agg.items():
        avg_score = data["sum"] / max(data["count"], 1)
        student_topic_matrix[student_id][key] = round(avg_score, 1)

    student_topic_matrix = {sid: dict(inner) for sid, inner in student_topic_matrix.items()}

    return render_template(
        "class_analytics.html",
        cls=cls,
        students=students,
        subject_averages=subject_averages,
        ability_counts=ability_counts,
        topic_keys=topic_keys,
        matrix=student_topic_matrix,
    )


@app.route("/teacher/record_result", methods=["POST"])
def teacher_record_result():
    teacher_id = session.get("teacher_id")
    if not teacher_id:
        return redirect("/teacher/login")

    student_id = request.form.get("student_id")
    subject_raw = request.form.get("subject", "").strip()
    topic = request.form.get("topic", "").strip()
    num_correct_raw = request.form.get("num_correct", "0")
    num_questions_raw = request.form.get("num_questions", "1")
    difficulty_level = request.form.get("difficulty_level") or None

    try:
        student_id = int(student_id)
    except (TypeError, ValueError):
        flash("Invalid student selection.", "error")
        return redirect("/teacher/dashboard")

    student = Student.query.get(student_id)
    if not student:
        flash("Student not found.", "error")
        return redirect("/teacher/dashboard")

    cls = Class.query.get(student.class_id)
    if not cls or cls.teacher_id != teacher_id:
        flash("Not authorized to modify this class.", "error")
        return redirect("/teacher/dashboard")

    try:
        num_correct = int(num_correct_raw)
        num_questions = int(num_questions_raw)
    except ValueError:
        flash("Invalid numbers for correct / total questions.", "error")
        return redirect(f"/teacher/class/{cls.id}/analytics")

    num_questions = max(num_questions, 1)
    num_correct = max(min(num_correct, num_questions), 0)

    normalized_subject = normalize_subject(subject_raw)
    score_percent = (num_correct / num_questions) * 100

    result = AssessmentResult(
        student_id=student.id,
        subject=normalized_subject,
        topic=topic or "General",
        num_correct=num_correct,
        num_questions=num_questions,
        score_percent=score_percent,
        difficulty_level=difficulty_level or student.ability_level,
        timestamp=datetime.utcnow(),
    )

    db.session.add(result)
    db.session.commit()

    recalc_student_ability(student)
    db.session.commit()

    flash("Result recorded successfully.", "info")
    return redirect(f"/teacher/class/{cls.id}/analytics")

# ============================================================
# LEGAL
# ============================================================

@app.route("/terms")
def terms():
    return render_template("terms.html")

@app.route("/privacy")
def privacy():
    return render_template("privacy.html")

@app.route("/disclaimer")
def disclaimer():
    return render_template("disclaimer.html")

# ============================================================
# RUN SERVER
# ============================================================

if __name__ == "__main__":
    app.run(debug=True)
















