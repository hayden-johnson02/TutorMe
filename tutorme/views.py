# Create your views here.
import logging

import requests
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render

from .forms import EditProfileForm, DynamicCourseForm, CreateSessionForm
from .models import Profile, Course, TutorSession

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
    return render(request, 'profile.html', {'courses': courses})


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
    if request.method == 'POST' and 'createTutorSession' in request.POST:
        create_session_form = CreateSessionForm(request.POST)
        if create_session_form.is_valid():
            TutorSession.objects.create( day=request.POST.get('day'), start_time=request.POST.get('start_time'),
                                         end_time=request.POST.get('end_time'), tutor=request.user.profile)
    create_session_form = CreateSessionForm()

    tutor_sessions_list = TutorSession.objects.all().filter(tutor=request.user.profile)
    if request.method == 'POST' and 'deleteTutorSessions' in request.POST:
        # TODO: delete the sessions selected
        print("TESTING")
        print(request.POST)
        for sess in tutor_sessions_list:
            if str(sess.id) in request.POST:
                print("TESTING2")
                pass

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
def tutor_list(request):
    if request.user.profile.is_student and request.method == 'GET' and 'searchTutors' in request.GET:
        subject = request.GET.get('subject')
        course_num = request.GET.get('number')
        first_name = request.GET.get('first_name')
        last_name = request.GET.get('last_name')
        course_name = request.GET.get('course_name')
        possible_tutors = list(Profile.objects.filter(is_tutor=True))
        possible_ids = []

        if subject != '':
            for current_course in Course.objects.all():
                possible_ids.append(current_course.subject)
                if str(current_course.subject).lower() == str(subject).lower():
                    possible_ids.append(str(current_course.profile.id))
            for tutor in possible_tutors:
                if str(tutor.id) not in possible_ids:
                    possible_tutors.remove(Profile.objects.get(pk=tutor.id))

        possible_ids = []
        if course_num != '':
            for current_course in Course.objects.all():
                if str(current_course.catalog_number) == str(course_num):
                    possible_ids.append(current_course.profile.id)
            for tutor in possible_tutors:
                if tutor.id not in possible_ids:
                    possible_tutors.remove(Profile.objects.get(pk=tutor.id))

        possible_ids = []
        if course_name != '':
            for current_course in Course.objects.all():
                if str(course_name).lower() in str(current_course.course_name).lower():
                    possible_ids.append(current_course.profile.id)
            for tutor in possible_tutors:
                if tutor.id not in possible_ids:
                    possible_tutors.remove(Profile.objects.get(pk=tutor.id))

        if first_name != '':
            for tutor in possible_tutors:
                if str(tutor.first_name).lower() != str(first_name).lower():
                    if len(possible_tutors) != 0:
                        possible_tutors.remove(Profile.objects.get(pk=tutor.id))
        if last_name != '':
            for tutor in possible_tutors:
                if str(tutor.last_name).lower() != str(last_name).lower():
                    if len(possible_tutors) != 0:
                        possible_tutors.remove(Profile.objects.get(pk=tutor.id))
        if len(possible_tutors) == 0:
            possible_tutors = None
        return render(request, 'view_tutors.html', {'tutor_list': possible_tutors, 'possible_ids': possible_ids})
    return render(request, 'view_tutors.html', {'tutor_list': Profile.objects.filter(is_tutor=True)})

@login_required(login_url='/login/')
def tutor_page(request, tutor_id):
    if request.user.profile.is_student:
        tutor_courses = []
        for course in list(Course.objects.all()):
            if course.profile.id == tutor_id:
                course_string = course.subject + ' ' + str(course.catalog_number) + ' ' + course.course_name
                tutor_courses.append(course_string)
        context = {
            'current_tutor': Profile.objects.get(pk=tutor_id),
            'tutor_courses': tutor_courses
        }
        return render(request, 'view_tutor_profile.html', context)
