"""
Visual Optimizer - Automatically tests and improves visual generation quality
Uses AI to evaluate generated visuals and refine prompts for better results
"""

import json
from typing import Dict, List, Tuple
from modules.ai_client import client


# Test cases for different visual types
VISUAL_TEST_CASES = {
    "coordinate_plane": {
        "prompt": "Explain the four quadrants of a coordinate plane with x and y axes",
        "subject": "math",
        "grade": "8",
        "expected_type": "mermaid",
        "quality_criteria": [
            "Shows all 4 quadrants clearly labeled",
            "Has visible x and y axes",
            "Indicates positive/negative regions",
            "Clean and easy to read"
        ]
    },
    "right_triangle": {
        "prompt": "A right triangle with sides 3, 4, and 5. Find the area.",
        "subject": "math",
        "grade": "7",
        "expected_type": "ascii",
        "quality_criteria": [
            "Triangle is clearly drawn",
            "All three sides are labeled with lengths",
            "Right angle is visible",
            "Proportions look reasonable"
        ]
    },
    "timeline": {
        "prompt": "Show the major events of World War 2 from 1939-1945",
        "subject": "history",
        "grade": "9",
        "expected_type": "mermaid",
        "quality_criteria": [
            "Events in chronological order",
            "Years are clearly shown",
            "At least 4-5 major events",
            "Easy to follow left to right or top to bottom"
        ]
    },
    "fraction": {
        "prompt": "Visualize the fraction 3/4 to show what it represents",
        "subject": "math",
        "grade": "5",
        "expected_type": "ascii",
        "quality_criteria": [
            "Numerator and denominator clearly separated",
            "Visual shows the division concept",
            "Labels explain what each part means",
            "Simple and grade-appropriate"
        ]
    },
    "process_flow": {
        "prompt": "Show the steps of the water cycle: evaporation, condensation, precipitation",
        "subject": "science",
        "grade": "6",
        "expected_type": "mermaid",
        "quality_criteria": [
            "All three stages shown",
            "Arrows show the flow/cycle",
            "Clear labels for each stage",
            "Forms a complete cycle"
        ]
    }
}


def evaluate_visual_quality(
    visual_content: str,
    visual_type: str,
    prompt: str,
    quality_criteria: List[str]
) -> Dict:
    """
    Use AI to evaluate the quality of a generated visual.

    Returns a score (0-10) and specific feedback.
    """
    system_prompt = """You are an expert at evaluating educational visual aids.
Rate the quality of visual diagrams on a scale of 0-10 based on:
- Clarity and readability
- Educational value
- Technical correctness
- Appropriate for students

Be honest and critical - we want to improve these visuals."""

    criteria_text = "\n".join([f"- {c}" for c in quality_criteria])

    user_prompt = f"""Evaluate this {visual_type.upper()} visual for educational use:

ORIGINAL QUESTION/TOPIC:
{prompt}

GENERATED VISUAL:
{visual_content}

QUALITY CRITERIA TO CHECK:
{criteria_text}

Please provide:
1. Overall score (0-10)
2. What works well
3. What needs improvement
4. Specific suggestions for better results

Format your response as JSON:
{{
    "score": <number 0-10>,
    "strengths": ["strength 1", "strength 2"],
    "weaknesses": ["weakness 1", "weakness 2"],
    "suggestions": ["suggestion 1", "suggestion 2"]
}}"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.2,
            response_format={"type": "json_object"}
        )

        result = json.loads(response.choices[0].message.content)
        return result

    except Exception as e:
        print(f"❌ Error evaluating visual: {e}")
        return {
            "score": 0,
            "strengths": [],
            "weaknesses": ["Could not evaluate"],
            "suggestions": []
        }


def generate_improved_prompt(
    original_prompt: str,
    visual_type: str,
    weaknesses: List[str],
    suggestions: List[str]
) -> str:
    """
    Generate an improved system prompt based on evaluation feedback.
    """
    system_prompt = """You are an expert at crafting AI prompts for visual generation.
Based on weaknesses and suggestions, improve the system prompt to generate better visuals."""

    user_prompt = f"""We're generating {visual_type} visuals for education, but they have quality issues.

WEAKNESSES IDENTIFIED:
{chr(10).join([f"- {w}" for w in weaknesses])}

IMPROVEMENT SUGGESTIONS:
{chr(10).join([f"- {s}" for s in suggestions])}

Generate an improved set of guidelines and examples for the system prompt.
Focus on specific, actionable improvements.

Return your response as a clear set of guidelines."""

    try:
        response = client.chat.completions.create(
            model="gpt-4o",  # Use stronger model for prompt optimization
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3
        )

        return response.choices[0].message.content

    except Exception as e:
        print(f"❌ Error generating improved prompt: {e}")
        return ""


def run_visual_optimization_tests() -> Dict:
    """
    Run all test cases and generate a comprehensive report.
    Returns optimization recommendations.
    """
    from modules.visual_generator import add_visual_to_question

    print("🧪 Running Visual Optimization Tests...\n")
    print("=" * 60)

    results = {
        "ascii": {"scores": [], "feedback": []},
        "mermaid": {"scores": [], "feedback": []},
        "overall": {"total_score": 0, "test_count": 0}
    }

    for test_name, test_case in VISUAL_TEST_CASES.items():
        print(f"\n📊 Testing: {test_name}")
        print("-" * 60)

        # Generate visual
        visual_data = add_visual_to_question(
            question_text=test_case["prompt"],
            topic=test_name,
            subject=test_case["subject"],
            grade=test_case["grade"]
        )

        visual_type = visual_data["visual_type"]
        visual_content = visual_data["visual_content"]

        print(f"Generated Type: {visual_type}")
        print(f"Expected Type: {test_case['expected_type']}")

        # Check if type matches expectation
        type_match = visual_type == test_case["expected_type"]
        print(f"Type Match: {'✅' if type_match else '❌'}")

        if visual_type == "none":
            print("⚠️  No visual generated - skipping evaluation")
            continue

        # Evaluate quality
        print(f"\n📝 Visual Content Preview:")
        preview = visual_content[:200] + "..." if len(visual_content) > 200 else visual_content
        print(preview)

        print(f"\n🔍 Evaluating quality...")
        evaluation = evaluate_visual_quality(
            visual_content,
            visual_type,
            test_case["prompt"],
            test_case["quality_criteria"]
        )

        score = evaluation.get("score", 0)
        print(f"\n⭐ Score: {score}/10")

        if evaluation.get("strengths"):
            print("\n✅ Strengths:")
            for s in evaluation["strengths"]:
                print(f"   • {s}")

        if evaluation.get("weaknesses"):
            print("\n❌ Weaknesses:")
            for w in evaluation["weaknesses"]:
                print(f"   • {w}")

        if evaluation.get("suggestions"):
            print("\n💡 Suggestions:")
            for s in evaluation["suggestions"]:
                print(f"   • {s}")

        # Store results
        results[visual_type]["scores"].append(score)
        results[visual_type]["feedback"].append({
            "test": test_name,
            "evaluation": evaluation
        })
        results["overall"]["total_score"] += score
        results["overall"]["test_count"] += 1

        print("=" * 60)

    # Calculate averages
    print("\n\n📈 SUMMARY REPORT")
    print("=" * 60)

    for vtype in ["ascii", "mermaid"]:
        if results[vtype]["scores"]:
            avg_score = sum(results[vtype]["scores"]) / len(results[vtype]["scores"])
            print(f"\n{vtype.upper()} Average Score: {avg_score:.1f}/10")

            # Collect all weaknesses and suggestions
            all_weaknesses = []
            all_suggestions = []
            for feedback in results[vtype]["feedback"]:
                all_weaknesses.extend(feedback["evaluation"].get("weaknesses", []))
                all_suggestions.extend(feedback["evaluation"].get("suggestions", []))

            if all_weaknesses:
                print(f"\nCommon Issues:")
                for w in set(all_weaknesses[:5]):  # Show top 5 unique
                    print(f"   • {w}")

    if results["overall"]["test_count"] > 0:
        overall_avg = results["overall"]["total_score"] / results["overall"]["test_count"]
        print(f"\n🎯 Overall Average Score: {overall_avg:.1f}/10")

        if overall_avg >= 8:
            print("✅ Visual quality is EXCELLENT!")
        elif overall_avg >= 6:
            print("⚠️  Visual quality is GOOD but could be improved")
        else:
            print("❌ Visual quality needs SIGNIFICANT improvement")

    print("\n" + "=" * 60)

    return results


def generate_optimization_recommendations(results: Dict) -> str:
    """
    Generate specific recommendations for improving visual_generator.py
    """
    recommendations = []

    for vtype in ["ascii", "mermaid"]:
        if not results[vtype]["scores"]:
            continue

        avg_score = sum(results[vtype]["scores"]) / len(results[vtype]["scores"])

        if avg_score < 7:
            # Collect feedback
            all_weaknesses = []
            all_suggestions = []
            for feedback in results[vtype]["feedback"]:
                all_weaknesses.extend(feedback["evaluation"].get("weaknesses", []))
                all_suggestions.extend(feedback["evaluation"].get("suggestions", []))

            # Generate improved prompt
            if all_weaknesses or all_suggestions:
                improved_guidelines = generate_improved_prompt(
                    f"{vtype} visual generation",
                    vtype,
                    list(set(all_weaknesses)),
                    list(set(all_suggestions))
                )

                recommendations.append({
                    "type": vtype,
                    "current_score": avg_score,
                    "improved_guidelines": improved_guidelines
                })

    return recommendations


if __name__ == "__main__":
    print("\n🚀 Visual Optimization System")
    print("Testing visual generation quality and providing improvements\n")

    # Run tests
    results = run_visual_optimization_tests()

    # Generate recommendations
    print("\n\n💡 OPTIMIZATION RECOMMENDATIONS")
    print("=" * 60)

    recommendations = generate_optimization_recommendations(results)

    if recommendations:
        for rec in recommendations:
            print(f"\n📝 Recommended improvements for {rec['type'].upper()}:")
            print(f"Current Average Score: {rec['current_score']:.1f}/10")
            print(f"\nImproved Guidelines:\n{rec['improved_guidelines']}")
            print("\n" + "-" * 60)
    else:
        print("\n✅ No major improvements needed - quality is good!")

    print("\n✨ Optimization complete!")
