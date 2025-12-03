# modules/answer_formatter.py
"""
Standardizes all AI answers into a clean, structured dictionary
so every subject page displays consistently.

subject.html expects these keys:
overview, key_facts, christian_view, agreement, difference, practice.
"""

import re


def _normalize_list(block):
    """
    Ensure a section is always a list of clean strings.
    Accepts:
    - list
    - string with bullet lines
    - None
    """
    if isinstance(block, list):
        return [str(x).strip() for x in block if str(x).strip()]

    if not block:
        return []

    text = str(block)
    lines = text.splitlines()
    items = []

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Remove leading bullets
        if line.startswith(("-", "•", "*")):
            line = line.lstrip("-•*").strip(" .\t")

        if line:
            items.append(line)

    return items


def parse_into_sections(text: str) -> dict:
    """
    Converts raw AI text using SECTION labels into a structured dictionary.
    Works for ALL helpers.
    All sections are paragraphs (strings), not lists, per CozmicLearning format.
    """

    sections = {
        "overview": "",
        "key_facts": "",
        "christian_view": "",
        "agreement": "",
        "difference": "",
        "practice": "",
    }

    if not text:
        return sections

    pattern = re.compile(r"(SECTION\s+[1-6][^\n]*)", re.IGNORECASE)
    parts = pattern.split(text)

    if len(parts) == 1:
        sections["overview"] = parts[0].strip()
        return sections

    it = iter(parts)
    _ = next(it, "")

    for label_line, content in zip(it, it):
        label = label_line.lower()
        content = content.strip()

        if "section 1" in label:
            sections["overview"] = content
        elif "section 2" in label:
            sections["key_facts"] = content
        elif "section 3" in label:
            sections["christian_view"] = content
        elif "section 4" in label:
            sections["agreement"] = content
        elif "section 5" in label:
            sections["difference"] = content
        elif "section 6" in label:
            sections["practice"] = content

    return sections


def format_answer(
    overview=None,
    key_facts=None,
    christian_view=None,
    agreement=None,
    difference=None,
    practice=None,
    raw_text=None
):
    """
    Normalize sections + return structure subject.html expects.
    If raw_text is provided, parse it into sections automatically.
    All sections are paragraphs (strings), not lists.
    """
    # If raw_text is provided, parse it and merge with any explicitly provided sections
    if raw_text:
        parsed = parse_into_sections(raw_text)
        return {
            "overview": (overview or parsed.get("overview", "")).strip(),
            "key_facts": (key_facts or parsed.get("key_facts", "")).strip(),
            "christian_view": (christian_view or parsed.get("christian_view", "")).strip(),
            "agreement": (agreement or parsed.get("agreement", "")).strip(),
            "difference": (difference or parsed.get("difference", "")).strip(),
            "practice": (practice or parsed.get("practice", "")).strip(),
            "raw_text": raw_text,
        }
    
    # Otherwise use the explicitly provided values
    return {
        "overview": (overview or "").strip(),
        "key_facts": (key_facts or "").strip(),
        "christian_view": (christian_view or "").strip(),
        "agreement": (agreement or "").strip(),
        "difference": (difference or "").strip(),
        "practice": (practice or "").strip(),
        "raw_text": raw_text or "",
    }



