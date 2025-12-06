"""
AI-powered lesson plan generation for homeschool parents
Generates comprehensive, structured lesson plans using OpenAI
"""

import os
import json
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
    Generate a comprehensive lesson plan using OpenAI.

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

    # Import OpenAI client using shared module
    from modules.shared_ai import get_client
    client = get_client()

    # Build the prompt
    prompt = f"""You are an expert homeschool curriculum designer. Create a comprehensive, engaging lesson plan for a homeschool parent teaching their own child.

IMPORTANT: This parent will be implementing the lesson themselves - they don't have access to worksheets, textbooks, or printed materials unless you specifically tell them what to create. Focus on practical, actionable activities that can be done with common household items or simple prep.

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
  "assessment": "Practical ways for the parent to assess understanding during and after the lesson (verbal questions, observations, simple tasks - no worksheets)",
  "homework": "Suggested practice activities to reinforce learning (be specific about what the student should do)",
  "extensions": "Specific ideas for extension activities for advanced students or deeper exploration"{"," + '"biblical_integration": "Relevant Bible verses and how they connect to this topic"' if biblical_integration else ""}
}}

Make it age-appropriate for grade {grade}, engaging, and practical for a homeschool setting."""

    try:
        # Use OpenAI Chat Completions API with timeout
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an expert homeschool curriculum designer. Generate comprehensive, engaging lesson plans in valid JSON format."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=4096,
            timeout=60.0  # 60 second timeout
        )

        # Extract JSON from response
        response_text = response.choices[0].message.content.strip()

        # Remove markdown code blocks if present
        if response_text.startswith("```"):
            lines = response_text.split("\n")
            # Remove first line (```json or ```) and last line (```)
            response_text = "\n".join(lines[1:-1]) if len(lines) > 2 else response_text
            response_text = response_text.strip()

        # Parse JSON
        lesson_data = json.loads(response_text)

        return {
            "success": True,
            "lesson": lesson_data
        }

    except json.JSONDecodeError as e:
        error_msg = f"JSON parsing error: {str(e)}"
        print(error_msg)
        try:
            print(f"Response was: {response_text[:500]}...")  # Log first 500 chars
        except:
            pass
        return {
            "success": False,
            "error": "Failed to parse AI response. Please try again."
        }
    except Exception as e:
        error_msg = f"Error generating lesson plan: {str(e)}"
        print(error_msg)
        return {
            "success": False,
            "error": "AI service error. Please try again."
        }
