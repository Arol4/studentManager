from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Etudiant,Note,Evaluation,Matiere
@receiver(post_save, sender=Evaluation)
def create_notes(sender, instance, created, **kwargs):
    if created:
        students=Etudiant.objects.all()
        for student in students:
            Note.objects.create(etudiant_id=student,evaluation_id=instance)

@receiver(post_save, sender=Matiere)
def create_evaluations(sender, instance, created, **kwargs):
    if created:
        Evaluation.objects.create(type_evaluation='CC', matiere_id=instance)
        Evaluation.objects.create(type_evaluation='SN', matiere_id=instance)

@receiver(post_save, sender=Etudiant)
def create_note(sender, instance, created, **kwargs):
    if created:
        evaluations=Evaluation.objects.all()
        for evaluation in evaluations:
            Note.objects.create(etudiant_id=instance,evaluation_id=evaluation)