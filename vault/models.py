from django.db import models
from uuid import uuid4
from core.models import TimeStampeModel
from django.conf import settings


def upload_patch(instance, filename):
    extensao = filename.split('.')[:-1]
    woner = instance.full_name(' ')[0]
    return f"uploads/{instance.woner.id}/{woner}/{uuid4()}.{extensao}"

class File(TimeStampeModel):
    woner = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="files",verbose_name="Dono")
    file = models.FileField('arquivo', upload_patch=upload_patch)
    name = models.CharField('Nome do arquivo',max_length=255)
    file_size = models.PositiveIntegerField("Bytes")
    types = models.CharField('Type', max_length=50)
    
    class Meta:
        verbose_name = "Arquivo",
        verbose_name_plural = "Arquivos"
        ordering = ["-created_at"]
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.name = self.file.name
            self.file_size = self.file_size
        super().save(*args, **kwargs)