# Create your views here.
from django.http import HttpResponse
from django.views import generic 

from django.shortcuts import render

from django.contrib.auth import logout


app_name = 'tutorme'

def index(request):
    return render(request, 'index.html', {})


def logout_view(request):
    logout(request)
    # Redirect to a success page.
    return render(request, 'index.html', {})

def login_view(request):
    return render(request, 'login.html', {})

class IndexView(generic.ListView):
    template_name = 'index.html'

    def get_queryset(self):

        return None
