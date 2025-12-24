"""
PowerGrid Study Tools - Flashcard and Quiz Generation

This module provides AI-powered study tools that generate flashcards
and practice quizzes from PowerGrid study guides.
"""

from modules.ai_helper import powergrid_master_ai


def generate_flashcards(study_guide_text, subject, topic, grade_level, count=10):
    """
    Generate flashcards from study guide content using AI.

    Args:
        study_guide_text: The full study guide content
        subject: The subject area (e.g., "math", "science")
        topic: The specific topic being studied
        grade_level: Student's grade level
        count: Number of flashcards to generate (default 10)

    Returns:
        List of flashcard dictionaries with 'term' and 'definition' keys
    """

    prompt = f"""
Based on this study guide content, create {count} high-quality flashcards for a grade {grade_level} student.

STUDY GUIDE:
{study_guide_text[:3000]}

FLASHCARD REQUIREMENTS:
- Create exactly {count} flashcards
- Focus on the MOST IMPORTANT concepts, terms, and facts
- Terms should be clear and concise (2-8 words)
- Definitions should be student-friendly and easy to understand (1-2 sentences)
- Cover different parts of the study guide (don't cluster on one section)
- Include a mix of vocabulary terms, key concepts, and important facts
- Avoid overly simple or overly complex cards

FORMAT YOUR RESPONSE EXACTLY LIKE THIS (one flashcard per line):
TERM: [concise term or question] | DEFINITION: [clear, student-friendly answer]

EXAMPLE OUTPUT:
TERM: Photosynthesis | DEFINITION: The process by which plants use sunlight, water, and carbon dioxide to create oxygen and energy in the form of sugar.
TERM: What are the reactants in photosynthesis? | DEFINITION: Carbon dioxide (CO2), water (H2O), and sunlight are the reactants that plants need for photosynthesis.

NOW CREATE THE FLASHCARDS:
"""

    # Call PowerGrid AI
    response = powergrid_master_ai(prompt, grade_level, character="Study Buddy")

    # Parse the response
    flashcards = []

    if isinstance(response, dict):
        response_text = response.get("raw_text") or response.get("text") or str(response)
    else:
        response_text = str(response)

    # Extract flashcards from response
    lines = response_text.split('\n')

    for line in lines:
        line = line.strip()
        if 'TERM:' in line and 'DEFINITION:' in line:
            try:
                # Split on | to separate term and definition
                parts = line.split('|')
                if len(parts) >= 2:
                    term_part = parts[0].strip()
                    def_part = parts[1].strip()

                    # Extract the actual term and definition
                    term = term_part.replace('TERM:', '').strip()
                    definition = def_part.replace('DEFINITION:', '').strip()

                    if term and definition:
                        flashcards.append({
                            'term': term,
                            'definition': definition
                        })
            except Exception as e:
                print(f"Error parsing flashcard line: {e}")
                continue

    # If parsing failed, create a fallback set
    if len(flashcards) < 3:
        flashcards = create_fallback_flashcards(study_guide_text, count)

    return flashcards[:count]


def generate_quiz(study_guide_text, subject, topic, grade_level, num_questions=5):
    """
    Generate a practice quiz from study guide content using AI.

    Args:
        study_guide_text: The full study guide content
        subject: The subject area
        topic: The specific topic
        grade_level: Student's grade level
        num_questions: Number of questions to generate (default 5)

    Returns:
        List of question dictionaries with question, options, correct_answer, and explanation
    """

    prompt = f"""
Based on this study guide content, create {num_questions} multiple-choice practice questions for a grade {grade_level} student.

STUDY GUIDE:
{study_guide_text[:3000]}

QUIZ REQUIREMENTS:
- Create exactly {num_questions} multiple-choice questions
- Each question should have 4 answer options (A, B, C, D)
- Questions should test understanding, not just memorization
- Cover different parts of the study guide
- Include a mix of difficulty levels
- Questions should be clear and unambiguous
- Provide a brief explanation for the correct answer

FORMAT YOUR RESPONSE EXACTLY LIKE THIS:

QUESTION 1:
Q: [Clear, specific question]
A) [First option]
B) [Second option]
C) [Third option]
D) [Fourth option]
CORRECT: [A, B, C, or D]
EXPLANATION: [Brief explanation of why this is correct]

QUESTION 2:
[Same format...]

EXAMPLE:
QUESTION 1:
Q: What is the primary function of chlorophyll in plants?
A) To store energy
B) To absorb light energy for photosynthesis
C) To transport water
D) To produce oxygen
CORRECT: B
EXPLANATION: Chlorophyll is the green pigment in plants that absorbs light energy (mainly from the sun) which is then used in the process of photosynthesis.

NOW CREATE THE QUIZ:
"""

    # Call PowerGrid AI
    response = powergrid_master_ai(prompt, grade_level, character="Quiz Master")

    # Parse the response
    questions = []

    if isinstance(response, dict):
        response_text = response.get("raw_text") or response.get("text") or str(response)
    else:
        response_text = str(response)

    # Parse questions from response
    current_question = None
    lines = response_text.split('\n')

    for line in lines:
        line = line.strip()

        if line.startswith('QUESTION'):
            if current_question and current_question.get('question'):
                questions.append(current_question)
            current_question = {
                'options': [],
                'question': '',
                'correct_answer': '',
                'explanation': ''
            }
        elif line.startswith('Q:') and current_question is not None:
            current_question['question'] = line[2:].strip()
        elif line.startswith(('A)', 'B)', 'C)', 'D)')) and current_question is not None:
            current_question['options'].append(line.strip())
        elif line.startswith('CORRECT:') and current_question is not None:
            correct = line.replace('CORRECT:', '').strip()
            current_question['correct_answer'] = correct[0] if correct else 'A'
        elif line.startswith('EXPLANATION:') and current_question is not None:
            current_question['explanation'] = line.replace('EXPLANATION:', '').strip()

    # Add the last question
    if current_question and current_question.get('question'):
        questions.append(current_question)

    # Validate and clean questions
    valid_questions = []
    for q in questions:
        if (q.get('question') and
            len(q.get('options', [])) == 4 and
            q.get('correct_answer') in ['A', 'B', 'C', 'D'] and
            q.get('explanation')):
            valid_questions.append(q)

    # If parsing failed, create fallback questions
    if len(valid_questions) < 2:
        valid_questions = create_fallback_quiz(study_guide_text, subject, topic, num_questions)

    return valid_questions[:num_questions]


def create_fallback_flashcards(study_guide_text, count):
    """Create simple flashcards by parsing the study guide if AI generation fails"""
    flashcards = []
    lines = study_guide_text.split('\n')

    for line in lines:
        line = line.strip()
        # Look for lines with colons (term: definition pattern)
        if ':' in line and len(line) < 200:
            parts = line.split(':', 1)
            if len(parts) == 2:
                term = parts[0].strip().replace('*', '').replace('#', '')
                definition = parts[1].strip()

                # Skip if too short or looks like a header
                if len(term) > 3 and len(definition) > 10 and len(term) < 100:
                    flashcards.append({
                        'term': term,
                        'definition': definition
                    })

        if len(flashcards) >= count:
            break

    # If still not enough, create generic ones
    if len(flashcards) < 3:
        flashcards = [
            {
                'term': 'Key Concept',
                'definition': 'Review the main concepts in this study guide to create your own flashcards.'
            },
            {
                'term': 'Important Terms',
                'definition': 'Identify the most important vocabulary terms from the material.'
            },
            {
                'term': 'Main Ideas',
                'definition': 'Focus on understanding the central themes and ideas presented.'
            }
        ]

    return flashcards


def create_fallback_quiz(study_guide_text, subject, topic, num_questions):
    """Create a simple fallback quiz if AI generation fails"""
    questions = [
        {
            'question': f'What is the main topic covered in this {subject} study guide?',
            'options': [
                f'A) {topic}',
                'B) General overview',
                'C) Advanced concepts',
                'D) Practice exercises'
            ],
            'correct_answer': 'A',
            'explanation': f'This study guide focuses on {topic}.'
        },
        {
            'question': 'What is the best way to use this study guide?',
            'options': [
                'A) Read it once quickly',
                'B) Review it carefully and take notes on key concepts',
                'C) Skip to the examples only',
                'D) Memorize every word'
            ],
            'correct_answer': 'B',
            'explanation': 'The most effective study method is to review carefully and actively engage with the material by taking notes.'
        }
    ]

    return questions[:num_questions]
