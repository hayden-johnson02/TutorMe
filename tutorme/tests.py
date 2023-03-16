from django.test import TestCase, SimpleTestCase
from tutorme.models import Profile, Course
from django.urls import reverse, resolve
from tutorme.views import index, logout_view, login_view, profile_view, edit_profile_view, create_account_view, delete_profile_view, tutor_list, tutor_page, account_type_choice
from django.contrib.auth import get_user_model


# Model Tests
# Used https://testdriven.io/blog/django-custom-user-model/


def create_student():
    User = get_user_model()
    testStudentUser = User.objects.create_user(username="TestStudent", email="mst4k@virginia.edu",
                                               password="password456")
    testStudentProfile = Profile(user=testStudentUser, email=testStudentUser.email, first_name="John",
                                 last_name="Dough", is_student=True, is_tutor=False,
                                 bio="Test Student")
    return testStudentProfile


def create_tutor():
    User = get_user_model()
    testTutorUser = User.objects.create_user(username="TestTutor", email="mst3k@virginia.edu", password="password123")
    testTutorProfile = Profile(user=testTutorUser, email=testTutorUser.email, first_name="Jane",
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

# class CourseModelTests(TestCase):
        

# View Tests


# Template Tests

# URL Tests
# Used: https://www.youtube.com/watch?v=0MrgsYswT1c

class TestUrls(SimpleTestCase):

    def test_all_url_is_resolved(self):

        PASS_MESSAGE = " url matches with correct view..."
        FAIL_MESSAGE = " url does NOT match with correct view..."

        urlDictionary = {
            "index" : index,
            "login" : login_view,
            "logout" : logout_view,
            "profile" : profile_view,
            "edit_profile" : edit_profile_view,
            "delete" : delete_profile_view,
            "createAccount" : create_account_view,
            "account_type_choice" : account_type_choice,
            "view_tutors" : tutor_list,

        }

        for urlName in urlDictionary:

            url = reverse(urlName)
            try:
                self.assertEquals(resolve(url).func, urlDictionary[urlName])
                
                print("\n" + urlName + PASS_MESSAGE)

            except: 
                print("\n" + urlName + FAIL_MESSAGE)
    
    

