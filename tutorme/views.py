# Create your views here.
import logging

import requests
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404

from .forms import EditProfileForm
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
    if request.method == 'GET' and 'searchCourses' in request.GET: #https://learndjango.com/tutorials/django-search-tutorial
        subject = request.GET.get("subject")
        number = request.GET.get("number")
        url = 'https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=UVA01&term=1238&page=1'
        if subject is not None:
            url = url + '&subject=' + subject
        if number is not None:
            url = url + '&catalog_nbr=' + number
        r = requests.get(url)
        clist = []
        for c in r.json():
            if (c['subject'] + " " + c['catalog_nbr']) not in clist:
                clist.append(c['subject'] + " " + c['catalog_nbr'])
    if request.method == 'POST' and 'addCourses' in request.POST:
        # add courses based on sis api search call
        # use dynamic form maybe?
        print(request.POST)
        pass
    if request.method == 'POST' and 'removeCourses' in request.POST:
        # delete courses that are selected
        pass
    form = EditProfileForm(instance=request.user.profile)
    courses = Course.objects.filter(profile=request.user.profile)
    if not courses:
        courses = None
    return render(request, 'edit_profile.html', {'form': form, 'courses': courses, 'clist': clist})


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

