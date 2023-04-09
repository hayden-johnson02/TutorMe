# Create your views here.
import logging
import datetime

import requests
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.timezone import make_aware

from .forms import EditProfileForm, DynamicCourseForm, CreateSessionForm, ReviewForm, DynamicSessionForm
from .models import Profile, Course, TutorRequest, TutorSession, Review, Favorite

from django.db.models import Q

app_name = 'tutorme'


def index(request):
    if request.user.is_authenticated and not request.user.profile.is_tutor and not request.user.profile.is_student:
        return render(request, 'createAccount.html', {})
    if request.user.is_authenticated and request.user.profile.is_student:
        favorites = Favorite.objects.all().filter(student=request.user.id)
    else:
        favorites = None

    return render(request, 'index.html', {'favorites': favorites})


def logout_view(request):
    logout(request)
    return redirect('index')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('profile')
    else:
        return render(request, 'login.html', {})


@login_required(login_url='/login/')
def profile_view(request):
    courses = Course.objects.filter(profile=request.user.profile)
    courses = courses.order_by('subject', 'catalog_number')
    if not courses:
        courses = None
    tutor_sessions = TutorSession.objects.filter(tutor=request.user.profile)
    if not tutor_sessions:
        tutor_sessions = None
    return render(request, 'profile.html', {'courses': courses, 'tutor_sessions': tutor_sessions})


# https://dev.to/earthcomfy/django-update-user-profile-33ho
# https://stackoverflow.com/questions/54438473/how-to-execute-file-py-on-html-button-press-using-django/54451774#54451774
@login_required(login_url='/login/')
def edit_profile_view(request):
    if request.method == 'POST' and 'editProfile' in request.POST:
        form = EditProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')

    clist = None
    search_course_form = None
    subject = ""
    number = ""
    course_name = ""
    # https://learndjango.com/tutorials/django-search-tutorial
    if request.method == 'GET' and 'searchCourses' in request.GET:
        subject = request.GET.get("subject").upper()
        number = request.GET.get("number")
        cn = request.GET.get("courseName")
        cn = cn.split(" ")
        course_name = ""
        for word in cn:
            course_name = course_name + word + "_"
        url = 'https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.' \
              'FieldFormula.IScript_ClassSearch?institution=UVA01&term=1238&page=1'
        url = url + '&subject=' + subject + '&catalog_nbr=' + number + '&keyword=' + course_name
        course_name = course_name.replace('_', ' ').rstrip()
        r = requests.get(url)
        clist = []
        for c in r.json():
            if (c['subject'] + " " + c['catalog_nbr'] + " " + c['descr']) not in clist:
                clist.append(c['subject'] + " " + c['catalog_nbr'] + " " + c['descr'])
        if clist:
            search_course_form = DynamicCourseForm(course_list=clist)

    if request.method == 'POST' and 'addCourses' in request.POST:
        clist = request.POST['addCourses'].replace('\'', '').replace('[', '').replace(']', '').split(', ')
        search_course_form = DynamicCourseForm(request.POST or None, course_list=clist)
        if search_course_form.is_valid():
            courses_to_add = search_course_form.cleaned_data.get('Select_Courses')
            for c in courses_to_add:
                data = c.split(" ")
                subj = data[0]
                course_num = data[1]
                course_name = ""
                for i in range(2, len(data)):
                    course_name = course_name + data[i] + " "
                course_name = course_name.rstrip(" ")
                user_already_has_course = Course.objects.filter(subject=subj, catalog_number=course_num,
                                                                course_name=course_name, profile=request.user.profile)
                if not user_already_has_course:
                    Course.objects.create(subject=subj, catalog_number=course_num,
                                          course_name=course_name, profile=request.user.profile)
            clist = None

    courses = Course.objects.filter(profile=request.user.profile)
    delete_course_form = None
    course_list = []
    if not courses:
        courses = None
    if courses:
        courses = courses.order_by('subject', 'catalog_number')
        for c in courses:
            course_list.append(c.subject + " " + str(c.catalog_number) + " " + c.course_name)
        delete_course_form = DynamicCourseForm(course_list=course_list)

    if request.method == 'POST' and 'removeCourses' in request.POST:
        delete_course_form = DynamicCourseForm(request.POST or None, course_list=course_list)
        if delete_course_form.is_valid():
            courses_to_delete = delete_course_form.cleaned_data.get('Select_Courses')
            for c in courses_to_delete:
                course_list.remove(c)
                data = c.split(" ")
                subj = data[0]
                course_num = data[1]
                course_name = ""
                for i in range(2, len(data)):
                    course_name = course_name + data[i] + " "
                course_name = course_name.rstrip(" ")
                Course.objects.filter(subject=subj, catalog_number=course_num, course_name=course_name,
                                      profile=request.user.profile).delete()
            if course_list:
                delete_course_form = DynamicCourseForm(course_list=course_list)
            else:
                delete_course_form = None

    # https://stackoverflow.com/questions/50547018/delete-object-with-form-in-django
    invalid_session_time = False
    if request.method == 'POST' and 'createTutorSession' in request.POST:
        create_session_form = CreateSessionForm(request.POST)
        if create_session_form.is_valid():
            TutorSession.objects.create(day=request.POST.get('day'), start_time=request.POST.get('start_time'),
                                        end_time=request.POST.get('end_time'), tutor=request.user.profile)
        else:
            invalid_session_time = True
    create_session_form = CreateSessionForm()
    tutor_sessions_list = TutorSession.objects.all().filter(tutor=request.user.profile)
    if request.method == 'POST' and 'deleteTutorSessions' in request.POST:
        for sess in tutor_sessions_list:
            if str(sess.id) in request.POST:
                TutorSession.objects.get(id=sess.id).delete()
        tutor_sessions_list = TutorSession.objects.all().filter(tutor=request.user.profile)
    if not tutor_sessions_list:
        tutor_sessions_list = None
    form = EditProfileForm(instance=request.user.profile)
    return render(request, 'edit_profile.html', {'form': form, 'courses': courses, 'clist': clist,
                                                 'search_course_form': search_course_form,
                                                 'searchSubject': subject,
                                                 'searchNumber': number,
                                                 'searchCourseName': course_name,
                                                 'delete_course_form': delete_course_form,
                                                 'create_session_form': create_session_form,
                                                 'tutor_sessions_list': tutor_sessions_list,
                                                 'invalid_session_time': invalid_session_time, })


def create_account_view(request):
    if request.user.is_authenticated:
        return render(request, 'index.html', {})
    return render(request, 'createAccount.html', {})


def account_type_choice(request):
    logging.debug(request.POST)
    if 'options' in request.POST:
        if request.POST['options'] == 'tutor_choice':
            request.user.profile.is_tutor = 1
            request.user.profile.is_student = 0
        else:
            request.user.profile.is_student = 1
            request.user.profile.is_tutor = 0
        request.user.profile.save()
        return redirect('profile')
    else:
        # user must choose an option
        return render(request, 'createAccount.html', {'error_message': "You must choose an option."})


@login_required(login_url='/login/')
def delete_profile_view(request):
    request.user.delete()
    logout(request)
    return redirect('index')


@login_required(login_url='/login/')
def tutor_list(request):
    if 'clearSearch' in request.GET or 'searchTutors' not in request.GET:
        keys = ['subject', 'course_number', 'first_name', 'last_name', 'course_name', 'min_rating']
        for key in keys:
            if key in request.session:
                del request.session[key]
    if request.user.profile.is_student and request.method == 'GET' and 'searchTutors' in request.GET:
        request.session['subject'] = request.GET.get('subject') if request.GET.get('subject') else ''
        request.session['course_number'] = request.GET.get('course_number') if request.GET.get('course_number') else ''
        request.session['first_name'] = request.GET.get('first_name') if request.GET.get('first_name') else ''
        request.session['last_name'] = request.GET.get('last_name') if request.GET.get('last_name') else ''
        request.session['course_name'] = request.GET.get('course_name') if request.GET.get('course_name') else ''
        request.session['min_rating'] = request.GET.get('min_rating') if request.GET.get('min_rating') else 0

    # Retrieve filter values from the session
    subject = request.session.get('subject', '')
    course_num = request.session.get('course_number', '')
    first_name = request.session.get('first_name', '')
    last_name = request.session.get('last_name', '')
    course_name = request.session.get('course_name', '')
    min_rating = request.session.get('min_rating', 0)

    # Filter by subject, course number, and course name
    course_filters = Q()
    if subject != '':
        course_filters &= Q(course__subject__iexact=subject)
    if course_num != '':
        course_filters &= Q(course__catalog_number=course_num)
    if course_name != '':
        course_filters &= Q(course__course_name__icontains=course_name)

    profile_filters = Q(is_tutor=True)
    if first_name != '':
        profile_filters &= Q(first_name__iexact=first_name)
    if last_name != '':
        profile_filters &= Q(last_name__iexact=last_name)

    possible_tutors = Profile.objects.filter(profile_filters).filter(course_filters).order_by('first_name').distinct()

    # Filter by rating
    for tutor in possible_tutors:
        if tutor.average_rating() < float(min_rating):
            possible_tutors = possible_tutors.exclude(pk=tutor.pk)

    print(f'rendering with filters: Subject={subject}, Course Number={course_num}, First Name={first_name}, Last Name={last_name}, Course Name={course_name} and Min Rating={min_rating}')
    return render(request, 'view_tutors.html', {
        'tutor_list': possible_tutors,
        'filter_subject': subject,
        'filter_course_number': course_num,
        'filter_first_name': first_name,
        'filter_last_name': last_name,
        'filter_course_name': course_name,
        'filter_min_rating': min_rating,
    })


@login_required(login_url='/login/')
def delete_review(request, review_id):
    review = Review.objects.get(pk=review_id)
    if request.user == review.reviewer:
        review.delete()
    return redirect('/view_tutors/' + str(review.tutor.profile.id))


@login_required(login_url='/login/')
def view_tutor(request, tutor_id):
    if request.user.profile.is_student:
        tutor = Profile.objects.get(pk=tutor_id)
        favorite = Favorite.objects.filter(tutor=tutor.user.profile, student=request.user.profile)
        if favorite:
            is_fav = True
        else:
            is_fav = False
        if request.method == 'POST': 
            if 'review' in request.POST:
                # submitting a review
                form = ReviewForm(request.POST)
                if form.is_valid():
                    review = form.save(commit=False)
                    review.tutor = tutor.user
                    review.reviewer = request.user
                    review.save()
                    return redirect('/view_tutors/' + str(tutor_id))
            if 'session_request' in request.POST and not TutorRequest.objects.filter(pk=request.POST.get('session_request')).exists():
                # session_request = session.id
                # submitting a session request
                comment = request.POST.get('comment')
                session = TutorSession.objects.get(pk=request.POST.get('session_request'))
                req = TutorRequest(tutor_session=session,
                                   student=request.user.profile,
                                   description=comment)
                req.save()
            if 'not_favorite' in request.POST and not is_fav:
                favorite = Favorite(student=request.user.profile, tutor=tutor.user.profile)
                favorite.save()
                is_fav = True
            elif 'favorite' in request.POST and is_fav:
                favorite = Favorite.objects.filter(tutor=tutor.user.profile, student=request.user.profile)
                favorite.delete()
                is_fav = False
        tutor_courses = Course.objects.filter(profile=tutor)
        tutor_courses = tutor_courses.order_by('subject', 'catalog_number')
        if not tutor_courses:
            tutor_courses = None
        tutor_sessions = TutorSession.objects.filter(tutor=tutor)
        if not tutor_sessions:
            tutor_sessions = None
        reviews = Review.objects.filter(tutor=tutor.user)
        if not reviews:
            reviews = None

        return render(request, 'view_tutor_profile.html', {'current_tutor': tutor,
                                                           'tutor_courses': tutor_courses,
                                                           'tutor_sessions': tutor_sessions,
                                                           'reviews': reviews,
                                                           'review_form': ReviewForm(),
                                                           'is_fav': is_fav,
                                                           'session_form': (TutorSession.objects.filter(tutor=tutor)),
                                                           'requested_sessions': [s.tutor_session for s in TutorRequest.objects.filter(student=request.user.profile).exclude(status='Approved').exclude(status='Denied')],
                                                           'approved_sessions': [s.tutor_session for s in TutorRequest.objects.filter(student=request.user.profile, status='Approved').exclude(status='Denied').exclude(status='Pending')],
                                                           'denied_sessions': [s.tutor_session for s in TutorRequest.objects.filter(student=request.user.profile, status='Denied').exclude(status='Approved').exclude(status='Pending')],
                                                           })
    return render(request, 'index.html', {})


@login_required(login_url='/login/')
def request_session(request, session_id):
    if request.user.profile.is_student:
        session = TutorSession.objects.get(pk=session_id)
        if 'submitSess' in request.POST and request.method == 'POST':
            form = DynamicSessionForm(request.POST or None, sessionID=session_id)
            if form.is_valid():
                date = request.POST.get('Select_Sess')
                datetime_object = datetime.datetime.strptime(date, '%Y-%m-%d')
                description = request.POST.get('comment')

                date = make_aware(datetime_object)
                new_request = TutorRequest(tutor_session=TutorSession.objects.get(pk=session_id),
                                           student=request.user.profile,
                                           description=description,
                                           date=date)
                new_request.save()
                return redirect('/view_tutors/' + str(session.tutor_id))
        form = DynamicSessionForm(sessionID=session_id)
        return render(request, 'request_session.html', {'session': session, 'form': form})
    return render(request, 'index.html', {})


@login_required(login_url='/login/')
def requests_page(request):
    if request.user.profile.is_tutor:
        tutor_sessions = TutorSession.objects.filter(tutor=request.user.profile)
        student_requests = []
        for session in tutor_sessions:
            for req in session.tutor_requests():
                student_requests.append(req)
        archive = False

        if request.method == 'GET' and 'Pending' in request.GET:
            for req in student_requests:
                if req.status != 'Pending':
                    student_requests.remove(req)

        if request.method == 'GET' and 'Approved' in request.GET:
            for req in student_requests:
                if req.status != 'Approved':
                    student_requests.remove(req)

        if request.method == 'GET' and 'Denied' in request.GET:
            for req in student_requests:
                if req.status != 'Denied':
                    student_requests.remove(req)

        if request.method == 'GET' and 'Archive' in request.GET:
            archive = True
            pass  # only old ones where dates have passed. Make sure when implementing this to
            # exclude old ones from all the others, including "all current"
        return render(request, 'requests_page.html', {'student_sessions': student_requests,
                                                      'archive': archive})
    return render(request, 'index.html', {})


@login_required(login_url='/login/')
def requests_page_update(request, request_id):
    try:
        tutor_request = get_object_or_404(TutorRequest, id=request_id)
        if request.method == 'POST':
            action = request.POST.get('action')
            if action == 'approve':
                tutor_request.status = 'Approved'
            elif action == 'deny':
                tutor_request.status = 'Denied'
            tutor_request.save()
    except:
        print('error')
    return requests_page(request) 


@login_required(login_url='/login/')
def student_sessions(request):
    if request.user.profile.is_student:
        archive = False
        student_requests = TutorRequest.objects.filter(student=request.user.profile)
        if request.method == 'GET' and 'Pending' in request.GET:
            student_requests = TutorRequest.objects.filter(student=request.user.profile).filter(status='Pending')
        if request.method == 'GET' and 'Approved' in request.GET:
            student_requests = TutorRequest.objects.filter(student=request.user.profile).filter(status='Approved')
        if request.method == 'GET' and 'Denied' in request.GET:
            student_requests = TutorRequest.objects.filter(student=request.user.profile).filter(status='Denied')
        if request.method == 'GET' and 'Archive' in request.GET:
            archive = True
            pass  # only old ones where dates have passed. Make sure when implementing this to
            # exclude old ones from all the others, including "all current"
        return render(request, 'student_sessions.html', {'student_sessions': student_requests, 'archive': archive})
    return render(request, 'index.html', {})


@login_required(login_url='/login/')
def student_sessions_update(request, request_id):
    try:
        tutor_request = get_object_or_404(TutorRequest, id=request_id)
        if request.method == 'POST':
            action = request.POST.get('action')
            if action == 'cancel':
                print('cancelling')
                tutor_request.delete()
    except:
        print('error')
    return student_sessions(request) 


@login_required(login_url='/login/')
def view_student(request, student_id):
    if request.user.profile.is_tutor:
        student = Profile.objects.get(pk=student_id)
        return render(request, 'view_student_profile.html', {'current_student': student})
    return render(request, 'index.html', {})