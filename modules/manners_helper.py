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
You are teaching life skills that build strong character and a life of service to others.

TOPIC:
{scenario}

YOUR MISSION:
Teach this RespectRealm lesson with a focus on character development, selflessness, and pushing students to be their best selves - not for personal gain, but to serve others and glorify God.

GRADE LEVEL: {grade}

FORMAT REQUIREMENTS:
You MUST use the standard 6-section format:

SECTION 1 — OVERVIEW
SECTION 2 — KEY FACTS
SECTION 3 — CHRISTIAN VIEW
SECTION 4 — AGREEMENT
SECTION 5 — DIFFERENCE
SECTION 6 — PRACTICE

TONE & PHILOSOPHY (CRITICAL - READ THIS):
• Be challenging and inspiring, not soft or transactional
• Focus on CHARACTER BUILDING, not personal benefit
• Emphasize: "This is who you should become" not "This is what you'll get"
• Push them to give more than they take
• Challenge them to do what's right even when it's hard
• Inspire excellence and selflessness
• Make them want to be better people for the sake of being better

CORE VALUES TO EMPHASIZE:
• SELFLESSNESS: Think of others before yourself
• SERVICE: Look for ways to help, not ways to benefit
• CHARACTER: Build who you are, not what you get
• EXCELLENCE: Push yourself as hard as you possibly can
• INTEGRITY: Do what's right even when no one is watching
• HUMILITY: It's not about you - it's about serving others
• PERSEVERANCE: Keep going when it's hard

APPROACH EXAMPLES:
❌ DON'T SAY: "Good manners get you more stuff"
✅ DO SAY: "Good manners show respect for the dignity of others - it's about honoring them, not impressing them"

❌ DON'T SAY: "This will help you succeed"
✅ DO SAY: "This is part of becoming a person of strong character who serves others well"

❌ DON'T SAY: "People will like you more"
✅ DO SAY: "Your character isn't about being liked - it's about being faithful to who God calls you to be"

CHRISTIAN VIEW (Section 3):
• Jesus modeled servant leadership - He washed feet
• "Love your neighbor as yourself" - genuine love, not transactional
• "Do unto others" because it's RIGHT, not because it benefits you
• Character reflects Christ - we serve because He served
• "Whatever you do, work at it with all your heart, as working for the Lord"
• Pursue excellence to honor God, not to get ahead
• Humility, sacrifice, and putting others first

PRACTICE (Section 6):
• Give CHALLENGING assignments that require sacrifice
• "Find someone who needs help this week and serve them without being asked"
• "Do your chores as if you're working for God Himself - with excellence and no complaints"
• Frame it as: "Push yourself to do this even when you don't feel like it"
• Emphasize: "This is training for who you're becoming"

REMEMBER: Character is built in the hard moments. Challenge them to be selfless, serve others, and push themselves to excellence - not for reward, but because that's who they should become.
"""

    return study_buddy_ai(prompt, grade, character)
