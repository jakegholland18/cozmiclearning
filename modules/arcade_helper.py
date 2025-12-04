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
        "grades": "1-12"
    },
    {
        "game_key": "fraction_frenzy",
        "name": "Fraction Frenzy 🍕",
        "description": "Match equivalent fractions under time pressure",
        "subject": "math",
        "icon": "🍕",
        "grades": "1-12"
    },
    {
        "game_key": "equation_race",
        "name": "Equation Race 🏎️",
        "description": "Solve equations faster than your grade level",
        "subject": "math",
        "icon": "🏎️",
        "grades": "1-12"
    },
    
    # Science Games
    {
        "game_key": "element_match",
        "name": "Element Match 🧪",
        "description": "Match chemical symbols to element names",
        "subject": "science",
        "icon": "🧪",
        "grades": "1-12"
    },
    {
        "game_key": "lab_quiz_rush",
        "name": "Lab Quiz Rush ⚗️",
        "description": "Rapid-fire science trivia challenge",
        "subject": "science",
        "icon": "⚗️",
        "grades": "1-12"
    },
    {
        "game_key": "planet_explorer",
        "name": "Planet Explorer 🌍",
        "description": "Test your astronomy and space knowledge",
        "subject": "science",
        "icon": "🪐",
        "grades": "1-12"
    },
    
    # Reading & Vocabulary
    {
        "game_key": "vocab_builder",
        "name": "Vocab Builder 📚",
        "description": "Match words to definitions in a race against time",
        "subject": "reading",
        "icon": "📚",
        "grades": "1-12"
    },
    {
        "game_key": "spelling_sprint",
        "name": "Spelling Sprint ✍️",
        "description": "Spell words correctly as fast as you can",
        "subject": "writing",
        "icon": "✍️",
        "grades": "1-12"
    },
    {
        "game_key": "grammar_quest",
        "name": "Grammar Quest 📝",
        "description": "Fix grammatical errors in record time",
        "subject": "writing",
        "icon": "📝",
        "grades": "1-12"
    },
    
    # History & Geography
    {
        "game_key": "history_timeline",
        "name": "Timeline Challenge ⏰",
        "description": "Put historical events in the correct order",
        "subject": "history",
        "icon": "⏰",
        "grades": "1-12"
    },
    {
        "game_key": "geography_dash",
        "name": "Geography Dash 🗺️",
        "description": "Identify countries, capitals, and landmarks",
        "subject": "history",
        "icon": "🗺️",
        "grades": "1-12"
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
        {"word": "gentle", "definition": "soft and kind", "options": ["rough", "soft and kind", "loud", "mean"]},
        {"word": "honest", "definition": "truthful", "options": ["lying", "truthful", "funny", "quiet"]},
        {"word": "proud", "definition": "feeling satisfied", "options": ["ashamed", "feeling satisfied", "scared", "tired"]},
        {"word": "angry", "definition": "feeling mad", "options": ["happy", "feeling mad", "sleepy", "hungry"]},
        {"word": "funny", "definition": "causing laughter", "options": ["sad", "causing laughter", "scary", "boring"]},
        {"word": "clever", "definition": "smart and quick", "options": ["dull", "smart and quick", "slow", "lazy"]},
        {"word": "simple", "definition": "easy to understand", "options": ["difficult", "easy to understand", "expensive", "colorful"]},
        {"word": "quiet", "definition": "making little noise", "options": ["loud", "making little noise", "bright", "heavy"]},
        {"word": "polite", "definition": "having good manners", "options": ["rude", "having good manners", "tired", "hungry"]},
        {"word": "bright", "definition": "giving much light", "options": ["dark", "giving much light", "quiet", "slow"]},
        {"word": "gentle", "definition": "soft and calm", "options": ["harsh", "soft and calm", "loud", "fast"]},
        {"word": "fresh", "definition": "newly made", "options": ["stale", "newly made", "hot", "cold"]},
        {"word": "warm", "definition": "pleasantly hot", "options": ["cold", "pleasantly hot", "wet", "dry"]},
        {"word": "strong", "definition": "having power", "options": ["weak", "having power", "small", "thin"]},
        {"word": "tiny", "definition": "very small", "options": ["huge", "very small", "loud", "fast"]},
    ],
    "middle": [
        {"word": "abundant", "definition": "existing in large quantities", "options": ["scarce", "existing in large quantities", "expensive", "colorful"]},
        {"word": "meticulous", "definition": "very careful and precise", "options": ["careless", "very careful and precise", "loud", "mysterious"]},
        {"word": "reluctant", "definition": "unwilling or hesitant", "options": ["eager", "unwilling or hesitant", "happy", "tired"]},
        {"word": "tranquil", "definition": "calm and peaceful", "options": ["chaotic", "calm and peaceful", "bright", "dark"]},
        {"word": "vibrant", "definition": "full of energy and life", "options": ["dull", "full of energy and life", "quiet", "broken"]},
        {"word": "diligent", "definition": "hard-working and careful", "options": ["lazy", "hard-working and careful", "funny", "mean"]},
        {"word": "eloquent", "definition": "fluent and persuasive in speech", "options": ["inarticulate", "fluent and persuasive in speech", "quiet", "rude"]},
        {"word": "resilient", "definition": "able to recover quickly", "options": ["fragile", "able to recover quickly", "weak", "slow"]},
        {"word": "innovative", "definition": "featuring new methods", "options": ["traditional", "featuring new methods", "boring", "expensive"]},
        {"word": "compassionate", "definition": "showing sympathy and concern", "options": ["cruel", "showing sympathy and concern", "angry", "tired"]},
        {"word": "ambitious", "definition": "having strong desire for success", "options": ["complacent", "having strong desire for success", "lazy", "sleepy"]},
        {"word": "versatile", "definition": "able to adapt or be adapted", "options": ["rigid", "able to adapt or be adapted", "boring", "expensive"]},
        {"word": "persistent", "definition": "continuing firmly", "options": ["giving up", "continuing firmly", "lazy", "weak"]},
        {"word": "skeptical", "definition": "not easily convinced", "options": ["gullible", "not easily convinced", "happy", "sad"]},
        {"word": "optimistic", "definition": "hopeful and confident", "options": ["pessimistic", "hopeful and confident", "angry", "sleepy"]},
        {"word": "genuine", "definition": "truly what it is said to be", "options": ["fake", "truly what it is said to be", "broken", "expensive"]},
        {"word": "magnificent", "definition": "extremely beautiful", "options": ["ugly", "extremely beautiful", "small", "boring"]},
        {"word": "triumphant", "definition": "having won a victory", "options": ["defeated", "having won a victory", "sleepy", "hungry"]},
        {"word": "peculiar", "definition": "strange or unusual", "options": ["normal", "strange or unusual", "bright", "dark"]},
        {"word": "inevitable", "definition": "certain to happen", "options": ["avoidable", "certain to happen", "funny", "sad"]},
    ],
    "high": [
        {"word": "articulate", "definition": "expressing oneself clearly", "options": ["mumbling", "expressing oneself clearly", "singing", "whispering"]},
        {"word": "benevolent", "definition": "kind and generous", "options": ["cruel", "kind and generous", "indifferent", "wealthy"]},
        {"word": "enigmatic", "definition": "mysterious and difficult to understand", "options": ["obvious", "mysterious and difficult to understand", "simple", "boring"]},
        {"word": "pragmatic", "definition": "dealing with things realistically", "options": ["idealistic", "dealing with things realistically", "emotional", "artistic"]},
        {"word": "tenacious", "definition": "persistent and determined", "options": ["giving up easily", "persistent and determined", "lazy", "confused"]},
        {"word": "eloquent", "definition": "fluent and persuasive speaking", "options": ["inarticulate", "fluent and persuasive speaking", "quiet", "rude"]},
        {"word": "meticulous", "definition": "showing great attention to detail", "options": ["careless", "showing great attention to detail", "lazy", "quick"]},
        {"word": "astute", "definition": "having sharp judgment", "options": ["foolish", "having sharp judgment", "slow", "tired"]},
        {"word": "circumspect", "definition": "wary and unwilling to take risks", "options": ["reckless", "wary and unwilling to take risks", "brave", "happy"]},
        {"word": "erudite", "definition": "having great knowledge", "options": ["ignorant", "having great knowledge", "simple", "boring"]},
        {"word": "fortuitous", "definition": "happening by chance", "options": ["planned", "happening by chance", "boring", "sad"]},
        {"word": "garrulous", "definition": "excessively talkative", "options": ["quiet", "excessively talkative", "sleepy", "angry"]},
        {"word": "impetuous", "definition": "acting without thought", "options": ["cautious", "acting without thought", "slow", "lazy"]},
        {"word": "judicious", "definition": "having good judgment", "options": ["reckless", "having good judgment", "simple", "quick"]},
        {"word": "lucid", "definition": "expressed clearly", "options": ["confusing", "expressed clearly", "dark", "loud"]},
        {"word": "magnanimous", "definition": "generous or forgiving", "options": ["petty", "generous or forgiving", "mean", "selfish"]},
        {"word": "nefarious", "definition": "wicked or criminal", "options": ["virtuous", "wicked or criminal", "happy", "kind"]},
        {"word": "ostentatious", "definition": "designed to impress", "options": ["modest", "designed to impress", "simple", "quiet"]},
        {"word": "pernicious", "definition": "having harmful effect", "options": ["beneficial", "having harmful effect", "helpful", "kind"]},
        {"word": "ubiquitous", "definition": "present everywhere", "options": ["rare", "present everywhere", "absent", "missing"]},
    ]
}

def generate_vocab_builder(grade_level):
    """Generate vocabulary matching game - NO REPEATS"""
    grade = int(grade_level) if grade_level.isdigit() else 5

    if grade <= 4:
        vocab_set = VOCAB_SETS["elementary"].copy()
    elif grade <= 8:
        vocab_set = VOCAB_SETS["middle"].copy()
    else:
        vocab_set = VOCAB_SETS["high"].copy()

    random.shuffle(vocab_set)
    return vocab_set[:20]  # Now returns unique questions only


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
        {"question": "What do plants produce during photosynthesis?", "answer": "oxygen", "options": ["oxygen", "carbon dioxide", "nitrogen", "water"]},
        {"question": "What is the largest planet in our solar system?", "answer": "jupiter", "options": ["jupiter", "saturn", "earth", "mars"]},
        {"question": "What animal lives both on land and in water?", "answer": "frog", "options": ["frog", "dog", "bird", "fish"]},
        {"question": "What is the hottest planet?", "answer": "venus", "options": ["venus", "mercury", "mars", "jupiter"]},
        {"question": "What makes plants green?", "answer": "chlorophyll", "options": ["chlorophyll", "water", "soil", "sunlight"]},
        {"question": "How many legs does a spider have?", "answer": "8", "options": ["8", "6", "10", "4"]},
        {"question": "What is the closest star to Earth?", "answer": "the sun", "options": ["the sun", "north star", "sirius", "alpha centauri"]},
        {"question": "What is frozen water called?", "answer": "ice", "options": ["ice", "snow", "vapor", "steam"]},
        {"question": "What do we call animals that eat only plants?", "answer": "herbivores", "options": ["herbivores", "carnivores", "omnivores", "predators"]},
        {"question": "What gas do humans breathe in?", "answer": "oxygen", "options": ["oxygen", "carbon dioxide", "nitrogen", "helium"]},
        {"question": "What is the hardest natural substance?", "answer": "diamond", "options": ["diamond", "gold", "iron", "stone"]},
        {"question": "What do tadpoles turn into?", "answer": "frogs", "options": ["frogs", "fish", "turtles", "snakes"]},
        {"question": "What is the Earth's natural satellite?", "answer": "the moon", "options": ["the moon", "the sun", "mars", "venus"]},
        {"question": "What do bees make?", "answer": "honey", "options": ["honey", "milk", "silk", "wax"]},
        {"question": "What is the center of the Earth called?", "answer": "core", "options": ["core", "crust", "mantle", "shell"]},
    ],
    "middle": [
        {"question": "What is the powerhouse of the cell?", "answer": "mitochondria", "options": ["mitochondria", "nucleus", "ribosome", "chloroplast"]},
        {"question": "What is the chemical symbol for gold?", "answer": "au", "options": ["au", "ag", "fe", "cu"]},
        {"question": "What type of rock is formed by cooling lava?", "answer": "igneous", "options": ["igneous", "sedimentary", "metamorphic", "granite"]},
        {"question": "What is the speed of light?", "answer": "299,792 km/s", "options": ["299,792 km/s", "150,000 km/s", "500,000 km/s", "1,000,000 km/s"]},
        {"question": "What is photosynthesis?", "answer": "plants making food from sunlight", "options": ["plants making food from sunlight", "breathing", "cell division", "decomposition"]},
        {"question": "What is the chemical formula for table salt?", "answer": "nacl", "options": ["nacl", "h2o", "co2", "o2"]},
        {"question": "What organelle contains DNA?", "answer": "nucleus", "options": ["nucleus", "ribosome", "vacuole", "cell wall"]},
        {"question": "What is the largest organ in the human body?", "answer": "skin", "options": ["skin", "liver", "heart", "brain"]},
        {"question": "What gas makes up most of Earth's atmosphere?", "answer": "nitrogen", "options": ["nitrogen", "oxygen", "carbon dioxide", "helium"]},
        {"question": "What is the process of water changing to vapor?", "answer": "evaporation", "options": ["evaporation", "condensation", "precipitation", "sublimation"]},
        {"question": "What are organisms that make their own food?", "answer": "producers", "options": ["producers", "consumers", "decomposers", "predators"]},
        {"question": "What is the smallest unit of life?", "answer": "cell", "options": ["cell", "atom", "molecule", "tissue"]},
        {"question": "What type of energy does the sun provide?", "answer": "light and heat", "options": ["light and heat", "electrical", "chemical", "nuclear"]},
        {"question": "What is the boiling point of water in Celsius?", "answer": "100°c", "options": ["100°c", "0°c", "50°c", "212°c"]},
        {"question": "What are the three states of matter?", "answer": "solid, liquid, gas", "options": ["solid, liquid, gas", "hot, cold, warm", "big, small, medium", "hard, soft, rough"]},
        {"question": "What is the chemical symbol for silver?", "answer": "ag", "options": ["ag", "au", "si", "s"]},
        {"question": "What is the study of weather called?", "answer": "meteorology", "options": ["meteorology", "geology", "biology", "astronomy"]},
        {"question": "What organ pumps blood through the body?", "answer": "heart", "options": ["heart", "lungs", "liver", "kidneys"]},
        {"question": "What is the freezing point of water in Celsius?", "answer": "0°c", "options": ["0°c", "100°c", "32°c", "-10°c"]},
        {"question": "What part of the plant conducts photosynthesis?", "answer": "leaves", "options": ["leaves", "roots", "stem", "flowers"]},
    ],
    "high": [
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
        {"question": "What is the study of fungi called?", "answer": "mycology", "options": ["mycology", "bacteriology", "virology", "parasitology"]},
        {"question": "What is the strongest type of chemical bond?", "answer": "covalent", "options": ["covalent", "ionic", "hydrogen", "metallic"]},
        {"question": "What is the unit of electrical resistance?", "answer": "ohm", "options": ["ohm", "ampere", "volt", "watt"]},
    ]
}

def generate_science_quiz(grade_level):
    """Generate science trivia questions - NO REPEATS"""
    grade = int(grade_level) if grade_level.isdigit() else 5

    if grade <= 4:
        questions = SCIENCE_QUESTIONS["elementary"].copy()
    elif grade <= 8:
        questions = SCIENCE_QUESTIONS["middle"].copy()
    else:
        questions = SCIENCE_QUESTIONS["high"].copy()

    random.shuffle(questions)
    return questions[:20]  # Now returns unique questions only


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
    """Match chemical symbols to element names - NO REPEATS"""
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
        {"symbol": "P", "name": "Phosphorus", "options": ["Phosphorus", "Potassium", "Platinum", "Palladium"]},
        {"symbol": "S", "name": "Sulfur", "options": ["Sulfur", "Sodium", "Silicon", "Silver"]},
        {"symbol": "Al", "name": "Aluminum", "options": ["Aluminum", "Argon", "Arsenic", "Silver"]},
        {"symbol": "Ne", "name": "Neon", "options": ["Neon", "Nitrogen", "Nickel", "Nobelium"]},
        {"symbol": "Li", "name": "Lithium", "options": ["Lithium", "Lead", "Lanthanum", "Lutetium"]},
    ]

    # Shuffle and take 20 unique elements - NO REPEATS
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


# ============================================================
# WRITING & LANGUAGE GAMES
# ============================================================

def generate_spelling_sprint(grade_level):
    """Spell words correctly as fast as you can - NO REPEATS"""
    grade = int(grade_level) if grade_level.isdigit() else 5

    word_lists = {
        "elementary": ["apple", "beach", "friend", "school", "happy", "pizza", "yellow", "elephant", "birthday", "library",
                      "garden", "rainbow", "treasure", "balloon", "mountain", "ocean", "dragon", "castle", "rocket", "adventure"],
        "middle": ["beautiful", "necessary", "receive", "separate", "definitely", "tomorrow", "although", "government", "experience", "restaurant",
                  "extraordinary", "consciousness", "opportunity", "temperature", "abbreviate", "acknowledgment", "acquaintance", "achievement", "desperate", "category"],
        "high": ["accommodate", "necessary", "occurrence", "occasionally", "recommend", "embarrass", "conscience", "rhythm", "privilege", "maintenance",
                "bureaucracy", "entrepreneurship", "pharmaceutical", "psychological", "sophisticated", "conscientious", "dilemma", "fluorescent", "guarantee", "harassment"]
    }

    if grade <= 4:
        words = word_lists["elementary"].copy()
    elif grade <= 8:
        words = word_lists["middle"].copy()
    else:
        words = word_lists["high"].copy()

    random.shuffle(words)
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
    """Fix grammatical errors in record time - NO REPEATS"""
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
    for item in base_questions[:20]:  # Take unique 20 questions only - NO REPEATS
        # Create wrong options
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
        {"event": "Printing Press Invented", "year": 1440},
        {"event": "Columbus Discovers America", "year": 1492},
        {"event": "Shakespeare's First Play", "year": 1590},
        {"event": "Civil Rights Act", "year": 1964},
    ]
    
    questions = []
    for _ in range(20):
        # Pick 2 events and ask which came first
        selected = random.sample(events, 2)
        correct_first = min(selected, key=lambda x: x['year'])
        
        questions.append({
            "question": f"Which event happened FIRST?",
            "answer": correct_first["event"],
            "options": [selected[0]["event"], selected[1]["event"]],
            "type": "timeline"
        })
    
    return questions


def generate_geography_dash(grade_level):
    """Identify countries, capitals, and landmarks - NO REPEATS"""
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
    return questions[:20]
