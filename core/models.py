from uuid import uuid4
from django.contrib.auth.models import AbstractUser
from django.db import models
from core.abstract_models import TimeStampeModel


class User(AbstractUser, TimeStampeModel):
        
    email = models.EmailField('Seu E-mail', unique=True)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
    
    def __str__(self):
        return f"Email: {self.email}"