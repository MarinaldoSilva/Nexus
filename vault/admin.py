from django.contrib import admin
from .models import File


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ["owner", "name", "file_size", "types"]
    list_filter = ["owner", "name", "types"]
    search_fields = ["name", "owner","types"]
    
    readonly_fields = ["owner","name","file_size","types", "created_at","updated_at"]
