from django.db.models import Prefetch
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt 
from datetime import date
import json
from .forms import LoginForm
from .models import Etudiant, Enseignant, Administrateur, Matiere, Evaluation, Note


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
    
    del(user.password)
    delattr(user, role + "_id")
    del(user._state)
    user.id = id
    user.role = role
    return render(request,'studentManagerApp/home-page.html',{'user':user, 'statistics': statistics})

def edit_page_view(request, id, role):
    # Common setup
    etudiants = Etudiant.objects.order_by('etudiant_id')
    
    if role == "enseignant":
        try:
            user = Enseignant.objects.get(enseignant_id=id)
            matieres = Matiere.objects.filter(enseignant_id=user).order_by('matiere_id')
        except Enseignant.DoesNotExist:
            messages.error(request, "Les données ne correspondent à aucun enseignant")
            return redirect('login-page')
            
    elif role == "administrateur":
        try:
            user = Administrateur.objects.get(administrateur_id=id)
            matieres = Matiere.objects.all().order_by('matiere_id')
        except Administrateur.DoesNotExist:
            messages.error(request, "Les données ne correspondent à aucun administrateur")
            return redirect('login-page')
    else:
        messages.error(request, "Rôle incorrect")
        return redirect('login-page')

    # Prefetch evaluations and notes in optimized way
    evaluations = Evaluation.objects.filter(
        matiere_id__in=matieres,
        type_evaluation__in=['CC', 'SN']
    ).prefetch_related(
        Prefetch('note_set', 
                 queryset=Note.objects.filter(etudiant_id__in=etudiants),
        to_attr='prefetched_notes')
    )
    
    # Create evaluation mapping: {(matiere_id, type): evaluation}
    eval_map = {}
    for eval in evaluations:
        key = (eval.matiere_id_id, eval.type_evaluation)
        eval_map[key] = eval

    # Prepare note data structure: {eval_id: {etudiant_id: note}}
    note_data = {}
    for eval in evaluations:
        note_mapping = {}
        for note in eval.prefetched_notes:
            note_mapping[note.etudiant_id_id] = note.note
        note_data[eval.evaluation_id] = note_mapping

    # Build note matrices
    ccs = []
    sns = []
    for matiere in matieres:
        cc_notes = []
        sn_notes = []
        
        # Get evaluations for this matiere
        cc_eval = eval_map.get((matiere.matiere_id, 'CC'))
        sn_eval = eval_map.get((matiere.matiere_id, 'SN'))
        
        # Build note lists for students
        for etudiant in etudiants:
            # CC notes
            if cc_eval:
                cc_notes.append(note_data[cc_eval.evaluation_id].get(etudiant.etudiant_id))
            else:
                cc_notes.append(None)
                
            # SN notes
            if sn_eval:
                sn_notes.append(note_data[sn_eval.evaluation_id].get(etudiant.etudiant_id))
            else:
                sn_notes.append(None)
                
        ccs.append(cc_notes)
        sns.append(sn_notes)
    delattr(user, role + "_id")
    del(user._state)
    user.id = id
    user.role = role
    return render(request, 'studentManagerApp/edit-page.html', {
        'user': user,
        'liste_des_matieres_enseignees': matieres,
        'etudiants': etudiants,
        'ccs': ccs,
        'sns': sns
    })

# Vue qui renvoie vers le tableau de note
def tableau_notes_view(request, id, role):
    if role == "etudiant":
        try:
            user = Etudiant.objects.get(etudiant_id=id)
        except Etudiant.DoesNotExist:
            messages.error(request, "Les données ne correspondent à aucun étudiant")
            return redirect('login-page')
        matieres = Matiere.objects.all()
        # J'initialise les listes contenants les notes de CC et de SN de toutes les matières pour l'étudiant conserné
        notes_cc=[]
        notes_sn=[]
        # Je récupere les notes de CC et de SN pour chaque matiere pour l'étudiant conserné
        for matiere in matieres:
            # Je récupere ou cree les evaluations concernées
            evaluation_cc,_ = Evaluation.objects.get_or_create(matiere_id=matiere, type_evaluation='CC')
            evaluation_sn,_ = Evaluation.objects.get_or_create(matiere_id=matiere, type_evaluation='SN')
            # Je récupere les notes de CC et de SN de l'étudiant concerné
            note,_ = Note.objects.get_or_create(etudiant_id=user, evaluation_id=evaluation_cc)
            note_cc=note.note
            note,_ = Note.objects.get_or_create(etudiant_id=user, evaluation_id=evaluation_sn)
            note_sn=note.note            
            # Je mets les  notes de CC et SN dans leurs listes respectives
            notes_cc.append(note_cc)
            notes_sn.append(note_sn)
        # Je crée un dictionnaire contenant les notes de CC et de SN
        notes={'CC':notes_cc, 'SN':notes_sn}
        # Je prépare le dictionnaire contenant les variables á transmettre á la vue du tableau de note
        del(user.password)
        del(user._state)
        delattr(user, role + "_id")
        user.id = id
        user.role = role
        variables= {'user':user, 'notes':notes, 'matieres':matieres}
    elif role == "enseignant" or role == "administrateur":
        if role == "enseignant":
            try:
                user = Enseignant.objects.get(enseignant_id=id)
            except Enseignant.DoesNotExist:
                messages.error(request, "Les données ne correspondent à aucun enseignant")
                return redirect('login-page')
            matieres = Matiere.objects.filter(enseignant_id=user)
        else:
            try:
                user = Administrateur.objects.get(administrateur_id=id)
            except Administrateur.DoesNotExist:
                messages.error(request, "Les données ne correspondent à aucun administrateur")
                return redirect('login-page')
            matieres = Matiere.objects.all()
        # J'initialise 2 grands classeurs pour toutes les notes de CC et de SN des matières concernées et tous les étudiants
        ccs=[]
        sns=[]
        etudiants = Etudiant.objects.all()
        # Je récupere les notes de tous les étudiants dans les matières concernées 
        for matiere in matieres:
            # J'initialise les listes contenant les notes de CC et de SN de tous les étudiants pour matière 
            notes_cc=[]
            notes_sn=[]
            # Je récupere ou cree les evaluations concernées
            eval_cc, _= Evaluation.objects.get_or_create(type_evaluation='CC', matiere_id = matiere)
            eval_sn, _ = Evaluation.objects.get_or_create(type_evaluation='SN', matiere_id = matiere)
            # Je récupere les notes de CC et de SN de chaque etudiant
            for etudiant in etudiants:
                # Je récupere les notes de CC et de SN de l'étudiant
                note,_ = Note.objects.get_or_create(etudiant_id=etudiant, evaluation_id=eval_cc)
                note_cc=note.note
                note,_ = Note.objects.get_or_create(etudiant_id=etudiant, evaluation_id=eval_sn)
                note_sn=note.note  
                # Je mets ces notes dans leurs listes respectives
                notes_cc.append(note_cc)
                notes_sn.append(note_sn)
            # Je mets les listes de notes de CC et SN dans le grand classeur
            ccs.append(notes_cc)
            sns.append(notes_sn)
        # Je crée un dictionnaire contenant les notes de CC et de SN de tous les étudiants
        notes={'CC':ccs, 'SN':sns}
        # Je prépare le dictionnaire contenant les variables á transmettre á la vue du tableau de note
        del(user.password)
        delattr(user, role + "_id")
        del(user._state)
        user.id = id
        user.role = role
        variables= {'user':user, 'notes':notes, 'matieres':matieres, 'etudiants':etudiants}
    else:
        messages.error(request, "Rôle incorrect")
        return redirect('login-page')
    return render(request, 'studentManagerApp/tableau-notes.html', variables)

@csrf_exempt
def enregistrer_notes(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            matiere_id = int(data['matiere_id'])
            type_evaluation = data['type_evaluation']
            notes = data['notes']

            try:
                matiere = Matiere.objects.get(matiere_id=matiere_id)
            except Matiere.DoesNotExist:
                return JsonResponse({'error': 'Matière non trouvée'}, status=404)
            
            for etudiant_id, note in notes.items():
                try:
                    etudiant = Etudiant.objects.get(etudiant_id=etudiant_id)
                except Etudiant.DoesNotExist:
                    return JsonResponse({'error': f'Étudiant {etudiant_id} non trouvé'}, status=404)
                evaluation, created = Evaluation.objects.get_or_create(
                    matiere_id=matiere,
                    type_evaluation=type_evaluation,
                    defaults={'date_evaluation': date.today()}
                )
                Note.objects.update_or_create(
                    etudiant_id=etudiant,
                    evaluation_id=evaluation,
                    defaults={'note': note}
                )
            return JsonResponse({'message': 'Notes enregistrées avec succès'})
        except Exception as e:
            return JsonResponse({
                'error': str(e)
            }, status=400)
    
    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)

def profile_page_view(request, id, role):
    if role == "etudiant":
        try:
            user = Etudiant.objects.get(etudiant_id=id)
        except Etudiant.DoesNotExist:
            messages.error(request, "Les données ne correspondent à aucun étudiant")
            return redirect('login-page')
    elif role == "enseignant":
        try:
            user = Enseignant.objects.get(enseignant_id=id)
        except Enseignant.DoesNotExist:
            messages.error(request, "Les données ne correspondent à aucun enseignant")
            return redirect('login-page')
    elif role == "administrateur":
        try:
            user = Administrateur.objects.get(administrateur_id=id)
        except Administrateur.DoesNotExist:
            messages.error(request, "Les données ne correspondent à aucun administrateur")
            return redirect('login-page')
    else:
        messages.error(request, "Rôle incorrect")
        return redirect('login-page')
    
    del(user.password)
    del(user._state)
    delattr(user, role + "_id")
    user.id = id
    user.role = role
    return render(request, 'studentManagerApp/profile-page.html', {'user': user})