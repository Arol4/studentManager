from django.contrib import admin
from .models import Utilisateurs,Admins,Enseignants,Etudiants,Matieres,Evaluation,Notes
admin.site.register(Utilisateurs)
admin.site.register(Admins)
admin.site.register(Enseignants)
admin.site.register(Etudiants)
admin.site.register(Matieres)
admin.site.register(Evaluation)
admin.site.register(Notes)

# Register your models here.
