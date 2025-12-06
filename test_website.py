#!/usr/bin/env python3
"""
Systematic Website Testing Script for CozmicLearning
Creates test accounts and identifies issues across all user types
"""

import requests
import json
from datetime import datetime

# Base URL - change this to your production URL
BASE_URL = "https://cozmiclearning-1.onrender.com"
# BASE_URL = "http://localhost:5000"  # Uncomment for local testing

class WebsiteTester:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
        self.issues = []
        self.successes = []

    def log_issue(self, category, severity, description, details=""):
        """Log an issue found during testing"""
        issue = {
            "category": category,
            "severity": severity,  # critical, high, medium, low
            "description": description,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
        self.issues.append(issue)
        print(f"❌ [{severity.upper()}] {category}: {description}")
        if details:
            print(f"   Details: {details}")

    def log_success(self, category, description):
        """Log a successful test"""
        self.successes.append({"category": category, "description": description})
        print(f"✅ {category}: {description}")

    def test_homepage(self):
        """Test that homepage loads"""
        print("\n🏠 Testing Homepage...")
        try:
            response = self.session.get(f"{self.base_url}/")
            if response.status_code == 200:
                self.log_success("Homepage", "Homepage loads successfully")
                return True
            else:
                self.log_issue("Homepage", "critical", f"Homepage returned status {response.status_code}")
                return False
        except Exception as e:
            self.log_issue("Homepage", "critical", "Cannot reach website", str(e))
            return False

    def create_test_student(self, name, email, password="TestPass123!"):
        """Create a test student account"""
        print(f"\n👨‍🎓 Creating test student: {name}...")
        try:
            response = self.session.post(
                f"{self.base_url}/student/signup",
                data={
                    "student_name": name,
                    "student_email": email,
                    "student_password": password,
                    "student_grade": "8"
                },
                allow_redirects=False
            )

            if response.status_code in [200, 302, 303]:
                self.log_success("Student Signup", f"Created student account: {email}")
                return True
            else:
                self.log_issue("Student Signup", "high", f"Failed to create student {email}",
                             f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_issue("Student Signup", "high", f"Error creating student {email}", str(e))
            return False

    def login_student(self, email, password="TestPass123!"):
        """Login as student"""
        print(f"\n🔑 Logging in as student: {email}...")
        try:
            response = self.session.post(
                f"{self.base_url}/student/login",
                data={
                    "student_email": email,
                    "student_password": password
                },
                allow_redirects=True
            )

            if "dashboard" in response.url.lower() or response.status_code == 200:
                self.log_success("Student Login", f"Successfully logged in as {email}")
                return True
            else:
                self.log_issue("Student Login", "high", f"Failed to login as {email}",
                             f"Redirected to: {response.url}")
                return False
        except Exception as e:
            self.log_issue("Student Login", "high", f"Error logging in as {email}", str(e))
            return False

    def test_student_dashboard(self):
        """Test student dashboard loads"""
        print("\n📊 Testing Student Dashboard...")
        try:
            response = self.session.get(f"{self.base_url}/student/dashboard")
            if response.status_code == 200:
                self.log_success("Student Dashboard", "Dashboard loads successfully")

                # Check for key elements
                if "Practice Session" in response.text or "practice" in response.text.lower():
                    self.log_success("Student Dashboard", "Practice session option visible")
                else:
                    self.log_issue("Student Dashboard", "medium", "Practice session option not found")

                return True
            else:
                self.log_issue("Student Dashboard", "high", f"Dashboard returned {response.status_code}")
                return False
        except Exception as e:
            self.log_issue("Student Dashboard", "high", "Error loading dashboard", str(e))
            return False

    def create_test_teacher(self, name, email, password="TeacherPass123!"):
        """Create a test teacher account"""
        print(f"\n👨‍🏫 Creating test teacher: {name}...")
        try:
            response = self.session.post(
                f"{self.base_url}/teacher/signup",
                data={
                    "teacher_name": name,
                    "teacher_email": email,
                    "teacher_password": password
                },
                allow_redirects=False
            )

            if response.status_code in [200, 302, 303]:
                self.log_success("Teacher Signup", f"Created teacher account: {email}")
                return True
            else:
                self.log_issue("Teacher Signup", "high", f"Failed to create teacher {email}",
                             f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_issue("Teacher Signup", "high", f"Error creating teacher {email}", str(e))
            return False

    def login_teacher(self, email, password="TeacherPass123!"):
        """Login as teacher"""
        print(f"\n🔑 Logging in as teacher: {email}...")
        try:
            response = self.session.post(
                f"{self.base_url}/teacher/login",
                data={
                    "teacher_email": email,
                    "teacher_password": password
                },
                allow_redirects=True
            )

            if "dashboard" in response.url.lower() or response.status_code == 200:
                self.log_success("Teacher Login", f"Successfully logged in as {email}")
                return True
            else:
                self.log_issue("Teacher Login", "high", f"Failed to login as {email}",
                             f"Redirected to: {response.url}")
                return False
        except Exception as e:
            self.log_issue("Teacher Login", "high", f"Error logging in as {email}", str(e))
            return False

    def test_teacher_dashboard(self):
        """Test teacher dashboard loads"""
        print("\n📊 Testing Teacher Dashboard...")
        try:
            response = self.session.get(f"{self.base_url}/teacher/dashboard")
            if response.status_code == 200:
                self.log_success("Teacher Dashboard", "Dashboard loads successfully")

                # Check for key features
                if "Create Class" in response.text or "class" in response.text.lower():
                    self.log_success("Teacher Dashboard", "Class creation option visible")
                else:
                    self.log_issue("Teacher Dashboard", "medium", "Class creation option not found")

                if "Lesson Plan" in response.text or "lesson" in response.text.lower():
                    self.log_success("Teacher Dashboard", "Lesson plan option visible")
                else:
                    self.log_issue("Teacher Dashboard", "medium", "Lesson plan option not found")

                return True
            else:
                self.log_issue("Teacher Dashboard", "high", f"Dashboard returned {response.status_code}")
                return False
        except Exception as e:
            self.log_issue("Teacher Dashboard", "high", "Error loading dashboard", str(e))
            return False

    def create_test_parent(self, name, email, password="ParentPass123!", plan="basic"):
        """Create a test parent account"""
        print(f"\n👨‍👩‍👧 Creating test parent: {name} ({plan} plan)...")
        try:
            response = self.session.post(
                f"{self.base_url}/parent/signup",
                data={
                    "parent_name": name,
                    "parent_email": email,
                    "parent_password": password,
                    "plan": plan
                },
                allow_redirects=False
            )

            if response.status_code in [200, 302, 303]:
                self.log_success("Parent Signup", f"Created parent account: {email} ({plan})")
                return True
            else:
                self.log_issue("Parent Signup", "high", f"Failed to create parent {email}",
                             f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_issue("Parent Signup", "high", f"Error creating parent {email}", str(e))
            return False

    def login_parent(self, email, password="ParentPass123!"):
        """Login as parent"""
        print(f"\n🔑 Logging in as parent: {email}...")
        try:
            response = self.session.post(
                f"{self.base_url}/parent/login",
                data={
                    "parent_email": email,
                    "parent_password": password
                },
                allow_redirects=True
            )

            if "dashboard" in response.url.lower() or response.status_code == 200:
                self.log_success("Parent Login", f"Successfully logged in as {email}")
                return True
            else:
                self.log_issue("Parent Login", "high", f"Failed to login as {email}",
                             f"Redirected to: {response.url}")
                return False
        except Exception as e:
            self.log_issue("Parent Login", "high", f"Error logging in as {email}", str(e))
            return False

    def logout(self):
        """Logout current user"""
        print("\n🚪 Logging out...")
        try:
            self.session.get(f"{self.base_url}/logout")
            self.session = requests.Session()  # Create new session
            self.log_success("Logout", "Successfully logged out")
        except Exception as e:
            self.log_issue("Logout", "low", "Error during logout", str(e))

    def generate_report(self):
        """Generate final test report"""
        print("\n" + "="*80)
        print("📋 TEST REPORT")
        print("="*80)

        print(f"\n✅ Successful Tests: {len(self.successes)}")
        print(f"❌ Issues Found: {len(self.issues)}")

        if self.issues:
            print("\n🔍 ISSUES BY SEVERITY:\n")

            for severity in ["critical", "high", "medium", "low"]:
                severity_issues = [i for i in self.issues if i["severity"] == severity]
                if severity_issues:
                    print(f"\n{severity.upper()} ({len(severity_issues)} issues):")
                    for issue in severity_issues:
                        print(f"  • {issue['category']}: {issue['description']}")
                        if issue['details']:
                            print(f"    → {issue['details']}")

        # Save to file
        report_file = f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "base_url": self.base_url,
                "total_tests": len(self.successes) + len(self.issues),
                "successes": self.successes,
                "issues": self.issues
            }, f, indent=2)

        print(f"\n📄 Full report saved to: {report_file}")
        print("="*80)

def main():
    print("🚀 CozmicLearning Website Testing Suite")
    print("="*80)

    tester = WebsiteTester(BASE_URL)

    # Test 1: Homepage
    if not tester.test_homepage():
        print("\n❌ Cannot reach website. Stopping tests.")
        tester.generate_report()
        return

    # Test 2: Student Flow
    print("\n" + "="*80)
    print("🧪 TESTING STUDENT FLOW")
    print("="*80)

    tester.create_test_student("Test Student", "teststudent@cozmictest.com")
    tester.logout()
    tester.login_student("teststudent@cozmictest.com")
    tester.test_student_dashboard()
    tester.logout()

    # Test 3: Teacher Flow
    print("\n" + "="*80)
    print("🧪 TESTING TEACHER FLOW")
    print("="*80)

    tester.create_test_teacher("Test Teacher", "testteacher@cozmictest.com")
    tester.logout()
    tester.login_teacher("testteacher@cozmictest.com")
    tester.test_teacher_dashboard()
    tester.logout()

    # Test 4: Parent Flow (Basic Plan)
    print("\n" + "="*80)
    print("🧪 TESTING PARENT FLOW (BASIC PLAN)")
    print("="*80)

    tester.create_test_parent("Test Parent", "testparent@cozmictest.com", plan="basic")
    tester.logout()
    tester.login_parent("testparent@cozmictest.com")
    tester.logout()

    # Test 5: Homeschool Parent Flow
    print("\n" + "="*80)
    print("🧪 TESTING HOMESCHOOL PARENT FLOW")
    print("="*80)

    tester.create_test_parent("Homeschool Parent", "homeschool@cozmictest.com", plan="homeschool_essential")
    tester.logout()
    tester.login_parent("homeschool@cozmictest.com")
    tester.logout()

    # Generate final report
    tester.generate_report()

if __name__ == "__main__":
    main()
