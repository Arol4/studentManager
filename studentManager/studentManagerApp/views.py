from django.db.models import Prefetch
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt 
from datetime import date
import json
from .forms import LoginForm
from .models import Etudiant, Enseignant, Administrateur, Matiere, Evaluation, Note, SessionUtilisateur
import logging
import secrets
import datetime

logger = logging.getLogger('studentManagerApp')
def login_view(request):
    if request.method =='POST':
        form=LoginForm(request.POST)
        if form.is_valid():
            nom=form.cleaned_data['nom']
            password=form.cleaned_data['password']
            role=form.cleaned_data['role']
            error_message = "Erreur de nom d'utilisateur ou de mot de passe ou de rôle."
            if role == "etudiant":
                try:
                    utilisateur = Etudiant.objects.get(nom=nom,password=password)
                    id = utilisateur.etudiant_id
                    
                except Etudiant.DoesNotExist:
                        messages.error(request, error_message)
                        return redirect('login-page')
            elif role == "enseignant":
                try:
                    utilisateur = Enseignant.objects.get(nom=nom,password=password)
                    id = utilisateur.enseignant_id
                except Enseignant.DoesNotExist:
                        messages.error(request, error_message)
                        return redirect('login-page')
            else:
                try:
                    utilisateur= Administrateur.objects.get(nom=nom,password=password)
                    id = utilisateur.administrateur_id
                except Administrateur.DoesNotExist:
                        messages.error(request, error_message)
                        return redirect('login-page')
            token = secrets.token_urlsafe(50)
            date_expiration = datetime.datetime.now() + datetime.timedelta(days=settings.SESSION_DURATION)
            session = SessionUtilisateur(
                type_utilisateur = role,
                utilisateur_id = id,
                token_session = token,
                date_expiration = date_expiration,
                ip_address = request.META.get('REMOTE_ADDR'),
                user_agent = request.META.get('HTTP_USER_AGENT', '')
            )
            session.save()
            response = redirect('home-page')
            response.set_cookie(
                'session_token',
                token,
                expires=date_expiration,
                httponly=True,
                secure=True if request.is_secure() else False
            )
            logger.info(f"Connexion réussie de l'utilisateur {nom} ({role}).")                 
            return response
    elif request.role and request.utilisateur_id:
        return redirect('home-page')
    else:
        form=LoginForm()
    return render(request,'studentManagerApp/HTML/log-in.html',{'form':form})

def home_page_view(request):
    id = request.utilisateur_id
    role = request.role
    if role == "etudiant":
        try:
            user=Etudiant.objects.get(etudiant_id=id)
        except Etudiant.DoesNotExist:
                messages.error(request,"Les donneés que vous avez entré sont invalides")
                return redirect('login-page')
    elif role == "enseignant":
        try:
            user=Enseignant.objects.get(enseignant_id=id)
        except Enseignant.DoesNotExist:
                messages.error(request,"Les donneés que vous avez entré sont invalides")
                return redirect('login-page')
    elif role == "administrateur":
        try:
            user=Administrateur.objects.get(administrateur_id=id)
        except Administrateur.DoesNotExist:
                messages.error(request,"Les donneés que vous avez entré sont invalides")
                return redirect('login-page')
    else:
        messages.error(request,"Les donneés que vous avez entré sont invalides")
        return redirect('login-page')
    
    del(user.password)
    delattr(user, role + "_id")
    del(user._state)
    user.id = id
    user.role = role
    return render(request,'studentManagerApp/HTML/home-page.html',{'user':user})

def stats_page_view(request):
    id = request.utilisateur_id
    role = request.role
    if role == "etudiant":
        try:
            user=Etudiant.objects.get(etudiant_id=id)
        except Etudiant.DoesNotExist:
                messages.error(request,"Les donneés que vous avez entré sont invalides")
                return redirect('login-page')
    elif role == "enseignant":
        try:
            user=Enseignant.objects.get(enseignant_id=id)
        except Enseignant.DoesNotExist:
                messages.error(request,"Les donneés que vous avez entré sont invalides")
                return redirect('login-page')
    elif role == "administrateur":
        try:
            user=Administrateur.objects.get(administrateur_id=id)
        except Administrateur.DoesNotExist:
                messages.error(request,"Les donneés que vous avez entré sont invalides")
                return redirect('login-page')
    else:
        messages.error(request,"Les donneés que vous avez entré sont invalides")
        return redirect('login-page')   
    nombre_etudiants = Etudiant.objects.count()
    nombre_matieres1 = Matiere.objects.filter(semestre=1).count()
    nombre_matieres2 = Matiere.objects.filter(semestre=2).count()
    nombre_enseignants = Enseignant.objects.count()
    statistics = { 'nombre_etudiants':nombre_etudiants,
                   'nombre_matieres1': nombre_matieres1,
                    'nombre_matieres2':nombre_matieres2, 
                    'nombre_enseignants':nombre_enseignants}
    
    del(user.password)
    delattr(user, role + "_id")
    del(user._state)
    user.id = id
    user.role = role
    return render(request,'studentManagerApp/HTML/stats-page.html',{'user':user, 'statistics': statistics})
  
def edit_page_view(request):
    id = request.utilisateur_id
    role = request.role
    if role == "enseignant":
        try:
            user = Enseignant.objects.get(enseignant_id=id)
            matieres = Matiere.objects.filter(enseignant_id=user).order_by('matiere_id')
        except Enseignant.DoesNotExist:
            messages.error(request, "Les donneés que vous avez entré sont invalides")
            return redirect('login-page')      
    elif role == "administrateur":
        try:
            user = Administrateur.objects.get(administrateur_id=id)
            matieres = Matiere.objects.all().order_by('matiere_id')
        except Administrateur.DoesNotExist:
            messages.error(request, "Les donneés que vous avez entré sont invalides")
            return redirect('login-page')
    else:
        messages.error(request, "Veuillez vous connecter pour continuer.")
        return redirect('login-page')
    
    etudiants = Etudiant.objects.order_by('etudiant_id')
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
    del(user.password)
    delattr(user, role + "_id")
    del(user._state)
    user.id = id
    user.role = role
    return render(request, 'studentManagerApp/HTML/edit-page.html', {
        'user': user,
        'liste_des_matieres_enseignees': matieres,
        'etudiants': etudiants,
        'ccs': ccs,
        'sns': sns
    })

# Vue qui renvoie vers le tableau de note
def tableau_notes_view(request):
    id = request.utilisateur_id
    role = request.role
    if role == "etudiant":
        try:
            user = Etudiant.objects.get(etudiant_id=id)
        except Etudiant.DoesNotExist:
            messages.error(request, "Les donneés que vous avez entré sont invalides")
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
        variables= dict()
    elif role == "enseignant":
        try:
            user = Enseignant.objects.get(enseignant_id=id)
        except Enseignant.DoesNotExist:
            messages.error(request, "Les donneés que vous avez entré sont invalides")
            return redirect('login-page')
        matieres = Matiere.objects.filter(enseignant_id=user)
        # J'initialise un grands classeurs pour toutes les notes de CC des matières concernées et tous les étudiants
        ccs=[]
        etudiants = Etudiant.objects.all()
        # Je récupere les notes de tous les étudiants dans les matières concernées 
        for matiere in matieres:
            # J'initialise les listes contenant les notes de CC de tous les étudiants pour matière 
            notes_cc=[]
            # Je récupere ou cree les evaluations concernées
            eval_cc, _= Evaluation.objects.get_or_create(type_evaluation='CC', matiere_id = matiere)
            # Je récupere les notes de CC de chaque etudiant
            for etudiant in etudiants:
                # Je récupere les notes de CC de l'étudiant
                note,_ = Note.objects.get_or_create(etudiant_id=etudiant, evaluation_id=eval_cc)
                note_cc=note.note 
                # Je mets ces notes dans leurs listes respectives
                notes_cc.append(note_cc)
            # Je mets les listes de notes de CC dans le grand classeur
            ccs.append(notes_cc)
        # Je crée un dictionnaire contenant les notes de CC de tous les étudiants
        notes={'CC':ccs}
        variables= {'etudiants':etudiants}
    elif role == "administrateur":
        try:
            user = Administrateur.objects.get(administrateur_id=id)
        except Administrateur.DoesNotExist:
            messages.error(request, "Les donneés que vous avez entré sont invalides")
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
        variables= {'etudiants':etudiants}
    else:
        messages.error(request, "Les donneés que vous avez entré sont invalides")
        return redirect('login-page')
    del(user.password)
    delattr(user, role + "_id")
    del(user._state)
    user.id = id
    user.role = role
    variables.update({'user':user, 'notes':notes, 'matieres':matieres})
    return render(request, 'studentManagerApp/HTML/tableau-notes.html', variables)

@csrf_exempt
def enregistrer_notes_matiere(request):
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
            
            evaluation, created = Evaluation.objects.get_or_create(
                matiere_id=matiere,
                type_evaluation=type_evaluation,
                defaults={'date_evaluation': date.today()}
            )

            notes_existantes_qs = Note.objects.filter(evaluation_id=evaluation)
            map_notes_existantes = { note.etudiant_id_id: note.note for note in notes_existantes_qs }

            ids_etudiants = [int(k) for k in notes.keys()]
            etudiants_qs = Etudiant.objects.filter(etudiant_id__in=ids_etudiants).only('etudiant_id', 'nom')
            map_etudiants = { e.etudiant_id: e.nom for e in etudiants_qs }

            notes_to_upsert = []
            message = ''
            for etudiant_id_str, nouvelle_note in notes.items():
                etudiant_id = int(etudiant_id_str)
                nom_etudiant = map_etudiants.get(etudiant_id, f"ID {etudiant_id}")
                ancienne_note = map_notes_existantes.get(etudiant_id)
                if ancienne_note != nouvelle_note:
                    if ancienne_note is None:
                        logger.info(f"Ajout de la note: {nom_etudiant}, {matiere.libelle}, {type_evaluation} (note: {nouvelle_note})")
                        message +=  f"\nAjout: {nom_etudiant} (note: {nouvelle_note})"
                    elif nouvelle_note is None:
                        logger.info(f"Suppression de la note: {nom_etudiant}, {matiere.libelle}, {type_evaluation} (ancienne note: {ancienne_note})")
                        message += f"\nSuppression: {nom_etudiant} (ancienne note: {ancienne_note})"
                    else:
                        logger.info(f"Modification de la note: {nom_etudiant}, {matiere.libelle}, {type_evaluation} (ancienne note: {ancienne_note} => Nouvelle note: {nouvelle_note})")
                        message += f"\nModification: {nom_etudiant} ({ancienne_note} => {nouvelle_note})"
                    
                    note_obj = Note(
                        etudiant_id_id=etudiant_id,
                        evaluation_id=evaluation,
                        note = nouvelle_note
                    )
                    notes_to_upsert.append(note_obj)
            if notes_to_upsert:
                Note.objects.bulk_create(
                    notes_to_upsert,
                    update_conflicts=True,
                    unique_fields=['etudiant_id', 'evaluation_id'],
                    update_fields=['note']
                )
            if message:
                message = f"Actions ci-dessous sur les notes de {type_evaluation} de {matiere.libelle} enregistrées avec succès:" + message
            else:
                message = "Aucune modification n'a été détectée."
            return JsonResponse({'message': message})
        except Exception as e:
            logger.error(f"Erreur lors de l'enregistrement : {type(e).__name__} - {e}")
            return JsonResponse({'error': str(e)}, status=400)
    logger.warning(f"Requête avec méthode {request.method} non autorisée pour l'enregistrement des notes d'une matière.")
    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)

@csrf_exempt
def enregistrer_notes_etudiant(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            etudiant_id = int(data["etudiant_id"])
            type_evaluation = data["type_evaluation"]
            notes = data["notes"]
            
            try:
                etudiant = Etudiant.objects.get(etudiant_id=etudiant_id)
            except Etudiant.DoesNotExist:
                return JsonResponse({"error": "Etudiant non trouvé"}, status = 404)
            
            ids_matieres = [int(k) for k in notes.keys()]
            matieres_qs = Matiere.objects.filter(matiere_id__in=ids_matieres).only('matiere_id', 'libelle')
            map_matieres = { m.matiere_id: m.libelle for m in matieres_qs }
            matiere_id_to_new_note = {m_id: round(float(notes[str(m_id)]), 2) if notes[str(m_id)] else None for m_id in map_matieres.keys() }
            evaluations_to_upsert = [
                Evaluation(
                    matiere_id_id=int(matiere_id),
                    type_evaluation=type_evaluation,
                    date_evaluation=date.today()
                ) for matiere_id in map_matieres.keys()
            ]
            Evaluation.objects.bulk_create(
                evaluations_to_upsert,
                ignore_conflicts=True
            )
            evaluations_qs = Evaluation.objects.filter(
                matiere_id_id__in = map_matieres.keys(),
                type_evaluation=type_evaluation
            )
            map_evaluations = { e.matiere_id_id: e.evaluation_id for e in evaluations_qs}
            anciennes_notes = Note.objects.filter(etudiant_id_id = etudiant_id, evaluation_id_id__in=map_evaluations.values())
            matiere_id_to_old_note = {m_id: n.note for m_id, e_id in map_evaluations.items() for n in anciennes_notes if n.evaluation_id_id == e_id}
            notes_to_upsert = []
            message = ''
            for matiere_id, nouvelle_note in matiere_id_to_new_note.items():
                ancienne_note = matiere_id_to_old_note[matiere_id]
                if ancienne_note != nouvelle_note:
                    if ancienne_note == None:
                        logger.info(f"Ajout de la note: {etudiant.nom}, {map_matieres[matiere_id]}, {type_evaluation} (note: {nouvelle_note})")
                        message += f"\nAjout: {map_matieres[matiere_id]} (note: {nouvelle_note})"
                    elif nouvelle_note == None:
                        logger.info(f"Suppression de la note: {etudiant.nom}, {map_matieres[matiere_id]}, {type_evaluation} (ancienne note: {ancienne_note})")
                        message += f"\nSuppression: {map_matieres[matiere_id]} (ancienne note: {ancienne_note})"
                    else:
                        logger.info(f"Modification de la note: {etudiant.nom}, {map_matieres[matiere_id]}, {type_evaluation} (ancienne note: {ancienne_note} => Nouvelle note: {nouvelle_note})")
                        message += f"\nModification: {map_matieres[matiere_id]} ({ancienne_note} => {nouvelle_note})"

                    note_obj = Note(
                        etudiant_id_id=etudiant_id,
                        evaluation_id_id=map_evaluations[matiere_id],
                        note=nouvelle_note
                    )
                    notes_to_upsert.append(note_obj)
            if notes_to_upsert:
                Note.objects.bulk_create(
                    notes_to_upsert,
                    update_conflicts=True,
                    unique_fields=['etudiant_id', 'evaluation_id'],
                    update_fields=['note']
                )
            if message:
                message = f"Actions ci-dessous sur les notes de {type_evaluation} de {etudiant.nom} enregistrées avec succès:" + message
            else:
                message = "Aucune modification n'a été détectée."
            return JsonResponse({"message": message})
        except Exception as e:
            logger.error(f"Erreur lors de l'enregistrement: {type(e).__name__} - {e}")
            return JsonResponse({"error": str(e)}, status=400)
    logger.warning(f"Requête avec méthode {request.method} non autorisée pour l'enregistrement des notes d'un étudiant")
    return JsonResponse({"error": "Méthode non autorisée"}, status=405)

def profile_page_view(request):
    id = request.utilisateur_id
    role = request.role
    if role == "etudiant":
        try:
            user = Etudiant.objects.get(etudiant_id=id)
        except Etudiant.DoesNotExist:
            messages.error(request, "Les donneés que vous avez entré sont invalides")
            return redirect('login-page')
    elif role == "enseignant":
        try:
            user = Enseignant.objects.get(enseignant_id=id)
        except Enseignant.DoesNotExist:
            messages.error(request, "Les donneés que vous avez entré sont invalides")
            return redirect('login-page')
    elif role == "administrateur":
        try:
            user = Administrateur.objects.get(administrateur_id=id)
        except Administrateur.DoesNotExist:
            messages.error(request, "Les donneés que vous avez entré sont invalides")
            return redirect('login-page')
    else:
        messages.error(request, "Les donneés que vous avez entré sont invalides")
        return redirect('login-page')
    
    del(user.password)
    del(user._state)
    delattr(user, role + "_id")
    user.id = id
    user.role = role
    return render(request, 'studentManagerApp/HTML/profile-page.html', {'user': user})

def log_out_view(request):
    if 'session_token' in request.COOKIES:
        token = request.COOKIES['session_token']
        session_utilisateur = SessionUtilisateur.objects.get(token_session = token)
        logger.info(f"Déconnexion réussie de l'utilisateur {session_utilisateur.name} ({session_utilisateur.type_utilisateur}).") 
        SessionUtilisateur.objects.filter(token_session=token).delete()
    response = redirect('login-page')
    response.delete_cookie('session_token')
    response['Cache-Control'] = 'no-cache, no-store, must_revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response