"""
Tutorial Content Templates - Based ONLY on actual coded features
Each tutorial matches exactly what exists in the CozmicLearning platform
"""

TUTORIALS = {
    # ===========================================
    # TEACHER TUTORIALS
    # ===========================================

    "teacher-signup": {
        "title": "Teacher Account Setup",
        "icon": "👨‍🏫",
        "category": "teacher",
        "duration": "3 min",
        "difficulty": "Beginner",
        "content": """
            <h2>👨‍🏫 Teacher Account Setup</h2>
            <p>Create your teacher account and start using CozmicLearning.</p>

            <div class="tutorial-steps">
                <div class="tutorial-step">
                    <h4>Step 1: Navigate to Teacher Signup</h4>
                    <p>Go to <code>/teacher/signup</code> or click "Teacher Signup" from the homepage.</p>
                </div>

                <div class="tutorial-step">
                    <h4>Step 2: Fill Out Registration Form</h4>
                    <ul>
                        <li><strong>Name:</strong> Your full name</li>
                        <li><strong>Email:</strong> Valid email address for login</li>
                        <li><strong>Password:</strong> Secure password (at least 8 characters)</li>
                    </ul>
                </div>

                <div class="tutorial-step">
                    <h4>Step 3: Submit and Login</h4>
                    <p>After signup, you'll be redirected to the teacher dashboard at <code>/teacher/dashboard</code>.</p>
                </div>
            </div>

            <div class="tutorial-tip">
                <strong>💡 Pro Tip:</strong> Use a strong password to protect student data!
            </div>
        """
    },

    "create-class": {
        "title": "Create a Class",
        "icon": "🏫",
        "category": "teacher",
        "duration": "2 min",
        "difficulty": "Beginner",
        "content": """
            <h2>🏫 Create a Class</h2>
            <p>Set up your first class to organize students and assignments.</p>

            <div class="tutorial-steps">
                <div class="tutorial-step">
                    <h4>Step 1: Go to Teacher Dashboard</h4>
                    <p>Navigate to <code>/teacher/dashboard</code> or <code>/teacher/classes</code>.</p>
                </div>

                <div class="tutorial-step">
                    <h4>Step 2: Click "Add Class"</h4>
                    <p>Fill out the form:</p>
                    <ul>
                        <li><strong>Class Name:</strong> E.g., "5th Grade Math" or "Smith Homeschool"</li>
                        <li><strong>Grade Level:</strong> Select K-12</li>
                    </ul>
                </div>

                <div class="tutorial-step">
                    <h4>Step 3: Get Your Join Code</h4>
                    <p>After creating the class, you'll receive a unique 8-character join code.</p>
                    <p>Share this code with students so they can join your class.</p>
                </div>
            </div>

            <div class="tutorial-tip">
                <strong>💡 Pro Tip:</strong> Create separate classes for different subjects or periods!
            </div>
        """
    },

    "add-students": {
        "title": "Add Students to Your Class",
        "icon": "👥",
        "category": "teacher",
        "duration": "3 min",
        "difficulty": "Beginner",
        "content": """
            <h2>👥 Add Students to Your Class</h2>
            <p>Two ways to add students: manually or have them join with a code.</p>

            <div class="tutorial-steps">
                <div class="tutorial-step">
                    <h4>Method 1: Students Join Themselves</h4>
                    <ol>
                        <li>Share your class join code with students</li>
                        <li>Students create accounts at <code>/student/signup</code></li>
                        <li>Students enter join code at <code>/student/join-class</code></li>
                        <li>They automatically appear in your class!</li>
                    </ol>
                </div>

                <div class="tutorial-step">
                    <h4>Method 2: Manually Add Students</h4>
                    <ol>
                        <li>Go to your class page</li>
                        <li>Click "Add Student"</li>
                        <li>Enter student name, email, password</li>
                        <li>Set ability level (Below/On-Level/Advanced)</li>
                        <li>Click "Create Student"</li>
                    </ol>
                </div>

                <div class="tutorial-step">
                    <h4>Step 3: Set Ability Levels</h4>
                    <p>For each student, choose their differentiation level:</p>
                    <ul>
                        <li><strong>Below Grade Level:</strong> Easier questions with more support</li>
                        <li><strong>On Grade Level:</strong> Standard grade-level content</li>
                        <li><strong>Advanced:</strong> Challenging content for gifted students</li>
                    </ul>
                </div>
            </div>

            <div class="tutorial-warning">
                <strong>⚠️ Privacy:</strong> For young students, use generic emails like "student1@yourschool.local"
            </div>
        """
    },

    "create-assignment": {
        "title": "Create Assignments",
        "icon": "📝",
        "category": "teacher",
        "duration": "5 min",
        "difficulty": "Intermediate",
        "content": """
            <h2>📝 Create Assignments</h2>
            <p>Generate AI-powered assignments for your class.</p>

            <div class="tutorial-steps">
                <div class="tutorial-step">
                    <h4>Step 1: Navigate to Create Assignment</h4>
                    <p>Go to <code>/teacher/assignments/create</code> or click "Create Assignment" from your dashboard.</p>
                </div>

                <div class="tutorial-step">
                    <h4>Step 2: Fill Out Assignment Details</h4>
                    <ul>
                        <li><strong>Title:</strong> Name of assignment (e.g., "Chapter 3 Fractions Quiz")</li>
                        <li><strong>Subject:</strong> Choose from subjects like num_forge, atom_sphere, story_verse</li>
                        <li><strong>Topic:</strong> Specific topic (e.g., "Adding Fractions")</li>
                        <li><strong>Instructions:</strong> Directions for students</li>
                        <li><strong>Open Date:</strong> When assignment becomes visible</li>
                        <li><strong>Due Date:</strong> Deadline for completion</li>
                        <li><strong>Assignment Type:</strong> practice, quiz, test, or homework</li>
                    </ul>
                </div>

                <div class="tutorial-step">
                    <h4>Step 3: Choose Differentiation Mode</h4>
                    <p>Select how questions adjust to student ability:</p>
                    <ul>
                        <li><strong>none:</strong> Same questions for all students</li>
                        <li><strong>adaptive:</strong> Questions adjust based on student level</li>
                        <li><strong>gap_fill:</strong> Focus on student weaknesses</li>
                        <li><strong>mastery:</strong> Repeat until mastered</li>
                        <li><strong>scaffold:</strong> Step-by-step support</li>
                    </ul>
                </div>

                <div class="tutorial-step">
                    <h4>Step 4: Generate Questions (AI)</h4>
                    <p>CozmicLearning uses AI to create questions based on your topic and grade level.</p>
                    <p>The system generates multiple-choice and free-response questions automatically.</p>
                </div>

                <div class="tutorial-step">
                    <h4>Step 5: Preview Before Publishing</h4>
                    <p>After creation, preview your assignment at <code>/teacher/assignments/[id]/preview</code>.</p>
                    <p>You can see the full mission, differentiation analysis, and all questions.</p>
                </div>

                <div class="tutorial-step">
                    <h4>Step 6: Publish to Students</h4>
                    <p>Click "Publish" at <code>/teacher/assignments/[id]/publish</code>.</p>
                    <p>Once published, students can see and start the assignment!</p>
                </div>
            </div>

            <div class="tutorial-tip">
                <strong>💡 Pro Tip:</strong> Use differentiation mode "adaptive" for mixed-ability classes!
            </div>
        """
    },

    "view-gradebook": {
        "title": "Using the Gradebook",
        "icon": "📊",
        "category": "teacher",
        "duration": "4 min",
        "difficulty": "Beginner",
        "content": """
            <h2>📊 Using the Gradebook</h2>
            <p>Track student performance and grades.</p>

            <div class="tutorial-steps">
                <div class="tutorial-step">
                    <h4>Step 1: Access Gradebook</h4>
                    <p>Navigate to <code>/teacher/gradebook</code> to see all your classes.</p>
                    <p>Click a specific class to view detailed grades at <code>/teacher/gradebook/class/[class_id]</code>.</p>
                </div>

                <div class="tutorial-step">
                    <h4>Step 2: View Student Submissions</h4>
                    <p>From the gradebook, click on any assignment to see submissions at <code>/teacher/assignments/[id]/submissions</code>.</p>
                    <p>You'll see:</p>
                    <ul>
                        <li>Which students submitted</li>
                        <li>Submission status (not_started, in_progress, submitted, graded)</li>
                        <li>Scores and completion times</li>
                    </ul>
                </div>

                <div class="tutorial-step">
                    <h4>Step 3: Grade Submissions</h4>
                    <p>Click on a submission to grade it at <code>/teacher/submissions/[id]/grade</code>.</p>
                    <p>You can:</p>
                    <ul>
                        <li>Assign points for each question</li>
                        <li>Add feedback comments</li>
                        <li>Save the grade</li>
                    </ul>
                </div>

                <div class="tutorial-step">
                    <h4>Step 4: Export Grades</h4>
                    <p>Download grades as CSV at <code>/teacher/gradebook/class/[class_id]/export</code>.</p>
                    <p>Open in Excel, Google Sheets, or any spreadsheet program.</p>
                </div>
            </div>

            <div class="tutorial-tip">
                <strong>💡 Pro Tip:</strong> Check gradebook daily to catch struggling students early!
            </div>
        """
    },

    "teacher-messaging": {
        "title": "Message Parents",
        "icon": "💬",
        "category": "teacher",
        "duration": "3 min",
        "difficulty": "Beginner",
        "content": """
            <h2>💬 Message Parents</h2>
            <p>Communicate with parents about student progress.</p>

            <div class="tutorial-steps">
                <div class="tutorial-step">
                    <h4>Step 1: View Messages</h4>
                    <p>Navigate to <code>/teacher/messages</code> to see all messages from parents.</p>
                </div>

                <div class="tutorial-step">
                    <h4>Step 2: Compose New Message</h4>
                    <p>Go to <code>/teacher/messages/compose</code> to send a message to a parent.</p>
                    <ul>
                        <li>Select student (message goes to their parent)</li>
                        <li>Write subject line</li>
                        <li>Write message body</li>
                        <li>Click Send</li>
                    </ul>
                </div>

                <div class="tutorial-step">
                    <h4>Step 3: Send Progress Reports</h4>
                    <p>Send detailed progress reports at <code>/teacher/send_progress_report/[student_id]</code>.</p>
                    <p>This includes:</p>
                    <ul>
                        <li>Recent assignment scores</li>
                        <li>Subject performance</li>
                        <li>Recommendations for improvement</li>
                    </ul>
                </div>
            </div>

            <div class="tutorial-warning">
                <strong>⚠️ Privacy:</strong> Keep all communication professional and student data confidential.
            </div>
        """
    },

    "lesson-plans": {
        "title": "Generate Lesson Plans",
        "icon": "📚",
        "category": "teacher",
        "duration": "5 min",
        "difficulty": "Intermediate",
        "content": """
            <h2>📚 Generate Lesson Plans</h2>
            <p>Create comprehensive lesson plans using AI.</p>

            <div class="tutorial-steps">
                <div class="tutorial-step">
                    <h4>Step 1: Generate a Lesson Plan</h4>
                    <p>Use the endpoint <code>/teacher/generate_lesson_plan</code> (POST) with:</p>
                    <ul>
                        <li>Subject (e.g., "Math", "Science")</li>
                        <li>Topic (e.g., "Photosynthesis")</li>
                        <li>Grade level</li>
                    </ul>
                </div>

                <div class="tutorial-step">
                    <h4>Step 2: Review Lesson Plan</h4>
                    <p>View all lesson plans at <code>/teacher/lesson_plans</code>.</p>
                    <p>Click any plan to view details at <code>/teacher/lesson_plans/[id]</code>.</p>
                    <p>Each plan includes 6 sections:</p>
                    <ul>
                        <li>Overview</li>
                        <li>Key Facts</li>
                        <li>Christian Worldview</li>
                        <li>Points of Agreement</li>
                        <li>Points of Difference</li>
                        <li>Practice Activities</li>
                    </ul>
                </div>

                <div class="tutorial-step">
                    <h4>Step 3: Edit or Regenerate Sections</h4>
                    <p>Edit plans at <code>/teacher/lesson_plans/[id]/edit</code>.</p>
                    <p>Regenerate specific sections at <code>/teacher/lesson_plans/[id]/regenerate_section</code>.</p>
                </div>

                <div class="tutorial-step">
                    <h4>Step 4: Print or Export</h4>
                    <p>Print lesson plans at <code>/teacher/lesson_plans/[id]/print</code>.</p>
                </div>
            </div>

            <div class="tutorial-tip">
                <strong>💡 Pro Tip:</strong> Regenerate sections you're not satisfied with - the AI creates new content each time!
            </div>
        """
    },

    # ===========================================
    # STUDENT TUTORIALS
    # ===========================================

    "student-login": {
        "title": "Student Login & Getting Started",
        "icon": "🎒",
        "category": "student",
        "duration": "3 min",
        "difficulty": "Beginner",
        "content": """
            <h2>🎒 Student Login & Getting Started</h2>
            <p>Log in and start your learning adventure!</p>

            <div class="tutorial-steps">
                <div class="tutorial-step">
                    <h4>Step 1: Go to Student Login</h4>
                    <p>Navigate to <code>/student/login</code>.</p>
                    <p>Enter your email and password that your teacher gave you.</p>
                </div>

                <div class="tutorial-step">
                    <h4>Step 2: Your Dashboard</h4>
                    <p>After login, you'll see your dashboard at <code>/dashboard</code>.</p>
                    <p>You'll see:</p>
                    <ul>
                        <li>Your XP points and level</li>
                        <li>Current streak (days in a row you've logged in)</li>
                        <li>Achievements and badges</li>
                        <li>Quick links to subjects and arcade games</li>
                    </ul>
                </div>

                <div class="tutorial-step">
                    <h4>Step 3: Explore the Menu</h4>
                    <p>Main navigation includes:</p>
                    <ul>
                        <li><strong>Dashboard:</strong> Your home screen</li>
                        <li><strong>Explore:</strong> Browse all 12 learning planets</li>
                        <li><strong>Arcade:</strong> Play educational games</li>
                        <li><strong>Assignments:</strong> Work from your teacher</li>
                    </ul>
                </div>
            </div>

            <div class="tutorial-tip">
                <strong>💡 Pro Tip:</strong> Log in daily to build your streak and earn bonus XP!
            </div>
        """
    },

    "take-assignment": {
        "title": "Complete Assignments",
        "icon": "✏️",
        "category": "student",
        "duration": "4 min",
        "difficulty": "Beginner",
        "content": """
            <h2>✏️ Complete Assignments</h2>
            <p>How to find and complete assignments from your teacher.</p>

            <div class="tutorial-steps">
                <div class="tutorial-step">
                    <h4>Step 1: View Your Assignments</h4>
                    <p>Go to <code>/student/assignments</code> to see all published assignments.</p>
                    <p>You'll see:</p>
                    <ul>
                        <li>Assignment titles</li>
                        <li>Due dates</li>
                        <li>Your status (not started, in progress, submitted)</li>
                    </ul>
                </div>

                <div class="tutorial-step">
                    <h4>Step 2: Start an Assignment</h4>
                    <p>Click any assignment to start at <code>/student/assignments/[id]/start</code>.</p>
                    <p>You'll see the first question and can begin answering.</p>
                </div>

                <div class="tutorial-step">
                    <h4>Step 3: Answer Questions</h4>
                    <p>Navigate through questions using "Next Question".</p>
                    <p>Your answers are saved automatically as you progress.</p>
                </div>

                <div class="tutorial-step">
                    <h4>Step 4: Submit Your Work</h4>
                    <p>When finished, click "Submit Assignment".</p>
                    <p>You'll see your score if it's auto-graded, or "Pending" if it needs teacher review.</p>
                </div>
            </div>

            <div class="tutorial-warning">
                <strong>⚠️ Important:</strong> Once submitted, you cannot change your answers!
            </div>
        """
    },

    "explore-subjects": {
        "title": "Explore Learning Planets",
        "icon": "🌌",
        "category": "student",
        "duration": "5 min",
        "difficulty": "Beginner",
        "content": """
            <h2>🌌 Explore Learning Planets</h2>
            <p>Discover all 12 subjects in the CozmicLearning galaxy!</p>

            <div class="tutorial-steps">
                <div class="tutorial-step">
                    <h4>Step 1: Browse Subjects</h4>
                    <p>Navigate to <code>/subjects</code> to see all 12 learning planets:</p>
                    <ul>
                        <li><strong>NumForge:</strong> Mathematics</li>
                        <li><strong>AtomSphere:</strong> Science</li>
                        <li><strong>InkHaven:</strong> Writing</li>
                        <li><strong>ChronoCore:</strong> History</li>
                        <li><strong>StoryVerse:</strong> Reading</li>
                        <li><strong>FaithRealm:</strong> Bible Studies</li>
                        <li><strong>CoinQuest:</strong> Financial Basics</li>
                        <li><strong>StockStar:</strong> Investing</li>
                        <li><strong>TerraNova:</strong> General Knowledge</li>
                        <li><strong>PowerGrid:</strong> Research Skills</li>
                        <li><strong>TruthForge:</strong> Worldview & Logic</li>
                        <li><strong>RespectRealm:</strong> Character Education</li>
                    </ul>
                </div>

                <div class="tutorial-step">
                    <h4>Step 2: Select a Subject</h4>
                    <p>Click any planet to access that subject's content.</p>
                    <p>You'll be able to explore topics and start learning!</p>
                </div>
            </div>

            <div class="tutorial-tip">
                <strong>💡 Challenge:</strong> Try to visit all 12 planets this week!
            </div>
        """
    },

    "play-arcade": {
        "title": "Play Arcade Games",
        "icon": "🎮",
        "category": "student",
        "duration": "3 min",
        "difficulty": "Beginner",
        "content": """
            <h2>🎮 Play Arcade Games</h2>
            <p>Learn through fun educational games!</p>

            <div class="tutorial-steps">
                <div class="tutorial-step">
                    <h4>Step 1: Open Arcade Hub</h4>
                    <p>Navigate to <code>/arcade</code> to see all available games.</p>
                    <p>Games are organized by subject (Math, Science, Language Arts, etc.).</p>
                </div>

                <div class="tutorial-step">
                    <h4>Step 2: Select a Game</h4>
                    <p>Click any game to see details at <code>/arcade/game/[game_key]</code>.</p>
                    <p>You'll see:</p>
                    <ul>
                        <li>Game description</li>
                        <li>Difficulty levels</li>
                        <li>Your high scores</li>
                        <li>Leaderboard</li>
                    </ul>
                </div>

                <div class="tutorial-step">
                    <h4>Step 3: Play the Game</h4>
                    <p>Click "Play" to start at <code>/arcade/play/[game_key]</code>.</p>
                    <p>Answer questions to earn points!</p>
                </div>

                <div class="tutorial-step">
                    <h4>Step 4: View Your Stats</h4>
                    <p>Check your arcade stats at <code>/arcade/stats</code> to see:</p>
                    <ul>
                        <li>Games played</li>
                        <li>High scores</li>
                        <li>Total XP earned</li>
                    </ul>
                </div>

                <div class="tutorial-step">
                    <h4>Step 5: Collect Badges</h4>
                    <p>View earned badges at <code>/arcade/badges</code>.</p>
                    <p>Earn badges by achieving milestones in games!</p>
                </div>
            </div>

            <div class="tutorial-tip">
                <strong>💡 Pro Tip:</strong> Play games related to your assignments to practice what you're learning!
            </div>
        """
    },

    # ===========================================
    # PARENT TUTORIALS
    # ===========================================

    "parent-dashboard": {
        "title": "Parent Dashboard Overview",
        "icon": "👨‍👩‍👧‍👦",
        "category": "parent",
        "duration": "4 min",
        "difficulty": "Beginner",
        "content": """
            <h2>👨‍👩‍👧‍👦 Parent Dashboard Overview</h2>
            <p>Monitor your children's learning progress.</p>

            <div class="tutorial-steps">
                <div class="tutorial-step">
                    <h4>Step 1: Login as Parent</h4>
                    <p>Go to <code>/parent/login</code> and enter your credentials.</p>
                    <p>After login, you'll see your dashboard at <code>/parent_dashboard</code>.</p>
                </div>

                <div class="tutorial-step">
                    <h4>Step 2: View Student Progress</h4>
                    <p>Navigate to <code>/parent/students</code> to see all linked students.</p>
                    <p>You can view:</p>
                    <ul>
                        <li>Student names and accounts</li>
                        <li>Current activity</li>
                        <li>Recent achievements</li>
                    </ul>
                </div>

                <div class="tutorial-step">
                    <h4>Step 3: Check Analytics</h4>
                    <p>Go to <code>/parent/analytics</code> to see detailed performance data:</p>
                    <ul>
                        <li>Subject-by-subject progress</li>
                        <li>Assignment scores</li>
                        <li>Learning trends</li>
                    </ul>
                </div>

                <div class="tutorial-step">
                    <h4>Step 4: View Messages</h4>
                    <p>Check teacher messages at <code>/parent/messages</code>.</p>
                    <p>Reply to messages or send new ones to teachers.</p>
                </div>
            </div>

            <div class="tutorial-tip">
                <strong>💡 Pro Tip:</strong> Check the dashboard weekly to stay informed about your child's progress!
            </div>
        """
    },

    "parent-time-limits": {
        "title": "Set Time Limits",
        "icon": "⏰",
        "category": "parent",
        "duration": "2 min",
        "difficulty": "Beginner",
        "content": """
            <h2>⏰ Set Time Limits</h2>
            <p>Control daily screen time for your students.</p>

            <div class="tutorial-steps">
                <div class="tutorial-step">
                    <h4>Step 1: Access Time Limits</h4>
                    <p>Navigate to <code>/parent/time-limits</code>.</p>
                </div>

                <div class="tutorial-step">
                    <h4>Step 2: Set Daily Limit</h4>
                    <p>Enter daily limit in minutes (5-480 minutes).</p>
                    <p>This applies to all your students.</p>
                </div>

                <div class="tutorial-step">
                    <h4>Step 3: Monitor Usage</h4>
                    <p>When students reach their limit, they'll see a "Time Limit Reached" message.</p>
                    <p>Time resets daily at midnight.</p>
                </div>
            </div>

            <div class="tutorial-warning">
                <strong>⚠️ Note:</strong> Time limits help promote healthy screen time habits!
            </div>
        """
    },

    "parent-safety": {
        "title": "Safety Monitoring",
        "icon": "🛡️",
        "category": "parent",
        "duration": "3 min",
        "difficulty": "Beginner",
        "content": """
            <h2>🛡️ Safety Monitoring</h2>
            <p>Review flagged content and monitor student activity.</p>

            <div class="tutorial-steps">
                <div class="tutorial-step">
                    <h4>Step 1: Access Safety Dashboard</h4>
                    <p>Navigate to <code>/parent/safety</code>.</p>
                </div>

                <div class="tutorial-step">
                    <h4>Step 2: Review Flagged Content</h4>
                    <p>See questions or responses that were flagged by AI moderation.</p>
                    <p>You'll see:</p>
                    <ul>
                        <li>What was flagged</li>
                        <li>Why it was flagged</li>
                        <li>Severity level</li>
                        <li>Date/time</li>
                    </ul>
                </div>

                <div class="tutorial-step">
                    <h4>Step 3: Take Action</h4>
                    <p>If concerned, contact your child's teacher or CozmicLearning support.</p>
                </div>
            </div>

            <div class="tutorial-tip">
                <strong>💡 Note:</strong> CozmicLearning uses AI moderation to keep learning safe and appropriate.
            </div>
        """
    },

    # ===========================================
    # GENERAL TUTORIALS
    # ===========================================

    "password-reset": {
        "title": "Reset Your Password",
        "icon": "🔑",
        "category": "general",
        "duration": "2 min",
        "difficulty": "Beginner",
        "content": """
            <h2>🔑 Reset Your Password</h2>
            <p>Recover access to your account if you forgot your password.</p>

            <div class="tutorial-steps">
                <div class="tutorial-step">
                    <h4>Step 1: Go to Forgot Password</h4>
                    <p>Navigate to <code>/forgot-password/[role]</code> where role is:</p>
                    <ul>
                        <li>student</li>
                        <li>teacher</li>
                        <li>parent</li>
                    </ul>
                </div>

                <div class="tutorial-step">
                    <h4>Step 2: Enter Your Email</h4>
                    <p>Type the email address associated with your account.</p>
                    <p>Click "Send Reset Link".</p>
                </div>

                <div class="tutorial-step">
                    <h4>Step 3: Check Your Email</h4>
                    <p>You'll receive an email with a password reset link.</p>
                    <p>Click the link to go to <code>/reset-password/[token]</code>.</p>
                </div>

                <div class="tutorial-step">
                    <h4>Step 4: Create New Password</h4>
                    <p>Enter your new password (minimum 8 characters).</p>
                    <p>Confirm it and click "Reset Password".</p>
                </div>

                <div class="tutorial-step">
                    <h4>Step 5: Login with New Password</h4>
                    <p>You can now login with your new credentials!</p>
                </div>
            </div>

            <div class="tutorial-warning">
                <strong>⚠️ Security:</strong> Use a strong, unique password for your account!
            </div>
        """
    },

    "join-class-student": {
        "title": "Join a Class (Student)",
        "icon": "➕",
        "category": "student",
        "duration": "2 min",
        "difficulty": "Beginner",
        "content": """
            <h2>➕ Join a Class</h2>
            <p>Use your teacher's join code to access class assignments.</p>

            <div class="tutorial-steps">
                <div class="tutorial-step">
                    <h4>Step 1: Get Join Code from Teacher</h4>
                    <p>Your teacher will give you an 8-character join code.</p>
                </div>

                <div class="tutorial-step">
                    <h4>Step 2: Navigate to Join Class</h4>
                    <p>Go to <code>/student/join-class</code>.</p>
                </div>

                <div class="tutorial-step">
                    <h4>Step 3: Enter Join Code</h4>
                    <p>Type the join code your teacher gave you.</p>
                    <p>Click "Join Class".</p>
                </div>

                <div class="tutorial-step">
                    <h4>Step 4: You're In!</h4>
                    <p>You'll now see assignments from this class in your assignments list.</p>
                </div>
            </div>

            <div class="tutorial-tip">
                <strong>💡 Pro Tip:</strong> You can join multiple classes if you have multiple teachers!
            </div>
        """
    }
}


def get_tutorial(tutorial_id):
    """Get a specific tutorial by ID"""
    return TUTORIALS.get(tutorial_id, {
        "title": "Tutorial Not Found",
        "content": "<p>This tutorial doesn't exist yet. Check back soon!</p>"
    })


def search_tutorials(query):
    """Search tutorials by query string"""
    query = query.lower()
    results = []

    for tid, tutorial in TUTORIALS.items():
        title = tutorial.get('title', '').lower()
        content = tutorial.get('content', '').lower()
        category = tutorial.get('category', '').lower()

        if query in title or query in content or query in category:
            results.append({
                "id": tid,
                "title": tutorial.get('title'),
                "icon": tutorial.get('icon'),
                "duration": tutorial.get('duration'),
                "difficulty": tutorial.get('difficulty'),
                "category": tutorial.get('category')
            })

    return results


def get_tutorials_by_category(category):
    """Get all tutorials for a specific category"""
    return {
        tid: tutorial
        for tid, tutorial in TUTORIALS.items()
        if tutorial.get('category') == category
    }
