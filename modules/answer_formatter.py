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
    """

    sections = {
        "overview": "",
        "key_facts": [],
        "christian_view": "",
        "agreement": [],
        "difference": [],
        "practice": [],
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
            sections["key_facts"] = _normalize_list(content)
        elif "section 3" in label:
            sections["christian_view"] = content
        elif "section 4" in label:
            sections["agreement"] = _normalize_list(content)
        elif "section 5" in label:
            sections["difference"] = _normalize_list(content)
        elif "section 6" in label:
            sections["practice"] = _normalize_list(content)

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
    """

    return {
        "overview": (overview or "").strip(),
        "key_facts": _normalize_list(key_facts),
        "christian_view": (christian_view or "").strip(),
        "agreement": _normalize_list(agreement),
        "difference": _normalize_list(difference),
        "practice": _normalize_list(practice),
        "raw_text": raw_text or "",
    }



