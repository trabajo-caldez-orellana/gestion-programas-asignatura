from rest_framework_simplejwt import authentication
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied
from rest_framework.authentication import CSRFCheck
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ErrorDetail

INVALID_TOKEN_MESSAGE = ErrorDetail("Invalid token.", code="INVALID_TOKEN_MESSAGE")
REFRESH_TOKEN_EXPIRED_MESSAGE = ErrorDetail(
    "Refresh token expired.", code="REFRESH_TOKEN_EXPIRED_MESSAGE"
)
NO_TOKEN_PROVIDED_MESSAGE = ErrorDetail(
    "No token was provided.", code="NO_TOKEN_PROVIDED_MESSAGE"
)

from django.conf import settings


class CustomJWTAuthentication(authentication.JWTAuthentication):
    def enforce_csrf(self, request):
        """
        Enforce CSRF validation.
        """

        def dummy_get_response(request):  # pragma: no cover
            return None

        check = CSRFCheck(dummy_get_response)
        # populates request.META['CSRF_COOKIE'], which is used in process_view()
        check.process_request(request)
        reason = check.process_view(request, None, (), {})
        if reason:
            raise PermissionDenied(f"CSRF Failed: {reason}")
        
    def authenticate(self, request):
        """
        Checks if the access token is valid. If the access token is valid, lets the user pass.
        If the access token is not valid, checks if the refresh token is valid.
        If the refresh token is valid, generates a new access token and lets the user pass.
        If the refresh token is not valid, raises a AuthenticationFailed exception.
        """
        self.enforce_csrf(request)

        if (
            IsAuthenticated
            not in getattr(request.resolver_match.func, "cls", []).permission_classes
        ):
            return None

        access_raw_token = request.COOKIES.get(settings.CUSTOM_AUTH_ACCESS_COOKIE, None)

        if access_raw_token is not None:
            try:
                validated_token = self.get_validated_token(access_raw_token)
                return self.get_user(validated_token), validated_token
            except InvalidToken:
                pass

        return self._authenticate_with_refresh(request)

    def _authenticate_with_refresh(self, request):
        refresh_raw_token = request.COOKIES.get(
            settings.CUSTOM_AUTH_REFRESH_COOKIE, None
        )

        if refresh_raw_token is None:
            raise AuthenticationFailed(NO_TOKEN_PROVIDED_MESSAGE)

        try:
            refresh_token = RefreshToken(refresh_raw_token)
            new_access_token = str(refresh_token.access_token)

            validated_token = self.get_validated_token(new_access_token)
            validated_user = self.get_user(validated_token)

            request.COOKIES[settings.CUSTOM_TEMPORAL_NEW_ACCESS_COOKIE] = (
                new_access_token
            )

            return validated_user, validated_token
        except TokenError:
            raise AuthenticationFailed(REFRESH_TOKEN_EXPIRED_MESSAGE)

class ReplaceRefreshedAccessTokenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):  # pragma: no cover
        response = self.get_response(request)
        new_access_token = request.COOKIES.get(
            settings.CUSTOM_TEMPORAL_NEW_ACCESS_COOKIE, None
        )

        if new_access_token is not None:
            response.set_cookie(
                key=settings.CUSTOM_AUTH_ACCESS_COOKIE,
                value=new_access_token,
                max_age=settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"],
                secure=settings.CUSTOM_AUTH_COOKIE_SECURE,
                httponly=settings.CUSTOM_AUTH_COOKIE_HTTP_ONLY,
                samesite=settings.CUSTOM_AUTH_COOKIE_SAMESITE,
            )

        return response
 