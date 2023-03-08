# Create your views here.
import logging

import requests
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import EditProfileForm, DynamicCourseForm
from .models import Profile, Course

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
        url = 'https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.' \
              'FieldFormula.IScript_ClassSearch?institution=UVA01&term=1238&page=1'
        url = url + '&subject=' + subject + '&catalog_nbr=' + number
        r = requests.get(url)
        clist = []
        for c in r.json():
            if (c['subject'] + " " + c['catalog_nbr']) not in clist:
                clist.append(c['subject'] + " " + c['catalog_nbr'])
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
                user_already_has_course = Course.objects.filter(subject=subj, catalog_number=course_num, profile=request.user.profile)
                if not user_already_has_course:
                    Course.objects.create(subject=subj, catalog_number=course_num, profile=request.user.profile)
            clist = None

    courses = Course.objects.filter(profile=request.user.profile)
    delete_course_form = None
    course_list = []
    if not courses:
        courses = None
    if courses:
        for c in courses:
            course_list.append(c.subject + " " + str(c.catalog_number))
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
                Course.objects.filter(subject=subj, catalog_number=course_num, profile=request.user.profile).delete()
            if course_list:
                delete_course_form = DynamicCourseForm(course_list=course_list)
            else:
                delete_course_form = None

    form = EditProfileForm(instance=request.user.profile)
    return render(request, 'edit_profile.html', {'form': form, 'courses': courses, 'clist': clist,
                                                 'search_course_form': search_course_form,
                                                 'delete_course_form': delete_course_form})


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
    if request.user.profile.is_student:
        context = {
            'tutor_list': Profile.objects.filter(is_tutor=True)
        }
        return render(request, 'view_tutors.html', context)
    else:
        return redirect('index')


@login_required(login_url='/login/')
def tutor_page(request, tutor_id):
    if request.user.profile.is_student:
        context = {
            'current_tutor': Profile.objects.get(pk=tutor_id)
        }
        return render(request, 'view_tutor_profile.html', context)
