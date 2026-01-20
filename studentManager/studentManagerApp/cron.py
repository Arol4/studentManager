from .models import SessionUtilisateur
import logging
import datetime
logger = logging.getLogger('studentManagerApp')
def monthly_cleanup():
    print(datetime.datetime.today().astimezone())
    logger.info("Suppression automatique mensuelle des sessions utilisateur expirées")
    sessions = SessionUtilisateur.objects.all()
    for session in sessions:
        if session.date_expiration < datetime.datetime.now(datetime.timezone.utc):
            logger.info(f"Suppression de la session de {session.type_utilisateur} {session.name}, commencée le {session.date_creation}), expirée le {session.date_expiration}")
            session.delete()