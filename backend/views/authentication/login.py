from urllib.parse import urlencode
import string
import random

from rest_framework import serializers, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from django.conf import settings
from django.shortcuts import redirect

from backend.mixins import PublicApiMixin, ApiErrorsMixin
from backend.utils import google_get_access_token, google_get_user_info
from backend.models import Usuario
from backend.views.authentication.utils import agregar_cookies_jwt


class GoogleLoginApi(PublicApiMixin, ApiErrorsMixin, APIView):
    class InputSerializer(serializers.Serializer):
        code = serializers.CharField(required=False)
        error = serializers.CharField(required=False)

    def generate_password(self):
        # Define the characters to use in the password
        characters = string.ascii_letters + string.digits + string.punctuation

        # Generate a random password by sampling from the characters
        password = "".join(random.choice(characters) for _ in range(12))

        return password

    def get(self, request, *args, **kwargs):
        input_serializer = self.InputSerializer(data=request.GET)
        input_serializer.is_valid(raise_exception=True)

        validated_data = input_serializer.validated_data

        code = validated_data.get("code")
        error = validated_data.get("error")

        login_url = f"{settings.BASE_FRONTEND_URL}/login"

        if error or not code:
            params = urlencode({"error": error})
            return redirect(f"{login_url}?{params}")

        redirect_uri = f"{settings.BASE_FRONTEND_URL}/login-loading"
        access_token = google_get_access_token(code=code, redirect_uri=redirect_uri)
        user_data = google_get_user_info(access_token=access_token)

        try:
            user = Usuario.objects.get(email=user_data["email"])
            refresh_token = RefreshToken.for_user(user)
        except Usuario.DoesNotExist:
            first_name = user_data.get("given_name", "")
            last_name = user_data.get("family_name", "")
            profile_picture = user_data.get("picture", "")
            user = Usuario.objects.create(
                email=user_data["email"],
                first_name=first_name,
                last_name=last_name,
                profile_picture=profile_picture,
            )
            user.set_password(self.generate_password())
            user.save()

            refresh_token = RefreshToken.for_user(user)

        response = Response({}, status=status.HTTP_200_OK)
        response = agregar_cookies_jwt(response, refresh_token)
        return response
