# Create your views here.
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views import generic 

from django.shortcuts import render

from django.contrib.auth import logout
from django.views.generic import CreateView

from .forms import StudentSignUpForm
from .models import User
from django import forms

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


def create_account_view(request):
    return render(request, 'createAccount.html', {})

#class create_student_view(CreateView):
#    model = User
#    form_class = createStudentForm
#    template_name = 'createStudent.html'


class CreateStudentView(generic.FormView):
    template_name = 'createStudent.html'
    form_class = StudentSignUpForm
    success_url = '/profile'

    def get_context_data(self, **kwargs):
        kwargs['is_student'] = True
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        form.is_student = True
        form.save()
        return super().form_valid(form)


def create_tutor_view(request):
    return render(request, 'createTutor.html', {})


class IndexView(generic.ListView):
    template_name = 'index.html'

    def get_queryset(self):

        return None
