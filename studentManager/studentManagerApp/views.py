from django.shortcuts import render, redirect
from .forms import LoginForm


def login_view(request):
    if request.method =='POST':
        form=LoginForm(request.POST)
        if form.is_valid():
            email=form.cleaned_data['email']
            password=form.cleaned_data['password']
            role=form.cleaned_data['role']
            return redirect('home-page')
    else:
        form=LoginForm()
    return render(request,'studentManagerApp/log-in.html',{'form':form})

# Create your views here.
