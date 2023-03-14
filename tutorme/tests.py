from django.test import TestCase
from tutorme.models import Profile, Course
from django.contrib.auth import get_user_model

# Model Tests
# Used https://testdriven.io/blog/django-custom-user-model/

def create_student():
    User = get_user_model()
    testStudentUser = User.objects.create_user(username="TestStudent", email="mst4k@virginia.edu", password="password456")
    testStudentProfile = Profile.objects.create(user=testStudentUser, email=testStudentUser.email, first_name="John",
                                                last_name="Dough", is_student=True, is_tutor=False,
                                                bio="Test Student")
    return testStudentProfile

def create_tutor():
    User = get_user_model()
    testTutorUser = User.objects.create_user(username= "TestTutor", email="mst3k@virginia.edu", password="password123")
    testTutorProfile = Profile.objects.create(user=testTutorUser, email=testTutorUser.email, first_name="Jane",
                                              last_name="Doe", is_student=False, is_tutor=True,
                                              bio="Test Tutor")
    return testTutorProfile
class ProfileModelTests(TestCase):

    def test_Student_Model(self):
        testStudent = create_student()
        self.assertIs(testStudent.is_student, True)
    def test_Tutor_Model(self):
        testTutor = create_tutor()
        self.assertIs(testTutor.is_tutor, True)

#class CourseModelTests(TestCase):


# View Tests



# Template Tests
