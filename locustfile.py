"""
CozmicLearning Load Testing Script
===================================

This script simulates realistic user behavior to test system performance under load.

Installation:
    pip install locust

Usage:
    # Run with web UI
    locust -f locustfile.py --host https://your-domain.com

    # Run headless with specific parameters
    locust -f locustfile.py --host https://your-domain.com --users 100 --spawn-rate 10 --run-time 5m --headless

Test Scenarios:
    1. Anonymous users browsing homepage
    2. Students logging in and practicing
    3. Teachers creating assignments
    4. Heavy AI question generation load

Performance Targets:
    - Response time p95 < 2 seconds
    - Error rate < 1%
    - Concurrent users: 500
"""

from locust import HttpUser, task, between, SequentialTaskSet
import random


class StudentBehavior(SequentialTaskSet):
    """Simulates typical student user flow"""

    def on_start(self):
        """Login when task set starts"""
        self.client.post("/student/login", data={
            "email": f"test_student_{random.randint(1, 1000)}@test.com",
            "password": "testpass123"
        })

    @task
    def view_dashboard(self):
        """View student dashboard"""
        self.client.get("/dashboard")

    @task
    def view_subjects(self):
        """Browse subjects page"""
        self.client.get("/subjects")

    @task
    def start_practice(self):
        """Start a practice session"""
        subject = random.choice([
            "num_forge", "atom_sphere", "ink_haven",
            "faith_realm", "chrono_core"
        ])
        self.client.get(f"/practice?subject={subject}")

    @task
    def ask_question(self):
        """Ask AI a question (simulated)"""
        with self.client.get(
            "/ask-question?subject=atom_sphere",
            catch_response=True
        ) as response:
            if response.status_code == 200:
                response.success()
            elif response.status_code == 429:  # Rate limited
                response.success()  # Don't count as error
            else:
                response.failure(f"Got status {response.status_code}")


class TeacherBehavior(SequentialTaskSet):
    """Simulates typical teacher user flow"""

    def on_start(self):
        """Login when task set starts"""
        self.client.post("/teacher/login", data={
            "email": f"test_teacher_{random.randint(1, 100)}@test.com",
            "password": "testpass123"
        })

    @task
    def view_dashboard(self):
        """View teacher dashboard"""
        self.client.get("/teacher/dashboard")

    @task
    def view_assignments(self):
        """View assignments page"""
        self.client.get("/teacher/assignments")

    @task
    def view_analytics(self):
        """View class analytics"""
        self.client.get("/teacher/analytics")


class AnonymousUser(HttpUser):
    """Simulates users browsing the site without logging in"""

    wait_time = between(1, 5)  # Wait 1-5 seconds between tasks
    weight = 3  # More anonymous users than logged-in users

    @task(5)
    def view_homepage(self):
        """Most common action - view homepage"""
        self.client.get("/")

    @task(2)
    def view_privacy(self):
        """View privacy page"""
        self.client.get("/privacy")

    @task(1)
    def view_terms(self):
        """View terms of service"""
        self.client.get("/terms")


class StudentUser(HttpUser):
    """Simulates logged-in student users"""

    tasks = [StudentBehavior]
    wait_time = between(2, 10)  # Students take time to read/answer
    weight = 5  # Many student users

    # Simulate different student activity levels
    min_wait = 2000
    max_wait = 10000


class TeacherUser(HttpUser):
    """Simulates logged-in teacher users"""

    tasks = [TeacherBehavior]
    wait_time = between(5, 15)  # Teachers spend more time planning
    weight = 1  # Fewer teacher users than students


class HeavyLoadUser(HttpUser):
    """Simulates heavy AI usage for stress testing"""

    wait_time = between(1, 3)
    weight = 1  # Small percentage of heavy users

    @task
    def generate_questions(self):
        """Generate AI questions (most expensive operation)"""
        with self.client.post(
            "/teacher/preview_questions",
            json={
                "topic": "Algebra basics",
                "subject": "num_forge",
                "grade": "8",
                "character": "everly",
                "differentiation_mode": "none",
                "student_ability": "on_level",
                "num_questions": 5
            },
            catch_response=True,
            timeout=60  # Long timeout for AI generation
        ) as response:
            if response.status_code == 200:
                response.success()
            elif response.status_code == 503:  # Service unavailable
                response.failure("AI service overloaded")
            else:
                response.failure(f"Got status {response.status_code}")


# Custom event handlers for detailed reporting
from locust import events

@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    print("\n" + "="*80)
    print("🚀 CozmicLearning Load Test Starting")
    print("="*80)
    print(f"Target: {environment.host}")
    print(f"Users: {environment.runner.target_user_count if hasattr(environment.runner, 'target_user_count') else 'N/A'}")
    print("="*80 + "\n")


@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    print("\n" + "="*80)
    print("🏁 CozmicLearning Load Test Complete")
    print("="*80)

    stats = environment.stats.total
    print(f"Total Requests: {stats.num_requests}")
    print(f"Total Failures: {stats.num_failures}")
    print(f"Failure Rate: {stats.fail_ratio * 100:.2f}%")
    print(f"Median Response Time: {stats.median_response_time}ms")
    print(f"95th Percentile: {stats.get_response_time_percentile(0.95)}ms")
    print(f"99th Percentile: {stats.get_response_time_percentile(0.99)}ms")
    print(f"Avg Response Time: {stats.avg_response_time:.2f}ms")
    print(f"Requests/sec: {stats.total_rps:.2f}")
    print("="*80 + "\n")


# Performance thresholds
@events.quitting.add_listener
def check_performance_requirements(environment, **kwargs):
    """Check if performance meets requirements"""
    stats = environment.stats.total

    print("\n" + "="*80)
    print("📊 Performance Requirements Check")
    print("="*80)

    requirements_met = True

    # Check error rate
    error_rate = stats.fail_ratio * 100
    if error_rate < 1:
        print(f"✅ Error Rate: {error_rate:.2f}% (Target: <1%)")
    else:
        print(f"❌ Error Rate: {error_rate:.2f}% (Target: <1%)")
        requirements_met = False

    # Check 95th percentile response time
    p95 = stats.get_response_time_percentile(0.95)
    if p95 < 2000:
        print(f"✅ 95th Percentile Response Time: {p95}ms (Target: <2000ms)")
    else:
        print(f"❌ 95th Percentile Response Time: {p95}ms (Target: <2000ms)")
        requirements_met = False

    # Check average response time
    avg = stats.avg_response_time
    if avg < 500:
        print(f"✅ Average Response Time: {avg:.2f}ms (Target: <500ms)")
    else:
        print(f"⚠️  Average Response Time: {avg:.2f}ms (Target: <500ms)")

    print("="*80)

    if requirements_met:
        print("🎉 All performance requirements met!")
    else:
        print("⚠️  Some performance requirements not met. Review logs and optimize.")

    print("="*80 + "\n")


"""
USAGE EXAMPLES
==============

1. Quick Test (10 users for 1 minute):
   locust -f locustfile.py --host https://cozmiclearning.com --users 10 --spawn-rate 2 --run-time 1m --headless

2. Realistic Load Test (100 users for 5 minutes):
   locust -f locustfile.py --host https://cozmiclearning.com --users 100 --spawn-rate 10 --run-time 5m --headless

3. Stress Test (500 users):
   locust -f locustfile.py --host https://cozmiclearning.com --users 500 --spawn-rate 50 --run-time 10m --headless

4. Interactive Web UI:
   locust -f locustfile.py --host https://cozmiclearning.com
   # Then open http://localhost:8089 in browser

5. Spike Test (rapid increase):
   locust -f locustfile.py --host https://cozmiclearning.com --users 200 --spawn-rate 100 --run-time 3m --headless

6. Endurance Test (sustained load):
   locust -f locustfile.py --host https://cozmiclearning.com --users 50 --spawn-rate 5 --run-time 30m --headless
"""
