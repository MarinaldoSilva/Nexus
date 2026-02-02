from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from unfold.admin import ModelAdmin


@admin.register(User)
class CustomUser(UserAdmin):
    #Colunas que aparecem na lista
    list_display = ("email", "first_name", "last_name", "is_staff", "created_at", "updated_at")
    
    #Filtros na barra lateral
    list_filter = ("is_staff", "is_active", "created_at")
    
    #Campo de busca (Pesquisa por email ou nome)
    search_fields = ("email", "first_name", "last_name")
    
    #Ordenação padrão
    ordering = ("-created_at",)
    
    fieldsets = (
        (None, {
            "fields": ("email", "password")
            }
        ),
        ("Informações Pessoais", {
            "fields": ("first_name", "last_name")
            }
        ),
        ("Permissões", {
            "fields": (
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            ),
        }),
        ("Datas Importantes", {
            "fields": ("last_login", "date_joined", "created_at", "updated_at")
            }
        ),
    )
    
    readonly_fields = ("created_at", "updated_at", "last_login", "date_joined")