from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from django.core.exceptions import ValidationError

from backend.common.mensajes_de_error import (
    MENSAJE_EMAIL_NO_PROPORCIONADO,
    MENSAJE_SUPERUSUARIO,
    MENSAJE_SUPERUSUARIO_ACTIVO,
    MENSAJE_SUPERUSUARIO_STAFF,
)


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValidationError({"email": MENSAJE_EMAIL_NO_PROPORCIONADO})

        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **kwargs):
        kwargs.setdefault("is_active", True)
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_superuser", True)
        if kwargs.get("is_active") is not True:
            raise ValidationError({"is_active": MENSAJE_SUPERUSUARIO_ACTIVO})
        if kwargs.get("is_staff") is not True:
            raise ValidationError({"is_staff": MENSAJE_SUPERUSUARIO_STAFF})
        if kwargs.get("is_superuser") is not True:
            raise ValidationError({"is_superuser": MENSAJE_SUPERUSUARIO})
        return self.create_user(email, password, **kwargs)


class Usuario(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}" 

    objects = UserManager()
