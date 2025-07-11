from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import LoginForm
from .models import Etudiant,Enseignant,Administrateur,Matiere


def login_view(request):
    if request.method =='POST':
        form=LoginForm(request.POST)
        if form.is_valid():
            nom=form.cleaned_data['nom']
            password=form.cleaned_data['password']
            role=form.cleaned_data['role']
            if role == "etudiant":
                try:
                    id=Etudiant.objects.get(nom=nom,password=password).etudiant_id
                except Etudiant.DoesNotExist:
                        messages.error(request,"Les donneés que vous avez entré ne correspondent á aucun de nos étudiants")
                        return redirect('login-page')
            elif role == "enseignant":
                try:
                    id=Enseignant.objects.get(nom=nom,password=password).enseignant_id
                except Enseignant.DoesNotExist:
                        messages.error(request,"Les donneés que vous avez entré ne correspondent á aucun de nos enseigants")
                        return redirect('login-page')
            else:
                try:
                    id=Administrateur.objects.get(nom=nom,password=password).administrateur_id
                except Administrateur.DoesNotExist:
                        messages.error(request,"Les donneés que vous avez entré ne correspondent á aucun de nos administrateurs")
                        return redirect('login-page')               
            return redirect('home-page', id=id, role=role)
    else:
        form=LoginForm()
    return render(request,'studentManagerApp/log-in.html',{'form':form})

def home_page_view(request, id, role):
    nombre_etudiants = Etudiant.objects.count()
    nombre_matieres1 = len(Matiere.objects.filter(semestre=1))
    nombre_matieres2 = len(Matiere.objects.filter(semestre=2))
    nombre_enseignants = Enseignant.objects.count()
    statistics = { 'nombre_etudiants':nombre_etudiants,
                   'nombre_matieres1': nombre_matieres1,
                    'nombre_matieres2':nombre_matieres2, 
                    'nombre_enseignants':nombre_enseignants}
    if role == "etudiant":
        try:
            user=Etudiant.objects.get(etudiant_id=id)
        except Etudiant.DoesNotExist:
                messages.error(request,"Les donneés que vous avez entré ne correspondent á aucun de nos étudiants")
                return redirect('login-page')
    elif role == "enseignant":
        try:
            user=Enseignant.objects.get(enseignant_id=id)
        except Enseignant.DoesNotExist:
                messages.error(request,"Les donneés que vous avez entré ne correspondent á aucun de nos enseigants")
                return redirect('login-page')
    else:
        try:
            user=Administrateur.objects.get(administrateur_id=id)
        except Administrateur.DoesNotExist:
                messages.error(request,"Les donneés que vous avez entré ne correspondent á aucun de nos administrateurs")
                return redirect('login-page')
    return render(request,'studentManagerApp/home-page.html',{'user':user, 'role':role, 'id':id, 'statistics': statistics})
# Create your views here.
