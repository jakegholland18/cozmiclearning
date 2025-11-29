def format_answer(overview, key_facts, christian_view, agreement, difference, practice):
    """
    Returns the unified answer format used by subject.html.
    All helpers will call this.
    """
    return {
        "overview": overview,
        "key_facts": key_facts,
        "christian_view": christian_view,
        "agreement": agreement,
        "difference": difference,
        "practice": practice
    }
