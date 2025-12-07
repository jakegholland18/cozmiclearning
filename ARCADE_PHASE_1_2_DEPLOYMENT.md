# Arcade Phase 1 & 2 - Quick Deployment Guide
## 16 Games with Difficulty System - Ready to Deploy!

---

## ✅ WHAT'S ALREADY DONE

1. ✅ **arcade_helper.py** - Complete with 16 games and difficulty system
2. ✅ **models.py** - Updated with difficulty fields
3. ✅ **add_arcade_difficulty.py** - Database migration script ready

---

## 🚀 DEPLOYMENT STEPS

### Step 1: Run Database Migration (5 minutes)

```bash
# Back up database first!
cp persistent_db/cozmiclearning.db persistent_db/cozmiclearning.db.backup

# Run migration
python add_arcade_difficulty.py
```

**Expected output:**
```
✅ Added difficulty column to game_sessions
✅ Added difficulty column to game_leaderboards
✅ Added difficulty column to daily_challenges
✅ MIGRATION COMPLETE!
```

---

### Step 2: Update Routes in app.py (15 minutes)

#### A. Update imports in `/arcade/play/<game_key>` route (line ~1559)

**Find this import block:**
```python
from modules.arcade_helper import (
    generate_speed_math,
    generate_number_detective,
    generate_fraction_frenzy,
    generate_equation_race,
    generate_element_match,
    generate_vocab_builder,
    generate_spelling_sprint,
    generate_grammar_quest,
    generate_science_quiz,
    generate_history_timeline,
    generate_geography_dash,
    ARCADE_GAMES
)
```

**Replace with:**
```python
from modules.arcade_helper import (
    generate_speed_math,
    generate_number_detective,
    generate_fraction_frenzy,
    generate_equation_race,
    generate_element_match,
    generate_vocab_builder,
    generate_spelling_sprint,
    generate_grammar_quest,
    generate_science_quiz,
    generate_history_timeline,
    generate_geography_dash,
    generate_multiplication_mayhem,
    generate_reading_racer,
    generate_map_master,
    generate_bible_trivia,
    ARCADE_GAMES
)
```

#### B. Update difficulty selection logic (line ~1579)

**Find this:**
```python
# Check if grade was provided in URL (from grade selection screen)
selected_grade = request.args.get("grade")

# If no grade selected, show grade selection screen
if not selected_grade:
    return render_template(
        "arcade_grade_select.html",
        game=game_info,
        character=session.get("character", "everly")
    )

# Use selected grade instead of session grade
grade = selected_grade
```

**Replace with:**
```python
# Check if difficulty was provided in URL (from difficulty selection screen)
selected_difficulty = request.args.get("difficulty")

# If no difficulty selected, show difficulty selection screen
if not selected_difficulty:
    return render_template(
        "arcade_difficulty_select.html",
        game=game_info,
        character=session.get("character", "everly")
    )

# Use selected difficulty
difficulty = selected_difficulty
```

#### C. Update game generators dict (line ~1593)

**Find this:**
```python
# Map each game to its specific generator
game_generators = {
    "speed_math": generate_speed_math,
    "number_detective": generate_number_detective,
    "fraction_frenzy": generate_fraction_frenzy,
    "equation_race": generate_equation_race,
    "element_match": generate_element_match,
    "lab_quiz_rush": generate_science_quiz,
    "planet_explorer": generate_science_quiz,
    "vocab_builder": generate_vocab_builder,
    "spelling_sprint": generate_spelling_sprint,
    "grammar_quest": generate_grammar_quest,
    "history_timeline": generate_history_timeline,
    "geography_dash": generate_geography_dash,
}

# Get the appropriate generator for this game
generator = game_generators.get(game_key, generate_speed_math)
questions = generator(grade)
```

**Replace with:**
```python
# Map each game to its specific generator
game_generators = {
    "speed_math": generate_speed_math,
    "number_detective": generate_number_detective,
    "fraction_frenzy": generate_fraction_frenzy,
    "equation_race": generate_equation_race,
    "element_match": generate_element_match,
    "lab_quiz_rush": generate_science_quiz,
    "planet_explorer": generate_science_quiz,
    "vocab_builder": generate_vocab_builder,
    "spelling_sprint": generate_spelling_sprint,
    "grammar_quest": generate_grammar_quest,
    "history_timeline": generate_history_timeline,
    "geography_dash": generate_geography_dash,
    "multiplication_mayhem": generate_multiplication_mayhem,
    "reading_racer": generate_reading_racer,
    "map_master": generate_map_master,
    "bible_trivia": generate_bible_trivia,
}

# Get the appropriate generator for this game
generator = game_generators.get(game_key, generate_speed_math)
questions = generator(difficulty)
```

#### D. Update session storage (line ~1613)

**Find this:**
```python
# Store questions in session along with selected grade
session["current_game"] = {
    "game_key": game_key,
    "questions": questions,
    "current_index": 0,
    "correct": 0,
    "selected_grade": grade,
    "start_time": datetime.utcnow().isoformat()
}
```

**Replace with:**
```python
# Store questions in session along with selected difficulty
session["current_game"] = {
    "game_key": game_key,
    "questions": questions,
    "current_index": 0,
    "correct": 0,
    "selected_difficulty": difficulty,
    "start_time": datetime.utcnow().isoformat()
}
```

#### E. Update arcade_play template render (line ~1624)

**Find this:**
```python
return render_template(
    "arcade_play.html",
    game=game_info,
    questions=questions,
    grade=grade,
    character=session.get("character", "everly")
)
```

**Replace with:**
```python
return render_template(
    "arcade_play.html",
    game=game_info,
    questions=questions,
    difficulty=difficulty,
    character=session.get("character", "everly")
)
```

#### F. Update `/arcade/submit` route (line ~1658)

**Find this:**
```python
# Get selected grade from current game session, fallback to student's grade
current_game = session.get("current_game", {})
grade = current_game.get("selected_grade") or session.get("grade", "5")

# ... (later line 1666)

# Save game session and get results
results = save_game_session(student_id, game_key, grade, score, time_seconds, correct, total)
```

**Replace with:**
```python
# Get selected difficulty from current game session, default to medium
current_game = session.get("current_game", {})
difficulty = current_game.get("selected_difficulty", "medium")

# ... (later)

# Save game session and get results
results = save_game_session(student_id, game_key, difficulty, score, time_seconds, correct, total)
```

#### G. Update `/arcade/game/<game_key>` route (line ~1537)

**Find this:**
```python
# Get leaderboard
try:
    leaderboard = get_leaderboard(game_key, grade, limit=10)
except Exception as e:
    app.logger.warning(f"Could not load leaderboard: {e}")
    leaderboard = []
```

**Replace with:**
```python
# Get leaderboards for all difficulties
leaderboards = {}
for diff in ['easy', 'medium', 'hard']:
    try:
        leaderboards[diff] = get_leaderboard(game_key, diff, limit=10)
    except Exception as e:
        app.logger.warning(f"Could not load {diff} leaderboard: {e}")
        leaderboards[diff] = []
```

**And update the template render (line ~1544):**
```python
return render_template(
    "arcade_game.html",
    game=game_info,
    stats=stats,
    leaderboards=leaderboards,  # Changed from 'leaderboard' to 'leaderboards'
    character=session["character"]
)
```

---

### Step 3: Create Templates (30 minutes)

See separate template files that will be provided next.

---

### Step 4: Test Locally (30 minutes)

1. Start the app: `python app.py`
2. Navigate to `/arcade`
3. Test each of the 4 new games:
   - Multiplication Mayhem
   - Reading Racer
   - Map Master
   - Bible Trivia
4. Test difficulty levels (Easy, Medium, Hard) on 2-3 games
5. Check leaderboards update correctly
6. Verify XP multipliers (Easy=1.0x, Medium=1.5x, Hard=2.0x)

---

### Step 5: Deploy to Production (15 minutes)

```bash
# Commit changes
git add .
git commit -m "Add Arcade Phase 1+2: 4 new games + difficulty system (16 total games)"

# Push to GitHub (triggers Render deployment)
git push origin main
```

**After deployment on Render:**
1. Run migration via Render shell or admin route
2. Test 2-3 games on production
3. Check for any errors in logs

---

## 📝 TESTING CHECKLIST

- [ ] Database migration runs successfully
- [ ] All 16 games appear in arcade hub
- [ ] "NEW!" badges show on 4 new games
- [ ] Difficulty selection works for all games
- [ ] Easy/Medium/Hard generate appropriate questions
- [ ] XP multipliers apply correctly (check completion screen)
- [ ] Leaderboards separate by difficulty
- [ ] Leaderboard tabs work on game detail page
- [ ] Bible Trivia game works on all difficulties
- [ ] Mobile responsive on all screens

---

## 🎯 QUICK REFERENCE

**16 Total Games:**
- 12 Existing games (updated for difficulty)
- 4 New games (Multiplication Mayhem, Reading Racer, Map Master, Bible Trivia)

**3 Difficulty Levels:**
- 🟢 Easy (1.0x XP) - Elementary
- 🟡 Medium (1.5x XP) - Middle School
- 🔴 Hard (2.0x XP) - High School

**Files Modified:**
- ✅ `modules/arcade_helper.py`
- ⏳ `app.py` (arcade routes)
- ⏳ `website/templates/arcade_difficulty_select.html` (NEW)
- ⏳ `website/templates/arcade_game.html` (UPDATE)
- ⏳ `website/templates/arcade_hub.html` (UPDATE)

---

**🎮 Ready to continue with template creation!**
