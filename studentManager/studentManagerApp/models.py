from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class Administrateur(models.Model):
    choix_poste = [
        ('directeur', 'Directeur'),
        ('chef_departement', 'Chef de departememt'),
        ('vice_directeur', 'Vice directeur'),
        ('concepteur', 'Concepteur')
    ]
    administrateur_id= models.AutoField(primary_key=True)
    nom = models.CharField(max_length=20,null=False)
    prenom = models.CharField(max_length=20)
    poste = models.CharField(choices=choix_poste, default='concepteur')
    password = models.CharField(max_length=20,null=False)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['nom','password'],name="Constraint_of_unicity_name_password_administrateur") 
        ]
    def __str__(self):
        return f"{self.nom} {self.prenom} - {self.poste}"

class Enseignant(models.Model):
    enseignant_id=models.AutoField(primary_key=True)
    nom=models.CharField(max_length=20,null=False)
    prenom=models.CharField(max_length=20,null=True)
    password = models.CharField(max_length=20,null=False)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['nom','password'],name="Constraint_of_unicity_name_password_enseignant") 
        ]
    def __str__(self):
        return f"{self.nom} {self.prenom}"
    
class Etudiant(models.Model):
    etudiant_id=models.AutoField(primary_key=True)
    matricule=models.CharField(max_length=20,unique=True,null=False)
    nom=models.CharField(max_length=20,null=False)
    prenom=models.CharField(max_length=20,null=False)
    dateNaiss=models.DateField(null=False)
    password = models.CharField(max_length=20,null=False)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['nom','password'],name="Constraint_of_unicity_name_password_etudiant") 
        ]
    def __str__(self):
        return f"{self.nom} {self.prenom} - {self.matricule}"


class Matiere(models.Model):
    matiere_id = models.AutoField(primary_key=True)
    libelle = models.CharField(max_length=30, null= False)
    semestre = models.IntegerField(null= False , validators= [MinValueValidator(1), MaxValueValidator(2)])
    nbre_credit = models.IntegerField()
    enseignant_id = models.ForeignKey(Enseignant, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.libelle} - Semestre {self.semestre} - {self.enseignant_id.nom} {self.enseignant_id.prenom}"


class Evaluation(models.Model):
    choix_type = [
        ('controle_continu', 'CC'),
        ('session_normale', 'SN'),
    ]

    evaluation_id = models.AutoField(primary_key=True)
    type_evaluation = models.CharField(choices= choix_type, default='controle_continu')
    date_evaluation = models.DateField(auto_now_add=True)
    Matiere_id = models.ForeignKey(Matiere, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.type_evaluation} - {self.date_evaluation} - {self.Matiere_id.libelle}"


class Note(models.Model):
    etudiant_id = models.ForeignKey(Etudiant, on_delete= models.CASCADE)
    evaluation_id = models.ForeignKey(Evaluation, on_delete=models.CASCADE)
    notes = models.IntegerField(null= False, validators=[MinValueValidator(0), MaxValueValidator(20)])
    def __str__(self):
        return f"{self.etudiant_id.nom} {self.etudiant_id.prenom} - {self.evaluation_id.type_evaluation} - Note: {self.notes}"