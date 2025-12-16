"""
Hierarchical Chapter Structure for CozmicLearning
Defines structured chapter-based learning paths for all subjects across grades K-12
Each chapter contains 4-6 lessons in a logical progression
"""

# Complete chapter structure for all subjects
# Format: subject_key -> grade -> chapters list
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
    },

    "atom_sphere": {
        "K": {
            "chapters": [
                {
                    "id": "five_senses_k",
                    "title": "Five Senses",
                    "description": "Explore how we learn about the world",
                    "icon": "👁️",
                    "color": "purple",
                    "lessons": [
                        "Sight - Using Our Eyes",
                        "Hearing - Using Our Ears",
                        "Touch - Using Our Hands",
                        "Taste and Smell"
                    ]
                },
                {
                    "id": "living_nonliving_k",
                    "title": "Living vs Non-Living",
                    "description": "Discover what makes something alive",
                    "icon": "🌱",
                    "color": "blue",
                    "lessons": [
                        "What is Living?",
                        "What is Non-Living?",
                        "Animals Are Living",
                        "Plants Are Living"
                    ]
                },
                {
                    "id": "weather_basics_k",
                    "title": "Weather Basics",
                    "description": "Learn about sun, rain, and seasons",
                    "icon": "☀️",
                    "color": "green",
                    "lessons": [
                        "Sunny Weather",
                        "Rainy Weather",
                        "The Four Seasons",
                        "Weather Patterns"
                    ]
                }
            ]
        },
        1: {
            "chapters": [
                {
                    "id": "five_senses",
                    "title": "Exploring Our Senses",
                    "description": "Deep dive into the five senses",
                    "icon": "👂",
                    "color": "purple",
                    "lessons": [
                        "How Sight Works",
                        "How Hearing Works",
                        "Touch and Textures",
                        "Taste and Smell Exploration"
                    ]
                },
                {
                    "id": "living_nonliving",
                    "title": "Living Things",
                    "description": "Characteristics of living organisms",
                    "icon": "🐛",
                    "color": "blue",
                    "lessons": [
                        "Needs of Living Things",
                        "Growth and Change",
                        "Animal Classification Basics",
                        "Plant Classification Basics"
                    ]
                },
                {
                    "id": "weather_seasons",
                    "title": "Weather & Seasons",
                    "description": "Understand weather patterns",
                    "icon": "🌦️",
                    "color": "green",
                    "lessons": [
                        "Temperature and Thermometers",
                        "Clouds and Rain",
                        "Seasonal Changes",
                        "Weather Safety"
                    ]
                },
                {
                    "id": "animal_habitats",
                    "title": "Animal Habitats",
                    "description": "Where animals live",
                    "icon": "🏔️",
                    "color": "orange",
                    "lessons": [
                        "Forest Habitats",
                        "Ocean Habitats",
                        "Desert Habitats",
                        "Arctic Habitats"
                    ]
                }
            ]
        },
        2: {
            "chapters": [
                {
                    "id": "plant_life_cycle",
                    "title": "Plant Life Cycles",
                    "description": "How plants grow and reproduce",
                    "icon": "🌻",
                    "color": "purple",
                    "lessons": [
                        "Seed to Sprout",
                        "Growing and Flowering",
                        "Making New Seeds",
                        "Plant Needs: Sun, Water, Air"
                    ]
                },
                {
                    "id": "states_matter",
                    "title": "States of Matter",
                    "description": "Solids, liquids, and gases",
                    "icon": "💧",
                    "color": "blue",
                    "lessons": [
                        "What Are Solids?",
                        "What Are Liquids?",
                        "What Are Gases?",
                        "Changing States"
                    ]
                },
                {
                    "id": "earth_sky",
                    "title": "Earth & Sky",
                    "description": "Learn about our planet and space",
                    "icon": "🌍",
                    "color": "green",
                    "lessons": [
                        "Earth's Land and Water",
                        "Day and Night",
                        "The Moon",
                        "Stars and Constellations"
                    ]
                },
                {
                    "id": "simple_machines_2",
                    "title": "Simple Machines",
                    "description": "Tools that help us work",
                    "icon": "⚙️",
                    "color": "orange",
                    "lessons": [
                        "Levers",
                        "Wheels and Axles",
                        "Ramps (Inclined Planes)",
                        "Pulleys"
                    ]
                }
            ]
        },
        3: {
            "chapters": [
                {
                    "id": "ecosystems",
                    "title": "Ecosystems",
                    "description": "How living things interact",
                    "icon": "🌳",
                    "color": "purple",
                    "lessons": [
                        "What is an Ecosystem?",
                        "Food Chains",
                        "Food Webs",
                        "Producers and Consumers",
                        "Decomposers"
                    ]
                },
                {
                    "id": "rocks_minerals",
                    "title": "Rocks & Minerals",
                    "description": "Earth's building blocks",
                    "icon": "⛰️",
                    "color": "blue",
                    "lessons": [
                        "Types of Rocks",
                        "The Rock Cycle",
                        "Minerals and Crystals",
                        "Soil Formation"
                    ]
                },
                {
                    "id": "force_motion",
                    "title": "Force & Motion",
                    "description": "How things move",
                    "icon": "🚀",
                    "color": "green",
                    "lessons": [
                        "Push and Pull",
                        "Gravity",
                        "Friction",
                        "Magnetism"
                    ]
                },
                {
                    "id": "human_body",
                    "title": "Human Body Systems",
                    "description": "How our body works",
                    "icon": "🫀",
                    "color": "orange",
                    "lessons": [
                        "Skeletal System",
                        "Muscular System",
                        "Digestive System",
                        "Circulatory System"
                    ]
                }
            ]
        },
        4: {
            "chapters": [
                {
                    "id": "energy_forms",
                    "title": "Forms of Energy",
                    "description": "Different types of energy",
                    "icon": "⚡",
                    "color": "purple",
                    "lessons": [
                        "What is Energy?",
                        "Heat Energy",
                        "Light Energy",
                        "Sound Energy",
                        "Energy Transfer"
                    ]
                },
                {
                    "id": "water_cycle",
                    "title": "The Water Cycle",
                    "description": "How water moves on Earth",
                    "icon": "💧",
                    "color": "blue",
                    "lessons": [
                        "Evaporation",
                        "Condensation",
                        "Precipitation",
                        "Collection and the Cycle"
                    ]
                },
                {
                    "id": "solar_system",
                    "title": "Our Solar System",
                    "description": "Planets and space",
                    "icon": "🪐",
                    "color": "green",
                    "lessons": [
                        "The Sun",
                        "Inner Planets",
                        "Outer Planets",
                        "Moons and Asteroids"
                    ]
                },
                {
                    "id": "sound_light",
                    "title": "Sound & Light",
                    "description": "Waves and properties",
                    "icon": "🌈",
                    "color": "orange",
                    "lessons": [
                        "Sound Waves",
                        "Volume and Pitch",
                        "Light Waves",
                        "Color and Reflection"
                    ]
                }
            ]
        },
        5: {
            "chapters": [
                {
                    "id": "cells_organisms",
                    "title": "Cells & Organisms",
                    "description": "Building blocks of life",
                    "icon": "🔬",
                    "color": "purple",
                    "lessons": [
                        "What Are Cells?",
                        "Plant vs Animal Cells",
                        "Single-Celled Organisms",
                        "Multi-Cellular Organisms",
                        "Cell Functions"
                    ]
                },
                {
                    "id": "chemical_physical",
                    "title": "Chemical vs Physical Changes",
                    "description": "Matter transformations",
                    "icon": "🧪",
                    "color": "blue",
                    "lessons": [
                        "Physical Changes",
                        "Chemical Changes",
                        "Signs of Chemical Reactions",
                        "Conservation of Mass"
                    ]
                },
                {
                    "id": "space_exploration",
                    "title": "Space Exploration",
                    "description": "Journey beyond Earth",
                    "icon": "🛸",
                    "color": "green",
                    "lessons": [
                        "History of Space Travel",
                        "Satellites and Probes",
                        "The ISS",
                        "Future of Space Exploration"
                    ]
                },
                {
                    "id": "electricity",
                    "title": "Electricity",
                    "description": "Electrical energy and circuits",
                    "icon": "💡",
                    "color": "orange",
                    "lessons": [
                        "What is Electricity?",
                        "Circuits",
                        "Conductors and Insulators",
                        "Static Electricity"
                    ]
                }
            ]
        },
        6: {
            "chapters": [
                {
                    "id": "photosynthesis",
                    "title": "Photosynthesis",
                    "description": "How plants make food",
                    "icon": "🌿",
                    "color": "purple",
                    "lessons": [
                        "Chloroplasts and Chlorophyll",
                        "The Photosynthesis Equation",
                        "Light and Dark Reactions",
                        "Importance to Life"
                    ]
                },
                {
                    "id": "periodic_table",
                    "title": "Periodic Table Intro",
                    "description": "Elements and their organization",
                    "icon": "🧬",
                    "color": "blue",
                    "lessons": [
                        "What Are Elements?",
                        "Reading the Periodic Table",
                        "Groups and Periods",
                        "Common Elements",
                        "Compounds vs Elements"
                    ]
                },
                {
                    "id": "plate_tectonics",
                    "title": "Plate Tectonics",
                    "description": "Earth's moving crust",
                    "icon": "🌋",
                    "color": "green",
                    "lessons": [
                        "Earth's Layers",
                        "Tectonic Plates",
                        "Earthquakes",
                        "Volcanoes"
                    ]
                },
                {
                    "id": "scientific_method",
                    "title": "Scientific Method",
                    "description": "How scientists investigate",
                    "icon": "🔬",
                    "color": "orange",
                    "lessons": [
                        "Ask Questions",
                        "Form Hypotheses",
                        "Design Experiments",
                        "Analyze Data and Conclude"
                    ]
                }
            ]
        }
    },

    "faith_realm": {
        "K": {
            "chapters": [
                {
                    "id": "gods_love_k",
                    "title": "God's Love",
                    "description": "Discover how much God loves you",
                    "icon": "💖",
                    "color": "purple",
                    "lessons": [
                        "God Made You Special",
                        "God Loves You Always",
                        "Jesus is Your Friend",
                        "Prayer is Talking to God"
                    ]
                },
                {
                    "id": "bible_stories_k",
                    "title": "Bible Story Time",
                    "description": "Learn favorite Bible stories",
                    "icon": "📖",
                    "color": "blue",
                    "lessons": [
                        "Noah's Ark",
                        "Baby Moses",
                        "David and Goliath",
                        "Jesus Loves Children"
                    ]
                },
                {
                    "id": "being_kind",
                    "title": "Being Kind Like Jesus",
                    "description": "Learn to show love to others",
                    "icon": "❤️",
                    "color": "green",
                    "lessons": [
                        "Sharing with Others",
                        "Helping Friends",
                        "Being Thankful",
                        "Obeying Parents"
                    ]
                }
            ]
        },
        1: {
            "chapters": [
                {
                    "id": "creation",
                    "title": "God's Amazing Creation",
                    "description": "Learn how God created everything",
                    "icon": "🌍",
                    "color": "purple",
                    "lessons": [
                        "In the Beginning",
                        "Day and Night",
                        "Animals and Plants",
                        "God Made People",
                        "Rest and Worship"
                    ]
                },
                {
                    "id": "jesus_birth",
                    "title": "Jesus Comes to Earth",
                    "description": "The Christmas story",
                    "icon": "⭐",
                    "color": "blue",
                    "lessons": [
                        "Mary and the Angel",
                        "Journey to Bethlehem",
                        "Jesus is Born",
                        "Shepherds and Wise Men"
                    ]
                },
                {
                    "id": "prayer_basics",
                    "title": "Talking to God",
                    "description": "Learn how to pray",
                    "icon": "🙏",
                    "color": "green",
                    "lessons": [
                        "What is Prayer?",
                        "Thanking God",
                        "Asking God for Help",
                        "Praying for Others"
                    ]
                }
            ]
        },
        2: {
            "chapters": [
                {
                    "id": "old_testament_heroes",
                    "title": "Heroes of Faith",
                    "description": "Meet brave people who followed God",
                    "icon": "🦁",
                    "color": "purple",
                    "lessons": [
                        "Abraham's Journey",
                        "Joseph's Colorful Coat",
                        "Moses and the Red Sea",
                        "Joshua and Jericho"
                    ]
                },
                {
                    "id": "ten_commandments",
                    "title": "God's Special Rules",
                    "description": "Learn the Ten Commandments",
                    "icon": "📜",
                    "color": "blue",
                    "lessons": [
                        "Love God First",
                        "Honor Your Parents",
                        "Be Truthful",
                        "Be Content"
                    ]
                },
                {
                    "id": "fruits_spirit",
                    "title": "Fruits of the Spirit",
                    "description": "Growing good character",
                    "icon": "🍎",
                    "color": "green",
                    "lessons": [
                        "Love, Joy, Peace",
                        "Patience and Kindness",
                        "Goodness and Faithfulness",
                        "Gentleness and Self-Control"
                    ]
                }
            ]
        },
        3: {
            "chapters": [
                {
                    "id": "jesus_miracles",
                    "title": "Jesus' Amazing Miracles",
                    "description": "See Jesus' power and compassion",
                    "icon": "✨",
                    "color": "purple",
                    "lessons": [
                        "Feeding 5000 People",
                        "Walking on Water",
                        "Healing the Sick",
                        "Calming the Storm",
                        "Raising Lazarus"
                    ]
                },
                {
                    "id": "parables",
                    "title": "Stories Jesus Told",
                    "description": "Learn from Jesus' parables",
                    "icon": "🌱",
                    "color": "blue",
                    "lessons": [
                        "The Good Samaritan",
                        "The Lost Sheep",
                        "The Prodigal Son",
                        "The Sower and the Seed"
                    ]
                },
                {
                    "id": "christian_character",
                    "title": "Living Like Jesus",
                    "description": "Following Jesus' example",
                    "icon": "⭐",
                    "color": "green",
                    "lessons": [
                        "Being Humble",
                        "Showing Forgiveness",
                        "Serving Others",
                        "Speaking Truth"
                    ]
                }
            ]
        },
        4: {
            "chapters": [
                {
                    "id": "life_of_jesus",
                    "title": "The Life of Jesus",
                    "description": "Follow Jesus' ministry on Earth",
                    "icon": "✝️",
                    "color": "purple",
                    "lessons": [
                        "Jesus' Baptism",
                        "Calling the Disciples",
                        "Teaching and Healing",
                        "The Last Supper",
                        "Crucifixion and Resurrection"
                    ]
                },
                {
                    "id": "new_testament_stories",
                    "title": "The Early Church",
                    "description": "How Christianity spread",
                    "icon": "📖",
                    "color": "blue",
                    "lessons": [
                        "Pentecost and the Holy Spirit",
                        "Peter's Ministry",
                        "Paul's Conversion",
                        "The Church Grows"
                    ]
                },
                {
                    "id": "bible_study_skills",
                    "title": "Studying God's Word",
                    "description": "Learn to read and understand the Bible",
                    "icon": "📚",
                    "color": "green",
                    "lessons": [
                        "Parts of the Bible",
                        "Finding Bible Verses",
                        "Understanding Context",
                        "Applying Scripture"
                    ]
                }
            ]
        },
        5: {
            "chapters": [
                {
                    "id": "books_bible",
                    "title": "Books of the Bible",
                    "description": "Navigate through Scripture",
                    "icon": "📚",
                    "color": "purple",
                    "lessons": [
                        "Old Testament Overview",
                        "The Gospels",
                        "Acts and Letters",
                        "Revelation and Prophecy"
                    ]
                },
                {
                    "id": "gospels_overview",
                    "title": "The Four Gospels",
                    "description": "Compare Gospel accounts",
                    "icon": "✝️",
                    "color": "blue",
                    "lessons": [
                        "Matthew's Gospel",
                        "Mark's Gospel",
                        "Luke's Gospel",
                        "John's Gospel"
                    ]
                },
                {
                    "id": "worship_praise",
                    "title": "Worship & Praise",
                    "description": "Honoring God",
                    "icon": "🎵",
                    "color": "green",
                    "lessons": [
                        "What is Worship?",
                        "Psalms of Praise",
                        "Prayer and Worship",
                        "Living in Worship"
                    ]
                }
            ]
        },
        6: {
            "chapters": [
                {
                    "id": "bible_timeline",
                    "title": "Bible Timeline",
                    "description": "Understanding biblical history",
                    "icon": "⏳",
                    "color": "purple",
                    "lessons": [
                        "Creation to Abraham",
                        "Exodus to Judges",
                        "Kings and Prophets",
                        "Jesus to Revelation",
                        "Putting It All Together"
                    ]
                },
                {
                    "id": "covenant_theology",
                    "title": "God's Covenants",
                    "description": "God's promises through history",
                    "icon": "🤝",
                    "color": "blue",
                    "lessons": [
                        "Covenant with Noah",
                        "Covenant with Abraham",
                        "Mosaic Covenant",
                        "New Covenant in Christ"
                    ]
                },
                {
                    "id": "christian_worldview",
                    "title": "Christian Worldview",
                    "description": "Seeing the world through faith",
                    "icon": "👁️",
                    "color": "green",
                    "lessons": [
                        "Creation and Purpose",
                        "Sin and Redemption",
                        "Truth and Morality",
                        "Eternal Perspective"
                    ]
                }
            ]
        }
    },

    # ============================================================================
    # CHRONO CORE (HISTORY)
    # ============================================================================

    "chrono_core": {
        "K": {
            "chapters": [
                {
                    "id": "me_and_my_family_k",
                    "title": "Me and My Family",
                    "description": "Learn about yourself and your family history",
                    "icon": "👨‍👩‍👧‍👦",
                    "color": "orange",
                    "lessons": [
                        "All About Me",
                        "My Family Tree",
                        "Family Traditions",
                        "Then and Now"
                    ]
                },
                {
                    "id": "community_helpers_k",
                    "title": "Community Helpers",
                    "description": "People who help our community",
                    "icon": "👮",
                    "color": "blue",
                    "lessons": [
                        "Police Officers and Firefighters",
                        "Doctors and Nurses",
                        "Teachers and Librarians",
                        "Mail Carriers and Store Workers"
                    ]
                },
                {
                    "id": "holidays_traditions_k",
                    "title": "Holidays and Traditions",
                    "description": "Special days we celebrate",
                    "icon": "🎉",
                    "color": "purple",
                    "lessons": [
                        "Thanksgiving and Gratitude",
                        "Christmas and Giving",
                        "Independence Day",
                        "Birthday Traditions"
                    ]
                }
            ]
        },
        1: {
            "chapters": [
                {
                    "id": "my_school_community",
                    "title": "My School and Community",
                    "description": "Understanding our local community",
                    "icon": "🏫",
                    "color": "green",
                    "lessons": [
                        "Our School History",
                        "Our Town or City",
                        "Community Rules and Laws",
                        "Being a Good Citizen"
                    ]
                },
                {
                    "id": "america_symbols",
                    "title": "American Symbols",
                    "description": "Important symbols of America",
                    "icon": "🗽",
                    "color": "red",
                    "lessons": [
                        "The American Flag",
                        "The Statue of Liberty",
                        "The Bald Eagle",
                        "The Liberty Bell"
                    ]
                },
                {
                    "id": "famous_americans",
                    "title": "Famous Americans",
                    "description": "People who shaped our country",
                    "icon": "⭐",
                    "color": "blue",
                    "lessons": [
                        "George Washington",
                        "Abraham Lincoln",
                        "Martin Luther King Jr.",
                        "Rosa Parks"
                    ]
                }
            ]
        },
        2: {
            "chapters": [
                {
                    "id": "early_america",
                    "title": "Early America",
                    "description": "How America began",
                    "icon": "⛵",
                    "color": "brown",
                    "lessons": [
                        "Native Americans",
                        "Christopher Columbus",
                        "The Pilgrims",
                        "The First Thanksgiving"
                    ]
                },
                {
                    "id": "colonial_life",
                    "title": "Colonial Life",
                    "description": "Life in the 13 colonies",
                    "icon": "🏘️",
                    "color": "orange",
                    "lessons": [
                        "The 13 Colonies",
                        "Colonial Jobs and Trades",
                        "Colonial Schools",
                        "Colonial Daily Life"
                    ]
                },
                {
                    "id": "american_revolution",
                    "title": "American Revolution",
                    "description": "America's fight for freedom",
                    "icon": "🎺",
                    "color": "red",
                    "lessons": [
                        "Why the Colonists Were Upset",
                        "The Boston Tea Party",
                        "The Revolutionary War",
                        "Declaring Independence"
                    ]
                }
            ]
        },
        3: {
            "chapters": [
                {
                    "id": "building_new_nation",
                    "title": "Building a New Nation",
                    "description": "Creating the United States government",
                    "icon": "🏛️",
                    "color": "blue",
                    "lessons": [
                        "The Constitution",
                        "The Bill of Rights",
                        "Three Branches of Government",
                        "Our First Presidents"
                    ]
                },
                {
                    "id": "westward_expansion",
                    "title": "Westward Expansion",
                    "description": "America grows west",
                    "icon": "🤠",
                    "color": "brown",
                    "lessons": [
                        "Lewis and Clark Expedition",
                        "The Oregon Trail",
                        "The Gold Rush",
                        "Life on the Frontier"
                    ]
                },
                {
                    "id": "civil_war_era",
                    "title": "Civil War Era",
                    "description": "A nation divided and reunited",
                    "icon": "⚔️",
                    "color": "gray",
                    "lessons": [
                        "Slavery in America",
                        "The Underground Railroad",
                        "The Civil War",
                        "Abraham Lincoln and Reconstruction"
                    ]
                }
            ]
        },
        4: {
            "chapters": [
                {
                    "id": "industrial_revolution",
                    "title": "Industrial Revolution",
                    "description": "America becomes industrial",
                    "icon": "🏭",
                    "color": "gray",
                    "lessons": [
                        "Inventions Change America",
                        "Factories and Cities Grow",
                        "Immigration to America",
                        "Life in the Late 1800s"
                    ]
                },
                {
                    "id": "progressive_era",
                    "title": "Progressive Era",
                    "description": "Reforming America",
                    "icon": "📰",
                    "color": "green",
                    "lessons": [
                        "Women's Suffrage",
                        "Child Labor Laws",
                        "Theodore Roosevelt",
                        "Conservation Movement"
                    ]
                },
                {
                    "id": "world_war_1",
                    "title": "World War I",
                    "description": "The Great War",
                    "icon": "🪖",
                    "color": "khaki",
                    "lessons": [
                        "Causes of World War I",
                        "America Enters the War",
                        "Life During Wartime",
                        "The War Ends"
                    ]
                }
            ]
        },
        5: {
            "chapters": [
                {
                    "id": "roaring_twenties",
                    "title": "The Roaring Twenties",
                    "description": "A decade of change",
                    "icon": "🎷",
                    "color": "gold",
                    "lessons": [
                        "New Technology and Culture",
                        "The Jazz Age",
                        "Economic Boom",
                        "Prohibition"
                    ]
                },
                {
                    "id": "great_depression",
                    "title": "Great Depression",
                    "description": "America's greatest economic crisis",
                    "icon": "💼",
                    "color": "brown",
                    "lessons": [
                        "The Stock Market Crash",
                        "Life During the Depression",
                        "The New Deal",
                        "The Dust Bowl"
                    ]
                },
                {
                    "id": "world_war_2",
                    "title": "World War II",
                    "description": "The war that changed the world",
                    "icon": "✈️",
                    "color": "navy",
                    "lessons": [
                        "Causes of World War II",
                        "America Joins the War",
                        "The Home Front",
                        "Victory and Peace"
                    ]
                }
            ]
        },
        6: {
            "chapters": [
                {
                    "id": "cold_war",
                    "title": "The Cold War",
                    "description": "Tension between superpowers",
                    "icon": "❄️",
                    "color": "blue",
                    "lessons": [
                        "The Iron Curtain",
                        "The Space Race",
                        "Korean and Vietnam Wars",
                        "Nuclear Arms Race"
                    ]
                },
                {
                    "id": "civil_rights_movement",
                    "title": "Civil Rights Movement",
                    "description": "The fight for equality",
                    "icon": "✊",
                    "color": "purple",
                    "lessons": [
                        "Segregation and Jim Crow Laws",
                        "Brown v. Board of Education",
                        "Martin Luther King Jr. and Peaceful Protest",
                        "The Civil Rights Act"
                    ]
                },
                {
                    "id": "modern_america",
                    "title": "Modern America",
                    "description": "Recent history and today",
                    "icon": "🌐",
                    "color": "teal",
                    "lessons": [
                        "The Fall of the Berlin Wall",
                        "The Digital Revolution",
                        "September 11, 2001",
                        "America in the 21st Century"
                    ]
                }
            ]
        }
    },

    # ============================================================================
    # STORY VERSE (LANGUAGE ARTS)
    # ============================================================================

    "story_verse": {
        "K": {
            "chapters": [
                {
                    "id": "letters_sounds_k",
                    "title": "Letters and Sounds",
                    "description": "Learning the alphabet",
                    "icon": "🔤",
                    "color": "red",
                    "lessons": [
                        "Letter Recognition A-M",
                        "Letter Recognition N-Z",
                        "Letter Sounds Beginning",
                        "Letter Sounds Practice"
                    ]
                },
                {
                    "id": "reading_readiness_k",
                    "title": "Reading Readiness",
                    "description": "Getting ready to read",
                    "icon": "📖",
                    "color": "blue",
                    "lessons": [
                        "Print Awareness",
                        "Rhyming Words",
                        "Simple Sight Words",
                        "Picture Clues"
                    ]
                },
                {
                    "id": "storytelling_k",
                    "title": "Storytelling",
                    "description": "Sharing stories",
                    "icon": "🗣️",
                    "color": "purple",
                    "lessons": [
                        "Beginning, Middle, End",
                        "Describing Pictures",
                        "Retelling Stories",
                        "Making Up Stories"
                    ]
                }
            ]
        },
        1: {
            "chapters": [
                {
                    "id": "phonics_foundations",
                    "title": "Phonics Foundations",
                    "description": "Sounding out words",
                    "icon": "🎵",
                    "color": "green",
                    "lessons": [
                        "Short Vowel Sounds",
                        "CVC Words (cat, dog, sun)",
                        "Consonant Blends (bl, tr, st)",
                        "Digraphs (ch, sh, th)"
                    ]
                },
                {
                    "id": "reading_comprehension_1",
                    "title": "Reading Comprehension",
                    "description": "Understanding what we read",
                    "icon": "💡",
                    "color": "yellow",
                    "lessons": [
                        "Main Idea",
                        "Story Details",
                        "Making Predictions",
                        "Answering Questions"
                    ]
                },
                {
                    "id": "writing_sentences",
                    "title": "Writing Sentences",
                    "description": "Creating complete sentences",
                    "icon": "✏️",
                    "color": "orange",
                    "lessons": [
                        "Capital Letters and Periods",
                        "Spacing Between Words",
                        "Complete Thoughts",
                        "Describing Words"
                    ]
                }
            ]
        },
        2: {
            "chapters": [
                {
                    "id": "advanced_phonics",
                    "title": "Advanced Phonics",
                    "description": "Complex word patterns",
                    "icon": "🔊",
                    "color": "purple",
                    "lessons": [
                        "Long Vowel Patterns (ai, ee, oa)",
                        "Silent E Words",
                        "R-Controlled Vowels (ar, er, ir, or, ur)",
                        "Multisyllabic Words"
                    ]
                },
                {
                    "id": "reading_fluency",
                    "title": "Reading Fluency",
                    "description": "Reading smoothly and expressively",
                    "icon": "📚",
                    "color": "teal",
                    "lessons": [
                        "Reading with Expression",
                        "Punctuation Clues",
                        "Reading Rate",
                        "Partner Reading"
                    ]
                },
                {
                    "id": "paragraph_writing",
                    "title": "Paragraph Writing",
                    "description": "Writing connected ideas",
                    "icon": "📝",
                    "color": "blue",
                    "lessons": [
                        "Topic Sentences",
                        "Supporting Details",
                        "Transition Words",
                        "Closing Sentences"
                    ]
                }
            ]
        },
        3: {
            "chapters": [
                {
                    "id": "vocabulary_building",
                    "title": "Vocabulary Building",
                    "description": "Expanding your word power",
                    "icon": "📖",
                    "color": "green",
                    "lessons": [
                        "Context Clues",
                        "Prefixes and Suffixes",
                        "Synonyms and Antonyms",
                        "Multiple Meaning Words"
                    ]
                },
                {
                    "id": "literary_elements",
                    "title": "Literary Elements",
                    "description": "Parts of a story",
                    "icon": "🎭",
                    "color": "red",
                    "lessons": [
                        "Character Analysis",
                        "Setting",
                        "Plot (Problem and Solution)",
                        "Theme and Message"
                    ]
                },
                {
                    "id": "narrative_writing",
                    "title": "Narrative Writing",
                    "description": "Writing stories",
                    "icon": "📔",
                    "color": "purple",
                    "lessons": [
                        "Story Planning",
                        "Dialogue",
                        "Descriptive Details",
                        "Revising and Editing"
                    ]
                }
            ]
        },
        4: {
            "chapters": [
                {
                    "id": "reading_strategies",
                    "title": "Reading Strategies",
                    "description": "Tools for better comprehension",
                    "icon": "🔍",
                    "color": "blue",
                    "lessons": [
                        "Making Inferences",
                        "Compare and Contrast",
                        "Cause and Effect",
                        "Summarizing"
                    ]
                },
                {
                    "id": "grammar_mechanics",
                    "title": "Grammar and Mechanics",
                    "description": "Rules of writing",
                    "icon": "📐",
                    "color": "orange",
                    "lessons": [
                        "Parts of Speech",
                        "Subject-Verb Agreement",
                        "Punctuation Rules",
                        "Capitalization"
                    ]
                },
                {
                    "id": "informational_writing",
                    "title": "Informational Writing",
                    "description": "Writing to teach",
                    "icon": "📰",
                    "color": "teal",
                    "lessons": [
                        "Research and Note-Taking",
                        "Organizing Information",
                        "Facts vs. Opinions",
                        "Writing How-To Guides"
                    ]
                }
            ]
        },
        5: {
            "chapters": [
                {
                    "id": "literary_analysis",
                    "title": "Literary Analysis",
                    "description": "Analyzing literature deeply",
                    "icon": "🔬",
                    "color": "purple",
                    "lessons": [
                        "Point of View",
                        "Figurative Language",
                        "Author's Purpose",
                        "Text Structure"
                    ]
                },
                {
                    "id": "research_writing",
                    "title": "Research Writing",
                    "description": "Writing research papers",
                    "icon": "🔎",
                    "color": "brown",
                    "lessons": [
                        "Finding Reliable Sources",
                        "Taking Effective Notes",
                        "Citing Sources",
                        "Writing a Research Report"
                    ]
                },
                {
                    "id": "persuasive_writing",
                    "title": "Persuasive Writing",
                    "description": "Writing to convince",
                    "icon": "💬",
                    "color": "red",
                    "lessons": [
                        "Forming Arguments",
                        "Supporting with Evidence",
                        "Addressing Counterarguments",
                        "Persuasive Techniques"
                    ]
                }
            ]
        },
        6: {
            "chapters": [
                {
                    "id": "poetry_analysis",
                    "title": "Poetry Analysis",
                    "description": "Understanding and writing poetry",
                    "icon": "🎨",
                    "color": "pink",
                    "lessons": [
                        "Poetic Devices (Metaphor, Simile)",
                        "Rhyme and Rhythm",
                        "Types of Poetry",
                        "Writing Original Poems"
                    ]
                },
                {
                    "id": "advanced_grammar",
                    "title": "Advanced Grammar",
                    "description": "Mastering complex grammar",
                    "icon": "📏",
                    "color": "navy",
                    "lessons": [
                        "Complex Sentences",
                        "Verbals (Gerunds, Participles, Infinitives)",
                        "Active vs. Passive Voice",
                        "Common Grammar Mistakes"
                    ]
                },
                {
                    "id": "multimedia_literacy",
                    "title": "Multimedia Literacy",
                    "description": "Reading and creating across media",
                    "icon": "🎬",
                    "color": "teal",
                    "lessons": [
                        "Analyzing Visual Media",
                        "Digital Research Skills",
                        "Creating Presentations",
                        "Media Literacy and Credibility"
                    ]
                }
            ]
        }
    },

    # ============================================================================
    # INK HAVEN (CREATIVE WRITING)
    # ============================================================================

    "ink_haven": {
        "K": {
            "chapters": [
                {
                    "id": "drawing_stories_k",
                    "title": "Drawing Stories",
                    "description": "Tell stories through pictures",
                    "icon": "🖍️",
                    "color": "rainbow",
                    "lessons": [
                        "Drawing Simple Pictures",
                        "Picture Sequences",
                        "Adding Labels",
                        "Sharing Your Drawings"
                    ]
                },
                {
                    "id": "imagination_play_k",
                    "title": "Imagination Play",
                    "description": "Using your imagination",
                    "icon": "🌈",
                    "color": "pink",
                    "lessons": [
                        "Pretend Play Stories",
                        "What If Questions",
                        "Making Believe",
                        "Creative Thinking"
                    ]
                }
            ]
        },
        1: {
            "chapters": [
                {
                    "id": "personal_narratives_1",
                    "title": "Personal Narratives",
                    "description": "Writing about your life",
                    "icon": "📓",
                    "color": "blue",
                    "lessons": [
                        "My Favorite Day",
                        "Something I Learned",
                        "A Special Memory",
                        "Someone Important to Me"
                    ]
                },
                {
                    "id": "creative_sentences",
                    "title": "Creative Sentences",
                    "description": "Making sentences interesting",
                    "icon": "✨",
                    "color": "purple",
                    "lessons": [
                        "Action Words",
                        "Describing Words",
                        "Silly Sentences",
                        "Sentence Variety"
                    ]
                }
            ]
        },
        2: {
            "chapters": [
                {
                    "id": "story_starters",
                    "title": "Story Starters",
                    "description": "Beginning creative stories",
                    "icon": "🚀",
                    "color": "orange",
                    "lessons": [
                        "Once Upon a Time",
                        "Creating Characters",
                        "Story Settings",
                        "Problem and Solution"
                    ]
                },
                {
                    "id": "poetry_fun",
                    "title": "Poetry Fun",
                    "description": "Writing simple poems",
                    "icon": "🎵",
                    "color": "pink",
                    "lessons": [
                        "Rhyming Poems",
                        "Acrostic Poems",
                        "Shape Poems",
                        "Color and Sensory Poems"
                    ]
                }
            ]
        },
        3: {
            "chapters": [
                {
                    "id": "fantasy_writing",
                    "title": "Fantasy Writing",
                    "description": "Creating magical worlds",
                    "icon": "🧙",
                    "color": "purple",
                    "lessons": [
                        "Magic and Magical Creatures",
                        "Building Fantasy Worlds",
                        "Fantasy Characters",
                        "Writing a Fantasy Story"
                    ]
                },
                {
                    "id": "descriptive_writing_3",
                    "title": "Descriptive Writing",
                    "description": "Painting pictures with words",
                    "icon": "🎨",
                    "color": "teal",
                    "lessons": [
                        "Show, Don't Tell",
                        "Five Senses Description",
                        "Metaphors and Similes",
                        "Vivid Vocabulary"
                    ]
                }
            ]
        },
        4: {
            "chapters": [
                {
                    "id": "adventure_stories",
                    "title": "Adventure Stories",
                    "description": "Writing exciting adventures",
                    "icon": "⚡",
                    "color": "red",
                    "lessons": [
                        "Creating Exciting Plots",
                        "Brave Characters",
                        "Dangerous Settings",
                        "Cliffhangers and Tension"
                    ]
                },
                {
                    "id": "character_development",
                    "title": "Character Development",
                    "description": "Creating believable characters",
                    "icon": "👤",
                    "color": "green",
                    "lessons": [
                        "Character Traits and Personality",
                        "Character Goals and Motivations",
                        "Character Flaws",
                        "Character Growth"
                    ]
                }
            ]
        },
        5: {
            "chapters": [
                {
                    "id": "mystery_writing",
                    "title": "Mystery Writing",
                    "description": "Crafting suspenseful mysteries",
                    "icon": "🔍",
                    "color": "navy",
                    "lessons": [
                        "Mystery Story Structure",
                        "Clues and Red Herrings",
                        "Creating Suspects",
                        "The Big Reveal"
                    ]
                },
                {
                    "id": "dialogue_craft",
                    "title": "Dialogue Craft",
                    "description": "Writing natural conversations",
                    "icon": "💬",
                    "color": "orange",
                    "lessons": [
                        "Dialogue Tags",
                        "Character Voice",
                        "Subtext and Meaning",
                        "Formatting Dialogue"
                    ]
                }
            ]
        },
        6: {
            "chapters": [
                {
                    "id": "world_building",
                    "title": "World Building",
                    "description": "Creating complete story worlds",
                    "icon": "🌍",
                    "color": "green",
                    "lessons": [
                        "Geography and Environment",
                        "Culture and Society",
                        "History and Backstory",
                        "Rules and Magic Systems"
                    ]
                },
                {
                    "id": "revision_editing",
                    "title": "Revision and Editing",
                    "description": "Improving your writing",
                    "icon": "✍️",
                    "color": "brown",
                    "lessons": [
                        "Self-Editing Techniques",
                        "Strengthening Weak Verbs",
                        "Cutting Unnecessary Words",
                        "Polishing Your Story"
                    ]
                }
            ]
        }
    },

    # ============================================================================
    # RESPECT REALM (CHARACTER EDUCATION)
    # ============================================================================

    "respect_realm": {
        "K": {
            "chapters": [
                {
                    "id": "kindness_k",
                    "title": "Kindness",
                    "description": "Being kind to others",
                    "icon": "💝",
                    "color": "pink",
                    "lessons": [
                        "What is Kindness?",
                        "Kind Words",
                        "Helping Others",
                        "Acts of Kindness"
                    ]
                },
                {
                    "id": "sharing_caring_k",
                    "title": "Sharing and Caring",
                    "description": "Learning to share",
                    "icon": "🤝",
                    "color": "blue",
                    "lessons": [
                        "Taking Turns",
                        "Sharing Toys",
                        "Caring for Friends",
                        "Being Fair"
                    ]
                },
                {
                    "id": "good_manners_k",
                    "title": "Good Manners",
                    "description": "Using polite words",
                    "icon": "🎩",
                    "color": "purple",
                    "lessons": [
                        "Please and Thank You",
                        "Excuse Me and Sorry",
                        "Good Listening",
                        "Table Manners"
                    ]
                }
            ]
        },
        1: {
            "chapters": [
                {
                    "id": "honesty_1",
                    "title": "Honesty",
                    "description": "Telling the truth",
                    "icon": "💎",
                    "color": "blue",
                    "lessons": [
                        "What is Honesty?",
                        "Telling the Truth",
                        "Admitting Mistakes",
                        "Why Honesty Matters"
                    ]
                },
                {
                    "id": "responsibility_1",
                    "title": "Responsibility",
                    "description": "Doing your part",
                    "icon": "⭐",
                    "color": "gold",
                    "lessons": [
                        "Following Through",
                        "Taking Care of Your Things",
                        "Doing Chores",
                        "Being Reliable"
                    ]
                },
                {
                    "id": "respect_others_1",
                    "title": "Respecting Others",
                    "description": "Treating people with respect",
                    "icon": "🙏",
                    "color": "green",
                    "lessons": [
                        "Listening to Others",
                        "Different is Good",
                        "Personal Space",
                        "Respecting Elders"
                    ]
                }
            ]
        },
        2: {
            "chapters": [
                {
                    "id": "courage_2",
                    "title": "Courage",
                    "description": "Being brave",
                    "icon": "🦁",
                    "color": "orange",
                    "lessons": [
                        "What is Courage?",
                        "Trying New Things",
                        "Standing Up for What's Right",
                        "Facing Fears"
                    ]
                },
                {
                    "id": "perseverance_2",
                    "title": "Perseverance",
                    "description": "Never giving up",
                    "icon": "💪",
                    "color": "red",
                    "lessons": [
                        "Keep Trying",
                        "Learning from Mistakes",
                        "Hard Work Pays Off",
                        "Finishing What You Start"
                    ]
                },
                {
                    "id": "empathy_2",
                    "title": "Empathy",
                    "description": "Understanding others' feelings",
                    "icon": "❤️",
                    "color": "pink",
                    "lessons": [
                        "How Others Feel",
                        "Putting Yourself in Their Shoes",
                        "Showing Compassion",
                        "Being a Good Friend"
                    ]
                }
            ]
        },
        3: {
            "chapters": [
                {
                    "id": "integrity_3",
                    "title": "Integrity",
                    "description": "Doing the right thing",
                    "icon": "⚖️",
                    "color": "blue",
                    "lessons": [
                        "What is Integrity?",
                        "Doing Right When No One's Watching",
                        "Keeping Your Word",
                        "Standing By Your Values"
                    ]
                },
                {
                    "id": "self_control_3",
                    "title": "Self-Control",
                    "description": "Managing yourself",
                    "icon": "🧘",
                    "color": "teal",
                    "lessons": [
                        "Controlling Your Temper",
                        "Waiting Your Turn",
                        "Making Good Choices",
                        "Thinking Before Acting"
                    ]
                },
                {
                    "id": "gratitude_3",
                    "title": "Gratitude",
                    "description": "Being thankful",
                    "icon": "🙌",
                    "color": "yellow",
                    "lessons": [
                        "Counting Your Blessings",
                        "Expressing Thanks",
                        "Appreciating What You Have",
                        "Gratitude Changes Attitude"
                    ]
                }
            ]
        },
        4: {
            "chapters": [
                {
                    "id": "cooperation_4",
                    "title": "Cooperation",
                    "description": "Working together",
                    "icon": "🤝",
                    "color": "green",
                    "lessons": [
                        "Teamwork",
                        "Compromise",
                        "Supporting Others",
                        "Group Success"
                    ]
                },
                {
                    "id": "citizenship_4",
                    "title": "Citizenship",
                    "description": "Being a good citizen",
                    "icon": "🏛️",
                    "color": "navy",
                    "lessons": [
                        "Community Service",
                        "Following Laws and Rules",
                        "Voting and Participation",
                        "Making a Difference"
                    ]
                },
                {
                    "id": "trustworthiness_4",
                    "title": "Trustworthiness",
                    "description": "Being someone people can trust",
                    "icon": "🤞",
                    "color": "blue",
                    "lessons": [
                        "Building Trust",
                        "Keeping Promises",
                        "Being Dependable",
                        "Earning Trust Back"
                    ]
                }
            ]
        },
        5: {
            "chapters": [
                {
                    "id": "leadership_5",
                    "title": "Leadership",
                    "description": "Leading with character",
                    "icon": "👑",
                    "color": "gold",
                    "lessons": [
                        "What Makes a Good Leader?",
                        "Inspiring Others",
                        "Serving Others",
                        "Leading by Example"
                    ]
                },
                {
                    "id": "forgiveness_5",
                    "title": "Forgiveness",
                    "description": "Letting go of hurt",
                    "icon": "🕊️",
                    "color": "white",
                    "lessons": [
                        "Why Forgiveness Matters",
                        "Forgiving Others",
                        "Asking for Forgiveness",
                        "Moving Forward"
                    ]
                },
                {
                    "id": "resilience_5",
                    "title": "Resilience",
                    "description": "Bouncing back from challenges",
                    "icon": "🌱",
                    "color": "green",
                    "lessons": [
                        "Overcoming Obstacles",
                        "Growth Mindset",
                        "Learning from Failure",
                        "Building Inner Strength"
                    ]
                }
            ]
        },
        6: {
            "chapters": [
                {
                    "id": "justice_fairness_6",
                    "title": "Justice and Fairness",
                    "description": "Treating everyone fairly",
                    "icon": "⚖️",
                    "color": "purple",
                    "lessons": [
                        "What is Justice?",
                        "Fairness in Action",
                        "Standing Against Injustice",
                        "Equality and Equity"
                    ]
                },
                {
                    "id": "wisdom_6",
                    "title": "Wisdom",
                    "description": "Making wise decisions",
                    "icon": "🦉",
                    "color": "brown",
                    "lessons": [
                        "Knowledge vs. Wisdom",
                        "Seeking Good Advice",
                        "Thinking Long-Term",
                        "Learning from Experience"
                    ]
                },
                {
                    "id": "humility_6",
                    "title": "Humility",
                    "description": "Staying humble",
                    "icon": "🙇",
                    "color": "gray",
                    "lessons": [
                        "Pride vs. Humility",
                        "Admitting You Don't Know",
                        "Celebrating Others",
                        "Staying Grounded"
                    ]
                }
            ]
        }
    },

    # ============================================================================
    # TERRA NOVA (GEOGRAPHY)
    # ============================================================================

    "terra_nova": {
        "K": {
            "chapters": [
                {
                    "id": "my_home_neighborhood_k",
                    "title": "My Home and Neighborhood",
                    "description": "Exploring where you live",
                    "icon": "🏡",
                    "color": "green",
                    "lessons": [
                        "My Address",
                        "My Neighborhood",
                        "Community Places",
                        "Getting Around"
                    ]
                },
                {
                    "id": "land_water_k",
                    "title": "Land and Water",
                    "description": "Earth's natural features",
                    "icon": "🌊",
                    "color": "blue",
                    "lessons": [
                        "Mountains and Hills",
                        "Rivers and Lakes",
                        "Oceans and Beaches",
                        "Deserts and Forests"
                    ]
                },
                {
                    "id": "weather_seasons_k",
                    "title": "Weather and Seasons",
                    "description": "Changes in our world",
                    "icon": "☀️",
                    "color": "yellow",
                    "lessons": [
                        "Sunny and Rainy Days",
                        "The Four Seasons",
                        "Hot and Cold",
                        "What to Wear"
                    ]
                }
            ]
        },
        1: {
            "chapters": [
                {
                    "id": "maps_globes_1",
                    "title": "Maps and Globes",
                    "description": "Understanding maps",
                    "icon": "🗺️",
                    "color": "orange",
                    "lessons": [
                        "What is a Map?",
                        "Reading Simple Maps",
                        "The Globe",
                        "Following Directions"
                    ]
                },
                {
                    "id": "my_town_city_1",
                    "title": "My Town or City",
                    "description": "Exploring your community",
                    "icon": "🏙️",
                    "color": "gray",
                    "lessons": [
                        "City vs. Country",
                        "Important Places in Town",
                        "How Cities Grow",
                        "My State"
                    ]
                },
                {
                    "id": "earth_features_1",
                    "title": "Earth's Features",
                    "description": "Landforms and bodies of water",
                    "icon": "⛰️",
                    "color": "brown",
                    "lessons": [
                        "Valleys and Plains",
                        "Islands and Peninsulas",
                        "Rivers Flow to the Sea",
                        "Natural Resources"
                    ]
                }
            ]
        },
        2: {
            "chapters": [
                {
                    "id": "continents_oceans_2",
                    "title": "Continents and Oceans",
                    "description": "Earth's major land and water",
                    "icon": "🌍",
                    "color": "blue",
                    "lessons": [
                        "The Seven Continents",
                        "The Five Oceans",
                        "Where We Live",
                        "People Around the World"
                    ]
                },
                {
                    "id": "usa_geography_2",
                    "title": "United States Geography",
                    "description": "Our country's geography",
                    "icon": "🇺🇸",
                    "color": "red",
                    "lessons": [
                        "50 States",
                        "Mountains and Rivers of USA",
                        "Different Regions",
                        "Famous Landmarks"
                    ]
                },
                {
                    "id": "communities_differ_2",
                    "title": "Communities Differ",
                    "description": "How places are different",
                    "icon": "🏘️",
                    "color": "teal",
                    "lessons": [
                        "Urban, Suburban, Rural",
                        "Climate Zones",
                        "Different Jobs in Different Places",
                        "How People Adapt"
                    ]
                }
            ]
        },
        3: {
            "chapters": [
                {
                    "id": "north_america_3",
                    "title": "North America",
                    "description": "Our continent in detail",
                    "icon": "🗽",
                    "color": "green",
                    "lessons": [
                        "Countries of North America",
                        "Major Landforms",
                        "Climate Zones",
                        "Natural Resources"
                    ]
                },
                {
                    "id": "us_regions_3",
                    "title": "U.S. Regions",
                    "description": "Five regions of America",
                    "icon": "🗺️",
                    "color": "orange",
                    "lessons": [
                        "The Northeast",
                        "The Southeast",
                        "The Midwest",
                        "The Southwest",
                        "The West"
                    ]
                },
                {
                    "id": "map_skills_3",
                    "title": "Map Skills",
                    "description": "Reading and using maps",
                    "icon": "🧭",
                    "color": "red",
                    "lessons": [
                        "Cardinal Directions",
                        "Map Keys and Symbols",
                        "Scale and Distance",
                        "Latitude and Longitude Basics"
                    ]
                }
            ]
        },
        4: {
            "chapters": [
                {
                    "id": "physical_geography_4",
                    "title": "Physical Geography",
                    "description": "Earth's physical features",
                    "icon": "🏔️",
                    "color": "brown",
                    "lessons": [
                        "How Mountains Form",
                        "River Systems",
                        "Erosion and Weathering",
                        "Plate Tectonics Basics"
                    ]
                },
                {
                    "id": "world_regions_4",
                    "title": "World Regions",
                    "description": "Major world regions",
                    "icon": "🌏",
                    "color": "blue",
                    "lessons": [
                        "Latin America",
                        "Europe",
                        "Africa",
                        "Asia",
                        "Australia and Oceania"
                    ]
                },
                {
                    "id": "climate_biomes_4",
                    "title": "Climate and Biomes",
                    "description": "Earth's climate zones",
                    "icon": "🌡️",
                    "color": "red",
                    "lessons": [
                        "What is Climate?",
                        "Tropical Rainforests",
                        "Deserts",
                        "Grasslands and Tundra"
                    ]
                }
            ]
        },
        5: {
            "chapters": [
                {
                    "id": "western_hemisphere_5",
                    "title": "Western Hemisphere",
                    "description": "Americas in depth",
                    "icon": "🌎",
                    "color": "green",
                    "lessons": [
                        "Physical Geography of the Americas",
                        "Cultural Regions",
                        "Economic Geography",
                        "Environmental Issues"
                    ]
                },
                {
                    "id": "usa_detail_5",
                    "title": "United States in Detail",
                    "description": "Deep dive into U.S. geography",
                    "icon": "🗺️",
                    "color": "red",
                    "lessons": [
                        "Major Geographic Features",
                        "State Comparisons",
                        "Population Distribution",
                        "Economic Regions"
                    ]
                },
                {
                    "id": "human_geography_5",
                    "title": "Human Geography",
                    "description": "How humans shape the Earth",
                    "icon": "👥",
                    "color": "purple",
                    "lessons": [
                        "Population and Migration",
                        "Cities and Urbanization",
                        "Transportation Networks",
                        "Human Impact on Environment"
                    ]
                }
            ]
        },
        6: {
            "chapters": [
                {
                    "id": "eastern_hemisphere_6",
                    "title": "Eastern Hemisphere",
                    "description": "Europe, Asia, Africa, Australia",
                    "icon": "🌍",
                    "color": "blue",
                    "lessons": [
                        "Physical Geography Overview",
                        "Major Rivers and Mountains",
                        "Climate Patterns",
                        "Natural Resources and Trade"
                    ]
                },
                {
                    "id": "cultural_geography_6",
                    "title": "Cultural Geography",
                    "description": "World cultures and regions",
                    "icon": "🎭",
                    "color": "rainbow",
                    "lessons": [
                        "World Religions Geography",
                        "Language Families",
                        "Cultural Regions",
                        "Global Connections"
                    ]
                },
                {
                    "id": "environmental_geography_6",
                    "title": "Environmental Geography",
                    "description": "Earth's environment and conservation",
                    "icon": "♻️",
                    "color": "green",
                    "lessons": [
                        "Ecosystems and Biodiversity",
                        "Climate Change",
                        "Conservation Efforts",
                        "Sustainable Development"
                    ]
                }
            ]
        }
    }
}


def get_chapters_for_subject_grade(subject: str, grade):
    """
    Get list of chapters for a subject and grade

    Args:
        subject: Subject key (e.g., 'num_forge')
        grade: Grade level - can be int (1-12) or str ('K')

    Returns:
        List of chapter dictionaries
    """
    if subject not in LESSON_CHAPTERS:
        return []

    # Convert integer grade to check for both int and str keys
    grade_key = grade if isinstance(grade, str) else int(grade)

    if grade_key not in LESSON_CHAPTERS[subject]:
        return []
    return LESSON_CHAPTERS[subject][grade_key].get("chapters", [])


def get_chapter_by_id(subject: str, grade, chapter_id: str):
    """
    Get a specific chapter by its ID

    Args:
        subject: Subject key
        grade: Grade level - can be int (1-12) or str ('K')
        chapter_id: Chapter identifier

    Returns:
        Chapter dictionary or None if not found
    """
    chapters = get_chapters_for_subject_grade(subject, grade)
    for chapter in chapters:
        if chapter.get("id") == chapter_id:
            return chapter
    return None
