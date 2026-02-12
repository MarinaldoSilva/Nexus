from django.contrib.auth.models import AbstractUser
from django.db import models

from core.abstract_models import TimestampedModel


class TypeChoicesUser(models.TextChoices):
    ADMIN = "Administrador", "Administrador"
    DEFAULT = "Default", "Default"


TYPE_USER_CHOICES = TypeChoicesUser.choices


class User(AbstractUser, TimestampedModel):
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    type_user = models.CharField(
        choices=TYPE_USER_CHOICES,
        default=TypeChoicesUser.DEFAULT,
        blank=True,
        null=True,
        max_length=50,
        help_text="Type_user",
    )
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    email = models.EmailField("Seu E-mail", unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return f"Email: {self.email}"
