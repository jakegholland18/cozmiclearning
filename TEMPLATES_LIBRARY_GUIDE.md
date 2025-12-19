# Assignment Templates Library - Implementation Guide

## Overview

The Assignment Templates Library allows teachers to quickly create assignments from pre-built, curriculum-aligned templates instead of starting from scratch. This dramatically reduces prep time and ensures high-quality assignments.

## Features Implemented

### 1. **Template Seed System**
- Created 6 starter templates covering Math, Science, Reading, Writing, and Money
- Templates organized by subject and grade level
- Each template includes:
  - Complete questions with answers, hints, and explanations
  - Differentiation mode recommendations
  - Estimated completion time
  - Skill focus tags
  - Standards alignment (CCSS, NGSS)

### 2. **Admin Seeding Endpoint**
**Route:** `/admin/seed-templates`

**Functionality:**
- Scans `templates_seed/templates/` directory for JSON files
- Loads templates into the database as system templates
- Checks for duplicates (skips existing templates)
- Provides detailed output of created/skipped/error templates
- Returns summary statistics

**Access:** Admin only

### 3. **Template Structure**

Each template JSON file follows this structure:

```json
{
  "title": "Template Title",
  "description": "Detailed description of what this template covers",
  "subject": "num_forge",
  "grade_level": "5",
  "tags": ["tag1", "tag2", "tag3"],
  "template_data": {
    "topic": "Topic Name",
    "instructions": "Student instructions",
    "differentiation_mode": "adaptive",
    "assignment_type": "practice",
    "num_questions": 10,
    "character": "nova",
    "questions": [
      {
        "prompt": "Question text",
        "type": "multiple_choice",
        "choices": ["A", "B", "C", "D"],
        "expected": ["Correct answer"],
        "hint": "Helpful hint",
        "explanation": "Why this is correct",
        "difficulty": "medium"
      }
    ],
    "metadata": {
      "estimated_time": 20,
      "skill_focus": ["skill1", "skill2"],
      "standards": ["CCSS.Math.5.NF.A.1"],
      "is_featured": true
    }
  }
}
```

## Starter Templates Included

### Math (num_forge)
1. **Adding Fractions with Unlike Denominators** (Grade 5)
   - 10 adaptive questions
   - Difficulty: Easy → Hard progression
   - Standards: CCSS.Math.5.NF.A.1
   - ⭐ Featured

2. **Multiplication Facts Mastery** (Grade 3)
   - 15 mastery-based questions
   - Times tables 2-10
   - Standards: CCSS.Math.3.OA.C.7
   - ⭐ Featured

### Science (atom_sphere)
3. **Photosynthesis: How Plants Make Food** (Grade 5)
   - 12 scaffold questions
   - Life science / biology focus
   - Standards: NGSS.5-LS1-1
   - ⭐ Featured

### Reading (story_verse)
4. **Finding the Main Idea** (Grade 4)
   - 10 adaptive comprehension questions
   - Passage-based with supporting details
   - Standards: CCSS.ELA-LITERACY.RI.4.2
   - ⭐ Featured

### Writing (ink_haven)
5. **Writing Strong Paragraphs** (Grade 3)
   - 10 scaffold questions
   - Topic sentences, details, conclusions
   - Standards: CCSS.ELA-LITERACY.W.3.2

### Money (coin_quest)
6. **Counting Coins and Bills** (Grade 2)
   - 12 adaptive questions
   - Real-world math application
   - Standards: CCSS.Math.2.MD.C.8
   - ⭐ Featured

## How to Use

### For Deployment

1. **Upload template files to production:**
   ```bash
   # Make sure templates_seed directory is deployed with your app
   # Directory structure should be:
   # /app
   #   /templates_seed
   #     /templates
   #       /math
   #       /science
   #       /reading
   #       /writing
   #       /money
   ```

2. **Run the seeding endpoint:**
   - Visit: `https://cozmiclearning.com/admin/seed-templates`
   - Must be logged in as admin
   - Returns JSON with results

3. **Verify templates loaded:**
   ```json
   {
     "success": true,
     "message": "Seeded 6 templates",
     "created": 6,
     "skipped": 0,
     "errors": 0,
     "total_system_templates": 6,
     "output": "Detailed log..."
   }
   ```

### For Teachers

**Browsing Templates:**
- Visit `/teacher/templates` to see all available templates
- Filter by subject, grade level, and tags
- Preview template questions before using

**Using a Template:**
1. Browse template library
2. Click "Use This Template" on desired template
3. Template data loads into session
4. Customize if needed (change title, dates, class, etc.)
5. Preview questions
6. Publish to students

**Creating Custom Templates:**
1. Create an assignment as usual
2. On the preview page, click "💾 Save as Template"
3. Enter title, description, tags
4. Choose whether to share publicly
5. Template saved for future use

## Database Schema

**AssignmentTemplate Model** (already exists in models.py):

```python
class AssignmentTemplate(db.Model):
    id = Column(Integer, primary_key=True)
    teacher_id = Column(Integer, nullable=True)  # NULL for system templates
    parent_id = Column(Integer, nullable=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    subject = Column(String(50))
    grade_level = Column(String(20))
    template_data = Column(Text, nullable=False)  # JSON
    is_public = Column(Boolean, default=False)
    use_count = Column(Integer, default=0)
    tags = Column(Text)  # JSON array
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
```

**System templates:**
- `teacher_id = NULL`
- `parent_id = NULL`
- `is_public = True`

**User templates:**
- `teacher_id` or `parent_id` set to owner
- `is_public` = True/False (user's choice)

## Adding More Templates

### Creating New Template JSON Files

1. Create a new JSON file in appropriate directory:
   ```
   templates_seed/templates/{subject}/{template_name}.json
   ```

2. Follow the structure shown above

3. Include quality questions with:
   - Clear prompts
   - Helpful hints
   - Detailed explanations
   - Appropriate difficulty progression

4. Add metadata:
   - Estimated time (minutes)
   - Skill focus tags
   - Standards alignment
   - Featured flag (for curated templates)

### Template Guidelines

**Question Quality:**
- Use age-appropriate language
- Provide helpful (not obvious) hints
- Write explanations that teach, not just confirm
- Include 3-4 answer choices for multiple choice
- Vary difficulty (easy → medium → hard)

**Differentiation Modes:**
- **adaptive**: Questions adjust based on performance (recommended for practice)
- **mastery**: Student must demonstrate proficiency before advancing
- **scaffold**: Provides hints and support for struggling students
- **none**: Standard assignment (good for assessments)

**Assignment Types:**
- **practice**: Learning-focused, adaptive, formative
- **quiz**: Quick assessment, fewer questions
- **homework**: Independent practice, flexible
- **assessment**: Formal evaluation, graded

### Rerunning the Seed

To add new templates after initial seeding:

1. Add new JSON files to `templates_seed/templates/`
2. Visit `/admin/seed-templates` again
3. Existing templates will be skipped
4. Only new templates will be created

## Template Library UI (Already Exists)

**Teacher Template Library Page:**
- Route: `/teacher/templates`
- Template: `teacher_template_library.html`
- Features:
  - Browse all public templates
  - Filter by subject and grade
  - Search by keyword
  - View template details
  - Use template button
  - Save template for later

**Homeschool Template Library Page:**
- Route: `/homeschool/templates`
- Template: `homeschool_template_library.html`
- Same features as teacher version

## Integration with Assignment Wizard

The assignment wizard we just created (`assignment_wizard.html`) can be enhanced to include a "Browse Templates" option:

**Future Enhancement:**
1. Add "Start from Template" button to wizard Step 1
2. Opens template library modal
3. User selects template
4. Wizard pre-populates with template data
5. User can still customize before creating

## Next Steps

### Immediate (Production)
1. ✅ Deploy `templates_seed/` directory to production
2. ✅ Run `/admin/seed-templates` endpoint
3. ✅ Verify templates appear in `/teacher/templates`
4. Test template → assignment flow

### Short-term (Enhancement)
1. Create 50+ more templates across all subjects
2. Add template preview modal to library page
3. Add "Featured Templates" section
4. Integrate templates into assignment wizard
5. Add "Save as Template" button to assignment preview pages

### Long-term (Advanced Features)
1. Template ratings and reviews
2. Community template submissions
3. Template collections/bundles
4. Template analytics (most used, highest rated)
5. AI-powered template recommendations
6. Template remix/fork feature

## Files Modified/Created

### New Files
1. `/templates_seed/seed_templates.py` - Standalone seed script
2. `/templates_seed/templates/math/fractions_addition_5th.json`
3. `/templates_seed/templates/math/multiplication_facts_3rd.json`
4. `/templates_seed/templates/science/photosynthesis_5th.json`
5. `/templates_seed/templates/reading/main_idea_4th.json`
6. `/templates_seed/templates/writing/paragraph_writing_3rd.json`
7. `/templates_seed/templates/money/counting_money_2nd.json`
8. `/TEMPLATES_LIBRARY_GUIDE.md` - This file

### Modified Files
1. `/app.py` - Added `/admin/seed-templates` endpoint (lines 4103-4231)

## Admin Endpoint Reference

### Seed Templates
```
GET /admin/seed-templates
```

**Authentication:** Admin only

**Response:**
```json
{
  "success": true,
  "message": "Seeded 6 templates",
  "created": 6,
  "skipped": 0,
  "errors": 0,
  "total_system_templates": 6,
  "output": "Detailed output log..."
}
```

**Use Case:**
- Initial setup after deployment
- Adding new template batches
- Re-syncing templates after updates

## Template Subjects Reference

Based on `subjects_config.py`:

- `num_forge` - Math (NumForge)
- `atom_sphere` - Science (AtomSphere)
- `ink_haven` - Writing (InkHaven)
- `story_verse` - Reading (StoryVerse)
- `chrono_core` - History (ChronoCore)
- `faith_realm` - Bible (FaithRealm)
- `coin_quest` - Money (CoinQuest)
- `stock_star` - Investing (StockStar)
- `truth_forge` - Apologetics (TruthForge)
- `map_verse` - Geography (MapVerse)
- `power_grid` - Deep Study (PowerGrid)
- `respect_realm` - Life Skills (RespectRealm)

## Success Metrics

**Adoption:**
- Track % of assignments created from templates vs. scratch
- Monitor template usage counts
- Measure time to create assignment (target: < 2 minutes with templates)

**Quality:**
- Template ratings (if implemented)
- Student completion rates
- Teacher feedback

**Growth:**
- Total templates available
- Community-contributed templates
- Template coverage across subjects/grades

---

## Quick Start Commands

```bash
# Deploy templates to production
git add templates_seed/
git commit -m "Add starter assignment templates"
git push

# After deployment, seed templates
curl -X GET https://cozmiclearning.com/admin/seed-templates \
  -H "Cookie: session=YOUR_SESSION_COOKIE"

# Or visit in browser (must be logged in as admin):
https://cozmiclearning.com/admin/seed-templates
```

## Support

For questions or issues with the template system:
1. Check this guide first
2. Review template JSON structure
3. Check `/admin/seed-templates` output for errors
4. Verify database has AssignmentTemplate table
5. Confirm templates directory structure is correct

---

**Last Updated:** 2025-12-19
**Status:** Ready for Production
**Templates Count:** 6 starter templates (expandable to 150+)
