from django.urls import path
from vault.views import (
    FileListAPIView, 
    FileCreateAPIView, 
    FileUpdateAPIView, 
    FileDestroyAPIView,
    CompressFileAPIView,
)

urlpatterns = [
    path('listar/', FileListAPIView.as_view(), name="meus_arquivos"),
    path('criar/', FileCreateAPIView.as_view(), name="criar_arquivo"),
    path('atualizar/<uuid:pk>/', FileUpdateAPIView.as_view(), name="atualizar_arquivo"),
    path('deletar/<uuid:pk>/', FileDestroyAPIView.as_view(), name="deletar_arquivo"),
    path('comprimir/', CompressFileAPIView.as_view(), name="comprimir_arquivo"),
    
]