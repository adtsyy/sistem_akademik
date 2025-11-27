
from django.contrib import admin
from django.urls import path, include
from .views import login_view

urlpatterns = [
    path("admin/", admin.site.urls),

    path("", login_view, name="login"),

    path("siswa/", include("siswa.urls")),
    path("guru/", include("guru.urls")),
    path("laporan/", include("laporan.urls")),
    path("admin-app/", include("admin_app.urls")),
    path('accounts/', include('accounts.urls')),
]
