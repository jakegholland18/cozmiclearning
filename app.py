import sys
import os
from flask import Flask, render_template, request, redirect, session, flash
from datetime import datetime, timedelta

# ============================================================
# FIX STATIC + TEMPLATE PATHS FOR RENDER
# ============================================================

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "website", "templates"),
    static_url_path="/static",
    static_folder=os.path.join(BASE_DIR, "website", "static")
)

app.secret_key = "b3c2e773eaa84cd6841a9ffa54c918881b9fab30bb02f7128"

# Make sure Python can see /modules
sys.path.append(os.path.abspath(os.path.join(BASE_DIR, "modules")))

# ---------------------------------------
# IMPORT AI LOGIC + CHARACTER DATA
# ---------------------------------------
from modules.shared_ai import study_buddy_ai
from modules.personality_helper import get_all_characters

# Updated helpers using your NEW 6-section strategy
import modules.math_helper     as math_helper
import modules.text_helper     as text_helper
import modules.question_helper as question_helper
import modules.science_helper  as science_helper
import modules.bible_helper    as bible_helper
import modules.history_helper  as history_helper
import modules.writing_helper  as writing_helper
import modules.study_helper    as study_helper
import modules.apologetics_helper as apologetics_helper
import modules.investment_helper  as investment_helper
import modules.money_helper       as money_helper


# ============================================================
# INITIALIZE USER SESSION
# ============================================================

def init_user():
    defaults = {
        "tokens": 0,
        "xp": 0,
        "level": 1,
        "streak": 1,
        "last_visit": str(datetime.today().date()),
        "inventory": [],
        "usage_minutes": 0,

        # Default character (must match personality helper keys)
        "character": "everly",

        # Track subject usage
        "progress": {
            "num_forge": {"questions": 0},
            "atom_sphere": {"questions": 0},
            "chrono_core": {"questions": 0},
            "ink_haven": {"questions": 0},
            "faith_realm": {"questions": 0},
            "coin_quest": {"questions": 0},
            "stock_star": {"questions": 0},
            "story_verse": {"questions": 0},
            "power_grid": {"questions": 0},
            "terra_nova": {"questions": 0},
            "truth_forge": {"questions": 0},
        }
    }

    for key, val in defaults.items():
        if key not in session:
            session[key] = val

    update_streak()


# ============================================================
# DAILY STREAK
# ============================================================

def update_streak():
    today = datetime.today().date()
    last = datetime.strptime(session["last_visit"], "%Y-%m-%d").date()

    if today != last:
        session["streak"] = session["streak"] + 1 if today - last == timedelta(days=1) else 1

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
        flash(f"LEVEL UP! You reached Level {session['level']}!", "info")


# ============================================================
# HOME → SUBJECTS
# ============================================================

@app.route("/")
def home():
    init_user()
    return redirect("/subjects")


# ============================================================
# SUBJECTS PLANET SCREEN
# ============================================================

@app.route("/subjects")
def subjects():
    init_user()

    planets = [
        ("chrono_core", "chrono_core.png", "ChronoCore"),
        ("num_forge", "num_forge.png", "NumForge"),
        ("atom_sphere", "atom_sphere.png", "AtomSphere"),
        ("story_verse", "story_verse.png", "StoryVerse"),
        ("ink_haven", "ink_haven.png", "InkHaven"),
        ("faith_realm", "faith_realm.png", "FaithRealm"),
        ("coin_quest", "coin_quest.png", "CoinQuest"),
        ("stock_star", "stock_star.png", "StockStar"),
        ("terra_nova", "terra_nova.png", "TerraNova"),
        ("power_grid", "power_grid.png", "PowerGrid"),
        ("truth_forge", "truth_forge.png", "TruthForge")
    ]

    return render_template("subjects.html", planets=planets, character=session["character"])


# ============================================================
# CHARACTER SELECTION
# ============================================================

@app.route("/choose-character")
def choose_character():
    init_user()
    characters = get_all_characters()
    return render_template("choose_character.html", characters=characters)


@app.route("/select-character", methods=["POST"])
def select_character():
    init_user()
    chosen = request.form.get("character")
    if chosen:
        session["character"] = chosen
    return redirect("/dashboard")


# ============================================================
# CHOOSE GRADE LEVEL
# ============================================================

@app.route("/choose-grade")
def choose_grade():
    init_user()
    subject = request.args.get("subject")
    return render_template("subject_select_form.html", subject=subject)


# ============================================================
# ASK QUESTION
# ============================================================

@app.route("/ask-question")
def ask_question():
    init_user()

    subject = request.args.get("subject")
    grade = request.args.get("grade")
    characters = get_all_characters()

    return render_template(
        "ask_question.html",
        subject=subject,
        grade=grade,
        character=session["character"],
        characters=characters
    )


# ============================================================
# SUBJECT → AI PROCESSING
# ============================================================

@app.route("/subject", methods=["POST"])
def subject_answer():
    init_user()

    grade = request.form.get("grade")
    subject = request.form.get("subject")
    question = request.form.get("question")
    character = session["character"]

    # Track number of questions asked
    session["progress"][subject]["questions"] += 1

    # NEW: All helpers now return 6-section structured answer
    subject_map = {
        "num_forge":  math_helper.explain_math,
        "atom_sphere": science_helper.explain_science,
        "faith_realm": bible_helper.bible_lesson,
        "chrono_core": history_helper.explain_history,
        "ink_haven":  writing_helper.help_write,
        "power_grid": study_helper.generate_quiz,
        "truth_forge": apologetics_helper.apologetics_answer,
        "stock_star": investment_helper.explain_investing,
        "coin_quest": money_helper.explain_money,
        "terra_nova": question_helper.answer_question,
        "story_verse": text_helper.summarize_text,
    }

    # Fetch correct helper
    if subject in subject_map:
        raw_answer = subject_map[subject](question, grade, character)
    else:
        raw_answer = "Hmm… I’m not sure which planet this belongs to."

    # Render final answer
    add_xp(20)
    session["tokens"] += 2

    return render_template("subject.html", answer=raw_answer, character=character)


# ============================================================
# STUDENT DASHBOARD
# ============================================================

@app.route("/dashboard")
def dashboard():
    init_user()

    xp = session["xp"]
    level = session["level"]
    tokens = session["tokens"]
    streak = session["streak"]
    character = session["character"]

    xp_to_next = level * 100
    xp_percent = int((xp / xp_to_next) * 100)

    missions = [
        "Visit 2 different planets",
        "Ask 1 science question",
        "Earn 20 XP",
    ]

    locked_characters = {
        "Everly": "Reach Level 3",
        "Nova": "3-day streak",
        "Lio": "Earn 200 XP total",
        "Buddy Barkston": "Buy for 100 tokens",
    }

    return render_template(
        "dashboard.html",
        xp=xp,
        level=level,
        tokens=tokens,
        streak=streak,
        character=character,
        xp_percent=xp_percent,
        xp_to_next=xp_to_next,
        missions=missions,
        locked_characters=locked_characters
    )


# ============================================================
# DISABLED SHOP + INVENTORY (UNTIL READY)
# ============================================================

@app.route("/shop")
def shop():
    return redirect("/dashboard")

@app.route("/inventory")
def inventory():
    return redirect("/dashboard")

@app.route("/buy/<item_id>")
def buy_item(item_id):
    return redirect("/dashboard")


# ============================================================
# PARENT DASHBOARD
# ============================================================

@app.route("/parent_dashboard")
def parent_dashboard():
    init_user()

    progress_display = {
        subject: data["questions"]
        for subject, data in session["progress"].items()
    }

    return render_template(
        "parent_dashboard.html",
        progress=progress_display,
        utilization=session["usage_minutes"],
        xp=session["xp"],
        level=session["level"],
        tokens=session["tokens"],
        character=session["character"]
    )


# ============================================================
# RUN SERVER
# ============================================================

if __name__ == "__main__":
    app.run(debug=True)
