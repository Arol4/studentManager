from django.core.management.base import BaseCommand
from studentManagerApp.models import SessionUtilisateur
import logging
import datetime
logger = logging.getLogger('studentManagerApp')
loggerForCron = logging.getLogger('loggerForCron')
class Command(BaseCommand):
    help = "This command delete expired session and is suppose to be executed monthly."

    def handle(self, *args, **options):
        logger.info("Suppression automatique mensuelle des sessions utilisateur expirées")
        loggerForCron.info("---  Suppression automatique mensuelle des sessions utilisateur expirées  ---")
        sessions = SessionUtilisateur.objects.all()
        for session in sessions:
            if session.date_expiration < datetime.datetime.now(datetime.timezone.utc):
                loggerForCron.debug(f"Suppression de la session de {session.type_utilisateur} {session.name}, commencée le {session.date_creation}), expirée le {session.date_expiration}")
                session.delete()