from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework.serializers import Serializer, CharField
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.conf import settings

from backend.views.authentication.utils import eliminar_cookies_jwt


class LogoutAPI(APIView):
    class InputSerializer(Serializer):
        refresh = CharField()

    def get(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get(settings.CUSTOM_AUTH_REFRESH_COOKIE, None)
        request.data["refresh"] = refresh_token
        input_serializer = self.InputSerializer(data=request.data)

        response = Response({})
        if not input_serializer.is_valid():
            response = Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"errors": input_serializer.errors},
            )
        else:
            try:
                token = RefreshToken(refresh_token)
            except TokenError as e:
                response = Response(
                    status=status.HTTP_400_BAD_REQUEST, data={"token": "Token invalido"}
                )

        eliminar_cookies_jwt(response)

        return response
