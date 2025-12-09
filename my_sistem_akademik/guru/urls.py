from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('dashboard/', views.dashboard_guru, name='guru_dashboard'),
    path('absen/', views.absen_siswa, name='absen_siswa'),  # legacy
    path('absensi/', views.absen_index, name='absen_index'),
    path('absensi/<int:jadwal_id>/', views.absen_detail, name='absen_detail'),
    path('nilai/', views.input_nilai, name='input_nilai'),
    path('jadwal/', views.jadwal_guru, name='jadwal_guru'),
    path('input-nilai/<int:jadwal_id>/', views.input_nilai_detail, name='input_nilai_detail'),
    path('rekap-nilai/', views.rekap_nilai, name='rekap_nilai'),
    path('api/update-nilai/', views.update_nilai_ajax, name='update_nilai_ajax'),
    path('riwayat-absensi/', views.riwayat_absensi, name='riwayat_absensi'),
]