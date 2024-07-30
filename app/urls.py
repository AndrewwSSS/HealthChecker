from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("main.urls", namespace="main")),
    path("api/", include("ajax.urls", namespace="api")),
    path("api/user/", include("user.urls", namespace="user")),
]
