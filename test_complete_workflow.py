#!/usr/bin/env python3
"""
COMPLETE END-TO-END TESTING for CozmicLearning
Tests full workflow: Teacher → Student → Parent interactions
"""

import requests
import json
import time
from datetime import datetime

# CONFIGURATION
BASE_URL = "http://localhost:5000"  # Change to production URL when ready
# BASE_URL = "https://cozmiclearning-1.onrender.com"

# Test accounts (will be created fresh each run)
TEST_ACCOUNTS = {
    "teacher": {
        "name": "Test Teacher",
        "email": f"teacher_test_{int(time.time())}@cozmictest.com",
        "password": "TeacherPass123!"
    },
    "students": [
        {
            "name": "Student One",
            "email": f"student1_test_{int(time.time())}@cozmictest.com",
            "password": "StudentPass123!",
            "grade": "8"
        },
        {
            "name": "Student Two",
            "email": f"student2_test_{int(time.time())}@cozmictest.com",
            "password": "StudentPass123!",
            "grade": "9"
        }
    ],
    "parent": {
        "name": "Test Parent",
        "email": f"parent_test_{int(time.time())}@cozmictest.com",
        "password": "ParentPass123!",
        "plan": "homeschool_essential"
    }
}

class CompleteWorkflowTester:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
        self.issues = []
        self.successes = []
        self.test_data = {}  # Store created IDs, etc.

    def log_issue(self, category, severity, description, details=""):
        """Log an issue"""
        issue = {
            "category": category,
            "severity": severity,
            "description": description,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
        self.issues.append(issue)
        print(f"\n❌ [{severity.upper()}] {category}")
        print(f"   {description}")
        if details:
            print(f"   Details: {details}")

    def log_success(self, category, description):
        """Log a success"""
        self.successes.append({"category": category, "description": description})
        print(f"✅ {category}: {description}")

    def section_header(self, title):
        """Print section header"""
        print("\n" + "="*80)
        print(f"🧪 {title}")
        print("="*80)

    # =====================================================================
    # PHASE 1: CREATE ALL TEST ACCOUNTS
    # =====================================================================

    def create_teacher_account(self):
        """Create teacher account"""
        print("\n👨‍🏫 Creating Teacher Account...")
        try:
            teacher = TEST_ACCOUNTS["teacher"]
            response = self.session.post(
                f"{self.base_url}/teacher/signup",
                data={
                    "teacher_name": teacher["name"],
                    "teacher_email": teacher["email"],
                    "teacher_password": teacher["password"]
                },
                allow_redirects=True
            )

            if response.status_code == 200 or "dashboard" in response.url:
                self.log_success("Teacher Signup", f"Created: {teacher['email']}")
                self.test_data["teacher_email"] = teacher["email"]
                return True
            else:
                self.log_issue("Teacher Signup", "critical", "Failed to create teacher",
                             f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_issue("Teacher Signup", "critical", "Error creating teacher", str(e))
            return False

    def create_student_accounts(self):
        """Create multiple student accounts"""
        print("\n👨‍🎓 Creating Student Accounts...")
        created_students = []

        for i, student in enumerate(TEST_ACCOUNTS["students"], 1):
            try:
                # Use new session for each student
                student_session = requests.Session()
                response = student_session.post(
                    f"{self.base_url}/student/signup",
                    data={
                        "student_name": student["name"],
                        "student_email": student["email"],
                        "student_password": student["password"],
                        "student_grade": student["grade"]
                    },
                    allow_redirects=True
                )

                if response.status_code == 200:
                    self.log_success("Student Signup", f"Student {i}: {student['email']}")
                    created_students.append(student["email"])
                else:
                    self.log_issue("Student Signup", "high",
                                 f"Failed to create student {i}",
                                 f"Status: {response.status_code}")
            except Exception as e:
                self.log_issue("Student Signup", "high",
                             f"Error creating student {i}", str(e))

        self.test_data["student_emails"] = created_students
        return len(created_students) == len(TEST_ACCOUNTS["students"])

    def create_parent_account(self):
        """Create parent account"""
        print("\n👨‍👩‍👧‍👦 Creating Parent Account...")
        try:
            parent = TEST_ACCOUNTS["parent"]
            parent_session = requests.Session()
            response = parent_session.post(
                f"{self.base_url}/parent/signup",
                data={
                    "parent_name": parent["name"],
                    "parent_email": parent["email"],
                    "parent_password": parent["password"],
                    "plan": parent["plan"]
                },
                allow_redirects=True
            )

            if response.status_code == 200:
                self.log_success("Parent Signup", f"Created: {parent['email']}")
                self.test_data["parent_email"] = parent["email"]
                return True
            else:
                self.log_issue("Parent Signup", "high", "Failed to create parent",
                             f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_issue("Parent Signup", "high", "Error creating parent", str(e))
            return False

    # =====================================================================
    # PHASE 2: TEACHER CREATES CLASS & ASSIGNS WORK
    # =====================================================================

    def teacher_create_class(self):
        """Teacher creates a class"""
        print("\n🏫 Teacher Creating Class...")
        try:
            # Login as teacher first
            teacher = TEST_ACCOUNTS["teacher"]
            self.session.post(
                f"{self.base_url}/teacher/login",
                data={
                    "teacher_email": teacher["email"],
                    "teacher_password": teacher["password"]
                }
            )

            # Create class
            response = self.session.post(
                f"{self.base_url}/teacher/create_class",
                data={
                    "class_name": "Test Class Grade 8-9",
                    "grade_level": "8"
                },
                allow_redirects=False
            )

            if response.status_code in [200, 302, 303]:
                self.log_success("Class Creation", "Teacher created class successfully")
                return True
            else:
                self.log_issue("Class Creation", "high", "Failed to create class",
                             f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_issue("Class Creation", "high", "Error creating class", str(e))
            return False

    def teacher_assign_practice(self):
        """Teacher assigns practice to students"""
        print("\n📝 Teacher Assigning Practice...")
        try:
            # Assign math practice
            response = self.session.post(
                f"{self.base_url}/teacher/assign_practice",
                data={
                    "subject": "num_forge",
                    "topic": "Linear Equations",
                    "difficulty": "medium",
                    "question_count": "5"
                }
            )

            if response.status_code in [200, 302]:
                self.log_success("Assignment Creation", "Teacher assigned practice")
                return True
            else:
                self.log_issue("Assignment Creation", "high",
                             "Failed to create assignment",
                             f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_issue("Assignment Creation", "high",
                         "Error creating assignment", str(e))
            return False

    # =====================================================================
    # PHASE 3: TEST ALL 12 SUBJECTS
    # =====================================================================

    def test_all_subjects(self):
        """Test that all 12 subjects load and work"""
        self.section_header("TESTING ALL 12 SUBJECT PLANETS")

        subjects = [
            ("num_forge", "NumForge (Math)"),
            ("atom_sphere", "AtomSphere (Science)"),
            ("chrono_core", "ChronoCore (History)"),
            ("story_verse", "StoryVerse (Reading)"),
            ("ink_haven", "InkHaven (Writing)"),
            ("faith_realm", "FaithRealm (Bible)"),
            ("coin_quest", "CoinQuest (Money)"),
            ("stock_star", "StockStar (Investing)"),
            ("terra_nova", "TerraNova (General)"),
            ("power_grid", "PowerGrid (Deep Study)"),
            ("truth_forge", "TruthForge (Apologetics)"),
            ("respect_realm", "RespectRealm (Life Skills)")
        ]

        for subject_key, subject_name in subjects:
            try:
                # Try to access subject page
                response = self.session.get(
                    f"{self.base_url}/choose-grade?subject={subject_key}"
                )

                if response.status_code == 200:
                    self.log_success("Subject Load", f"{subject_name} accessible")
                else:
                    self.log_issue("Subject Load", "high",
                                 f"{subject_name} failed to load",
                                 f"Status: {response.status_code}")
            except Exception as e:
                self.log_issue("Subject Load", "high",
                             f"{subject_name} error", str(e))

    def test_respect_realm_lessons(self):
        """Test RespectRealm specifically (44 lessons)"""
        self.section_header("TESTING RESPECTREALM - 44 LESSONS")

        print("\n📚 Testing RespectRealm Landing Page...")
        try:
            response = self.session.get(f"{self.base_url}/respectrealm")

            if response.status_code == 200:
                self.log_success("RespectRealm", "Landing page loads")

                # Check for categories in response
                categories = [
                    "Table Manners",
                    "Public Behavior",
                    "Respect & Courtesy",
                    "Basic Courtesy",
                    "Phone & Digital Manners",
                    "Personal Care & Hygiene",
                    "Conversation Skills",
                    "Responsibility & Work Ethic",
                    "Physical Discipline & Fitness",
                    "Humility & Growth"
                ]

                for category in categories:
                    if category in response.text:
                        self.log_success("RespectRealm", f"Category found: {category}")
                    else:
                        self.log_issue("RespectRealm", "medium",
                                     f"Category not visible: {category}")
            else:
                self.log_issue("RespectRealm", "high",
                             "Landing page failed",
                             f"Status: {response.status_code}")

        except Exception as e:
            self.log_issue("RespectRealm", "high", "Error loading page", str(e))

    # =====================================================================
    # PHASE 4: STUDENT COMPLETES WORK
    # =====================================================================

    def student_complete_practice(self):
        """Student logs in and completes practice"""
        print("\n📚 Student Completing Practice...")
        try:
            student = TEST_ACCOUNTS["students"][0]
            student_session = requests.Session()

            # Login as student
            student_session.post(
                f"{self.base_url}/student/login",
                data={
                    "student_email": student["email"],
                    "student_password": student["password"]
                }
            )

            # Try to access practice
            response = student_session.get(f"{self.base_url}/practice/num_forge")

            if response.status_code == 200:
                self.log_success("Student Practice", "Student accessed practice mode")
                return True
            else:
                self.log_issue("Student Practice", "medium",
                             "Student could not access practice",
                             f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_issue("Student Practice", "medium",
                         "Error in student practice", str(e))
            return False

    # =====================================================================
    # PHASE 5: TEACHER VIEWS ANALYTICS
    # =====================================================================

    def teacher_view_analytics(self):
        """Teacher views class analytics"""
        print("\n📊 Teacher Viewing Analytics...")
        try:
            # Already logged in as teacher
            response = self.session.get(f"{self.base_url}/teacher/analytics")

            if response.status_code == 200:
                self.log_success("Teacher Analytics", "Analytics page loads")

                # Check for key elements
                if "progress" in response.text.lower() or "student" in response.text.lower():
                    self.log_success("Teacher Analytics", "Shows student progress data")

                return True
            else:
                self.log_issue("Teacher Analytics", "medium",
                             "Analytics page failed",
                             f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_issue("Teacher Analytics", "medium",
                         "Error loading analytics", str(e))
            return False

    # =====================================================================
    # PHASE 6: PARENT VIEWS REPORTS
    # =====================================================================

    def parent_view_reports(self):
        """Parent views student progress reports"""
        print("\n📈 Parent Viewing Reports...")
        try:
            parent = TEST_ACCOUNTS["parent"]
            parent_session = requests.Session()

            # Login as parent
            parent_session.post(
                f"{self.base_url}/parent/login",
                data={
                    "parent_email": parent["email"],
                    "parent_password": parent["password"]
                }
            )

            # Access parent dashboard
            response = parent_session.get(f"{self.base_url}/parent_dashboard")

            if response.status_code == 200:
                self.log_success("Parent Dashboard", "Dashboard loads")

                # Check for analytics/reports
                if "analytics" in response.text.lower() or "progress" in response.text.lower():
                    self.log_success("Parent Reports", "Progress reports visible")

                return True
            else:
                self.log_issue("Parent Dashboard", "medium",
                             "Dashboard failed to load",
                             f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_issue("Parent Dashboard", "medium",
                         "Error loading dashboard", str(e))
            return False

    # =====================================================================
    # PHASE 7: HOMESCHOOL LESSON PLANS
    # =====================================================================

    def test_lesson_plans(self):
        """Test lesson plan creation and library"""
        self.section_header("TESTING LESSON PLANS")

        print("\n📚 Testing Lesson Plan Library...")
        try:
            # Should still be logged in as parent
            response = self.session.get(f"{self.base_url}/parent/lesson-plans")

            if response.status_code == 200:
                self.log_success("Lesson Plans", "Library page loads")

                # Check for back button and create button
                if "Back to Dashboard" in response.text:
                    self.log_success("Lesson Plans", "Back button present")
                else:
                    self.log_issue("Lesson Plans", "low",
                                 "Back button not found")

                return True
            else:
                self.log_issue("Lesson Plans", "medium",
                             "Library page failed",
                             f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_issue("Lesson Plans", "medium",
                         "Error loading library", str(e))
            return False

    # =====================================================================
    # FINAL REPORT
    # =====================================================================

    def generate_report(self):
        """Generate comprehensive test report"""
        print("\n\n" + "="*80)
        print("📋 COMPLETE WORKFLOW TEST REPORT")
        print("="*80)

        total_tests = len(self.successes) + len(self.issues)
        success_rate = (len(self.successes) / total_tests * 100) if total_tests > 0 else 0

        print(f"\n📊 SUMMARY:")
        print(f"   Total Tests: {total_tests}")
        print(f"   ✅ Passed: {len(self.successes)}")
        print(f"   ❌ Failed: {len(self.issues)}")
        print(f"   Success Rate: {success_rate:.1f}%")

        if self.issues:
            print("\n🔍 ISSUES BY SEVERITY:")

            for severity in ["critical", "high", "medium", "low"]:
                severity_issues = [i for i in self.issues if i["severity"] == severity]
                if severity_issues:
                    print(f"\n   {severity.upper()} ({len(severity_issues)} issues):")
                    for issue in severity_issues:
                        print(f"      • {issue['category']}: {issue['description']}")
                        if issue['details']:
                            print(f"        → {issue['details']}")

        # Save detailed report
        report_file = f"workflow_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "base_url": self.base_url,
                "test_accounts": TEST_ACCOUNTS,
                "total_tests": total_tests,
                "success_rate": success_rate,
                "successes": self.successes,
                "issues": self.issues
            }, f, indent=2)

        print(f"\n📄 Full report saved to: {report_file}")
        print("="*80)

        # Return True if no critical issues
        critical_issues = [i for i in self.issues if i["severity"] == "critical"]
        return len(critical_issues) == 0


def main():
    """Run complete workflow test"""
    print("🚀 CozmicLearning COMPLETE WORKFLOW TESTING")
    print("="*80)
    print(f"Base URL: {BASE_URL}")
    print(f"Test Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80)

    tester = CompleteWorkflowTester(BASE_URL)

    # PHASE 1: Create accounts
    tester.section_header("PHASE 1: CREATE TEST ACCOUNTS")
    tester.create_teacher_account()
    tester.create_student_accounts()
    tester.create_parent_account()

    # PHASE 2: Teacher workflow
    tester.section_header("PHASE 2: TEACHER WORKFLOW")
    tester.teacher_create_class()
    tester.teacher_assign_practice()
    tester.teacher_view_analytics()

    # PHASE 3: Test all subjects
    tester.test_all_subjects()
    tester.test_respect_realm_lessons()

    # PHASE 4: Student workflow
    tester.section_header("PHASE 4: STUDENT WORKFLOW")
    tester.student_complete_practice()

    # PHASE 5: Parent workflow
    tester.section_header("PHASE 5: PARENT WORKFLOW")
    tester.parent_view_reports()
    tester.test_lesson_plans()

    # FINAL REPORT
    success = tester.generate_report()

    if success:
        print("\n✅ ALL CRITICAL TESTS PASSED!")
        return 0
    else:
        print("\n❌ CRITICAL ISSUES FOUND - REVIEW REPORT")
        return 1


if __name__ == "__main__":
    exit(main())
