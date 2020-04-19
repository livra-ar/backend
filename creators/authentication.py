    

from rest_framework import status, exceptions
from rest_framework.authentication import get_authorization_header, BaseAuthentication

from .models import *


class TokenAuthentication(BaseAuthentication):

    model = None

    def get_model(self):
        return Token

    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != b'token':
            return None

        if len(auth) == 1:
            msg = 'Invalid token header. No credentials provided.'
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = 'Invalid token header. Token string should not contain spaces.'
            raise exceptions.AuthenticationFailed(msg)

        try:
            token = auth[1].decode()
        except UnicodeError:
            msg = 'Invalid token header. Token string should not contain invalid characters.'
            raise exceptions.AuthenticationFailed(msg)

        return self.authenticate_credentials(token)

    def authenticate_credentials(self, key):
        model = self.get_model()
        try:
            token = model.objects.get(key=key)
        except model.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid token.')

        return (token.user, token)

    def authenticate_header(self, request):
        return 'Token'



from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password

class CreatorAuthBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None):     
        # Check the username/password and return a user.
        try:
            user = Creator.objects.get(email=email)
            if check_password(password, user.password):
                return user
            return None
        except Creator.DoesNotExist:
            return None