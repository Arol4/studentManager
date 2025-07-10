from django.contrib import admin
from .models import Administrateur,Enseignant,Etudiant,Matiere,Evaluation,Note
admin.site.register(Administrateur)
admin.site.register(Enseignant)
admin.site.register(Etudiant)
admin.site.register(Matiere)
admin.site.register(Evaluation)
class NoteAdmin(admin.ModelAdmin):
    list_display=('etudiant_id','evaluation_id','note',)
    ordering=('evaluation_id','etudiant_id')
admin.site.register(Note, NoteAdmin)

# Register your models here.
