from django.urls import path
from . import views

urlpatterns = [
    path('', views.siswa_list, name='siswa_list'),
    path('tambah/', views.siswa_tambah, name='siswa_tambah'),
    path('<int:id>/', views.siswa_detail, name='siswa_detail'),
    path('edit/<int:id>/', views.siswa_edit, name='siswa_edit'),
    path('hapus/<int:id>/', views.siswa_hapus, name='siswa_hapus'),
]