from django.db import models
from uuid import uuid4


class TimeStampeModel(models.Model):
    
    class Meta:
        abstract = True
    
    id = models.UUIDField(
        default=uuid4,
        primary_key=True,
        unique=True,
        editable=False,
    )
    
    created_at = models.DateTimeField("criado em",auto_now_add=True)
    updated_at = models.DateTimeField("atualizado em",auto_now=True)
    
    
    