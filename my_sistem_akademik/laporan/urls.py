from django.urls import path
from . import views

urlpatterns = [
    path('', views.halaman_laporan, name='halaman_laporan'),
    path('rapor/', views.daftar_rapor, name='daftar_rapor'),
    path('spp/', views.daftar_spp, name='daftar_spp'),
    path('gaji/', views.daftar_gaji, name='daftar_gaji'),
]
