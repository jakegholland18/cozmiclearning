"""
Generate expanded question banks for arcade games.
Run this script once to generate 100+ questions per difficulty level for each game type.
"""

from modules.shared_ai import get_client
import json

def generate_science_questions(difficulty='easy', count=100):
    """Generate science quiz questions"""

    difficulty_params = {
        'easy': '3rd-5th grade basic science concepts',
        'medium': '6th-8th grade intermediate science topics',
        'hard': '9th-12th grade advanced science and physics'
    }

    prompt = f"""Generate {count} multiple choice science questions for {difficulty_params[difficulty]}.

REQUIREMENTS:
1. Questions should be factual, educational, and age-appropriate
2. Each question needs exactly 4 answer options (one correct, three incorrect)
3. Incorrect options should be plausible but clearly wrong
4. Cover diverse topics: biology, chemistry, physics, earth science, astronomy
5. Vary question difficulty within the level
6. Make distractors match the format/length of correct answers

OUTPUT FORMAT (JSON array):
[
  {{
    "question": "What is H2O commonly known as?",
    "answer": "water",
    "options": ["water", "oxygen", "hydrogen", "salt"]
  }},
  ...
]

Return ONLY the JSON array, no other text."""

    client = get_client()
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an educational quiz generator. Return only valid JSON."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.8
    )

    return json.loads(response.choices[0].message.content)


def generate_geography_questions(difficulty='easy', count=100):
    """Generate geography quiz questions"""

    difficulty_params = {
        'easy': '3rd-5th grade basic geography (continents, oceans, major countries)',
        'medium': '6th-8th grade intermediate geography (capitals, regions, landmarks)',
        'hard': '9th-12th grade advanced geography (geopolitics, climate zones, topography)'
    }

    prompt = f"""Generate {count} multiple choice geography questions for {difficulty_params[difficulty]}.

REQUIREMENTS:
1. Questions should be factual, educational, and age-appropriate
2. Each question needs exactly 4 answer options (one correct, three incorrect)
3. Cover: countries, capitals, continents, oceans, landmarks, rivers, mountains
4. Include world geography, not just one region
5. Make distractors plausible locations or features

OUTPUT FORMAT (JSON array):
[
  {{
    "question": "What is the capital of France?",
    "answer": "paris",
    "options": ["paris", "london", "berlin", "madrid"]
  }},
  ...
]

Return ONLY the JSON array, no other text."""

    client = get_client()
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an educational quiz generator. Return only valid JSON."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.8
    )

    return json.loads(response.choices[0].message.content)


def generate_history_questions(difficulty='easy', count=100):
    """Generate history quiz questions"""

    difficulty_params = {
        'easy': '3rd-5th grade basic history (famous people, major events, simple dates)',
        'medium': '6th-8th grade intermediate history (historical periods, world events, cause-effect)',
        'hard': '9th-12th grade advanced history (complex events, analysis, historical movements)'
    }

    prompt = f"""Generate {count} multiple choice history questions for {difficulty_params[difficulty]}.

REQUIREMENTS:
1. Questions should be factual, educational, and age-appropriate
2. Each question needs exactly 4 answer options (one correct, three incorrect)
3. Cover: world history, American history, ancient civilizations, modern history
4. Include diverse perspectives and global events
5. From a Christian worldview, present history truthfully

OUTPUT FORMAT (JSON array):
[
  {{
    "question": "Who was the first president of the United States?",
    "answer": "george washington",
    "options": ["george washington", "thomas jefferson", "john adams", "benjamin franklin"]
  }},
  ...
]

Return ONLY the JSON array, no other text."""

    client = get_client()
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an educational quiz generator. Return only valid JSON."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.8
    )

    return json.loads(response.choices[0].message.content)


if __name__ == "__main__":
    print("Generating expanded question banks...")
    print("\nThis will take a few minutes and cost approximately $0.50 in API calls.")
    print("Generated questions will be saved to question_banks.json")

    response = input("\nProceed? (y/n): ")
    if response.lower() != 'y':
        print("Cancelled.")
        exit()

    all_questions = {}

    # Generate science questions
    print("\nGenerating science questions...")
    all_questions['science'] = {
        'easy': generate_science_questions('easy', 100),
        'medium': generate_science_questions('medium', 100),
        'hard': generate_science_questions('hard', 100)
    }
    print("✓ Science questions complete")

    # Generate geography questions
    print("\nGenerating geography questions...")
    all_questions['geography'] = {
        'easy': generate_geography_questions('easy', 100),
        'medium': generate_geography_questions('medium', 100),
        'hard': generate_geography_questions('hard', 100)
    }
    print("✓ Geography questions complete")

    # Generate history questions
    print("\nGenerating history questions...")
    all_questions['history'] = {
        'easy': generate_history_questions('easy', 100),
        'medium': generate_history_questions('medium', 100),
        'hard': generate_history_questions('hard', 100)
    }
    print("✓ History questions complete")

    # Save to file
    with open('question_banks.json', 'w') as f:
        json.dump(all_questions, f, indent=2)

    print("\n✅ All question banks generated successfully!")
    print("Total questions generated:", sum(len(q) for subject in all_questions.values() for q in subject.values()))
    print("\nNext steps:")
    print("1. Review question_banks.json")
    print("2. Copy question sets into arcade_helper.py")
    print("3. Delete this script and question_banks.json")
