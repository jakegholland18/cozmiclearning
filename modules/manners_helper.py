# modules/manners_helper.py

from modules.shared_ai import study_buddy_ai


# Preset RespectRealm Lessons - Organized by Category
RESPECTREALM_LESSONS = {
    "table_manners": {
        "category": "Table Manners & Dining",
        "icon": "🍽️",
        "lessons": [
            {
                "id": "basic_table",
                "title": "Basic Table Manners",
                "description": "How to sit, use utensils, and behave at the table",
                "hook": "This skill gets you invited back to nice places (and impresses dates)",
                "story": "Marcus got invited to dinner at his friend's wealthy grandparents' mansion. He was nervous but knew the basics. While other kids were messy, he sat properly, used utensils correctly, and was polite. The grandmother was so impressed she told Marcus's friend, 'Your friend has excellent manners. You should be more like him.' Marcus got invited back multiple times and even got to go on their yacht. All because of basic table manners."
            },
            {
                "id": "restaurant",
                "title": "Restaurant Etiquette",
                "description": "Ordering, tipping, and being respectful in restaurants",
                "hook": "People judge you hard at restaurants - waiters, dates, and potential employers",
                "story": "Sarah went to lunch with her future boss as part of a job interview. She was kind to the waiter, ordered decisively, said please and thank you, and left a good tip. After they left, the boss told her: 'I always take candidates to lunch because how they treat servers tells me everything I need to know about their character. You're hired.' That job changed her life."
            },
            {
                "id": "family_dinner",
                "title": "Family Dinner Time",
                "description": "Making dinner time pleasant for everyone",
                "hook": "Good dinner behavior = more freedom and trust from parents",
                "story": "Jake used to complain, play on his phone, and leave the table a mess. His parents were always frustrated and said no to everything he wanted. Then he started being pleasant at dinner - helping set the table, staying engaged, cleaning up. Within two weeks, his parents noticed and he started getting 'yes' way more often to hanging out with friends and getting extra privileges."
            },
            {
                "id": "eating_politely",
                "title": "Eating Politely",
                "description": "Chewing with your mouth closed, not talking with food in mouth",
                "hook": "Gross eating = people avoid you (even if they don't tell you why)",
                "story": "Emma wondered why kids stopped sitting with her at lunch. Nobody told her, but the truth was she chewed with her mouth open and talked with food in her mouth. It was disgusting. Once her older sister finally told her the truth, Emma fixed it immediately. Within a week, friends started sitting with her again."
            },
        ]
    },
    "public_behavior": {
        "category": "Public Behavior",
        "icon": "🏪",
        "lessons": [
            {
                "id": "store_behavior",
                "title": "How to Act in Stores",
                "description": "Being respectful while shopping",
                "hook": "Store employees remember bad behavior - and they talk to your parents",
                "story": "Tyler and his friends were loud and messy at Target. The manager recognized Tyler from his school basketball team and called his coach. Tyler got benched for two games. Meanwhile, his teammate Alex was always respectful in public, and when the team needed donations for new jerseys, the same store manager sponsored them because 'those kids represent us well.'"
            },
            {
                "id": "church_behavior",
                "title": "Church & Quiet Places",
                "description": "Behavior in church, libraries, and other quiet spaces",
                "hook": "Adults judge your entire family based on how you act in church",
                "story": "The Johnson kids were disruptive every Sunday. Parents whispered about them. Then the Johnsons started teaching their kids proper church behavior. Within a month, other families started inviting them to events and the parents made new friends. 'People finally see us as a respectable family,' the mom said."
            },
            {
                "id": "waiting_in_line",
                "title": "Waiting Your Turn",
                "description": "Patience in lines and taking turns",
                "hook": "Impatient people get a reputation - and miss out on opportunities",
                "story": "At the amusement park, kids were cutting in line and complaining. The park employee noticed one girl, Maya, who waited patiently and was kind to others. When the VIP fast-pass contest winner didn't show up, the employee gave it to Maya. 'I noticed you've been so patient and kind. You deserve this.' She got front-of-line access all day."
            },
            {
                "id": "indoor_voice",
                "title": "Using Your Indoor Voice",
                "description": "When and how to control your volume",
                "hook": "Loud = annoying = people avoid you",
                "story": "Brandon was always the loudest kid everywhere. He wondered why he stopped getting invited to things. The truth? Parents texted each other 'Not inviting Brandon, he's too loud and my ears can't handle it.' Once he learned volume control, invitations started coming back."
            },
        ]
    },
    "respect": {
        "category": "Respect & Courtesy",
        "icon": "🤝",
        "lessons": [
            {
                "id": "greeting_adults",
                "title": "Greeting Adults Properly",
                "description": "How to introduce yourself and show respect",
                "hook": "First impressions open doors - or slam them shut forever",
                "story": "Two students interviewed for a scholarship. Chris mumbled 'hey' and looked at his phone. Jordan stood up, shook hands firmly, made eye contact and said 'Nice to meet you, sir.' Same grades, same test scores. Jordan got the $10,000 scholarship. The judge said: 'Jordan showed maturity and respect. That tells me about character, not just academics.'"
            },
            {
                "id": "yes_sir_maam",
                "title": "Yes Sir, Yes Ma'am",
                "description": "Respectful responses to adults",
                "hook": "This tiny habit makes adults want to help you succeed",
                "story": "At summer camp, counselors noticed two kids. One said 'yeah' and 'whatever.' The other said 'Yes ma'am' and 'No sir.' When it came time to pick a camp leader who'd get special privileges and a recommendation letter, they chose the respectful kid without hesitation. 'That kid gets it. They'll go far in life.'"
            },
            {
                "id": "listening",
                "title": "Active Listening",
                "description": "How to listen when others are talking",
                "hook": "People will literally pay you more if you're a good listener",
                "story": "In a group project, everyone talked over each other except Mia. She listened carefully, asked good questions, and remembered what people said. The teacher noticed and recommended her for a paid internship. 'Mia has a skill most adults don't have - she actually listens. Companies need that.'"
            },
            {
                "id": "interrupting",
                "title": "Not Interrupting",
                "description": "Waiting for your turn to speak",
                "hook": "Interrupters are seen as disrespectful and don't get taken seriously",
                "story": "Student council elections: David interrupted constantly, talked over people, couldn't wait his turn. Lisa waited patiently and spoke when appropriate. Even though David had better ideas, Lisa won by a landslide. Students said: 'David doesn't respect anyone. Lisa actually listens to us.'"
            },
        ]
    },
    "basic_courtesy": {
        "category": "Basic Courtesy",
        "icon": "💝",
        "lessons": [
            {
                "id": "please_thank_you",
                "title": "Please and Thank You",
                "description": "Using polite words every day",
                "hook": "These 'magic words' actually work - people give you more when you use them",
                "story": "Cashier experiment: One kid demanded 'Give me a refund.' Another said 'Could I please get a refund? Thank you so much.' Same situation, same store policy. Guess who got extra help, a gift card for the trouble, and a smile? Manners literally get you more stuff."
            },
            {
                "id": "excuse_me",
                "title": "Excuse Me & I'm Sorry",
                "description": "When and how to apologize",
                "hook": "Knowing how to apologize gets you out of trouble faster",
                "story": "Two kids knocked over a display at the store. One ran away. The other said 'I'm so sorry, that was my fault. Can I help clean it up?' The runner got banned from the store. The apologizer got thanked for being responsible and was allowed back anytime. Same mistake, totally different outcome."
            },
            {
                "id": "holding_doors",
                "title": "Holding Doors Open",
                "description": "Being helpful and courteous",
                "hook": "Small acts of courtesy build a reputation that pays off big",
                "story": "Anthony held the door for an older woman at Starbucks. She smiled and left. Ten minutes later she came back and said, 'I own a business and I need responsible young people. Here's my card - call me about a job.' That door-holding moment turned into his first job at 15."
            },
            {
                "id": "eye_contact",
                "title": "Making Eye Contact",
                "description": "Showing respect through eye contact",
                "hook": "Eye contact = confidence = people take you seriously",
                "story": "Job interview for same position. Candidate 1: looked at the floor, mumbled answers. Candidate 2: made eye contact, spoke clearly. Interviewer's notes: 'Candidate 1 seems dishonest or scared. Candidate 2 shows confidence and honesty.' Eye contact got the job."
            },
        ]
    },
    "phone_digital": {
        "category": "Phone & Digital Manners",
        "icon": "📱",
        "lessons": [
            {
                "id": "phone_calls",
                "title": "Phone Call Etiquette",
                "description": "How to make and answer phone calls politely",
                "hook": "Adults are shocked when young people can actually talk on the phone - it gets you opportunities",
                "story": "College application required a phone interview. Most students texted asking to do it over email instead. Rachel called back professionally: 'Hello, this is Rachel returning your call about the application.' The admissions officer was stunned. 'You're the ONLY student who called back professionally. You're admitted.' Phone skills = rare = valuable."
            },
            {
                "id": "texting_manners",
                "title": "Texting Properly",
                "description": "When and how to text respectfully",
                "hook": "Bad texting ruins friendships and opportunities (screenshots last forever)",
                "story": "Group chat drama: One person talked trash, thinking it was private. Screenshots got leaked. Friendships destroyed, college admission rescinded, job offer pulled. Meanwhile, another student always texted respectfully and kindly - their texts were screenshotted too, but as EXAMPLES of good character. Your texts define your reputation."
            },
            {
                "id": "social_media",
                "title": "Social Media Behavior",
                "description": "Being kind and appropriate online",
                "hook": "Colleges and employers check your social media - one bad post can cost you everything",
                "story": "Two students applied to the same college. Same grades, same scores. College checked social media. Student A: respectful posts, kind comments, positive content. Student B: mean comments, inappropriate photos, trash talk. Student A got in with a scholarship. Student B got rejected. The dean said: 'We check social media because character matters.'"
            },
            {
                "id": "screen_time",
                "title": "Screen Time Manners",
                "description": "When to put your phone away",
                "hook": "Being on your phone at the wrong time makes you look disrespectful and immature",
                "story": "Family dinner at a nice restaurant for grandma's birthday. One grandson was on his phone the whole time. Another put his phone away and engaged with grandma. Months later when grandma updated her will, she left the engaged grandson a large inheritance and cut the phone-addicted one out. 'He couldn't even look up from his screen for one dinner. That showed me everything.'"
            },
        ]
    },
    "personal_care": {
        "category": "Personal Care & Hygiene",
        "icon": "🧼",
        "lessons": [
            {
                "id": "hygiene_basics",
                "title": "Basic Hygiene",
                "description": "Washing hands, brushing teeth, staying clean",
                "hook": "People notice bad hygiene but won't tell you - they just avoid you",
                "story": "Middle school truth bomb: A girl wondered why nobody sat near her on the bus. Her best friend finally told her - 'You smell bad and your breath is gross.' It was brutal but necessary. She started basic hygiene and within a week, people stopped avoiding her. Nobody told her sooner because it's awkward, but they definitely noticed."
            },
            {
                "id": "dressing_properly",
                "title": "Dressing Appropriately",
                "description": "Choosing clothes for different occasions",
                "hook": "Dressing right = respect and opportunities; dressing wrong = doors closed",
                "story": "Two students showed up to court for community service. One wore athletic shorts and a wrinkled t-shirt. The other wore khakis and a button-up. The judge cut the well-dressed student's hours in half and wrote a recommendation letter. 'Dressing appropriately shows you take this seriously and respect the court.'"
            },
            {
                "id": "grooming",
                "title": "Personal Grooming",
                "description": "Taking care of your appearance",
                "hook": "Looking put-together makes people assume you're more capable and trustworthy",
                "story": "School presentation day. Both students had the same project quality. One: messy hair, wrinkled clothes, dirty shoes. The other: clean, neat, put-together. Guess who got an A and who got a B? The teacher admitted: 'Presentation matters. The neat student looked professional and prepared. Fair? Maybe not. Reality? Yes.'"
            },
            {
                "id": "cleanliness",
                "title": "Keeping Things Clean",
                "description": "Cleaning up after yourself",
                "hook": "Clean up after yourself = more freedom and trust from everyone",
                "story": "Teen asked to borrow dad's truck for the weekend. Dad said yes. Teen returned it trashed - fast food bags, mud, empty bottles. Next time teen asked? 'No. You showed me you're not responsible.' Teen's friend always returned it cleaner than he got it. That friend got to borrow the truck whenever he wanted AND got it for free when he turned 18."
            },
        ]
    },
    "conversation": {
        "category": "Conversation Skills",
        "icon": "💬",
        "lessons": [
            {
                "id": "small_talk",
                "title": "Making Small Talk",
                "description": "How to have pleasant conversations",
                "hook": "Small talk is the secret weapon of successful people - it builds connections that matter",
                "story": "Elevator ride: CEO and intern going to the same floor. Awkward silence. Intern made small talk: 'How's your day going? Busy week?' They chatted for 2 minutes. CEO remembered him and invited him to an important meeting. That connection led to a full-time job offer. All from small talk in an elevator."
            },
            {
                "id": "asking_questions",
                "title": "Asking Good Questions",
                "description": "Showing interest in others",
                "hook": "People love talking about themselves - ask questions and they'll think you're amazing",
                "story": "Two kids at a family party. One talked about himself nonstop. The other asked adults questions about their lives and listened. Adults later told the parents: 'Your first kid is annoying, but your second kid is so mature and interesting!' The question-asker got recommendations, job offers, and respect. The talker got eye rolls."
            },
            {
                "id": "compliments",
                "title": "Giving Compliments",
                "description": "Being kind and genuine",
                "hook": "Genuine compliments make people remember you (and want to help you)",
                "story": "Job shadow day: One student complimented the mentor's presentation skills genuinely. 'That was really clear - how did you learn to explain things so well?' The mentor was impressed and offered to be a reference, write a recommendation, and introduced the student to other professionals. One genuine compliment opened multiple doors."
            },
            {
                "id": "disagreeing_politely",
                "title": "Disagreeing Politely",
                "description": "How to disagree without being rude",
                "hook": "How you disagree determines if people respect your opinion or dismiss you as rude",
                "story": "Class debate: Student A said 'That's stupid and you're wrong.' Student B said 'I see your point, but have you considered this perspective?' Both disagreed. Student A got detention for disrespect. Student B got praise from the teacher and respect from classmates. The message matters, but HOW you say it matters more."
            },
        ]
    },
    "responsibility": {
        "category": "Responsibility & Work Ethic",
        "icon": "💼",
        "lessons": [
            {
                "id": "chores",
                "title": "Doing Chores Without Complaining",
                "description": "Taking responsibility at home",
                "hook": "Kids who do chores without whining get way more privileges and freedom",
                "story": "Two siblings. One complained about every chore, dragged it out, did terrible work. The other just did chores quickly without drama. Parents gave the responsible kid later curfew, more allowance, car privileges, and freedom. The complainer got nothing. Dad said: 'If you can't handle simple chores responsibly, why would I trust you with bigger stuff?'"
            },
            {
                "id": "being_on_time",
                "title": "Being On Time",
                "description": "Punctuality and respecting others' time",
                "hook": "Late people don't get second chances - in jobs, relationships, or life",
                "story": "Basketball tryouts. Kid showed up 15 minutes late with an excuse. Coach cut him immediately. 'If you can't respect my time at tryouts, you won't respect practice schedules.' Another kid was always early, stayed late. He made the team even though he wasn't the most skilled. 'I can teach skill, but I can't teach character.'"
            },
            {
                "id": "keeping_promises",
                "title": "Keeping Your Word",
                "description": "Following through on commitments",
                "hook": "Break your word enough times and nobody will trust or help you",
                "story": "Group project: One member promised to do their part multiple times but never delivered. The group warned the teacher. That student got an F and the reputation of being unreliable. Nobody wanted to work with them again. Another student who always delivered got chosen for every leadership opportunity. Your word is your currency."
            },
            {
                "id": "hard_work",
                "title": "Working Hard",
                "description": "Developing a strong work ethic",
                "hook": "Hard workers get opportunities lazy people dream about",
                "story": "Summer job at a restaurant. Most teens did the minimum. One kid worked harder than anyone - stayed late, cleaned extra, helped without being asked. Manager noticed and promoted him to shift leader with a raise. When college started, he got a glowing recommendation letter that helped him get a scholarship. 'I've had hundreds of teenagers work here. This kid's work ethic is the best I've ever seen.'"
            },
        ]
    },
}


def get_all_lessons():
    """Get all lessons organized by category."""
    return RESPECTREALM_LESSONS


def get_lesson_by_id(lesson_id):
    """Find a specific lesson by its ID."""
    for category_key, category_data in RESPECTREALM_LESSONS.items():
        for lesson in category_data["lessons"]:
            if lesson["id"] == lesson_id:
                return {
                    "lesson": lesson,
                    "category": category_data["category"],
                    "icon": category_data["icon"]
                }
    return None


def teach_manners(scenario: str, grade: str, character: str) -> str:
    """
    Teaches manners, common sense, courtesy, and respectful behavior.

    Covers topics like:
    - Table manners and dining etiquette
    - Public behavior and social awareness
    - Respect for elders and authority
    - Common courtesy (please, thank you, excuse me)
    - Phone etiquette and digital manners
    - Personal hygiene and presentation
    - Conversation skills and active listening
    - Conflict resolution and apologies
    - Helping others and being considerate
    - Cultural sensitivity and awareness
    """

    prompt = f"""
You are teaching life skills that actually matter - the real-world stuff nobody teaches in school but everyone needs to know.

TOPIC:
{scenario}

YOUR MISSION:
Teach this RespectRealm lesson like you're giving someone the cheat codes to life. This isn't your grandma's etiquette class - this is street-smart, practical knowledge that opens doors and gets results.

GRADE LEVEL: {grade}

FORMAT REQUIREMENTS:
You MUST use the standard 6-section format:

SECTION 1 — OVERVIEW
SECTION 2 — KEY FACTS
SECTION 3 — CHRISTIAN VIEW
SECTION 4 — AGREEMENT
SECTION 5 — DIFFERENCE
SECTION 6 — PRACTICE

TONE & STYLE (CRITICAL - READ THIS):
• Talk like you're an older sibling or cool mentor, NOT a parent or teacher
• Be direct and honest - "Here's the truth nobody tells you..."
• Show them what's in it for THEM (money, respect, opportunities, freedom)
• Use real stories and examples they can visualize
• NO preaching, lecturing, or "you should because I said so"
• Instead: "Here's why smart people do this..." "Want to know the secret?"
• Focus on results: "This skill = this reward" or "Skip this = this consequence"
• Be slightly edgy but not inappropriate - keep it real
• Explain the game: "Adults judge you on this stuff whether it's fair or not"

WHY IT WORKS - SHOW THEM THE PAYOFF:
• Better treatment from adults = more privileges, more freedom, more trust
• Respect from peers = better friendships, better reputation
• Future opportunities = scholarships, jobs, recommendations
• Avoid consequences = not getting banned, rejected, or embarrassed
• Position it as: "This is how you WIN at life, not how you should behave"

REAL TALK EXAMPLES:
❌ DON'T SAY: "You should be polite because it's the right thing to do"
✅ DO SAY: "Being polite literally gets you more stuff. People give perks to polite kids."

❌ DON'T SAY: "Good manners show respect for others"
✅ DO SAY: "Good manners make adults think you're mature, which means they trust you with more freedom"

❌ DON'T SAY: "You need to listen when others talk"
✅ DO SAY: "Good listeners get promoted and paid more. It's a superpower nobody teaches."

CHRISTIAN VIEW (Section 3):
• Connect to biblical wisdom naturally - not preachy
• Show how Jesus was strategic: loving others actually benefits YOU
• "Love your neighbor" = people help you back
• "Do unto others" = build a reputation that opens doors
• Character = reflection of your faith = credibility
• Frame it as: "This is wisdom from the Bible that successful people use"

PRACTICE (Section 6):
• Give SPECIFIC missions they can do this week
• Make it feel like a challenge or experiment
• "Try this and watch what happens..."
• "This week's mission: [specific action] and report back on the results"
• Frame practice as "field testing" life hacks, not homework

REMEMBER: Kids need this content but won't listen to lectures. Make it feel like insider knowledge, not rules from adults.
"""

    return study_buddy_ai(prompt, grade, character)
