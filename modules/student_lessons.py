"""
Student Lessons - Grade-appropriate structured learning content
Provides curated lessons for each subject and grade level with AI follow-up chat
"""

import os
import json
from typing import Dict, List, Optional
from modules.shared_ai import get_client


# Lesson topics organized by subject and grade
LESSON_TOPICS = {
    "num_forge": {
        1: ["Counting to 100", "Addition & Subtraction", "Shapes & Patterns", "Money Basics"],
        2: ["Place Value", "Two-Digit Addition", "Time & Calendar", "Measurement Basics"],
        3: ["Multiplication Tables", "Division Basics", "Fractions Introduction", "Area & Perimeter"],
        4: ["Multi-Digit Multiplication", "Long Division", "Decimals", "Geometry Fundamentals"],
        5: ["Fraction Operations", "Decimal Operations", "Order of Operations", "Volume & Surface Area"],
        6: ["Ratios & Proportions", "Percentages", "Integers", "Coordinate Plane"],
        7: ["Algebraic Expressions", "Solving Equations", "Probability", "Statistics"],
        8: ["Linear Equations", "Systems of Equations", "Functions", "Pythagorean Theorem"],
        9: ["Quadratic Equations", "Polynomials", "Graphing Functions", "Exponential Growth"],
        10: ["Trigonometry Basics", "Advanced Algebra", "Sequences & Series", "Logarithms"],
        11: ["Pre-Calculus", "Trigonometric Functions", "Conic Sections", "Limits"],
        12: ["Calculus Introduction", "Derivatives", "Integrals", "Applications of Calculus"]
    },
    "atom_sphere": {
        1: ["Five Senses", "Living vs Non-Living", "Weather Basics", "Animal Habitats"],
        2: ["Plant Life Cycle", "States of Matter", "Earth & Sky", "Simple Machines"],
        3: ["Ecosystems", "Rocks & Minerals", "Force & Motion", "Human Body Systems"],
        4: ["Energy Forms", "Water Cycle", "Solar System", "Sound & Light"],
        5: ["Cells & Organisms", "Chemical vs Physical Changes", "Space Exploration", "Electricity"],
        6: ["Photosynthesis", "Periodic Table Intro", "Plate Tectonics", "Scientific Method"],
        7: ["Cell Biology", "Atomic Structure", "Climate & Weather", "Simple Machines Deep Dive"],
        8: ["Genetics Basics", "Chemical Reactions", "Earth's Layers", "Newton's Laws"],
        9: ["Evolution & Natural Selection", "Chemical Bonding", "Astronomy", "Energy Transfer"],
        10: ["DNA & Protein Synthesis", "Stoichiometry", "Geology", "Waves & Optics"],
        11: ["Advanced Biology", "Organic Chemistry", "Environmental Science", "Thermodynamics"],
        12: ["AP Biology Topics", "AP Chemistry Topics", "AP Physics Topics", "Biochemistry"]
    },
    "chrono_core": {
        1: ["My Family History", "Holidays & Traditions", "Community Helpers", "Then vs Now"],
        2: ["American Symbols", "Native Americans", "Early Explorers", "Pilgrims & Plymouth"],
        3: ["Colonial America", "American Revolution", "Founding Fathers", "Constitution Basics"],
        4: ["Westward Expansion", "Civil War", "Reconstruction", "Industrial Revolution"],
        5: ["World War I", "Great Depression", "World War II", "Civil Rights Movement"],
        6: ["Ancient Civilizations", "Greek & Roman Empire", "Middle Ages", "Renaissance"],
        7: ["Age of Exploration", "American Colonies Deep Dive", "Revolutionary War Details", "Early Republic"],
        8: ["Manifest Destiny", "Civil War Causes", "Reconstruction Era", "Gilded Age"],
        9: ["Progressive Era", "WWI & WWII", "Cold War", "Vietnam Era"],
        10: ["Ancient World History", "Medieval Europe", "Islamic Golden Age", "Asian Empires"],
        11: ["Modern European History", "World Wars Deep Dive", "Decolonization", "Modern Middle East"],
        12: ["AP US History Topics", "AP World History Topics", "Government & Politics", "Economics History"]
    },
    "story_verse": {
        1: ["Letter Sounds", "Sight Words", "Simple Sentences", "Story Elements"],
        2: ["Reading Fluency", "Main Idea", "Character Analysis", "Sequencing Events"],
        3: ["Context Clues", "Cause & Effect", "Compare & Contrast", "Fiction vs Non-Fiction"],
        4: ["Theme Identification", "Point of View", "Literary Devices", "Summarizing"],
        5: ["Inference Skills", "Author's Purpose", "Text Structure", "Vocabulary Building"],
        6: ["Complex Texts", "Figurative Language", "Textual Evidence", "Critical Reading"],
        7: ["Literary Analysis", "Poetry Analysis", "Drama & Plays", "Research Skills"],
        8: ["Advanced Comprehension", "Rhetoric & Persuasion", "Media Literacy", "Annotating Texts"],
        9: ["Classic Literature", "Modern Fiction", "Non-Fiction Analysis", "Argument Analysis"],
        10: ["World Literature", "Literary Criticism", "Advanced Poetry", "Comparative Reading"],
        11: ["British Literature", "American Literature", "Literary Theory", "Advanced Rhetoric"],
        12: ["AP Literature Topics", "College-Level Reading", "Critical Theory", "Research Methods"]
    },
    "ink_haven": {
        1: ["Writing Letters", "Simple Sentences", "Personal Narratives", "Drawing & Labels"],
        2: ["Paragraph Writing", "Descriptive Writing", "Opinion Writing", "Grammar Basics"],
        3: ["Essay Structure", "Creative Stories", "Informative Writing", "Editing Skills"],
        4: ["Multi-Paragraph Essays", "Research Reports", "Persuasive Writing", "Dialogue Writing"],
        5: ["Five-Paragraph Essay", "Compare/Contrast Essays", "Narrative Techniques", "Revising Strategies"],
        6: ["Argumentative Writing", "Literary Analysis", "Research Papers", "Citation Basics"],
        7: ["Advanced Essays", "Creative Writing", "Technical Writing", "Peer Review"],
        8: ["Rhetorical Analysis", "Synthesis Essays", "Personal Essays", "Advanced Grammar"],
        9: ["College Essay Prep", "Analytical Writing", "Research Methods", "Style & Voice"],
        10: ["Advanced Rhetoric", "Literary Criticism Writing", "Argumentative Mastery", "Publication"],
        11: ["AP Language Topics", "College Writing", "Creative Non-Fiction", "Advanced Research"],
        12: ["AP Literature Writing", "Thesis Development", "Academic Writing", "Professional Writing"]
    },
    "faith_realm": {
        1: ["God's Love", "Creation Story", "Jesus' Birth", "Prayer Basics"],
        2: ["Bible Stories", "Ten Commandments", "Psalms for Kids", "Fruits of the Spirit"],
        3: ["Old Testament Heroes", "Jesus' Miracles", "Parables", "Christian Character"],
        4: ["Life of Jesus", "New Testament Stories", "Christian Living", "Bible Study Skills"],
        5: ["Books of the Bible", "Gospels Overview", "Epistles Introduction", "Worship & Praise"],
        6: ["Bible Timeline", "Covenant Theology", "Christian Worldview", "Apologetics Intro"],
        7: ["Systematic Theology Basics", "Church History", "Doctrine Fundamentals", "Christian Ethics"],
        8: ["Theology Deep Dive", "Reformation History", "Biblical Interpretation", "Spiritual Disciplines"],
        9: ["Advanced Apologetics", "Philosophy & Faith", "World Religions", "Christian Leadership"],
        10: ["Theology II", "Biblical Languages Intro", "Missions & Evangelism", "Christian Apologetics"],
        11: ["Systematic Theology III", "Biblical Exegesis", "Christian Philosophy", "Ministry Prep"],
        12: ["Advanced Theology", "Hermeneutics", "Apologetics Mastery", "Vocational Ministry"]
    },
    "coin_quest": {
        3: ["Counting Money", "Saving vs Spending", "Needs vs Wants", "Earning Money"],
        4: ["Budgeting Basics", "Making Change", "Banks & Savings", "Giving & Tithing"],
        5: ["Income & Expenses", "Simple Budgets", "Interest Basics", "Financial Goals"],
        6: ["Banking Fundamentals", "Credit vs Debit", "Budgeting Skills", "Earning Strategies"],
        7: ["Financial Planning", "Compound Interest", "Checking Accounts", "Smart Shopping"],
        8: ["Credit Basics", "Loans & Debt", "Building Wealth", "Career & Income"],
        9: ["Personal Finance", "Credit Scores", "Insurance Basics", "Taxes Introduction"],
        10: ["Advanced Budgeting", "Retirement Planning Intro", "Real Estate Basics", "Entrepreneurship"],
        11: ["Investment Basics", "Financial Independence", "College Financing", "Career Planning"],
        12: ["Advanced Personal Finance", "Investment Strategies", "Tax Planning", "Wealth Building"]
    },
    "stock_star": {
        6: ["What Are Stocks?", "Supply & Demand", "Business Basics", "Saving vs Investing"],
        7: ["Stock Market Intro", "Bulls & Bears", "Risk & Reward", "Company Research"],
        8: ["Stock Types", "Market Indices", "Portfolio Basics", "Economic Indicators"],
        9: ["Investment Strategies", "Bonds & Securities", "Diversification", "Market Analysis"],
        10: ["Advanced Investing", "Options & Futures Intro", "Economic Cycles", "Global Markets"],
        11: ["Portfolio Management", "Technical Analysis", "Fundamental Analysis", "Investment Psychology"],
        12: ["Advanced Trading", "Alternative Investments", "Financial Planning", "Wealth Management"]
    },
    "truth_forge": {
        6: ["What is Truth?", "Logic Basics", "Critical Thinking", "Christian Worldview"],
        7: ["Arguments & Evidence", "Logical Fallacies", "Defending Your Faith", "Science & Faith"],
        8: ["Philosophy Introduction", "Worldview Comparison", "Moral Reasoning", "Apologetics Methods"],
        9: ["Classical Apologetics", "Presuppositional Apologetics", "Evidential Apologetics", "Cultural Engagement"],
        10: ["Advanced Philosophy", "Atheism & Skepticism", "World Religions", "Christian Philosophers"],
        11: ["Theological Apologetics", "Historical Jesus", "Problem of Evil", "Resurrection Evidence"],
        12: ["Apologetics Mastery", "Contemporary Issues", "Postmodernism", "Public Defense"]
    },
    "terra_nova": {
        1: ["Maps & Globes", "Continents & Oceans", "My Community", "Landforms"],
        2: ["US Geography", "State Capitals", "Climate Zones", "Natural Resources"],
        3: ["World Geography", "Countries & Cultures", "Physical Features", "Human Geography"],
        4: ["North America Deep Dive", "South America", "Europe", "Africa"],
        5: ["Asia", "Australia & Oceania", "Antarctica", "World Cultures"],
        6: ["Geographic Regions", "Population & Migration", "Economic Geography", "Political Geography"],
        7: ["Physical Geography", "Climate & Biomes", "Natural Disasters", "Environmental Issues"],
        8: ["Human Geography", "Urbanization", "Cultural Geography", "Geopolitics"],
        9: ["Regional Studies", "Development Geography", "Globalization", "Geographic Technologies"],
        10: ["Advanced Physical Geography", "Cultural Landscapes", "Political Borders", "Resource Management"],
        11: ["Geographic Analysis", "Spatial Patterns", "Geographic Research", "Global Issues"],
        12: ["AP Human Geography Topics", "Geographic Thought", "Advanced GIS", "Sustainability"]
    },
    "power_grid": {
        6: ["Goal Setting", "Time Management", "Study Skills", "Responsibility"],
        7: ["Career Exploration", "Communication Skills", "Teamwork", "Problem Solving"],
        8: ["Leadership Basics", "Financial Literacy", "Work Ethic", "Digital Citizenship"],
        9: ["Career Planning", "Resume Building", "Interview Skills", "Networking"],
        10: ["College Preparation", "SAT/ACT Prep", "Scholarship Research", "Career Paths"],
        11: ["College Applications", "Career Readiness", "Professional Skills", "Life Planning"],
        12: ["Transition to Adulthood", "Job Search Strategies", "Financial Independence", "Life Skills Mastery"]
    },
    "respect_realm": {
        1: ["Kindness", "Sharing", "Following Rules", "Good Manners"],
        2: ["Honesty", "Respect for Others", "Self-Control", "Gratitude"],
        3: ["Responsibility", "Perseverance", "Empathy", "Courage"],
        4: ["Integrity", "Compassion", "Patience", "Forgiveness"],
        5: ["Leadership Qualities", "Citizenship", "Diligence", "Humility"],
        6: ["Character Building", "Moral Reasoning", "Service & Volunteering", "Conflict Resolution"],
        7: ["Emotional Intelligence", "Decision Making", "Peer Pressure", "Self-Discipline"],
        8: ["Identity & Values", "Social Responsibility", "Media Discernment", "Healthy Relationships"],
        9: ["Ethics & Morality", "Critical Choices", "Influence & Impact", "Personal Growth"],
        10: ["Character Leadership", "Moral Courage", "Social Justice", "Purpose & Calling"],
        11: ["Advanced Ethics", "Cultural Competence", "Servant Leadership", "Legacy Building"],
        12: ["Character Mastery", "Life Philosophy", "Mentoring Others", "Impact Planning"]
    }
}


def get_lessons_for_subject_grade(subject: str, grade: int) -> List[str]:
    """Get list of lesson topics for a subject and grade"""
    if subject not in LESSON_TOPICS:
        return []
    if grade not in LESSON_TOPICS[subject]:
        return []
    return LESSON_TOPICS[subject][grade]


def generate_student_lesson(
    subject: str,
    grade: int,
    topic: str,
    character: str = "everly"
) -> Dict:
    """
    Generate an engaging, interactive lesson for a student.

    Args:
        subject: Subject key (e.g., "num_forge")
        grade: Grade level (1-12)
        topic: Lesson topic/title
        character: AI mentor character

    Returns:
        Dictionary containing lesson content and structure
    """
    from subjects_config import get_subject

    subject_config = get_subject(subject)
    subject_name = subject_config.get("name", subject) if subject_config else subject

    # Character personalities for lesson delivery
    character_styles = {
        "everly": "enthusiastic warrior-princess who makes learning an adventure",
        "jasmine": "curious explorer who discovers knowledge through investigation",
        "lio": "tactical space agent who breaks down complex concepts strategically",
        "theo": "wise scholar who explains deep concepts with patience and clarity",
        "nova": "inventive engineer who builds understanding through hands-on discovery"
    }

    character_style = character_styles.get(character, character_styles["nova"])

    client = get_client()

    prompt = f"""You are {character.title()}, a {character_style}, teaching a Grade {grade} student.

Create an engaging, interactive lesson on "{topic}" for {subject_name}.

IMPORTANT GUIDELINES:
- Make it FUN and ENGAGING (use stories, examples, analogies)
- Grade {grade} appropriate language and complexity
- Break complex ideas into simple steps
- Include real-world examples students can relate to
- Use encouraging, supportive tone
- End with thought-provoking questions for discussion

Generate the lesson in this EXACT JSON format (valid JSON only, no markdown):

{{
  "title": "{topic}",
  "hook": "An engaging opening that captures attention and relates to student's life (2-3 sentences)",
  "learning_goal": "What the student will be able to do after this lesson",
  "explanation": "Main teaching content broken into clear sections with examples (use \\n\\n for paragraphs)",
  "key_concepts": [
    "Important concept 1",
    "Important concept 2",
    "Important concept 3"
  ],
  "examples": [
    {{
      "scenario": "Real-world example or problem",
      "solution": "How to solve it or apply the concept"
    }},
    {{
      "scenario": "Another example",
      "solution": "Solution explanation"
    }}
  ],
  "try_it": {{
    "instruction": "A simple practice problem or activity for the student to try",
    "hint": "A helpful hint if they get stuck"
  }},
  "discussion_questions": [
    "Thought-provoking question 1 about the concept",
    "Thought-provoking question 2 about real-world application",
    "Thought-provoking question 3 about deeper understanding"
  ],
  "summary": "Quick recap of main points (2-3 sentences)",
  "encouragement": "Encouraging closing message from {character.title()}"
}}

Make it grade {grade} appropriate, engaging, and educational!"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": f"You are {character.title()}, an enthusiastic AI mentor. Generate engaging lessons in valid JSON format."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=3000,
            timeout=60.0
        )

        response_text = response.choices[0].message.content.strip()

        # Remove markdown code blocks if present
        if response_text.startswith("```"):
            lines = response_text.split("\n")
            response_text = "\n".join(lines[1:-1]) if len(lines) > 2 else response_text
            response_text = response_text.strip()

        lesson_data = json.loads(response_text)

        return {
            "success": True,
            "lesson": lesson_data,
            "subject": subject,
            "grade": grade,
            "character": character
        }

    except json.JSONDecodeError as e:
        print(f"JSON parsing error: {e}")
        return {
            "success": False,
            "error": "Failed to generate lesson. Please try again."
        }
    except Exception as e:
        print(f"Error generating lesson: {e}")
        return {
            "success": False,
            "error": "AI service error. Please try again."
        }


def get_lesson_chat_response(
    lesson_topic: str,
    subject: str,
    grade: int,
    question: str,
    character: str = "everly",
    conversation_history: List[Dict] = None
) -> str:
    """
    Get AI response for follow-up questions about a lesson.

    Args:
        lesson_topic: The lesson topic being discussed
        subject: Subject area
        grade: Student grade level
        question: Student's question
        character: AI mentor character
        conversation_history: Previous conversation messages

    Returns:
        AI response string
    """
    from subjects_config import get_subject

    subject_config = get_subject(subject)
    subject_name = subject_config.get("name", subject) if subject_config else subject

    client = get_client()

    if conversation_history is None:
        conversation_history = []

    system_message = f"""You are {character.title()}, an encouraging AI mentor helping a Grade {grade} student
understand "{lesson_topic}" in {subject_name}.

Guidelines:
- Keep responses clear and grade-appropriate
- Use encouraging, supportive tone
- Break down complex ideas into simple terms
- Provide examples when helpful
- Ask follow-up questions to check understanding
- Praise good questions and effort
- Keep responses concise (2-3 paragraphs max)"""

    messages = [{"role": "system", "content": system_message}]

    # Add conversation history
    for msg in conversation_history:
        messages.append(msg)

    # Add current question
    messages.append({"role": "user", "content": question})

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.7,
            max_tokens=500,
            timeout=30.0
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"Error getting chat response: {e}")
        return "I'm having trouble right now. Please try asking again!"
