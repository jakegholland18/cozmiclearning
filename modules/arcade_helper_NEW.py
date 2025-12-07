"""
Arcade Mode - Learning Games & Competitions
Generates interactive games for students across all subjects

UPDATED: December 2024
- Added 10 new games (22 total)
- Implemented 3-tier difficulty system (Easy/Medium/Hard)
- Replaced grade-level system with difficulty tiers
"""

import random
from datetime import datetime
from models import db, GameSession, GameLeaderboard, ArcadeGame


# ============================================================
# GAME CATALOG - 22 GAMES TOTAL
# ============================================================

ARCADE_GAMES = [
    # ========== MATH GAMES (7 total) ==========
    {
        "game_key": "speed_math",
        "name": "Speed Math ⚡",
        "description": "Solve as many math problems as you can in 60 seconds!",
        "subject": "math",
        "icon": "🔢",
        "difficulties": ["easy", "medium", "hard"]
    },
    {
        "game_key": "number_detective",
        "name": "Number Detective 🔍",
        "description": "Find patterns and solve number mysteries",
        "subject": "math",
        "icon": "🕵️",
        "difficulties": ["easy", "medium", "hard"]
    },
    {
        "game_key": "fraction_frenzy",
        "name": "Fraction Frenzy 🍕",
        "description": "Match equivalent fractions under time pressure",
        "subject": "math",
        "icon": "🍕",
        "difficulties": ["easy", "medium", "hard"]
    },
    {
        "game_key": "equation_race",
        "name": "Equation Race 🏎️",
        "description": "Solve equations faster than ever",
        "subject": "math",
        "icon": "🏎️",
        "difficulties": ["easy", "medium", "hard"]
    },
    # NEW MATH GAMES
    {
        "game_key": "multiplication_mayhem",
        "name": "Multiplication Mayhem 🎯",
        "description": "Master multiplication tables through rapid-fire challenges",
        "subject": "math",
        "icon": "🎯",
        "difficulties": ["easy", "medium", "hard"]
    },
    {
        "game_key": "decimal_dash",
        "name": "Decimal Dash 💯",
        "description": "Add, subtract, multiply, and divide decimals",
        "subject": "math",
        "icon": "💯",
        "difficulties": ["easy", "medium", "hard"]
    },
    {
        "game_key": "algebra_arcade",
        "name": "Algebra Arcade 📐",
        "description": "Solve for x in various algebraic equations",
        "subject": "math",
        "icon": "📐",
        "difficulties": ["easy", "medium", "hard"]
    },

    # ========== SCIENCE GAMES (6 total) ==========
    {
        "game_key": "element_match",
        "name": "Element Match 🧪",
        "description": "Match chemical symbols to element names",
        "subject": "science",
        "icon": "🧪",
        "difficulties": ["easy", "medium", "hard"]
    },
    {
        "game_key": "lab_quiz_rush",
        "name": "Lab Quiz Rush ⚗️",
        "description": "Rapid-fire science trivia challenge",
        "subject": "science",
        "icon": "⚗️",
        "difficulties": ["easy", "medium", "hard"]
    },
    {
        "game_key": "planet_explorer",
        "name": "Planet Explorer 🪐",
        "description": "Test your astronomy and space knowledge",
        "subject": "science",
        "icon": "🪐",
        "difficulties": ["easy", "medium", "hard"]
    },
    # NEW SCIENCE GAMES
    {
        "game_key": "body_systems_battle",
        "name": "Body Systems Battle 🫀",
        "description": "Learn about human body systems and organs",
        "subject": "science",
        "icon": "🫀",
        "difficulties": ["easy", "medium", "hard"]
    },
    {
        "game_key": "ecosystem_explorer",
        "name": "Ecosystem Explorer 🌳",
        "description": "Food chains, habitats, and environmental science",
        "subject": "science",
        "icon": "🌳",
        "difficulties": ["easy", "medium", "hard"]
    },
    {
        "game_key": "physics_phenom",
        "name": "Physics Phenom ⚛️",
        "description": "Motion, forces, energy, and simple machines",
        "subject": "science",
        "icon": "⚛️",
        "difficulties": ["easy", "medium", "hard"]
    },

    # ========== READING & WRITING GAMES (5 total) ==========
    {
        "game_key": "vocab_builder",
        "name": "Vocab Builder 📚",
        "description": "Match words to definitions in a race against time",
        "subject": "reading",
        "icon": "📚",
        "difficulties": ["easy", "medium", "hard"]
    },
    {
        "game_key": "spelling_sprint",
        "name": "Spelling Sprint ✍️",
        "description": "Spell words correctly as fast as you can",
        "subject": "writing",
        "icon": "✍️",
        "difficulties": ["easy", "medium", "hard"]
    },
    {
        "game_key": "grammar_quest",
        "name": "Grammar Quest 📝",
        "description": "Fix grammatical errors in record time",
        "subject": "writing",
        "icon": "📝",
        "difficulties": ["easy", "medium", "hard"]
    },
    # NEW READING/WRITING GAMES
    {
        "game_key": "reading_racer",
        "name": "Reading Racer 📖",
        "description": "Read passages and answer comprehension questions",
        "subject": "reading",
        "icon": "📖",
        "difficulties": ["easy", "medium", "hard"]
    },
    {
        "game_key": "punctuation_pro",
        "name": "Punctuation Pro 📌",
        "description": "Add correct punctuation to sentences",
        "subject": "writing",
        "icon": "📌",
        "difficulties": ["easy", "medium", "hard"]
    },

    # ========== HISTORY & GEOGRAPHY GAMES (4 total) ==========
    {
        "game_key": "history_timeline",
        "name": "Timeline Challenge ⏰",
        "description": "Put historical events in the correct order",
        "subject": "history",
        "icon": "⏰",
        "difficulties": ["easy", "medium", "hard"]
    },
    {
        "game_key": "geography_dash",
        "name": "Geography Dash 🗺️",
        "description": "Identify countries, capitals, and landmarks",
        "subject": "history",
        "icon": "🗺️",
        "difficulties": ["easy", "medium", "hard"]
    },
    # NEW HISTORY/GEOGRAPHY GAMES
    {
        "game_key": "map_master",
        "name": "Map Master 🌍",
        "description": "Identify countries, states, and cities on maps",
        "subject": "history",
        "icon": "🌍",
        "difficulties": ["easy", "medium", "hard"]
    },
    {
        "game_key": "historical_heroes",
        "name": "Historical Heroes 🎖️",
        "description": "Match famous figures to their achievements",
        "subject": "history",
        "icon": "🎖️",
        "difficulties": ["easy", "medium", "hard"]
    },
]


def initialize_arcade_games():
    """Create arcade game records in database"""
    for game_data in ARCADE_GAMES:
        existing = ArcadeGame.query.filter_by(game_key=game_data["game_key"]).first()
        if not existing:
            game = ArcadeGame(
                game_key=game_data["game_key"],
                name=game_data["name"],
                description=game_data["description"],
                subject=game_data["subject"],
                icon=game_data["icon"],
                difficulty_levels="easy,medium,hard"  # All games support 3 difficulties
            )
            db.session.add(game)

    db.session.commit()
    print(f"✅ Initialized {len(ARCADE_GAMES)} arcade games in database")


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def generate_multiple_choice(correct_answer, wrong_range=20, count=3):
    """Generate multiple choice options including the correct answer"""
    options = [correct_answer]

    # Generate wrong answers
    while len(options) < 4:
        if isinstance(correct_answer, int):
            # For numbers, generate nearby wrong answers
            wrong = correct_answer + random.randint(-wrong_range, wrong_range)
            if wrong != correct_answer and wrong > 0 and wrong not in options:
                options.append(wrong)
        elif isinstance(correct_answer, float):
            # For decimals
            wrong = round(correct_answer + random.uniform(-wrong_range, wrong_range), 2)
            if wrong != correct_answer and wrong > 0 and wrong not in options:
                options.append(wrong)

    random.shuffle(options)
    return options


# ============================================================
# GAME GENERATORS - MATH GAMES
# ============================================================

def generate_speed_math(difficulty='medium'):
    """Generate math problems based on difficulty level"""
    questions = []

    for _ in range(20):  # 20 questions per game
        if difficulty == 'easy':
            # Elementary level (grades 1-4)
            op = random.choice(["add", "subtract", "multiply"])
            if op == "add":
                a = random.randint(1, 50)
                b = random.randint(1, 50)
                questions.append({
                    "question": f"{a} + {b}",
                    "answer": a + b,
                    "type": "addition"
                })
            elif op == "subtract":
                a = random.randint(10, 100)
                b = random.randint(1, a)
                questions.append({
                    "question": f"{a} - {b}",
                    "answer": a - b,
                    "type": "subtraction"
                })
            else:  # multiply
                a = random.randint(2, 12)
                b = random.randint(2, 12)
                questions.append({
                    "question": f"{a} × {b}",
                    "answer": a * b,
                    "type": "multiplication"
                })

        elif difficulty == 'medium':
            # Middle school level (grades 5-8)
            op = random.choice(["add", "subtract", "multiply", "divide"])
            if op == "divide":
                b = random.randint(2, 15)
                answer = random.randint(2, 20)
                a = b * answer
                questions.append({
                    "question": f"{a} ÷ {b}",
                    "answer": answer,
                    "type": "division"
                })
            elif op == "multiply":
                a = random.randint(5, 25)
                b = random.randint(5, 25)
                questions.append({
                    "question": f"{a} × {b}",
                    "answer": a * b,
                    "type": "multiplication"
                })
            else:
                a = random.randint(10, 250)
                b = random.randint(10, 200)
                if op == "add":
                    questions.append({
                        "question": f"{a} + {b}",
                        "answer": a + b,
                        "type": "addition"
                    })
                else:
                    if a < b:
                        a, b = b, a
                    questions.append({
                        "question": f"{a} - {b}",
                        "answer": a - b,
                        "type": "subtraction"
                    })

        else:  # hard
            # High school level (grades 9-12)
            op = random.choice(["multiply", "percent", "algebra", "fraction"])
            if op == "percent":
                whole = random.randint(50, 500)
                pct = random.choice([10, 15, 20, 25, 30, 40, 50, 75])
                questions.append({
                    "question": f"{pct}% of {whole}",
                    "answer": int(whole * pct / 100),
                    "type": "percentage"
                })
            elif op == "algebra":
                # Simple: x + a = b
                a = random.randint(5, 50)
                b = random.randint(a + 5, 150)
                questions.append({
                    "question": f"x + {a} = {b}, solve for x",
                    "answer": b - a,
                    "type": "algebra"
                })
            elif op == "fraction":
                # Add fractions with same denominator
                denom = random.choice([2, 3, 4, 5, 6, 8, 10])
                num1 = random.randint(1, denom-1)
                num2 = random.randint(1, denom-1)
                questions.append({
                    "question": f"{num1}/{denom} + {num2}/{denom}",
                    "answer": (num1 + num2) / denom,
                    "type": "fraction"
                })
            else:
                a = random.randint(15, 50)
                b = random.randint(15, 50)
                questions.append({
                    "question": f"{a} × {b}",
                    "answer": a * b,
                    "type": "multiplication"
                })

    random.shuffle(questions)
    return questions


# Continue in next message...
