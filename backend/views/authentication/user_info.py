from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import AccessToken

from django.conf import settings
from django.db.models import Q

from backend.serializers import UserSerializer
from backend.models import Rol
from backend.common.choices import Roles


class GoogleAuthApi(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        new_access_token = request.COOKIES.get(
            settings.CUSTOM_TEMPORAL_NEW_ACCESS_COOKIE, None
        )
        access_token = request.COOKIES.get(settings.CUSTOM_AUTH_ACCESS_COOKIE, None)
        # If the access token is expired, then use the new access token
        token = new_access_token if new_access_token is not None else access_token
        exp_time = AccessToken(token).get("exp") * 1000

        user = request.user
        response_data = {
                'user': UserSerializer(user).data,
                'roles': {
                    'es_docente': Rol.objects.filter(Q(rol=Roles.DOCENTE) | Q(rol=Roles.TITULAR_CATEDRA)).exists(),
                    'es_administrador': user.is_superuser,
                    'es_director_de_carrera': Rol.objects.filter(rol=Roles.DIRECTOR_CARRERA).exists(),
                    'es_secretario_academico': Rol.objects.filter(rol=Roles.SECRETARIO).exists()
                },
            }
        
        response = Response(
            data={"data": response_data, "expires_at": exp_time},
        )

        return response