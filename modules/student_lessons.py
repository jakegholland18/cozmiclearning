"""
Student Lessons - Grade-appropriate structured learning content
Provides curated lessons for each subject and grade level with AI follow-up chat
"""

import os
import json
from typing import Dict, List, Optional
from modules.shared_ai import get_client


# Lesson topics organized by subject and grade
LESSON_TOPICS = {
    "num_forge": {
        1: ["Counting to 100", "Addition & Subtraction", "Shapes & Patterns", "Money Basics"],
        2: ["Place Value", "Two-Digit Addition", "Time & Calendar", "Measurement Basics"],
        3: ["Multiplication Tables", "Division Basics", "Fractions Introduction", "Area & Perimeter"],
        4: ["Multi-Digit Multiplication", "Long Division", "Decimals", "Geometry Fundamentals"],
        5: ["Fraction Operations", "Decimal Operations", "Order of Operations", "Volume & Surface Area"],
        6: ["Ratios & Proportions", "Percentages", "Integers", "Coordinate Plane"],
        7: ["Algebraic Expressions", "Solving Equations", "Probability", "Statistics"],
        8: ["Linear Equations", "Systems of Equations", "Functions", "Pythagorean Theorem"],
        9: ["Quadratic Equations", "Polynomials", "Graphing Functions", "Exponential Growth"],
        10: ["Trigonometry Basics", "Advanced Algebra", "Sequences & Series", "Logarithms"],
        11: ["Pre-Calculus", "Trigonometric Functions", "Conic Sections", "Limits"],
        12: ["Calculus Introduction", "Derivatives", "Integrals", "Applications of Calculus"]
    },
    "atom_sphere": {
        1: ["Five Senses", "Living vs Non-Living", "Weather Basics", "Animal Habitats"],
        2: ["Plant Life Cycle", "States of Matter", "Earth & Sky", "Simple Machines"],
        3: ["Ecosystems", "Rocks & Minerals", "Force & Motion", "Human Body Systems"],
        4: ["Energy Forms", "Water Cycle", "Solar System", "Sound & Light"],
        5: ["Cells & Organisms", "Chemical vs Physical Changes", "Space Exploration", "Electricity"],
        6: ["Photosynthesis", "Periodic Table Intro", "Plate Tectonics", "Scientific Method"],
        7: ["Cell Biology", "Atomic Structure", "Climate & Weather", "Simple Machines Deep Dive"],
        8: ["Genetics Basics", "Chemical Reactions", "Earth's Layers", "Newton's Laws"],
        9: ["Evolution & Natural Selection", "Chemical Bonding", "Astronomy", "Energy Transfer"],
        10: ["DNA & Protein Synthesis", "Stoichiometry", "Geology", "Waves & Optics"],
        11: ["Advanced Biology", "Organic Chemistry", "Environmental Science", "Thermodynamics"],
        12: ["AP Biology Topics", "AP Chemistry Topics", "AP Physics Topics", "Biochemistry"]
    },
    "chrono_core": {
        1: ["My Family History", "Holidays & Traditions", "Community Helpers", "Then vs Now"],
        2: ["American Symbols", "Native Americans", "Early Explorers", "Pilgrims & Plymouth"],
        3: ["Colonial America", "American Revolution", "Founding Fathers", "Constitution Basics"],
        4: ["Westward Expansion", "Civil War", "Reconstruction", "Industrial Revolution"],
        5: ["World War I", "Great Depression", "World War II", "Civil Rights Movement"],
        6: ["Ancient Civilizations", "Greek & Roman Empire", "Middle Ages", "Renaissance"],
        7: ["Age of Exploration", "American Colonies Deep Dive", "Revolutionary War Details", "Early Republic"],
        8: ["Manifest Destiny", "Civil War Causes", "Reconstruction Era", "Gilded Age"],
        9: ["Progressive Era", "WWI & WWII", "Cold War", "Vietnam Era"],
        10: ["Ancient World History", "Medieval Europe", "Islamic Golden Age", "Asian Empires"],
        11: ["Modern European History", "World Wars Deep Dive", "Decolonization", "Modern Middle East"],
        12: ["AP US History Topics", "AP World History Topics", "Government & Politics", "Economics History"]
    },
    "story_verse": {
        1: ["Letter Sounds", "Sight Words", "Simple Sentences", "Story Elements"],
        2: ["Reading Fluency", "Main Idea", "Character Analysis", "Sequencing Events"],
        3: ["Context Clues", "Cause & Effect", "Compare & Contrast", "Fiction vs Non-Fiction"],
        4: ["Theme Identification", "Point of View", "Literary Devices", "Summarizing"],
        5: ["Inference Skills", "Author's Purpose", "Text Structure", "Vocabulary Building"],
        6: ["Complex Texts", "Figurative Language", "Textual Evidence", "Critical Reading"],
        7: ["Literary Analysis", "Poetry Analysis", "Drama & Plays", "Research Skills"],
        8: ["Advanced Comprehension", "Rhetoric & Persuasion", "Media Literacy", "Annotating Texts"],
        9: ["Classic Literature", "Modern Fiction", "Non-Fiction Analysis", "Argument Analysis"],
        10: ["World Literature", "Literary Criticism", "Advanced Poetry", "Comparative Reading"],
        11: ["British Literature", "American Literature", "Literary Theory", "Advanced Rhetoric"],
        12: ["AP Literature Topics", "College-Level Reading", "Critical Theory", "Research Methods"]
    },
    "ink_haven": {
        1: ["Writing Letters", "Simple Sentences", "Personal Narratives", "Drawing & Labels"],
        2: ["Paragraph Writing", "Descriptive Writing", "Opinion Writing", "Grammar Basics"],
        3: ["Essay Structure", "Creative Stories", "Informative Writing", "Editing Skills"],
        4: ["Multi-Paragraph Essays", "Research Reports", "Persuasive Writing", "Dialogue Writing"],
        5: ["Five-Paragraph Essay", "Compare/Contrast Essays", "Narrative Techniques", "Revising Strategies"],
        6: ["Argumentative Writing", "Literary Analysis", "Research Papers", "Citation Basics"],
        7: ["Advanced Essays", "Creative Writing", "Technical Writing", "Peer Review"],
        8: ["Rhetorical Analysis", "Synthesis Essays", "Personal Essays", "Advanced Grammar"],
        9: ["College Essay Prep", "Analytical Writing", "Research Methods", "Style & Voice"],
        10: ["Advanced Rhetoric", "Literary Criticism Writing", "Argumentative Mastery", "Publication"],
        11: ["AP Language Topics", "College Writing", "Creative Non-Fiction", "Advanced Research"],
        12: ["AP Literature Writing", "Thesis Development", "Academic Writing", "Professional Writing"]
    },
    "faith_realm": {
        1: ["God's Love", "Creation Story", "Jesus' Birth", "Prayer Basics"],
        2: ["Bible Stories", "Ten Commandments", "Psalms for Kids", "Fruits of the Spirit"],
        3: ["Old Testament Heroes", "Jesus' Miracles", "Parables", "Christian Character"],
        4: ["Life of Jesus", "New Testament Stories", "Christian Living", "Bible Study Skills"],
        5: ["Books of the Bible", "Gospels Overview", "Epistles Introduction", "Worship & Praise"],
        6: ["Bible Timeline", "Covenant Theology", "Christian Worldview", "Apologetics Intro"],
        7: ["Systematic Theology Basics", "Church History", "Doctrine Fundamentals", "Christian Ethics"],
        8: ["Theology Deep Dive", "Reformation History", "Biblical Interpretation", "Spiritual Disciplines"],
        9: ["Advanced Apologetics", "Philosophy & Faith", "World Religions", "Christian Leadership"],
        10: ["Theology II", "Biblical Languages Intro", "Missions & Evangelism", "Christian Apologetics"],
        11: ["Systematic Theology III", "Biblical Exegesis", "Christian Philosophy", "Ministry Prep"],
        12: ["Advanced Theology", "Hermeneutics", "Apologetics Mastery", "Vocational Ministry"]
    },
    "coin_quest": {
        3: ["Counting Money", "Saving vs Spending", "Needs vs Wants", "Earning Money"],
        4: ["Budgeting Basics", "Making Change", "Banks & Savings", "Giving & Tithing"],
        5: ["Income & Expenses", "Simple Budgets", "Interest Basics", "Financial Goals"],
        6: ["Banking Fundamentals", "Credit vs Debit", "Budgeting Skills", "Earning Strategies"],
        7: ["Financial Planning", "Compound Interest", "Checking Accounts", "Smart Shopping"],
        8: ["Credit Basics", "Loans & Debt", "Building Wealth", "Career & Income"],
        9: ["Personal Finance", "Credit Scores", "Insurance Basics", "Taxes Introduction"],
        10: ["Advanced Budgeting", "Retirement Planning Intro", "Real Estate Basics", "Entrepreneurship"],
        11: ["Investment Basics", "Financial Independence", "College Financing", "Career Planning"],
        12: ["Advanced Personal Finance", "Investment Strategies", "Tax Planning", "Wealth Building"]
    },
    "stock_star": {
        6: ["What Are Stocks?", "Supply & Demand", "Business Basics", "Saving vs Investing"],
        7: ["Stock Market Intro", "Bulls & Bears", "Risk & Reward", "Company Research"],
        8: ["Stock Types", "Market Indices", "Portfolio Basics", "Economic Indicators"],
        9: ["Investment Strategies", "Bonds & Securities", "Diversification", "Market Analysis"],
        10: ["Advanced Investing", "Options & Futures Intro", "Economic Cycles", "Global Markets"],
        11: ["Portfolio Management", "Technical Analysis", "Fundamental Analysis", "Investment Psychology"],
        12: ["Advanced Trading", "Alternative Investments", "Financial Planning", "Wealth Management"]
    },
    "truth_forge": {
        6: ["What is Truth?", "Logic Basics", "Critical Thinking", "Christian Worldview"],
        7: ["Arguments & Evidence", "Logical Fallacies", "Defending Your Faith", "Science & Faith"],
        8: ["Philosophy Introduction", "Worldview Comparison", "Moral Reasoning", "Apologetics Methods"],
        9: ["Classical Apologetics", "Presuppositional Apologetics", "Evidential Apologetics", "Cultural Engagement"],
        10: ["Advanced Philosophy", "Atheism & Skepticism", "World Religions", "Christian Philosophers"],
        11: ["Theological Apologetics", "Historical Jesus", "Problem of Evil", "Resurrection Evidence"],
        12: ["Apologetics Mastery", "Contemporary Issues", "Postmodernism", "Public Defense"]
    },
    "terra_nova": {
        1: ["Maps & Globes", "Continents & Oceans", "My Community", "Landforms"],
        2: ["US Geography", "State Capitals", "Climate Zones", "Natural Resources"],
        3: ["World Geography", "Countries & Cultures", "Physical Features", "Human Geography"],
        4: ["North America Deep Dive", "South America", "Europe", "Africa"],
        5: ["Asia", "Australia & Oceania", "Antarctica", "World Cultures"],
        6: ["Geographic Regions", "Population & Migration", "Economic Geography", "Political Geography"],
        7: ["Physical Geography", "Climate & Biomes", "Natural Disasters", "Environmental Issues"],
        8: ["Human Geography", "Urbanization", "Cultural Geography", "Geopolitics"],
        9: ["Regional Studies", "Development Geography", "Globalization", "Geographic Technologies"],
        10: ["Advanced Physical Geography", "Cultural Landscapes", "Political Borders", "Resource Management"],
        11: ["Geographic Analysis", "Spatial Patterns", "Geographic Research", "Global Issues"],
        12: ["AP Human Geography Topics", "Geographic Thought", "Advanced GIS", "Sustainability"]
    },
    "power_grid": {
        6: ["Goal Setting", "Time Management", "Study Skills", "Responsibility"],
        7: ["Career Exploration", "Communication Skills", "Teamwork", "Problem Solving"],
        8: ["Leadership Basics", "Financial Literacy", "Work Ethic", "Digital Citizenship"],
        9: ["Career Planning", "Resume Building", "Interview Skills", "Networking"],
        10: ["College Preparation", "SAT/ACT Prep", "Scholarship Research", "Career Paths"],
        11: ["College Applications", "Career Readiness", "Professional Skills", "Life Planning"],
        12: ["Transition to Adulthood", "Job Search Strategies", "Financial Independence", "Life Skills Mastery"]
    },
    "respect_realm": {
        1: ["Kindness", "Sharing", "Following Rules", "Good Manners"],
        2: ["Honesty", "Respect for Others", "Self-Control", "Gratitude"],
        3: ["Responsibility", "Perseverance", "Empathy", "Courage"],
        4: ["Integrity", "Compassion", "Patience", "Forgiveness"],
        5: ["Leadership Qualities", "Citizenship", "Diligence", "Humility"],
        6: ["Character Building", "Moral Reasoning", "Service & Volunteering", "Conflict Resolution"],
        7: ["Emotional Intelligence", "Decision Making", "Peer Pressure", "Self-Discipline"],
        8: ["Identity & Values", "Social Responsibility", "Media Discernment", "Healthy Relationships"],
        9: ["Ethics & Morality", "Critical Choices", "Influence & Impact", "Personal Growth"],
        10: ["Character Leadership", "Moral Courage", "Social Justice", "Purpose & Calling"],
        11: ["Advanced Ethics", "Cultural Competence", "Servant Leadership", "Legacy Building"],
        12: ["Character Mastery", "Life Philosophy", "Mentoring Others", "Impact Planning"]
    }
}


# NEW: Hierarchical Chapter Structure for Structured Lesson Mode
# Each subject has chapters organized by grade level
# Each chapter contains 4-6 lessons in a logical progression
LESSON_CHAPTERS = {
    "num_forge": {
        "K": {
            "chapters": [
                {
                    "id": "numbers_0_10",
                    "title": "Numbers 0-10",
                    "description": "Learn to count and recognize numbers from 0 to 10",
                    "icon": "🔢",
                    "color": "purple",
                    "lessons": [
                        "Counting Objects 1-5",
                        "Counting Objects 6-10",
                        "Writing Numbers 0-10",
                        "Number Order and Patterns"
                    ]
                },
                {
                    "id": "shapes_colors",
                    "title": "Shapes & Colors",
                    "description": "Identify basic shapes and colors",
                    "icon": "🔷",
                    "color": "blue",
                    "lessons": [
                        "Circles and Squares",
                        "Triangles and Rectangles",
                        "Colors All Around",
                        "Sorting by Shape and Color"
                    ]
                },
                {
                    "id": "comparing_k",
                    "title": "Comparing & Sorting",
                    "description": "Learn to compare sizes and sort objects",
                    "icon": "⚖️",
                    "color": "green",
                    "lessons": [
                        "Big and Small",
                        "More and Less",
                        "Same and Different",
                        "Sorting Fun"
                    ]
                }
            ]
        },
        1: {
            "chapters": [
                {
                    "id": "counting_basics",
                    "title": "Counting & Number Sense",
                    "description": "Master counting, number recognition, and understanding quantities",
                    "icon": "🔢",
                    "color": "purple",
                    "lessons": [
                        "Numbers 1-20",
                        "Counting to 100",
                        "Comparing Numbers (Greater/Less)",
                        "Number Patterns"
                    ]
                },
                {
                    "id": "addition_intro",
                    "title": "Beginning Addition",
                    "description": "Learn to add numbers together and solve simple problems",
                    "icon": "➕",
                    "color": "blue",
                    "lessons": [
                        "What is Addition?",
                        "Adding Within 10",
                        "Adding Within 20",
                        "Addition Word Problems"
                    ]
                },
                {
                    "id": "subtraction_intro",
                    "title": "Beginning Subtraction",
                    "description": "Understand taking away and finding the difference",
                    "icon": "➖",
                    "color": "green",
                    "lessons": [
                        "What is Subtraction?",
                        "Subtracting Within 10",
                        "Subtracting Within 20",
                        "Subtraction Word Problems"
                    ]
                },
                {
                    "id": "shapes_patterns",
                    "title": "Shapes & Patterns",
                    "description": "Explore 2D shapes and create patterns",
                    "icon": "🔷",
                    "color": "orange",
                    "lessons": [
                        "Basic 2D Shapes",
                        "Comparing Shapes",
                        "Creating Patterns",
                        "Extending Patterns"
                    ]
                }
            ]
        },
        2: {
            "chapters": [
                {
                    "id": "place_value_2",
                    "title": "Place Value Discovery",
                    "description": "Understand tens and ones in two-digit numbers",
                    "icon": "💯",
                    "color": "purple",
                    "lessons": [
                        "Understanding Tens and Ones",
                        "Building Two-Digit Numbers",
                        "Expanded Form",
                        "Comparing Two-Digit Numbers"
                    ]
                },
                {
                    "id": "addition_2digit",
                    "title": "Two-Digit Addition",
                    "description": "Add larger numbers with and without regrouping",
                    "icon": "➕",
                    "color": "blue",
                    "lessons": [
                        "Adding Without Regrouping",
                        "Adding With Regrouping",
                        "Addition Strategies",
                        "Word Problem Solving"
                    ]
                },
                {
                    "id": "time_calendar",
                    "title": "Time & Calendar",
                    "description": "Learn to tell time and understand calendars",
                    "icon": "🕐",
                    "color": "green",
                    "lessons": [
                        "Telling Time to the Hour",
                        "Telling Time to Half Hour",
                        "Days, Weeks, and Months",
                        "Reading Calendars"
                    ]
                },
                {
                    "id": "measurement_2",
                    "title": "Measurement Basics",
                    "description": "Measure length, weight, and capacity",
                    "icon": "📏",
                    "color": "orange",
                    "lessons": [
                        "Measuring Length",
                        "Measuring Weight",
                        "Measuring Capacity",
                        "Choosing Tools"
                    ]
                }
            ]
        },
        3: {
            "chapters": [
                {
                    "id": "mult_mastery",
                    "title": "Multiplication Mastery",
                    "description": "Learn multiplication fundamentals and master times tables",
                    "icon": "✖️",
                    "color": "purple",
                    "lessons": [
                        "What is Multiplication?",
                        "Multiplication by 2s and 5s",
                        "Multiplication by 3s and 4s",
                        "Multiplication by 10s and 100s",
                        "Multiplication Tables (6-9)",
                        "Multiplication Word Problems"
                    ]
                },
                {
                    "id": "division_intro",
                    "title": "Understanding Division",
                    "description": "Discover division and learn to share equally",
                    "icon": "➗",
                    "color": "blue",
                    "prerequisite": "mult_mastery",
                    "lessons": [
                        "Division as Sharing",
                        "Division and Multiplication Connection",
                        "Division Facts (÷2, ÷5, ÷10)",
                        "Division with Remainders",
                        "Division Word Problems"
                    ]
                },
                {
                    "id": "fractions_begin",
                    "title": "Fraction Foundations",
                    "description": "Explore fractions and parts of a whole",
                    "icon": "🍕",
                    "color": "orange",
                    "lessons": [
                        "What Are Fractions?",
                        "Fractions on a Number Line",
                        "Comparing Fractions",
                        "Equivalent Fractions",
                        "Adding Like Fractions",
                        "Subtracting Like Fractions"
                    ]
                },
                {
                    "id": "measurement_geo",
                    "title": "Measurement & Geometry",
                    "description": "Learn about area, perimeter, and shapes",
                    "icon": "📏",
                    "color": "green",
                    "lessons": [
                        "Understanding Perimeter",
                        "Calculating Perimeter",
                        "Introduction to Area",
                        "Finding Area of Rectangles",
                        "Real-World Measurement"
                    ]
                }
            ]
        },
        4: {
            "chapters": [
                {
                    "id": "multidigit_mult",
                    "title": "Multi-Digit Multiplication",
                    "description": "Multiply larger numbers using strategies",
                    "icon": "✖️",
                    "color": "purple",
                    "lessons": [
                        "Multiplying by 10, 100, 1000",
                        "Two-Digit × One-Digit",
                        "Two-Digit × Two-Digit",
                        "Multiplication Estimation",
                        "Real-World Multiplication"
                    ]
                },
                {
                    "id": "long_division",
                    "title": "Long Division",
                    "description": "Master division with larger numbers",
                    "icon": "➗",
                    "color": "blue",
                    "lessons": [
                        "Division Steps",
                        "One-Digit Divisors",
                        "Remainders in Division",
                        "Division Estimation",
                        "Division Applications"
                    ]
                },
                {
                    "id": "decimals_intro",
                    "title": "Introduction to Decimals",
                    "description": "Understand decimal numbers and place value",
                    "icon": "🔸",
                    "color": "green",
                    "lessons": [
                        "Decimal Place Value",
                        "Comparing Decimals",
                        "Rounding Decimals",
                        "Adding Decimals",
                        "Subtracting Decimals"
                    ]
                },
                {
                    "id": "geometry_fund",
                    "title": "Geometry Fundamentals",
                    "description": "Explore angles, shapes, and symmetry",
                    "icon": "📐",
                    "color": "orange",
                    "lessons": [
                        "Types of Angles",
                        "Lines and Line Segments",
                        "Triangles and Quadrilaterals",
                        "Symmetry and Reflections"
                    ]
                }
            ]
        },
        5: {
            "chapters": [
                {
                    "id": "fraction_ops",
                    "title": "Fraction Operations",
                    "description": "Add, subtract, multiply, and divide fractions",
                    "icon": "🍕",
                    "color": "purple",
                    "lessons": [
                        "Adding Unlike Fractions",
                        "Subtracting Unlike Fractions",
                        "Multiplying Fractions",
                        "Dividing Fractions",
                        "Mixed Number Operations"
                    ]
                },
                {
                    "id": "decimal_ops",
                    "title": "Decimal Operations",
                    "description": "Compute with decimals confidently",
                    "icon": "🔸",
                    "color": "blue",
                    "lessons": [
                        "Multiplying Decimals",
                        "Dividing Decimals",
                        "Converting Fractions to Decimals",
                        "Decimal Word Problems"
                    ]
                },
                {
                    "id": "order_operations",
                    "title": "Order of Operations",
                    "description": "Learn PEMDAS and solve complex expressions",
                    "icon": "🎯",
                    "color": "green",
                    "lessons": [
                        "Introduction to PEMDAS",
                        "Parentheses and Brackets",
                        "Multi-Step Problems",
                        "Real-World Applications"
                    ]
                },
                {
                    "id": "volume_surface",
                    "title": "Volume & Surface Area",
                    "description": "Calculate 3D measurements",
                    "icon": "📦",
                    "color": "orange",
                    "lessons": [
                        "Understanding Volume",
                        "Volume of Rectangular Prisms",
                        "Surface Area Basics",
                        "Real-World 3D Problems"
                    ]
                }
            ]
        },
        6: {
            "chapters": [
                {
                    "id": "ratios_proportions",
                    "title": "Ratios & Proportions",
                    "description": "Compare quantities and solve proportion problems",
                    "icon": "⚖️",
                    "color": "purple",
                    "lessons": [
                        "Understanding Ratios",
                        "Equivalent Ratios",
                        "Solving Proportions",
                        "Scale Drawings",
                        "Ratio Word Problems"
                    ]
                },
                {
                    "id": "percentages",
                    "title": "Percentages",
                    "description": "Master percent calculations and applications",
                    "icon": "%",
                    "color": "blue",
                    "lessons": [
                        "Percent Basics",
                        "Percent of a Number",
                        "Discounts and Sales Tax",
                        "Percent Increase/Decrease"
                    ]
                },
                {
                    "id": "integers",
                    "title": "Integers & Negative Numbers",
                    "description": "Work with positive and negative numbers",
                    "icon": "➖➕",
                    "color": "green",
                    "lessons": [
                        "Understanding Integers",
                        "Adding Integers",
                        "Subtracting Integers",
                        "Multiplying and Dividing Integers"
                    ]
                },
                {
                    "id": "coordinate_plane",
                    "title": "Coordinate Plane",
                    "description": "Plot points and graph on a coordinate system",
                    "icon": "📊",
                    "color": "orange",
                    "lessons": [
                        "The Coordinate Plane",
                        "Plotting Points",
                        "Graphing Shapes",
                        "Distance on the Plane"
                    ]
                }
            ]
        },
        7: {
            "chapters": [
                {
                    "id": "algebraic_expressions",
                    "title": "Algebraic Expressions",
                    "description": "Work with variables and expressions",
                    "icon": "🔤",
                    "color": "purple",
                    "lessons": [
                        "Variables and Constants",
                        "Writing Expressions",
                        "Evaluating Expressions",
                        "Combining Like Terms",
                        "Distributive Property"
                    ]
                },
                {
                    "id": "solving_equations",
                    "title": "Solving Equations",
                    "description": "Find unknown values in equations",
                    "icon": "🎯",
                    "color": "blue",
                    "lessons": [
                        "One-Step Equations",
                        "Two-Step Equations",
                        "Multi-Step Equations",
                        "Equations with Variables on Both Sides"
                    ]
                },
                {
                    "id": "probability_7",
                    "title": "Probability",
                    "description": "Calculate chances and likelihood",
                    "icon": "🎲",
                    "color": "green",
                    "lessons": [
                        "Probability Basics",
                        "Experimental vs Theoretical",
                        "Compound Events",
                        "Probability Applications"
                    ]
                },
                {
                    "id": "statistics_7",
                    "title": "Statistics",
                    "description": "Analyze data and find patterns",
                    "icon": "📈",
                    "color": "orange",
                    "lessons": [
                        "Mean, Median, Mode",
                        "Range and Outliers",
                        "Data Displays",
                        "Interpreting Graphs"
                    ]
                }
            ]
        },
        8: {
            "chapters": [
                {
                    "id": "linear_equations",
                    "title": "Linear Equations",
                    "description": "Master equations of lines",
                    "icon": "📐",
                    "color": "purple",
                    "lessons": [
                        "Slope and Rate of Change",
                        "Slope-Intercept Form",
                        "Point-Slope Form",
                        "Graphing Linear Equations",
                        "Writing Linear Equations"
                    ]
                },
                {
                    "id": "systems_equations",
                    "title": "Systems of Equations",
                    "description": "Solve multiple equations together",
                    "icon": "🔗",
                    "color": "blue",
                    "lessons": [
                        "Solving by Graphing",
                        "Solving by Substitution",
                        "Solving by Elimination",
                        "Systems Word Problems"
                    ]
                },
                {
                    "id": "functions",
                    "title": "Functions",
                    "description": "Understand input-output relationships",
                    "icon": "ƒ",
                    "color": "green",
                    "lessons": [
                        "What is a Function?",
                        "Function Notation",
                        "Evaluating Functions",
                        "Domain and Range"
                    ]
                },
                {
                    "id": "pythagorean",
                    "title": "Pythagorean Theorem",
                    "description": "Apply the famous triangle formula",
                    "icon": "📏",
                    "color": "orange",
                    "lessons": [
                        "Understanding the Theorem",
                        "Finding Missing Sides",
                        "Pythagorean Triples",
                        "Real-World Applications"
                    ]
                }
            ]
        },
        9: {
            "chapters": [
                {
                    "id": "quadratic_equations",
                    "title": "Quadratic Equations",
                    "description": "Solve equations with x²",
                    "icon": "x²",
                    "color": "purple",
                    "lessons": [
                        "Quadratic Basics",
                        "Factoring Quadratics",
                        "Quadratic Formula",
                        "Completing the Square",
                        "Graphing Parabolas"
                    ]
                },
                {
                    "id": "polynomials",
                    "title": "Polynomials",
                    "description": "Work with multi-term expressions",
                    "icon": "📐",
                    "color": "blue",
                    "lessons": [
                        "Adding and Subtracting Polynomials",
                        "Multiplying Polynomials",
                        "Factoring Polynomials",
                        "Polynomial Division"
                    ]
                },
                {
                    "id": "graphing_functions",
                    "title": "Graphing Functions",
                    "description": "Visualize different function types",
                    "icon": "📊",
                    "color": "green",
                    "lessons": [
                        "Linear Functions Review",
                        "Quadratic Functions",
                        "Absolute Value Functions",
                        "Exponential Functions"
                    ]
                },
                {
                    "id": "exponential_growth",
                    "title": "Exponential Growth & Decay",
                    "description": "Model real-world change",
                    "icon": "📈",
                    "color": "orange",
                    "lessons": [
                        "Exponential Growth",
                        "Exponential Decay",
                        "Growth Models",
                        "Real-World Applications"
                    ]
                }
            ]
        },
        10: {
            "chapters": [
                {
                    "id": "trig_basics",
                    "title": "Trigonometry Basics",
                    "description": "Learn sine, cosine, and tangent",
                    "icon": "📐",
                    "color": "purple",
                    "lessons": [
                        "Right Triangle Trigonometry",
                        "SOH-CAH-TOA",
                        "Finding Missing Sides",
                        "Finding Missing Angles",
                        "Trig Word Problems"
                    ]
                },
                {
                    "id": "advanced_algebra",
                    "title": "Advanced Algebra",
                    "description": "Master complex algebraic concepts",
                    "icon": "🔤",
                    "color": "blue",
                    "lessons": [
                        "Rational Expressions",
                        "Radical Expressions",
                        "Complex Numbers",
                        "Advanced Factoring"
                    ]
                },
                {
                    "id": "sequences_series",
                    "title": "Sequences & Series",
                    "description": "Explore patterns in numbers",
                    "icon": "🔢",
                    "color": "green",
                    "lessons": [
                        "Arithmetic Sequences",
                        "Geometric Sequences",
                        "Series and Summation",
                        "Applications"
                    ]
                },
                {
                    "id": "logarithms",
                    "title": "Logarithms",
                    "description": "Understand inverse of exponents",
                    "icon": "log",
                    "color": "orange",
                    "lessons": [
                        "Introduction to Logarithms",
                        "Logarithm Properties",
                        "Solving Logarithmic Equations",
                        "Applications of Logarithms"
                    ]
                }
            ]
        },
        11: {
            "chapters": [
                {
                    "id": "precalc_functions",
                    "title": "Pre-Calculus Functions",
                    "description": "Advanced function analysis",
                    "icon": "ƒ",
                    "color": "purple",
                    "lessons": [
                        "Function Transformations",
                        "Inverse Functions",
                        "Rational Functions",
                        "Piecewise Functions",
                        "Function Composition"
                    ]
                },
                {
                    "id": "trig_functions",
                    "title": "Trigonometric Functions",
                    "description": "Master the unit circle and trig identities",
                    "icon": "⭕",
                    "color": "blue",
                    "lessons": [
                        "Unit Circle",
                        "Trig Identities",
                        "Graphing Trig Functions",
                        "Inverse Trig Functions"
                    ]
                },
                {
                    "id": "conic_sections",
                    "title": "Conic Sections",
                    "description": "Study circles, ellipses, parabolas, hyperbolas",
                    "icon": "⚪",
                    "color": "green",
                    "lessons": [
                        "Circles",
                        "Ellipses",
                        "Parabolas",
                        "Hyperbolas"
                    ]
                },
                {
                    "id": "limits",
                    "title": "Introduction to Limits",
                    "description": "Prepare for calculus",
                    "icon": "∞",
                    "color": "orange",
                    "lessons": [
                        "What is a Limit?",
                        "Evaluating Limits",
                        "Limits at Infinity",
                        "Continuity"
                    ]
                }
            ]
        },
        12: {
            "chapters": [
                {
                    "id": "calc_intro",
                    "title": "Calculus Introduction",
                    "description": "Begin your calculus journey",
                    "icon": "∫",
                    "color": "purple",
                    "lessons": [
                        "Limits Review",
                        "Continuity and Differentiability",
                        "Introduction to Derivatives",
                        "Rates of Change"
                    ]
                },
                {
                    "id": "derivatives",
                    "title": "Derivatives",
                    "description": "Master differentiation",
                    "icon": "d/dx",
                    "color": "blue",
                    "lessons": [
                        "Power Rule",
                        "Product and Quotient Rules",
                        "Chain Rule",
                        "Implicit Differentiation",
                        "Applications of Derivatives"
                    ]
                },
                {
                    "id": "integrals",
                    "title": "Integrals",
                    "description": "Learn integration techniques",
                    "icon": "∫",
                    "color": "green",
                    "lessons": [
                        "Antiderivatives",
                        "Definite Integrals",
                        "Fundamental Theorem of Calculus",
                        "Integration Techniques",
                        "Applications of Integrals"
                    ]
                },
                {
                    "id": "calc_applications",
                    "title": "Applications of Calculus",
                    "description": "Apply calculus to real problems",
                    "icon": "🎯",
                    "color": "orange",
                    "lessons": [
                        "Optimization Problems",
                        "Related Rates",
                        "Area and Volume",
                        "Physics Applications"
                    ]
                }
            ]
        }
    },
    "coin_quest": {
        3: {
            "chapters": [
                {
                    "id": "money_recognition",
                    "title": "Coins & Bills",
                    "description": "Learn to identify and count money",
                    "icon": "💰",
                    "color": "purple",
                    "lessons": [
                        "Penny, Nickel, Dime, Quarter",
                        "Counting Coins",
                        "Dollar Bills",
                        "Making Amounts"
                    ]
                },
                {
                    "id": "saving_spending",
                    "title": "Save or Spend?",
                    "description": "Make smart money choices",
                    "icon": "🏦",
                    "color": "blue",
                    "lessons": [
                        "What is Saving?",
                        "What is Spending?",
                        "Piggy Bank Goals",
                        "Wise Choices"
                    ]
                },
                {
                    "id": "needs_wants",
                    "title": "Needs vs Wants",
                    "description": "Understand the difference",
                    "icon": "🎯",
                    "color": "green",
                    "lessons": [
                        "What Are Needs?",
                        "What Are Wants?",
                        "Making Good Choices",
                        "Priority Practice"
                    ]
                },
                {
                    "id": "earning_money",
                    "title": "Earning Money",
                    "description": "Learn how people earn money",
                    "icon": "💵",
                    "color": "orange",
                    "lessons": [
                        "Jobs and Work",
                        "Chores for Money",
                        "Being Responsible",
                        "Earning Goals"
                    ]
                }
            ]
        },
        4: {
            "chapters": [
                {
                    "id": "budgeting_basics",
                    "title": "Budgeting Basics",
                    "description": "Learn to plan spending",
                    "icon": "📊",
                    "color": "purple",
                    "lessons": [
                        "What is a Budget?",
                        "Income and Expenses",
                        "Simple Budget Planning",
                        "Tracking Money"
                    ]
                },
                {
                    "id": "making_change",
                    "title": "Making Change",
                    "description": "Calculate change from purchases",
                    "icon": "💱",
                    "color": "blue",
                    "lessons": [
                        "Counting Up Method",
                        "Subtraction Method",
                        "Real Shopping Practice",
                        "Money Math Games"
                    ]
                },
                {
                    "id": "banks_savings",
                    "title": "Banks & Savings",
                    "description": "Understand how banks work",
                    "icon": "🏦",
                    "color": "green",
                    "lessons": [
                        "What Banks Do",
                        "Savings Accounts",
                        "Deposits and Withdrawals",
                        "Interest Introduction"
                    ]
                },
                {
                    "id": "giving_tithing",
                    "title": "Giving & Tithing",
                    "description": "Learn about generosity",
                    "icon": "🎁",
                    "color": "orange",
                    "lessons": [
                        "Why We Give",
                        "Biblical Generosity",
                        "Tithing Basics",
                        "Helping Others"
                    ]
                }
            ]
        },
        5: {
            "chapters": [
                {
                    "id": "income_expenses",
                    "title": "Income & Expenses",
                    "description": "Track money in and out",
                    "icon": "💰",
                    "color": "purple",
                    "lessons": [
                        "Types of Income",
                        "Fixed vs Variable Expenses",
                        "Calculating Net Income",
                        "Expense Tracking"
                    ]
                },
                {
                    "id": "simple_budgets",
                    "title": "Creating Budgets",
                    "description": "Make your own budget",
                    "icon": "📝",
                    "color": "blue",
                    "lessons": [
                        "Budget Categories",
                        "Allocating Money",
                        "50/30/20 Rule Intro",
                        "Budget Practice"
                    ]
                },
                {
                    "id": "interest_basics",
                    "title": "Interest Basics",
                    "description": "Learn how money grows",
                    "icon": "📈",
                    "color": "green",
                    "lessons": [
                        "What is Interest?",
                        "Simple Interest",
                        "Earning Interest",
                        "Interest Calculations"
                    ]
                },
                {
                    "id": "financial_goals",
                    "title": "Financial Goals",
                    "description": "Plan for the future",
                    "icon": "🎯",
                    "color": "orange",
                    "lessons": [
                        "Short-Term Goals",
                        "Long-Term Goals",
                        "Saving Strategies",
                        "Goal Achievement"
                    ]
                }
            ]
        },
        6: {
            "chapters": [
                {
                    "id": "banking_fundamentals",
                    "title": "Banking Fundamentals",
                    "description": "Master banking basics",
                    "icon": "🏦",
                    "color": "purple",
                    "lessons": [
                        "Types of Bank Accounts",
                        "Checking Accounts",
                        "Savings Accounts",
                        "Online Banking"
                    ]
                },
                {
                    "id": "credit_debit",
                    "title": "Credit vs Debit",
                    "description": "Understand payment methods",
                    "icon": "💳",
                    "color": "blue",
                    "lessons": [
                        "Debit Cards",
                        "Credit Cards",
                        "Pros and Cons",
                        "Responsible Use"
                    ]
                },
                {
                    "id": "budgeting_skills",
                    "title": "Advanced Budgeting",
                    "description": "Improve budget skills",
                    "icon": "📊",
                    "color": "green",
                    "lessons": [
                        "Zero-Based Budgeting",
                        "Envelope Method",
                        "Budget Adjustments",
                        "Real-Life Practice"
                    ]
                },
                {
                    "id": "earning_strategies",
                    "title": "Earning Strategies",
                    "description": "Ways to make money",
                    "icon": "💵",
                    "color": "orange",
                    "lessons": [
                        "Part-Time Jobs",
                        "Small Business Ideas",
                        "Online Opportunities",
                        "Skill Development"
                    ]
                }
            ]
        }
    }
}


def get_chapters_for_subject_grade(subject: str, grade) -> List[Dict]:
    """Get list of chapters for a subject and grade

    Args:
        subject: Subject key (e.g., 'num_forge')
        grade: Grade level - can be int (1-12) or str ('K')
    """
    if subject not in LESSON_CHAPTERS:
        return []

    # Convert integer grade to check for both int and str keys
    grade_key = grade if isinstance(grade, str) else int(grade)

    if grade_key not in LESSON_CHAPTERS[subject]:
        return []
    return LESSON_CHAPTERS[subject][grade_key].get("chapters", [])


def get_chapter_by_id(subject: str, grade, chapter_id: str) -> Optional[Dict]:
    """Get a specific chapter by its ID

    Args:
        subject: Subject key
        grade: Grade level - can be int (1-12) or str ('K')
        chapter_id: Chapter identifier
    """
    chapters = get_chapters_for_subject_grade(subject, grade)
    for chapter in chapters:
        if chapter.get("id") == chapter_id:
            return chapter
    return None


def get_lessons_for_subject_grade(subject: str, grade: int) -> List[str]:
    """Get list of lesson topics for a subject and grade"""
    if subject not in LESSON_TOPICS:
        return []
    if grade not in LESSON_TOPICS[subject]:
        return []
    return LESSON_TOPICS[subject][grade]


def generate_student_lesson(
    subject: str,
    grade: int,
    topic: str,
    character: str = "everly",
    chapter_id: str = None,
    chapter_context: Dict = None
) -> Dict:
    """
    Generate an engaging, interactive lesson for a student.

    Args:
        subject: Subject key (e.g., "num_forge")
        grade: Grade level (1-12)
        topic: Lesson topic/title
        character: AI mentor character
        chapter_id: Optional chapter ID for context
        chapter_context: Optional dict with chapter title, description, and lesson position

    Returns:
        Dictionary containing lesson content and structure
    """
    from subjects_config import get_subject

    subject_config = get_subject(subject)
    subject_name = subject_config.get("name", subject) if subject_config else subject

    # Character personalities for lesson delivery
    character_styles = {
        "everly": "enthusiastic warrior-princess who makes learning an adventure",
        "jasmine": "curious explorer who discovers knowledge through investigation",
        "lio": "tactical space agent who breaks down complex concepts strategically",
        "theo": "wise scholar who explains deep concepts with patience and clarity",
        "nova": "inventive engineer who builds understanding through hands-on discovery"
    }

    character_style = character_styles.get(character, character_styles["nova"])

    client = get_client()

    # Build chapter context string if provided
    chapter_info = ""
    if chapter_context:
        chapter_title = chapter_context.get("chapter_title", "")
        chapter_desc = chapter_context.get("chapter_description", "")
        lesson_number = chapter_context.get("lesson_number", 1)
        total_lessons = chapter_context.get("total_lessons", 1)
        previous_lessons = chapter_context.get("previous_lessons", [])

        chapter_info = f"""
CHAPTER CONTEXT:
- This lesson is part of the chapter: "{chapter_title}"
- Chapter goal: {chapter_desc}
- This is lesson {lesson_number} of {total_lessons} in this chapter
"""
        if previous_lessons:
            chapter_info += f"- Previous lessons in this chapter: {', '.join(previous_lessons)}\n"

        chapter_info += """
IMPORTANT: Build on the chapter's overall theme and connect this lesson to the chapter's learning progression.
Make sure content is appropriate for lesson {lesson_number} in this sequence.
"""

    prompt = f"""You are {character.title()}, a {character_style}, teaching a Grade {grade} student.

Create an engaging, interactive lesson on "{topic}" for {subject_name}.
{chapter_info}
IMPORTANT GUIDELINES:
- Make it FUN and ENGAGING (use stories, examples, analogies)
- Grade {grade} appropriate language and complexity
- Break complex ideas into simple steps
- Include real-world examples students can relate to
- Use encouraging, supportive tone
- End with thought-provoking questions for discussion
{"- Connect to the chapter theme and build on previous lessons" if chapter_info else ""}

Generate the lesson in this EXACT JSON format (valid JSON only, no markdown):

{{
  "title": "{topic}",
  "hook": "An engaging opening that captures attention and relates to student's life (2-3 sentences)",
  "learning_goal": "What the student will be able to do after this lesson",
  "explanation": "Main teaching content broken into clear sections with examples (use \\n\\n for paragraphs)",
  "key_concepts": [
    "Important concept 1",
    "Important concept 2",
    "Important concept 3"
  ],
  "examples": [
    {{
      "scenario": "Real-world example or problem",
      "solution": "How to solve it or apply the concept"
    }},
    {{
      "scenario": "Another example",
      "solution": "Solution explanation"
    }}
  ],
  "try_it": {{
    "instruction": "A simple practice problem or activity for the student to try",
    "hint": "A helpful hint if they get stuck"
  }},
  "discussion_questions": [
    "Thought-provoking question 1 about the concept",
    "Thought-provoking question 2 about real-world application",
    "Thought-provoking question 3 about deeper understanding"
  ],
  "summary": "Quick recap of main points (2-3 sentences)",
  "encouragement": "Encouraging closing message from {character.title()}"
}}

Make it grade {grade} appropriate, engaging, and educational!"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": f"You are {character.title()}, an enthusiastic AI mentor. Generate engaging lessons in valid JSON format."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=3000,
            timeout=60.0
        )

        response_text = response.choices[0].message.content.strip()

        # Remove markdown code blocks if present
        if response_text.startswith("```"):
            lines = response_text.split("\n")
            response_text = "\n".join(lines[1:-1]) if len(lines) > 2 else response_text
            response_text = response_text.strip()

        lesson_data = json.loads(response_text)

        return {
            "success": True,
            "lesson": lesson_data,
            "subject": subject,
            "grade": grade,
            "character": character
        }

    except json.JSONDecodeError as e:
        print(f"JSON parsing error: {e}")
        return {
            "success": False,
            "error": "Failed to generate lesson. Please try again."
        }
    except Exception as e:
        print(f"Error generating lesson: {e}")
        return {
            "success": False,
            "error": "AI service error. Please try again."
        }


def get_lesson_chat_response(
    lesson_topic: str,
    subject: str,
    grade: int,
    question: str,
    character: str = "everly",
    conversation_history: List[Dict] = None
) -> str:
    """
    Get AI response for follow-up questions about a lesson.

    Args:
        lesson_topic: The lesson topic being discussed
        subject: Subject area
        grade: Student grade level
        question: Student's question
        character: AI mentor character
        conversation_history: Previous conversation messages

    Returns:
        AI response string
    """
    from subjects_config import get_subject

    subject_config = get_subject(subject)
    subject_name = subject_config.get("name", subject) if subject_config else subject

    client = get_client()

    if conversation_history is None:
        conversation_history = []

    system_message = f"""You are {character.title()}, an encouraging AI mentor helping a Grade {grade} student
understand "{lesson_topic}" in {subject_name}.

Guidelines:
- Keep responses clear and grade-appropriate
- Use encouraging, supportive tone
- Break down complex ideas into simple terms
- Provide examples when helpful
- Ask follow-up questions to check understanding
- Praise good questions and effort
- Keep responses concise (2-3 paragraphs max)"""

    messages = [{"role": "system", "content": system_message}]

    # Add conversation history
    for msg in conversation_history:
        messages.append(msg)

    # Add current question
    messages.append({"role": "user", "content": question})

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.7,
            max_tokens=500,
            timeout=30.0
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"Error getting chat response: {e}")
        return "I'm having trouble right now. Please try asking again!"
