from django.urls import path

from core.views import UserListAPIView, UserUpdateAPIView

urlpatterns = [
    path("perfil/", UserListAPIView.as_view(), name="list-perfil"),
    path("perfil/editar/", UserUpdateAPIView.as_view(), name="editar-perfil"),
]
