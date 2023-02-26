# Create your views here.
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views import generic 

from django.shortcuts import render

from django.contrib.auth import logout


app_name = 'tutorme'


def index(request):
    if request.user.is_authenticated:
        if (request.user.profile.is_tutor == 0) & (request.user.profile.is_student == 0):
            return render(request, 'createAccount.html', {})
    return render(request, 'index.html', {})


def logout_view(request):
    logout(request)
    # Redirect to a success page.
    return render(request, 'index.html', {})


def login_view(request):
    return render(request, 'login.html', {})


@login_required(login_url='/login/')
def profile_view(request):
    return render(request, 'profile.html', {})

def create_account_view(request):
    if request.user.is_authenticated:
        if (request.user.profile.is_tutor == 1) or (request.user.profile.is_student == 1):
            return render(request, 'index.html', {})
    return render(request, 'createAccount.html', {})


def create_student_view(request):
    request.user.profile.is_student = 1
    request.user.profile.is_tutor = 0
    request.user.profile.save()
    return render(request, 'index.html', {})


def create_tutor_view(request):
    request.user.profile.is_tutor = 1
    request.user.profile.is_student = 0
    request.user.profile.save()
    return render(request, 'index.html', {})

@login_required(login_url='/login/')
def delete_profile_view(request):
    request.user.delete()
    logout(request)
    return render(request, 'index.html', {})