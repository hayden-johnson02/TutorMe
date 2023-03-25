# Create your views here.
import logging

import requests
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render

from .forms import EditProfileForm, DynamicCourseForm, CreateSessionForm, ReviewForm
from .models import Profile, Course, TutorSession, Review

from django.db.models import Q

app_name = 'tutorme'


def index(request):
    if request.user.is_authenticated and not request.user.profile.is_tutor and not request.user.profile.is_student:
        return render(request, 'createAccount.html', {})
    return render(request, 'index.html', {})


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
    # https://learndjango.com/tutorials/django-search-tutorial
    if request.method == 'GET' and 'searchCourses' in request.GET:
        subject = request.GET.get("subject")
        number = request.GET.get("number")
        cn = request.GET.get("courseName")
        cn = cn.split(" ")
        course_name = ""
        for word in cn:
            course_name = course_name + word + "_"
        url = 'https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.' \
              'FieldFormula.IScript_ClassSearch?institution=UVA01&term=1238&page=1'
        url = url + '&subject=' + subject + '&catalog_nbr=' + number + '&keyword=' + course_name
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
    start = ''
    if request.method == 'POST' and 'createTutorSession' in request.POST:
        create_session_form = CreateSessionForm(request.POST)
        if create_session_form.is_valid():

            TutorSession.objects.create(day=request.POST.get('day'), start_time=request.POST.get('start_time'),
                                        end_time=request.POST.get('end_time'), tutor=request.user.profile)
    create_session_form = CreateSessionForm()
    tutor_sessions_list = TutorSession.objects.all().filter(tutor=request.user.profile)
    if request.method == 'POST' and 'deleteTutorSessions' in request.POST:
        for sess in tutor_sessions_list:
            if str(sess.id) in request.POST:
                TutorSession.objects.get(id=sess.id).delete()

    if not tutor_sessions_list:
        tutor_sessions_list = None

    form = EditProfileForm(instance=request.user.profile)
    return render(request, 'edit_profile.html', {'form': form, 'courses': courses, 'clist': clist,
                                                 'search_course_form': search_course_form,
                                                 'delete_course_form': delete_course_form,
                                                 'create_session_form': create_session_form,
                                                 'tutor_sessions_list': tutor_sessions_list,})


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
def tutor_list_old(request):
    if request.user.profile.is_student and request.method == 'GET' and 'searchTutors' in request.GET:
        subject = request.GET.get('subject')
        course_num = request.GET.get('number')
        first_name = request.GET.get('first_name')
        last_name = request.GET.get('last_name')
        course_name = request.GET.get('course_name')
        all_tutors = list(Profile.objects.filter(is_tutor=True))
        possible_tutors = all_tutors.copy()

        tutors_with_courses = []
        for course in Course.objects.all():
            tutors_with_courses.append(str(course.profile.id))
        for tutor in all_tutors:
            if str(tutor.id) not in tutors_with_courses:
                    if subject != '' or course_name != '' or course_num != '':
                        if Profile.objects.get(pk=tutor.id) in possible_tutors:
                            possible_tutors.remove(Profile.objects.get(pk=tutor.id))

        possible_ids1 = []
        if subject != '':
            for current_course in Course.objects.all():
                if str(current_course.subject).lower() == str(subject).lower():
                    possible_ids1.append(str(current_course.profile.id))
            for tutor in all_tutors:
                if str(tutor.id) not in possible_ids1 and Profile.objects.get(pk=tutor.id) in possible_tutors:
                    possible_tutors.remove(Profile.objects.get(pk=tutor.id))

        possible_ids2 = []
        if course_num != '':
            for current_course in Course.objects.all():
                if str(current_course.catalog_number) == str(course_num):
                    possible_ids2.append(str(current_course.profile.id))
            for tutor in all_tutors:
                if str(tutor.id) not in possible_ids2 and Profile.objects.get(pk=tutor.id) in possible_tutors:
                    possible_tutors.remove(Profile.objects.get(pk=tutor.id))

        possible_ids3 = []
        if course_name != '':
            for current_course in Course.objects.all():
                if str(course_name).lower() in str(current_course.course_name).lower():
                    possible_ids3.append(str(current_course.profile.id))
            for tutor in all_tutors:
                if str(tutor.id) not in possible_ids3 and Profile.objects.get(pk=tutor.id) in possible_tutors:
                    possible_tutors.remove(Profile.objects.get(pk=tutor.id))

        if first_name != '':
            for tutor in all_tutors:
                if str(tutor.first_name).lower() != str(first_name).lower():
                    if len(possible_tutors) != 0 and Profile.objects.get(pk=tutor.id) in possible_tutors:
                        possible_tutors.remove(Profile.objects.get(pk=tutor.id))

        if last_name != '':
            for tutor in all_tutors:
                if tutor.last_name.lower() != last_name.lower():
                    if len(possible_tutors) != 0 and Profile.objects.get(pk=tutor.id) in possible_tutors:
                        possible_tutors.remove(Profile.objects.get(pk=tutor.id))

        if len(possible_tutors) == 0:
            possible_tutors = None
        return render(request, 'view_tutors.html', {'tutor_list': possible_tutors, 'possible_ids': possible_ids1})
    return render(request, 'view_tutors.html', {'tutor_list': Profile.objects.filter(is_tutor=True)})

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

    possible_tutors = Profile.objects.filter(profile_filters).filter(course_filters).distinct()

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
        if request.method == 'POST':
            form = ReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.tutor = tutor.user
                review.reviewer = request.user
                review.save()
                return redirect('/view_tutors/' + str(tutor_id))
        else:
            form = ReviewForm()

        tutor_courses = Course.objects.filter(profile=tutor)
        tutor_sessions = TutorSession.objects.filter(tutor=tutor)
        reviews = Review.objects.filter(tutor=tutor.user)

        return render(request, 'view_tutor_profile.html', {'current_tutor': tutor,
                                                           'tutor_courses': tutor_courses,
                                                           'tutor_sessions': tutor_sessions,
                                                           'reviews': reviews,
                                                           'form': form})
    return render(request, 'index.html', {})
