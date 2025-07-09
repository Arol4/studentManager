from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import LoginForm
from .models import Etudiant,Enseignant,Administrateur


def login_view(request):
    if request.method =='POST':
        form=LoginForm(request.POST)
        if form.is_valid():
            nom=form.cleaned_data['nom']
            password=form.cleaned_data['password']
            role=form.cleaned_data['role']
            try:
                id=Etudiant.objects.get(nom=nom,password=password).etudiant_id
            except Etudiant.DoesNotExist:
                try:
                    id=Enseignant.objects.get(nom=nom,password=password).enseignant_id
                except Enseignant.DoesNotExist:
                    try:
                        id=Administrateur.objects.get(nom=nom,password=password).administrateur_id
                    except Administrateur.DoesNotExist:
                        messages.error(request,"Les donneés que vous avez entré ne correspondent á aucun de nos comptes")
                        return redirect('login-page')
            return redirect('home-page', id=id, role=role)
    else:
        form=LoginForm()
    return render(request,'studentManagerApp/log-in.html',{'form':form})

def home_page_view(request, id, role):
    user={'nom':"Berios",'role':role}
    return render(request,'studentManagerApp/home-page.html',{'user':user})
# Create your views here.
