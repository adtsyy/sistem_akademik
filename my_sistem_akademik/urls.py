from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('laporan/', include('laporan.urls')),
    path('siswa/', include('siswa_app.urls')),
]
