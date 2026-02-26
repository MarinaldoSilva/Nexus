from django.contrib import admin
from .models import SharedLink

@admin.register(SharedLink)
class SharedLinkAdmin(admin.ModelAdmin):
    list_display = ["link", "file", "folder", "created_by", "created_at", "expired", "is_active"]
    search_fields = ["link", "file__name", "folder__name", "created_by__email"]
    list_filter = ["is_active", "created_at", "expired"]
    readonly_fields = ["link", "created_at"]
