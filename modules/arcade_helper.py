"""
Arcade Mode - Learning Games & Competitions
Generates interactive games for students across all subjects
"""

import random
from datetime import datetime
from models import db, GameSession, GameLeaderboard, ArcadeGame


# ============================================================
# GAME CATALOG
# ============================================================

ARCADE_GAMES = [
    # Math Games
    {
        "game_key": "speed_math",
        "name": "Speed Math ⚡",
        "description": "Solve as many math problems as you can in 60 seconds!",
        "subject": "math",
        "icon": "🔢",
        "grades": "1-12"
    },
    {
        "game_key": "number_detective",
        "name": "Number Detective 🔍",
        "description": "Find patterns and solve number mysteries",
        "subject": "math",
        "icon": "🕵️",
        "grades": "3-8"
    },
    {
        "game_key": "fraction_frenzy",
        "name": "Fraction Frenzy 🍕",
        "description": "Match equivalent fractions under time pressure",
        "subject": "math",
        "icon": "🍕",
        "grades": "3-7"
    },
    {
        "game_key": "equation_race",
        "name": "Equation Race 🏎️",
        "description": "Solve equations faster than your grade level",
        "subject": "math",
        "icon": "🏎️",
        "grades": "5-12"
    },
    
    # Science Games
    {
        "game_key": "element_match",
        "name": "Element Match 🧪",
        "description": "Match chemical symbols to element names",
        "subject": "science",
        "icon": "🧪",
        "grades": "6-12"
    },
    {
        "game_key": "lab_quiz_rush",
        "name": "Lab Quiz Rush ⚗️",
        "description": "Rapid-fire science trivia challenge",
        "subject": "science",
        "icon": "⚗️",
        "grades": "4-12"
    },
    {
        "game_key": "planet_explorer",
        "name": "Planet Explorer 🌍",
        "description": "Test your astronomy and space knowledge",
        "subject": "science",
        "icon": "🪐",
        "grades": "2-8"
    },
    
    # Reading & Vocabulary
    {
        "game_key": "vocab_builder",
        "name": "Vocab Builder 📚",
        "description": "Match words to definitions in a race against time",
        "subject": "reading",
        "icon": "📚",
        "grades": "3-12"
    },
    {
        "game_key": "spelling_sprint",
        "name": "Spelling Sprint ✍️",
        "description": "Spell words correctly as fast as you can",
        "subject": "writing",
        "icon": "✍️",
        "grades": "1-8"
    },
    {
        "game_key": "grammar_quest",
        "name": "Grammar Quest 📝",
        "description": "Fix grammatical errors in record time",
        "subject": "writing",
        "icon": "📝",
        "grades": "4-10"
    },
    
    # History & Geography
    {
        "game_key": "history_timeline",
        "name": "Timeline Challenge ⏰",
        "description": "Put historical events in the correct order",
        "subject": "history",
        "icon": "⏰",
        "grades": "5-12"
    },
    {
        "game_key": "geography_dash",
        "name": "Geography Dash 🗺️",
        "description": "Identify countries, capitals, and landmarks",
        "subject": "history",
        "icon": "🗺️",
        "grades": "3-12"
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
                difficulty_levels=game_data["grades"]
            )
            db.session.add(game)
    
    db.session.commit()


# ============================================================
# GAME GENERATORS - SPEED MATH
# ============================================================

def generate_speed_math(grade_level):
    """Generate math problems based on grade level"""
    grade = int(grade_level) if grade_level.isdigit() else 5
    questions = []
    
    for _ in range(20):  # 20 questions per game
        if grade <= 2:
            # Addition/subtraction within 20
            a = random.randint(1, 20)
            b = random.randint(1, 20)
            if random.choice([True, False]):
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
        
        elif grade <= 4:
            # Multiplication tables, two-digit addition
            op = random.choice(["add", "subtract", "multiply"])
            if op == "multiply":
                a = random.randint(2, 12)
                b = random.randint(2, 12)
                questions.append({
                    "question": f"{a} × {b}",
                    "answer": a * b,
                    "type": "multiplication"
                })
            elif op == "add":
                a = random.randint(10, 99)
                b = random.randint(10, 99)
                questions.append({
                    "question": f"{a} + {b}",
                    "answer": a + b,
                    "type": "addition"
                })
            else:
                a = random.randint(20, 99)
                b = random.randint(10, a)
                questions.append({
                    "question": f"{a} - {b}",
                    "answer": a - b,
                    "type": "subtraction"
                })
        
        elif grade <= 6:
            # All operations including division
            op = random.choice(["add", "subtract", "multiply", "divide"])
            if op == "divide":
                b = random.randint(2, 12)
                answer = random.randint(2, 15)
                a = b * answer
                questions.append({
                    "question": f"{a} ÷ {b}",
                    "answer": answer,
                    "type": "division"
                })
            elif op == "multiply":
                a = random.randint(2, 25)
                b = random.randint(2, 20)
                questions.append({
                    "question": f"{a} × {b}",
                    "answer": a * b,
                    "type": "multiplication"
                })
            else:
                a = random.randint(10, 200)
                b = random.randint(10, 150)
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
        
        else:
            # Advanced: fractions, decimals, percentages, algebra
            op = random.choice(["multiply", "percent", "algebra"])
            if op == "percent":
                whole = random.randint(20, 200)
                pct = random.choice([10, 20, 25, 50, 75])
                questions.append({
                    "question": f"{pct}% of {whole}",
                    "answer": int(whole * pct / 100),
                    "type": "percentage"
                })
            elif op == "algebra":
                # Simple: x + a = b, solve for x
                a = random.randint(5, 30)
                b = random.randint(a + 5, 100)
                questions.append({
                    "question": f"x + {a} = {b}",
                    "answer": b - a,
                    "type": "algebra"
                })
            else:
                a = random.randint(10, 50)
                b = random.randint(10, 50)
                questions.append({
                    "question": f"{a} × {b}",
                    "answer": a * b,
                    "type": "multiplication"
                })
    
    return questions


# ============================================================
# VOCABULARY BUILDER
# ============================================================

VOCAB_SETS = {
    "elementary": [
        {"word": "brave", "definition": "showing courage", "options": ["scared", "showing courage", "quiet", "loud"]},
        {"word": "curious", "definition": "eager to learn", "options": ["bored", "eager to learn", "tired", "hungry"]},
        {"word": "enormous", "definition": "very large", "options": ["tiny", "very large", "red", "fast"]},
        {"word": "gleeful", "definition": "full of joy", "options": ["sad", "angry", "full of joy", "sick"]},
        {"word": "swift", "definition": "very fast", "options": ["slow", "very fast", "heavy", "light"]},
    ],
    "middle": [
        {"word": "abundant", "definition": "existing in large quantities", "options": ["scarce", "existing in large quantities", "expensive", "colorful"]},
        {"word": "meticulous", "definition": "very careful and precise", "options": ["careless", "very careful and precise", "loud", "mysterious"]},
        {"word": "reluctant", "definition": "unwilling or hesitant", "options": ["eager", "unwilling or hesitant", "happy", "tired"]},
        {"word": "tranquil", "definition": "calm and peaceful", "options": ["chaotic", "calm and peaceful", "bright", "dark"]},
        {"word": "vibrant", "definition": "full of energy and life", "options": ["dull", "full of energy and life", "quiet", "broken"]},
    ],
    "high": [
        {"word": "articulate", "definition": "expressing oneself clearly", "options": ["mumbling", "expressing oneself clearly", "singing", "whispering"]},
        {"word": "benevolent", "definition": "kind and generous", "options": ["cruel", "kind and generous", "indifferent", "wealthy"]},
        {"word": "enigmatic", "definition": "mysterious and difficult to understand", "options": ["obvious", "mysterious and difficult to understand", "simple", "boring"]},
        {"word": "pragmatic", "definition": "dealing with things realistically", "options": ["idealistic", "dealing with things realistically", "emotional", "artistic"]},
        {"word": "tenacious", "definition": "persistent and determined", "options": ["giving up easily", "persistent and determined", "lazy", "confused"]},
    ]
}

def generate_vocab_builder(grade_level):
    """Generate vocabulary matching game"""
    grade = int(grade_level) if grade_level.isdigit() else 5
    
    if grade <= 4:
        vocab_set = VOCAB_SETS["elementary"] * 4  # Repeat to get 20 questions
    elif grade <= 8:
        vocab_set = VOCAB_SETS["middle"] * 4
    else:
        vocab_set = VOCAB_SETS["high"] * 4
    
    random.shuffle(vocab_set)
    return vocab_set[:20]


# ============================================================
# SCIENCE TRIVIA
# ============================================================

SCIENCE_QUESTIONS = {
    "elementary": [
        {"question": "What is H2O commonly known as?", "answer": "water", "options": ["water", "oxygen", "hydrogen", "salt"]},
        {"question": "What planet is known as the Red Planet?", "answer": "mars", "options": ["mars", "venus", "jupiter", "saturn"]},
        {"question": "What gas do plants absorb from the air?", "answer": "carbon dioxide", "options": ["carbon dioxide", "oxygen", "nitrogen", "helium"]},
        {"question": "What is the center of an atom called?", "answer": "nucleus", "options": ["nucleus", "proton", "electron", "neutron"]},
        {"question": "What force pulls objects toward Earth?", "answer": "gravity", "options": ["gravity", "magnetism", "friction", "pressure"]},
    ],
    "middle": [
        {"question": "What is the powerhouse of the cell?", "answer": "mitochondria", "options": ["mitochondria", "nucleus", "ribosome", "chloroplast"]},
        {"question": "What is the chemical symbol for gold?", "answer": "au", "options": ["au", "ag", "fe", "cu"]},
        {"question": "What type of rock is formed by cooling lava?", "answer": "igneous", "options": ["igneous", "sedimentary", "metamorphic", "granite"]},
        {"question": "What is the speed of light?", "answer": "299,792 km/s", "options": ["299,792 km/s", "150,000 km/s", "500,000 km/s", "1,000,000 km/s"]},
        {"question": "What is photosynthesis?", "answer": "plants making food from sunlight", "options": ["plants making food from sunlight", "breathing", "cell division", "decomposition"]},
    ],
    "high": [
        {"question": "What is Avogadro's number?", "answer": "6.022 × 10²³", "options": ["6.022 × 10²³", "3.14 × 10⁸", "9.81 × 10¹⁰", "1.602 × 10⁻¹⁹"]},
        {"question": "What is the most abundant element in the universe?", "answer": "hydrogen", "options": ["hydrogen", "helium", "oxygen", "carbon"]},
        {"question": "What law states energy cannot be created or destroyed?", "answer": "conservation of energy", "options": ["conservation of energy", "newton's first law", "thermodynamics", "relativity"]},
        {"question": "What is DNA's shape called?", "answer": "double helix", "options": ["double helix", "single strand", "triple bond", "circular"]},
        {"question": "What particle has no electric charge?", "answer": "neutron", "options": ["neutron", "proton", "electron", "photon"]},
    ]
}

def generate_science_quiz(grade_level):
    """Generate science trivia questions"""
    grade = int(grade_level) if grade_level.isdigit() else 5
    
    if grade <= 4:
        questions = SCIENCE_QUESTIONS["elementary"] * 4
    elif grade <= 8:
        questions = SCIENCE_QUESTIONS["middle"] * 4
    else:
        questions = SCIENCE_QUESTIONS["high"] * 4
    
    random.shuffle(questions)
    return questions[:20]


# ============================================================
# GAME SESSION MANAGEMENT
# ============================================================

def save_game_session(student_id, game_key, grade_level, score, time_seconds, correct, total):
    """Save completed game session and update leaderboard"""
    accuracy = (correct / total * 100) if total > 0 else 0
    
    # Calculate XP and tokens based on performance
    base_xp = 50
    accuracy_bonus = int(accuracy / 10) * 5
    speed_bonus = max(0, (60 - time_seconds) // 10 * 10) if time_seconds < 60 else 0
    xp_earned = base_xp + accuracy_bonus + speed_bonus
    tokens_earned = max(1, score // 100)
    
    # Save session
    session = GameSession(
        student_id=student_id,
        game_key=game_key,
        grade_level=str(grade_level),
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
        grade_level=str(grade_level)
    ).first()
    
    if not leaderboard:
        leaderboard = GameLeaderboard(
            student_id=student_id,
            game_key=game_key,
            grade_level=str(grade_level),
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
        "accuracy": accuracy
    }


def get_leaderboard(game_key, grade_level, limit=10):
    """Get top scores for a game at a specific grade level"""
    from models import Student
    
    leaderboards = db.session.query(
        GameLeaderboard, Student
    ).join(
        Student, GameLeaderboard.student_id == Student.id
    ).filter(
        GameLeaderboard.game_key == game_key,
        GameLeaderboard.grade_level == str(grade_level)
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
        "recent_sessions": sessions[-5:]  # Last 5 sessions
    }


# ============================================================
# ADDITIONAL MATH GAMES
# ============================================================

def generate_number_detective(grade_level):
    """Find patterns and solve number mysteries"""
    grade = int(grade_level) if grade_level.isdigit() else 5
    questions = []
    
    for _ in range(20):
        pattern_type = random.choice(["sequence", "missing", "odd_one_out"])
        
        if pattern_type == "sequence":
            # Number sequences
            start = random.randint(2, 20)
            step = random.choice([2, 3, 5, 10])
            seq = [start + i * step for i in range(5)]
            answer = seq[-1] + step
            questions.append({
                "question": f"What comes next? {', '.join(map(str, seq))}, __",
                "answer": answer,
                "type": "sequence",
                "options": [answer, answer + 1, answer - 1, answer + step]
            })
        
        elif pattern_type == "missing":
            # Find missing number in pattern
            start = random.randint(5, 30)
            step = random.choice([3, 4, 5, 7])
            seq = [start + i * step for i in range(4)]
            missing_idx = random.randint(1, 2)
            answer = seq[missing_idx]
            seq[missing_idx] = "?"
            questions.append({
                "question": f"Find the missing number: {', '.join(map(str, seq))}",
                "answer": answer,
                "type": "missing",
                "options": [answer, answer + 1, answer - 1, answer + step]
            })
        
        else:
            # Odd one out
            base = random.randint(2, 10) * 2  # Even number
            evens = [base + i * 2 for i in range(3)]
            odd = random.randint(1, 20) * 2 + 1
            nums = evens + [odd]
            random.shuffle(nums)
            questions.append({
                "question": f"Which number is odd? {', '.join(map(str, nums))}",
                "answer": odd,
                "type": "odd_one_out",
                "options": nums
            })
    
    return questions


def generate_fraction_frenzy(grade_level):
    """Match equivalent fractions"""
    questions = []
    
    for _ in range(20):
        # Generate simple fractions and their equivalents
        num = random.randint(1, 8)
        den = random.randint(num + 1, 12)
        mult = random.choice([2, 3, 4])
        
        equiv_num = num * mult
        equiv_den = den * mult
        
        question_type = random.choice(["match", "simplify"])
        
        if question_type == "match":
            questions.append({
                "question": f"Which fraction equals {num}/{den}?",
                "answer": f"{equiv_num}/{equiv_den}",
                "type": "match",
                "options": [
                    f"{equiv_num}/{equiv_den}",
                    f"{equiv_num + 1}/{equiv_den}",
                    f"{equiv_num}/{equiv_den + 1}",
                    f"{num}/{den + 1}"
                ]
            })
        else:
            # Simplify fraction
            questions.append({
                "question": f"Simplify: {equiv_num}/{equiv_den}",
                "answer": f"{num}/{den}",
                "type": "simplify",
                "options": [
                    f"{num}/{den}",
                    f"{num + 1}/{den}",
                    f"{num}/{den + 1}",
                    f"{equiv_num}/{den}"
                ]
            })
    
    return questions


def generate_equation_race(grade_level):
    """Solve equations faster than your grade level"""
    grade = int(grade_level) if grade_level.isdigit() else 5
    questions = []
    
    for _ in range(20):
        if grade <= 6:
            # Simple one-step equations: x + a = b or x - a = b
            a = random.randint(5, 30)
            x = random.randint(10, 50)
            op = random.choice(["+", "-"])
            
            if op == "+":
                b = x + a
                questions.append({
                    "question": f"Solve: x + {a} = {b}",
                    "answer": x,
                    "type": "one_step"
                })
            else:
                b = x - a
                questions.append({
                    "question": f"Solve: x - {a} = {b}",
                    "answer": x,
                    "type": "one_step"
                })
        else:
            # Two-step equations: ax + b = c
            a = random.randint(2, 10)
            x = random.randint(5, 20)
            b = random.randint(5, 30)
            c = a * x + b
            
            questions.append({
                "question": f"Solve: {a}x + {b} = {c}",
                "answer": x,
                "type": "two_step"
            })
    
    return questions


# ============================================================
# SCIENCE GAMES
# ============================================================

def generate_element_match(grade_level):
    """Match chemical symbols to element names"""
    elements = [
        {"symbol": "H", "name": "Hydrogen", "options": ["Hydrogen", "Helium", "Hafnium", "Holmium"]},
        {"symbol": "O", "name": "Oxygen", "options": ["Oxygen", "Osmium", "Oganesson", "Oxide"]},
        {"symbol": "C", "name": "Carbon", "options": ["Carbon", "Calcium", "Copper", "Chromium"]},
        {"symbol": "N", "name": "Nitrogen", "options": ["Nitrogen", "Neon", "Nickel", "Nobelium"]},
        {"symbol": "Fe", "name": "Iron", "options": ["Iron", "Fluorine", "Fermium", "Francium"]},
        {"symbol": "Au", "name": "Gold", "options": ["Gold", "Silver", "Aluminum", "Argon"]},
        {"symbol": "Ag", "name": "Silver", "options": ["Silver", "Gold", "Argon", "Arsenic"]},
        {"symbol": "Na", "name": "Sodium", "options": ["Sodium", "Nitrogen", "Neon", "Nickel"]},
        {"symbol": "Cl", "name": "Chlorine", "options": ["Chlorine", "Calcium", "Carbon", "Copper"]},
        {"symbol": "He", "name": "Helium", "options": ["Helium", "Hydrogen", "Hafnium", "Holmium"]},
        {"symbol": "Ca", "name": "Calcium", "options": ["Calcium", "Carbon", "Cadmium", "Californium"]},
        {"symbol": "K", "name": "Potassium", "options": ["Potassium", "Krypton", "Phosphorus", "Platinum"]},
        {"symbol": "Mg", "name": "Magnesium", "options": ["Magnesium", "Manganese", "Mercury", "Molybdenum"]},
        {"symbol": "Zn", "name": "Zinc", "options": ["Zinc", "Zirconium", "Xenon", "Yttrium"]},
        {"symbol": "Cu", "name": "Copper", "options": ["Copper", "Carbon", "Curium", "Cesium"]},
    ]
    
    questions = []
    for _ in range(20):
        elem = random.choice(elements)
        random.shuffle(elem["options"])
        questions.append({
            "question": f"What element is '{elem['symbol']}'?",
            "answer": elem["name"],
            "options": elem["options"][:],
            "type": "element"
        })
    
    return questions


# ============================================================
# WRITING & LANGUAGE GAMES
# ============================================================

def generate_spelling_sprint(grade_level):
    """Spell words correctly as fast as you can"""
    grade = int(grade_level) if grade_level.isdigit() else 5
    
    word_lists = {
        "elementary": ["apple", "beach", "friend", "school", "happy", "pizza", "yellow", "elephant", "birthday", "library"],
        "middle": ["beautiful", "necessary", "receive", "separate", "definitely", "tomorrow", "although", "government", "experience", "restaurant"],
        "high": ["accommodate", "necessary", "occurrence", "occasionally", "recommend", "embarrass", "conscience", "rhythm", "privilege", "maintenance"]
    }
    
    if grade <= 4:
        words = word_lists["elementary"] * 2
    elif grade <= 8:
        words = word_lists["middle"] * 2
    else:
        words = word_lists["high"] * 2
    
    questions = []
    for word in words[:20]:
        # Create misspelled versions
        misspelled = [
            word[:2] + word[2:].replace('e', 'a', 1),  # Vowel swap
            word[:-1] + ('s' if word[-1] != 's' else 'z'),  # Wrong ending
            word[:3] + word[4:] if len(word) > 4 else word + 'e'  # Missing/extra letter
        ]
        
        options = [word] + misspelled[:3]
        random.shuffle(options)
        
        questions.append({
            "question": f"Spell correctly: {word.upper()}",
            "answer": word,
            "options": options,
            "type": "spelling"
        })
    
    return questions


def generate_grammar_quest(grade_level):
    """Fix grammatical errors in record time"""
    questions = [
        {"question": "Their going to the store", "answer": "They're going to the store", "error": "their/they're"},
        {"question": "The cat is sleeping in it's bed", "answer": "The cat is sleeping in its bed", "error": "its/it's"},
        {"question": "Me and him went to school", "answer": "He and I went to school", "error": "pronoun case"},
        {"question": "She don't like apples", "answer": "She doesn't like apples", "error": "subject-verb agreement"},
        {"question": "I seen that movie before", "answer": "I have seen that movie before", "error": "past participle"},
        {"question": "Your the best!", "answer": "You're the best!", "error": "your/you're"},
        {"question": "Between you and I", "answer": "Between you and me", "error": "pronoun case"},
        {"question": "I could of done better", "answer": "I could have done better", "error": "could of/could have"},
        {"question": "There house is big", "answer": "Their house is big", "error": "there/their"},
        {"question": "Its a beautiful day", "answer": "It's a beautiful day", "error": "its/it's"},
    ]
    
    # Expand to 20 questions
    questions = questions * 2
    random.shuffle(questions)
    return questions[:20]


# ============================================================
# HISTORY & GEOGRAPHY GAMES
# ============================================================

def generate_history_timeline(grade_level):
    """Put historical events in the correct order"""
    events = [
        {"event": "Declaration of Independence", "year": 1776},
        {"event": "Civil War Begins", "year": 1861},
        {"event": "World War I Starts", "year": 1914},
        {"event": "Great Depression", "year": 1929},
        {"event": "World War II Ends", "year": 1945},
        {"event": "Moon Landing", "year": 1969},
        {"event": "Fall of Berlin Wall", "year": 1989},
        {"event": "Internet Created", "year": 1989},
        {"event": "American Revolution", "year": 1775},
        {"event": "Constitution Signed", "year": 1787},
    ]
    
    questions = []
    for _ in range(20):
        # Pick 4 random events
        selected = random.sample(events, 4)
        correct_order = sorted(selected, key=lambda x: x['year'])
        shuffled = selected.copy()
        random.shuffle(shuffled)
        
        questions.append({
            "question": "Put these events in chronological order (earliest first):",
            "events": [e["event"] for e in shuffled],
            "answer": ", ".join([e["event"] for e in correct_order]),
            "type": "timeline"
        })
    
    return questions


def generate_geography_dash(grade_level):
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
    ]
    
    questions = questions * 2
    random.shuffle(questions)
    return questions[:20]
