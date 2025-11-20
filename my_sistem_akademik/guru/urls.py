from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard_guru, name='guru_dashboard'),
    path('absen/', views.absen_siswa, name='absen_siswa'),
    path('nilai/', views.input_nilai, name='input_nilai'),
]