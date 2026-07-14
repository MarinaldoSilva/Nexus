from django.contrib import admin

from vault.models import File, Folder


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ["name", "owner", "file_size", "file_type", "created_at"]

    search_fields = ["name", "owner", "file_type"]

    readonly_fields = [
        "owner",
        "name",
        "file_size",
        "file_type",
        "created_at",
        "updated_at",
    ]

    def save_model(self, request, obj, form, change):
        if not obj.owner_id:
            obj.owner = request.user
        super().save_model(request, obj, form, change)


@admin.register(Folder)
class FolderAdmin(admin.ModelAdmin):
    list_display = ["name", "owner", "parent", "created_at"]

    search_fields = ["name", "owner__username", "owner__email"]

    list_filter = ["created_at"]

    readonly_fields = ["owner", "created_at", "updated_at"]

    def save_model(self, request, obj, form, change):
        if not obj.owner_id:
            obj.owner = request.user
        super().save_model(request, obj, form, change)
