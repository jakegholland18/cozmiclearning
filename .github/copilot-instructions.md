# CozmicLearning Copilot Instructions

## Project Overview
CozmicLearning is an AI-powered educational platform combining gamification, subject-specific tutoring, and differentiated practice missions. Built with Flask + SQLite, it serves students, parents, and teachers with:
- **11 "planets"** (subjects): NumForge (math), AtomSphere (science), InkHaven (writing), etc.
- **Multi-role authentication**: student/parent/teacher/owner + admin
- **Differentiation engine**: generates AI practice missions at varying difficulty levels
- **Analytics**: per-student ability assessment and class-wide subject performance tracking

## Architecture Essentials

### Core Data Model (`models.py`)
- **Parent** → one-to-many **Students** (for parent dashboard access)
- **Teacher** → one-to-many **Classes** → one-to-many **Students**
- **AssignedPractice** (teacher assignments) has optional **AssignedQuestions**
- **AssessmentResult** (DB-backed scores) feeds into student ability tier calculation
  - Ability levels: `"struggling"` | `"on_level"` | `"advanced"` (auto-computed from last 10 results avg)

### Subject Routing (`app.py` lines 150–165)
Every subject maps to a helper module function via `subject_map`:
```python
subject_map = {
    "num_forge": math_helper.explain_math,
    "atom_sphere": science_helper.explain_science,
    # ... 9 more subjects
    "power_grid": None,  # handled separately (study guide mode)
}
```
When adding new subjects: add entry to `subject_map` AND create corresponding helper module.

### Session-Based State (app.py lines 195–220)
Students maintain gamification state in Flask session:
- `tokens`, `xp`, `level`, `streak` — gameplay metrics
- `practice`: active mission dict; `practice_step`: current index
- `conversation`: deep study chat history; `deep_study_chat`: PowerGrid chat
- `character`: visual avatar (everly, lio, nova, etc.)

## Critical Developer Workflows

### Adding a New Subject (Planet)
1. Create `modules/<subject>_helper.py` with function `explain_<subject>(question, grade, character)`
2. Add entry to `subject_map` in `app.py` line ~150
3. Function must return dict with `"raw_text"` key OR plain string
4. Use `study_buddy_ai()` from `shared_ai.py` for AI generation — **always include character voice**

### Differentiation in Practice Missions
`apply_differentiation()` in `practice_helper.py` (lines 37–72) modifies AI prompts based on mode:
- `"none"`: standard difficulty
- `"adaptive"`: difficulty scales per attempt
- `"gap_fill"`: target misconceptions
- `"mastery"`: multi-step, application-heavy
- `"scaffold"`: confidence-building, step-broken

Teacher sets `differentiation_mode` when creating assignment; AI generator uses this.

### Practice Mission Flow
1. **Generate** (`generate_practice_session()` in practice_helper.py): AI creates mission dict with `steps` array
2. **Display** (`assignment_step`): render current step, show hint if requested
3. **Grade** (`practice_step` POST): `answers_match()` checks flexibility (tolerates formatting, case, units)
4. **Record** (optional): `AssessmentResult` saved on final step completion

Steps don't auto-save to DB — stored in session until completion.

### AI Integration Pattern
All subject helpers follow this pattern:
```python
from modules.shared_ai import study_buddy_ai, build_character_voice, grade_depth_instruction

prompt = f"Your teaching prompt... {grade_depth_instruction(grade)}"
result = study_buddy_ai(prompt, grade, character)
# result is dict with 'raw_text' key or raw string
```

## Project-Specific Conventions

### Database Rebuild on Startup
`rebuild_database_if_needed()` (app.py lines 78–113) auto-rebuilds DB if critical columns missing.
Check for new column requirements before migration — no migration framework; manual checks via PRAGMA.

### Six-Section Format for Explanations
All subject lessons must use `BASE_SYSTEM_PROMPT` format (shared_ai.py):
```
SECTION 1 — OVERVIEW
[2–3 sentences]

SECTION 2 — KEY FACTS
[3–5 sentences, paragraphs only, no bullets]

SECTION 3 — CHRISTIAN VIEW
[worldview perspective]

SECTION 4 — AGREEMENT
[common ground]

SECTION 5 — DIFFERENCE
[divergent worldviews]

SECTION 6 — PRACTICE
[sample question]
```
**Strict rule**: No bullets, no lists, only paragraphs with full sentences.

### Answer Matching Logic
`answers_match()` in app.py (lines 354–387) normalizes user vs. expected answers:
1. Exact string match (case-insensitive)
2. Numeric token normalization: strips `"percent"`, `"%"`, `"$"`, commas, etc.
3. Float comparison with 1e-6 tolerance
**Implication**: accept flexible answer formats for math/money answers.

### Grade Level Depth Rules
`grade_depth_instruction()` in shared_ai.py auto-scales explanation complexity:
- Grades 1–3: very simple words, short sentences
- Grades 4–5: simple language with clear examples
- Grades 6–8: moderate detail
- Grades 9–10: deeper reasoning
- Grades 11–12: college-level rigor

Always pass grade to AI helpers; AI adjusts vocabulary automatically.

### Teacher-Only Routes & Owner Privileges
- `is_owner()` checks if teacher email matches `OWNER_EMAIL` (jakegholland18@gmail.com)
- Owner can view/edit all classes/assignments; regular teachers see only their own
- Owner role set via email, not a separate field

### Streaks & Daily Gamification
- `update_streak()` (app.py lines 265–277): incremented on new day visit, resets if gap > 1 day
- Called on every `init_user()`
- XP: each subject answer grants 20 XP; level-up every `level * 100` XP threshold

## Integration Points & Dependencies

### External APIs
- **OpenAI**: via `shared_ai.get_client()` using `OPENAI_API_KEY` env var
  - Models used: GPT (check for latest model in helper files)
  - All calls go through `study_buddy_ai()` wrapper

### Key File Dependencies
- `shared_ai.py`: central AI call hub; all helpers depend on this
- `answer_formatter.py`: parses AI responses into section structure
- `personality_helper.py`: character voices and avatar data
- `practice_helper.py`: mission generation engine

### Database Relationships to Preserve
- Deleting a Teacher cascades if FK enforced; check SQLAlchemy relationship backref
- Student ability recalculation (`recompute_student_ability()`) reads last 10 `AssessmentResult` rows only
- `AssignedPractice.preview_json` stores full mission JSON; regenerate on edit

## Common Pitfalls & Gotchas

1. **Session state clears on logout**: `session.clear()` destroys all student progress state (intentional)
2. **No cascade deletes configured**: manually handle orphaned questions when deleting assignments
3. **AI response parsing assumes six-section format**: if subject helper breaks format, downstream rendering fails
4. **Grade level is string throughout**: convert to int in helper if numeric math needed
5. **Teacher role validation**: always check both teacher_id in session AND teacher owns resource before rendering
6. **Differentiation mode ignored on generic practice**: only applied in teacher-assigned missions via `apply_differentiation()`

## Testing & Debugging Advice

- **SQL errors**: run `rebuild_database_if_needed()` or manually delete `cozmiclearning.db` and restart
- **Missing OpenAI responses**: check `OPENAI_API_KEY` env var; verify API quota
- **Session data lost**: ensure `session.modified = True` after session updates (session dict doesn't auto-detect deep changes)
- **Practice missions not generating**: verify subject is in `subject_map` and helper returns proper dict structure
- **Analytics show "0" for ability**: run `recompute_student_ability()` to recalculate from stored results
