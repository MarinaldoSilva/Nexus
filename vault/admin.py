from django.contrib import admin

from vault.models import File, Folder


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ["name", "owner", "file_size", "types", "created_at"]

    search_fields = ["name", "owner", "types"]

    readonly_fields = [
        "owner",
        "name",
        "file_size",
        "types",
        "created_at",
        "updated_at",
    ]


@admin.register(Folder)
class FolderAdmin(admin.ModelAdmin):
    list_display = ["name", "owner", "parent", "created_at"]

    search_fields = ["name", "owner__username", "owner__email"]

    list_filter = ["created_at"]

    readonly_fields = ["owner", "created_at", "updated_at"]
