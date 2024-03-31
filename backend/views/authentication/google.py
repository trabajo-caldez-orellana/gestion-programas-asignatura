from urllib.parse import urlencode
from rest_framework import serializers, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.conf import settings
from django.shortcuts import redirect
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.response import Response
from backend.mixins import PublicApiMixin, ApiErrorsMixin
from backend.utils import google_get_access_token, google_get_user_info, generate_tokens_for_user
from backend.models import Usuario
from backend.serializers import UserSerializer
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.views import TokenRefreshView

def refresh_access_token(refresh_token):
    try:
        refresh_token = RefreshToken(refresh_token)
        access_token = refresh_token.access_token
        return access_token
    except TokenError as e:
        # Manejar el caso en que el refresh token sea inválido o haya expirado
        # Por ejemplo, puedes devolver un error al frontend
        return None

class GoogleLoginApi(PublicApiMixin, ApiErrorsMixin, APIView):
    class InputSerializer(serializers.Serializer):
        code = serializers.CharField(required=False)
        error = serializers.CharField(required=False)

    def get(self, request, *args, **kwargs):
        input_serializer = self.InputSerializer(data=request.GET)
        input_serializer.is_valid(raise_exception=True)

        validated_data = input_serializer.validated_data

        code = validated_data.get('code')
        error = validated_data.get('error')

        login_url = f'{settings.BASE_FRONTEND_URL}/login'
    
        if error or not code:
            params = urlencode({'error': error})
            return redirect(f'{login_url}?{params}')

        redirect_uri = f'{settings.BASE_FRONTEND_URL}/inicio'
        access_token, refresh_token = google_get_access_token(code=code, redirect_uri=redirect_uri)

        user_data = google_get_user_info(access_token=access_token)

        try:
            user = Usuario.objects.get(email=user_data['email'])

            refresh_token = RefreshToken.for_user(user)
            access_token = refresh_token.access_token

            response_data = {
                'user': UserSerializer(user).data,
                'access_token': str(access_token),
                'refresh_token': str(refresh_token),
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Usuario.DoesNotExist:
            first_name = user_data.get('given_name', '')
            last_name = user_data.get('family_name', '')

            user = Usuario.objects.create(
                email=user_data['email'],
                first_name=first_name,
                last_name=last_name,
            )
         
            refresh_token = RefreshToken.for_user(user)
            access_token = refresh_token.access_token

            response_data = {
                'user': UserSerializer(user).data,
                'access_token': str(access_token),
                'refresh_token': str(refresh_token),
            }
            return Response(response_data, status=status.HTTP_200_OK)
        

class GoogleAuthApi(PublicApiMixin, ApiErrorsMixin, APIView):
    class InputSerializer(serializers.Serializer):
        code = serializers.CharField(required=False)
        error = serializers.CharField(required=False)


    authentication_classes = [JWTAuthentication]

    def get(self, request, *args, **kwargs):

        # import pdb; pdb.set_trace()

        user = request.user

        if request is not None and not isinstance(user, AnonymousUser):
            response_data = {
                'user': UserSerializer(user).data,
            }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            # Si el usuario no está autenticado, devuelve un 401 Unauthorized
             return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

