from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Etudiant,Note,Evaluation
@receiver(post_save, sender=Evaluation)
def create_notes(sender, instance, created, **kwargs):
    if created:
        students=Etudiant.objects.all()
        for student in students:
            Note.objects.create(etudiant_id=student,evaluation_id=instance)