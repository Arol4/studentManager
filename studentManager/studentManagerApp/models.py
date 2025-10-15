from django.db import models
from datetime import date
from django.utils import timezone
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

class Enseignant(models.Model):
    enseignant_id=models.AutoField(primary_key=True)
    nom=models.CharField(max_length=20,null=False)
    prenom=models.CharField(max_length=20,blank=True,null=True)
    password = models.CharField(max_length=20,null=False)
    sexe = models.CharField(choices=[('m','Masculin'),('f','Féminin')],default='m')
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['nom','password'],name="Constraint_of_unicity_name_password_enseignant") 
        ]
    def __str__(self):
        sexe = 'Mr' if (self.sexe == 'm') else 'Mme'
        return f"{sexe} {self.nom}"
    
class Etudiant(models.Model):
    etudiant_id=models.AutoField(primary_key=True)
    matricule=models.CharField(max_length=20,unique=True,null=False)
    nom=models.CharField(max_length=30,null=False)
    prenom=models.CharField(max_length=30,null=False)
    dateNaiss=models.DateField(null=False)
    password = models.CharField(max_length=20,null=False)
    sexe = models.CharField(choices=[('m','Masculin'),('f','Féminin')],default='m')
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['nom','password'],name="Constraint_of_unicity_name_password_etudiant") 
        ]
    def __str__(self):
        return f"{self.matricule} - {self.nom} {self.prenom}"


class Matiere(models.Model):
    matiere_id = models.AutoField(primary_key=True)
    libelle = models.CharField(max_length=30, null= False)
    semestre = models.IntegerField(null= False , validators= [MinValueValidator(1), MaxValueValidator(2)])
    nbre_credit = models.IntegerField()
    enseignant_id = models.ForeignKey(Enseignant, on_delete=models.CASCADE)
    def __str__(self):
        sexe = 'Mr' if (self.enseignant_id.sexe == 'm') else 'Mme'
        return f"{self.libelle} - Semestre {self.semestre} - {sexe} {self.enseignant_id.nom}"


class Evaluation(models.Model):
    choix_type = [
        ('CC', 'CC'),
        ('SN', 'SN'),
    ]

    evaluation_id = models.AutoField(primary_key=True)
    type_evaluation = models.CharField(choices= choix_type, default='CC')
    date_evaluation = models.DateField(default=date.today)
    matiere_id = models.ForeignKey(Matiere, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.matiere_id.libelle} - {self.type_evaluation} - {self.date_evaluation}"
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['matiere_id','type_evaluation'],name="Constraint_of_unicity_matiere_type_evaluation_evaluation") 
        ]

class Note(models.Model):
    etudiant_id = models.ForeignKey(Etudiant, on_delete= models.CASCADE)
    evaluation_id = models.ForeignKey(Evaluation, on_delete=models.CASCADE)
    note = models.FloatField(null= True,blank=True, validators=[MinValueValidator(0), MaxValueValidator(20)])

class SessionUtilisateur(models.Model):
    TYPE_UTILISATEUR = (
        ('etudiant', 'Étudiant'),
        ('enseignant', 'Enseignant'),
        ('administrateur', 'Administrateur')
    )
    type_utilisateur = models.CharField(max_length=20, choices=TYPE_UTILISATEUR)
    utilisateur_id = models.PositiveIntegerField()
    token_session = models.CharField(max_length=100, unique=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_expiration = models.DateTimeField(default=timezone.now())
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null = True, blank = True)

    def save(self, *args, **kwargs):
        if self.date_expiration and timezone.is_naive(self.date_expiration):
            self.date_expiration = timezone.make_aware(self.date_expiration, timezone.get_current_timezone())
        super().save(*args, **kwargs)