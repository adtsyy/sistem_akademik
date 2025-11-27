from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),

    # Pegawai
    path("pegawai/", views.list_pegawai, name="list_pegawai"),
    path("pegawai/tambah/", views.tambah_pegawai, name="tambah_pegawai"),
    path("pegawai/edit/<int:id>/", views.edit_pegawai, name="edit_pegawai"),
    path("pegawai/hapus/<int:id>/", views.hapus_pegawai, name="hapus_pegawai"),

    # Jadwal
    path("jadwal/", views.list_jadwal, name="list_jadwal"),
    path("jadwal/tambah/", views.tambah_jadwal, name="tambah_jadwal"),
    path("jadwal/edit/<int:id>/", views.edit_jadwal, name="edit_jadwal"),
    path("jadwal/hapus/<int:id>/", views.hapus_jadwal, name="hapus_jadwal"),
]