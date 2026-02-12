from django.urls import include, path
from rest_framework.routers import DefaultRouter

from vault.views import FileViewSet, FolderViewSet

router = DefaultRouter()
router.register(r"folders", FolderViewSet, basename="folder")
router.register(r"", FileViewSet, basename="file")

urlpatterns = [
    path("", include(router.urls)),
]
