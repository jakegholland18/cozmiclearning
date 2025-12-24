"""
Visual Generator for Assignments and Lessons
Generates ASCII art, Mermaid diagrams, and visual descriptions for educational content
"""

import os
from typing import Dict, Optional, Literal
from modules.ai_client import client

VisualType = Literal["ascii", "mermaid", "description", "none"]


def should_include_visual(question_text: str, topic: str = "") -> bool:
    """
    Determine if a question/lesson would benefit from a visual aid.

    Returns True for math problems, science concepts, geography, timelines, etc.
    """
    visual_keywords = [
        # Math
        "graph", "plot", "coordinate", "triangle", "rectangle", "circle", "shape",
        "diagram", "angle", "perimeter", "area", "volume", "fraction", "slope",

        # Science
        "atom", "molecule", "cell", "ecosystem", "food chain", "water cycle",
        "solar system", "circuit", "force", "motion", "structure",

        # History/Geography
        "timeline", "map", "battle", "route", "territory", "continent",
        "country", "region", "migration", "expansion",

        # General
        "flowchart", "process", "sequence", "comparison", "table", "chart"
    ]

    text_lower = (question_text + " " + topic).lower()
    return any(keyword in text_lower for keyword in visual_keywords)


def detect_visual_type(content: str, subject: str = "") -> VisualType:
    """
    Detect the best type of visual for the content.

    Returns:
        "ascii" - for simple diagrams, math problems, shapes
        "mermaid" - for flowcharts, timelines, graphs, org charts
        "description" - for complex scenes that need description
        "none" - if no visual needed
    """
    content_lower = content.lower()

    # Mermaid is best for:
    mermaid_keywords = [
        "flowchart", "timeline", "sequence", "process", "steps", "flow",
        "organizational", "hierarchy", "relationship", "comparison",
        "before and after", "cause and effect"
    ]

    if any(keyword in content_lower for keyword in mermaid_keywords):
        return "mermaid"

    # ASCII is best for:
    ascii_keywords = [
        "triangle", "rectangle", "square", "circle", "shape", "angle",
        "coordinate", "graph", "plot", "table", "grid", "chart"
    ]

    if any(keyword in content_lower for keyword in ascii_keywords):
        return "ascii"

    # If it seems visual-related but not a good fit for ASCII/Mermaid
    if should_include_visual(content):
        return "description"

    return "none"


def generate_ascii_visual(prompt: str, context: str = "") -> str:
    """
    Generate ASCII art or text-based diagram for a question/concept.

    Args:
        prompt: The question or concept needing visualization
        context: Additional context (subject, grade level, etc.)

    Returns:
        ASCII art diagram as a string
    """
    system_prompt = """You are an expert at creating clear ASCII art diagrams for education.

GUIDELINES:
- Use only standard ASCII characters (no unicode)
- Keep diagrams simple and clear
- Label important parts
- Use consistent spacing and alignment
- Maximum width: 60 characters
- Include a brief caption above the diagram

EXAMPLES:

For a right triangle problem:
```
Right Triangle ABC:
        C
        |\\
        | \\
     6  |  \\  10
        |   \\
        |    \\
        |_____\\
        A   8   B

Angle C = 90°
Find angle A.
```

For a coordinate plane:
```
y-axis
  |
4 |     * (3,4)
  |
2 |  * (1,2)
  |
--+--+--+--+---> x-axis
  0  2  4

Plot these points
```"""

    user_prompt = f"""Create a clear ASCII art diagram for this educational content:

{prompt}

{f"Context: {context}" if context else ""}

Return ONLY the ASCII diagram with a brief caption. Keep it simple and educational."""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3,
            max_tokens=500
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"❌ Error generating ASCII visual: {e}")
        return f"[Visual diagram for: {prompt[:100]}...]"


def generate_mermaid_diagram(prompt: str, context: str = "") -> str:
    """
    Generate Mermaid.js diagram code for flowcharts, timelines, etc.

    Args:
        prompt: The concept/process needing visualization
        context: Additional context

    Returns:
        Mermaid diagram code as a string
    """
    system_prompt = """You are an expert at creating educational diagrams using Mermaid.js syntax.

MERMAID DIAGRAM TYPES:
- flowchart: For processes, decisions, flows
- graph: For relationships, connections
- timeline: For historical events, sequences
- pie: For percentages, proportions

GUIDELINES:
- Use simple, clear labels
- Limit complexity (max 10 nodes)
- Use appropriate shapes for meaning
- Include a title in the diagram

EXAMPLE FLOWCHART:
```mermaid
flowchart TD
    A[Start: Read the problem] --> B{Is it addition?}
    B -->|Yes| C[Add the numbers]
    B -->|No| D[Check if subtraction]
    C --> E[Write your answer]
    D --> F[Subtract the numbers]
    F --> E
```

EXAMPLE TIMELINE:
```mermaid
timeline
    title American Revolution Timeline
    1765 : Stamp Act passed
    1773 : Boston Tea Party
    1775 : Battle of Lexington
    1776 : Declaration of Independence
```"""

    user_prompt = f"""Create a Mermaid diagram for this educational content:

{prompt}

{f"Context: {context}" if context else ""}

Return ONLY the Mermaid code (starting with ```mermaid). Keep it educational and grade-appropriate."""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3,
            max_tokens=800
        )

        result = response.choices[0].message.content.strip()

        # Extract just the mermaid code if wrapped in markdown
        if "```mermaid" in result:
            start = result.find("```mermaid") + 10
            end = result.find("```", start)
            if end > start:
                result = result[start:end].strip()

        return result

    except Exception as e:
        print(f"❌ Error generating Mermaid diagram: {e}")
        return f"graph TD\n    A[{prompt[:50]}...]"


def generate_visual_description(prompt: str, context: str = "") -> str:
    """
    Generate a detailed visual description for complex scenes.

    Use this when ASCII/Mermaid aren't suitable but students need to visualize.
    """
    system_prompt = """You are helping students visualize complex concepts through vivid descriptions.

Create SHORT, clear visual descriptions that help students picture the concept mentally.

Keep descriptions:
- Brief (2-4 sentences max)
- Concrete and specific
- Age-appropriate
- Focused on key visual elements

Example: "Picture a large cell like a tiny factory. The nucleus sits in the center like a control room with DNA blueprints. The mitochondria float around like little power plants, creating energy for the cell to use."
"""

    user_prompt = f"""Create a brief visual description for this educational content:

{prompt}

{f"Context: {context}" if context else ""}

Help students visualize this concept clearly."""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.5,
            max_tokens=300
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"❌ Error generating visual description: {e}")
        return ""


def add_visual_to_question(question_text: str, topic: str = "", subject: str = "", grade: str = "8") -> Dict[str, str]:
    """
    Automatically add appropriate visual aid to a question.

    Returns:
        {
            "visual_type": "ascii" | "mermaid" | "description" | "none",
            "visual_content": "the generated visual content",
            "visual_caption": "brief caption/title for the visual"
        }
    """
    # Check if visual would be helpful
    if not should_include_visual(question_text, topic):
        return {
            "visual_type": "none",
            "visual_content": "",
            "visual_caption": ""
        }

    # Detect best visual type
    visual_type = detect_visual_type(question_text + " " + topic, subject)

    if visual_type == "none":
        return {
            "visual_type": "none",
            "visual_content": "",
            "visual_caption": ""
        }

    context = f"Subject: {subject}, Grade: {grade}, Topic: {topic}"

    # Generate the appropriate visual
    visual_content = ""
    visual_caption = ""

    if visual_type == "ascii":
        visual_content = generate_ascii_visual(question_text, context)
        visual_caption = "Diagram:"

    elif visual_type == "mermaid":
        visual_content = generate_mermaid_diagram(question_text, context)
        visual_caption = "Visual diagram:"

    elif visual_type == "description":
        visual_content = generate_visual_description(question_text, context)
        visual_caption = "Visualize this:"

    return {
        "visual_type": visual_type,
        "visual_content": visual_content,
        "visual_caption": visual_caption
    }


def add_visual_to_lesson(lesson_data: Dict, subject: str = "", grade: int = 8) -> Dict:
    """
    Add visual aids to lesson content where appropriate.

    Modifies the lesson_data dict in place, adding visual fields.

    Returns:
        Updated lesson_data with visual fields added
    """
    # Add visual to explanation if it would help
    if "explanation" in lesson_data:
        explanation = lesson_data["explanation"]
        title = lesson_data.get("title", "")

        if should_include_visual(explanation, title):
            visual = add_visual_to_question(
                f"{title}: {explanation[:500]}",
                topic=title,
                subject=subject,
                grade=str(grade)
            )

            if visual["visual_type"] != "none":
                lesson_data["visual"] = visual

    # Add visuals to examples if they would help
    if "examples" in lesson_data and isinstance(lesson_data["examples"], list):
        for i, example in enumerate(lesson_data["examples"]):
            if isinstance(example, dict) and "scenario" in example:
                scenario = example["scenario"]

                if should_include_visual(scenario):
                    visual = add_visual_to_question(
                        scenario,
                        subject=subject,
                        grade=str(grade)
                    )

                    if visual["visual_type"] != "none":
                        lesson_data["examples"][i]["visual"] = visual

    return lesson_data
