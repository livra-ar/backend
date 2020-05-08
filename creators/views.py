from rest_framework import views, mixins, permissions, exceptions
from rest_framework.response import Response
from rest_framework_mongoengine import viewsets
from rest_framework import parsers, renderers
import time
from django.http import Http404
from .serializers import *
from .models import Token, Creator
from .authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes, permission_classes,api_view
from django.contrib.auth.hashers import check_password, make_password
from rest_framework.authtoken.views import ObtainAuthToken

from rest_framework.response import Response

class CreatorAuthToken(ObtainAuthToken):
    serializer_class = AuthTokenSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        try:
            token = Token.objects.get(user=user)
        except Token.DoesNotExist:
            token = Token(user=user)
            token.save()

        return Response({
            'id': str(user.id),
            'name': user.name,
            'token': token.key
        })

class UserViewSet(mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    permission_classes = (permissions.AllowAny, )
    serializer_class = UserSerializer

    def get_queryset(self):
        return Creator.objects.all()
    def create(self, request, *args, **kwargs):
        request.data['email'] = request.data['email'].lower()
        request.data['password'] = make_password(request.data['password'])
        return super(UserViewSet, self).create(request, *args, **kwargs)

@api_view(['HEAD'])
@permission_classes([permissions.AllowAny])
def check_email(request, email, format=None):
    try:
        email = email.lower()
        creator = Creator.objects.get(email=email)
        return Response(email)
    except Creator.DoesNotExist:
        raise Http404

# class ObtainAuthToken(views.APIView):
#     throttle_classes = ()
#     permission_classes = ()
#     authentication_classes = (TokenAuthentication, )
#     # parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
#     # renderer_classes = (renderers.JSONRenderer,)
#     serializer_class = AuthTokenSerializer

#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#         token, created = Token.objects.get_or_create(user=user)
#         return Response({'token': token.key})


# obtain_auth_token = ObtainAuthToken.as_view()
