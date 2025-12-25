# modules/content_moderation.py
"""
Content moderation for AI Study Buddy using OpenAI Moderation API
"""

import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def moderate_content(text: str) -> dict:
    """
    Check content for inappropriate material using OpenAI Moderation API.

    Args:
        text: The content to moderate

    Returns:
        dict with:
            - flagged (bool): Whether content violates policies
            - categories (dict): Which categories were flagged
            - category_scores (dict): Confidence scores for each category
            - reason (str): Human-readable reason if flagged
    """
    try:
        response = client.moderations.create(input=text)
        result = response.results[0]

        # Build human-readable reason
        reason = None
        if result.flagged:
            flagged_categories = [
                category.replace('/', ' or ').replace('_', ' ').title()
                for category, flagged in result.categories.model_dump().items()
                if flagged
            ]
            reason = f"Flagged for: {', '.join(flagged_categories)}"

        return {
            'flagged': result.flagged,
            'categories': result.categories.model_dump(),
            'category_scores': result.category_scores.model_dump(),
            'reason': reason
        }

    except Exception as e:
        print(f"Moderation API error: {e}")
        # Fail open - don't block if moderation fails
        return {
            'flagged': False,
            'categories': {},
            'category_scores': {},
            'reason': None,
            'error': str(e)
        }


def check_academic_dishonesty(text: str) -> dict:
    """
    Check if content suggests cheating or academic dishonesty.

    Returns:
        dict with:
            - flagged (bool): Whether content suggests cheating
            - reason (str): Why it was flagged
            - keywords (list): Suspicious keywords found
    """
    # Keywords that suggest cheating
    cheating_keywords = [
        'write my essay',
        'do my homework',
        'give me the answer',
        'solve this for me',
        'complete this assignment',
        'write this paper for me',
        'full solution',
        'just tell me the answer'
    ]

    text_lower = text.lower()
    found_keywords = [kw for kw in cheating_keywords if kw in text_lower]

    if found_keywords:
        return {
            'flagged': True,
            'reason': 'Possible academic dishonesty - requesting direct answers',
            'keywords': found_keywords
        }

    return {
        'flagged': False,
        'reason': None,
        'keywords': []
    }


def should_notify_parent(moderation_result: dict, cheating_result: dict) -> bool:
    """
    Determine if parents should be notified based on moderation results.

    Parents are notified for:
    - Violence or threats
    - Sexual content
    - Self-harm content
    - Repeated cheating attempts

    NOT notified for:
    - Mild profanity (handled with warning)
    - Academic questions (even if pushing boundaries)
    """
    if not moderation_result.get('flagged'):
        return False

    categories = moderation_result.get('categories', {})

    # Serious categories that require parent notification
    serious_categories = [
        'violence',
        'violence/graphic',
        'self-harm',
        'self-harm/intent',
        'self-harm/instructions',
        'sexual',
        'sexual/minors'
    ]

    for category in serious_categories:
        if categories.get(category, False):
            return True

    # Also notify for academic dishonesty
    if cheating_result.get('flagged'):
        return True

    return False


def get_moderation_summary(moderation_result: dict) -> str:
    """
    Get a human-readable summary of moderation results.

    Args:
        moderation_result: Result from moderate_content()

    Returns:
        str: Summary like "Safe" or "Flagged for: Violence, Sexual"
    """
    if not moderation_result.get('flagged'):
        return "Safe"

    return moderation_result.get('reason', 'Flagged for policy violation')
