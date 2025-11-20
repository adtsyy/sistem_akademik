from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('', lambda request: redirect('/laporan/')),
    path('admin/', admin.site.urls),
    path('laporan/', include('laporan.urls')),
]
