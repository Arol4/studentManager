from django.contrib import admin
from .models import Administrateur,Enseignant,Etudiant,Matiere,Evaluation,Note
class AdministrateurAdmin(admin.ModelAdmin):
    list_display=('nom','prenom','poste',)
    list_filter=('poste',)
    ordering=('poste','nom')

class EtudiantAdmin(admin.ModelAdmin):
    list_display=('matricule','nom','prenom',)
    ordering=('nom',)

class MatiereAdmin(admin.ModelAdmin):
    list_display=('libelle','semestre','nbre_credit','enseignant_id')
    list_filter=('semestre',)
    ordering=('semestre','libelle')

class NoteAdmin(admin.ModelAdmin):
    list_display=('etudiant_id','evaluation_id','note',)
    list_filter=('evaluation_id',)
    ordering=('evaluation_id','etudiant_id')

class EvaluationAdmin(admin.ModelAdmin):
    list_display=('matiere_id','type_evaluation',)
    list_filter=('type_evaluation',)
    ordering=('type_evaluation','matiere_id')
admin.site.register(Administrateur,AdministrateurAdmin)
admin.site.register(Enseignant)
admin.site.register(Etudiant, EtudiantAdmin)
admin.site.register(Matiere, MatiereAdmin)
admin.site.register(Evaluation, EvaluationAdmin)
admin.site.register(Note, NoteAdmin)

# Register your models here.
