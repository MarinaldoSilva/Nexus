from uuid import uuid4

from django.conf import settings
from django.db import models

from vault.models import File, Folder


class SharedLink(models.Model):
    file = models.ForeignKey(
        File,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="shared_links_file",
    )

    folder = models.ForeignKey(
        Folder,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="shared_links_folder",
    )

    link = models.UUIDField(
        unique=True,
        default=uuid4,
        primary_key=True,
    )

    expired = models.DateTimeField()

    created_at = models.DateTimeField(auto_now_add=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="shared_links_created",
    )

    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        shared = (
            self.file.name
            if self.file
            else (self.folder.name if self.folder else "Aquivo não nomeado")
        )
        return f"Created_by: {self.created_by.email} - shered: {shared}"
