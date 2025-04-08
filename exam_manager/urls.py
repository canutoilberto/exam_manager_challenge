from django.contrib import admin
from django.urls import path
from apps.provas import api

urlpatterns = [
    path("admin/", admin.site.urls),
    # Endpoints da API
    path("api/", api.api.urls),
]
