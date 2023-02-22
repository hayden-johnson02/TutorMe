from django.test import TestCase
from .models import User, Student, Tutor

class UserModelTests(TestCase) :
    def test_student_is_student_and_not_tutor(self):
        """
        Creates a student user object and makes sure it is a student
        """
        testUser = User(is_student=True, is_tutor=False, email="mst3k@virginia.edu", first_name="John", last_name="Doe")
        self.assertIs(testUser.is_student, True)
        self.assertIs(testUser.is_tutor, False)

    def test_student_is_tutor_and_not_student(self):
        """
        Creates a tutor user object and makes sure it is a tutor
        """
        testUser = User(is_student=False, is_tutor=True, email="mst3k@virginia.edu", first_name="John", last_name="Doe")
        self.assertIs(testUser.is_student, False)
        self.assertIs(testUser.is_tutor, True)

