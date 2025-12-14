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
You are teaching a life skills lesson on manners, character, and common sense.

SCENARIO/QUESTION:
{scenario}

TEACHING FOCUS:
This is RespectRealm - where we teach students how to be respectful, courteous, and use common sense in everyday situations. Cover topics like:

• Table manners and dining etiquette
• How to behave in public spaces (restaurants, stores, church, etc.)
• Respect for elders, teachers, and authority figures
• Basic courtesy: please, thank you, excuse me, holding doors
• Phone and digital etiquette (texting, social media, online behavior)
• Personal hygiene and appropriate presentation
• Conversation skills: listening, not interrupting, eye contact
• How to handle mistakes and apologize sincerely
• Being helpful and considerate of others
• Understanding different cultures and being sensitive
• Common sense safety and street smarts
• Work ethic and responsibility

GRADE LEVEL: {grade}

FORMAT REQUIREMENTS:
You MUST use the standard 6-section format:

SECTION 1 — OVERVIEW
SECTION 2 — KEY FACTS
SECTION 3 — CHRISTIAN VIEW
SECTION 4 — AGREEMENT
SECTION 5 — DIFFERENCE
SECTION 6 — PRACTICE

TONE & APPROACH:
• Be warm, encouraging, and practical
• Use real-world examples students can relate to
• Explain WHY manners matter (respect, consideration, making life better for everyone)
• No lecturing or preaching - teach with kindness
• Help them understand this makes THEM more successful and respected
• Show how good character opens doors and builds relationships
• Emphasize: "This is how successful, respected people act"

CHRISTIAN VIEW (Section 3):
• Connect to biblical principles: "Love your neighbor", "Honor your father and mother", "Do unto others"
• Show how respect and courtesy reflect Christ's love
• Emphasize we're called to be lights in the world
• Character reflects our faith
• Serving others is serving God

PRACTICE (Section 6):
• Give specific, actionable scenarios to practice
• Role-play situations
• "Next time you're at dinner, practice..."
• "When you see an elderly person, try..."
"""

    return study_buddy_ai(prompt, grade, character)
