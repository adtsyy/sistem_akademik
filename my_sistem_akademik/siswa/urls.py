from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.siswa_dashboard, name='siswa_dashboard'),
    path('list/', views.siswa_list, name='siswa_list'),
    path('tambah/', views.siswa_tambah, name='siswa_tambah'),
    path('siswa/<str:nis>/', views.siswa_detail, name='siswa_detail'),
    path('siswa/<str:nis>/edit/', views.siswa_edit, name='siswa_edit'),
    path('siswa/<str:nis>/hapus/', views.siswa_hapus, name='siswa_hapus'),
]