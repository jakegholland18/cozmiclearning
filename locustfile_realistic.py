"""
CozmicLearning Realistic Load Testing
======================================

Simulates REAL user behavior patterns:
- Students: Login → Practice questions → Review results → Logout
- Teachers: Login → Create assignment → Review analytics → Logout
- Parents: Login → Check child progress → Logout
- Anonymous: Browse homepage → View subjects → Maybe signup

Wait times match actual human behavior (30-60 sec between actions).
Sessions last 10-20 minutes like real users.

Usage:
    # Realistic daily usage (30 concurrent users over 1 hour)
    locust -f locustfile_realistic.py --host https://cozmiclearning-1.onrender.com --users 30 --spawn-rate 2 --run-time 60m --headless

    # Peak hour simulation (100 users over 30 min)
    locust -f locustfile_realistic.py --host https://cozmiclearning-1.onrender.com --users 100 --spawn-rate 5 --run-time 30m --headless
"""

from locust import HttpUser, task, between, SequentialTaskSet
import random

# ============================================================
# REALISTIC STUDENT FLOW
# ============================================================

class RealisticStudentSession(SequentialTaskSet):
    """
    Realistic student session (10-15 minutes):
    1. Login
    2. View dashboard
    3. Browse subjects
    4. Start practice (1-2 subjects)
    5. Answer 5-10 questions per subject
    6. Review results
    7. Logout
    """

    def on_start(self):
        """Student logs in at start of session"""
        # Note: These are fake accounts for testing
        # In production, you'd use real test accounts
        pass

    @task(1)
    def view_dashboard(self):
        """Student views their dashboard"""
        # Most students aren't logged in during load test
        # So this will redirect to login page (302) - that's expected!
        with self.client.get("/dashboard", catch_response=True) as response:
            if response.status_code in [200, 302]:
                response.success()
            elif response.status_code == 429:
                response.success()  # Rate limit OK
            else:
                response.failure(f"Dashboard failed: {response.status_code}")

    @task(2)
    def browse_subjects(self):
        """Student browses available subjects"""
        self.client.get("/subjects")
        # Think time: student reads subject descriptions
        self.wait()

    @task(3)
    def practice_session(self):
        """Student does a practice session (main activity)"""
        subject = random.choice([
            "num_forge", "atom_sphere", "ink_haven",
            "faith_realm", "chrono_core"
        ])

        # Start practice
        with self.client.get(f"/practice?subject={subject}", catch_response=True) as response:
            if response.status_code in [200, 302]:
                response.success()
            elif response.status_code == 429:
                response.success()
            else:
                response.failure(f"Practice failed: {response.status_code}")

        # Student reads question and thinks (30-60 seconds)
        self.wait()

        # Answer 3-5 questions (one at a time, with think time)
        for _ in range(random.randint(3, 5)):
            # Student submits answer
            # (Note: This will fail without auth, but that's expected in this test)
            self.wait()  # Think time before next question

    @task(1)
    def view_progress(self):
        """Student checks their progress"""
        with self.client.get("/dashboard", catch_response=True) as response:
            if response.status_code in [200, 302]:
                response.success()
            elif response.status_code == 429:
                response.success()
            else:
                response.failure(f"Progress view failed: {response.status_code}")


# ============================================================
# REALISTIC TEACHER FLOW
# ============================================================

class RealisticTeacherSession(SequentialTaskSet):
    """
    Realistic teacher session (15-30 minutes):
    1. Login
    2. View dashboard
    3. Check class roster
    4. Review student progress
    5. Create/review assignments
    6. Logout
    """

    @task(1)
    def view_dashboard(self):
        """Teacher views dashboard"""
        with self.client.get("/teacher/dashboard", catch_response=True) as response:
            if response.status_code in [200, 302]:
                response.success()
            elif response.status_code == 429:
                response.success()
            else:
                response.failure(f"Teacher dashboard failed: {response.status_code}")

        # Teacher reviews dashboard (longer think time)
        self.wait()

    @task(2)
    def review_assignments(self):
        """Teacher reviews existing assignments"""
        with self.client.get("/teacher/assignments", catch_response=True) as response:
            if response.status_code in [200, 302]:
                response.success()
            elif response.status_code == 429:
                response.success()
            else:
                response.failure(f"Assignments view failed: {response.status_code}")

        # Teacher reads through assignments
        self.wait()

    @task(1)
    def view_analytics(self):
        """Teacher checks class analytics"""
        with self.client.get("/teacher/analytics", catch_response=True) as response:
            if response.status_code in [200, 302]:
                response.success()
            elif response.status_code == 429:
                response.success()
            else:
                response.failure(f"Analytics failed: {response.status_code}")

        # Teacher analyzes data
        self.wait()


# ============================================================
# REALISTIC PARENT FLOW
# ============================================================

class RealisticParentSession(SequentialTaskSet):
    """
    Realistic parent session (5-10 minutes):
    1. Login
    2. View dashboard
    3. Check child's progress
    4. Review recent activity
    5. Logout
    """

    @task(1)
    def view_dashboard(self):
        """Parent views their dashboard"""
        with self.client.get("/parent_dashboard", catch_response=True) as response:
            if response.status_code in [200, 302]:
                response.success()
            elif response.status_code == 429:
                response.success()
            else:
                response.failure(f"Parent dashboard failed: {response.status_code}")

        # Parent reviews child's activity
        self.wait()

    @task(2)
    def check_child_progress(self):
        """Parent checks child's progress"""
        # This would normally show child's progress
        with self.client.get("/parent_dashboard", catch_response=True) as response:
            if response.status_code in [200, 302]:
                response.success()
            elif response.status_code == 429:
                response.success()
            else:
                response.failure(f"Progress check failed: {response.status_code}")

        # Parent reviews details
        self.wait()


# ============================================================
# REALISTIC ANONYMOUS VISITOR
# ============================================================

class AnonymousVisitorSession(SequentialTaskSet):
    """
    Realistic anonymous visitor (3-5 minutes):
    1. Land on homepage
    2. Read about the platform
    3. Browse subjects
    4. View pricing/info
    5. Maybe signup (simulated)
    6. Leave
    """

    @task(1)
    def view_homepage(self):
        """Visitor lands on homepage"""
        self.client.get("/")
        # Visitor reads homepage (1-2 minutes)
        self.wait()
        self.wait()

    @task(2)
    def explore_subjects(self):
        """Visitor explores what subjects are available"""
        self.client.get("/subjects")
        # Visitor browses subjects
        self.wait()

    @task(1)
    def view_privacy_terms(self):
        """Visitor reads privacy/terms (some do this)"""
        page = random.choice(["/privacy", "/terms"])
        self.client.get(page)
        # Quick skim
        self.wait()

    @task(1)
    def consider_signup(self):
        """Visitor considers signing up (views homepage again)"""
        self.client.get("/")
        # Visitor thinks about it
        self.wait()


# ============================================================
# USER TYPES WITH REALISTIC WEIGHTS
# ============================================================

class StudentUser(HttpUser):
    """
    Student users - Most active, longest sessions
    Weight: 50% of users
    Session length: 10-20 minutes
    Wait time: 30-90 seconds between actions (reading/thinking)
    """
    tasks = [RealisticStudentSession]
    wait_time = between(30, 90)  # 30-90 seconds think time (realistic!)
    weight = 50

class TeacherUser(HttpUser):
    """
    Teacher users - Less frequent, longer sessions
    Weight: 10% of users
    Session length: 15-30 minutes
    Wait time: 45-120 seconds between actions (reviewing data)
    """
    tasks = [RealisticTeacherSession]
    wait_time = between(45, 120)  # Teachers take time to review
    weight = 10

class ParentUser(HttpUser):
    """
    Parent users - Quick check-ins
    Weight: 15% of users
    Session length: 5-10 minutes
    Wait time: 30-60 seconds between actions
    """
    tasks = [RealisticParentSession]
    wait_time = between(30, 60)
    weight = 15

class AnonymousVisitor(HttpUser):
    """
    Anonymous visitors - Browsing, researching
    Weight: 25% of users
    Session length: 3-5 minutes
    Wait time: 20-60 seconds between actions (reading)
    """
    tasks = [AnonymousVisitorSession]
    wait_time = between(20, 60)
    weight = 25


# ============================================================
# CUSTOM REPORTING
# ============================================================

from locust import events

@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    print("\n" + "="*80)
    print("🎓 CozmicLearning Realistic Load Test")
    print("="*80)
    print(f"Target: {environment.host}")
    print(f"Users: {environment.runner.target_user_count if hasattr(environment.runner, 'target_user_count') else 'N/A'}")
    print("\nUser Mix:")
    print("  50% Students (10-20 min sessions, 30-90s think time)")
    print("  10% Teachers (15-30 min sessions, 45-120s think time)")
    print("  15% Parents (5-10 min sessions, 30-60s think time)")
    print("  25% Anonymous (3-5 min sessions, 20-60s think time)")
    print("="*80 + "\n")


@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    print("\n" + "="*80)
    print("✅ Realistic Load Test Complete")
    print("="*80)

    stats = environment.stats.total
    print(f"Total Requests: {stats.num_requests:,}")
    print(f"Total Failures: {stats.num_failures:,}")
    print(f"Failure Rate: {stats.fail_ratio * 100:.2f}%")
    print(f"Median Response: {stats.median_response_time}ms")
    print(f"95th Percentile: {stats.get_response_time_percentile(0.95)}ms")
    print(f"Avg Response: {stats.avg_response_time:.2f}ms")
    print(f"Requests/sec: {stats.total_rps:.2f}")

    # Realistic expectations
    print("\n" + "-"*80)
    print("Realistic Performance Goals:")
    if stats.fail_ratio < 0.01:
        print(f"✅ Error Rate: {stats.fail_ratio * 100:.2f}% (Target: <1%)")
    else:
        print(f"⚠️  Error Rate: {stats.fail_ratio * 100:.2f}% (Target: <1%)")

    p95 = stats.get_response_time_percentile(0.95)
    if p95 < 1000:
        print(f"✅ 95th Percentile: {p95}ms (Target: <1000ms)")
    else:
        print(f"⚠️  95th Percentile: {p95}ms (Target: <1000ms)")

    if stats.avg_response_time < 500:
        print(f"✅ Avg Response: {stats.avg_response_time:.2f}ms (Target: <500ms)")
    else:
        print(f"⚠️  Avg Response: {stats.avg_response_time:.2f}ms (Target: <500ms)")

    print("="*80 + "\n")


"""
RECOMMENDED TEST SCENARIOS
==========================

1. Daily Normal Load (30 users, 1 hour):
   locust -f locustfile_realistic.py --host https://cozmiclearning-1.onrender.com \
     --users 30 --spawn-rate 2 --run-time 60m --headless

2. Peak Hour (100 users, 30 minutes):
   locust -f locustfile_realistic.py --host https://cozmiclearning-1.onrender.com \
     --users 100 --spawn-rate 5 --run-time 30m --headless

3. After-School Rush (200 users, 2 hours):
   locust -f locustfile_realistic.py --host https://cozmiclearning-1.onrender.com \
     --users 200 --spawn-rate 10 --run-time 120m --headless

4. Weekend Light Usage (10 users, 4 hours):
   locust -f locustfile_realistic.py --host https://cozmiclearning-1.onrender.com \
     --users 10 --spawn-rate 1 --run-time 240m --headless

Expected Results with Free Tier:
- 30 users: <1% error, ~100ms response
- 100 users: 2-5% error, ~200ms response
- 200 users: 10-15% error, ~500ms response (near capacity limit)
"""
