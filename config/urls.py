from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from core.views import AccountInactiveView

urlpatterns = [
    path("admin/", admin.site.urls),
    # Login, Logout, Password Reset
    path("api/auth/", include("dj_rest_auth.urls")),
    # Sign U
    path("api/auth/register/", include("dj_rest_auth.registration.urls")),
    path("accounts/", include("allauth.urls")),
    path("account/inactive/", AccountInactiveView.as_view(), name="account_inactive"),
    path("api/core/", include("core.urls")),
    path("api/files/", include("vault.urls")),
    path("api/share/", include("share.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
