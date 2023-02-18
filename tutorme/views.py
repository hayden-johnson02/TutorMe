# Create your views here.
from django.http import HttpResponse
from django.views import generic 

from django.shortcuts import render



app_name = 'tutorme'

def index(request):
    return render(request, 'index.html', {})

class IndexView(generic.ListView):
    template_name = 'index.html'

    def get_queryset(self):

        return None
