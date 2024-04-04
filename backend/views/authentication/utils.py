from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from django.conf import settings

def refresh_access_token(refresh_token):
    try:
        refresh_token = RefreshToken(refresh_token)
        access_token = refresh_token.access_token
        return access_token
    except TokenError as e:
        # Manejar el caso en que el refresh token sea inválido o haya expirado
        # Por ejemplo, puedes devolver un error al frontend
        return None

def agregar_cookies_jwt(response, credentials: RefreshToken):
    response.set_cookie(
        key=settings.CUSTOM_AUTH_ACCESS_COOKIE,
        value=credentials.access_token,
        max_age=settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"],
        secure=settings.CUSTOM_AUTH_COOKIE_SECURE,
        httponly=settings.CUSTOM_AUTH_COOKIE_HTTP_ONLY,
        samesite=settings.CUSTOM_AUTH_COOKIE_SAMESITE,
    )

    response.set_cookie(
        key=settings.CUSTOM_AUTH_REFRESH_COOKIE,
        value=credentials,
        max_age=settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"],
        secure=settings.CUSTOM_AUTH_COOKIE_SECURE,
        httponly=settings.CUSTOM_AUTH_COOKIE_HTTP_ONLY,
        samesite=settings.CUSTOM_AUTH_COOKIE_SAMESITE,
    )

    return response

def eliminar_cookies_jwt(response):
    response.delete_cookie(settings.CUSTOM_AUTH_ACCESS_COOKIE)
    response.delete_cookie(settings.CUSTOM_AUTH_REFRESH_COOKIE)
    return response