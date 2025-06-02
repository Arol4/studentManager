from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Utilisateurs(models.Model):
    
    choix_role = [
        ('admin', 'Administrateur'),
        ('etudiant', 'Etudiant'),
        ('enseignant', 'Enseignant')
    ]
    utilisateur_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=20,null=False)
    password = models.CharField(max_length=20,null=False)
    role = models.CharField(choices=choix_role, default='etudiant')


class Admins(models.Model):
    choix_poste = [
        ('directeur', 'Directeur'),
        ('chef_departement', 'Chef de departememt'),
        ('vice_directeur', 'Vice directeur'),
        ('concepteur', 'Concepteur')
    ]
    admin_id= models.AutoField(primary_key=True)
    nom = models.CharField(max_length=20,null=False)
    prenom = models.CharField(max_length=20)
    poste = models.CharField(choices=choix_poste, default='concepteur')
    utilisateur_id = models.ForeignKey(Utilisateurs, on_delete=models.CASCADE)

class Enseignants(models.Model):
    enseignant_id=models.AutoField(primary_key=True)
    nom=models.CharField(max_length=20,null=False)
    prenom=models.CharField(max_length=20)
    utilisateur_id=models.ForeignKey(Utilisateurs,on_delete=models.CASCADE)
    
class Etudiants(models.Model):
    etudiant_id=models.AutoField(primary_key=True)
    matricule=models.CharField(max_length=20,unique=True,null=False)
    nom=models.CharField(max_length=20,null=False)
    prenom=models.CharField(max_length=20,null=False)
    dateNaiss=models.DateField(null=False)
    utilisateur_id=models.ForeignKey(Utilisateurs,on_delete=models.CASCADE)


class Matieres(models.Model):
    matiere_id = models.AutoField(primary_key=True)
    libelle = models.CharField(max_length=30, null= False)
    semestre = models.IntegerField(null= False , validators= [MinValueValidator(1), MaxValueValidator(2)])
    nbre_credit = models.IntegerField()
    enseignant_id = models.ForeignKey(Enseignants, on_delete=models.CASCADE)


class Evaluation(models.Model):
    choix_type = [
        ('controle_continu', 'CC'),
        ('session_normale', 'SN'),
    ]

    evaluation_id = models.AutoField(primary_key=True)
    type_evaluation = models.CharField(choices= choix_type, default='controle_continu')
    date_evaluation = models.DateField(auto_now_add=True)
    Matiere_id = models.ForeignKey(Matieres, on_delete=models.CASCADE)


class Notes(models.Model):
    etudiant_id = models.ForeignKey(Etudiants, on_delete= models.CASCADE)
    evaluation_id = models.ForeignKey(Evaluation, on_delete=models.CASCADE)
    notes = models.IntegerField(null= False, validators=[MinValueValidator(0), MaxValueValidator(20)])







