from django.test import TestCase, SimpleTestCase, Client
from tutorme.models import Profile, Course, TutorSession, TutorRequest, Review, Favorite
from django.urls import reverse, resolve
from tutorme.views import *
from django.contrib.auth import get_user_model
from django.utils.timezone import datetime
from django.http import HttpRequest



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
def create_course(tutor_profile, subject, catalog_number, course_name) :
    testCourse = Course(profile=tutor_profile, subject=subject, catalog_number=catalog_number, course_name=course_name)
    return testCourse

def create_review(tutor, reviewer, rating, comment, created_at) :
    testReview = Review(tutor=tutor, reviewer=reviewer, rating=rating, comment=comment, created_at=created_at)
    return testReview


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

class ReviewModelTests(TestCase) :

    # Used https://www.geeksforgeeks.org/datetimefield-django-models/
    def test_Valid_Review_Tutor(self):
        User = get_user_model()
        testTutorUser = User.objects.create_user(username="TestTutor", email="mst3k@virginia.edu",
                                                 password="password123")
        User2 = get_user_model()
        testStudentUser = User2.objects.create_user(username="TestStudent", email="mst4k@virginia.edu",
                                                   password="password456")
        d = datetime(2023, 3, 28, 23, 55, 59, 342380)
        testReview = create_review(testTutorUser, testStudentUser, 5, "Great tutor!", d)
        self.assertEquals(testTutorUser, testReview.tutor)

    def test_Valid_Review_Reviewer(self):
        User = get_user_model()
        testTutorUser = User.objects.create_user(username="TestTutor", email="mst3k@virginia.edu",
                                                 password="password123")
        User2 = get_user_model()
        testStudentUser = User2.objects.create_user(username="TestStudent", email="mst4k@virginia.edu",
                                                   password="password456")
        d = datetime(2023, 3, 28, 23, 55, 59, 342380)
        testReview = create_review(testTutorUser, testStudentUser, 5, "Great tutor!", d)
        self.assertEquals(testStudentUser, testReview.reviewer)

    def test_Valid_Review_Rating(self):
        User = get_user_model()
        testTutorUser = User.objects.create_user(username="TestTutor", email="mst3k@virginia.edu",
                                                 password="password123")
        User2 = get_user_model()
        testStudentUser = User2.objects.create_user(username="TestStudent", email="mst4k@virginia.edu",
                                                   password="password456")
        d = datetime(2023, 3, 28, 23, 55, 59, 342380)
        testReview = create_review(testTutorUser, testStudentUser, 5, "Great tutor!", d)
        self.assertEquals(5, testReview.rating)
    def test_Valid_Review_Datetime(self):
        User = get_user_model()
        testTutorUser = User.objects.create_user(username="TestTutor", email="mst3k@virginia.edu",
                                                 password="password123")
        User2 = get_user_model()
        testStudentUser = User2.objects.create_user(username="TestStudent", email="mst4k@virginia.edu",
                                                   password="password456")
        d = datetime(2023, 3, 28, 23, 55, 59, 342380)
        testReview = create_review(testTutorUser, testStudentUser, 5, "Great tutor!", d)
        self.assertEquals(d, testReview.created_at)

class FavoriteModelTests(TestCase):
    def test_Valid_Favorite_Student(self):
        tutor = create_tutor()
        student = create_student()
        favorite = Favorite(student=student, tutor=tutor)
        self.assertEquals(student, favorite.student)
    def test_Valid_Favorite_Tutor(self):
        tutor = create_tutor()
        student = create_student()
        favorite = Favorite(student=student, tutor=tutor)
        self.assertEquals(tutor, favorite.tutor)
class TutorSessionTests(TestCase) :
    def test_Valid_Session_Tutor(self):
        tutor = create_tutor()
        d1 = datetime(2023, 3, 28, 20, 55, 59, 342380)
        d2 = datetime(2023, 3, 28, 21, 55, 59, 342380)
        validSession = TutorSession(day = "Thursday", start_time=d1, end_time=d2, tutor =tutor)
        self.assertEquals(tutor, validSession.tutor)

    def test_Valid_Session_Day(self):
        tutor = create_tutor()
        d1 = datetime(2023, 3, 28, 20, 55, 59, 342380)
        d2 = datetime(2023, 3, 28, 21, 55, 59, 342380)
        validSession = TutorSession(day = "Thursday", start_time=d1, end_time=d2, tutor =tutor)
        self.assertEquals("Thursday", validSession.day)

    def test_Valid_Session_Times(self):
        tutor = create_tutor()
        d1 = datetime(2023, 3, 28, 20, 55, 59, 342380)
        d2 = datetime(2023, 3, 28, 21, 55, 59, 342380)
        validSession = TutorSession(day = "Thursday", start_time=d1, end_time=d2, tutor =tutor)
        self.assertEquals(d1, validSession.start_time)
        self.assertEquals(d2, validSession.end_time)

    def test_Invalid_Session_Day(self):
        tutor = create_tutor()
        d1 = datetime(2023, 3, 28, 20, 55, 59, 342380)
        d2 = datetime(2023, 3, 28, 21, 55, 59, 342380)
        validSession = TutorSession(day = "Thursda", start_time=d1, end_time=d2, tutor =tutor)
        self.assertEquals("Thursda", validSession.day)

def create_valid_tutor_session(tutor) :
    d1 = datetime(2023, 3, 28, 20, 55, 59, 342380)
    d2 = datetime(2023, 3, 28, 21, 55, 59, 342380)
    validSession = TutorSession(day="Thursday", start_time=d1, end_time=d2, tutor=tutor)
    return validSession

class TutorRequestTests(TestCase) :

    def test_Valid_Request_Tutor(self):
        student = create_student()
        tutor = create_tutor()
        session = create_valid_tutor_session(tutor)
        request = TutorRequest(tutor_session=session, student=student)
        self.assertEquals(tutor, request.tutor_session.tutor)

    def test_Valid_Request_Student(self):
        student = create_student()
        tutor = create_tutor()
        session = create_valid_tutor_session(tutor)
        request = TutorRequest(tutor_session=session, student=student)
        self.assertEquals(student, request.student)

    def test_Valid_Request_Not_Accepted(self):
        student = create_student()
        tutor = create_tutor()
        session = create_valid_tutor_session(tutor)
        request = TutorRequest(tutor_session=session, student=student)
        self.assertEquals(False, request.is_accepted)

    def test_Valid_Request_Accepted(self):
        student = create_student()
        tutor = create_tutor()
        session = create_valid_tutor_session(tutor)
        request = TutorRequest(tutor_session=session, student=student, is_accepted=True)
        self.assertEquals(True, request.is_accepted)

    def test_Valid_Request_Description(self):
        student = create_student()
        tutor = create_tutor()
        session = create_valid_tutor_session(tutor)
        request = TutorRequest(tutor_session=session, student=student, description="Testing!")
        self.assertEquals("Testing!", request.description)

    def test_Valid_Request_Status(self):
        student = create_student()
        tutor = create_tutor()
        session = create_valid_tutor_session(tutor)
        request = TutorRequest(tutor_session=session, student=student)
        self.assertEquals("Pending", request.status)


# View Tests
validStatusCodes = {200, 301, 302}
# https://www.youtube.com/watch?v=hA_VxnxCHbo
class TestView(TestCase):

    

    print("Testing views...")
    def test_index_view(self): # index view
        client = Client()

        response = client.get(reverse('index'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
    
    def test_login_view(self): # login view
        client = Client()

        response = client.get(reverse('login'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "login.html")
    
    def test_create_account_view(self): # create account view
        client = Client()
        global validStatusCodes

        response = client.get(reverse('createAccount'))
        
        if response.status_code in validStatusCodes:
            self.assertTemplateUsed(response, "createAccount.html")
        else:
            print("profile has status code:", response.status_code, "which is not valid")
            raise Exception(AssertionError)

# Template Tests

# URL Tests
# Used: https://www.youtube.com/watch?v=0MrgsYswT1c

class TestUrls(TestCase):

    def test_all_url_is_resolved(self):
       # databases = '__all__'


        newRequest = HttpRequest()
        newRequest.method = 'POST'
        User = get_user_model()
        user = User.objects.create_user(username="TestTutor", email="mst3k@virginia.edu", password="password123")
        user.save()

        newRequest.user = user
        

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
            "requests_page" : requests_page,
            "student_sessions_update" : student_sessions_update,    
            "requests_page_update" : requests_page_update,

        }
        
        urlWithID = [ 'student_sessions_update', "requests_page_update"]

    
        # without ID
        print("Testing Url's without ID arguments...")
        for urlName in urlDictionary:

            # differentiate between url with id and without id
            url = None

            if urlName not in urlWithID:
                url = reverse(urlName)
            else:
                continue

        
            try:
                
                self.assertEquals(resolve(url).func, urlDictionary[urlName])
                #print(resolve(url))
                
                print("\n" + urlName + PASS_MESSAGE)

            except: 
                print("\n" + urlName + FAIL_MESSAGE)

        print("Testing Url's with ID arguments")

        for urlName in urlWithID:
            url = reverse(urlDictionary[urlName], args = (0, ))

            try:
                self.assertEquals(resolve(url).func, urlDictionary[urlName])
                print("\n" + urlName + PASS_MESSAGE)

            except:
                print("\n" + urlName + FAIL_MESSAGE)


            
        



        



           
        

    
    

