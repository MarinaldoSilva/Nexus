from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    #Login, Logout, Password Reset
    path("api/auth/", include("dj_rest_auth.urls")),
    #Sign U
    path("api/auth/register/", include("dj_rest_auth.registration.urls")),
]
