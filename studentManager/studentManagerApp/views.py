from django.shortcuts import render
from django.http import HttpResponse


def login_view(request):
    return render(request,'studentManagerApp/log-in.html')

# Create your views here.
