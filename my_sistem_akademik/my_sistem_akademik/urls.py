from django.contrib import admin
from django.urls import path, include
from laporan.views import home  # <-- pastikan nama sesuai dengan views.py
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),  # halaman utama
    path('laporan/', include('laporan.urls')),
    path('login/', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('guru/', include('guru.urls')),
]
