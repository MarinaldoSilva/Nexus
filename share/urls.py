from django.urls import path, include
from rest_framework.routers import DefaultRouter
from share.views import SharedLinkViewSet

router = DefaultRouter()

router.register(r'files', SharedLinkViewSet, basename='Sharedlink')

urlpatterns = [
    path('', include(router.urls))
]

