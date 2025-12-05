"""
AI-powered lesson plan generation for homeschool parents
Generates comprehensive, structured lesson plans using Claude
"""

import anthropic
import os
from typing import Dict, List, Optional


def generate_lesson_plan(
    title: str,
    topic: str,
    subject: str,
    grade: str,
    duration: int = 60,
    biblical_integration: bool = False,
    hands_on: bool = True
) -> Dict:
    """
    Generate a comprehensive lesson plan using Claude AI.

    Args:
        title: Lesson title
        topic: Topic/theme to teach
        subject: Subject area (math, science, history, etc.)
        grade: Grade level (K, 1-12)
        duration: Lesson duration in minutes
        biblical_integration: Include Bible verses and principles
        hands_on: Prefer hands-on activities

    Returns:
        Dictionary containing structured lesson plan data
    """

    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    # Build the prompt
    prompt = f"""You are an expert homeschool curriculum designer. Create a comprehensive, engaging lesson plan for:

**Title:** {title}
**Topic:** {topic}
**Subject:** {subject.title()}
**Grade Level:** {grade}
**Duration:** {duration} minutes
**Preferences:** {"Include Biblical integration. " if biblical_integration else ""}{"Focus on hands-on, experiential learning." if hands_on else ""}

Generate a complete lesson plan in the following JSON format (respond with ONLY valid JSON, no markdown code blocks):

{{
  "objectives": [
    "Clear, measurable learning objective 1",
    "Clear, measurable learning objective 2",
    "Clear, measurable learning objective 3"
  ],
  "materials": [
    "Material 1 needed",
    "Material 2 needed",
    "Material 3 needed"
  ],
  "activities": [
    {{
      "section": "Introduction/Hook",
      "duration": 10,
      "description": "Engaging activity to introduce the topic",
      "instructions": "Step-by-step teacher instructions"
    }},
    {{
      "section": "Direct Instruction",
      "duration": 15,
      "description": "Core teaching content",
      "instructions": "What to teach and how"
    }},
    {{
      "section": "Guided Practice",
      "duration": 20,
      "description": "Students practice with guidance",
      "instructions": "Activity details and facilitation tips"
    }},
    {{
      "section": "Independent Work",
      "duration": 10,
      "description": "Students apply learning independently",
      "instructions": "Assignment or task details"
    }},
    {{
      "section": "Closure/Assessment",
      "duration": 5,
      "description": "Review and assess understanding",
      "instructions": "How to wrap up and check for understanding"
    }}
  ],
  "discussion_questions": [
    "Thought-provoking question 1",
    "Thought-provoking question 2",
    "Thought-provoking question 3",
    "Thought-provoking question 4",
    "Thought-provoking question 5"
  ],
  "assessment": "Description of how to assess student understanding (formative and summative ideas)",
  "homework": "Suggested homework or practice activities to reinforce learning",
  "extensions": "Ideas for extension activities for advanced students or deeper exploration"{"," + '"biblical_integration": "Relevant Bible verses and how they connect to this topic"' if biblical_integration else ""}
}}

Make it age-appropriate for grade {grade}, engaging, and practical for a homeschool setting."""

    try:
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=4000,
            temperature=0.7,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        # Extract JSON from response
        response_text = message.content[0].text.strip()

        # Remove markdown code blocks if present
        if response_text.startswith("```"):
            lines = response_text.split("\n")
            response_text = "\n".join(lines[1:-1]) if len(lines) > 2 else response_text

        # Parse JSON
        import json
        lesson_data = json.loads(response_text)

        return {
            "success": True,
            "lesson": lesson_data
        }

    except Exception as e:
        print(f"Error generating lesson plan: {e}")
        return {
            "success": False,
            "error": str(e)
        }
