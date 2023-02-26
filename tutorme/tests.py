from django.test import TestCase
from .models import Profile

class UserModelTests(TestCase) :
    def test_student_is_student_and_not_tutor(self):
        """
        Creates a student user object and makes sure it is a student
        """
        testProfile = Profile(is_student=True, is_tutor=False, email="mst3k@virginia.edu", first_name="John",
                        last_name="Doe")
        self.assertIs(testProfile.is_student, True)
        self.assertIs(testProfile.is_tutor, False)


    def test_student_is_tutor_and_not_student(self):
        """
        Creates a tutor user object and makes sure it is a tutor
        """
        testProfile = Profile(is_student=False, is_tutor=True, email="mst3k@virginia.edu", first_name="John",
                         last_name="Doe")
        self.assertIs(testProfile.is_student, False)
        self.assertIs(testProfile.is_tutor, True)
