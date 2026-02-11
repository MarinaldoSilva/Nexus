from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Audit

@admin.register(Audit)
class AuditAdmin(admin.ModelAdmin):
    list_display = ('action', 'dono', 'content_type', 'object_id', 'ip_address', 'timestamp')
    
    list_filter = ('action', 'timestamp', 'content_type')
    search_fields = ('ip_address', 'object_id', 'dono__username', 'dono__email')
    readonly_fields = ('dono', 'content_type', 'object_id', 'content_object', 'action', 'cache_data', 'timestamp', 'ip_address')
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False