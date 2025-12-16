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
