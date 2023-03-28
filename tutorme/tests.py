from django.test import TestCase, SimpleTestCase
from tutorme.models import Profile, Course, TutorSession, TutorRequest
from django.urls import reverse, resolve
from tutorme.views import index, logout_view, login_view, profile_view, edit_profile_view, create_account_view, delete_profile_view, tutor_list, account_type_choice
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

def create_second_student():
    User = get_user_model()
    testStudentUser = User.objects.create_user(username="TestStudent2", email="mst2k@virginia.edu",
                                               password="password456")
    testStudentProfile = Profile(user=testStudentUser, email=testStudentUser.email, first_name="John2",
                                 last_name="Dough2", is_student=True, is_tutor=False,
                                 bio="Test Student 2")
    return testStudentProfile


def create_tutor():
    User = get_user_model()
    testTutorUser = User.objects.create_user(username="TestTutor", email="mst3k@virginia.edu", password="password123")
    testTutorProfile = Profile(user=testTutorUser, email=testTutorUser.email, first_name="Jane",
                               last_name="Doe", is_student=False, is_tutor=True,
                               bio="Test Tutor", hourly_rate=10, venmo="Jane.Doe25")
    return testTutorProfile

def create_second_tutor():
    User = get_user_model()
    User.save()
    testTutorUser = User.objects.create_user(username="TestTutor2", email="mst5k@virginia.edu", password="password123")
    testTutorProfile = Profile(user=testTutorUser, email=testTutorUser.email, first_name="Jane2",
                               last_name="Doe2", is_student=False, is_tutor=True,
                               bio="Test Tutor 2", hourly_rate=15, venmo="Jane.Doe26")
    return testTutorProfile


class ProfileModelTests(TestCase):

    def test_Student_is_student(self):
        testStudent = create_student()
        self.assertIs(testStudent.is_student, True)

    def test_Student_Name(self):
        testStudent = create_student()
        self.assertEquals("John", testStudent.first_name)
        self.assertEquals("Dough", testStudent.last_name)

    def test_Student_Email(self):
        testStudent = create_student()
        self.assertEquals("mst4k@virginia.edu", testStudent.email)

    def test_Student_Bio(self):
        testStudent = create_student()
        self.assertEquals("Test Student", testStudent.bio)

    def test_Tutor_is_tutor(self):
        testTutor = create_tutor()
        self.assertIs(testTutor.is_tutor, True)

    def test_Tutor_Name(self):
        testTutor = create_tutor()
        self.assertEquals("Jane", testTutor.first_name)
        self.assertEquals("Doe", testTutor.last_name)

    def test_Tutor_Email(self):
        testTutor = create_tutor()
        self.assertEquals("mst3k@virginia.edu", testTutor.email)

    def test_Tutor_Bio(self):
        testTutor = create_tutor()
        self.assertEquals("Test Tutor", testTutor.bio)
    def test_Tutor_Hourly_Rate(self):
        testTutor = create_tutor()
        self.assertEquals(10, testTutor.hourly_rate)
    def test_Tutor_Venmo(self):
        testTutor = create_tutor()
        self.assertEquals("Jane.Doe25", testTutor.venmo)


def create_course(tutor_profile, subject, catalog_number, course_name) :
    testCourse = Course(profile=tutor_profile, subject=subject, catalog_number=catalog_number, course_name=course_name)
    return testCourse
class CourseModelTests(TestCase):
    def test_Valid_Course_Tutor(self):
        tutor = create_tutor()
        testCourse = create_course(tutor, "APMA", 3100, "Probability")
        self.assertEquals(tutor, testCourse.profile)
    def test_Valid_Course_Subject(self):
        tutor = create_tutor()
        testCourse = create_course(tutor, "APMA", 3100, "Probability")
        self.assertEquals("APMA", testCourse.subject)
    def test_Valid_Course_Catalog_Number(self):
        tutor = create_tutor()
        testCourse = create_course(tutor, "APMA", 3100, "Probability")
        self.assertEquals(3100, testCourse.catalog_number)
    def test_Valid_Course_Name(self):
        tutor = create_tutor()
        testCourse = create_course(tutor, "APMA", 3100, "Probability")
        self.assertEquals("Probability", testCourse.course_name)
    def test_Invalid_Course_Subject(self):
        tutor = create_tutor()
        testCourse = create_course(tutor, "APMAA", 31000, "Probability")
        self.assertEquals("APMAA", testCourse.subject)
        

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
    
    

