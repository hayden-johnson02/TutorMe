# Create your views here.
import logging

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from tutorme.models import Profile

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
    return render(request, 'profile.html', {})

def create_account_view(request):
    if request.user.is_authenticated:
        return render(request, 'index.html', {})
    return render(request, 'createAccount.html', {})

def account_type_choice(request):
    logging.debug(request.POST)
    if 'options' in request.POST:
        if request.POST['options'] == 'tutor_choice':
            request.user.profile.is_tutor = 1
        else:
            request.user.profile.is_student = 1
        request.user.profile.save()
        return redirect('profile')
    else:
        # user must choose an option
        return render(request, 'createAccount.html',{'error_message': "You must choose an option."})
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


