from django.contrib import admin
from django.urls import path, include
from laporan.views import home  # <-- pastikan nama sesuai dengan views.py

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),  # halaman utama
    path('laporan/', include('laporan.urls')),
]
