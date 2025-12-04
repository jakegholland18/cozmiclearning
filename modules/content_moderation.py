# modules/content_moderation.py
"""
Content Moderation System for CozmicLearning

Multi-layered safety system to protect students and platform integrity:
1. OpenAI Moderation API - Flag harmful content
2. Keyword filtering - Block inappropriate words/phrases
3. Input validation - Sanitize and limit input
4. Rate limiting - Prevent spam/abuse
5. Activity logging - Track all interactions for review
"""

import os
import re
from datetime import datetime, timedelta
from openai import OpenAI


# -------------------------------------------------------
# OpenAI Moderation API
# -------------------------------------------------------
def check_openai_moderation(text: str) -> dict:
    """
    Use OpenAI's Moderation API to check for policy violations.
    
    Returns dict:
    {
        "flagged": bool,
        "categories": dict of categories that were flagged,
        "category_scores": dict of confidence scores,
        "reason": str description of why it was flagged
    }
    """
    try:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response = client.moderations.create(input=text)
        
        result = response.results[0]
        
        flagged_categories = []
        if result.flagged:
            # Collect which categories were flagged
            for category, is_flagged in result.categories.model_dump().items():
                if is_flagged:
                    flagged_categories.append(category.replace('_', ' ').replace('/', ' or '))
        
        return {
            "flagged": result.flagged,
            "categories": result.categories.model_dump(),
            "category_scores": result.category_scores.model_dump(),
            "reason": ", ".join(flagged_categories) if flagged_categories else None
        }
    
    except Exception as e:
        # If moderation API fails, log error but don't block (fail open)
        print(f"⚠️ Moderation API error: {e}")
        return {
            "flagged": False,
            "categories": {},
            "category_scores": {},
            "reason": None,
            "error": str(e)
        }


# -------------------------------------------------------
# Keyword Filtering
# -------------------------------------------------------
BLOCKED_KEYWORDS = [
    # Profanity (keeping list minimal, relying on OpenAI moderation for comprehensive coverage)
    r'\bf+u+c+k+',
    r'\bs+h+i+t+',
    r'\bb+i+t+c+h+',
    r'\ba+s+s+h+o+l+e+',
    r'\bd+a+m+n+',
    r'\bh+e+l+l+',
    r'\bc+r+a+p+',
    
    # Inappropriate requests (trying to bypass educational purpose)
    r'write.{0,20}essay.{0,20}for.{0,20}me',
    r'do.{0,20}homework.{0,20}for.{0,20}me',
    r'complete.{0,20}assignment',
    r'give.{0,20}me.{0,20}answers',
    r'test.{0,20}answers',
    r'cheat',
    
    # Off-topic abuse
    r'hack',
    r'exploit',
    r'jailbreak',
    r'ignore.{0,20}(previous|above|system).{0,20}(instructions|prompt|rules)',
    r'pretend.{0,20}you.{0,20}are',
    r'act.{0,20}as.{0,20}if',
]

def check_keyword_filter(text: str) -> dict:
    """
    Check text against blocked keyword patterns.
    
    Returns dict:
    {
        "flagged": bool,
        "matched_pattern": str or None,
        "reason": str description
    }
    """
    text_lower = text.lower()
    
    for pattern in BLOCKED_KEYWORDS:
        if re.search(pattern, text_lower, re.IGNORECASE):
            return {
                "flagged": True,
                "matched_pattern": pattern,
                "reason": "Contains inappropriate or blocked content"
            }
    
    return {
        "flagged": False,
        "matched_pattern": None,
        "reason": None
    }


# -------------------------------------------------------
# Input Validation
# -------------------------------------------------------
def validate_input(text: str, max_length: int = 1000) -> dict:
    """
    Validate and sanitize user input.
    
    Returns dict:
    {
        "valid": bool,
        "sanitized_text": str,
        "reason": str if invalid
    }
    """
    if not text or not isinstance(text, str):
        return {
            "valid": False,
            "sanitized_text": "",
            "reason": "Question cannot be empty"
        }
    
    # Remove excessive whitespace
    sanitized = " ".join(text.split())
    
    # Check length
    if len(sanitized) < 3:
        return {
            "valid": False,
            "sanitized_text": sanitized,
            "reason": "Question is too short (minimum 3 characters)"
        }
    
    if len(sanitized) > max_length:
        return {
            "valid": False,
            "sanitized_text": sanitized[:max_length],
            "reason": f"Question is too long (maximum {max_length} characters)"
        }
    
    # Check for spam patterns (repeated characters)
    if re.search(r'(.)\1{20,}', sanitized):
        return {
            "valid": False,
            "sanitized_text": sanitized,
            "reason": "Question contains spam or invalid patterns"
        }
    
    # Check for URL/link spam (basic check)
    if re.search(r'(https?://|www\.)\S+', sanitized, re.IGNORECASE):
        # Allow educational links but flag for review
        pass
    
    return {
        "valid": True,
        "sanitized_text": sanitized,
        "reason": None
    }


# -------------------------------------------------------
# Rate Limiting (Per-Student)
# -------------------------------------------------------
# In-memory storage for rate limiting (production should use Redis/database)
_rate_limit_tracker = {}

def check_rate_limit(student_id: int, max_requests: int = 20, window_minutes: int = 60) -> dict:
    """
    Check if student has exceeded rate limit.
    
    Returns dict:
    {
        "allowed": bool,
        "remaining": int,
        "reset_time": datetime or None
    }
    """
    now = datetime.utcnow()
    window_start = now - timedelta(minutes=window_minutes)
    
    # Initialize or clean old requests
    if student_id not in _rate_limit_tracker:
        _rate_limit_tracker[student_id] = []
    
    # Remove requests outside current window
    _rate_limit_tracker[student_id] = [
        timestamp for timestamp in _rate_limit_tracker[student_id]
        if timestamp > window_start
    ]
    
    current_count = len(_rate_limit_tracker[student_id])
    
    if current_count >= max_requests:
        # Find oldest request to determine reset time
        oldest = min(_rate_limit_tracker[student_id])
        reset_time = oldest + timedelta(minutes=window_minutes)
        
        return {
            "allowed": False,
            "remaining": 0,
            "reset_time": reset_time,
            "reason": f"Rate limit exceeded. Maximum {max_requests} questions per {window_minutes} minutes."
        }
    
    # Add current request
    _rate_limit_tracker[student_id].append(now)
    
    return {
        "allowed": True,
        "remaining": max_requests - current_count - 1,
        "reset_time": None,
        "reason": None
    }


# -------------------------------------------------------
# Master Moderation Function
# -------------------------------------------------------
def moderate_content(text: str, student_id: int = None, context: str = "question") -> dict:
    """
    Run all moderation checks on user input.
    
    Args:
        text: The user's question/message
        student_id: Student ID for rate limiting (optional)
        context: Type of interaction ("question", "chat", "practice")
    
    Returns dict:
    {
        "allowed": bool - Whether content should be processed,
        "flagged": bool - Whether content was flagged (for logging),
        "sanitized_text": str - Cleaned input text,
        "reason": str - Why content was blocked/flagged,
        "moderation_data": dict - Full details for logging
    }
    """
    result = {
        "allowed": True,
        "flagged": False,
        "sanitized_text": text,
        "reason": None,
        "moderation_data": {}
    }
    
    # Step 1: Input validation
    validation = validate_input(text)
    result["moderation_data"]["validation"] = validation
    
    if not validation["valid"]:
        result["allowed"] = False
        result["flagged"] = True
        result["reason"] = validation["reason"]
        return result
    
    result["sanitized_text"] = validation["sanitized_text"]
    
    # Step 2: Rate limiting (if student_id provided)
    if student_id is not None:
        rate_check = check_rate_limit(student_id)
        result["moderation_data"]["rate_limit"] = rate_check
        
        if not rate_check["allowed"]:
            result["allowed"] = False
            result["flagged"] = True
            result["reason"] = rate_check["reason"]
            return result
    
    # Step 3: Keyword filtering
    keyword_check = check_keyword_filter(validation["sanitized_text"])
    result["moderation_data"]["keyword_filter"] = keyword_check
    
    if keyword_check["flagged"]:
        result["allowed"] = False
        result["flagged"] = True
        result["reason"] = "Your question contains inappropriate content. Please ask educational questions only."
        return result
    
    # Step 4: OpenAI Moderation API
    openai_check = check_openai_moderation(validation["sanitized_text"])
    result["moderation_data"]["openai_moderation"] = openai_check
    
    if openai_check["flagged"]:
        result["allowed"] = False
        result["flagged"] = True
        categories = openai_check["reason"] or "policy violations"
        result["reason"] = f"Your question was flagged for: {categories}. Please ask appropriate educational questions."
        return result
    
    # All checks passed
    return result


# -------------------------------------------------------
# Helper: Get flagged reason summary
# -------------------------------------------------------
def get_moderation_summary(moderation_result: dict) -> str:
    """
    Create human-readable summary of moderation result for logging.
    """
    if not moderation_result.get("flagged"):
        return "Passed all checks"
    
    parts = []
    data = moderation_result.get("moderation_data", {})
    
    if data.get("validation", {}).get("valid") is False:
        parts.append(f"Validation: {data['validation'].get('reason')}")
    
    if data.get("rate_limit", {}).get("allowed") is False:
        parts.append("Rate limit exceeded")
    
    if data.get("keyword_filter", {}).get("flagged"):
        parts.append(f"Keyword filter: {data['keyword_filter'].get('matched_pattern')}")
    
    if data.get("openai_moderation", {}).get("flagged"):
        parts.append(f"OpenAI: {data['openai_moderation'].get('reason')}")
    
    return " | ".join(parts) if parts else "Unknown reason"
