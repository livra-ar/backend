from django.contrib.auth.backends import BaseBackend
from .models import Moderator
from django.contrib.auth.hashers import check_password
class ModeratorBackend(BaseBackend):

    def authenticate(self, request, email = None, password=None):
        try:
            moderator = Moderator.objects.get(email=email)
            if check_password(password, moderator.password):
                return moderator
        except Moderator.DoesNotExist:
            return None

        return None

    def get_user(user_id):
        try:
            return Moderator.objects.get(id=user_id)
        except Moderator.DoesNotExist:
            return None
