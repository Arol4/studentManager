from django.contrib import admin
from .models import Administrateur,Enseignant,Etudiant,Matiere,Evaluation,Note
admin.site.register(Administrateur)
admin.site.register(Enseignant)
admin.site.register(Etudiant)
admin.site.register(Matiere)
admin.site.register(Evaluation)
admin.site.register(Note)

# Register your models here.
