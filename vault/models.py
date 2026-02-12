import mimetypes
from uuid import uuid4

from django.conf import settings
from django.db import models

from core.models import TimestampedModel


def upload_path(instance, filename):
    extensao = filename.split(".")[-1]
    file_name = f"{uuid4()}.{extensao}"

    try:
        user_id = instance.owner.id
    except Exception:
        user_id = "user_unknown"
    return f"uploads/{user_id}/{file_name}"


class Folder(TimestampedModel):
    class Meta:
        verbose_name = "Pasta"
        verbose_name_plural = "Pastas"
        unique_together = ["parent", "name", "owner"]

    name = models.CharField("Nome da pasta", max_length=255)
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="pasta pai",
        related_name="subpastas",
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="folders"
    )

    def __str__(self):
        if self.parent:
            return f"{self.parent.name}/{self.name}"
        return self.name


class File(TimestampedModel):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="files",
        verbose_name="Dono",
    )
    folder = models.ForeignKey(
        Folder,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="files",
        verbose_name="Pasta",
    )
    file = models.FileField("arquivo", upload_to=upload_path)
    name = models.CharField(
        "Nome do arquivo", max_length=255, null=True, blank=True, editable=False
    )
    file_size = models.PositiveIntegerField(
        "Bytes", null=True, blank=True, editable=False
    )
    types = models.CharField(
        "Type", max_length=50, null=True, blank=True, editable=False
    )

    class Meta:
        verbose_name = ("Arquivo",)
        verbose_name_plural = "Arquivos"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id and self.file:
            self.name = self.file.name
            self.file_size = getattr(self.file, "size", len(self.file.read()))
            self.file.seek(0)

            tipo_arquivo, _ = mimetypes.guess_type(self.file.name)
            if tipo_arquivo:
                self.types = tipo_arquivo
            else:
                self.types = "tipo não localizado"
        super().save(*args, **kwargs)
