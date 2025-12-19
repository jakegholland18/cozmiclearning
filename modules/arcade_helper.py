"""
Arcade Mode - Learning Games & Competitions
Generates interactive games for students across all subjects

UPDATED: December 2024
- Added 10 new games (26 total games across all subjects)
- New categories: Geography (4), Financial Literacy (2), Character Education (2), Critical Thinking (2)
- Implemented 3-tier difficulty system (Easy/Medium/Hard)
- Replaced grade-level system with difficulty tiers
"""

import random
import time
from datetime import datetime
from models import db, GameSession, GameLeaderboard, ArcadeGame


# ============================================================
# RANDOM SEED HELPER
# ============================================================

def reseed_random():
    """
    Reseed the random number generator with current time.
    Call this at the start of each game generation to ensure fresh questions.
    """
    random.seed(time.time() + random.random())


# ============================================================
# QUESTION DEDUPLICATION HELPER
# ============================================================

def is_duplicate_question(question, seen_questions):
    """
    Check if a question is a duplicate.
    Returns True if duplicate, False if unique.

    Args:
        question: dict with 'question' field (and optionally 'answer', 'word', etc.)
        seen_questions: set of question strings seen so far
    """
    # Create a unique identifier for this question
    # For math questions, use the question text
    # For vocab/spelling, use the word or question text
    # For other questions, use the full question text

    if 'word' in question:
        # Vocabulary/spelling question - track by word
        identifier = question['word'].lower()
    elif 'question' in question:
        # Math or other text-based question - track by question text
        identifier = str(question['question']).lower().strip()
    elif 'symbol' in question:
        # Element match - track by symbol
        identifier = question['symbol'].upper()
    else:
        # Generic fallback - stringify the whole question
        identifier = str(question)

    if identifier in seen_questions:
        return True  # Duplicate found

    seen_questions.add(identifier)
    return False  # Unique question


# ============================================================
# GAME CATALOG - 26 GAMES TOTAL
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
    # NEW MATH GAME
    {
        "game_key": "multiplication_mayhem",
        "name": "Multiplication Mayhem 🎯",
        "description": "Master multiplication tables through rapid-fire challenges",
        "subject": "math",
        "icon": "🎯",
        "difficulties": ["easy", "medium", "hard"],
        "is_new": True
    },

    # ========== SCIENCE GAMES (4 total) ==========
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

    # ========== READING & WRITING GAMES (3 total) ==========
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
    # NEW READING GAME
    {
        "game_key": "reading_racer",
        "name": "Reading Racer 📖",
        "description": "Read passages and answer comprehension questions",
        "subject": "reading",
        "icon": "📖",
        "difficulties": ["easy", "medium", "hard"],
        "is_new": True
    },

    # ========== HISTORY & GEOGRAPHY GAMES (3 total) ==========
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
    # NEW GEOGRAPHY GAME
    {
        "game_key": "map_master",
        "name": "Map Master 🌍",
        "description": "Identify countries, states, and cities on maps",
        "subject": "history",
        "icon": "🌍",
        "difficulties": ["easy", "medium", "hard"],
        "is_new": True
    },

    # ========== BIBLE & FAITH GAME (1 total) ==========
    {
        "game_key": "bible_trivia",
        "name": "Bible Trivia ✝️",
        "description": "Test your knowledge of Bible stories and verses",
        "subject": "bible",
        "icon": "✝️",
        "difficulties": ["easy", "medium", "hard"],
        "is_new": True
    },

    # ========== NEW MAPVERSE GEOGRAPHY GAMES (4 total) ==========
    {
        "game_key": "country_spotter",
        "name": "Country Spotter 🌎",
        "description": "Identify countries by their outline and shape",
        "subject": "geography",
        "icon": "🌎",
        "difficulties": ["easy", "medium", "hard"],
        "is_new": True
    },
    {
        "game_key": "capital_quest",
        "name": "Capital Quest 🏛️",
        "description": "Match countries to their capitals in a race against time",
        "subject": "geography",
        "icon": "🏛️",
        "difficulties": ["easy", "medium", "hard"],
        "is_new": True
    },
    {
        "game_key": "flag_frenzy",
        "name": "Flag Frenzy 🚩",
        "description": "Identify countries by their flags",
        "subject": "geography",
        "icon": "🚩",
        "difficulties": ["easy", "medium", "hard"],
        "is_new": True
    },
    {
        "game_key": "landmark_locator",
        "name": "Landmark Locator 🗼",
        "description": "Match famous landmarks to countries and cities",
        "subject": "geography",
        "icon": "🗼",
        "difficulties": ["easy", "medium", "hard"],
        "is_new": True
    },

    # ========== FINANCIAL LITERACY GAMES (2 total) ==========
    {
        "game_key": "money_marathon",
        "name": "Money Marathon 💰",
        "description": "Make smart financial decisions under time pressure",
        "subject": "money",
        "icon": "💰",
        "difficulties": ["easy", "medium", "hard"],
        "is_new": True
    },
    {
        "game_key": "investment_simulator",
        "name": "Investment Simulator 📈",
        "description": "Build your portfolio and watch your wealth grow",
        "subject": "investing",
        "icon": "📈",
        "difficulties": ["easy", "medium", "hard"],
        "is_new": True
    },

    # ========== CHARACTER EDUCATION GAMES (2 total) ==========
    {
        "game_key": "etiquette_expert",
        "name": "Etiquette Expert 🎩",
        "description": "Choose the polite and respectful response in social situations",
        "subject": "manners",
        "icon": "🎩",
        "difficulties": ["easy", "medium", "hard"],
        "is_new": True
    },
    {
        "game_key": "virtue_quest",
        "name": "Virtue Quest ⚔️",
        "description": "Identify virtues and character traits in action",
        "subject": "manners",
        "icon": "⚔️",
        "difficulties": ["easy", "medium", "hard"],
        "is_new": True
    },

    # ========== CRITICAL THINKING GAMES (2 total) ==========
    {
        "game_key": "logic_lock",
        "name": "Logic Lock 🧩",
        "description": "Spot logical fallacies and test your reasoning skills",
        "subject": "apologetics",
        "icon": "🧩",
        "difficulties": ["easy", "medium", "hard"],
        "is_new": True
    },
    {
        "game_key": "worldview_warriors",
        "name": "Worldview Warriors 🛡️",
        "description": "Compare worldviews and defend biblical truth",
        "subject": "apologetics",
        "icon": "🛡️",
        "difficulties": ["easy", "medium", "hard"],
        "is_new": True
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
                difficulty_levels="easy,medium,hard"
            )
            db.session.add(game)

    db.session.commit()
    print(f"✅ Initialized {len(ARCADE_GAMES)} arcade games in database")


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def shuffle_question_options(question):
    """
    Shuffle the options array for a question while preserving the correct answer.
    This prevents predictable answer patterns (like always being at index 1).

    Args:
        question (dict): Question dict with 'answer' and 'options' keys

    Returns:
        dict: Same question with shuffled options
    """
    if 'options' not in question or 'answer' not in question:
        return question

    # Make a copy to avoid modifying the original
    shuffled_options = question['options'].copy()
    random.shuffle(shuffled_options)

    # Return updated question dict
    return {**question, 'options': shuffled_options}


def generate_multiple_choice(correct_answer, wrong_range=20, count=3):
    """Generate multiple choice options including the correct answer"""
    options = [correct_answer]

    while len(options) < 4:
        if isinstance(correct_answer, int):
            wrong = correct_answer + random.randint(-wrong_range, wrong_range)
            if wrong != correct_answer and wrong > 0 and wrong not in options:
                options.append(wrong)
        elif isinstance(correct_answer, float):
            wrong = round(correct_answer + random.uniform(-wrong_range, wrong_range), 2)
            if wrong != correct_answer and wrong > 0 and wrong not in options:
                options.append(wrong)

    random.shuffle(options)
    return options


# ============================================================
# GAME GENERATORS - UPDATED FOR DIFFICULTY
# ============================================================

def generate_speed_math(difficulty='medium'):
    """Generate math problems based on difficulty level"""
    reseed_random()  # Ensure fresh questions every time

    questions = []
    seen_questions = set()
    max_attempts = 200  # Prevent infinite loops

    attempts = 0
    while len(questions) < 20 and attempts < max_attempts:
        attempts += 1
        question = None
        if difficulty == 'easy':
            # Elementary level (grades 1-4)
            op = random.choice(["add", "subtract", "multiply"])
            if op == "add":
                a = random.randint(1, 50)
                b = random.randint(1, 50)
                question = {
                    "question": f"{a} + {b}",
                    "answer": a + b,
                    "type": "addition"
                }
            elif op == "subtract":
                a = random.randint(10, 100)
                b = random.randint(1, a)
                question = {
                    "question": f"{a} - {b}",
                    "answer": a - b,
                    "type": "subtraction"
                }
            else:  # multiply
                a = random.randint(2, 12)
                b = random.randint(2, 12)
                question = {
                    "question": f"{a} × {b}",
                    "answer": a * b,
                    "type": "multiplication"
                }

        elif difficulty == 'medium':
            # Middle school level (grades 5-8)
            op = random.choice(["add", "subtract", "multiply", "divide"])
            if op == "divide":
                b = random.randint(2, 15)
                answer = random.randint(2, 20)
                a = b * answer
                question = {
                    "question": f"{a} ÷ {b}",
                    "answer": answer,
                    "type": "division"
                }
            elif op == "multiply":
                a = random.randint(5, 25)
                b = random.randint(5, 25)
                question = {
                    "question": f"{a} × {b}",
                    "answer": a * b,
                    "type": "multiplication"
                }
            else:
                a = random.randint(10, 250)
                b = random.randint(10, 200)
                if op == "add":
                    question = {
                        "question": f"{a} + {b}",
                        "answer": a + b,
                        "type": "addition"
                    }
                else:
                    if a < b:
                        a, b = b, a
                    question = {
                        "question": f"{a} - {b}",
                        "answer": a - b,
                        "type": "subtraction"
                    }

        else:  # hard
            # High school level (grades 9-12)
            op = random.choice(["multiply", "percent", "algebra", "fraction"])
            if op == "percent":
                whole = random.randint(50, 500)
                pct = random.choice([10, 15, 20, 25, 30, 40, 50, 75])
                question = {
                    "question": f"{pct}% of {whole}",
                    "answer": int(whole * pct / 100),
                    "type": "percentage"
                }
            elif op == "algebra":
                # Simple: x + a = b
                a = random.randint(5, 50)
                b = random.randint(a + 5, 150)
                question = {
                    "question": f"x + {a} = {b}, solve for x",
                    "answer": b - a,
                    "type": "algebra"
                }
            elif op == "fraction":
                # Add fractions with same denominator
                denom = random.choice([2, 3, 4, 5, 6, 8, 10])
                num1 = random.randint(1, denom-1)
                num2 = random.randint(1, denom-1)
                total = num1 + num2
                if total < denom:
                    question = {
                        "question": f"{num1}/{denom} + {num2}/{denom}",
                        "answer": f"{total}/{denom}",
                        "type": "fraction"
                    }
                else:
                    # Fallback to multiplication
                    a = random.randint(15, 50)
                    b = random.randint(15, 50)
                    question = {
                        "question": f"{a} × {b}",
                        "answer": a * b,
                        "type": "multiplication"
                    }
            else:
                a = random.randint(15, 50)
                b = random.randint(15, 50)
                question = {
                    "question": f"{a} × {b}",
                    "answer": a * b,
                    "type": "multiplication"
                }

        # Check for duplicates before adding
        if question and not is_duplicate_question(question, seen_questions):
            questions.append(question)

    random.shuffle(questions)
    return questions


# ============================================================
# VOCABULARY BUILDER - UPDATED FOR DIFFICULTY
# ============================================================

VOCAB_SETS = {
    "easy": [
        {"word": "brave", "definition": "showing courage", "options": ["being scared", "showing courage", "staying quiet", "acting silly"]},
        {"word": "curious", "definition": "eager to learn", "options": ["feeling bored", "eager to learn", "being tired", "staying lazy"]},
        {"word": "enormous", "definition": "very large", "options": ["very tiny", "very large", "quite red", "really fast"]},
        {"word": "gleeful", "definition": "full of joy", "options": ["feeling sad", "being angry", "full of joy", "getting sick"]},
        {"word": "swift", "definition": "very fast", "options": ["very slow", "very fast", "quite heavy", "rather light"]},
        {"word": "gentle", "definition": "soft and kind", "options": ["being rough", "soft and kind", "very loud", "acting mean"]},
        {"word": "honest", "definition": "truthful", "options": ["always lying", "truthful", "being funny", "staying quiet"]},
        {"word": "proud", "definition": "feeling satisfied", "options": ["being ashamed", "feeling satisfied", "getting scared", "being tired"]},
        {"word": "clever", "definition": "smart and quick", "options": ["being dull", "smart and quick", "acting slow", "feeling lazy"]},
        {"word": "simple", "definition": "easy to understand", "options": ["hard to grasp", "easy to understand", "costly to buy", "bright and colorful"]},
        {"word": "quiet", "definition": "making little noise", "options": ["making loud sounds", "making little noise", "shining very bright", "weighing quite heavy"]},
        {"word": "polite", "definition": "having good manners", "options": ["acting quite rude", "having good manners", "feeling very tired", "being quite hungry"]},
        {"word": "bright", "definition": "giving much light", "options": ["being quite dark", "giving much light", "staying very quiet", "moving quite slow"]},
        {"word": "fresh", "definition": "newly made", "options": ["getting quite stale", "newly made", "being very hot", "feeling quite cold"]},
        {"word": "warm", "definition": "pleasantly hot", "options": ["feeling quite cold", "pleasantly hot", "being very wet", "staying quite dry"]},
        {"word": "strong", "definition": "having power", "options": ["being quite weak", "having power", "seeming very small", "looking quite thin"]},
        {"word": "tiny", "definition": "very small", "options": ["being quite huge", "very small", "sounding quite loud", "moving really fast"]},
        {"word": "funny", "definition": "causing laughter", "options": ["making people sad", "causing laughter", "being quite scary", "seeming very boring"]},
        {"word": "happy", "definition": "feeling joy", "options": ["being quite sad", "feeling joy", "getting very angry", "acting quite tired"]},
        {"word": "kind", "definition": "caring and helpful", "options": ["acting quite mean", "caring and helpful", "being very loud", "moving really fast"]},
    ],
    "medium": [
        {"word": "abundant", "definition": "existing in large quantities", "options": ["being quite scarce", "existing in large quantities", "costing very much", "looking quite bright"]},
        {"word": "meticulous", "definition": "very careful and precise", "options": ["acting quite careless", "very careful and precise", "sounding rather loud", "seeming quite mysterious"]},
        {"word": "reluctant", "definition": "unwilling or hesitant", "options": ["being very eager", "unwilling or hesitant", "feeling quite happy", "acting rather tired"]},
        {"word": "tranquil", "definition": "calm and peaceful", "options": ["wild and chaotic", "calm and peaceful", "shining very bright", "being quite dark"]},
        {"word": "vibrant", "definition": "full of energy and life", "options": ["being quite dull", "full of energy and life", "staying very quiet", "looking quite broken"]},
        {"word": "diligent", "definition": "hard-working and careful", "options": ["being quite lazy", "hard-working and careful", "acting very funny", "seeming rather mean"]},
        {"word": "eloquent", "definition": "fluent and persuasive in speech", "options": ["being quite inarticulate", "fluent and persuasive in speech", "staying very quiet", "acting rather rude"]},
        {"word": "resilient", "definition": "able to recover quickly", "options": ["being quite fragile", "able to recover quickly", "seeming rather weak", "moving very slow"]},
        {"word": "innovative", "definition": "featuring new methods", "options": ["following old traditions", "featuring new methods", "being quite boring", "costing very much"]},
        {"word": "compassionate", "definition": "showing sympathy and concern", "options": ["acting quite cruel", "showing sympathy and concern", "getting very angry", "feeling rather tired"]},
        {"word": "ambitious", "definition": "having strong desire for success", "options": ["feeling quite complacent", "having strong desire for success", "being very lazy", "feeling quite sleepy"]},
        {"word": "versatile", "definition": "able to adapt or be adapted", "options": ["being quite rigid", "able to adapt or be adapted", "seeming very boring", "costing too much"]},
        {"word": "persistent", "definition": "continuing firmly", "options": ["giving up easily", "continuing firmly", "being very lazy", "acting quite weak"]},
        {"word": "skeptical", "definition": "not easily convinced", "options": ["being very gullible", "not easily convinced", "feeling quite happy", "seeming very sad"]},
        {"word": "optimistic", "definition": "hopeful and confident", "options": ["being quite pessimistic", "hopeful and confident", "feeling very angry", "seeming quite sleepy"]},
        {"word": "genuine", "definition": "truly what it is said to be", "options": ["being completely fake", "truly what it is said to be", "appearing quite broken", "costing too much"]},
        {"word": "magnificent", "definition": "extremely beautiful", "options": ["looking quite ugly", "extremely beautiful", "being very small", "seeming quite boring"]},
        {"word": "triumphant", "definition": "having won a victory", "options": ["being completely defeated", "having won a victory", "feeling quite sleepy", "seeming very hungry"]},
        {"word": "peculiar", "definition": "strange or unusual", "options": ["appearing quite normal", "strange or unusual", "looking very bright", "seeming quite dark"]},
        {"word": "inevitable", "definition": "certain to happen", "options": ["being completely avoidable", "certain to happen", "seeming quite funny", "appearing very sad"]},
    ],
    "hard": [
        {"word": "articulate", "definition": "expressing oneself clearly", "options": ["mumbling incoherent words", "expressing oneself clearly", "singing random melodies", "whispering very quietly"]},
        {"word": "benevolent", "definition": "kind and generous", "options": ["acting quite cruel", "kind and generous", "seeming rather indifferent", "appearing very wealthy"]},
        {"word": "enigmatic", "definition": "mysterious and difficult to understand", "options": ["appearing completely obvious", "mysterious and difficult to understand", "seeming quite simple", "being rather boring"]},
        {"word": "pragmatic", "definition": "dealing with things realistically", "options": ["being overly idealistic", "dealing with things realistically", "acting very emotional", "seeming quite artistic"]},
        {"word": "tenacious", "definition": "persistent and determined", "options": ["giving up very easily", "persistent and determined", "being quite lazy", "feeling rather confused"]},
        {"word": "astute", "definition": "having sharp judgment", "options": ["acting quite foolish", "having sharp judgment", "moving very slow", "feeling rather tired"]},
        {"word": "circumspect", "definition": "wary and unwilling to take risks", "options": ["being completely reckless", "wary and unwilling to take risks", "acting very brave", "seeming quite happy"]},
        {"word": "erudite", "definition": "having great knowledge", "options": ["being completely ignorant", "having great knowledge", "appearing quite simple", "seeming rather boring"]},
        {"word": "fortuitous", "definition": "happening by chance", "options": ["being carefully planned", "happening by chance", "appearing quite boring", "seeming very sad"]},
        {"word": "garrulous", "definition": "excessively talkative", "options": ["being extremely quiet", "excessively talkative", "feeling quite sleepy", "acting very angry"]},
        {"word": "impetuous", "definition": "acting without thought", "options": ["being overly cautious", "acting without thought", "moving very slow", "seeming quite lazy"]},
        {"word": "judicious", "definition": "having good judgment", "options": ["acting quite reckless", "having good judgment", "appearing very simple", "moving quite quick"]},
        {"word": "lucid", "definition": "expressed clearly", "options": ["being extremely confusing", "expressed clearly", "appearing very dark", "seeming quite loud"]},
        {"word": "magnanimous", "definition": "generous or forgiving", "options": ["acting quite petty", "generous or forgiving", "being very mean", "appearing quite selfish"]},
        {"word": "nefarious", "definition": "wicked or criminal", "options": ["being completely virtuous", "wicked or criminal", "seeming very happy", "acting quite kind"]},
        {"word": "ostentatious", "definition": "designed to impress", "options": ["appearing quite modest", "designed to impress", "being very simple", "seeming quite quiet"]},
        {"word": "pernicious", "definition": "having harmful effect", "options": ["being truly beneficial", "having harmful effect", "appearing quite helpful", "seeming very kind"]},
        {"word": "ubiquitous", "definition": "present everywhere", "options": ["being extremely rare", "present everywhere", "appearing quite absent", "seeming completely missing"]},
        {"word": "vicarious", "definition": "experienced through another", "options": ["being completely direct", "experienced through another", "appearing quite personal", "seeming very immediate"]},
        {"word": "zealous", "definition": "filled with enthusiasm", "options": ["being quite apathetic", "filled with enthusiasm", "feeling very bored", "seeming rather tired"]},
    ]
}

def generate_vocab_builder(difficulty='medium'):
    """
    Generate vocabulary matching game with AI-generated fresh questions.
    Each time a student plays, they get completely new vocabulary words.
    """
    from modules.shared_ai import get_client

    # Define difficulty parameters
    difficulty_params = {
        'easy': {
            'grade_level': '3rd-5th grade',
            'word_complexity': 'simple everyday words',
            'num_words': 15
        },
        'medium': {
            'grade_level': '6th-8th grade',
            'word_complexity': 'intermediate academic vocabulary',
            'num_words': 15
        },
        'hard': {
            'grade_level': '9th-12th grade',
            'word_complexity': 'advanced SAT/ACT level vocabulary',
            'num_words': 15
        }
    }

    params = difficulty_params.get(difficulty, difficulty_params['medium'])

    prompt = f"""Generate {params['num_words']} unique vocabulary words for a {params['grade_level']} vocabulary matching game.

REQUIREMENTS:
1. Words should be {params['word_complexity']}
2. Each word needs a clear definition (2-4 words, like "showing great courage" or "having strong desire")
3. Each word needs 3 INCORRECT distractor options that:
   - Are plausible but wrong
   - Match the LENGTH and WORD COUNT of the correct definition
   - Are not obviously wrong
   - Use similar grammatical structure as correct answer

OUTPUT FORMAT (JSON array):
[
  {{
    "word": "brave",
    "definition": "showing great courage",
    "options": ["feeling very scared", "showing great courage", "acting quite silly", "being overly loud"]
  }},
  ...
]

CRITICAL: All 4 options must have similar length (2-4 words each). Do NOT use single-word distractors.
Make questions educational and age-appropriate. Avoid repetition across words.
Return ONLY the JSON array, no other text."""

    try:
        client = get_client()
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a vocabulary game generator. Return only valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.9  # Higher temperature for variety
        )

        import json
        vocab_data = json.loads(response.choices[0].message.content)

        # Shuffle options for each question to prevent position patterns
        shuffled_vocab = [shuffle_question_options(q) for q in vocab_data]
        return shuffled_vocab

    except Exception as e:
        print(f"Error generating vocab with AI: {e}")
        # Fallback to static questions if AI fails
        vocab_set = VOCAB_SETS.get(difficulty, VOCAB_SETS["medium"]).copy()
        random.shuffle(vocab_set)
        shuffled_vocab = [shuffle_question_options(q) for q in vocab_set[:15]]
        return shuffled_vocab


# ============================================================
# SCIENCE GAMES - UPDATED FOR DIFFICULTY
# ============================================================

SCIENCE_QUESTIONS = {
    "easy": [
        {"question": "What is H2O commonly known as?", "answer": "water", "options": ["water", "oxygen", "hydrogen", "salt"]},
        {"question": "What planet is known as the Red Planet?", "answer": "mars", "options": ["mars", "venus", "jupiter", "saturn"]},
        {"question": "What gas do plants absorb from the air?", "answer": "carbon dioxide", "options": ["carbon dioxide", "oxygen", "nitrogen", "helium"]},
        {"question": "What is the center of an atom called?", "answer": "nucleus", "options": ["nucleus", "proton", "electron", "neutron"]},
        {"question": "What force pulls objects toward Earth?", "answer": "gravity", "options": ["gravity", "magnetism", "friction", "pressure"]},
        {"question": "What do plants produce during photosynthesis?", "answer": "oxygen", "options": ["oxygen", "carbon dioxide", "nitrogen", "water"]},
        {"question": "What is the largest planet in our solar system?", "answer": "jupiter", "options": ["jupiter", "saturn", "earth", "mars"]},
        {"question": "What is the hottest planet?", "answer": "venus", "options": ["venus", "mercury", "mars", "jupiter"]},
        {"question": "What makes plants green?", "answer": "chlorophyll", "options": ["chlorophyll", "water", "soil", "sunlight"]},
        {"question": "How many legs does a spider have?", "answer": "8", "options": ["8", "6", "10", "4"]},
        {"question": "What is the closest star to Earth?", "answer": "the sun", "options": ["the sun", "north star", "sirius", "alpha centauri"]},
        {"question": "What is frozen water called?", "answer": "ice", "options": ["ice", "snow", "vapor", "steam"]},
        {"question": "What do we call animals that eat only plants?", "answer": "herbivores", "options": ["herbivores", "carnivores", "omnivores", "predators"]},
        {"question": "What gas do humans breathe in?", "answer": "oxygen", "options": ["oxygen", "carbon dioxide", "nitrogen", "helium"]},
        {"question": "What is the hardest natural substance?", "answer": "diamond", "options": ["diamond", "gold", "iron", "stone"]},
        {"question": "What is the Earth's natural satellite?", "answer": "the moon", "options": ["the moon", "the sun", "mars", "venus"]},
        {"question": "What do bees make?", "answer": "honey", "options": ["honey", "milk", "silk", "wax"]},
        {"question": "What is the center of the Earth called?", "answer": "core", "options": ["core", "crust", "mantle", "shell"]},
        {"question": "How many bones do adult humans have?", "answer": "206", "options": ["206", "300", "150", "100"]},
        {"question": "What do caterpillars turn into?", "answer": "butterflies", "options": ["butterflies", "moths", "bees", "dragonflies"]},
        {"question": "What is the study of living things called?", "answer": "biology", "options": ["biology", "geology", "astronomy", "chemistry"]},
        {"question": "What animal is known for changing colors?", "answer": "chameleon", "options": ["chameleon", "lizard", "frog", "snake"]},
        {"question": "What do you call a baby frog?", "answer": "tadpole", "options": ["tadpole", "froglet", "polliwog", "spawn"]},
        {"question": "What season comes after winter?", "answer": "spring", "options": ["spring", "summer", "fall", "autumn"]},
        {"question": "What is the largest mammal?", "answer": "blue whale", "options": ["blue whale", "elephant", "giraffe", "hippo"]},
        {"question": "How many wings does a bee have?", "answer": "4", "options": ["4", "2", "6", "8"]},
        {"question": "What is the fastest land animal?", "answer": "cheetah", "options": ["cheetah", "lion", "horse", "gazelle"]},
        {"question": "What do plants need to grow?", "answer": "sunlight, water, soil", "options": ["sunlight, water, soil", "only water", "only sunlight", "only soil"]},
        {"question": "What is the outer layer of Earth called?", "answer": "crust", "options": ["crust", "mantle", "core", "surface"]},
        {"question": "What color is a ruby?", "answer": "red", "options": ["red", "blue", "green", "yellow"]},
        {"question": "How many hearts does an octopus have?", "answer": "3", "options": ["3", "1", "2", "4"]},
        {"question": "What do we use to measure temperature?", "answer": "thermometer", "options": ["thermometer", "barometer", "scale", "ruler"]},
        {"question": "What is the tallest type of tree?", "answer": "redwood", "options": ["redwood", "oak", "pine", "maple"]},
        {"question": "What is steam made from?", "answer": "boiling water", "options": ["boiling water", "ice melting", "air heating", "fire burning"]},
        {"question": "What bird can't fly but swims?", "answer": "penguin", "options": ["penguin", "duck", "swan", "pelican"]},
        {"question": "What are clouds made of?", "answer": "water droplets", "options": ["water droplets", "cotton", "smoke", "air"]},
        {"question": "What is the nearest planet to the sun?", "answer": "mercury", "options": ["mercury", "venus", "earth", "mars"]},
        {"question": "How many eyes does a spider have?", "answer": "8", "options": ["8", "2", "6", "4"]},
        {"question": "What do bats use to see in the dark?", "answer": "echolocation", "options": ["echolocation", "night vision", "smell", "touch"]},
        {"question": "What is a baby kangaroo called?", "answer": "joey", "options": ["joey", "calf", "pup", "kit"]},
        {"question": "What is the largest desert?", "answer": "sahara", "options": ["sahara", "gobi", "mojave", "kalahari"]},
        {"question": "What organ helps you smell?", "answer": "nose", "options": ["nose", "tongue", "ears", "eyes"]},
        {"question": "What is the study of stars called?", "answer": "astronomy", "options": ["astronomy", "astrology", "geology", "biology"]},
        {"question": "How many teeth do adult humans have?", "answer": "32", "options": ["32", "28", "24", "20"]},
        {"question": "What animal is the biggest on land?", "answer": "elephant", "options": ["elephant", "rhino", "hippo", "giraffe"]},
        {"question": "What do you call molten rock?", "answer": "magma", "options": ["magma", "lava", "stone", "mineral"]},
        {"question": "What sense do you use to taste?", "answer": "tongue", "options": ["tongue", "nose", "mouth", "lips"]},
        {"question": "How many continents are there?", "answer": "7", "options": ["7", "5", "6", "8"]},
        {"question": "What is a group of fish called?", "answer": "school", "options": ["school", "herd", "flock", "pack"]},
        {"question": "What color is chlorophyll?", "answer": "green", "options": ["green", "yellow", "blue", "brown"]},
        {"question": "What is the opposite of evaporation?", "answer": "condensation", "options": ["condensation", "precipitation", "sublimation", "freezing"]},
        {"question": "How many planets are in our solar system?", "answer": "8", "options": ["8", "9", "7", "10"]},
        {"question": "What is the smallest planet?", "answer": "mercury", "options": ["mercury", "mars", "pluto", "venus"]},
        {"question": "What do you call animals without backbones?", "answer": "invertebrates", "options": ["invertebrates", "vertebrates", "mammals", "reptiles"]},
        {"question": "What gas makes soda fizzy?", "answer": "carbon dioxide", "options": ["carbon dioxide", "oxygen", "nitrogen", "helium"]},
        {"question": "What is the fastest bird?", "answer": "peregrine falcon", "options": ["peregrine falcon", "eagle", "hawk", "sparrow"]},
        {"question": "What is the boiling point of water in Fahrenheit?", "answer": "212°f", "options": ["212°f", "100°f", "32°f", "0°f"]},
        {"question": "What do you call a scientist who studies rocks?", "answer": "geologist", "options": ["geologist", "biologist", "chemist", "physicist"]},
        {"question": "What animal breathes through its skin?", "answer": "frog", "options": ["frog", "fish", "snake", "bird"]},
        {"question": "What is the largest ocean?", "answer": "pacific", "options": ["pacific", "atlantic", "indian", "arctic"]},
    ],
    "medium": [
        {"question": "What is the powerhouse of the cell?", "answer": "mitochondria", "options": ["mitochondria", "nucleus", "ribosome", "chloroplast"]},
        {"question": "What is the chemical symbol for gold?", "answer": "au", "options": ["au", "ag", "fe", "cu"]},
        {"question": "What type of rock is formed by cooling lava?", "answer": "igneous", "options": ["igneous", "sedimentary", "metamorphic", "granite"]},
        {"question": "What is the chemical formula for table salt?", "answer": "nacl", "options": ["nacl", "h2o", "co2", "o2"]},
        {"question": "What organelle contains DNA?", "answer": "nucleus", "options": ["nucleus", "ribosome", "vacuole", "cell wall"]},
        {"question": "What is the largest organ in the human body?", "answer": "skin", "options": ["skin", "liver", "heart", "brain"]},
        {"question": "What gas makes up most of Earth's atmosphere?", "answer": "nitrogen", "options": ["nitrogen", "oxygen", "carbon dioxide", "helium"]},
        {"question": "What is the process of water changing to vapor?", "answer": "evaporation", "options": ["evaporation", "condensation", "precipitation", "sublimation"]},
        {"question": "What are organisms that make their own food?", "answer": "producers", "options": ["producers", "consumers", "decomposers", "predators"]},
        {"question": "What is the smallest unit of life?", "answer": "cell", "options": ["cell", "atom", "molecule", "tissue"]},
        {"question": "What is the boiling point of water in Celsius?", "answer": "100°c", "options": ["100°c", "0°c", "50°c", "212°c"]},
        {"question": "What are the three states of matter?", "answer": "solid, liquid, gas", "options": ["solid, liquid, gas", "hot, cold, warm", "big, small, medium", "hard, soft, rough"]},
        {"question": "What is the chemical symbol for silver?", "answer": "ag", "options": ["ag", "au", "si", "s"]},
        {"question": "What organ pumps blood through the body?", "answer": "heart", "options": ["heart", "lungs", "liver", "kidneys"]},
        {"question": "What is the freezing point of water in Celsius?", "answer": "0°c", "options": ["0°c", "100°c", "32°c", "-10°c"]},
        {"question": "What part of the plant conducts photosynthesis?", "answer": "leaves", "options": ["leaves", "roots", "stem", "flowers"]},
        {"question": "What is photosynthesis?", "answer": "plants making food from sunlight", "options": ["plants making food from sunlight", "breathing", "cell division", "decomposition"]},
        {"question": "What type of energy does the sun provide?", "answer": "light and heat", "options": ["light and heat", "electrical", "chemical", "nuclear"]},
        {"question": "What is the study of weather called?", "answer": "meteorology", "options": ["meteorology", "geology", "biology", "astronomy"]},
        {"question": "What is speed of light approximately?", "answer": "300,000 km/s", "options": ["300,000 km/s", "150,000 km/s", "500,000 km/s", "1,000,000 km/s"]},
        {"question": "What is the chemical symbol for iron?", "answer": "fe", "options": ["fe", "ir", "i", "fn"]},
        {"question": "What is the process by which plants lose water?", "answer": "transpiration", "options": ["transpiration", "respiration", "evaporation", "condensation"]},
        {"question": "What type of animal is a frog?", "answer": "amphibian", "options": ["amphibian", "reptile", "mammal", "fish"]},
        {"question": "What is the formula for carbon dioxide?", "answer": "co2", "options": ["co2", "co", "o2", "c2o"]},
        {"question": "What is the longest bone in the human body?", "answer": "femur", "options": ["femur", "tibia", "humerus", "radius"]},
        {"question": "What layer of the atmosphere do we live in?", "answer": "troposphere", "options": ["troposphere", "stratosphere", "mesosphere", "thermosphere"]},
        {"question": "What is the process where liquid becomes solid?", "answer": "freezing", "options": ["freezing", "melting", "boiling", "evaporating"]},
        {"question": "What is the smallest bone in the human body?", "answer": "stapes", "options": ["stapes", "femur", "radius", "tibia"]},
        {"question": "What are animals that eat both plants and meat?", "answer": "omnivores", "options": ["omnivores", "herbivores", "carnivores", "producers"]},
        {"question": "What is the study of fossils called?", "answer": "paleontology", "options": ["paleontology", "archaeology", "geology", "biology"]},
        {"question": "What part of the cell controls activities?", "answer": "nucleus", "options": ["nucleus", "cytoplasm", "membrane", "mitochondria"]},
        {"question": "What is the unit of measurement for energy?", "answer": "joule", "options": ["joule", "watt", "newton", "pascal"]},
        {"question": "What is the primary gas in Earth's atmosphere?", "answer": "nitrogen", "options": ["nitrogen", "oxygen", "carbon dioxide", "argon"]},
        {"question": "What is the hardest mineral on Earth?", "answer": "diamond", "options": ["diamond", "quartz", "topaz", "corundum"]},
        {"question": "What organ filters blood in the body?", "answer": "kidneys", "options": ["kidneys", "liver", "lungs", "heart"]},
        {"question": "What is the process of cell eating?", "answer": "phagocytosis", "options": ["phagocytosis", "pinocytosis", "osmosis", "diffusion"]},
        {"question": "What are negatively charged particles?", "answer": "electrons", "options": ["electrons", "protons", "neutrons", "ions"]},
        {"question": "What is the study of earthquakes?", "answer": "seismology", "options": ["seismology", "geology", "volcanology", "meteorology"]},
        {"question": "What blood type is the universal donor?", "answer": "o negative", "options": ["o negative", "ab positive", "a positive", "b negative"]},
        {"question": "What is the largest artery in the body?", "answer": "aorta", "options": ["aorta", "carotid", "femoral", "pulmonary"]},
        {"question": "What is the unit of electric current?", "answer": "ampere", "options": ["ampere", "volt", "ohm", "watt"]},
        {"question": "What gas is released when vinegar and baking soda mix?", "answer": "carbon dioxide", "options": ["carbon dioxide", "oxygen", "hydrogen", "nitrogen"]},
        {"question": "What is the simplest form of matter?", "answer": "element", "options": ["element", "compound", "mixture", "molecule"]},
        {"question": "What causes tides on Earth?", "answer": "moon's gravity", "options": ["moon's gravity", "sun's heat", "earth's rotation", "wind"]},
        {"question": "What is the measure of acidity or alkalinity?", "answer": "ph", "options": ["ph", "temperature", "density", "mass"]},
        {"question": "What is the genetic material in cells?", "answer": "dna", "options": ["dna", "rna", "protein", "lipid"]},
        {"question": "What part of the brain controls balance?", "answer": "cerebellum", "options": ["cerebellum", "cerebrum", "medulla", "hypothalamus"]},
        {"question": "What is the speed of sound approximately?", "answer": "343 m/s", "options": ["343 m/s", "300 m/s", "400 m/s", "500 m/s"]},
        {"question": "What is the main component of natural gas?", "answer": "methane", "options": ["methane", "propane", "butane", "ethane"]},
        {"question": "What is the study of plants called?", "answer": "botany", "options": ["botany", "zoology", "ecology", "biology"]},
        {"question": "What is the chemical symbol for sodium?", "answer": "na", "options": ["na", "so", "s", "n"]},
        {"question": "What type of rock is marble?", "answer": "metamorphic", "options": ["metamorphic", "igneous", "sedimentary", "volcanic"]},
        {"question": "What is the normal human body temperature in Celsius?", "answer": "37°c", "options": ["37°c", "36°c", "38°c", "35°c"]},
        {"question": "What is the layer that protects Earth from UV rays?", "answer": "ozone layer", "options": ["ozone layer", "troposphere", "stratosphere", "mesosphere"]},
        {"question": "What is the longest river in the world?", "answer": "nile", "options": ["nile", "amazon", "mississippi", "yangtze"]},
        {"question": "What is the process where plants make their food?", "answer": "photosynthesis", "options": ["photosynthesis", "respiration", "transpiration", "digestion"]},
        {"question": "What is the charge of a proton?", "answer": "positive", "options": ["positive", "negative", "neutral", "variable"]},
        {"question": "What are the building blocks of all matter?", "answer": "atoms", "options": ["atoms", "molecules", "cells", "particles"]},
        {"question": "What is the pigment that makes blood red?", "answer": "hemoglobin", "options": ["hemoglobin", "chlorophyll", "melanin", "keratin"]},
    ],
    "hard": [
        {"question": "What is Avogadro's number?", "answer": "6.022 × 10²³", "options": ["6.022 × 10²³", "3.14 × 10⁸", "9.81 × 10¹⁰", "1.602 × 10⁻¹⁹"]},
        {"question": "What is the most abundant element in the universe?", "answer": "hydrogen", "options": ["hydrogen", "helium", "oxygen", "carbon"]},
        {"question": "What law states energy cannot be created or destroyed?", "answer": "conservation of energy", "options": ["conservation of energy", "newton's first law", "thermodynamics", "relativity"]},
        {"question": "What is DNA's shape called?", "answer": "double helix", "options": ["double helix", "single strand", "triple bond", "circular"]},
        {"question": "What particle has no electric charge?", "answer": "neutron", "options": ["neutron", "proton", "electron", "photon"]},
        {"question": "What is the SI unit of force?", "answer": "newton", "options": ["newton", "joule", "watt", "pascal"]},
        {"question": "What is the process of cell division called?", "answer": "mitosis", "options": ["mitosis", "meiosis", "osmosis", "photosynthesis"]},
        {"question": "What is the charge of an electron?", "answer": "negative", "options": ["negative", "positive", "neutral", "variable"]},
        {"question": "What is the universal solvent?", "answer": "water", "options": ["water", "alcohol", "acetone", "benzene"]},
        {"question": "What is the study of heredity?", "answer": "genetics", "options": ["genetics", "ecology", "anatomy", "physiology"]},
        {"question": "What are the basic building blocks of proteins?", "answer": "amino acids", "options": ["amino acids", "nucleotides", "lipids", "carbohydrates"]},
        {"question": "What is the atomic number of carbon?", "answer": "6", "options": ["6", "12", "8", "14"]},
        {"question": "What is Newton's first law called?", "answer": "law of inertia", "options": ["law of inertia", "law of acceleration", "law of action-reaction", "law of gravity"]},
        {"question": "What is the powerhouse of metabolism?", "answer": "atp", "options": ["atp", "glucose", "oxygen", "enzyme"]},
        {"question": "What is the pH of pure water?", "answer": "7", "options": ["7", "0", "14", "1"]},
        {"question": "What particle orbits the nucleus?", "answer": "electron", "options": ["electron", "proton", "neutron", "photon"]},
        {"question": "What is the process of liquid turning to gas?", "answer": "vaporization", "options": ["vaporization", "condensation", "sublimation", "deposition"]},
        {"question": "What is the strongest type of chemical bond?", "answer": "covalent", "options": ["covalent", "ionic", "hydrogen", "metallic"]},
        {"question": "What is the unit of electrical resistance?", "answer": "ohm", "options": ["ohm", "ampere", "volt", "watt"]},
        {"question": "What is Planck's constant used for?", "answer": "quantum mechanics", "options": ["quantum mechanics", "relativity", "thermodynamics", "electromagnetism"]},
        {"question": "What is the formula for calculating force?", "answer": "f = ma", "options": ["f = ma", "e = mc²", "p = mv", "w = fd"]},
        {"question": "What are the four fundamental forces?", "answer": "gravity, electromagnetic, strong, weak", "options": ["gravity, electromagnetic, strong, weak", "gravity, magnetic, electric, nuclear", "strong, weak, normal, friction", "push, pull, lift, drag"]},
        {"question": "What is entropy?", "answer": "measure of disorder", "options": ["measure of disorder", "measure of energy", "measure of force", "measure of mass"]},
        {"question": "What is the second law of thermodynamics?", "answer": "entropy always increases", "options": ["entropy always increases", "energy is conserved", "action equals reaction", "inertia stays constant"]},
        {"question": "What is the Heisenberg uncertainty principle?", "answer": "position and momentum can't both be known exactly", "options": ["position and momentum can't both be known exactly", "energy and time are related", "mass and energy are equivalent", "light has wave-particle duality"]},
        {"question": "What is the process of sexual cell division?", "answer": "meiosis", "options": ["meiosis", "mitosis", "cytokinesis", "binary fission"]},
        {"question": "What is the primary function of ribosomes?", "answer": "protein synthesis", "options": ["protein synthesis", "dna replication", "energy production", "waste removal"]},
        {"question": "What are the three types of RNA?", "answer": "mrna, trna, rrna", "options": ["mrna, trna, rrna", "dna, rna, arna", "nuclear, cytoplasmic, mitochondrial", "coding, non-coding, regulatory"]},
        {"question": "What is the difference between exothermic and endothermic?", "answer": "releases vs absorbs heat", "options": ["releases vs absorbs heat", "fast vs slow reaction", "reversible vs irreversible", "catalyzed vs uncatalyzed"]},
        {"question": "What is molarity?", "answer": "moles per liter", "options": ["moles per liter", "mass per volume", "atoms per mole", "grams per liter"]},
        {"question": "What is the ideal gas law?", "answer": "pv = nrt", "options": ["pv = nrt", "f = ma", "e = mc²", "v = ir"]},
        {"question": "What are isotopes?", "answer": "same element, different neutrons", "options": ["same element, different neutrons", "different elements, same electrons", "same mass, different charge", "different atoms, same size"]},
        {"question": "What is oxidation?", "answer": "loss of electrons", "options": ["loss of electrons", "gain of electrons", "sharing electrons", "transfer of protons"]},
        {"question": "What is the first law of thermodynamics?", "answer": "energy is conserved", "options": ["energy is conserved", "entropy increases", "matter is conserved", "momentum is conserved"]},
        {"question": "What is Le Chatelier's principle?", "answer": "equilibrium shifts to counter changes", "options": ["equilibrium shifts to counter changes", "reactions go to completion", "energy is minimized", "entropy is maximized"]},
        {"question": "What is the periodic table organized by?", "answer": "atomic number", "options": ["atomic number", "atomic mass", "electron count", "neutron count"]},
        {"question": "What are valence electrons?", "answer": "outermost electrons", "options": ["outermost electrons", "innermost electrons", "nucleus electrons", "free electrons"]},
        {"question": "What is electromagnetic radiation?", "answer": "energy transmitted as waves", "options": ["energy transmitted as waves", "charged particles in motion", "static electric fields", "magnetic field lines"]},
        {"question": "What is specific heat capacity?", "answer": "energy to raise 1g by 1°c", "options": ["energy to raise 1g by 1°c", "total energy in substance", "energy per mole", "heat of fusion"]},
        {"question": "What are covalent bonds?", "answer": "shared electrons", "options": ["shared electrons", "transferred electrons", "attracted ions", "metallic lattice"]},
        {"question": "What is the difference between kinetic and potential energy?", "answer": "motion vs position", "options": ["motion vs position", "heat vs cold", "electrical vs mechanical", "nuclear vs chemical"]},
        {"question": "What is a catalyst?", "answer": "speeds reaction without being consumed", "options": ["speeds reaction without being consumed", "provides energy for reaction", "combines with reactants", "increases yield"]},
        {"question": "What is wave-particle duality?", "answer": "light acts as both wave and particle", "options": ["light acts as both wave and particle", "matter and energy are the same", "waves can become particles", "particles create waves"]},
        {"question": "What is the electromagnetic spectrum?", "answer": "all wavelengths of em radiation", "options": ["all wavelengths of em radiation", "visible light only", "radio to microwave", "infrared to ultraviolet"]},
        {"question": "What is half-life?", "answer": "time for half to decay", "options": ["time for half to decay", "time to double", "time to react completely", "average lifetime"]},
        {"question": "What is the difference between mass and weight?", "answer": "mass is matter, weight is force", "options": ["mass is matter, weight is force", "mass is heavier than weight", "weight is constant, mass changes", "no difference"]},
        {"question": "What is osmosis?", "answer": "water moving across membrane", "options": ["water moving across membrane", "diffusion of gases", "active transport", "cell division"]},
        {"question": "What is the electron configuration of oxygen?", "answer": "1s² 2s² 2p⁴", "options": ["1s² 2s² 2p⁴", "1s² 2s² 2p⁶", "1s² 2p⁶", "2s² 2p⁴"]},
        {"question": "What is a buffer solution?", "answer": "resists ph changes", "options": ["resists ph changes", "highly acidic", "highly basic", "neutral solution"]},
        {"question": "What is quantum entanglement?", "answer": "particles linked regardless of distance", "options": ["particles linked regardless of distance", "electrons orbiting nucleus", "wave interference", "energy quantization"]},
        {"question": "What is the function of telomeres?", "answer": "protect chromosome ends", "options": ["protect chromosome ends", "code for proteins", "regulate genes", "store genetic info"]},
        {"question": "What is redox reaction?", "answer": "simultaneous oxidation and reduction", "options": ["simultaneous oxidation and reduction", "acid-base neutralization", "precipitation reaction", "combustion reaction"]},
        {"question": "What is the doppler effect?", "answer": "frequency change due to motion", "options": ["frequency change due to motion", "light bending in gravity", "wave interference", "sound reflection"]},
        {"question": "What is the difference between accuracy and precision?", "answer": "closeness to true vs consistent values", "options": ["closeness to true vs consistent values", "precise is always accurate", "accuracy is measurement, precision is calculation", "no difference"]},
        {"question": "What is an allele?", "answer": "variant form of a gene", "options": ["variant form of a gene", "type of chromosome", "dna sequence", "protein product"]},
        {"question": "What is the greenhouse effect?", "answer": "atmosphere traps heat", "options": ["atmosphere traps heat", "plants releasing oxygen", "ocean currents warming", "solar radiation increasing"]},
        {"question": "What is superconductivity?", "answer": "zero electrical resistance", "options": ["zero electrical resistance", "infinite conductivity", "perfect insulation", "high efficiency"]},
        {"question": "What is the strong nuclear force?", "answer": "holds nucleus together", "options": ["holds nucleus together", "attracts electrons", "creates gravity", "generates magnetism"]},
        {"question": "What is the Pauli exclusion principle?", "answer": "no two electrons same quantum state", "options": ["no two electrons same quantum state", "electrons orbit in pairs", "electrons repel each other", "electrons have fixed energy"]},
    ]
}

def generate_science_quiz(difficulty='medium'):
    """Generate science trivia questions based on difficulty"""
    questions = SCIENCE_QUESTIONS.get(difficulty, SCIENCE_QUESTIONS["medium"]).copy()
    random.shuffle(questions)

    # Shuffle options for each question to prevent predictable patterns
    shuffled_questions = [shuffle_question_options(q) for q in questions[:20]]
    return shuffled_questions


# ============================================================
# NEW GAME 1: MULTIPLICATION MAYHEM
# ============================================================

def generate_multiplication_mayhem(difficulty='medium'):
    """Master multiplication tables through rapid-fire challenges"""
    questions = []
    seen_questions = set()
    max_attempts = 200

    attempts = 0
    while len(questions) < 20 and attempts < max_attempts:
        attempts += 1

        if difficulty == 'easy':
            # 1-5 times tables
            a = random.randint(1, 5)
            b = random.randint(1, 10)
        elif difficulty == 'medium':
            # 1-12 times tables
            a = random.randint(1, 12)
            b = random.randint(1, 12)
        else:  # hard
            # Larger numbers and mixed difficulty
            if random.random() < 0.5:
                # Double-digit multiplication
                a = random.randint(10, 25)
                b = random.randint(10, 25)
            else:
                # Three-digit by one-digit
                a = random.randint(100, 999)
                b = random.randint(2, 9)

        answer = a * b
        question = {
            "question": f"{a} × {b}",
            "answer": answer,
            "type": "multiplication",
            "options": generate_multiple_choice(answer, wrong_range=max(20, answer // 5))
        }

        if not is_duplicate_question(question, seen_questions):
            questions.append(question)

    return questions


# ============================================================
# NEW GAME 2: READING RACER
# ============================================================

READING_PASSAGES = {
    "easy": [
        {
            "passage": "The cat sat on the mat. It was a big, fluffy cat with orange fur. The cat liked to sleep in the sun. It purred when it was happy.",
            "questions": [
                {"q": "What color was the cat?", "a": "orange", "opts": ["orange", "black", "white", "brown"]},
                {"q": "Where did the cat sit?", "a": "on the mat", "opts": ["on the mat", "on the chair", "in a box", "on the bed"]},
                {"q": "What did the cat like to do?", "a": "sleep in the sun", "opts": ["sleep in the sun", "play with toys", "chase mice", "climb trees"]},
            ]
        },
        {
            "passage": "Dogs are loyal pets. They can learn tricks and help people. Some dogs work as helpers for people who cannot see. Dogs wag their tails when they are happy.",
            "questions": [
                {"q": "What makes dogs good pets?", "a": "they are loyal", "opts": ["they are loyal", "they are big", "they are small", "they sleep a lot"]},
                {"q": "What do dogs do when happy?", "a": "wag their tails", "opts": ["wag their tails", "bark loudly", "sleep", "run away"]},
                {"q": "What can some dogs help with?", "a": "helping people who cannot see", "opts": ["helping people who cannot see", "cooking food", "building houses", "driving cars"]},
            ]
        },
    ],
    "medium": [
        {
            "passage": "Photosynthesis is the process plants use to make food. Plants take in carbon dioxide from the air and water from the soil. Using energy from sunlight, they convert these into glucose and oxygen. The oxygen is released into the air, which animals need to breathe.",
            "questions": [
                {"q": "What do plants make during photosynthesis?", "a": "glucose and oxygen", "opts": ["glucose and oxygen", "water and carbon dioxide", "soil and air", "sunlight and energy"]},
                {"q": "Where do plants get carbon dioxide?", "a": "from the air", "opts": ["from the air", "from the soil", "from water", "from sunlight"]},
                {"q": "What energy source do plants use?", "a": "sunlight", "opts": ["sunlight", "electricity", "wind", "heat"]},
            ]
        },
        {
            "passage": "The water cycle is the continuous movement of water on Earth. Water evaporates from oceans and lakes into the atmosphere. It forms clouds through condensation. When clouds become heavy, precipitation falls as rain or snow. This water returns to bodies of water, completing the cycle.",
            "questions": [
                {"q": "What happens when water evaporates?", "a": "it goes into the atmosphere", "opts": ["it goes into the atmosphere", "it freezes", "it disappears", "it turns into soil"]},
                {"q": "How do clouds form?", "a": "through condensation", "opts": ["through condensation", "through evaporation", "through precipitation", "through freezing"]},
                {"q": "What is precipitation?", "a": "rain or snow", "opts": ["rain or snow", "evaporation", "clouds", "oceans"]},
            ]
        },
    ],
    "hard": [
        {
            "passage": "Quantum mechanics revolutionized physics in the early 20th century. Unlike classical physics, which describes the macroscopic world, quantum mechanics governs the behavior of subatomic particles. The uncertainty principle states that we cannot simultaneously know both the exact position and momentum of a particle. This fundamental limitation challenges our intuitive understanding of reality.",
            "questions": [
                {"q": "What does quantum mechanics govern?", "a": "subatomic particles", "opts": ["subatomic particles", "large objects", "planets", "galaxies"]},
                {"q": "What can't be known simultaneously?", "a": "position and momentum", "opts": ["position and momentum", "mass and energy", "time and space", "speed and direction"]},
                {"q": "When did quantum mechanics develop?", "a": "early 20th century", "opts": ["early 20th century", "19th century", "18th century", "21st century"]},
            ]
        },
        {
            "passage": "DNA replication is a fundamental process in all living organisms. The double helix structure unwinds, and each strand serves as a template for creating a new complementary strand. DNA polymerase enzymes facilitate this process, reading the template strand and adding nucleotides. This semi-conservative replication ensures genetic information is accurately passed to daughter cells.",
            "questions": [
                {"q": "What enzyme facilitates DNA replication?", "a": "DNA polymerase", "opts": ["DNA polymerase", "RNA polymerase", "helicase", "ligase"]},
                {"q": "What does each DNA strand become?", "a": "a template", "opts": ["a template", "a protein", "an enzyme", "a cell"]},
                {"q": "What type of replication is this?", "a": "semi-conservative", "opts": ["semi-conservative", "conservative", "dispersive", "random"]},
            ]
        },
    ]
}

def generate_reading_racer(difficulty='medium'):
    """Read passages and answer comprehension questions"""
    passages = READING_PASSAGES.get(difficulty, READING_PASSAGES["medium"])

    # Select 5-7 passages and extract questions to get ~20 questions total
    num_passages = min(7, len(passages))
    selected_passages = random.sample(passages, num_passages)

    questions = []
    for passage_data in selected_passages:
        for q_data in passage_data["questions"]:
            questions.append({
                "passage": passage_data["passage"],
                "question": q_data["q"],
                "answer": q_data["a"],
                "options": q_data["opts"],
                "type": "comprehension"
            })

    # Fill to 20 questions if needed
    while len(questions) < 20:
        passage_data = random.choice(passages)
        q_data = random.choice(passage_data["questions"])
        questions.append({
            "passage": passage_data["passage"],
            "question": q_data["q"],
            "answer": q_data["a"],
            "options": q_data["opts"],
            "type": "comprehension"
        })

    random.shuffle(questions)

    # Shuffle options for each question to prevent predictable patterns
    shuffled_questions = [shuffle_question_options(q) for q in questions[:20]]
    return shuffled_questions


# ============================================================
# NEW GAME 3: MAP MASTER
# ============================================================

MAP_QUESTIONS = {
    "easy": [
        {"question": "What continent is the United States in?", "answer": "North America", "options": ["North America", "South America", "Europe", "Asia"]},
        {"question": "What ocean is west of the United States?", "answer": "Pacific", "options": ["Pacific", "Atlantic", "Indian", "Arctic"]},
        {"question": "What country is north of the United States?", "answer": "Canada", "options": ["Canada", "Mexico", "Cuba", "Brazil"]},
        {"question": "What country is south of the United States?", "answer": "Mexico", "options": ["Mexico", "Canada", "Brazil", "Cuba"]},
        {"question": "What ocean is east of the United States?", "answer": "Atlantic", "options": ["Atlantic", "Pacific", "Indian", "Arctic"]},
        {"question": "What is the capital of the United States?", "answer": "Washington DC", "options": ["Washington DC", "New York", "Los Angeles", "Chicago"]},
        {"question": "What state is known as the Sunshine State?", "answer": "Florida", "options": ["Florida", "California", "Texas", "Hawaii"]},
        {"question": "What state is the largest by area?", "answer": "Alaska", "options": ["Alaska", "Texas", "California", "Montana"]},
        {"question": "What ocean touches California?", "answer": "Pacific", "options": ["Pacific", "Atlantic", "Indian", "Arctic"]},
        {"question": "What continent has the most countries?", "answer": "Africa", "options": ["Africa", "Asia", "Europe", "South America"]},
        {"question": "Which state is an island?", "answer": "Hawaii", "options": ["Hawaii", "Florida", "California", "Alaska"]},
        {"question": "What is the longest river in the US?", "answer": "Missouri", "options": ["Missouri", "Mississippi", "Colorado", "Rio Grande"]},
        {"question": "What mountain range is in the western US?", "answer": "Rocky Mountains", "options": ["Rocky Mountains", "Appalachian", "Cascades", "Sierra Nevada"]},
        {"question": "What are the Great Lakes near?", "answer": "Canada border", "options": ["Canada border", "Mexico border", "Pacific Ocean", "Atlantic Ocean"]},
        {"question": "What desert is in the southwestern US?", "answer": "Mojave", "options": ["Mojave", "Sahara", "Gobi", "Arabian"]},
        {"question": "What state has the Grand Canyon?", "answer": "Arizona", "options": ["Arizona", "Utah", "Nevada", "New Mexico"]},
        {"question": "What is the smallest state?", "answer": "Rhode Island", "options": ["Rhode Island", "Delaware", "Connecticut", "Hawaii"]},
        {"question": "What city is known as the Big Apple?", "answer": "New York City", "options": ["New York City", "Los Angeles", "Chicago", "Boston"]},
        {"question": "What state is Hollywood in?", "answer": "California", "options": ["California", "Nevada", "Florida", "New York"]},
        {"question": "What is the hottest state on average?", "answer": "Florida", "options": ["Florida", "Arizona", "Texas", "California"]},
    ],
    "medium": [
        {"question": "What is the capital of France?", "answer": "Paris", "options": ["Paris", "London", "Berlin", "Rome"]},
        {"question": "What country has the Eiffel Tower?", "answer": "France", "options": ["France", "Italy", "Spain", "England"]},
        {"question": "What is the capital of Japan?", "answer": "Tokyo", "options": ["Tokyo", "Beijing", "Seoul", "Bangkok"]},
        {"question": "What is the capital of Germany?", "answer": "Berlin", "options": ["Berlin", "Munich", "Frankfurt", "Hamburg"]},
        {"question": "What country has the Great Wall?", "answer": "China", "options": ["China", "Japan", "Korea", "Mongolia"]},
        {"question": "What is the capital of Italy?", "answer": "Rome", "options": ["Rome", "Milan", "Venice", "Florence"]},
        {"question": "Where is the Taj Mahal?", "answer": "India", "options": ["India", "Pakistan", "Bangladesh", "Nepal"]},
        {"question": "What is the capital of Spain?", "answer": "Madrid", "options": ["Madrid", "Barcelona", "Seville", "Valencia"]},
        {"question": "What country is shaped like a boot?", "answer": "Italy", "options": ["Italy", "Greece", "Spain", "Portugal"]},
        {"question": "What is the capital of Canada?", "answer": "Ottawa", "options": ["Ottawa", "Toronto", "Montreal", "Vancouver"]},
        {"question": "Where is Machu Picchu?", "answer": "Peru", "options": ["Peru", "Bolivia", "Ecuador", "Colombia"]},
        {"question": "What is the capital of Australia?", "answer": "Canberra", "options": ["Canberra", "Sydney", "Melbourne", "Brisbane"]},
        {"question": "What strait separates Africa and Europe?", "answer": "Gibraltar", "options": ["Gibraltar", "Bering", "Hormuz", "Bosphorus"]},
        {"question": "What is the driest desert?", "answer": "Atacama", "options": ["Atacama", "Sahara", "Gobi", "Mojave"]},
        {"question": "What country has the most pyramids?", "answer": "Sudan", "options": ["Sudan", "Egypt", "Mexico", "Peru"]},
        {"question": "What is the highest mountain in Africa?", "answer": "Kilimanjaro", "options": ["Kilimanjaro", "Kenya", "Atlas", "Drakensberg"]},
        {"question": "What sea is between Europe and Africa?", "answer": "Mediterranean", "options": ["Mediterranean", "Red Sea", "Black Sea", "Caspian"]},
        {"question": "What is the southernmost continent?", "answer": "Antarctica", "options": ["Antarctica", "Australia", "South America", "Africa"]},
        {"question": "What country has the most islands?", "answer": "Sweden", "options": ["Sweden", "Indonesia", "Philippines", "Japan"]},
        {"question": "What canal connects two oceans?", "answer": "Panama Canal", "options": ["Panama Canal", "Suez Canal", "Erie Canal", "Kiel Canal"]},
    ],
    "hard": [
        {"question": "What is the only country in both Europe and Asia?", "answer": "Russia", "options": ["Russia", "Turkey", "Kazakhstan", "Azerbaijan"]},
        {"question": "What is the deepest ocean trench?", "answer": "Mariana Trench", "options": ["Mariana Trench", "Puerto Rico Trench", "Java Trench", "Philippine Trench"]},
        {"question": "What African country was never colonized?", "answer": "Ethiopia", "options": ["Ethiopia", "Liberia", "Egypt", "Morocco"]},
        {"question": "What is the world's smallest country?", "answer": "Vatican City", "options": ["Vatican City", "Monaco", "San Marino", "Liechtenstein"]},
        {"question": "What strait separates Asia and North America?", "answer": "Bering Strait", "options": ["Bering Strait", "Gibraltar", "Hormuz", "Malacca"]},
        {"question": "What is the driest place on Earth?", "answer": "Atacama Desert", "options": ["Atacama Desert", "Death Valley", "Sahara", "Antarctica"]},
        {"question": "What ocean current warms Western Europe?", "answer": "Gulf Stream", "options": ["Gulf Stream", "Kuroshio", "Humboldt", "California"]},
        {"question": "What mountain range separates Europe and Asia?", "answer": "Ural Mountains", "options": ["Ural Mountains", "Caucasus", "Himalayas", "Alps"]},
        {"question": "What is the largest landlocked country?", "answer": "Kazakhstan", "options": ["Kazakhstan", "Mongolia", "Chad", "Bolivia"]},
        {"question": "What sea has the highest salinity?", "answer": "Dead Sea", "options": ["Dead Sea", "Red Sea", "Black Sea", "Caspian Sea"]},
        {"question": "What river flows through the most countries?", "answer": "Danube", "options": ["Danube", "Nile", "Amazon", "Rhine"]},
        {"question": "What is the Ring of Fire?", "answer": "volcanic belt around Pacific", "options": ["volcanic belt around Pacific", "desert region", "trade route", "ocean current"]},
        {"question": "What country has the most time zones?", "answer": "France", "options": ["France", "Russia", "USA", "China"]},
        {"question": "What is the lowest point on Earth's land?", "answer": "Dead Sea shore", "options": ["Dead Sea shore", "Death Valley", "Caspian Sea", "Lake Assal"]},
        {"question": "What African lake is the deepest?", "answer": "Lake Tanganyika", "options": ["Lake Tanganyika", "Lake Victoria", "Lake Malawi", "Lake Chad"]},
        {"question": "What is the world's longest mountain range?", "answer": "Andes", "options": ["Andes", "Rockies", "Himalayas", "Alps"]},
        {"question": "What line divides North and South Korea?", "answer": "38th parallel", "options": ["38th parallel", "DMZ", "Yalu River", "17th parallel"]},
        {"question": "What is the largest island?", "answer": "Greenland", "options": ["Greenland", "New Guinea", "Borneo", "Madagascar"]},
        {"question": "What ocean is the smallest?", "answer": "Arctic", "options": ["Arctic", "Indian", "Southern", "Atlantic"]},
        {"question": "What country spans 11 time zones?", "answer": "Russia", "options": ["Russia", "USA", "China", "Canada"]},
    ]
}

def generate_map_master(difficulty='medium'):
    """Identify countries, states, and cities on maps"""
    questions = MAP_QUESTIONS.get(difficulty, MAP_QUESTIONS["medium"]).copy()
    random.shuffle(questions)

    # Shuffle options for each question to prevent predictable patterns
    shuffled_questions = [shuffle_question_options(q) for q in questions[:20]]
    return shuffled_questions


# ============================================================
# KEEP ALL EXISTING GAMES FROM ORIGINAL FILE
# ============================================================

def generate_number_detective(difficulty='medium'):
    """Find patterns and solve number mysteries"""
    questions = []
    seen_questions = set()
    max_attempts = 200

    attempts = 0
    while len(questions) < 20 and attempts < max_attempts:
        attempts += 1
        pattern_type = random.choice(["sequence", "missing", "odd_one_out"])

        if difficulty == 'easy':
            start = random.randint(2, 10)
            step = random.choice([2, 5])
        elif difficulty == 'medium':
            start = random.randint(2, 20)
            step = random.choice([2, 3, 5, 10])
        else:  # hard
            start = random.randint(5, 50)
            step = random.choice([3, 4, 7, 11, 13])

        question = None
        if pattern_type == "sequence":
            seq = [start + i * step for i in range(5)]
            answer = seq[-1] + step
            question = {
                "question": f"What comes next? {', '.join(map(str, seq))}, __",
                "answer": answer,
                "type": "sequence",
                "options": [answer, answer + 1, answer - 1, answer + step]
            }
        elif pattern_type == "missing":
            seq = [start + i * step for i in range(4)]
            missing_idx = random.randint(1, 2)
            answer = seq[missing_idx]
            seq[missing_idx] = "?"
            question = {
                "question": f"Find the missing number: {', '.join(map(str, seq))}",
                "answer": answer,
                "type": "missing",
                "options": [answer, answer + 1, answer - 1, answer + step]
            }
        else:
            base = random.randint(2, 10) * 2
            evens = [base + i * 2 for i in range(3)]
            odd = random.randint(1, 20) * 2 + 1
            nums = evens + [odd]
            random.shuffle(nums)
            question = {
                "question": f"Which number is odd? {', '.join(map(str, nums))}",
                "answer": odd,
                "type": "odd_one_out",
                "options": nums
            }

        if question and not is_duplicate_question(question, seen_questions):
            questions.append(question)

    return questions


def generate_fraction_frenzy(difficulty='medium'):
    """Match equivalent fractions"""
    questions = []
    seen_questions = set()
    max_attempts = 200

    attempts = 0
    while len(questions) < 20 and attempts < max_attempts:
        attempts += 1

        if difficulty == 'easy':
            num = random.randint(1, 4)
            den = random.randint(num + 1, 8)
        elif difficulty == 'medium':
            num = random.randint(1, 8)
            den = random.randint(num + 1, 12)
        else:  # hard
            num = random.randint(1, 12)
            den = random.randint(num + 1, 20)

        mult = random.choice([2, 3, 4])
        equiv_num = num * mult
        equiv_den = den * mult

        question_type = random.choice(["match", "simplify"])

        question = None
        if question_type == "match":
            question = {
                "question": f"Which fraction equals {num}/{den}?",
                "answer": f"{equiv_num}/{equiv_den}",
                "type": "match",
                "options": [
                    f"{equiv_num}/{equiv_den}",
                    f"{equiv_num + 1}/{equiv_den}",
                    f"{equiv_num}/{equiv_den + 1}",
                    f"{num}/{den + 1}"
                ]
            }
        else:
            question = {
                "question": f"Simplify: {equiv_num}/{equiv_den}",
                "answer": f"{num}/{den}",
                "type": "simplify",
                "options": [
                    f"{num}/{den}",
                    f"{num + 1}/{den}",
                    f"{num}/{den + 1}",
                    f"{equiv_num}/{den}"
                ]
            }

        if question and not is_duplicate_question(question, seen_questions):
            questions.append(question)

    return questions


def generate_equation_race(difficulty='medium'):
    """Solve equations faster than your grade level"""
    questions = []
    seen_questions = set()
    max_attempts = 200

    attempts = 0
    while len(questions) < 20 and attempts < max_attempts:
        attempts += 1
        question = None

        if difficulty == 'easy':
            a = random.randint(5, 20)
            x = random.randint(10, 30)
            op = random.choice(["+", "-"])

            if op == "+":
                b = x + a
                question = {
                    "question": f"Solve: x + {a} = {b}",
                    "answer": x,
                    "type": "one_step"
                }
            else:
                b = x - a
                question = {
                    "question": f"Solve: x - {a} = {b}",
                    "answer": x,
                    "type": "one_step"
                }
        elif difficulty == 'medium':
            a = random.randint(5, 30)
            x = random.randint(10, 50)
            op = random.choice(["+", "-"])

            if op == "+":
                b = x + a
                question = {
                    "question": f"Solve: x + {a} = {b}",
                    "answer": x,
                    "type": "one_step"
                }
            else:
                b = x - a
                question = {
                    "question": f"Solve: x - {a} = {b}",
                    "answer": x,
                    "type": "one_step"
                }
        else:  # hard
            a = random.randint(2, 10)
            x = random.randint(5, 20)
            b = random.randint(5, 30)
            c = a * x + b

            question = {
                "question": f"Solve: {a}x + {b} = {c}",
                "answer": x,
                "type": "two_step"
            }

        if question and not is_duplicate_question(question, seen_questions):
            questions.append(question)

    return questions


def generate_element_match(difficulty='medium'):
    """Match chemical symbols to element names"""

    elements_easy = [
        {"symbol": "H", "name": "Hydrogen", "options": ["Hydrogen", "Helium", "Hafnium", "Holmium"]},
        {"symbol": "O", "name": "Oxygen", "options": ["Oxygen", "Osmium", "Oganesson", "Oxide"]},
        {"symbol": "C", "name": "Carbon", "options": ["Carbon", "Calcium", "Copper", "Chromium"]},
        {"symbol": "N", "name": "Nitrogen", "options": ["Nitrogen", "Neon", "Nickel", "Nobelium"]},
        {"symbol": "Fe", "name": "Iron", "options": ["Iron", "Fluorine", "Fermium", "Francium"]},
        {"symbol": "Au", "name": "Gold", "options": ["Gold", "Silver", "Aluminum", "Argon"]},
        {"symbol": "Ag", "name": "Silver", "options": ["Silver", "Gold", "Argon", "Arsenic"]},
        {"symbol": "Na", "name": "Sodium", "options": ["Sodium", "Nitrogen", "Neon", "Nickel"]},
        {"symbol": "He", "name": "Helium", "options": ["Helium", "Hydrogen", "Hafnium", "Holmium"]},
        {"symbol": "Ca", "name": "Calcium", "options": ["Calcium", "Carbon", "Cadmium", "Californium"]},
    ]

    elements_medium = elements_easy + [
        {"symbol": "Cl", "name": "Chlorine", "options": ["Chlorine", "Calcium", "Carbon", "Copper"]},
        {"symbol": "K", "name": "Potassium", "options": ["Potassium", "Krypton", "Phosphorus", "Platinum"]},
        {"symbol": "Mg", "name": "Magnesium", "options": ["Magnesium", "Manganese", "Mercury", "Molybdenum"]},
        {"symbol": "Zn", "name": "Zinc", "options": ["Zinc", "Zirconium", "Xenon", "Yttrium"]},
        {"symbol": "Cu", "name": "Copper", "options": ["Copper", "Carbon", "Curium", "Cesium"]},
    ]

    elements_hard = elements_medium + [
        {"symbol": "P", "name": "Phosphorus", "options": ["Phosphorus", "Potassium", "Platinum", "Palladium"]},
        {"symbol": "S", "name": "Sulfur", "options": ["Sulfur", "Sodium", "Silicon", "Silver"]},
        {"symbol": "Al", "name": "Aluminum", "options": ["Aluminum", "Argon", "Arsenic", "Silver"]},
        {"symbol": "Ne", "name": "Neon", "options": ["Neon", "Nitrogen", "Nickel", "Nobelium"]},
        {"symbol": "Li", "name": "Lithium", "options": ["Lithium", "Lead", "Lanthanum", "Lutetium"]},
    ]

    if difficulty == 'easy':
        elements = elements_easy
    elif difficulty == 'medium':
        elements = elements_medium
    else:
        elements = elements_hard

    random.shuffle(elements)
    questions = []
    for elem in elements[:20]:
        options_copy = elem["options"][:]
        random.shuffle(options_copy)
        questions.append({
            "question": f"What element is '{elem['symbol']}'?",
            "answer": elem["name"],
            "options": options_copy,
            "type": "element"
        })

    return questions


def generate_spelling_sprint(difficulty='medium'):
    """Spell words correctly as fast as you can"""

    word_data = {
        "easy": [
            {"word": "apple", "wrong": ["aple", "appel", "appal"]},
            {"word": "beach", "wrong": ["beech", "beatch", "bech"]},
            {"word": "friend", "wrong": ["freind", "frend", "friand"]},
            {"word": "school", "wrong": ["skool", "shcool", "scool"]},
            {"word": "happy", "wrong": ["hapy", "happie", "hapi"]},
            {"word": "pizza", "wrong": ["piza", "pitsa", "peezza"]},
            {"word": "yellow", "wrong": ["yelow", "yello", "yellaw"]},
            {"word": "elephant", "wrong": ["elefant", "elephent", "elaphant"]},
            {"word": "birthday", "wrong": ["brithday", "birthdy", "berthday"]},
            {"word": "library", "wrong": ["libary", "liberry", "librery"]},
            {"word": "garden", "wrong": ["gardan", "gardun", "garding"]},
            {"word": "rainbow", "wrong": ["rainbo", "rainebow", "ranbow"]},
            {"word": "treasure", "wrong": ["tresure", "treasur", "treazure"]},
            {"word": "balloon", "wrong": ["baloon", "ballon", "beloon"]},
            {"word": "mountain", "wrong": ["mountin", "mountian", "moutain"]},
            {"word": "ocean", "wrong": ["ocian", "osean", "occean"]},
            {"word": "dragon", "wrong": ["dragan", "dragun", "dragan"]},
            {"word": "castle", "wrong": ["casel", "castel", "cassle"]},
            {"word": "rocket", "wrong": ["roket", "rockit", "rokket"]},
            {"word": "adventure", "wrong": ["adventur", "adventchur", "advenchure"]},
        ],
        "medium": [
            {"word": "beautiful", "wrong": ["beautifull", "beutiful", "beautyful"]},
            {"word": "necessary", "wrong": ["neccessary", "necessery", "neccesary"]},
            {"word": "receive", "wrong": ["recieve", "recive", "receeve"]},
            {"word": "separate", "wrong": ["seperate", "separete", "seprate"]},
            {"word": "definitely", "wrong": ["definately", "definitly", "definetly"]},
            {"word": "tomorrow", "wrong": ["tommorow", "tommorrow", "tomorow"]},
            {"word": "although", "wrong": ["altough", "althought", "althow"]},
            {"word": "government", "wrong": ["goverment", "governmant", "govenment"]},
            {"word": "experience", "wrong": ["experiance", "experiance", "exprience"]},
            {"word": "restaurant", "wrong": ["restarant", "resturant", "resteraunt"]},
            {"word": "extraordinary", "wrong": ["extrordinary", "extraordinery", "extraodinary"]},
            {"word": "consciousness", "wrong": ["consciousnes", "conciousness", "consciosness"]},
            {"word": "opportunity", "wrong": ["oportunity", "oppurtunity", "opportunety"]},
            {"word": "temperature", "wrong": ["temperture", "temprature", "temperatue"]},
            {"word": "abbreviate", "wrong": ["abreviate", "abbrevate", "abbrieviate"]},
            {"word": "acknowledgment", "wrong": ["acknowledgement", "acknowlegment", "acknoledgment"]},
            {"word": "acquaintance", "wrong": ["aquaintance", "acquantance", "acquaintence"]},
            {"word": "achievement", "wrong": ["acheivment", "achievment", "achievemant"]},
            {"word": "desperate", "wrong": ["desparate", "desprate", "desperet"]},
            {"word": "category", "wrong": ["catagory", "categery", "catergory"]},
        ],
        "hard": [
            {"word": "accommodate", "wrong": ["accomodate", "acommodate", "acomodate"]},
            {"word": "occurrence", "wrong": ["occurence", "occurance", "occurrance"]},
            {"word": "occasionally", "wrong": ["ocasionally", "occassionally", "occasionaly"]},
            {"word": "recommend", "wrong": ["recomend", "reccommend", "recommand"]},
            {"word": "embarrass", "wrong": ["embarass", "embarras", "embaress"]},
            {"word": "conscience", "wrong": ["concience", "conscence", "conciense"]},
            {"word": "rhythm", "wrong": ["rythm", "rhythem", "rithm"]},
            {"word": "privilege", "wrong": ["priviledge", "privilage", "privlege"]},
            {"word": "maintenance", "wrong": ["maintainance", "maintenence", "maintanance"]},
            {"word": "bureaucracy", "wrong": ["buracracy", "bureaucrasy", "beaucracy"]},
            {"word": "entrepreneurship", "wrong": ["entrepeneurship", "entreprenurship", "enterpreneurship"]},
            {"word": "pharmaceutical", "wrong": ["pharmeceutical", "pharmacutical", "pharmaseutical"]},
            {"word": "psychological", "wrong": ["psycological", "phychological", "psycholigical"]},
            {"word": "sophisticated", "wrong": ["sophisicated", "sofisticated", "sophistacated"]},
            {"word": "conscientious", "wrong": ["conciencious", "conscienscious", "conscientous"]},
            {"word": "dilemma", "wrong": ["dilemna", "dilema", "dillemma"]},
            {"word": "fluorescent", "wrong": ["florescent", "flourescent", "florescent"]},
            {"word": "guarantee", "wrong": ["garantee", "guarentee", "garentee"]},
            {"word": "harassment", "wrong": ["harrasment", "harasment", "harrassment"]},
            {"word": "liaison", "wrong": ["liason", "liaision", "liasion"]},
        ]
    }

    word_set = word_data.get(difficulty, word_data["medium"])
    random.shuffle(word_set)

    questions = []
    for item in word_set[:20]:
        word = item["word"]
        wrong_options = item["wrong"]
        options = [word] + wrong_options
        random.shuffle(options)

        questions.append({
            "question": f"Spell correctly: {word.upper()}",
            "answer": word,
            "options": options,
            "type": "spelling"
        })

    return questions


def generate_grammar_quest(difficulty='medium'):
    """Fix grammatical errors in record time"""

    base_questions = [
        {"wrong": "Their going to the store", "correct": "They're going to the store"},
        {"wrong": "The cat is sleeping in it's bed", "correct": "The cat is sleeping in its bed"},
        {"wrong": "Me and him went to school", "correct": "He and I went to school"},
        {"wrong": "She don't like apples", "correct": "She doesn't like apples"},
        {"wrong": "I seen that movie before", "correct": "I have seen that movie before"},
        {"wrong": "Your the best!", "correct": "You're the best!"},
        {"wrong": "Between you and I", "correct": "Between you and me"},
        {"wrong": "I could of done better", "correct": "I could have done better"},
        {"wrong": "There house is big", "correct": "Their house is big"},
        {"wrong": "Its a beautiful day", "correct": "It's a beautiful day"},
        {"wrong": "He don't care", "correct": "He doesn't care"},
        {"wrong": "Me and my friend", "correct": "My friend and I"},
        {"wrong": "I should of known", "correct": "I should have known"},
        {"wrong": "Your awesome", "correct": "You're awesome"},
        {"wrong": "We was going home", "correct": "We were going home"},
        {"wrong": "The dog wagged it's tail", "correct": "The dog wagged its tail"},
        {"wrong": "Let's keep this between you and I", "correct": "Let's keep this between you and me"},
        {"wrong": "Me and her are friends", "correct": "She and I are friends"},
        {"wrong": "I could care less", "correct": "I couldn't care less"},
        {"wrong": "Who's book is this?", "correct": "Whose book is this?"},
    ]

    questions = []
    random.shuffle(base_questions)

    for item in base_questions[:20]:
        other_wrongs = [q["wrong"] for q in base_questions if q["wrong"] != item["wrong"]]
        random.shuffle(other_wrongs)

        options = [item["correct"], item["wrong"]] + other_wrongs[:2]
        random.shuffle(options)

        questions.append({
            "question": f"Fix the error: '{item['wrong']}'",
            "answer": item["correct"],
            "options": options,
            "type": "grammar"
        })

    random.shuffle(questions)
    return questions[:20]


def generate_history_timeline(difficulty='medium'):
    """Put historical events in the correct order"""

    events = [
        {"event": "Declaration of Independence", "year": 1776},
        {"event": "Civil War Begins", "year": 1861},
        {"event": "World War I Starts", "year": 1914},
        {"event": "Great Depression", "year": 1929},
        {"event": "World War II Ends", "year": 1945},
        {"event": "Moon Landing", "year": 1969},
        {"event": "Fall of Berlin Wall", "year": 1989},
        {"event": "American Revolution", "year": 1775},
        {"event": "Constitution Signed", "year": 1787},
        {"event": "Printing Press Invented", "year": 1440},
        {"event": "Columbus Discovers America", "year": 1492},
        {"event": "Civil Rights Act", "year": 1964},
    ]

    questions = []
    seen_questions = set()
    max_attempts = 200

    attempts = 0
    while len(questions) < 20 and attempts < max_attempts:
        attempts += 1
        selected = random.sample(events, 2)
        correct_first = min(selected, key=lambda x: x['year'])

        question = {
            "question": f"Which event happened FIRST?",
            "answer": correct_first["event"],
            "options": [selected[0]["event"], selected[1]["event"]],
            "type": "timeline"
        }

        if not is_duplicate_question(question, seen_questions):
            questions.append(question)

    return questions


def generate_geography_dash(difficulty='medium'):
    """Identify countries, capitals, and landmarks"""

    questions = [
        {"question": "What is the capital of France?", "answer": "Paris", "options": ["Paris", "London", "Berlin", "Rome"]},
        {"question": "Which country has the Great Wall?", "answer": "China", "options": ["China", "Japan", "Korea", "Mongolia"]},
        {"question": "What is the largest ocean?", "answer": "Pacific", "options": ["Pacific", "Atlantic", "Indian", "Arctic"]},
        {"question": "Where are the pyramids of Giza?", "answer": "Egypt", "options": ["Egypt", "Mexico", "Peru", "Iraq"]},
        {"question": "What is the capital of Japan?", "answer": "Tokyo", "options": ["Tokyo", "Beijing", "Seoul", "Bangkok"]},
        {"question": "Which continent is Australia in?", "answer": "Oceania", "options": ["Oceania", "Asia", "Africa", "Antarctica"]},
        {"question": "What is the longest river?", "answer": "Nile", "options": ["Nile", "Amazon", "Mississippi", "Yangtze"]},
        {"question": "Where is the Eiffel Tower?", "answer": "Paris", "options": ["Paris", "London", "Rome", "Madrid"]},
        {"question": "What is the capital of Italy?", "answer": "Rome", "options": ["Rome", "Milan", "Venice", "Florence"]},
        {"question": "Which ocean is between US and Europe?", "answer": "Atlantic", "options": ["Atlantic", "Pacific", "Indian", "Arctic"]},
        {"question": "What is the capital of Spain?", "answer": "Madrid", "options": ["Madrid", "Barcelona", "Seville", "Valencia"]},
        {"question": "Where is Mount Everest?", "answer": "Nepal", "options": ["Nepal", "India", "China", "Tibet"]},
        {"question": "What is the capital of Canada?", "answer": "Ottawa", "options": ["Ottawa", "Toronto", "Montreal", "Vancouver"]},
        {"question": "Which country is shaped like a boot?", "answer": "Italy", "options": ["Italy", "Greece", "Spain", "Portugal"]},
        {"question": "What is the smallest continent?", "answer": "Australia", "options": ["Australia", "Europe", "Antarctica", "South America"]},
        {"question": "Where is the Statue of Liberty?", "answer": "New York", "options": ["New York", "Washington DC", "Boston", "Philadelphia"]},
        {"question": "What is the capital of Germany?", "answer": "Berlin", "options": ["Berlin", "Munich", "Frankfurt", "Hamburg"]},
        {"question": "Which desert is the largest?", "answer": "Sahara", "options": ["Sahara", "Gobi", "Arabian", "Kalahari"]},
        {"question": "What is the capital of Brazil?", "answer": "Brasilia", "options": ["Brasilia", "Rio de Janeiro", "Sao Paulo", "Salvador"]},
        {"question": "Where is the Taj Mahal?", "answer": "India", "options": ["India", "Pakistan", "Bangladesh", "Nepal"]},
    ]

    random.shuffle(questions)

    # Shuffle options for each question to prevent predictable patterns
    shuffled_questions = [shuffle_question_options(q) for q in questions[:20]]
    return shuffled_questions


# ============================================================
# NEW GAME 4: BIBLE TRIVIA
# ============================================================

BIBLE_QUESTIONS = {
    "easy": [
        {"question": "Who built the ark?", "answer": "Noah", "options": ["Noah", "Moses", "Abraham", "David"]},
        {"question": "Who was swallowed by a big fish?", "answer": "Jonah", "options": ["Jonah", "Peter", "Paul", "John"]},
        {"question": "Who defeated Goliath?", "answer": "David", "options": ["David", "Saul", "Samuel", "Solomon"]},
        {"question": "Who led the Israelites out of Egypt?", "answer": "Moses", "options": ["Moses", "Aaron", "Joshua", "Abraham"]},
        {"question": "Who was Jesus' mother?", "answer": "Mary", "options": ["Mary", "Martha", "Ruth", "Sarah"]},
        {"question": "How many disciples did Jesus have?", "answer": "12", "options": ["12", "10", "7", "40"]},
        {"question": "Who betrayed Jesus?", "answer": "Judas", "options": ["Judas", "Peter", "John", "Thomas"]},
        {"question": "What is the first book of the Bible?", "answer": "Genesis", "options": ["Genesis", "Exodus", "Matthew", "Psalms"]},
        {"question": "Who was the first man?", "answer": "Adam", "options": ["Adam", "Noah", "Abraham", "Moses"]},
        {"question": "Who was the first woman?", "answer": "Eve", "options": ["Eve", "Sarah", "Mary", "Ruth"]},
        {"question": "How many days did God create the world?", "answer": "6", "options": ["6", "7", "5", "8"]},
        {"question": "What did God create on the first day?", "answer": "Light", "options": ["Light", "Land", "Animals", "Humans"]},
        {"question": "Where was Jesus born?", "answer": "Bethlehem", "options": ["Bethlehem", "Jerusalem", "Nazareth", "Egypt"]},
        {"question": "What is the last book of the Bible?", "answer": "Revelation", "options": ["Revelation", "Acts", "Romans", "Jude"]},
        {"question": "Who walked on water with Jesus?", "answer": "Peter", "options": ["Peter", "John", "James", "Andrew"]},
        {"question": "How many days was Jesus in the tomb?", "answer": "3", "options": ["3", "7", "40", "1"]},
        {"question": "What did Jesus turn water into?", "answer": "Wine", "options": ["Wine", "Milk", "Oil", "Honey"]},
        {"question": "Who denied Jesus three times?", "answer": "Peter", "options": ["Peter", "Judas", "John", "Thomas"]},
        {"question": "What animal spoke to Balaam?", "answer": "Donkey", "options": ["Donkey", "Snake", "Camel", "Horse"]},
        {"question": "Who was the strongest man in the Bible?", "answer": "Samson", "options": ["Samson", "David", "Goliath", "Moses"]},
    ],
    "medium": [
        {"question": "Who wrote most of the Psalms?", "answer": "David", "options": ["David", "Solomon", "Moses", "Asaph"]},
        {"question": "What was Paul's name before conversion?", "answer": "Saul", "options": ["Saul", "Samuel", "Simon", "Stephen"]},
        {"question": "Who interpreted dreams for Pharaoh?", "answer": "Joseph", "options": ["Joseph", "Daniel", "Jacob", "Moses"]},
        {"question": "How many plagues did God send on Egypt?", "answer": "10", "options": ["10", "7", "12", "40"]},
        {"question": "What was Jesus' first miracle?", "answer": "Water to wine", "options": ["Water to wine", "Healing blind", "Feeding 5000", "Walking on water"]},
        {"question": "Who was the wisest king?", "answer": "Solomon", "options": ["Solomon", "David", "Saul", "Hezekiah"]},
        {"question": "What was the forbidden fruit likely?", "answer": "Unknown", "options": ["Unknown", "Apple", "Fig", "Grape"]},
        {"question": "Who replaced Judas as a disciple?", "answer": "Matthias", "options": ["Matthias", "Paul", "Mark", "Barnabas"]},
        {"question": "How many books are in the New Testament?", "answer": "27", "options": ["27", "39", "66", "12"]},
        {"question": "Who was thrown into a lion's den?", "answer": "Daniel", "options": ["Daniel", "David", "Jonah", "Joseph"]},
        {"question": "What is the shortest verse in the Bible?", "answer": "Jesus wept", "options": ["Jesus wept", "God is love", "Pray always", "Rejoice"]},
        {"question": "Who was the oldest man in the Bible?", "answer": "Methuselah", "options": ["Methuselah", "Noah", "Abraham", "Adam"]},
        {"question": "How many years did the Israelites wander?", "answer": "40", "options": ["40", "7", "12", "70"]},
        {"question": "Who was the first king of Israel?", "answer": "Saul", "options": ["Saul", "David", "Solomon", "Samuel"]},
        {"question": "What did Jacob give Joseph?", "answer": "Coat of many colors", "options": ["Coat of many colors", "Silver", "Sheep", "Land"]},
        {"question": "Who baptized Jesus?", "answer": "John the Baptist", "options": ["John the Baptist", "Peter", "James", "Paul"]},
        {"question": "Where did Jesus grow up?", "answer": "Nazareth", "options": ["Nazareth", "Bethlehem", "Jerusalem", "Capernaum"]},
        {"question": "Who was the brother of Moses?", "answer": "Aaron", "options": ["Aaron", "Joshua", "Caleb", "Hur"]},
        {"question": "What are the first four books of NT called?", "answer": "Gospels", "options": ["Gospels", "Epistles", "Acts", "Pauline Letters"]},
        {"question": "Who was swallowed by the earth?", "answer": "Korah", "options": ["Korah", "Achan", "Ananias", "Judas"]},
    ],
    "hard": [
        {"question": "Who was the high priest when Jesus was tried?", "answer": "Caiaphas", "options": ["Caiaphas", "Annas", "Eli", "Zadok"]},
        {"question": "What was Paul's occupation?", "answer": "Tentmaker", "options": ["Tentmaker", "Fisherman", "Carpenter", "Tax collector"]},
        {"question": "How many chapters are in the book of Psalms?", "answer": "150", "options": ["150", "100", "119", "180"]},
        {"question": "Who was the father of John the Baptist?", "answer": "Zechariah", "options": ["Zechariah", "Zacharias", "Zacchaeus", "Zebedee"]},
        {"question": "What is the longest chapter in the Bible?", "answer": "Psalm 119", "options": ["Psalm 119", "Isaiah 53", "John 3", "Romans 8"]},
        {"question": "Who succeeded Moses as leader?", "answer": "Joshua", "options": ["Joshua", "Caleb", "Aaron", "Eleazar"]},
        {"question": "What language was most of OT written in?", "answer": "Hebrew", "options": ["Hebrew", "Aramaic", "Greek", "Latin"]},
        {"question": "Who wrote the book of Revelation?", "answer": "John", "options": ["John", "Paul", "Peter", "Luke"]},
        {"question": "How many books did Paul write?", "answer": "13", "options": ["13", "14", "12", "10"]},
        {"question": "Who was the mother of Samuel?", "answer": "Hannah", "options": ["Hannah", "Sarah", "Rachel", "Leah"]},
        {"question": "What does 'Immanuel' mean?", "answer": "God with us", "options": ["God with us", "Savior", "Prince of Peace", "Messiah"]},
        {"question": "Who was the Roman governor at Jesus' trial?", "answer": "Pontius Pilate", "options": ["Pontius Pilate", "Herod", "Caesar", "Felix"]},
        {"question": "What is the 'love chapter'?", "answer": "1 Corinthians 13", "options": ["1 Corinthians 13", "John 3", "Romans 8", "Ephesians 5"]},
        {"question": "Who was David's best friend?", "answer": "Jonathan", "options": ["Jonathan", "Joab", "Nathan", "Solomon"]},
        {"question": "How many pieces of silver for Jesus?", "answer": "30", "options": ["30", "40", "20", "100"]},
        {"question": "Who was the first martyr?", "answer": "Stephen", "options": ["Stephen", "James", "Peter", "Paul"]},
        {"question": "What is the longest book in the Bible?", "answer": "Psalms", "options": ["Psalms", "Isaiah", "Jeremiah", "Genesis"]},
        {"question": "Who was king when Jesus was born?", "answer": "Herod the Great", "options": ["Herod the Great", "Caesar Augustus", "Herod Antipas", "Pilate"]},
        {"question": "What does 'Gospel' mean?", "answer": "Good News", "options": ["Good News", "God's Word", "Holy Book", "Sacred Text"]},
        {"question": "Who was the Queen who visited Solomon?", "answer": "Queen of Sheba", "options": ["Queen of Sheba", "Esther", "Jezebel", "Vashti"]},
    ]
}

def generate_bible_trivia(difficulty='medium'):
    """Test your knowledge of Bible stories and verses"""
    questions = BIBLE_QUESTIONS.get(difficulty, BIBLE_QUESTIONS["medium"]).copy()
    random.shuffle(questions)

    # Shuffle options for each question to prevent predictable patterns
    shuffled_questions = [shuffle_question_options(q) for q in questions[:20]]
    return shuffled_questions


# ============================================================
# NEW GEOGRAPHY GAMES (MapVerse)
# ============================================================

def generate_country_spotter(difficulty='medium'):
    """Identify countries by their outline/shape"""
    # Country data with descriptions of their shapes
    countries_by_difficulty = {
        'easy': [
            {"country": "Italy", "shape_hint": "Boot-shaped", "answer": "Italy", "options": ["Italy", "Greece", "Spain", "Portugal"]},
            {"country": "United Kingdom", "shape_hint": "Island nation west of Europe", "answer": "United Kingdom", "options": ["United Kingdom", "Ireland", "Iceland", "Denmark"]},
            {"country": "Japan", "shape_hint": "Crescent-shaped island chain", "answer": "Japan", "options": ["Japan", "Philippines", "Indonesia", "Taiwan"]},
            {"country": "Australia", "shape_hint": "Large island continent", "answer": "Australia", "options": ["Australia", "Greenland", "Madagascar", "New Zealand"]},
            {"country": "Chile", "shape_hint": "Long, narrow country along coast", "answer": "Chile", "options": ["Chile", "Argentina", "Peru", "Colombia"]},
        ],
        'medium': [
            {"country": "Norway", "shape_hint": "Scandinavian with many fjords", "answer": "Norway", "options": ["Norway", "Sweden", "Finland", "Denmark"]},
            {"country": "Thailand", "shape_hint": "Southeast Asian, elephant-head shaped", "answer": "Thailand", "options": ["Thailand", "Vietnam", "Cambodia", "Myanmar"]},
            {"country": "Croatia", "shape_hint": "Crescent along Adriatic Sea", "answer": "Croatia", "options": ["Croatia", "Slovenia", "Bosnia", "Serbia"]},
            {"country": "Somalia", "shape_hint": "Horn of Africa", "answer": "Somalia", "options": ["Somalia", "Ethiopia", "Kenya", "Eritrea"]},
            {"country": "Panama", "shape_hint": "S-shaped connecting continents", "answer": "Panama", "options": ["Panama", "Costa Rica", "Nicaragua", "Honduras"]},
        ],
        'hard': [
            {"country": "Lesotho", "shape_hint": "Completely surrounded by South Africa", "answer": "Lesotho", "options": ["Lesotho", "Swaziland", "Botswana", "Zimbabwe"]},
            {"country": "Moldova", "shape_hint": "Between Romania and Ukraine", "answer": "Moldova", "options": ["Moldova", "Belarus", "Latvia", "Estonia"]},
            {"country": "Bhutan", "shape_hint": "Himalayan kingdom between giants", "answer": "Bhutan", "options": ["Bhutan", "Nepal", "Laos", "Cambodia"]},
            {"country": "Burundi", "shape_hint": "Small African Great Lakes country", "answer": "Burundi", "options": ["Burundi", "Rwanda", "Uganda", "Malawi"]},
            {"country": "Timor-Leste", "shape_hint": "Half of an island in Southeast Asia", "answer": "Timor-Leste", "options": ["Timor-Leste", "Brunei", "Papua New Guinea", "Solomon Islands"]},
        ]
    }

    questions = countries_by_difficulty.get(difficulty, countries_by_difficulty["medium"]).copy()
    random.shuffle(questions)

    # Format as standard questions
    formatted = []
    for q in questions:
        formatted.append({
            "question": f"Which country is {q['shape_hint']}?",
            "answer": q["answer"],
            "options": q["options"]
        })

    # Shuffle options for each question to prevent predictable patterns
    shuffled_questions = [shuffle_question_options(q) for q in formatted[:15]]
    return shuffled_questions


def generate_capital_quest(difficulty='medium'):
    """Match countries to their capitals"""
    capitals_by_difficulty = {
        'easy': [
            {"question": "What is the capital of France?", "answer": "Paris", "options": ["Paris", "London", "Rome", "Berlin"]},
            {"question": "What is the capital of Japan?", "answer": "Tokyo", "options": ["Tokyo", "Seoul", "Beijing", "Bangkok"]},
            {"question": "What is the capital of Canada?", "answer": "Ottawa", "options": ["Ottawa", "Toronto", "Montreal", "Vancouver"]},
            {"question": "What is the capital of Egypt?", "answer": "Cairo", "options": ["Cairo", "Alexandria", "Giza", "Luxor"]},
            {"question": "What is the capital of Australia?", "answer": "Canberra", "options": ["Canberra", "Sydney", "Melbourne", "Brisbane"]},
            {"question": "What is the capital of Brazil?", "answer": "Brasília", "options": ["Brasília", "Rio de Janeiro", "São Paulo", "Salvador"]},
            {"question": "What is the capital of India?", "answer": "New Delhi", "options": ["New Delhi", "Mumbai", "Bangalore", "Kolkata"]},
            {"question": "What is the capital of Germany?", "answer": "Berlin", "options": ["Berlin", "Munich", "Hamburg", "Frankfurt"]},
            {"question": "What is the capital of Mexico?", "answer": "Mexico City", "options": ["Mexico City", "Guadalajara", "Monterrey", "Cancun"]},
            {"question": "What is the capital of United Kingdom?", "answer": "London", "options": ["London", "Manchester", "Edinburgh", "Birmingham"]},
        ],
        'medium': [
            {"question": "What is the capital of Switzerland?", "answer": "Bern", "options": ["Bern", "Zurich", "Geneva", "Basel"]},
            {"question": "What is the capital of Vietnam?", "answer": "Hanoi", "options": ["Hanoi", "Ho Chi Minh City", "Da Nang", "Hue"]},
            {"question": "What is the capital of Morocco?", "answer": "Rabat", "options": ["Rabat", "Casablanca", "Marrakech", "Fez"]},
            {"question": "What is the capital of Pakistan?", "answer": "Islamabad", "options": ["Islamabad", "Karachi", "Lahore", "Rawalpindi"]},
            {"question": "What is the capital of New Zealand?", "answer": "Wellington", "options": ["Wellington", "Auckland", "Christchurch", "Hamilton"]},
            {"question": "What is the capital of Nigeria?", "answer": "Abuja", "options": ["Abuja", "Lagos", "Kano", "Ibadan"]},
            {"question": "What is the capital of Peru?", "answer": "Lima", "options": ["Lima", "Cusco", "Arequipa", "Trujillo"]},
            {"question": "What is the capital of South Africa?", "answer": "Pretoria", "options": ["Pretoria", "Cape Town", "Johannesburg", "Durban"]},
        ],
        'hard': [
            {"question": "What is the capital of Kazakhstan?", "answer": "Astana", "options": ["Astana", "Almaty", "Shymkent", "Karaganda"]},
            {"question": "What is the capital of Myanmar?", "answer": "Naypyidaw", "options": ["Naypyidaw", "Yangon", "Mandalay", "Bagan"]},
            {"question": "What is the capital of Côte d'Ivoire?", "answer": "Yamoussoukro", "options": ["Yamoussoukro", "Abidjan", "Bouaké", "Daloa"]},
            {"question": "What is the capital of Bhutan?", "answer": "Thimphu", "options": ["Thimphu", "Paro", "Punakha", "Phuentsholing"]},
            {"question": "What is the capital of Turkmenistan?", "answer": "Ashgabat", "options": ["Ashgabat", "Turkmenabat", "Dashoguz", "Mary"]},
            {"question": "What is the capital of Palau?", "answer": "Ngerulmud", "options": ["Ngerulmud", "Koror", "Melekeok", "Airai"]},
        ]
    }

    questions = capitals_by_difficulty.get(difficulty, capitals_by_difficulty["medium"]).copy()
    random.shuffle(questions)

    # Shuffle options for each question to prevent predictable patterns
    shuffled_questions = [shuffle_question_options(q) for q in questions[:20]]
    return shuffled_questions


def generate_flag_frenzy(difficulty='medium'):
    """Identify countries by their flags"""
    flags_by_difficulty = {
        'easy': [
            {"question": "Which country has a red maple leaf on its flag?", "answer": "Canada", "options": ["Canada", "USA", "Mexico", "Australia"]},
            {"question": "Which country has a blue, white, and red tricolor with vertical stripes?", "answer": "France", "options": ["France", "Netherlands", "Russia", "USA"]},
            {"question": "Which country has a red circle on a white background?", "answer": "Japan", "options": ["Japan", "Bangladesh", "Palau", "South Korea"]},
            {"question": "Which country has 50 stars and 13 stripes?", "answer": "USA", "options": ["USA", "Liberia", "Malaysia", "Chile"]},
            {"question": "Which country has a Union Jack in the corner and stars?", "answer": "Australia", "options": ["Australia", "New Zealand", "Fiji", "Tuvalu"]},
        ],
        'medium': [
            {"question": "Which country has a green cedar tree in the center?", "answer": "Lebanon", "options": ["Lebanon", "Cyprus", "Jordan", "Syria"]},
            {"question": "Which country has a dragon on its flag?", "answer": "Bhutan", "options": ["Bhutan", "Wales", "China", "Mongolia"]},
            {"question": "Which Nordic country has a white cross on blue?", "answer": "Finland", "options": ["Finland", "Sweden", "Norway", "Iceland"]},
            {"question": "Which country has a sun with 32 rays?", "answer": "Uruguay", "options": ["Uruguay", "Argentina", "Paraguay", "Bolivia"]},
        ],
        'hard': [
            {"question": "Which country has the only non-rectangular flag?", "answer": "Nepal", "options": ["Nepal", "Bhutan", "Vatican City", "Switzerland"]},
            {"question": "Which country has a machete and cog wheel?", "answer": "Angola", "options": ["Angola", "Mozambique", "Congo", "Zambia"]},
            {"question": "Which country has a two-headed eagle?", "answer": "Albania", "options": ["Albania", "Serbia", "Montenegro", "Russia"]},
        ]
    }

    questions = flags_by_difficulty.get(difficulty, flags_by_difficulty["medium"]).copy()
    random.shuffle(questions)
    return questions[:15]


def generate_landmark_locator(difficulty='medium'):
    """Match famous landmarks to countries/cities"""
    landmarks_by_difficulty = {
        'easy': [
            {"question": "Where is the Eiffel Tower located?", "answer": "Paris, France", "options": ["Paris, France", "London, UK", "Rome, Italy", "Berlin, Germany"]},
            {"question": "Where is the Statue of Liberty?", "answer": "New York, USA", "options": ["New York, USA", "Philadelphia, USA", "Boston, USA", "Washington DC, USA"]},
            {"question": "Where are the Pyramids of Giza?", "answer": "Cairo, Egypt", "options": ["Cairo, Egypt", "Alexandria, Egypt", "Luxor, Egypt", "Athens, Greece"]},
            {"question": "Where is the Taj Mahal?", "answer": "Agra, India", "options": ["Agra, India", "Delhi, India", "Mumbai, India", "Jaipur, India"]},
            {"question": "Where is Big Ben?", "answer": "London, UK", "options": ["London, UK", "Edinburgh, UK", "Dublin, Ireland", "Paris, France"]},
        ],
        'medium': [
            {"question": "Where is Machu Picchu?", "answer": "Peru", "options": ["Peru", "Bolivia", "Ecuador", "Colombia"]},
            {"question": "Where is the Sagrada Familia?", "answer": "Barcelona, Spain", "options": ["Barcelona, Spain", "Madrid, Spain", "Seville, Spain", "Valencia, Spain"]},
            {"question": "Where is Christ the Redeemer statue?", "answer": "Rio de Janeiro, Brazil", "options": ["Rio de Janeiro, Brazil", "São Paulo, Brazil", "Buenos Aires, Argentina", "Santiago, Chile"]},
            {"question": "Where is Angkor Wat?", "answer": "Cambodia", "options": ["Cambodia", "Thailand", "Vietnam", "Laos"]},
        ],
        'hard': [
            {"question": "Where is Petra (the rock city)?", "answer": "Jordan", "options": ["Jordan", "Israel", "Egypt", "Lebanon"]},
            {"question": "Where is Borobudur Temple?", "answer": "Indonesia", "options": ["Indonesia", "Thailand", "Myanmar", "Cambodia"]},
            {"question": "Where is the Blue Mosque?", "answer": "Istanbul, Turkey", "options": ["Istanbul, Turkey", "Ankara, Turkey", "Cairo, Egypt", "Tehran, Iran"]},
        ]
    }

    questions = landmarks_by_difficulty.get(difficulty, landmarks_by_difficulty["medium"]).copy()
    random.shuffle(questions)
    return questions[:15]


# ============================================================
# FINANCIAL LITERACY GAMES
# ============================================================

def generate_money_marathon(difficulty='medium'):
    """Make smart financial decisions under time pressure"""
    questions_by_difficulty = {
        'easy': [
            {"question": "You have $20. A toy costs $12. How much change will you get?", "answer": "$8", "options": ["$8", "$12", "$6", "$10"]},
            {"question": "What is 10% of $50?", "answer": "$5", "options": ["$5", "$10", "$15", "$20"]},
            {"question": "A shirt is $30 with a 20% discount. What's the sale price?", "answer": "$24", "options": ["$24", "$25", "$26", "$28"]},
            {"question": "You earn $10/hour. How much for 5 hours?", "answer": "$50", "options": ["$50", "$40", "$60", "$45"]},
            {"question": "Which is MORE money?", "answer": "4 quarters", "options": ["4 quarters", "9 dimes", "15 nickels", "50 pennies"]},
            {"question": "A pizza costs $18. Split between 3 people. How much each?", "answer": "$6", "options": ["$6", "$9", "$5", "$7"]},
            {"question": "Sales tax is 5%. What's tax on $100?", "answer": "$5", "options": ["$5", "$10", "$15", "$20"]},
        ],
        'medium': [
            {"question": "You buy 3 items: $12.50, $8.75, and $15.25. What's the total?", "answer": "$36.50", "options": ["$36.50", "$35.50", "$37.50", "$38.00"]},
            {"question": "A $500 bike is 30% off. What do you pay?", "answer": "$350", "options": ["$350", "$300", "$400", "$375"]},
            {"question": "You have a $100 budget. Items cost $45, $38, $22. Can you buy all?", "answer": "No, over budget", "options": ["No, over budget", "Yes, under budget", "Exactly $100", "Need $5 more"]},
            {"question": "Interest on $1000 at 5% for 1 year?", "answer": "$50", "options": ["$50", "$100", "$25", "$75"]},
            {"question": "Best deal: 5 pencils for $2 OR 12 pencils for $4?", "answer": "12 for $4", "options": ["12 for $4", "5 for $2", "Same price", "Can't tell"]},
        ],
        'hard': [
            {"question": "Investment of $5000 at 8% annual return for 2 years (simple interest)?", "answer": "$5800", "options": ["$5800", "$5400", "$6000", "$5600"]},
            {"question": "Monthly payment on $300 if you pay it off in 6 months (no interest)?", "answer": "$50", "options": ["$50", "$60", "$40", "$45"]},
            {"question": "Your budget is $2000/month. Rent=$800, Food=$400, Transport=$200. How much left?", "answer": "$600", "options": ["$600", "$500", "$700", "$400"]},
            {"question": "Stock bought at $25, sold at $35. What's the percent gain?", "answer": "40%", "options": ["40%", "25%", "50%", "35%"]},
        ]
    }

    questions = questions_by_difficulty.get(difficulty, questions_by_difficulty["medium"]).copy()
    random.shuffle(questions)

    # Shuffle options for each question to prevent predictable patterns
    shuffled_questions = [shuffle_question_options(q) for q in questions[:20]]
    return shuffled_questions


def generate_investment_simulator(difficulty='medium'):
    """Build your portfolio and understand investing"""
    questions_by_difficulty = {
        'easy': [
            {"question": "What is a stock?", "answer": "Ownership in a company", "options": ["Ownership in a company", "A loan to a company", "A savings account", "A type of bond"]},
            {"question": "What does diversification mean?", "answer": "Spreading money across investments", "options": ["Spreading money across investments", "Buying one stock only", "Selling everything", "Keeping cash"]},
            {"question": "Which is generally safer?", "answer": "Savings account", "options": ["Savings account", "Individual stocks", "Cryptocurrency", "Futures trading"]},
            {"question": "What is a dividend?", "answer": "Company profit paid to shareholders", "options": ["Company profit paid to shareholders", "Stock price increase", "Investment fee", "Tax payment"]},
            {"question": "What's the benefit of starting to invest early?", "answer": "More time for compound growth", "options": ["More time for compound growth", "Lower taxes", "Guaranteed returns", "No risk"]},
        ],
        'medium': [
            {"question": "What is an index fund?", "answer": "Fund tracking a market index", "options": ["Fund tracking a market index", "Single company stock", "Real estate fund", "Bond only fund"]},
            {"question": "What is compound interest?", "answer": "Interest on interest", "options": ["Interest on interest", "One-time interest", "Monthly fees", "Tax penalty"]},
            {"question": "Which has higher potential returns and risk?", "answer": "Stocks", "options": ["Stocks", "Bonds", "Savings accounts", "CDs"]},
            {"question": "What is asset allocation?", "answer": "How you divide investments", "options": ["How you divide investments", "Buying stocks only", "Selling everything", "Day trading"]},
            {"question": "What's a 401(k)?", "answer": "Retirement investment account", "options": ["Retirement investment account", "Type of stock", "Savings account", "Credit card"]},
        ],
        'hard': [
            {"question": "What is a PE ratio?", "answer": "Price to Earnings ratio", "options": ["Price to Earnings ratio", "Profit Estimate ratio", "Public Exchange ratio", "Portfolio Equity ratio"]},
            {"question": "What is dollar-cost averaging?", "answer": "Investing same amount regularly", "options": ["Investing same amount regularly", "Buying low selling high", "One large investment", "Only buying dips"]},
            {"question": "What are capital gains?", "answer": "Profit from selling investments", "options": ["Profit from selling investments", "Dividend payments", "Interest earned", "Initial investment"]},
            {"question": "What is market volatility?", "answer": "Price fluctuation rate", "options": ["Price fluctuation rate", "Company bankruptcy", "High returns", "Low risk"]},
        ]
    }

    questions = questions_by_difficulty.get(difficulty, questions_by_difficulty["medium"]).copy()
    random.shuffle(questions)

    # Shuffle options for each question to prevent predictable patterns
    shuffled_questions = [shuffle_question_options(q) for q in questions[:20]]
    return shuffled_questions


# ============================================================
# CHARACTER EDUCATION GAMES (RespectRealm)
# ============================================================

def generate_etiquette_expert(difficulty='medium'):
    """Choose the polite and respectful response"""
    scenarios_by_difficulty = {
        'easy': [
            {"question": "Someone holds the door open for you. What should you say?", "answer": "Thank you", "options": ["Thank you", "Nothing", "You're welcome", "Excuse me"]},
            {"question": "You need to interrupt a conversation. What should you say?", "answer": "Excuse me", "options": ["Excuse me", "Hey!", "Listen!", "Move"]},
            {"question": "When should you say 'please'?", "answer": "When asking for something", "options": ["When asking for something", "When angry", "Never", "Only with strangers"]},
            {"question": "At dinner, when should you start eating?", "answer": "After everyone is served", "options": ["After everyone is served", "Immediately", "When you want", "Last"]},
            {"question": "You bump into someone. What do you say?", "answer": "I'm sorry/Excuse me", "options": ["I'm sorry/Excuse me", "Watch out", "Your fault", "Nothing"]},
            {"question": "Someone gives you a gift. What's the first thing to say?", "answer": "Thank you", "options": ["Thank you", "I don't like it", "How much was it?", "I have one"]},
        ],
        'medium': [
            {"question": "You're invited to dinner at 6pm. When should you arrive?", "answer": "5-10 minutes early or on time", "options": ["5-10 minutes early or on time", "30 minutes early", "30 minutes late", "Whenever you want"]},
            {"question": "At a restaurant, who should order first?", "answer": "Guests/older people first", "options": ["Guests/older people first", "Youngest first", "Whoever is hungriest", "Doesn't matter"]},
            {"question": "Someone's phone is ringing in a movie. They should:", "answer": "Silence it immediately", "options": ["Silence it immediately", "Answer quietly", "Let it ring", "Leave it"]},
            {"question": "You disagree with an adult. How should you express it?", "answer": "Respectfully state your view", "options": ["Respectfully state your view", "Argue loudly", "Say they're wrong", "Stay silent even if important"]},
            {"question": "Meeting someone new, what's appropriate?", "answer": "Handshake and eye contact", "options": ["Handshake and eye contact", "Hug immediately", "Wave from far away", "Look at phone"]},
        ],
        'hard': [
            {"question": "At a formal dinner, which fork do you use first?", "answer": "Outermost fork", "options": ["Outermost fork", "Biggest fork", "Smallest fork", "Doesn't matter"]},
            {"question": "Someone makes a mistake in public. The polite response is:", "answer": "Ignore it or help privately", "options": ["Ignore it or help privately", "Point it out loudly", "Laugh", "Tell everyone"]},
            {"question": "You receive a gift you don't like. You should:", "answer": "Thank them graciously anyway", "options": ["Thank them graciously anyway", "Say you don't like it", "Don't say anything", "Ask for receipt"]},
            {"question": "In a disagreement, you should:", "answer": "Listen first, then respond calmly", "options": ["Listen first, then respond calmly", "Interrupt to correct them", "Raise your voice", "Walk away immediately"]},
        ]
    }

    questions = scenarios_by_difficulty.get(difficulty, scenarios_by_difficulty["medium"]).copy()
    random.shuffle(questions)
    return questions[:15]


def generate_virtue_quest(difficulty='medium'):
    """Identify virtues and character traits in action"""
    scenarios_by_difficulty = {
        'easy': [
            {"question": "Sarah finds $20 and returns it to the owner. What virtue is this?", "answer": "Honesty", "options": ["Honesty", "Kindness", "Courage", "Patience"]},
            {"question": "Tom helps an elderly neighbor carry groceries. What is this?", "answer": "Kindness", "options": ["Kindness", "Justice", "Wisdom", "Faith"]},
            {"question": "Emma tells the truth even though she'll get in trouble. What is this?", "answer": "Honesty", "options": ["Honesty", "Foolishness", "Meanness", "Pride"]},
            {"question": "David waits his turn without complaining. What virtue?", "answer": "Patience", "options": ["Patience", "Laziness", "Fear", "Anger"]},
            {"question": "Maria stands up to a bully. What does this show?", "answer": "Courage", "options": ["Courage", "Anger", "Meanness", "Pride"]},
        ],
        'medium': [
            {"question": "John apologizes after making a mistake. This shows:", "answer": "Humility", "options": ["Humility", "Weakness", "Pride", "Fear"]},
            {"question": "Lisa resists cheating even when others do. This is:", "answer": "Integrity", "options": ["Integrity", "Foolishness", "Pride", "Weakness"]},
            {"question": "Mike forgives his friend who hurt him. This shows:", "answer": "Forgiveness/Mercy", "options": ["Forgiveness/Mercy", "Weakness", "Forgetfulness", "Fear"]},
            {"question": "Anna works hard even when no one is watching. This is:", "answer": "Diligence/Integrity", "options": ["Diligence/Integrity", "Showing off", "Wasting time", "Pride"]},
            {"question": "Bible verse: 'Love is patient, love is kind' describes:", "answer": "True love/Charity", "options": ["True love/Charity", "Weakness", "Foolishness", "Romance only"]},
        ],
        'hard': [
            {"question": "Joseph chose prison over sin (Genesis 39). This shows:", "answer": "Integrity/Purity", "options": ["Integrity/Purity", "Foolishness", "Fear", "Pride"]},
            {"question": "Daniel prayed publicly despite the law. This is:", "answer": "Faithfulness/Courage", "options": ["Faithfulness/Courage", "Rebellion", "Stupidity", "Showing off"]},
            {"question": "Opposite of humility is:", "answer": "Pride", "options": ["Pride", "Confidence", "Courage", "Honesty"]},
            {"question": "'Whatever is true, noble, right...' (Phil 4:8) teaches:", "answer": "Guard your thoughts", "options": ["Guard your thoughts", "Think positive only", "Ignore problems", "Be judgmental"]},
        ]
    }

    questions = scenarios_by_difficulty.get(difficulty, scenarios_by_difficulty["medium"]).copy()
    random.shuffle(questions)
    return questions[:15]


# ============================================================
# CRITICAL THINKING GAMES (TruthForge)
# ============================================================

def generate_logic_lock(difficulty='medium'):
    """Spot logical fallacies and test reasoning"""
    fallacies_by_difficulty = {
        'easy': [
            {"question": "'Everyone's doing it, so it must be okay.' What fallacy is this?", "answer": "Bandwagon/Appeal to popularity", "options": ["Bandwagon/Appeal to popularity", "Ad hominem", "Straw man", "False cause"]},
            {"question": "'You're wrong because you're a bad person.' What fallacy?", "answer": "Ad hominem", "options": ["Ad hominem", "Straw man", "Slippery slope", "Red herring"]},
            {"question": "'If we allow A, then Z will definitely happen!' What fallacy?", "answer": "Slippery slope", "options": ["Slippery slope", "False dilemma", "Straw man", "Circular reasoning"]},
            {"question": "'You either agree with me or you hate freedom.' What fallacy?", "answer": "False dilemma", "options": ["False dilemma", "Ad hominem", "Bandwagon", "Straw man"]},
            {"question": "'It happened after X, so X must have caused it.' What fallacy?", "answer": "False cause", "options": ["False cause", "Straw man", "Ad hominem", "Circular reasoning"]},
        ],
        'medium': [
            {"question": "'You can't prove it's NOT true, so it must be true.' What fallacy?", "answer": "Appeal to ignorance", "options": ["Appeal to ignorance", "Burden of proof", "Straw man", "Red herring"]},
            {"question": "'The Bible is true because the Bible says it's true.' What fallacy?", "answer": "Circular reasoning", "options": ["Circular reasoning", "Valid argument", "Straw man", "False dilemma"]},
            {"question": "'You don't have a PhD, so your argument is wrong.' What fallacy?", "answer": "Appeal to authority/credentials", "options": ["Appeal to authority/credentials", "Ad hominem", "Valid reasoning", "Straw man"]},
            {"question": "'Let's talk about something else instead.' What fallacy?", "answer": "Red herring", "options": ["Red herring", "Straw man", "Ad hominem", "False dilemma"]},
        ],
        'hard': [
            {"question": "'No true Christian would ever doubt.' What fallacy?", "answer": "No true Scotsman", "options": ["No true Scotsman", "Appeal to purity", "Straw man", "Ad hominem"]},
            {"question": "'Science can't explain X, therefore God.' What fallacy?", "answer": "God of the gaps", "options": ["God of the gaps", "Valid argument", "Appeal to ignorance", "False cause"]},
            {"question": "'I'm a good person, so God owes me.' What fallacy?", "answer": "Works righteousness", "options": ["Works righteousness", "Valid theology", "Humility", "Faith"]},
        ]
    }

    questions = fallacies_by_difficulty.get(difficulty, fallacies_by_difficulty["medium"]).copy()
    random.shuffle(questions)
    return questions[:15]


def generate_worldview_warriors(difficulty='medium'):
    """Compare worldviews and defend biblical truth"""
    questions_by_difficulty = {
        'easy': [
            {"question": "What is a worldview?", "answer": "How you see/interpret reality", "options": ["How you see/interpret reality", "Your favorite view", "Just opinions", "Scientific facts"]},
            {"question": "Christianity teaches that truth is:", "answer": "Absolute and from God", "options": ["Absolute and from God", "Relative to each person", "Unknowable", "Created by society"]},
            {"question": "The Bible says all humans have:", "answer": "Value because made in God's image", "options": ["Value because made in God's image", "Value only if successful", "No inherent value", "Value from society"]},
            {"question": "Who determines right and wrong in Christianity?", "answer": "God", "options": ["God", "Each person decides", "Society decides", "No one, it's relative"]},
            {"question": "The Bible's view of the universe's origin is:", "answer": "Created by God", "options": ["Created by God", "Random chance", "Always existed", "Unknown"]},
        ],
        'medium': [
            {"question": "Relativism claims that:", "answer": "Truth is different for everyone", "options": ["Truth is different for everyone", "Truth is absolute", "Truth comes from God", "Truth is knowable"]},
            {"question": "Secular humanism places ultimate authority in:", "answer": "Human reason", "options": ["Human reason", "God's revelation", "Nature", "Tradition"]},
            {"question": "The problem with 'your truth vs my truth' is:", "answer": "Contradictions can't both be true", "options": ["Contradictions can't both be true", "It's perfectly logical", "It respects everyone", "It's scientifically proven"]},
            {"question": "Christianity's basis for morality is:", "answer": "God's unchanging character", "options": ["God's unchanging character", "Human opinion", "Cultural norms", "Evolutionary benefit"]},
        ],
        'hard': [
            {"question": "Naturalism claims that:", "answer": "Only physical/material exists", "options": ["Only physical/material exists", "Spiritual realm exists", "God created nature", "Miracles are possible"]},
            {"question": "The cosmological argument states:", "answer": "Everything caused needs a Cause", "options": ["Everything caused needs a Cause", "Universe created itself", "No explanation needed", "Science disproves God"]},
            {"question": "If atheism is true, then:", "answer": "No objective morality exists", "options": ["No objective morality exists", "Morality still objective", "We create meaning", "All views are invalid"]},
            {"question": "The moral argument for God says:", "answer": "Objective morality needs a Moral Lawgiver", "options": ["Objective morality needs a Moral Lawgiver", "Morality evolved", "Morality is cultural", "Morality doesn't exist"]},
        ]
    }

    questions = questions_by_difficulty.get(difficulty, questions_by_difficulty["medium"]).copy()
    random.shuffle(questions)
    return questions[:15]


# ============================================================
# GAME SESSION MANAGEMENT - UPDATED FOR DIFFICULTY
# ============================================================

def save_game_session(student_id, game_key, difficulty, score, time_seconds, correct, total):
    """Save completed game session and update leaderboard with difficulty"""
    accuracy = (correct / total * 100) if total > 0 else 0

    # Calculate XP with difficulty multipliers
    difficulty_multipliers = {
        'easy': 1.0,
        'medium': 1.5,
        'hard': 2.0
    }
    multiplier = difficulty_multipliers.get(difficulty, 1.0)

    base_xp = 50
    accuracy_bonus = int(accuracy / 10) * 5
    speed_bonus = max(0, (60 - time_seconds) // 10 * 10) if time_seconds < 60 else 0
    xp_earned = int((base_xp + accuracy_bonus + speed_bonus) * multiplier)
    tokens_earned = max(1, int((score // 100) * multiplier))

    # Save session
    session = GameSession(
        student_id=student_id,
        game_key=game_key,
        difficulty=difficulty,
        score=score,
        time_seconds=time_seconds,
        accuracy=accuracy,
        questions_answered=total,
        questions_correct=correct,
        xp_earned=xp_earned,
        tokens_earned=tokens_earned,
        completed_at=datetime.utcnow()
    )
    db.session.add(session)

    # Update or create leaderboard entry
    leaderboard = GameLeaderboard.query.filter_by(
        student_id=student_id,
        game_key=game_key,
        difficulty=difficulty
    ).first()

    if not leaderboard:
        leaderboard = GameLeaderboard(
            student_id=student_id,
            game_key=game_key,
            difficulty=difficulty,
            high_score=score,
            best_time=time_seconds,
            best_accuracy=accuracy,
            total_plays=1
        )
        db.session.add(leaderboard)
    else:
        leaderboard.total_plays += 1
        if score > leaderboard.high_score:
            leaderboard.high_score = score
        if time_seconds < leaderboard.best_time or leaderboard.best_time == 0:
            leaderboard.best_time = time_seconds
        if accuracy > leaderboard.best_accuracy:
            leaderboard.best_accuracy = accuracy
        leaderboard.last_played = datetime.utcnow()

    db.session.commit()

    return {
        "xp_earned": xp_earned,
        "tokens_earned": tokens_earned,
        "new_high_score": not leaderboard or score > leaderboard.high_score,
        "accuracy": accuracy,
        "difficulty_multiplier": multiplier
    }


def get_leaderboard(game_key, difficulty, limit=10):
    """Get top scores for a game at a specific difficulty level"""
    from models import Student

    leaderboards = db.session.query(
        GameLeaderboard, Student
    ).join(
        Student, GameLeaderboard.student_id == Student.id
    ).filter(
        GameLeaderboard.game_key == game_key,
        GameLeaderboard.difficulty == difficulty
    ).order_by(
        GameLeaderboard.high_score.desc()
    ).limit(limit).all()

    return [
        {
            "student_name": student.student_name,
            "high_score": lb.high_score,
            "best_time": lb.best_time,
            "best_accuracy": lb.best_accuracy,
            "total_plays": lb.total_plays
        }
        for lb, student in leaderboards
    ]


def get_student_stats(student_id, game_key=None):
    """Get student's arcade statistics"""
    if game_key:
        sessions = GameSession.query.filter_by(
            student_id=student_id,
            game_key=game_key
        ).all()
    else:
        sessions = GameSession.query.filter_by(student_id=student_id).all()

    if not sessions:
        return None

    total_xp = sum(s.xp_earned for s in sessions)
    total_tokens = sum(s.tokens_earned for s in sessions)
    avg_accuracy = sum(s.accuracy for s in sessions) / len(sessions)

    return {
        "total_plays": len(sessions),
        "total_xp_earned": total_xp,
        "total_tokens_earned": total_tokens,
        "average_accuracy": round(avg_accuracy, 1),
        "best_score": max(s.score for s in sessions),
        "recent_sessions": sessions[-5:]
    }
