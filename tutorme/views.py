# Create your views here.
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views import generic 
from django.views.generic import CreateView

from django.shortcuts import render

from django.contrib.auth import logout
from .models import Dummy


app_name = 'tutorme'

def index(request):
    return render(request, 'index.html', {})


def logout_view(request):
    logout(request)
    # Redirect to a success page.
    return render(request, 'index.html', {})

def login_view(request):
    return render(request, 'login.html', {})

def profile_view(request):
    return render(request, 'profile.html', {})

@login_required(login_url='/login/')
def profile_view(request):
    return render(request, 'profile.html', {})

class IndexView(generic.ListView):
    template_name = 'index.html'

    def get_queryset(self):

        return None

def student_view(request):
    return render(request, 'studentHomePage.html', {})
