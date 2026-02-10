from django.db import models
from uuid import uuid4
import mimetypes
from core.models import TimestampedModel
from django.conf import settings


def upload_path(instance, filename):
    extensao = filename.split('.')[-1]
    file_name = f"{uuid4()}.{extensao}"
    
    try:
        user_id = instance.owner.id
    except Exception as e:
        user_id = "user_unknown"
    return f"uploads/{user_id}/{file_name}"

class File(TimestampedModel):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="files",
        verbose_name="Dono"
    )
    file = models.FileField('arquivo', upload_to=upload_path)
    name = models.CharField('Nome do arquivo',max_length=255, null=True, blank=True, editable=False)
    file_size = models.PositiveIntegerField("Bytes", null=True, blank=True, editable=False)
    types = models.CharField('Type', max_length=50, null=True, blank=True, editable=False)
    
    class Meta:
        verbose_name = "Arquivo",
        verbose_name_plural = "Arquivos"
        ordering = ["-created_at"]
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.id and self.file:
            self.name = self.file.name
            self.file_size = getattr(self.file, 'size', len(self.file.read()))
            self.file.seek(0)
            
            tipo_arquivo, _ = mimetypes.guess_type(self.file.name)
            if tipo_arquivo:
                self.types = tipo_arquivo
            else:
                self.types = "tipo não localizado"
        super().save(*args, **kwargs)