# modules/manners_helper.py

from modules.shared_ai import study_buddy_ai


# Preset RespectRealm Lessons - Organized by Category
RESPECTREALM_LESSONS = {
    "table_manners": {
        "category": "Table Manners & Dining",
        "icon": "🍽️",
        "lessons": [
            {"id": "basic_table", "title": "Basic Table Manners", "description": "How to sit, use utensils, and behave at the table"},
            {"id": "restaurant", "title": "Restaurant Etiquette", "description": "Ordering, tipping, and being respectful in restaurants"},
            {"id": "family_dinner", "title": "Family Dinner Time", "description": "Making dinner time pleasant for everyone"},
            {"id": "eating_politely", "title": "Eating Politely", "description": "Chewing with your mouth closed, not talking with food in mouth"},
        ]
    },
    "public_behavior": {
        "category": "Public Behavior",
        "icon": "🏪",
        "lessons": [
            {"id": "store_behavior", "title": "How to Act in Stores", "description": "Being respectful while shopping"},
            {"id": "church_behavior", "title": "Church & Quiet Places", "description": "Behavior in church, libraries, and other quiet spaces"},
            {"id": "waiting_in_line", "title": "Waiting Your Turn", "description": "Patience in lines and taking turns"},
            {"id": "indoor_voice", "title": "Using Your Indoor Voice", "description": "When and how to control your volume"},
        ]
    },
    "respect": {
        "category": "Respect & Courtesy",
        "icon": "🤝",
        "lessons": [
            {"id": "greeting_adults", "title": "Greeting Adults Properly", "description": "How to introduce yourself and show respect"},
            {"id": "yes_sir_maam", "title": "Yes Sir, Yes Ma'am", "description": "Respectful responses to adults"},
            {"id": "listening", "title": "Active Listening", "description": "How to listen when others are talking"},
            {"id": "interrupting", "title": "Not Interrupting", "description": "Waiting for your turn to speak"},
        ]
    },
    "basic_courtesy": {
        "category": "Basic Courtesy",
        "icon": "💝",
        "lessons": [
            {"id": "please_thank_you", "title": "Please and Thank You", "description": "Using polite words every day"},
            {"id": "excuse_me", "title": "Excuse Me & I'm Sorry", "description": "When and how to apologize"},
            {"id": "holding_doors", "title": "Holding Doors Open", "description": "Being helpful and courteous"},
            {"id": "eye_contact", "title": "Making Eye Contact", "description": "Showing respect through eye contact"},
        ]
    },
    "phone_digital": {
        "category": "Phone & Digital Manners",
        "icon": "📱",
        "lessons": [
            {"id": "phone_calls", "title": "Phone Call Etiquette", "description": "How to make and answer phone calls politely"},
            {"id": "texting_manners", "title": "Texting Properly", "description": "When and how to text respectfully"},
            {"id": "social_media", "title": "Social Media Behavior", "description": "Being kind and appropriate online"},
            {"id": "screen_time", "title": "Screen Time Manners", "description": "When to put your phone away"},
        ]
    },
    "personal_care": {
        "category": "Personal Care & Hygiene",
        "icon": "🧼",
        "lessons": [
            {"id": "hygiene_basics", "title": "Basic Hygiene", "description": "Washing hands, brushing teeth, staying clean"},
            {"id": "dressing_properly", "title": "Dressing Appropriately", "description": "Choosing clothes for different occasions"},
            {"id": "grooming", "title": "Personal Grooming", "description": "Taking care of your appearance"},
            {"id": "cleanliness", "title": "Keeping Things Clean", "description": "Cleaning up after yourself"},
        ]
    },
    "conversation": {
        "category": "Conversation Skills",
        "icon": "💬",
        "lessons": [
            {"id": "small_talk", "title": "Making Small Talk", "description": "How to have pleasant conversations"},
            {"id": "asking_questions", "title": "Asking Good Questions", "description": "Showing interest in others"},
            {"id": "compliments", "title": "Giving Compliments", "description": "Being kind and genuine"},
            {"id": "disagreeing_politely", "title": "Disagreeing Politely", "description": "How to disagree without being rude"},
        ]
    },
    "responsibility": {
        "category": "Responsibility & Work Ethic",
        "icon": "💼",
        "lessons": [
            {"id": "chores", "title": "Doing Chores Without Complaining", "description": "Taking responsibility at home"},
            {"id": "being_on_time", "title": "Being On Time", "description": "Punctuality and respecting others' time"},
            {"id": "keeping_promises", "title": "Keeping Your Word", "description": "Following through on commitments"},
            {"id": "hard_work", "title": "Working Hard", "description": "Developing a strong work ethic"},
        ]
    },
    "physical_discipline": {
        "category": "Physical Discipline & Fitness",
        "icon": "💪",
        "lessons": [
            {"id": "exercise_habit", "title": "Building an Exercise Habit", "description": "Push your body to build strength and discipline"},
            {"id": "sports_character", "title": "Sports & Character", "description": "Teamwork, losing gracefully, and playing hard"},
            {"id": "physical_challenges", "title": "Embracing Physical Challenges", "description": "Don't quit when it gets hard - push through"},
            {"id": "taking_care_body", "title": "Taking Care of Your Body", "description": "Your body is a temple - treat it with respect"},
            {"id": "outdoor_work", "title": "Outdoor Work & Manual Labor", "description": "The value of physical work and getting your hands dirty"},
            {"id": "athletic_excellence", "title": "Pursuing Athletic Excellence", "description": "Train hard, compete with honor, serve your team"},
        ]
    },
    "humility_growth": {
        "category": "Humility & Growth",
        "icon": "🙏",
        "lessons": [
            {"id": "accepting_correction", "title": "Accepting Correction", "description": "Listen when you're wrong - that's how champions grow"},
            {"id": "humble_spirit", "title": "Cultivating a Humble Spirit", "description": "The strongest people don't need to brag"},
            {"id": "admitting_mistakes", "title": "Admitting Your Mistakes", "description": "Own it. Fix it. Learn from it. Move forward."},
            {"id": "learning_from_failure", "title": "Learning from Failure", "description": "Failure isn't final - it's training for success"},
            {"id": "no_excuses", "title": "No Excuses, Just Ownership", "description": "Take responsibility - no blame, no excuses"},
            {"id": "teachable_heart", "title": "Having a Teachable Heart", "description": "Stay humble. Stay hungry. Keep learning."},
        ]
    },
}


def get_all_lessons():
    """Get all lessons organized by category."""
    return RESPECTREALM_LESSONS


def get_lesson_by_id(lesson_id):
    """Find a specific lesson by its ID."""
    for category_key, category_data in RESPECTREALM_LESSONS.items():
        for lesson in category_data["lessons"]:
            if lesson["id"] == lesson_id:
                return {
                    "lesson": lesson,
                    "category": category_data["category"],
                    "icon": category_data["icon"]
                }
    return None


def teach_manners(scenario: str, grade: str, character: str) -> str:
    """
    Teaches manners, common sense, courtesy, and respectful behavior.

    Covers topics like:
    - Table manners and dining etiquette
    - Public behavior and social awareness
    - Respect for elders and authority
    - Common courtesy (please, thank you, excuse me)
    - Phone etiquette and digital manners
    - Personal hygiene and presentation
    - Conversation skills and active listening
    - Conflict resolution and apologies
    - Helping others and being considerate
    - Cultural sensitivity and awareness
    """

    prompt = f"""
You are a CHARACTER COACH teaching life skills that forge CHAMPIONS of virtue and service.

TOPIC:
{scenario}

YOUR MISSION:
Teach this RespectRealm lesson with INTENSE MOTIVATIONAL ENERGY - like a Rocky training montage meets a sermon on the mount. Make them WANT to push harder, be better, serve more. This is about becoming a WARRIOR of character who serves others and honors God.

GRADE LEVEL: {grade}

FORMAT REQUIREMENTS:
You MUST use the standard 6-section format:

SECTION 1 — OVERVIEW
SECTION 2 — KEY FACTS
SECTION 3 — CHRISTIAN VIEW
SECTION 4 — AGREEMENT
SECTION 5 — DIFFERENCE
SECTION 6 — PRACTICE

TONE & ENERGY (CRITICAL - THIS IS THE GAME CHANGER):
• Write like Rocky giving a pre-fight speech - RAW, POWERFUL, AUTHENTIC
• Use short punchy sentences. Drive points home. Make them FEEL it.
• Talk directly to them: "You want to be great? Then DO great things."
• Don't be preachy - be INSPIRING. Fire them up!
• Use phrases like: "Here's the truth..." "Let me tell you something..." "Listen up..."
• Make them believe they can be BETTER, STRONGER, MORE than they think
• Channel coaches who push their athletes: intense, demanding, but believing in them
• NO fluff. NO soft language. Just TRUTH delivered with FIRE.

MOTIVATIONAL SPEECH STYLE:
✅ "The world will tell you to take the easy road. Don't. Champions take the HARD road."
✅ "Your character is forged in the moments when nobody's watching. That's where legends are made."
✅ "You think this is about being polite? No. This is about being EXCELLENT. About being FAITHFUL."
✅ "Every single day you get a choice: be ordinary or be EXTRAORDINARY. Which one are you choosing?"
✅ "It's gonna be hard. Good. That's how you know it's worth doing."
✅ "Jesus didn't come to be served - He came to SERVE. And He's calling you to do the same. Are you ready?"

CORE VALUES TO HAMMER HOME:
• SELFLESSNESS: "It's not about you - it's about WHO YOU CAN SERVE"
• SERVICE: "Look for the person who needs help. Then BE that help."
• CHARACTER: "Who you are when nobody's looking - THAT'S who you really are"
• EXCELLENCE: "Give 110%. Then find another 10%."
• INTEGRITY: "Do what's right even when it costs you something"
• HUMILITY: "The strongest people are the ones who serve others"
• PERSEVERANCE: "When it gets hard, that's when you DIG DEEPER"

BAD vs GOOD EXAMPLES:
❌ DON'T SAY: "Good manners show respect for the dignity of others"
✅ DO SAY: "Here's the truth: when you show respect, you're saying 'You matter.' That's POWERFUL. That's how you change the world - one person at a time."

❌ DON'T SAY: "This is part of becoming a person of strong character"
✅ DO SAY: "You want to be great? Then BUILD YOUR CHARACTER like you're training for the Olympics. Every rep counts. Every choice matters."

❌ DON'T SAY: "Your character isn't about being liked"
✅ DO SAY: "Listen up: Your character isn't a popularity contest. It's about being FAITHFUL to who God made you to be. Be that person with EVERYTHING you've got."

CHRISTIAN VIEW (Section 3) - MAKE IT POWERFUL:
• "Jesus washed FEET. The King of Kings got on His KNEES to serve. If that doesn't fire you up, check your pulse."
• "Love your neighbor as yourself - not because it feels good, but because it's RIGHT. Because that's what champions do."
• "Whatever you do, work at it with ALL YOUR HEART - like you're working for the Lord Himself. That means NO half-efforts."
• "Be a servant leader like Christ. That's real strength. That's real power."

PRACTICE (Section 6) - CHALLENGE THEM LIKE A COACH:
• Make assignments DEMANDING: "This week, find someone who needs help and serve them WITHOUT being asked. No recognition. No praise. Just DO IT."
• "Do your chores like you're training for battle. Excellence in the small things builds excellence in EVERYTHING."
• "Push yourself when you don't feel like it. That's where character is FORGED."
• End with fire: "You've got what it takes. Now GO PROVE IT."

REMEMBER: Write every section like you're coaching them to be CHAMPIONS. Make them want to run through a wall. This is about building WARRIORS of character who serve others with EVERYTHING they've got. NO EXCUSES. NO SHORTCUTS. JUST EXCELLENCE.
"""

    return study_buddy_ai(prompt, grade, character)
