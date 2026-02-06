from django.urls import path, include
from rest_framework.routers import DefaultRouter
from vault.views import FileViewSet

router = DefaultRouter()
router.register(r'', FileViewSet, basename='file')

urlpatterns = [
    path('', include(router.urls)),
]