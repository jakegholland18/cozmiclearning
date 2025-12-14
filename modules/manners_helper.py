# modules/manners_helper.py

from modules.shared_ai import study_buddy_ai


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
This is NobleForge - where we teach students how to be respectful, courteous, and use common sense in everyday situations. Cover topics like:

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
