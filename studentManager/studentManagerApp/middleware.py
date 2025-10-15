from .models import SessionUtilisateur
from django.utils import timezone

class AuthMiddleware:
    def __init__(self, get_response):
       self.get_response = get_response

    def __call__(self, request):
        if 'session_token' in request.COOKIES:
            session_token = request.COOKIES['session_token']
            try:
                session = SessionUtilisateur.objects.get(token_session = session_token, date_expiration__gt = timezone.now())
                request.utilisateur_id = session.utilisateur_id
                request.role = session.type_utilisateur
            except (SessionUtilisateur.DoesNotExist):
                request.utilisateur_id = None
                request.role = None
        else:
            request.utilisateur_id = None
            request.role = None
        response = self.get_response(request) 
        return response