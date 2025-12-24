# Visual Optimization System

## What This Does

Instead of manually testing prompts, this system **automatically**:
1. ✅ Tests visual generation with real scenarios (coordinate planes, triangles, timelines, etc.)
2. ✅ Uses AI to evaluate quality (scores 0-10)
3. ✅ Identifies specific weaknesses
4. ✅ Generates improved prompt recommendations
5. ✅ Saves recommendations for you to review

## How to Use

### Quick Start

```bash
# Run the optimization tool
python3 optimize_visuals.py
```

That's it! The tool will:
- Test 5 different visual scenarios
- Show you the scores for each
- Generate recommendations if scores are below 7/10
- Optionally save a detailed report

### What Gets Tested

1. **Coordinate Plane** (Mermaid) - Quadrants with X/Y axes
2. **Right Triangle** (ASCII) - Triangle with labeled sides
3. **Timeline** (Mermaid) - Historical events in sequence
4. **Fraction Visual** (ASCII) - Visual representation of 3/4
5. **Process Flow** (Mermaid) - Water cycle diagram

### Understanding Scores

- **8-10**: Excellent quality ✅
- **6-7**: Good but could improve ⚠️
- **0-5**: Needs significant work ❌

### After Running

The tool will show you:
- Overall average score
- Specific strengths and weaknesses for each visual type
- Concrete suggestions for improvement
- Improved prompt guidelines (if needed)

### Applying Improvements

If recommendations are generated:
1. Review the suggested improvements
2. Update `modules/visual_generator.py` with the new prompts
3. Re-run `python3 optimize_visuals.py` to verify
4. Repeat until scores are 8+

## Example Output

```
📊 Testing: coordinate_plane
------------------------------------------------------------
Generated Type: mermaid
Expected Type: mermaid
Type Match: ✅

⭐ Score: 7/10

✅ Strengths:
   • Shows all 4 quadrants clearly
   • Clean and readable

❌ Weaknesses:
   • Axes labels could be more prominent
   • Missing example points

💡 Suggestions:
   • Add sample points in each quadrant
   • Use bolder axis labels
```

## Advanced Usage

### Testing Specific Visual Types

Edit `modules/visual_optimizer.py` and modify `VISUAL_TEST_CASES` to add your own test scenarios.

### Adjusting Quality Criteria

Each test case has `quality_criteria` - customize these to match your specific needs.

### Using Different AI Models

The optimizer uses:
- `gpt-4o-mini` for quality evaluation (fast, cheap)
- `gpt-4o` for prompt optimization (better recommendations)

You can adjust these in `visual_optimizer.py` if needed.

## Benefits

✅ **No Manual Testing** - AI does the evaluation
✅ **Objective Scores** - Consistent 0-10 ratings
✅ **Specific Feedback** - Not just "bad" but "why" and "how to fix"
✅ **Continuous Improvement** - Run anytime to verify changes
✅ **Cost Effective** - Uses mini model for most work

## Workflow

```
┌─────────────────┐
│ Run optimizer   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Get scores &    │
│ recommendations │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Update prompts  │
│ in generator.py │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Re-run to verify│
└────────┬────────┘
         │
         ▼
    Score 8+? ───Yes──> Done! ✅
         │
         No
         │
         └──────> (Loop back)
```

## Tips

1. **Run before major changes** - Establish baseline scores
2. **Run after prompt updates** - Verify improvements
3. **Check the report file** - Detailed analysis saved for review
4. **Focus on lowest scores first** - Biggest impact
5. **Test edge cases** - Add your own test scenarios

## Cost

Each optimization run costs approximately:
- ~5 API calls to GPT-4o-mini ($0.01)
- ~2 API calls to GPT-4o ($0.05)
- **Total: ~$0.06 per run**

Very affordable for automated quality assurance!
